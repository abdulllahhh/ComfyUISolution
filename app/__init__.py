from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
SHARED_SECRET = os.getenv("FLASK_SHARED_SECRET")

def check_token():
        # Only protect your workflow routes (optional)
        if request.path.startswith("/api/workflow"):
            token = request.headers.get("Authorization")
            expected_token = f"Bearer {SHARED_SECRET}"
            if token != expected_token:
                return jsonify({"error": "Unauthorized"}), 401

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")
    app.before_request(check_token)
    # Register Blueprints
    from app.routes.workflow_api import workflow_bp
    app.register_blueprint(workflow_bp, url_prefix="/api/workflow")
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200
    return app
