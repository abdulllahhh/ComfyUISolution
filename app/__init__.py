from flask import Flask, request, jsonify

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")
    @app.before_request
    def check_token():
        # Only protect your workflow routes (optional)
        if request.path.startswith("/api/workflow"):
            token = request.headers.get("Authorization")
            expected_token = "Bearer my-secret-token"
            if token != expected_token:
                return jsonify({"error": "Unauthorized"}), 401
    # Register Blueprints
    from app.routes.workflow_api import workflow_bp
    app.register_blueprint(workflow_bp, url_prefix="/api/workflow")

    return app
