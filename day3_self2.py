from pathlib import Path
from datetime import date
import json
from agents.image import batch_generate

with open("scene_prompts.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)
out_dir = Path("outputs") / date.today().isoformat()
out_dir.mkdir(parents=True, exist_ok=True)
batch_generate(scenes["scenes"], "gpt", out_dir)

# scenes = json.loads("scene_prompts.json")
# out_dir = Path("outputs") / date.today().isoformat()
# out_dir.mkdir(parents=True, exist_ok=True)
# batch_generate(scenes["scenes"], "flux", out_dir)
