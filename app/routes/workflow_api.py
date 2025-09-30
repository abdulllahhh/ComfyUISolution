import os
import base64
from flask import Blueprint, current_app, request, jsonify, send_file
from app.services.workflow_service import run_workflow

workflow_bp = Blueprint("workflow_api", __name__)

@workflow_bp.route("/run-model", methods=["POST"])
def run_model():
    data = request.get_json()
    if not data or "prompt" not in data or "user_id" not in data:
        return jsonify({"error": "user_id and prompt are required"}), 400
    
    result = run_workflow(params=data)
    if result["status_code"] != 200:
        return jsonify(result), result["status_code"]
    
    file_path = result["file_path"]
    
    try:
        response = send_file(
            file_path, 
            mimetype="image/png",
            as_attachment=False,
            download_name=result["filename"]
        )
        
        # Schedule cleanup after response is sent
        @response.call_on_close
        def cleanup():
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Failed to delete {file_path}: {e}")
        
        return response
    except Exception as e:
        current_app.logger.error(f"Failed to send file: {e}")
        return jsonify({"error": f"Failed to send file: {str(e)}"}), 500