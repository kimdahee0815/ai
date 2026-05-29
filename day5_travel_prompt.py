from openai import OpenAI
from dotenv import load_dotenv
import base64
import json
from pathlib import Path

load_dotenv()
client = OpenAI()
Path("outputs").mkdir(exist_ok=True)

with open("domains/travel_prompts.json", "r", encoding="utf-8") as f:
    config = json.load(f)

style = config["prompt_style"]

style_base = ", ".join([
    style["shot"],
    style["lighting"],
    style["lens_or_style"],
    style["mood"]
])

def negative_to_positive(negative_str):
    """negative 항목을 'no X, without X' 형태로 변환"""
    items = [item.strip() for item in negative_str.split(",")]
    converted = [f"no {item}" for item in items if item]
    return ", ".join(converted)

for scene in config["scenes"]:
    scene_id = scene["id"]
    visual_focus = scene["visual_focus"]
    addons = ", ".join(scene["prompt_addons"])
    negative_as_positive = negative_to_positive(scene["negative_prompt"])

    prompt = f"{visual_focus}, {style_base}, {addons}, {negative_as_positive}"

    output_path = f"outputs/travel_{scene_id}.png"

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )

    b64_data = response.data[0].b64_json
    img_data = base64.b64decode(b64_data)

    with open(output_path, "wb") as f:
        f.write(img_data)

    print(f"[{scene_id}] 생성 완료 → {output_path}")
    print(f"  프롬프트: {prompt[:80]}...")

print("\n전체 씬 이미지 생성 완료")