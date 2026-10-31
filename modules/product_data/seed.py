"""Load synthetic demo catalogue records into the SQLite database."""

import sqlite3

from app.demo_catalog import DEMO_PRODUCTS, DIMENSIONS


def seed_demo_products(connection: sqlite3.Connection) -> None:
    for product_id, product in sorted(DEMO_PRODUCTS.items()):
        connection.execute(
            """
            INSERT OR REPLACE INTO products (
                product_id, name, brand, category, release_year, description,
                is_demo, carbon_footprint, score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product["product_id"],
                product["name"],
                product["brand"],
                product["category"],
                int(product["release_year"]),
                product["description"],
                int(bool(product.get("demo", True))),
                (
                    int(product["carbon_footprint"])
                    if product.get("carbon_footprint") is not None
                    else None
                ),
                float(product["score"]),
            ),
        )

        for dimension in DIMENSIONS:
            score = product["scores"].get(dimension)
            if score is not None:
                connection.execute(
                    """
                    INSERT OR REPLACE INTO product_scores (
                        product_id, dimension_name, score
                    ) VALUES (?, ?, ?)
                    """,
                    (product_id, dimension, float(score)),
                )

            for index, indicator in enumerate(product.get("indicators", {}).get(dimension, [])):
                indicator_name = indicator.get("name")
                if not indicator_name:
                    continue

                source_text = indicator.get("source") or "No source supplied"
                connection.execute(
                    """
                    INSERT OR REPLACE INTO product_indicators (
                        product_id, dimension_name, indicator_name,
                        indicator_value, source_text, sort_order
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        product_id,
                        dimension,
                        indicator_name,
                        (
                            None
                            if indicator.get("value") in (None, "Unavailable")
                            else str(indicator["value"])
                        ),
                        source_text,
                        index,
                    ),
                )

                connection.execute(
                    """
                    INSERT OR REPLACE INTO source_references (
                        product_id, dimension_name, indicator_name,
                        publisher, url, accessed_at, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        product_id,
                        dimension,
                        indicator_name,
                        source_text,
                        None,
                        None,
                        "Synthetic data created for the demo catalogue.",
                    ),
                )
