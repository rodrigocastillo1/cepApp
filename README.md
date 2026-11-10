# cepApp
Capstone Project for the Compact Programming Course in Python. This is an AI-powered web app for exploring electronics product passports, evaluating circularity, and understanding sustainability through data, analytics, and AI.
<<<<<<< HEAD

Prof. Dr. Galyna Tabunshchyk

Group 11.
Topic: AI-Powered Circular Economy Product Passport

| Student                    | Matriculation number | Subsystem                                                        |
| -------------------------- | -------------------- | ---------------------------------------------------------------- |
| Rodrigo Castillo Alcantara | ESE - 7226791        | - Analytics Subsystem<br>- AI provider Subsystem               |
| Elnur Allazov              | ESE - 7226316        | - Product Data Subsystem<br>- Circularity Assessment Subsystem |

# [Homeworkassignment001] Subsystem UML Class Diagrams

The following diagrams describe the classes present in each of the application subsystems.

For more information watch the presentation video: [HomeAssignment1-CPC(GROUP 11)](https://www.youtube.com/watch?v=vU1BhcSXFp0)

## 1. Product Data Subsystem

![](./docs/UML_Diagrams/UML_Subsystem1_ProductRepository.svg)

## 2. Circularity Assessment Subsystem

![](./docs/UML_Diagrams/UML_Subsystem2_CircularityScorer.svg)

## 3. Analytics Subsystem

![](./docs/UML_Diagrams/UML_Subsystem3_AnalyticsService.svg)

## 4. AI provider Subsystem

![](./docs/UML_Diagrams/UML_Subsystem4_AIProvider.svg)

## 5. Tool - QR generator utility

![](./docs/UML_Diagrams/UML_Tool_DemoQRCodeGenerator.svg)


---
=======
>>>>>>> Homeworkassignment002

Prof. Dr. Galyna Tabunshchyk

Group 11.
Topic: AI-Powered Circular Economy Product Passport

| Student                    | Matriculation number | Subsystem                                                        |
| -------------------------- | -------------------- | ---------------------------------------------------------------- |
| Rodrigo Castillo Alcantara | ESE - 7226791        | - Analytics Subsystem<br>- AI provider Subsystem               |
| Elnur Allazov              | ESE - 7226316        | - Product Data Subsystem<br>- Circularity Assessment Subsystem |

# [Homeworkassignment002] Architecture Diagrams

For more information watch the presentation video: [HomeAssignment2-CPC(GROUP 11)](https://www.youtube.com/watch?v=BfJSN0wDNUU)

## Real-Time Processing Pipeline

```mermaid
flowchart LR
    P["DemoLifecycleEventProducer"] -->|"JSON · lifecycle-events"| B["Redpanda<br/>Kafka-compatible broker"]
    B --> F["Faust app and agent"]
    F -->|"decode JSON"| V["LifecycleEventProcessor"]
    V -->|"product lookup"| R["ProductRepository"]
    R --> D[("catalogue.db<br/>products + lifecycle_events")]
    V -->|"verified + nonnegative + known product"| S["LifecycleEventStore"]
    S --> D
    C["Analytics page<br/>chart polls every 3 seconds"] -->|"GET /api/analytics/carbon-footprint"| W["Flask API"]
    W -->|"aggregate totals"| S
    W -->|"JSON response"| C
```

Compose runs Redpanda, the Faust worker, the demo producer, and Flask. The
faust worker and web app share the `catalogue.db` SQLite file.

## Live analytics feature: class diagrams

```mermaid
classDiagram
direction LR

class DemoLifecycleEventProducer {
  +str topic
  +float interval_seconds
  +tuple products
  +KafkaProducer producer
  +create_event() dict~str, object~
  +run_forever()
}

class LifecycleEventProcessor {
  +ProductRepository repository
  +LifecycleEventStore event_store
  +process(payload) bool
}

class ProductRepository {
  +str database_path
  +list_products() list~Product~
  +get_product_by_id(product_id) Product | None
  +search_products(query) list~Product~
}

class LifecycleEventStore {
  +Path database_path
  +initialize()
  +record_event(event_id, product_id, brand, carbon_delta_kg_co2e, occurred_at) bool
  +get_brand_totals() list~dict~
}

class Product {
  +str product_id
  +str brand
  +str category
}

class KafkaProducer {
  <<external library>>
}

DemoLifecycleEventProducer ..> KafkaProducer : publishes JSON events
LifecycleEventProcessor --> ProductRepository : looks up product and brand
LifecycleEventProcessor --> LifecycleEventStore : records accepted event
ProductRepository ..> Product : loads from catalogue
```

---

### Run the Docker Compose demo

1. Start Docker Desktop.
2. From the project folder, start all services:
   ```powershell
   docker compose up --build
   ```
3. Open the app at `http://localhost:5000`. The live brand chart is at
   `http://localhost:5000/analytics`.
4. To stop the services, press **Ctrl+C** in the terminal, then run:
   ```powershell
   docker compose down
   ```
