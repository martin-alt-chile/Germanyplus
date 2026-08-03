from __future__ import annotations

from datetime import date, timedelta
from typing import Any


INTERVAL_DAYS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}


def update_vocabulary_progress(
    vocabulary_state: dict[str, Any],
    word_id: str,
    *,
    correct: bool,
    today: date | None = None,
) -> dict[str, Any]:
    today = today or date.today()
    current = dict(vocabulary_state.get(word_id) or {})
    old_box = int(current.get("box") or 0)
    new_box = min(5, old_box + 1) if correct else 1
    interval = INTERVAL_DAYS[new_box]
    current.update(
        {
            "box": new_box,
            "next_due": (today + timedelta(days=interval)).isoformat(),
            "last_seen": today.isoformat(),
            "correct": int(current.get("correct") or 0) + int(correct),
            "incorrect": int(current.get("incorrect") or 0) + int(not correct),
        }
    )
    vocabulary_state[word_id] = current
    return current


def due_word_ids(vocabulary_state: dict[str, Any], today: date | None = None) -> list[str]:
    today = today or date.today()
    due: list[tuple[str, int, str]] = []
    for word_id, progress in vocabulary_state.items():
        if not isinstance(progress, dict):
            continue
        next_due = str(progress.get("next_due") or "")
        if next_due and next_due <= today.isoformat():
            due.append((word_id, int(progress.get("box") or 0), next_due))
    due.sort(key=lambda item: (item[2], item[1], item[0]))
    return [item[0] for item in due]


def mastery_percent(vocabulary_state: dict[str, Any]) -> int:
    if not vocabulary_state:
        return 0
    points = 0
    for progress in vocabulary_state.values():
        if isinstance(progress, dict):
            points += min(5, max(0, int(progress.get("box") or 0)))
    return round(points / (len(vocabulary_state) * 5) * 100)
