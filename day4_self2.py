from pathlib import Path
import fal_client
from fal_client import Completed, InProgress, Queued
import time
import requests
from agents.video import status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget
from datetime import datetime
import asyncio

async def poll_and_download(task_id):

    iteration = 0
    start_ts = time.time()
    status = ""
    
    while True:
        if not (check_max_iter(iteration) and check_timeout(start_ts)):
            print("[가드 발동] 중단")
            break

        status = await status_kling(task_id)
        print(f"[{iteration}] status: {status}")

        if check_predicate(status):
            break

        iteration += 1
        time.sleep(5)

    # 루프 종료 후 저장
    if check_predicate(status):
        video_url = await result_kling(task_id)

        today = datetime.now().strftime("%Y-%m-%d")  
        output_dir = Path("outputs") / today
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "scene_1.mp4"

        response = requests.get(video_url, timeout=30)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)

        size_kb = output_path.stat().st_size // 1024
        print(f"저장 경로: {output_path} ({size_kb} KB)")
    else:
        print("[실패] 가드 발동으로 영상 저장 안 됨")

if __name__ == "__main__":
    from pipeline import picture_diary_pipeline
    
    KLING_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"
    task_id = Path("kling_task_id.txt").read_text().strip()
    print(f"self1에서 받은 task_id: {task_id}")

    while True:
        status = fal_client.status(KLING_MODEL, task_id, with_logs=False)
        print(f"status: {type(status).__name__}")
        if isinstance(status, Completed):
            break
        time.sleep(0.5)

    asyncio.run(poll_and_download(task_id))

    diary_text = Path("diary.md").read_text(encoding="utf-8")

    result = picture_diary_pipeline(diary_text=diary_text, animate_first=False)

    print("\n" + "="*50)
    print("📔 그림일기 생성 완료")
    print("="*50)

    print(f"\n📝 장면 ({len(result['scenes'])}개)")
    for i, scene in enumerate(result['scenes'], 1):
        print(f"  {i}. {scene['scene_kr']}")

    print(f"\n🖼️  이미지 ({len(result['images'])}개)")
    for path in result['images']:
        print(f"  - {path}")

    if result['video']:
        print(f"\n🎬 영상\n  - {result['video']}")

    print("\n" + "="*50)