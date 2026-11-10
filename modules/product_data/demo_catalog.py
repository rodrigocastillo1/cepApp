"""Synthetic product records used by the product-data module."""

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
    "PHN-CIRCA-PLUS": {
        "product_id": "PHN-CIRCA-PLUS",
        "name": "Circa Plus",
        "brand": "Circa Mobile",
        "category": "Smartphone",
        "release_year": 2026,
        "description": "Synthetic smartphone example added to test the product-data flow.",
        "demo": True,
        "carbon_footprint": 128,
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled battery material", "value": "55%", "source": "Synthetic example"},
                {"name": "Recycled rare-earth elements", "value": "65%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "8.0 / 10", "source": "Synthetic example"},
                {"name": "Software support", "value": "5 years", "source": "Synthetic example"},
                {"name": "Replaceable battery", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "88%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "Available", "source": "Synthetic example"},
            ],
        },
    },
    "LAP-ASTER-13": {
        "product_id": "LAP-ASTER-13",
        "name": "Aster 13",
        "brand": "Aster Computing",
        "category": "Laptop",
        "release_year": 2026,
        "description": "Synthetic laptop example for exploring product passport data.",
        "demo": True,
        "carbon_footprint": 168,
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled aluminum content", "value": "62%", "source": "Synthetic example"},
                {"name": "Recycled plastics", "value": "38%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "7.8 / 10", "source": "Synthetic example"},
                {"name": "Spare-parts availability", "value": "6 years", "source": "Synthetic example"},
                {"name": "Standard fasteners", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "86%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "Available", "source": "Synthetic example"},
            ],
        },
    },
    "LAP-VERDANT-16": {
        "product_id": "LAP-VERDANT-16",
        "name": "Verdant 16",
        "brand": "Verdant Devices",
        "category": "Laptop",
        "release_year": 2025,
        "description": "Synthetic large-screen laptop example with repair and recovery indicators.",
        "demo": True,
        "carbon_footprint": 205,
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled aluminum content", "value": "48%", "source": "Synthetic example"},
                {"name": "Recycled plastics", "value": "52%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "6.9 / 10", "source": "Synthetic example"},
                {"name": "Spare-parts availability", "value": "5 years", "source": "Synthetic example"},
                {"name": "Standard fasteners", "value": "No", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "78%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "Unavailable", "source": "No source supplied"},
            ],
        },
    },
    "PHN-NOVA-2": {
        "product_id": "PHN-NOVA-2",
        "name": "Nova 2",
        "brand": "Nova Circuit",
        "category": "Smartphone",
        "release_year": 2026,
        "description": "Synthetic smartphone example with recycled-material and software-support data.",
        "demo": True,
        "carbon_footprint": 132,
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled battery material", "value": "58%", "source": "Synthetic example"},
                {"name": "Recycled rare-earth elements", "value": "42%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "8.3 / 10", "source": "Synthetic example"},
                {"name": "Software support", "value": "7 years", "source": "Synthetic example"},
                {"name": "Replaceable battery", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "91%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "Available", "source": "Synthetic example"},
            ],
        },
    },
    "PHN-ORBIT-1": {
        "product_id": "PHN-ORBIT-1",
        "name": "Orbit One",
        "brand": "Orbit Mobile",
        "category": "Smartphone",
        "release_year": 2025,
        "description": "Synthetic smartphone example with a replaceable-battery design.",
        "demo": True,
        "carbon_footprint": 149,
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled battery material", "value": "35%", "source": "Synthetic example"},
                {"name": "Recycled plastics", "value": "30%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "7.1 / 10", "source": "Synthetic example"},
                {"name": "Software support", "value": "6 years", "source": "Synthetic example"},
                {"name": "Replaceable battery", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "80%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "No", "source": "Synthetic example"},
            ],
        },
    },
    "LAP-MOSS-14": {
        "product_id": "LAP-MOSS-14",
        "name": "MossBook 14",
        "brand": "Moss Technologies",
        "category": "Laptop",
        "release_year": 2026,
        "description": "Synthetic laptop example with several years of parts support.",
        "demo": True,
        "carbon_footprint": 176,
        "indicators": {
            "Material Inputs": [
                {"name": "Recycled aluminum content", "value": "70%", "source": "Synthetic example"},
                {"name": "Recycled plastics", "value": "25%", "source": "Synthetic example"},
            ],
            "Design & Durability": [
                {"name": "Repairability index", "value": "8.5 / 10", "source": "Synthetic example"},
                {"name": "Spare-parts availability", "value": "7 years", "source": "Synthetic example"},
                {"name": "Standard fasteners", "value": "Yes", "source": "Synthetic example"},
            ],
            "End-of-Life Recovery": [
                {"name": "Recyclability estimate", "value": "89%", "source": "Synthetic example"},
                {"name": "Take-back program", "value": "Available", "source": "Synthetic example"},
            ],
        },
    },
}


def list_demo_products():
    return [DEMO_PRODUCTS[product_id] for product_id in sorted(DEMO_PRODUCTS)]
