from jinja2 import Template
import json, uuid, requests, time
from flask import current_app

def run_workflow(params: dict):
    # Load template once (better to cache this at app startup)
    with open("app/input/workflow1.json.j2", "r", encoding="utf-8") as f:
        template_str = f.read()

    # Default values if user doesn't supply
    defaults = {
        "seed": int(time.time()),  # unique seed per run
        "steps": 20,
        "cfg": 8,
        "prompt": "black photo",
        "filename_prefix": f"run_{uuid.uuid4().hex[:8]}"
    }

    # Merge defaults + user params
    merged = {**defaults, **params}

    # Render template
    rendered = Template(template_str).render(**merged)
    workflow = json.loads(rendered)

    # Send to ComfyUI
    client_id = str(uuid.uuid4())
    r = requests.post(
        f"{current_app.config['HOST']}/prompt",
        json={"prompt": workflow, "client_id": client_id}
    )

    return {
        "status_code": r.status_code,
        "response": r.json() if r.headers.get("Content-Type") == "application/json" else r.text
    }