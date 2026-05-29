from openai import OpenAI
from dotenv import load_dotenv
import base64
from pathlib import Path
from day5_02_emoticons import APPEARANCE, EMOTIONS

load_dotenv()
client = OpenAI()
Path("outputs").mkdir(exist_ok=True)

for emotion, detail in EMOTIONS.items():
    prompt = (
        f"{APPEARANCE}, "
        f"emotion: {emotion}, {detail}, "
        "white background, centered, sticker style illustration"
    )

    output_path = f"outputs/emotion_{emotion}.png"

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

    print(f"[{emotion}] → {output_path}")

print("감정 캐릭터 이미지 생성 완료")