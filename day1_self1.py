import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def load_api_key() -> str:
    load_dotenv()
    open_api_key: str | None = os.getenv("OPENAI_API_KEY")
    
    if open_api_key is None:
        return ""
    else:
        return open_api_key[:5]
    
def build_scene_prompt() -> str:
    prompt = """
    medium shot, cloudy afternoon crosswalk, single ray of sunlight,
people waiting at traffic light, soft gray sky, cafe reflection on glass,
cool wind, watercolor diary illustration
    """
    return prompt

def generate_image(client:OpenAI, prompt:str) -> str:
    response = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png" # gpt-image-2 모델 항상 base64 반환
    )
    return response.data[0].b64_json;

def save_image(image_b64: str, out_path: Path) -> None:
    image_bytes=base64.b64decode(image_b64)
    out_path.write_bytes(image_bytes)
    
if __name__ == "__main__":
    load_api_key()
    client = OpenAI()              
    prompt = build_scene_prompt()
    print(f"[프롬프트] {prompt}")
    image_b64 = generate_image(client, prompt)
    print(f"[응답 base64] {image_b64[:60]}...")
    out_path = Path("outputs") / "scene01_dalle.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(image_b64, out_path)
    print(f"[저장 완료] {out_path}")
