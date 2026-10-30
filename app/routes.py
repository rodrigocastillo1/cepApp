"""Flask routes for the responsive product passport interface."""

from io import BytesIO

import qrcode
from qrcode.image.svg import SvgPathImage
from flask import Blueprint, abort, redirect, render_template, request, url_for

from .demo_catalog import DEMO_PRODUCTS, DIMENSIONS, get_brand_analytics

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return render_template("index.html", products=DEMO_PRODUCTS.values())


@main.get("/search")
def search():
    product_id = request.args.get("product_id", "").strip()
    if not product_id:
        return render_template(
            "index.html",
            products=DEMO_PRODUCTS.values(),
            search_error="Enter a product ID to search.",
        ), 400

    if product_id not in DEMO_PRODUCTS:
        return render_template(
            "index.html",
            products=DEMO_PRODUCTS.values(),
            search_error=f"No product was found for “{product_id}”. Try a sample ID below.",
            search_value=product_id,
        ), 404

    return redirect(url_for("main.product_passport", product_id=product_id))


@main.get("/products/<product_id>")
def product_passport(product_id: str):
    product = DEMO_PRODUCTS.get(product_id)
    if product is None:
        abort(404)
    return render_template(
        "product.html",
        product=product,
        dimensions=DIMENSIONS,
        qr_url=url_for("main.product_qr", product_id=product_id),
    )


@main.get("/products/<product_id>/qr.svg")
def product_qr(product_id: str):
    if product_id not in DEMO_PRODUCTS:
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
    return render_template(
        "analytics.html",
        products=DEMO_PRODUCTS.values(),
        brands=get_brand_analytics(),
    )


@main.route("/products/<product_id>/coach", methods=["GET", "POST"])
def coach(product_id: str):
    product = DEMO_PRODUCTS.get(product_id)
    if product is None:
        abort(404)

    question = ""
    answer = None
    error = None
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            error = "Enter a question to continue."
        elif len(question) > 500:
            error = "Keep your question under 500 characters."
        else:
            answer = (
                "This is a demo response, not an AI-generated answer. "
                "The example data for this product is synthetic and has not "
                "been verified. Review the indicator values and their source "
                "notes on the passport page; unavailable values should not be "
                "interpreted as zero."
            )

    return render_template(
        "coach.html",
        product=product,
        question=question,
        answer=answer,
        error=error,
    ), 400 if error else 200


@main.app_errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404
