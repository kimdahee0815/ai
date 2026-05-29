from openai import OpenAI
from dotenv import load_dotenv
import base64
from pathlib import Path
from day5_01_product_catalog import angle_map, shot_map, products

load_dotenv()
client = OpenAI()
Path("outputs").mkdir(exist_ok=True)

for product in products:
    shot = shot_map[product["size"]]
    angle = angle_map[product["angle"]]

    prompt = (
        f"{product['desc']}, product photography, "
        f"{shot}, {angle}, "
        "clean white background, studio lighting with soft shadow, "
        "8k quality, commercial catalog style"
    )

    output_path = f"outputs/product_{product['name']}.png"

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )

    img_data = base64.b64decode(response.data[0].b64_json)
    with open(output_path, "wb") as f:
        f.write(img_data)

    print(f"[{product['name']}] {shot} / {angle} → {output_path}")

print("제품 카탈로그 이미지 생성 완료")