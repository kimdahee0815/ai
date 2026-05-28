import json
from pathlib import Path

from ab_test import compute_p95, run_ab_test


BASE_DIR = Path(__file__).parent
DOMAIN_NAME = "travel"
N_CALLS = 3


def main() -> None:
    # Step 1. 도메인 프롬프트 JSON 로드
    domain_path = BASE_DIR / "domains" / f"{DOMAIN_NAME}_prompts.json"
    with open(domain_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    selected_scene = data["scenes"][0]
    prompt = selected_scene["diary_sentence"] + " " + " ".join(selected_scene["prompt_addons"])

    # Step 2. A/B 실행 + P95 계산
    time_list = run_ab_test(prompt=prompt, n_calls=N_CALLS)
    a_time_list = time_list["a"]
    b_time_list = time_list["b"]
    p95_a = compute_p95(a_time_list)
    p95_b = compute_p95(b_time_list)

    # Step 3. ab_test_results.json 저장
    result_path = BASE_DIR / "ab_test_results.json"
    ab_test_results = {
        "domain": DOMAIN_NAME,
        "seed": {"a": 42, "b": 137},
        "latencies": {"a": a_time_list, "b": b_time_list},
        "p95": {"a": p95_a, "b": p95_b},
    }
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(ab_test_results, f, ensure_ascii=False, indent=2)

    # Step 4. cost_report.md 작성
    report_path = BASE_DIR / "cost_report.md"
    report = f"""# 그림일기 파이프라인 5일 누적 비용 보고서

## 기본 정보

| 항목 | 값 |
|---|---|
| 작성 세션 | Day 5 self1 |
| 선택 도메인 | {DOMAIN_NAME} |
| A seed | 42 |
| B seed | 137 |
| A/B 호출 수 | A {N_CALLS}회 / B {N_CALLS}회 |

## 5일 누적 비용

| Day | 주요 작업 | 호출 수 | 단가 또는 추정 단가 | 합계 |
|---|---|---:|---:|---:|
| Day 1 | 환경 확인과 첫 호출 | 1 | $0.003 | $0.003 |
| Day 2 | 장면 JSON 생성 | 2 | $0.003 | $0.006 |
| Day 3 | 이미지 생성 | 3 | $0.003 | $0.009 |
| Day 4 | 영상 생성 | 2 | $0.050 | $0.100 |
| Day 5 self1 | 도메인 A/B 테스트 | {N_CALLS * 2} | $0.003 | ${N_CALLS * 2 * 0.003:.3f} |
| 합계 |  | {8 + N_CALLS * 2} |  | ${0.118 + N_CALLS * 2 * 0.003:.3f} |

## P95 지연

| 그룹 | seed | 호출 수 | P95 지연 |
|---|---:|---:|---:|
| A | 42 | {N_CALLS} | {p95_a:.3f}초 |
| B | 137 | {N_CALLS} | {p95_b:.3f}초 |

## README로 옮길 값

| 항목 | 값 |
|---|---:|
| p95_latency_s | {max(p95_a, p95_b):.3f} |
| cost_per_image | $0.003 |
| total_cost_usd | ${0.118 + N_CALLS * 2 * 0.003:.3f} |
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    main()
