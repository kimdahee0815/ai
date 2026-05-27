from pathlib import Path

import fal_client

from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-27" / "scene_1.png"

image_url = fal_client.upload_file(str(IMAGE_PATH))

PROMPT = "static shot, gentle smile, eye blink, slight head turn, cinematic lighting"

request_id = submit_kling(image_url, PROMPT)
Path("kling_task_id.txt").write_text(request_id, encoding="utf-8")
print(f"task_id 저장 완료: {request_id}")