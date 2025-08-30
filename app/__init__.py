from flask import Flask

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    # Register Blueprints
    from app.routes.workflow_api import workflow_bp
    app.register_blueprint(workflow_bp, url_prefix="/api/workflow")

    return app
