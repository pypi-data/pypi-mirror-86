__all__ = ["Plumber"]

import string
import random
import networkx as nx
from copy import deepcopy
from functools import partial
from threading import Thread, Lock, Timer
from pyplumber.Sink import Sink
from pyplumber.Task import Task
from pyplumber.exceptions import FatalError


class Plumber:
    """
    Plumber define how Daemons and Tasks
    interact with each other, handling
    dependencies, the execution flow and
    monitoring for timeouts.
    """

    ALLOWED_WDT_ACTIONS = ["terminate", "restart", "warn"]

    def __init__(
        self,
        debug: bool = False,
        name: str = "",
        use_linux_watchdog: bool = False,
        *args,
        **kwargs
    ) -> None:
        self.__G = nx.DiGraph()
        self.__graphLock = Lock()
        self.__outputs = []
        self.__debug = debug
        self.__plumber = None
        self.__name = name if name != "" else "Plumber-{}".format(self._generateId())
        self.__running = True
        self.__out = {}
        self.__sink = Sink()

    def __repr__(self) -> str:
        return "<PyPlumber Plumber (name={})>".format(self.name)

    def __str__(self) -> str:
        return self.__repr__()

    def _generateId(self) -> str:
        return "".join(random.choice(string.ascii_letters) for x in range(10))

    def setDebug(self, val):
        self.__debug = val

    @property
    def name(self) -> str:
        return self.__name

    def log(self, msg: str) -> None:
        if self.__debug:
            print(msg)

    def add(
        self,
        cls,
        args: tuple = (),
        kwargs: dict = {},
        dependencies: list = [],
        output: bool = False,
        wdt_enabled: bool = False,
        wdt_action: str = "terminate",
        wdt_timeout: float = 24 * 3600,
    ):
        if wdt_action not in self.ALLOWED_WDT_ACTIONS:
            raise FatalError(
                "Watchdog action {} not in the following allowed actions: {}".format(
                    wdt_action, self.ALLOWED_WDT_ACTIONS
                )
            )
        obj = cls(*args, **kwargs)
        if not (issubclass(type(obj), Task)):
            self.log("Accepted objects must inherit from Task")
        self.__graphLock.acquire()
        if obj.name not in self.__G:
            kw = deepcopy(kwargs)
            kw["name"] = obj.name
            self.__G.add_node(
                obj.name,
                cls=cls,
                args=args,
                kwargs=kw,
                obj=obj,
                wdt_enabled=wdt_enabled,
                wdt_action=wdt_action,
                wdt_timeout=wdt_timeout,
                timer=None,
                timer_started=False,
                executed=False,
            )
        if len(dependencies) > 0:
            for dep in dependencies:
                try:
                    if dep.name not in self.__G:
                        raise FatalError(
                            "Dependencies for a Task must be added to the Plumber before the task itself"
                        )
                except AttributeError:
                    raise FatalError("Dependencies must be already built objects")
                self.__G.add_edge(dep.name, obj.name)
        if output:
            self.__outputs.append(obj.name)
        self.__graphLock.release()
        return obj

    def setup(self) -> None:
        self.__graphLock.acquire()
        for node in self.__G.nodes():
            self.__G.node[node]["obj"].setSink(self.__sink)
            self.__G.node[node]["obj"].setPlumber(self)
            self.__G.node[node]["obj"].setup()
        self.__graphLock.release()

    def start(self) -> None:
        self.__graphLock.acquire()
        for node in self.__G.nodes():
            self.__G.node[node]["obj"].start()
        self.__graphLock.release()

    def __wdtHandler(self, name: str) -> None:
        action = self.__G.node[name]["wdt_action"]
        if action == "restart":
            self.__graphLock.acquire()
            print("Node {} has triggered the watchdog, restarting...".format(name))
            self.__G.node[name]["obj"].kill()
            self.__G.node[name]["obj"] = self.__G.node[name]["cls"](
                *self.__G.node[name]["args"], **self.__G.node[name]["kwargs"]
            )
            self.__G.node[name]["obj"].start()
            self.__graphLock.release()
        elif action == "terminate":
            print(
                "Node {} has triggered the watchdog, will terminate everything soon".format(
                    name
                )
            )
            self.stop()
        elif action == "warn":
            print(
                "Node {} has triggered the watchdog! This is just a warning.".format(
                    name
                )
            )
        return

    def startTimer(self, name: str) -> None:
        self.__graphLock.acquire()
        if not self.__G.node[name]["timer_started"]:
            self.__G.node[name]["timer"] = Timer(
                interval=self.__G.node[name]["wdt_timeout"],
                function=self.__wdtHandler,
                args=(name,),
            )
            self.__G.node[name]["timer"].daemon = True
            self.__G.node[name]["timer"].start()
            self.__G.node[name]["timer_started"] = True
        self.__graphLock.release()

    def cancelTimer(self, name: str, pipeline: str = "") -> None:
        self.__graphLock.acquire()
        try:
            self.__G.node[name]["timer"].cancel()
            self.__G.node[name]["timer_started"] = False
        except AttributeError:
            print("Failed to cancel timer for node {}".format(name))
        self.__graphLock.release()

    def _appendToResult(self, node, result):
        self.__out[node] = result

    def clear(self):
        self.__graphLock.acquire()
        del self.__out
        self.__out = {}
        for node in self.__G.nodes:
            self.__G.node[node]["executed"] = False
        self.__graphLock.release()

    def forward(self, wait: bool = False) -> list:
        self.clear()
        for node in self.__outputs:
            self.log("--> Getting result from output node {}".format(node))
            thread = Thread(
                target=self.nodeResult,
                args=(node, True, partial(self._appendToResult, node)),
                daemon=True,
            )
            thread.start()
        while (
            wait
            and len(list(self.__out.keys())) < len(self.__outputs)
            and self.__running
        ):
            pass
        return self.__out

    def loop(self) -> None:
        while self.__running:
            yield self.forward(wait=True)

    def stop(self) -> None:
        self.__running = False
        for key in self.__G.nodes():
            self.__G.node[key]["obj"].kill()
        raise SystemExit

    def nodeResult(
        self, node: str, output: bool = False, callback: callable = None
    ) -> None:
        # Check if it's been executed this time
        self.__graphLock.acquire()
        if self.__G.node[node]["executed"]:
            return
        self.__graphLock.release()
        # Get predecessors
        preds = list(self.__G.predecessors(node))
        self.log("--> Node {} predecessors: {}".format(node, preds))
        # No predecessors means root
        if len(preds) > 0:
            # Iterate over predecessors
            self.log("--> Will iterate over predecessors now")
            for pred in preds:
                self.log(
                    "--> Predecessor {} has no data, will call for nodeResult".format(
                        pred
                    )
                )
                self.nodeResult(pred)
            self.log("--> Successfully executed dependencies for node {}".format(node))
        # Get data from node
        self.log("--> Starting timer for node {}".format(node))
        self.startTimer(node)
        success = False
        while not success and self.__running:
            try:
                data = self.__G.node[node]["obj"].execute()
                success = True
            except:
                self.__wdtHandler(node)
        self.log("--> Canceling timer for node {}".format(node))
        self.cancelTimer(node, self.name)
        self.log("--> No predecessors, data is {}".format(data))
        if output and callback:
            callback(data)
        self.__graphLock.acquire()
        self.__G.node[node]["executed"] = True
        self.__graphLock.release()
        return

    def print(self, file=None) -> None:
        try:
            import matplotlib.pyplot as plt

            nx.draw_networkx(self.__G, with_labels=True)
            if not file:
                plt.show()
            else:
                plt.savefig(file)
        except ImportError:
            print(
                'Plotting dependencies for pyPlumber are not installed on this environment. If you want to plot the dependency chart please install them with "pip install pyplumber[plot]"'
            )
