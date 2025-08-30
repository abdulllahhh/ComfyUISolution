# comfy_simple_run.py
import json
import uuid
import requests

HOST = "http://127.0.0.1:8188"

def run_workflow(workflow_file: str):
    # Load workflow json
    with open(workflow_file, "r", encoding="utf-8") as f:
        wf = json.load(f)

    # Normalize (some exports wrap as {"prompt": {...}})
    if isinstance(wf, dict) and "prompt" in wf:
        prompt = wf["prompt"]
    else:
        prompt = wf

    # Send to ComfyUI
    client_id = str(uuid.uuid4())
    r = requests.post(f"{HOST}/prompt",
                      json={"prompt": prompt, "client_id": client_id})
    print("Status:", r.status_code)
    print("Response:", r.text)

if __name__ == "__main__":
    run_workflow("api2.json")
