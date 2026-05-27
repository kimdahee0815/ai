import os
from dotenv import load_dotenv
import fal_client

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

# status_kling, result_kling 함수는 self2에서 작성
