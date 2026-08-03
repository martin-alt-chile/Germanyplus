from __future__ import annotations

from datetime import date, timedelta
from typing import Any


def completed_dates(state: dict[str, Any]) -> set[date]:
    values: set[date] = set()
    for session in state.get("sessions", []):
        try:
            values.add(date.fromisoformat(str(session["date"])))
        except (KeyError, TypeError, ValueError):
            continue
    return values


def current_streak(state: dict[str, Any], today: date | None = None) -> int:
    today = today or date.today()
    dates = completed_dates(state)
    if not dates:
        return 0
    cursor = today if today in dates else today - timedelta(days=1)
    streak = 0
    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def lessons_this_week(state: dict[str, Any], today: date | None = None) -> int:
    today = today or date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return sum(monday <= day <= sunday for day in completed_dates(state))


def total_correct_answers(state: dict[str, Any]) -> int:
    total = 0
    for session in state.get("sessions", []):
        total += int(session.get("reading_correct") or 0)
        total += int(session.get("vocabulary_correct") or 0)
    return total
