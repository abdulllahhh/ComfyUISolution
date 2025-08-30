from flask import Blueprint, request, jsonify
from app.services.workflow_service import run_workflow

workflow_bp = Blueprint("workflow_api", __name__)

@workflow_bp.route("/run-model", methods=["POST"])
def run_model():
    """
    POST /api/workflow/run-file
    Body: { "workflow_file": "workflow1.json" }
    """
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "prompt is required"}), 400

    result = run_workflow(params=data)
    return jsonify(result), result["status_code"]

