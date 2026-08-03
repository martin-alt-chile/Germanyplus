from datetime import date

from germany_plus.srs import due_word_ids, mastery_percent, update_vocabulary_progress


def test_correct_answer_moves_word_forward() -> None:
    state = {}
    progress = update_vocabulary_progress(state, "hallo", correct=True, today=date(2026, 8, 2))
    assert progress["box"] == 1
    assert progress["next_due"] == "2026-08-03"

    progress = update_vocabulary_progress(state, "hallo", correct=True, today=date(2026, 8, 3))
    assert progress["box"] == 2
    assert progress["next_due"] == "2026-08-06"


def test_wrong_answer_returns_to_box_one() -> None:
    state = {"hallo": {"box": 4, "correct": 4, "incorrect": 0}}
    progress = update_vocabulary_progress(state, "hallo", correct=False, today=date(2026, 8, 2))
    assert progress["box"] == 1
    assert progress["incorrect"] == 1


def test_due_words_are_safe_and_sorted() -> None:
    state = {
        "b": {"box": 2, "next_due": "2026-08-01"},
        "a": {"box": 1, "next_due": "2026-08-01"},
        "future": {"box": 1, "next_due": "2026-08-10"},
        "broken": "old-format",
    }
    assert due_word_ids(state, today=date(2026, 8, 2)) == ["a", "b"]


def test_mastery_percent() -> None:
    assert mastery_percent({}) == 0
    assert mastery_percent({"a": {"box": 5}, "b": {"box": 0}}) == 50
