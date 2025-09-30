from glob import glob
import os
from jinja2 import Template
import json, uuid, requests, time
from flask import current_app
OUTPUT_DIR = "D:\\AI\\ComfyUI_windows_portable\\ComfyUI\\output"
import logging

logger = logging.getLogger("waitress")  # use same logger as waitress
def run_workflow(params: dict):
    # Load Jinja2 template
    with open("app/input/workflow1.json.j2", "r", encoding="utf-8") as f:
        template_str = f.read()

    # Defaults
    defaults = {
        "user_id": params["user_id"],
        "seed": int(time.time()),  # unique seed per run
        "steps": 20,
        "cfg": 8,
        "prompt": "black photo",
        "uuid": uuid.uuid4().hex[:8]
    }

    # Add filename prefix => ensures we can find the output image
    defaults["filename_prefix"] = f"{defaults['user_id']}_{defaults['uuid']}"
    logger.info("Filename prefix:", defaults["filename_prefix"])
    # Merge params
    merged = {**defaults, **params}

    # Render template into workflow
    rendered = Template(template_str).render(**merged)
    workflow = json.loads(rendered)

    # Send to ComfyUI
    client_id = str(uuid.uuid4())
    r = requests.post(
        f"{current_app.config['HOST']}/prompt",
        json={"prompt": workflow, "client_id": client_id}
    )

    # Check if request was accepted
    if r.status_code != 200:
        return {
            "status_code": r.status_code,
            "response": r.text
        }

    # Wait briefly for Comfy to finish writing the output
    prefix = merged["filename_prefix"]
    pattern = os.path.join(OUTPUT_DIR, f"{prefix}*.png")

    file_path = None
    for _ in range(30):  # retry up to ~30s
        files = glob(pattern)
        if files:
            # get latest file
            file_path = max(files, key=os.path.getmtime)
            break
        time.sleep(1)

    if not file_path:
        return {
            "status_code": 500,
            "error": "Image not found in output folder"
        }

    # Return metadata (not raw image yet)
    return {
        "status_code": 200,
        "file_path": file_path,      # e.g. comfy/output/user_123_ab12cd.png
        "filename": os.path.basename(file_path),
        "comfy_response": r.json()
    }