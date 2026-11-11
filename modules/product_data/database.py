from __future__ import annotations

import sqlite3
from pathlib import Path

from .errors import DatabaseError
from .seed import seed_demo_products

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "catalogue.db"


def get_database_path(database_path: str | Path | None = None) -> Path:
    if database_path is None:
        return DEFAULT_DATABASE_PATH
    return Path(database_path)


def connect_database(database_path: str | Path | None = None) -> sqlite3.Connection:
    path = get_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        connection = sqlite3.connect(str(path))
    except sqlite3.Error as error:
        raise DatabaseError(f"Could not connect to SQLite database: {path}") from error
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: str | Path | None = None) -> Path:
    path = get_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
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
                    carbon_footprint INTEGER
                )
                """
            )
            _remove_legacy_score_storage(connection)
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
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS product_qr_codes (
                    product_id TEXT PRIMARY KEY,
                    svg_data BLOB NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                )
                """
            )
            seed_demo_products(connection)
    except sqlite3.Error as error:
        raise DatabaseError(
            f"Could not initialize SQLite database: {path}"
        ) from error

    return path


def _remove_legacy_score_storage(connection: sqlite3.Connection) -> None:
    product_columns = {
        row["name"] for row in connection.execute("PRAGMA table_info(products)")
    }
    if "score" in product_columns:
        connection.execute("PRAGMA foreign_keys = OFF")
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                CREATE TABLE products_without_scores (
                    product_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    category TEXT NOT NULL,
                    release_year INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    is_demo INTEGER NOT NULL DEFAULT 1,
                    carbon_footprint INTEGER
                )
                """
            )
            connection.execute(
                """
                INSERT INTO products_without_scores (
                    product_id, name, brand, category, release_year,
                    description, is_demo, carbon_footprint
                )
                SELECT product_id, name, brand, category, release_year,
                       description, is_demo, carbon_footprint
                FROM products
                """
            )
            connection.execute("DROP TABLE IF EXISTS product_scores")
            connection.execute("DROP TABLE products")
            connection.execute(
                "ALTER TABLE products_without_scores RENAME TO products"
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.execute("PRAGMA foreign_keys = ON")
    else:
        connection.execute("DROP TABLE IF EXISTS product_scores")
