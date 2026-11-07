"""Errors raised by the product-data subsystem."""


class ProductDataError(RuntimeError):
    """Base error for product-data operations."""


class DatabaseError(ProductDataError):
    """Raised when a database operation fails."""


class ProductRepositoryError(ProductDataError):
    """Raised when the repository cannot retrieve product data."""
