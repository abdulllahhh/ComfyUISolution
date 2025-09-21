import os
from flask import Blueprint, request, jsonify, send_file
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



# OUTPUT_DIR = "D:\AI\ComfyUI_windows_portable\ComfyUI\output"

# @workflow_bp.route("/get-result/<user_id>", methods=["GET"])
# def get_result(user_id):
#     for file in sorted(os.listdir(OUTPUT_DIR), reverse=True):
#         if file.startswith(user_id):
#             return send_file(os.path.join(OUTPUT_DIR, file), mimetype="image/png")
#     return jsonify({"error": "no image found"}), 404