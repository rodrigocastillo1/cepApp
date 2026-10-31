from __future__ import annotations

import sqlite3
from pathlib import Path

from .demo_catalog import DEMO_PRODUCTS, DIMENSIONS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "catalogue.db"


def get_database_path(database_path: str | Path | None = None) -> Path:
    if database_path is None:
        return DEFAULT_DATABASE_PATH
    return Path(database_path)


def connect_database(database_path: str | Path | None = None) -> sqlite3.Connection:
    path = get_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: str | Path | None = None) -> Path:
    path = get_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with connect_database(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                brand TEXT NOT NULL,
                category TEXT NOT NULL,
                release_year INTEGER NOT NULL,
                description TEXT NOT NULL,
                is_demo INTEGER NOT NULL DEFAULT 1,
                carbon_footprint INTEGER,
                score REAL NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS product_scores (
                product_id TEXT NOT NULL,
                dimension_name TEXT NOT NULL,
                score REAL NOT NULL,
                PRIMARY KEY (product_id, dimension_name),
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS product_indicators (
                product_id TEXT NOT NULL,
                dimension_name TEXT NOT NULL,
                indicator_name TEXT NOT NULL,
                indicator_value TEXT,
                source_text TEXT,
                sort_order INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (product_id, dimension_name, indicator_name),
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS source_references (
                source_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                dimension_name TEXT NOT NULL,
                indicator_name TEXT NOT NULL,
                publisher TEXT,
                url TEXT,
                accessed_at TEXT,
                notes TEXT,
                UNIQUE (product_id, dimension_name, indicator_name),
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
            """
        )
        seed_demo_products(connection)

    return path


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
                    "INSERT OR REPLACE INTO product_scores (product_id, dimension_name, score) VALUES (?, ?, ?)",
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

    connection.commit()


def get_demo_product_ids() -> list[str]:
    return list(sorted(DEMO_PRODUCTS))
