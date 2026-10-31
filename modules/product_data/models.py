from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourceReference:
    source_id: int | None = None
    publisher: str | None = None
    url: str | None = None
    accessed_at: str | None = None
    notes: str | None = None

    @property
    def display_text(self) -> str:
        return self.publisher or self.notes or "No source supplied"


@dataclass(frozen=True)
class Indicator:
    product_id: str
    dimension: str
    name: str
    value: str | None
    source_reference: SourceReference

    @property
    def source(self) -> str:
        return self.source_reference.display_text


@dataclass
class Product:
    product_id: str
    name: str
    brand: str
    category: str
    release_year: int
    description: str
    is_demo: bool
    carbon_footprint: int | None
    score: float
    scores: dict[str, float] = field(default_factory=dict)
    indicators: dict[str, list[Indicator]] = field(default_factory=dict)
