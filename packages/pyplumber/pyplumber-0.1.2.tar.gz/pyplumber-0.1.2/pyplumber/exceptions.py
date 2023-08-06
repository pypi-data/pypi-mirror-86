__all__ = ["SerializationError", "DeserializationError", "FatalError"]


class SerializationError(Exception):
    pass


class DeserializationError(Exception):
    pass


class FatalError(Exception):
    pass