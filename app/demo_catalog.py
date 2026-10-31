"""Synthetic product records used to seed the SQLite-backed catalogue."""

DIMENSIONS = (
    "Material Inputs",
    "Design & Durability",
    "End-of-Life Recovery",
)

DEMO_PRODUCTS = {
    "LAP-LOOP-14": {
        "product_id": "LAP-LOOP-14",
        "name": "LoopBook 14",
        "brand": "LoopWorks",
        "category": "Laptop",
        "release_year": 2025,
        "description": "Illustrative laptop record for previewing the product passport.",
        "demo": True,
        "carbon_footprint": 185,
        "score": 82.5,
        "scores": {
            "Material Inputs": 80.0,
            "Design & Durability": 85.0,
            "End-of-Life Recovery": 81.0,
        },
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled aluminum content", "value": "75%", "source": "Synthetic example"},
                {"name": "Recycled plastics", "value": "45%", "source": "Synthetic example"},
                {"name": "Conflict-mineral declaration", "value": "Unavailable", "source": "No source supplied"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "8.8 / 10", "source": "Synthetic example"},
                {"name": "Spare-parts availability", "value": "7 years", "source": "Synthetic example"},
                {"name": "Standard fasteners", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "92%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "Available", "source": "Synthetic example"},
                {"name": "Recovery fee", "value": "Unavailable", "source": "No source supplied"},
            ],
        },
    },
    "PHN-CIRCA-ONE": {
        "product_id": "PHN-CIRCA-ONE",
        "name": "Circa One",
        "brand": "Circa Mobile",
        "category": "Smartphone",
        "release_year": 2025,
        "description": "Illustrative smartphone record for previewing the product passport.",
        "demo": True,
        "carbon_footprint": 142,
        "score": 84.5,
        "scores": {
            "Material Inputs": 88.0,
            "Design & Durability": 78.0,
            "End-of-Life Recovery": 89.0,
        },
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled battery material", "value": "70%", "source": "Synthetic example"},
                {"name": "Recycled rare-earth elements", "value": "60%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "7.2 / 10", "source": "Synthetic example"},
                {"name": "Software support", "value": "6 years", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "90%", "source": "Synthetic example"},
            ],
        },
    },
    "LAP-LOOP-PRO": {
        "product_id": "LAP-LOOP-PRO",
        "name": "LoopBook Pro",
        "brand": "LoopWorks",
        "category": "Laptop",
        "release_year": 2024,
        "description": "Illustrative laptop record with a focus on repair and long-term use.",
        "demo": True,
        "carbon_footprint": 195,
        "score": 79.0,
        "scores": {
            "Material Inputs": 75.0,
            "Design & Durability": 88.0,
            "End-of-Life Recovery": 74.0,
        },
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled casing material", "value": "50%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "9.2 / 10", "source": "Synthetic example"},
                {"name": "Replaceable battery", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "82%", "source": "Synthetic example"},
            ],
        },
    },
    "PHN-CIRCA-MINI": {
        "product_id": "PHN-CIRCA-MINI",
        "name": "Circa Mini",
        "brand": "Circa Mobile",
        "category": "Smartphone",
        "release_year": 2024,
        "description": "Illustrative smartphone record for the responsive catalogue preview.",
        "demo": True,
        "carbon_footprint": 115,
        "score": 77.2,
        "scores": {
            "Material Inputs": 78.0,
            "Design & Durability": 72.0,
            "End-of-Life Recovery": 82.0,
        },
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled plastic components", "value": "20%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "7.5 / 10", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "85%", "source": "Synthetic example"},
            ],
        },
    },
}


def list_demo_products():
    return [DEMO_PRODUCTS[product_id] for product_id in sorted(DEMO_PRODUCTS)]


def get_brand_analytics(products=None):
    """Return preview-only aggregates from the synthetic catalogue."""
    catalogue = list(products or DEMO_PRODUCTS.values())
    grouped = {}
    for product in catalogue:
        brand = grouped.setdefault(product["brand"], {"scores": [], "carbon": []})
        brand["scores"].append(product["score"])
        brand["carbon"].append(product["carbon_footprint"])

    return [
        {
            "brand": brand,
            "average_score": sum(values["scores"]) / len(values["scores"]),
            "average_carbon": sum(values["carbon"]) / len(values["carbon"]),
            "product_count": len(values["scores"]),
        }
        for brand, values in sorted(grouped.items())
    ]
