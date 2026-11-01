"""Synthetic product records used to seed the SQLite-backed catalogue."""

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
