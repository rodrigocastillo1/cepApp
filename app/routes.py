"""Flask routes for the responsive product passport interface."""

import re

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from modules.ai.gemini_provider import GeminiProvider
from modules.ai.openai_provider import OpenAIProvider
from modules.ai.provider import AIProvider, AIProviderError, AIProviderNotConfigured
from modules.analytics.lifecycle_store import LifecycleEventStore
from modules.analytics.service import AnalyticsService
from modules.circularity.scoring import CircularityScorer
from modules.product_data.models import Indicator, Product
from modules.product_data.product_repository import ProductRepository

main = Blueprint("main", __name__)
circularity_scorer = CircularityScorer()


def get_repository() -> ProductRepository:
    return ProductRepository(current_app.config["DATABASE"])


def get_lifecycle_event_store() -> LifecycleEventStore:
    return LifecycleEventStore(current_app.config["DATABASE"])


def get_ai_provider() -> AIProvider:
    configured_provider = current_app.config.get("AI_PROVIDER")
    if configured_provider is not None and not isinstance(configured_provider, str):
        return configured_provider
    provider_name = str(configured_provider or "openai").lower()
    if provider_name == "openai":
        return OpenAIProvider(
            api_key=current_app.config.get("OPENAI_API_KEY"),
            model=current_app.config["OPENAI_MODEL"],
        )
    if provider_name == "gemini":
        return GeminiProvider(
            api_key=current_app.config.get("GEMINI_API_KEY"),
            model=current_app.config["GEMINI_MODEL"],
        )
    raise AIProviderNotConfigured(
        "Set AI_PROVIDER to either 'openai' or 'gemini'."
    )


def find_mentioned_indicator(question: str, product: Product) -> Indicator | None:
    normalized_question = re.sub(r"[^a-z0-9]+", " ", question.casefold()).strip()
    return next(
        (
            indicator
            for indicators in product.indicators.values()
            for indicator in indicators
            if re.sub(r"[^a-z0-9]+", " ", indicator.name.casefold()).strip()
            in normalized_question
        ),
        None,
    )


@main.get("/")
def index():
    return render_template("index.html", products=get_repository().list_products())


@main.get("/search")
def search():
    repository = get_repository()
    product_id = request.args.get("product_id", "").strip()
    if not product_id:
        return render_template(
            "index.html",
            products=repository.list_products(),
            search_error="Enter a product ID to search.",
        ), 400

    product = repository.get_product_by_id(product_id)
    if product is None:
        return render_template(
            "index.html",
            products=repository.list_products(),
            search_error=f"No product was found for “{product_id}”. Try a sample ID below.",
            search_value=product_id,
        ), 404

    return redirect(url_for("main.product_passport", product_id=product_id))


@main.get("/products/<product_id>")
def product_passport(product_id: str):
    product = get_repository().get_product_by_id(product_id)
    if product is None:
        abort(404)
    return render_template(
        "product.html",
        product=product,
        dimensions=circularity_scorer.methodology.dimensions,
        assessment=circularity_scorer.calculate(product),
        qr_url=url_for("main.product_qr", product_id=product_id),
    )


@main.get("/products/<product_id>/qr.svg")
def product_qr(product_id: str):
    svg_data = get_repository().get_product_qr_svg(product_id)
    if svg_data is None:
        abort(404)

    return svg_data, 200, {"Content-Type": "image/svg+xml"}


@main.get("/analytics")
def analytics():
    repository = get_repository()
    products = repository.list_products()
    analytics_service = AnalyticsService(circularity_scorer)
    return render_template(
        "analytics.html",
        products=products,
        brands=analytics_service.get_brand_analytics(products),
        product_dimensions=analytics_service.get_product_dimension_analytics(products),
        category_dimensions=analytics_service.get_category_dimension_analytics(products),
        indicators=analytics_service.get_indicator_analytics(products),
        scorer=circularity_scorer,
    )


@main.get("/about")
def about():
    return render_template("about.html")


@main.get("/api/analytics/carbon-footprint")
def carbon_footprint_analytics():
    return jsonify(brands=get_lifecycle_event_store().get_brand_totals())


@main.route("/products/<product_id>/coach", methods=["GET", "POST"])
def coach(product_id: str):
    product = get_repository().get_product_by_id(product_id)
    if product is None:
        abort(404)

    session_generation = current_app.config["COACH_SESSION_GENERATION"]
    if session.get("_coach_session_generation") != session_generation:
        session.clear()
        session["_coach_session_generation"] = session_generation

    assessment = circularity_scorer.calculate(product)
    history_key = f"coach_history:{product.product_id}"
    history = session.get(history_key, [])
    question = ""
    error = None
    response_status = 200
    configured_provider = current_app.config.get("AI_PROVIDER")
    if configured_provider is not None and not isinstance(configured_provider, str):
        ai_configured = True
    elif configured_provider == "gemini":
        ai_configured = bool((current_app.config.get("GEMINI_API_KEY") or "").strip())
    else:
        ai_configured = bool((current_app.config.get("OPENAI_API_KEY") or "").strip())
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            error = "Enter a question to continue."
            response_status = 400
        elif len(question) > 500:
            error = "Keep your question under 500 characters."
            response_status = 400
        else:
            try:
                answer = get_ai_provider().generate_answer(
                    question,
                    product,
                    assessment,
                )
                indicator = find_mentioned_indicator(question, product)
                history = [
                    *history,
                    {
                        "question": question,
                        "answer": answer,
                        "indicator_name": indicator.name if indicator else None,
                        "indicator_value": indicator.value if indicator else None,
                    },
                ][-5:]
                session[history_key] = history
                return redirect(url_for("main.coach", product_id=product_id))
            except AIProviderNotConfigured:
                error = "The AI coach is not configured. Check AI_PROVIDER and its API key in the server configuration."
                response_status = 503
            except AIProviderError:
                current_app.logger.exception(
                    "AI coach provider failed for product %s",
                    product.product_id,
                )
                error = "The AI coach is temporarily unavailable. Please try again later."
                response_status = 502

    return render_template(
        "coach.html",
        product=product,
        assessment=assessment,
        question=question,
        history=history,
        error=error,
        ai_configured=ai_configured,
    ), response_status


@main.app_errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404
