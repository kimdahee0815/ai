import os
from dotenv import load_dotenv
import fal_client
from datetime import datetime
from pathlib import Path
import requests
import asyncio

load_dotenv()

KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video" 

def submit_kling(image_url: str, prompt: str, duration: int = 5) -> str:
    handler = fal_client.submit(
        KLING_MODEL,
        arguments = {
            "image_url": image_url,
            "prompt": prompt,
            "duration": duration
        }
    )
    return handler.request_id

async def status_kling(request_id: str) -> str:
    """Kling status 1회 조회. 상태 문자열 반환."""
    status = await fal_client.status_async(
        KLING_MODEL,
        request_id=request_id,
        with_logs=False
    )
    return type(status).__name__

async def result_kling(request_id: str) -> str:
    """Kling 완료된 영상 결과 받기. 영상 URL 반환."""
    result = await fal_client.result_async(
        KLING_MODEL,
        request_id=request_id
    )
    # print(result)
    return result["video"]["url"]

async def generate_video(image_path: str, prompt: str, output_path: str) -> str:
    image_url = fal_client.upload_file(image_path)
    handler = fal_client.submit(
        KLING_MODEL,
        arguments={"image_url": image_url, "prompt": prompt}
    )
    request_id = handler.request_id

    # 폴링
    while True:
        status = await fal_client.status_async(KLING_MODEL, request_id=request_id, with_logs=False)
        if type(status).__name__ == "Completed":
            break
        await asyncio.sleep(3)

    result = await fal_client.result_async(KLING_MODEL, request_id=request_id)
    video_url = result["video"]["url"]

    response = requests.get(video_url, timeout=30)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

    return str(output_path)
        
