from datetime import datetime, timezone
from typing import Mapping

from modules.analytics.lifecycle_store import LifecycleEventStore
from modules.product_data.product_repository import ProductRepository


class LifecycleEventProcessor:
    def __init__(
        self,
        repository: ProductRepository,
        event_store: LifecycleEventStore,
    ) -> None:
        self.repository = repository
        self.event_store = event_store

    def process(self, payload: Mapping[str, object]) -> bool:
        if payload.get("verified") is not True:
            return False

        carbon_delta = float(payload["carbon_delta_kg_co2e"])
        if carbon_delta < 0:
            return False

        product = self.repository.get_product_by_id(str(payload["product_id"]))
        if product is None:
            return False

        occurred_at = datetime.fromisoformat(
            str(payload["occurred_at"]).replace("Z", "+00:00")
        )
        normalized_time = occurred_at.astimezone(timezone.utc).isoformat(
            timespec="seconds"
        )
        return self.event_store.record_event(
            event_id=str(payload["event_id"]),
            product_id=product.product_id,
            brand=product.brand,
            carbon_delta_kg_co2e=carbon_delta,
            occurred_at=normalized_time,
        )
