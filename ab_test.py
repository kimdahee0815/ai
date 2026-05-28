import time
import statistics

from agents.image import generate_image


def time_one_call(prompt: str, seed: int, model: str = "flux") -> float:
    """이미지 1회 호출에 걸린 시간을 초 단위로 돌려주는 함수."""
    start_time = time.perf_counter()
    res = generate_image(prompt=prompt, seed=seed, model=model)
    end_time = time.perf_counter()
    return end_time - start_time


def run_ab_test(prompt: str, n_calls: int = 3) -> dict:
    """같은 prompt를 seed A/B로 나누어 여러 번 호출하는 함수."""
    seed_a = 42
    seed_b = 137
    time_a = []
    time_b = []
    for i in range(n_calls):
        a_total_time = time_one_call(prompt=prompt, seed=seed_a)
        time_a.append(a_total_time)
    for i in range(n_calls):
        b_total_time = time_one_call(prompt=prompt, seed=seed_b)
        time_b.append(b_total_time)
    return {
        "a": time_a,
        "b": time_b
    }


def compute_p95(latencies: list[float]) -> float:
    """지연 시간 목록에서 P95 값을 계산하는 함수."""
    if not latencies:
        return 0.0
    # n=20 => 5% 단위 분위수, index 18 = 95번째 백분위
    return statistics.quantiles(latencies, n=20)[18]


