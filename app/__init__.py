import os
from pathlib import Path

from flask import Flask
from dotenv import load_dotenv

from .database import get_database_path, initialize_database


def create_app() -> Flask:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    app = Flask(__name__)
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("No SECRET_KEY found. Must be set in the environment or .env file.")
    app.config["SECRET_KEY"] = secret_key
    app.config["DATABASE"] = str(get_database_path())
    initialize_database(app.config["DATABASE"])

    from .routes import main
    app.register_blueprint(main)

    return app
