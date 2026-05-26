import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client

def load_keys() -> None:
    """.env에서 FAL_KEY와 OPENAI_API_KEY를 로드합니다."""
    load_dotenv()
    fal_key: str | None = os.getenv("FAL_KEY")
    
    if fal_key is None:
        print("[FAL_KEY LOAD 오류]")
    else:
        print(f"FAL_KEY: {fal_key[:5]}")

def load_first_prompt() -> str:
    """scene_prompts.json에서 첫 번째 장면의 prompt_en을 반환합니다."""
    data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
    return data["scenes"][0]["prompt_en"]

def call_flux_schnell(prompt: str) -> str:
    """FLUX-schnell로 이미지 1장 생성, URL을 반환합니다."""
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "num_images":1
        }
    )
    fal_image_url = result["images"][0]["url"]
    return fal_image_url


def save_image(url: str, out_path: Path) -> None:
    """URL의 PNG 바이트를 내려받아 out_path에 저장합니다."""
    image_bytes=requests.get(url)
    out_path.write_bytes(image_bytes.content)

if __name__ == "__main__":
    load_keys()
    prompt = load_first_prompt()
    print(f"[프롬프트] {prompt[:60]}...")
    url = call_flux_schnell(prompt)
    print(f"[FLUX URL] {url[:60]}...")
    out_path = Path("outputs") / "scene01_fal.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(url, out_path)
    print(f"[저장 완료] {out_path}")