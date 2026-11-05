import os
from pathlib import Path
from typing import Mapping

from flask import Flask
from dotenv import load_dotenv

from modules.product_data.database import get_database_path, initialize_database


def create_app() -> Flask:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=str(get_database_path()),
        AI_PROVIDER=os.getenv("AI_PROVIDER", "openai").strip().lower(),
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        OPENAI_MODEL=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        GEMINI_API_KEY=os.getenv("GEMINI_API_KEY"),
        GEMINI_MODEL=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
    )

    secret_key = app.config.get("SECRET_KEY") or os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("No SECRET_KEY found. Must be set in the environment or .env file.")
    app.config["SECRET_KEY"] = secret_key
    initialize_database(app.config["DATABASE"])

    from .routes import main
    app.register_blueprint(main)

    return app
