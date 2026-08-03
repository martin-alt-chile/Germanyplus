from germany_plus.content import ALL_VOCABULARY, LESSONS, validate_content


def test_content_is_valid() -> None:
    validate_content()


def test_every_lesson_has_full_daily_flow() -> None:
    assert len(LESSONS) >= 8
    for lesson in LESSONS:
        assert lesson.level == "A1"
        assert len(lesson.paragraphs) in {2, 3}
        assert len(lesson.questions) == 10
        assert len(lesson.vocabulary) == 10


def test_vocabulary_ids_are_unique() -> None:
    ids = [item.id for item in ALL_VOCABULARY]
    assert len(ids) == len(set(ids))
