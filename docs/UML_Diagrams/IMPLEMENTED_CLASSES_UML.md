# Subsystem UML Class Diagrams

These diagrams describe the classes present in each of the application subsystems. The diagrams in this document are the source text of the mermaid diagrams rendered in the README:md file.

## 1. Product Data Subsystem

```mermaid
classDiagram
direction LR

class Product {
  +str product_id
  +str name
  +str brand
  +str category
  +int release_year
  +str description
  +bool is_demo
  +int carbon_footprint
  +dict indicators
}

class Indicator {
  +str product_id
  +str dimension
  +str name
  +str value
  +SourceReference source_reference
  +source str
}

class SourceReference {
  +int source_id
  +str publisher
  +str url
  +str accessed_at
  +str notes
  +display_text str
}

class ProductRepository {
  +str database_path
  +_connect() sqlite3.Connection
  +list_products() list~Product~
  +get_product_by_id(product_id) Product
  +search_products(query) list~Product~
}

Product "1" *-- "0..*" Indicator : groups by dimension
Indicator "1" *-- "1" SourceReference : has source details
ProductRepository ..> Product : creates
ProductRepository ..> Indicator : creates
ProductRepository ..> SourceReference : creates
```


## 2. Circularity Assessment Subsystem

```mermaid
classDiagram
direction T

class ScoringMethodology {
  +str version
  +tuple~str~ dimensions
  +int max_years_for_full_score
  +frozenset~str~ missing_values
  +Mapping~str, float~ binary_scores
  +frozenset~str~ supported_binary_indicators
  +frozenset~str~ supported_rating_indicators
  +frozenset~str~ supported_year_indicators
  +str missing_data_note
  +__post_init__()
}

class CircularityScorer {
  +ScoringMethodology methodology
  +calculate(product) CircularityAssessment
  +calculate_component(dimension, indicators) ComponentScore
  +normalize(indicator) float
}

class CircularityAssessment {
  +str product_id
  +float overall_score
  +tuple~ComponentScore~ components
  +float coverage
  +str methodology_version
  +str missing_data_note
}

class ComponentScore {
  +str dimension
  +float score
  +float coverage
  +tuple~str~ used_indicators
  +int total_indicators
}

class Product
class Indicator

CircularityScorer --> ScoringMethodology : applies
CircularityScorer ..> Product : calculates from
CircularityScorer ..> Indicator : normalizes
CircularityScorer ..> CircularityAssessment : creates
CircularityAssessment "1" *-- "0..*" ComponentScore : breakdown
```

## 3. Analytics Subsystem

```mermaid
classDiagram
direction TB

class AnalyticsService {
  +CircularityScorer scorer
  +get_brand_analytics(products) list~dict~
  +get_product_dimension_analytics(products) list~dict~
  +get_category_dimension_analytics(products) list~dict~
  +get_indicator_analytics(products) list~dict~
}

class _BrandAggregate {
  +int product_count
  +list~float~ scores
  +list~float~ carbon
}

class CircularityScorer
class Product
class CircularityAssessment
class ComponentScore

AnalyticsService --> CircularityScorer : uses
AnalyticsService ..> Product : aggregates
AnalyticsService ..> CircularityAssessment : reads
AnalyticsService ..> ComponentScore : reads
AnalyticsService ..> _BrandAggregate : groups brand data
```


![](.\docs\UML_Diagrams\UML1.svg)

## 4. AI provider Subsystem

```mermaid
---
config:
  layout: elk
---
classDiagram
direction BT

class AIProvider {
  <<abstract>>
  +generate_answer(question, product, assessment)* str
}

class OpenAIProvider {
  +str model
  -Any _client
  -type _api_error
  +generate_answer(question, product, assessment) str
}

class GeminiProvider {
  +str model
  -Any _client
  -type _api_error
  +generate_answer(question, product, assessment) str
}

class AIProviderError {
}

class AIProviderNotConfigured {
}

class RuntimeError {
  <<external Python exception>>
}

class Product
class CircularityAssessment

OpenAIProvider --|> AIProvider
GeminiProvider --|> AIProvider
AIProviderNotConfigured --|> AIProviderError
AIProviderError --|> RuntimeError
OpenAIProvider ..> Product : uses evidence
OpenAIProvider ..> CircularityAssessment : uses score context
GeminiProvider ..> Product : uses evidence
GeminiProvider ..> CircularityAssessment : uses score context
OpenAIProvider ..> AIProviderError : raises on failure
GeminiProvider ..> AIProviderError : raises on failure
```

## 5. Tool - QR generator utility

```mermaid
classDiagram
direction LR

class DemoQRCodeGenerator {
  +Path output_directory
  +build_qr_code(product_id) QRCode
  +generate(product_id) Path
  +generate_all() list~Path~
}

class QRCode {
  <<external qrcode library>>
}

DemoQRCodeGenerator ..> QRCode : creates
```

`DemoQRCodeGenerator` produces SVG files with the product ID as the QR
payload.
