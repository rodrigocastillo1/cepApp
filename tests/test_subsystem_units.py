"""Unit tests for the project's data, scoring, analytics, AI, and QR subsystems."""

import sqlite3
from types import SimpleNamespace

import pytest

from modules.ai.gemini_provider import GeminiProvider
from modules.ai.openai_provider import OpenAIProvider
from modules.ai.provider import AIProviderNotConfigured
from modules.analytics.errors import InvalidAnalyticsInput
from modules.analytics.service import AnalyticsService
from modules.circularity.errors import (
    CircularityCalculationError,
    InvalidMethodologyError,
)
from modules.circularity.methodology import ScoringMethodology
from modules.circularity.scoring import CircularityScorer
from modules.product_data.database import connect_database, initialize_database
from modules.product_data.errors import DatabaseError, ProductRepositoryError
from modules.product_data.models import Indicator, SourceReference
from modules.product_data.product_repository import ProductRepository
from tools.generate_demo_qr_codes import DemoQRCodeGenerator, QRCodeGenerationError


def _repository(tmp_path):
    database_path = tmp_path / "subsystem-tests.sqlite"
    initialize_database(database_path)
    return ProductRepository(database_path)


def _indicator(value, name="Recycled content"):
    return Indicator(
        product_id="TEST-PRODUCT",
        dimension="Material Inputs",
        name=name,
        value=value,
        source_reference=SourceReference(),
    )


def test_product_data_initializes_three_tables_without_saved_scores(tmp_path):
    database_path = tmp_path / "schema.sqlite"
    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        product_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(products)")
        }

    assert {"products", "product_indicators", "source_references"} <= tables
    assert "score" not in product_columns
    assert "product_scores" not in tables


def test_product_repository_reconstructs_product_indicators_and_sources(tmp_path):
    product = _repository(tmp_path).get_product_by_id("LAP-LOOP-14")

    assert product is not None
    assert product.name == "LoopBook 14"
    assert product.brand == "LoopWorks"
    indicators = product.indicators["Material Inputs"]
    
    assert all(indicator.product_id == product.product_id for indicator in indicators)
    assert all(indicator.source_reference.source_id is not None for indicator in indicators)


def test_product_repository_returns_none_for_unknown_id(tmp_path):
    assert _repository(tmp_path).get_product_by_id("NO-SUCH-PRODUCT") is None


def test_product_repository_searches_case_insensitively_and_handles_blank_query(tmp_path):
    repository = _repository(tmp_path)

    results = repository.search_products("  loopbook  ")

    assert {product.name for product in results} == {"LoopBook 14", "LoopBook Pro"}
    assert repository.search_products("   ") == []


def test_circularity_normalizes_percentages_and_rejects_out_of_range_values():
    scorer = CircularityScorer()

    assert scorer.normalize(_indicator("75%")) == 75
    assert scorer.normalize(_indicator("0%")) == 0
    assert scorer.normalize(_indicator("100%")) == 100
    assert scorer.normalize(_indicator("101%")) is None
    assert scorer.normalize(_indicator("-1%")) is None


def test_circularity_normalizes_supported_rating_year_and_binary_indicators():
    scorer = CircularityScorer()

    assert scorer.normalize(_indicator("8.8 / 10", "Repairability index")) == 88
    assert scorer.normalize(_indicator("7 years", "Spare-parts availability")) == 100
    assert scorer.normalize(_indicator("10 years", "Software support")) == 100
    assert scorer.normalize(_indicator("Yes", "Standard fasteners")) == 100
    assert scorer.normalize(_indicator("No", "Replaceable battery")) == 0


def test_circularity_excludes_missing_and_unsupported_indicator_values():
    scorer = CircularityScorer()

    assert scorer.normalize(_indicator(None)) is None
    assert scorer.normalize(_indicator("Unavailable")) is None
    assert scorer.normalize(_indicator("unknown text")) is None
    assert scorer.normalize(_indicator("Yes", "Unrecognized question")) is None


def test_circularity_assessment_averages_dimensions_and_reports_coverage(tmp_path):
    product = _repository(tmp_path).get_product_by_id("LAP-LOOP-14")
    assert product is not None

    assessment = CircularityScorer().calculate(product)
    assert assessment.overall_score == 84
    assert assessment.coverage == 1
    assert [component.score for component in assessment.components] == [60, 96, 96]
    assert assessment.components[0].coverage == pytest.approx(2 / 3)


def test_analytics_calculates_brand_score_carbon_and_product_count(tmp_path):
    repository = _repository(tmp_path)
    products = [
        product
        for product in repository.list_products()
        if product.brand == "LoopWorks"
    ]
    scorer = CircularityScorer()

    brand = next(
        item
        for item in AnalyticsService(scorer).get_brand_analytics(products)
        if item["brand"] == "LoopWorks"
    )
    expected_score = sum(scorer.calculate(product).overall_score for product in products) / len(products)

    assert brand["product_count"] == 2
    assert brand["average_score"] == pytest.approx(expected_score)
    assert brand["average_carbon"] == 190


def test_analytics_category_dimension_averages_use_available_scores(tmp_path):
    repository = _repository(tmp_path)
    products = [
        product
        for product in repository.list_products()
        if product.category == "Laptop"
    ]
    service = AnalyticsService(CircularityScorer())

    category = next(
        item
        for item in service.get_category_dimension_analytics(products)
        if item["category"] == "Laptop"
    )

    assert category["product_count"] == len(products)
    for index, dimension in enumerate(category["dimensions"]):
        scores = [
            assessment.components[index].score
            for product in products
            if (
                assessment := service.scorer.calculate(product)
            ).components[index].score is not None
        ]
        assert dimension["product_count"] == len(scores)
        assert dimension["average_score"] == pytest.approx(sum(scores) / len(scores))


def test_analytics_indicator_data_excludes_missing_values_and_keeps_raw_values(tmp_path):
    products = _repository(tmp_path).list_products()
    indicators = AnalyticsService().get_indicator_analytics(products)

    recycled_aluminum = next(
        item for item in indicators if item["name"] == "Recycled aluminum content"
    )
    loopbook = next(
        item for item in recycled_aluminum["entries"]
        if item["product_id"] == "LAP-LOOP-14"
    )

    assert loopbook["value"] == "75%"
    assert loopbook["normalized_value"] == 75
    assert all(
        item["name"] != "Conflict-mineral declaration"
        for item in indicators
    )


def test_openai_provider_reports_missing_credentials():
    with pytest.raises(AIProviderNotConfigured, match="OPENAI_API_KEY"):
        OpenAIProvider(api_key=None)


def test_gemini_provider_reports_missing_credentials():
    with pytest.raises(AIProviderNotConfigured, match="GEMINI_API_KEY"):
        GeminiProvider(api_key="  ")


def test_ai_providers_return_trimmed_answers_using_injected_clients(tmp_path):
    product = _repository(tmp_path).get_product_by_id("LAP-LOOP-14")
    assert product is not None
    assessment = CircularityScorer().calculate(product)

    openai_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **_kwargs: SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(content="  OpenAI answer  ")
                        )
                    ]
                )
            )
        )
    )
    gemini_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **_kwargs: SimpleNamespace(
                text="  Gemini answer  "
            )
        )
    )

    assert (
        OpenAIProvider(api_key=None, client=openai_client).generate_answer(
            "Question", product, assessment
        )
        == "OpenAI answer"
    )
    assert (
        GeminiProvider(api_key=None, client=gemini_client).generate_answer(
            "Question", product, assessment
        )
        == "Gemini answer"
    )


def test_qr_generator_saves_svg_containing_demo_product_id(tmp_path):
    generator = DemoQRCodeGenerator(tmp_path / "qr-codes")
    qr_code = generator.build_qr_code("LAP-LOOP-14")
    output_path = generator.generate("LAP-LOOP-14")

    assert "LAP-LOOP-14" in str(qr_code.data_list[0].data)
    assert output_path.name == "LAP-LOOP-14.svg"
    assert "<svg" in output_path.read_text(encoding="utf-8")
    with pytest.raises(QRCodeGenerationError, match="Unknown demo product ID"):
        generator.build_qr_code("NO-SUCH-PRODUCT")


def test_product_data_database_connection_raises_subsystem_error(tmp_path, monkeypatch):
    def fail_connect(_path):
        raise sqlite3.OperationalError("connection failed")

    monkeypatch.setattr("modules.product_data.database.sqlite3.connect", fail_connect)

    with pytest.raises(DatabaseError, match="Could not connect"):
        connect_database(tmp_path / "failure.sqlite")


def test_product_repository_wraps_sql_errors_with_repository_error(tmp_path):
    repository = ProductRepository(tmp_path / "uninitialized.sqlite")

    with pytest.raises(ProductRepositoryError, match="product list"):
        repository.list_products()


def test_circularity_invalid_methodology_raises_subsystem_error():
    with pytest.raises(InvalidMethodologyError, match="version"):
        ScoringMethodology(version=" ")

    with pytest.raises(InvalidMethodologyError, match="year cap"):
        ScoringMethodology(max_years_for_full_score=0)


def test_circularity_invalid_inputs_raise_subsystem_error():
    scorer = CircularityScorer()

    with pytest.raises(CircularityCalculationError, match="Product instance"):
        scorer.calculate(None)

    with pytest.raises(CircularityCalculationError, match="Indicator instance"):
        scorer.normalize(None)


def test_analytics_rejects_non_product_input_with_subsystem_error():
    with pytest.raises(InvalidAnalyticsInput, match="list of Product"):
        AnalyticsService().get_brand_analytics([object()])
