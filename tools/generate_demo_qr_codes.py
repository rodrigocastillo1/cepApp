"""Generate QR code image files for products in the demo catalogue."""

import argparse
from io import BytesIO
from pathlib import Path

from qrcode.main import QRCode

from modules.product_data.demo_catalog import DEMO_PRODUCTS
from modules.product_data.qr_codes import build_product_qr_code, render_qr_code_svg


class QRCodeGenerationError(ValueError):
    """Raised when a demo product QR code cannot be generated."""


class DemoQRCodeGenerator:
    """Create QR codes that contain only a demo product's ID."""

    def __init__(
        self,
        output_directory: str | Path = Path("data/demo_qr_codes"),
    ) -> None:
        self.output_directory = Path(output_directory)

    def build_qr_code(self, product_id: str) -> QRCode:
        """Build a QR code for a known demo product ID."""
        if product_id not in DEMO_PRODUCTS:
            raise QRCodeGenerationError(f"Unknown demo product ID: {product_id}")

        return build_product_qr_code(product_id)

    def generate(self, product_id: str) -> Path:
        """Save one demo product QR code as an SVG and return its path."""
        qr_code = self.build_qr_code(product_id)
        self.output_directory.mkdir(parents=True, exist_ok=True)

        image_path = self.output_directory / f"{product_id}.svg"
        image_path.write_bytes(render_qr_code_svg(qr_code))
        return image_path

    def generate_all(self) -> list[Path]:
        """Generate QR code SVGs for every product in the demo catalogue."""
        return [
            self.generate(product_id)
            for product_id in sorted(DEMO_PRODUCTS)
        ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate QR code SVGs for the demo product catalogue."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/demo_qr_codes"),
        help="Directory for generated SVG files (default: data/demo_qr_codes).",
    )
    args = parser.parse_args()

    generated_files = DemoQRCodeGenerator(args.output_dir).generate_all()
    print(f"Generated {len(generated_files)} demo QR codes in {args.output_dir}.")
    for image_path in generated_files:
        print(image_path)


if __name__ == "__main__":
    main()
