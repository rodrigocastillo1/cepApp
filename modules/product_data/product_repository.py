from __future__ import annotations

import sqlite3
from pathlib import Path

from .database import connect_database, get_database_path
from .errors import ProductRepositoryError
from .models import Indicator, Product, SourceReference


class ProductRepository:
    def __init__(self, database_path: str | Path | None = None) -> None:
        self.database_path = str(get_database_path(database_path))

    def _connect(self) -> sqlite3.Connection:
        return connect_database(self.database_path)

    def list_products(self) -> list[Product]:
        try:
            with self._connect() as connection:
                rows = connection.execute(
                    "SELECT product_id FROM products ORDER BY brand, name"
                ).fetchall()
        except sqlite3.Error as error:
            raise ProductRepositoryError("Could not retrieve the product list.") from error
        products = []
        for row in rows:
            product = self.get_product_by_id(row["product_id"])
            if product is not None:
                products.append(product)
        return products

    def get_product_by_id(self, product_id: str) -> Product | None:
        try:
            with self._connect() as connection:
                product_row = connection.execute(
                    "SELECT * FROM products WHERE product_id = ?",
                    (product_id,),
                ).fetchone()
                if product_row is None:
                    return None

                indicator_rows = connection.execute(
                    """
                    SELECT
                        pi.dimension_name,
                        pi.indicator_name,
                        pi.indicator_value,
                        pi.source_text,
                        sr.source_id,
                        sr.publisher,
                        sr.url,
                        sr.accessed_at,
                        sr.notes
                    FROM product_indicators AS pi
                    LEFT JOIN source_references AS sr
                        ON sr.product_id = pi.product_id
                        AND sr.dimension_name = pi.dimension_name
                        AND sr.indicator_name = pi.indicator_name
                    WHERE pi.product_id = ?
                    ORDER BY pi.dimension_name, pi.sort_order, pi.indicator_name
                    """,
                    (product_id,),
                ).fetchall()
        except sqlite3.Error as error:
            raise ProductRepositoryError(
                f"Could not retrieve product {product_id!r}."
            ) from error

        indicators: dict[str, list[Indicator]] = {}

        for row in indicator_rows:
            source_reference = SourceReference(
                source_id=row["source_id"],
                publisher=row["publisher"] or row["source_text"],
                url=row["url"],
                accessed_at=row["accessed_at"],
                notes=row["notes"],
            )
            indicator = Indicator(
                product_id=product_row["product_id"],
                dimension=row["dimension_name"],
                name=row["indicator_name"],
                value=row["indicator_value"],
                source_reference=source_reference,
            )
            indicators.setdefault(row["dimension_name"], []).append(indicator)

        return Product(
            product_id=product_row["product_id"],
            name=product_row["name"],
            brand=product_row["brand"],
            category=product_row["category"],
            release_year=product_row["release_year"],
            description=product_row["description"],
            is_demo=bool(product_row["is_demo"]),
            carbon_footprint=product_row["carbon_footprint"],
            indicators=indicators,
        )

    def get_product_qr_svg(self, product_id: str) -> bytes | None:
        try:
            with self._connect() as connection:
                row = connection.execute(
                    "SELECT svg_data FROM product_qr_codes WHERE product_id = ?",
                    (product_id,),
                ).fetchone()
        except sqlite3.Error as error:
            raise ProductRepositoryError(
                f"Could not retrieve QR code for product {product_id!r}."
            ) from error

        return bytes(row["svg_data"]) if row is not None else None

    def search_products(self, query: str) -> list[Product]:
        normalized = query.strip()
        if not normalized:
            return []

        try:
            with self._connect() as connection:
                rows = connection.execute(
                    """
                    SELECT product_id FROM products
                    WHERE LOWER(product_id) LIKE ? OR LOWER(name) LIKE ? OR LOWER(brand) LIKE ?
                    ORDER BY brand, name
                    """,
                    (f"%{normalized.lower()}%", f"%{normalized.lower()}%", f"%{normalized.lower()}%"),
                ).fetchall()
        except sqlite3.Error as error:
            raise ProductRepositoryError("Could not search the product catalogue.") from error

        products = []
        for row in rows:
            product = self.get_product_by_id(row["product_id"])
            if product is not None:
                products.append(product)
        return products
