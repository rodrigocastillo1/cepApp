"""Errors raised by the circularity assessment subsystem."""


class CircularityError(RuntimeError):
    """Base error for circularity assessment operations."""


class InvalidMethodologyError(CircularityError, ValueError):
    """Raised when scoring methodology settings are invalid."""


class CircularityCalculationError(CircularityError):
    """Raised when assessment input cannot be processed."""
