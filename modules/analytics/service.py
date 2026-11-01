from __future__ import annotations

from dataclasses import dataclass, field

from modules.circularity.scoring import CircularityScorer
from modules.product_data.models import Product


@dataclass
class _BrandAggregate:
    product_count: int = 0
    scores: list[float] = field(default_factory=list)
    carbon: list[float] = field(default_factory=list)


class AnalyticsService:
    def __init__(self, scorer: CircularityScorer | None = None) -> None:
        self.scorer = scorer or CircularityScorer()

    def get_brand_analytics(self, products: list[Product]) -> list[dict]:
        grouped: dict[str, _BrandAggregate] = {}
        for product in products:
            brand = grouped.setdefault(product.brand, _BrandAggregate())
            brand.product_count += 1
            assessment = self.scorer.calculate(product)
            if assessment.overall_score is not None:
                brand.scores.append(assessment.overall_score)
            if product.carbon_footprint is not None:
                brand.carbon.append(float(product.carbon_footprint))

        return [
            {
                "brand": name,
                "average_score": (
                    sum(values.scores) / len(values.scores)
                    if values.scores
                    else None
                ),
                "average_carbon": (
                    sum(values.carbon) / len(values.carbon)
                    if values.carbon
                    else None
                ),
                "product_count": values.product_count,
            }
            for name, values in sorted(grouped.items())
        ]
