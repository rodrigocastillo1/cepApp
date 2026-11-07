import json
import os

import faust

from modules.analytics.lifecycle_store import LifecycleEventStore
from modules.lifecycle.event_processor import LifecycleEventProcessor
from modules.product_data.product_repository import ProductRepository

app = faust.App(
    "cep-lifecycle-demo",
    broker=os.getenv("KAFKA_BROKER", "kafka://localhost:9092"),
)
verified_events = app.topic("lifecycle-events", value_serializer="raw")

database_path = os.getenv("DATABASE", "catalogue.db")
processor = LifecycleEventProcessor(
    ProductRepository(database_path),
    LifecycleEventStore(database_path),
)


@app.agent(verified_events)
async def process_verified_events(events):
    async for payload in events:
        processor.process(json.loads(payload))
