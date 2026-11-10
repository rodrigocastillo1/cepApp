import json
import os
import random
import time
from datetime import datetime, timezone
from uuid import uuid4

from kafka import KafkaProducer

from modules.product_data.demo_catalog import DEMO_PRODUCTS


class DemoLifecycleEventProducer:
    def __init__(
        self,
        broker: str,
        topic: str = "lifecycle-events",
        interval_seconds: float = 3,
    ) -> None:
        self.topic = topic
        self.interval_seconds = interval_seconds
        self.products = tuple(DEMO_PRODUCTS)
        self.producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda event: json.dumps(event).encode("utf-8"),
        )

    def create_event(self) -> dict[str, object]:
        if random.random() < 0.05:
            carbon_delta = round(random.uniform(-5, -0.1), 2)
        else:
            carbon_delta = round(random.uniform(0, 5), 2)
        return {
            "event_id": str(uuid4()),
            "product_id": random.choice(self.products),
            "occurred_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "carbon_delta_kg_co2e": carbon_delta,
            "verified": True,
        }

    def run_forever(self) -> None:
        print(f"Publishing synthetic events to {self.topic}. Press Ctrl+C to stop.")
        while True:
            event = self.create_event()
            self.producer.send(
                self.topic,
                value=event,
            )
            self.producer.flush(timeout=10)
            print(
                f"Published {event['event_id']} for {event['product_id']}: "
                f"{event['carbon_delta_kg_co2e']} kg CO2e"
            )
            time.sleep(self.interval_seconds)


def main() -> None:
    producer = DemoLifecycleEventProducer(
        broker=os.getenv("KAFKA_BROKER", "localhost:9092"),
        interval_seconds=float(os.getenv("EVENT_INTERVAL_SECONDS", "3")),
    )
    try:
        producer.run_forever()
    except KeyboardInterrupt:
        print("Stopping event producer.")
    finally:
        producer.producer.close()


if __name__ == "__main__":
    main()
