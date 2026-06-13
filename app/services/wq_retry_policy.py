from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class RemoteWaitDecision:
    category: str
    wait_seconds: int
    reason: str


def next_wait_seconds(
    failure_count: int,
    short_seconds: int = 30,
    long_seconds: int = 600,
    cycle_size: int = 5,
) -> int:
    count = max(1, int(failure_count or 1))
    cycle = max(1, int(cycle_size or 5))
    if count % cycle == 0:
        return max(int(short_seconds), int(long_seconds))
    return int(short_seconds)


def classify_post_exception(
    exc: Exception,
    failure_count: int,
    short_wait_seconds: int = 30,
    long_wait_seconds: int = 600,
) -> RemoteWaitDecision:
    if isinstance(exc, (requests.exceptions.RequestException, OSError, ConnectionResetError)):
        wait_seconds = int(long_wait_seconds) if int(failure_count or 1) >= 3 else int(short_wait_seconds)
        return RemoteWaitDecision(
            "network",
            wait_seconds,
            "network_disconnect",
        )
    return RemoteWaitDecision("error", 0, "non_retryable")


def should_retry_without_skipping(decision: RemoteWaitDecision) -> bool:
    return decision.category in {"rate_limit", "network"}
