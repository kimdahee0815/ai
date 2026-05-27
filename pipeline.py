import json
from datetime import date
from pathlib import Path
from agents.scene import extract_scenes     
from agents.image import batch_generate    
from agents.video import submit_kling, status_kling, result_kling
import fal_client
import asyncio

def picture_diary_pipeline(diary_text: str, model: str = "flux", animate_first: bool = True) -> dict:
    """그림일기 통합 파이프라인. diary 텍스트 → scenes → images → (선택) 첫 장면 영상 → results.json."""
    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    scenes = extract_scenes(diary_text)

    image_paths = batch_generate(scenes, model, out_dir)
    
    video_url = None
    if animate_first == True:
        image_url = fal_client.upload_file(str(image_paths[0]))
        request_id = submit_kling(image_url, scenes[0]["prompt_en"])
        video_url = asyncio.run(result_kling(request_id))
        video_path = out_dir / "scene_1.mp4"

    metadata = {
        "diary_first_line": diary_text.splitlines()[0],
        "scenes": scenes,
        "image_paths": [str(p) for p in image_paths],
        "video_path": str(video_url) if video_url else None
    }
    (out_dir / "results.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return {"scenes": scenes, "images": metadata["image_paths"], "video": metadata["video_path"]}
