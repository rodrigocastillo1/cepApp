"""Provider-independent interface for product sustainability coaching."""

from abc import ABC, abstractmethod

from modules.circularity.scoring import CircularityAssessment
from modules.product_data.models import Product


class AIProviderError(RuntimeError):
    """Raised when an AI provider cannot generate a coach response."""


class AIProviderNotConfigured(AIProviderError):
    """Raised when the selected AI provider has no required credentials."""


class AIProvider(ABC):
    """Interface implemented by each supported AI service."""

    @abstractmethod
    def generate_answer(
        self,
        question: str,
        product: Product,
        assessment: CircularityAssessment,
    ) -> str:
        """Answer a question using the supplied product evidence."""
