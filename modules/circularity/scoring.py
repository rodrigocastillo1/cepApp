from __future__ import annotations

import re
from dataclasses import dataclass

from modules.circularity.errors import CircularityCalculationError
from modules.circularity.methodology import (
    DEFAULT_METHODOLOGY,
    ScoringMethodology,
)
from modules.product_data.models import Indicator, Product

_PERCENT_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)\s*%$")
_RATING_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)\s*/\s*10$")
_YEARS_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)\s+years?$")


@dataclass(frozen=True)
class ComponentScore:
    dimension: str
    score: float | None
    coverage: float
    used_indicators: tuple[str, ...]
    total_indicators: int


@dataclass(frozen=True)
class CircularityAssessment:
    product_id: str
    overall_score: float | None
    components: tuple[ComponentScore, ...]
    coverage: float
    methodology_version: str
    missing_data_note: str


class CircularityScorer:
    """Calculate an illustrative, project-defined score from product indicators."""

    def __init__(
        self,
        methodology: ScoringMethodology = DEFAULT_METHODOLOGY,
    ) -> None:
        self.methodology = methodology

    def calculate(self, product: Product) -> CircularityAssessment:
        if not isinstance(product, Product):
            raise CircularityCalculationError(
                "Circularity scoring requires a Product instance."
            )

        components = tuple(
            self.calculate_component(
                dimension,
                product.indicators.get(dimension, []),
            )
            for dimension in self.methodology.dimensions
        )
        available_scores = [
            component.score
            for component in components
            if component.score is not None
        ]
        overall_score = (
            sum(available_scores) / len(available_scores)
            if available_scores
            else None
        )

        return CircularityAssessment(
            product_id=product.product_id,
            overall_score=overall_score,
            components=components,
            coverage=len(available_scores) / len(self.methodology.dimensions),
            methodology_version=self.methodology.version,
            missing_data_note=self.methodology.missing_data_note,
        )

    def calculate_component(
        self,
        dimension: str,
        indicators: list[Indicator],
    ) -> ComponentScore:
        normalized = [
            (indicator.name, value)
            for indicator in indicators
            if (value := self.normalize(indicator)) is not None
        ]
        values = [value for _, value in normalized]
        score = sum(values) / len(values) if values else None

        return ComponentScore(
            dimension=dimension,
            score=score,
            coverage=len(normalized) / len(indicators) if indicators else 0.0,
            used_indicators=tuple(name for name, _ in normalized),
            total_indicators=len(indicators),
        )

    def normalize(self, indicator: Indicator) -> float | None:
        """Map supported example formats to 0–100; return None if unsupported."""
        if not isinstance(indicator, Indicator):
            raise CircularityCalculationError(
                "Indicator normalization requires an Indicator instance."
            )
        if indicator.value is None:
            return None

        value = indicator.value.strip().lower()
        if value in self.methodology.missing_values:
            return None
        indicator_name = indicator.name.strip().lower()
        if (
            indicator_name in self.methodology.supported_binary_indicators
            and value in self.methodology.binary_scores
        ):
            return self.methodology.binary_scores[value]

        match = _PERCENT_PATTERN.fullmatch(value)
        if match:
            percentage = float(match.group(1))
            return percentage if 0 <= percentage <= 100 else None

        match = (
            _RATING_PATTERN.fullmatch(value)
            if indicator_name in self.methodology.supported_rating_indicators
            else None
        )
        if match:
            rating = float(match.group(1))
            return rating * 10 if 0 <= rating <= 10 else None

        match = (
            _YEARS_PATTERN.fullmatch(value)
            if indicator_name in self.methodology.supported_year_indicators
            else None
        )
        if match:
            years = float(match.group(1))
            if years < 0:
                return None
            return min(years / self.methodology.max_years_for_full_score, 1.0) * 100

        return None
