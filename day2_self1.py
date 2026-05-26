from pathlib import Path
import re
REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]

def load_draft(path: Path) -> str:
    if path.exists():
        scene_draft = path.read_text(encoding="utf-8")
        print(f"[scene_draft.md] {len(scene_draft)}자 로드 완료")
        return scene_draft
    else:
        print(f"[로드 실패] [scene_draft.md]")
        return ""
    
def count_scenes(text: str) -> int:
    return len(re.findall(r'^## 장면 \d+', text, re.M))

def check_fields(text:str, scene_idx: int) -> list[str]:
    missing: list[str] = []

    sections = re.split(r'^## 장면 \d+', text, flags=re.M)
    section = sections[scene_idx]  # 장면 1 -> index 1
    missing = [f for f in REQUIRED_FIELDS if f + ":" not in section]
    
    return missing

if __name__ == "__main__":
    draft = load_draft(Path("scene_draft.md"))
    n = count_scenes(draft)
    print(f"[검출] 장면 수: {n}")
    for scene_idx in range(1, n+1):
        missing_fields = check_fields(draft, scene_idx)
        if len(missing_fields) != 0:
            print(f"[필드 누락] 장면{scene_idx}: {missing_fields}")
            continue
        print(f"장면{scene_idx}: OK")
    print("[완료] 모든 장면 OK이면 self2로 진행하세요.")