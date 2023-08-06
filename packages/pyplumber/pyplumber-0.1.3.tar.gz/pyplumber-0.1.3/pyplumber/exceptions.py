__all__ = ["SerializationError", "DeserializationError", "FatalError"]


class SerializationError(Exception):
    """
    Exception raised when
    serialization fails.
    """

    pass


class DeserializationError(Exception):
    """
    Exception raised when
    deserialization fails.
    """

    pass


class FatalError(Exception):
    """
    General purpose exception.
    """

    pass
