"""Versioned rules for the educational circularity scoring prototype."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class ScoringMethodology:
    version: str = "prototype-v1"
    dimensions: tuple[str, ...] = (
        "Material Inputs",
        "Design & Durability",
        "End-of-Life Recovery",
    )
    max_years_for_full_score: int = 7
    missing_values: frozenset[str] = frozenset(
        {"", "unavailable", "n/a", "na", "unknown", "not reported"}
    )
    binary_scores: Mapping[str, float] = field(
        default_factory=lambda: MappingProxyType(
            {
                "yes": 100.0,
                "available": 100.0,
                "no": 0.0,
            }
        )
    )
    supported_binary_indicators: frozenset[str] = frozenset(
        {
            "standard fasteners",
            "replaceable battery",
            "take-back program",
        }
    )
    supported_rating_indicators: frozenset[str] = frozenset(
        {"repairability index"}
    )
    supported_year_indicators: frozenset[str] = frozenset(
        {
            "spare-parts availability",
            "software support",
        }
    )
    missing_data_note: str = (
        "Only indicators with recognized values are averaged. "
        "Available dimensions receive equal weight in the overall score; "
        "missing or unsupported values are excluded, not treated as zero. "
        "Coverage shows how much data contributed."
    )

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("Methodology version must not be empty.")
        if not self.dimensions:
            raise ValueError("Methodology must define at least one dimension.")
        if self.max_years_for_full_score <= 0:
            raise ValueError("The year cap must be greater than zero.")
        if any(not 0 <= score <= 100 for score in self.binary_scores.values()):
            raise ValueError("Binary indicator scores must be between 0 and 100.")
        object.__setattr__(
            self,
            "binary_scores",
            MappingProxyType(dict(self.binary_scores)),
        )


DEFAULT_METHODOLOGY = ScoringMethodology()
