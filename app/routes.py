"""Flask routes for the responsive product passport interface."""

from io import BytesIO

import qrcode
from qrcode.image.svg import SvgPathImage
from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for

from modules.ai.openai_provider import OpenAIProvider
from modules.ai.provider import AIProvider, AIProviderError, AIProviderNotConfigured
from modules.analytics.service import AnalyticsService
from modules.circularity.scoring import CircularityScorer
from modules.product_data.product_repository import ProductRepository

main = Blueprint("main", __name__)
circularity_scorer = CircularityScorer()


def get_repository() -> ProductRepository:
    return ProductRepository(current_app.config["DATABASE"])


def get_ai_provider() -> AIProvider:
    configured_provider = current_app.config.get("AI_PROVIDER")
    if configured_provider is not None:
        return configured_provider
    return OpenAIProvider(
        api_key=current_app.config.get("OPENAI_API_KEY"),
        model=current_app.config["OPENAI_MODEL"],
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
    if get_repository().get_product_by_id(product_id) is None:
        abort(404)

    passport_url = url_for(
        "main.product_passport",
        product_id=product_id,
        _external=True,
    )
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(passport_url)
    qr.make(fit=True)
    image = qr.make_image(image_factory=SvgPathImage)
    output = BytesIO()
    image.save(output)
    return output.getvalue(), 200, {"Content-Type": "image/svg+xml"}


@main.get("/analytics")
def analytics():
    repository = get_repository()
    products = repository.list_products()
    return render_template(
        "analytics.html",
        products=products,
        brands=AnalyticsService(circularity_scorer).get_brand_analytics(products),
        scorer=circularity_scorer,
    )


@main.route("/products/<product_id>/coach", methods=["GET", "POST"])
def coach(product_id: str):
    product = get_repository().get_product_by_id(product_id)
    if product is None:
        abort(404)

    assessment = circularity_scorer.calculate(product)
    question = ""
    answer = None
    error = None
    response_status = 200
    ai_configured = (
        current_app.config.get("AI_PROVIDER") is not None
        or bool(current_app.config.get("OPENAI_API_KEY"))
    )
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
            except AIProviderNotConfigured:
                error = "The AI coach is not configured. Set OPENAI_API_KEY on the server to enable it."
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
        answer=answer,
        error=error,
        ai_configured=ai_configured,
    ), response_status


@main.app_errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404
