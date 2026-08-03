from datetime import date, timedelta

from germany_plus.schedule import daily_lesson_id, lesson_order_for_day, next_lesson_id


LESSON_IDS = ["a", "b", "c", "d", "e", "f", "g", "h"]


def test_daily_topic_changes_every_day() -> None:
    start = date(2026, 8, 1)
    topics = [daily_lesson_id(start + timedelta(days=offset), LESSON_IDS) for offset in range(32)]
    assert all(current != following for current, following in zip(topics, topics[1:]))


def test_rotation_repeats_only_after_full_catalogue() -> None:
    day = date(2026, 8, 3)
    first_cycle = [daily_lesson_id(day + timedelta(days=offset), LESSON_IDS) for offset in range(len(LESSON_IDS))]
    assert len(set(first_cycle)) == len(LESSON_IDS)
    assert daily_lesson_id(day + timedelta(days=len(LESSON_IDS)), LESSON_IDS) == first_cycle[0]


def test_extra_sessions_use_each_topic_before_repeating() -> None:
    day = date(2026, 8, 3)
    order = lesson_order_for_day(day, LESSON_IDS)
    completed: list[str] = []
    selected: list[str] = []
    for _ in range(len(LESSON_IDS)):
        lesson_id = next_lesson_id(day, LESSON_IDS, completed)
        selected.append(lesson_id)
        completed.append(lesson_id)
    assert selected == order
    assert len(set(selected)) == len(LESSON_IDS)


def test_ninth_session_starts_a_new_cycle() -> None:
    day = date(2026, 8, 3)
    order = lesson_order_for_day(day, LESSON_IDS)
    assert next_lesson_id(day, LESSON_IDS, order) == order[0]
