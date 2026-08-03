from __future__ import annotations

import hashlib
import random
from datetime import date
from typing import Iterable, Sequence


# Stable reference date: the daily plan is determined by the calendar, so it
# survives browser restarts, Streamlit reboots and future GitHub deployments.
ROTATION_EPOCH = date(2026, 1, 1)


def _catalogue_order(lesson_ids: Sequence[str]) -> list[str]:
    """Return one stable, deterministic order for the complete catalogue."""
    order = list(lesson_ids)
    seed_text = "germany-plus-daily-rotation|" + "|".join(order)
    seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:16], 16)
    random.Random(seed).shuffle(order)
    return order


def daily_lesson_index(day: date, lesson_count: int) -> int:
    """Return today's position in the automatic catalogue cycle."""
    if lesson_count <= 0:
        raise ValueError("lesson_count must be greater than zero")
    return (day - ROTATION_EPOCH).days % lesson_count


def lesson_order_for_day(day: date, lesson_ids: Sequence[str]) -> list[str]:
    """Return today's topic first, then every other topic without repetition."""
    if not lesson_ids:
        raise ValueError("lesson_ids cannot be empty")
    catalogue = _catalogue_order(lesson_ids)
    start = daily_lesson_index(day, len(catalogue))
    return catalogue[start:] + catalogue[:start]


def daily_lesson_id(day: date, lesson_ids: Sequence[str]) -> str:
    return lesson_order_for_day(day, lesson_ids)[0]


def next_lesson_id(
    day: date,
    lesson_ids: Sequence[str],
    completed_lesson_ids: Iterable[str],
) -> str:
    """Choose the next same-day session.

    The daily topic is always first. Extra sessions continue through every other
    topic before any topic repeats. After completing the entire catalogue in one
    day, a new pass begins; question and vocabulary order are still reshuffled
    by the app for each individual session.
    """
    order = lesson_order_for_day(day, lesson_ids)
    completed = [lesson_id for lesson_id in completed_lesson_ids if lesson_id in order]
    completed_set = set(completed)

    for lesson_id in order:
        if lesson_id not in completed_set:
            return lesson_id

    return order[len(completed) % len(order)]
