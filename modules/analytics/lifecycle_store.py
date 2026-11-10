from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


class LifecycleEventStore:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(self.database_path), timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    def initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            with connection:
                connection.execute(
                    "DROP INDEX IF EXISTS lifecycle_events_occurred_at"
                )
                table = connection.execute(
                    """
                    SELECT sql FROM sqlite_master
                    WHERE type = 'table' AND name = 'lifecycle_events'
                    """
                ).fetchone()
                if table is None:
                    self._create_events_table(connection)
                elif "carbon_delta_kg_co2e > 0" in table["sql"]:
                    connection.execute(
                        "ALTER TABLE lifecycle_events RENAME TO lifecycle_events_old"
                    )
                    self._create_events_table(connection)
                    connection.execute(
                        """
                        INSERT INTO lifecycle_events
                        SELECT * FROM lifecycle_events_old
                        """
                    )
                    connection.execute("DROP TABLE lifecycle_events_old")

    @staticmethod
    def _create_events_table(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE lifecycle_events (
                event_id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                brand TEXT NOT NULL,
                carbon_delta_kg_co2e REAL NOT NULL
                    CHECK (carbon_delta_kg_co2e >= 0),
                occurred_at TEXT NOT NULL
            )
            """
        )

    def record_event(
        self,
        event_id: str,
        product_id: str,
        brand: str,
        carbon_delta_kg_co2e: float,
        occurred_at: str,
    ) -> bool:
        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO lifecycle_events (
                        event_id, product_id, brand,
                        carbon_delta_kg_co2e, occurred_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (event_id, product_id, brand, carbon_delta_kg_co2e, occurred_at),
                )
        return cursor.rowcount == 1

    def get_brand_totals(self) -> list[dict[str, object]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT brand, SUM(carbon_delta_kg_co2e) AS total_kg_co2e,
                       COUNT(*) AS event_count, MAX(occurred_at) AS updated_at
                FROM lifecycle_events
                GROUP BY brand
                ORDER BY total_kg_co2e DESC, brand
                """
            ).fetchall()

        return [
            {
                "brand": row["brand"],
                "total_kg_co2e": round(row["total_kg_co2e"], 2),
                "event_count": row["event_count"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]
