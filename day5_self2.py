from pathlib import Path
import fal_client
from fal_client import Completed, InProgress, Queued
import time
import requests
from agents.scene import extract_scenes
from agents.video import status_kling, result_kling, generate_video
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget
from datetime import datetime
import asyncio

if __name__ == "__main__":    
    KLING_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"

    diary_text = Path("diary.md").read_text(encoding="utf-8")

    image_path = Path("outputs") / "2026-05-28" / "scene_02.png"
    
    scenes = extract_scenes(diary_text)
    
    timestamp = datetime.now().strftime("%H%M%S")
    today = datetime.now().strftime("%Y-%m-%d")  
    output_dir = Path("outputs") / today
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path("outputs") / f"scene_{timestamp}.mp4"
    
    result = asyncio.run(generate_video(image_path=image_path, prompt=scenes[1]["prompt_en"], output_path=output_path))

    print(f"영상 저장 경로: {result}")

