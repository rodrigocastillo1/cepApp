"""Build SVG QR codes for product identifiers."""

from io import BytesIO

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.main import QRCode
from qrcode.image.svg import SvgPathImage


def build_product_qr_code(product_id: str) -> QRCode:
    qr_code = qrcode.QRCode(
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr_code.add_data(product_id)
    qr_code.make(fit=True)
    return qr_code


def render_qr_code_svg(qr_code: QRCode) -> bytes:
    image = qr_code.make_image(image_factory=SvgPathImage)
    output = BytesIO()
    image.save(output)
    return output.getvalue()


def generate_product_qr_svg(product_id: str) -> bytes:
    return render_qr_code_svg(build_product_qr_code(product_id))
