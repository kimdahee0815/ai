import subprocess
from pathlib import Path

def check_env_in_gitignore() -> bool:
    """.gitignore에 .env가 있는지 확인."""
    text = Path('.gitignore').read_text(encoding='utf-8')
    return '.env' in text

def check_env_in_staged() -> bool:
    """git staged 파일 목록에 .env가 없는지 확인 (False면 안전)."""
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        capture_output=True,
        text=True
    )
    return '.env' in result.stdout

if __name__ == "__main__":
    gitignore_safe = check_env_in_gitignore()
    staged_unsafe = check_env_in_staged()

    print(f".gitignore에 .env 등록: {gitignore_safe}")
    print(f".env가 staged에 포함됨: {staged_unsafe}")

    if gitignore_safe and not staged_unsafe:
        print("✅ push 가능")
    else:
        if not gitignore_safe:
            print("❌ .gitignore에 .env를 추가하세요")
        if staged_unsafe:
            print("❌ .env가 staged에 있습니다 — git reset HEAD .env 로 제거하세요")