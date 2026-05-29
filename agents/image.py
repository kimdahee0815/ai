import os, requests, json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import fal_client
import base64

load_dotenv()

COMMON_STYLE = "watercolor diary illustration, muted gray-blue city palette, quiet urban street, cloudy afternoon mood, soft pencil outline"

def call_dalle(prompt: str, seed: int | None = None) -> str:
    """Chat gpt 2로 1장 생성, URL 반환."""
    client = OpenAI()
    response = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png" # gpt-image-2 모델 항상 base64 반환
    )
    return response.data[0].b64_json

def call_flux(prompt: str, seed: int = 42) -> str:
    """FLUX로 1장 생성, URL 반환. seed로 일관성 강화."""
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "num_images":1,
            "seed": seed
        }
    )
    fal_image_url = result["images"][0]["url"]
    return fal_image_url

# def generate_image(prompt: str, model: str = "gpt", seed: int = 42) -> str:
#     """모델 분기 함수. GPT 또는 FLUX 호출."""
#     model = model.lower()
    
#     if model == "gpt":
#         result = call_dalle(prompt)
#     else:
#         result = call_flux(prompt, seed)
#     return result

def generate_image(prompt: str, model: str = "gpt", output_path: str="", seed: int = 42) -> str:
    """모델 분기 함수. GPT 또는 FLUX 호출."""
    model = model.lower()
    
    if model == "gpt":
        result = call_dalle(prompt)
        if output_path != "":
            image_bytes=base64.b64decode(result)
            output_path.write_bytes(image_bytes)
            return output_path
    else:
        result = call_flux(prompt, seed)
        if output_path != "":
            image_bytes=requests.get(result)
            output_path.write_bytes(image_bytes.content)
            return output_path
    return result

def save_image(model:str, data: str, out_path: Path) -> None:
    model = model.lower()

    if model == "gpt":
        image_bytes=base64.b64decode(data)
        out_path.write_bytes(image_bytes)
    else:
        image_bytes=requests.get(data)
        out_path.write_bytes(image_bytes.content)

def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    """scenes 리스트를 받아 4장 일괄 생성 후 저장 경로 반환. try/except로 한 장 실패 시 격리."""
    saved: list[Path] = []
    for idx, scene in enumerate(scenes):
        try:
            result = generate_image(prompt=scene["prompt_en"] + ", " + COMMON_STYLE, model=model, seed=scene["scene_id"])
            filename = f"scene_{scene['scene_id']:02d}.png"
            save_image(model, result, out_dir / filename)
            saved.append(out_dir / filename)
        except Exception as e:
            print(f"[실패] {scene}[{idx}] : {e}")
            continue
    return saved
