# guardrails.py — 비동기 폴링 4종 가드
import time
from typing import Callable

MAX_ITER = 60
TIMEOUT_SEC = 300
BUDGET_CAP_USD = 0.50

def check_max_iter(iteration: int) -> bool:
    return iteration < MAX_ITER

def check_timeout(start_ts: float) -> bool:
    return time.time() - start_ts < TIMEOUT_SEC

def check_predicate(status: str, accept: tuple = ("completed", "succeeded")) -> bool:
    return status.lower() in accept

def check_budget(used_usd: float) -> bool:
    return used_usd < BUDGET_CAP_USD
