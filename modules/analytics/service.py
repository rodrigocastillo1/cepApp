from __future__ import annotations

from dataclasses import dataclass, field

from modules.analytics.errors import InvalidAnalyticsInput
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

    @staticmethod
    def _validate_products(products: list[Product]) -> None:
        if not isinstance(products, list) or any(
            not isinstance(product, Product) for product in products
        ):
            raise InvalidAnalyticsInput(
                "Analytics methods require a list of Product instances."
            )

    def get_brand_analytics(self, products: list[Product]) -> list[dict]:
        self._validate_products(products)
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

    def get_product_dimension_analytics(self, products: list[Product]) -> list[dict]:
        self._validate_products(products)
        product_analytics = []
        for product in products:
            assessment = self.scorer.calculate(product)
            product_analytics.append(
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "category": product.category,
                    "dimensions": [
                        {
                            "name": component.dimension,
                            "score": component.score,
                        }
                        for component in assessment.components
                    ],
                }
            )
        return product_analytics

    def get_category_dimension_analytics(
        self,
        products: list[Product],
    ) -> list[dict]:
        self._validate_products(products)
        grouped: dict[str, dict] = {}
        for product in products:
            category = grouped.setdefault(
                product.category,
                {
                    "product_count": 0,
                    "dimensions": {
                        dimension: {"scores": [], "product_count": 0}
                        for dimension in self.scorer.methodology.dimensions
                    },
                },
            )
            category["product_count"] += 1
            assessment = self.scorer.calculate(product)
            for component in assessment.components:
                if component.score is not None:
                    dimension = category["dimensions"][component.dimension]
                    dimension["scores"].append(component.score)
                    dimension["product_count"] += 1

        return [
            {
                "category": name,
                "product_count": values["product_count"],
                "dimensions": [
                    {
                        "name": dimension,
                        "average_score": (
                            sum(dimension_data["scores"])
                            / len(dimension_data["scores"])
                            if dimension_data["scores"]
                            else None
                        ),
                        "product_count": dimension_data["product_count"],
                    }
                    for dimension, dimension_data in values["dimensions"].items()
                ],
            }
            for name, values in sorted(grouped.items())
        ]

    def get_indicator_analytics(self, products: list[Product]) -> list[dict]:
        self._validate_products(products)
        grouped: dict[tuple[str, str], list[dict]] = {}
        for product in products:
            for dimension in self.scorer.methodology.dimensions:
                for indicator in product.indicators.get(dimension, []):
                    normalized_value = self.scorer.normalize(indicator)
                    if normalized_value is None:
                        continue
                    grouped.setdefault((dimension, indicator.name), []).append(
                        {
                            "product_id": product.product_id,
                            "product_name": product.name,
                            "value": indicator.value,
                            "normalized_value": normalized_value,
                        }
                    )

        dimension_order = {
            dimension: index
            for index, dimension in enumerate(self.scorer.methodology.dimensions)
        }
        return [
            {
                "dimension": dimension,
                "name": name,
                "entries": values,
            }
            for (dimension, name), values in sorted(
                grouped.items(),
                key=lambda item: (
                    dimension_order[item[0][0]],
                    item[0][1].casefold(),
                ),
            )
        ]
