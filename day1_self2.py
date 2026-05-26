import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def build_prompt_variants() -> list[tuple[str, str]]:
    variants: list[tuple[str, str]] = [
        (
            "scene01_ws.png",
            "wide shot, eye-level, rim light, cloudy afternoon crosswalk, single ray of sunlight, people waiting at traffic light, soft gray sky, cafe reflection on glass, cool wind, watercolor diary illustration"
        ),
        (
            "scene01_cu.png",
            "close-up, eye-level, soft front, cloudy afternoon crosswalk, single ray of sunlight, people waiting at traffic light, soft gray sky, cafe reflection on glass, cool wind, watercolor diary illustration"
        ),
        (
            "scene01_bs.png",
            "Bust shot, low angle, backlit, cloudy afternoon crosswalk, single ray of sunlight, people waiting at traffic light, soft gray sky, cafe reflection on glass, cool wind, watercolor diary illustration"
        ),
    ]
    return variants

def call_dalle(client:OpenAI, prompt:str) -> str:
    response = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png" # gpt-image-2 모델 항상 base64 반환
    )
    return response.data[0].b64_json

def save_image(image_b64: str, out_path: Path) -> None:
    image_bytes=base64.b64decode(image_b64)
    out_path.write_bytes(image_bytes)

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    variants = build_prompt_variants()
    for filename, prompt in variants:
        print(f"[호출 시작] {filename} ...")
        try:
            image_b64 = call_dalle(client, prompt)
            save_image(image_b64, output_dir/filename)
            print(f"[저장 완료] {filename}")
        except Exception as e:
            print(f"[실패] {filename} : {e}")
            continue
    
    print("\n끝. outputs/ 폴더에서 3장을 비교해 보세요.")
