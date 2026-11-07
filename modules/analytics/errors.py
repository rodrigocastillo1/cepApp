"""Errors raised by the analytics subsystem."""


class AnalyticsError(RuntimeError):
    """Base error for analytics operations."""


class InvalidAnalyticsInput(AnalyticsError, ValueError):
    """Raised when analytics receives invalid product data."""
