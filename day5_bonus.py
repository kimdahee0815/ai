
from openai import OpenAI
from dotenv import load_dotenv
import fal_client
import base64
from pathlib import Path
import requests

load_dotenv()
client=OpenAI()
Path("outputs").mkdir(exist_ok=True)

base = "narrow cobblestone alley, aged buildings, watercolor diary illustration, travel journal style"

time_variants = [
    ("golden_hour", f"{base}, golden hour warm lighting, orange and amber tones, long soft shadows, bokeh background"),
    ("blue_hour",   f"{base}, blue hour cool lighting, twilight purple-blue tones, soft glowing windows, calm atmosphere"),
]

for light_name, prompt in time_variants:
    output_path=f"outputs/travel_{light_name}.png"
    response = client.images.generate(
        model="gpt-image-1.5",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )
    b64_data=response.data[0].b64_json
    
    img_data = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(img_data)
        
    print(f"{light_name} 여행 사진 생성 완료. -> {output_path}")

print("여행 블로그 이미지 (golden hour vs blue hour) 생성 완료")

