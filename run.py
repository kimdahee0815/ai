import sys
from pathlib import Path
from module import extract_scenes, save_scenes, validate_scenes
from day2_self1 import load_draft

print("[1] 장면 추출 중...")
draft = load_draft(Path("scene_draft.md"))
scenes = extract_scenes(draft)
print(f"-> {len(scenes)}개 장면 추출 완료")
print("[2] 장면 검증 중")
errors = validate_scenes(scenes)
if errors:
    for err in errors:
        print(f"-> {err}")
    sys.exit(1)
else:
    print("-> 검증 통과 (4장면, 7필드)")

print("[3] scene_prompts.json 저장 중 ...")
save_scenes(scenes, "scene_prompts.json")
print(" -> 저장완료")