from __future__ import annotations

import hashlib
import html
import random
import uuid
from pathlib import Path
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Any

import streamlit as st
from PIL import Image

from germany_plus.content import (
    ALL_VOCABULARY,
    LESSONS,
    LESSON_BY_ID,
    VOCABULARY_BY_ID,
    Lesson,
    VocabularyItem,
)
from germany_plus.metrics import completed_dates, current_streak, lessons_this_week
from germany_plus.srs import due_word_ids, mastery_percent, update_vocabulary_progress
from germany_plus.storage import default_state, load_state, save_state
from germany_plus.theme import apply_theme, wordmark


APP_ICON = Image.open(Path(__file__).resolve().parent / "assets" / "germany_plus_icon.png")

st.set_page_config(
    page_title="Germany+ — Alemán A1 para Lula",
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)
apply_theme()


NAV_ITEMS = ["Inicio", "Lección", "Repaso", "Progreso"]

LOCAL_TZ = ZoneInfo("America/Santiago")


def _local_now() -> datetime:
    return datetime.now(LOCAL_TZ)


def _today() -> date:
    return _local_now().date()


CATEGORY_ORDER = [
    "Vida diaria",
    "Conversación",
    "Universidad",
    "Trabajo",
    "Viajes",
    "Comida",
    "Salud",
    "Tiempo libre",
]


def _initialise() -> None:
    if "app_state" not in st.session_state:
        state, source, error = load_state()
        st.session_state.app_state = state
        st.session_state.storage_source = source
        st.session_state.storage_error = error
    if "main_nav" not in st.session_state:
        st.session_state.main_nav = "Inicio"
    if "home_nonce" not in st.session_state:
        st.session_state.home_nonce = uuid.uuid4().hex


def _persist() -> None:
    source, error = save_state(st.session_state.app_state)
    st.session_state.storage_source = source
    st.session_state.storage_error = error


def _safe_state() -> dict[str, Any]:
    state = st.session_state.app_state
    if not isinstance(state, dict):
        state = default_state()
        st.session_state.app_state = state
    state.setdefault("sessions", [])
    state.setdefault("vocabulary", {})
    state.setdefault("xp", 0)
    state.setdefault("preferences", {})
    return state


def _go(page: str) -> None:
    st.session_state.pending_nav = page
    st.rerun()


def _seed(*parts: object) -> int:
    raw = "|".join(str(part) for part in parts)
    return int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16], 16)


def _today_lesson() -> Lesson:
    rng = random.Random(_seed(_today().isoformat(), st.session_state.home_nonce))
    return rng.choice(LESSONS)


def _shuffled(values: list[str] | tuple[str, ...], *seed_parts: object) -> list[str]:
    output = list(values)
    random.Random(_seed(*seed_parts)).shuffle(output)
    return output


def _start_lesson(lesson: Lesson | None = None) -> None:
    lesson = lesson or _today_lesson()
    token = uuid.uuid4().hex
    vocab_ids = [item.id for item in lesson.vocabulary]
    random.Random(_seed(token, lesson.id, "vocab-order")).shuffle(vocab_ids)
    st.session_state.lesson_run = {
        "token": token,
        "lesson_id": lesson.id,
        "phase": "reading",
        "index": 0,
        "reading_correct": 0,
        "vocabulary_correct": 0,
        "answers": {},
        "vocab_ids": vocab_ids,
        "started_at": _local_now().isoformat(timespec="seconds"),
    }
    st.session_state.pending_nav = "Lección"
    st.rerun()


def _clear_lesson() -> None:
    st.session_state.pop("lesson_run", None)
    st.session_state.home_nonce = uuid.uuid4().hex
    st.session_state.pending_nav = "Inicio"
    st.rerun()


def _lesson_progress(run: dict[str, Any]) -> tuple[int, int]:
    phase = run.get("phase")
    index = int(run.get("index") or 0)
    if phase == "reading":
        return 0, 20
    if phase == "comprehension":
        return index, 20
    if phase == "vocabulary":
        return 10 + index, 20
    return 20, 20


def _vocab_question(item: VocabularyItem, *, token: str, index: int) -> dict[str, Any]:
    reverse = index % 2 == 1
    pool = [candidate for candidate in ALL_VOCABULARY if candidate.id != item.id]
    rng = random.Random(_seed(token, item.id, index, "vocab-question"))
    distractors = rng.sample(pool, 3)
    if reverse:
        prompt = f"¿Cómo se dice «{item.spanish}» en alemán?"
        answer = item.german
        options = [item.german] + [candidate.german for candidate in distractors]
    else:
        prompt = f"¿Qué significa «{item.german}»?"
        answer = item.spanish
        options = [item.spanish] + [candidate.spanish for candidate in distractors]
    rng.shuffle(options)
    return {"prompt": prompt, "answer": answer, "options": options}


def _complete_lesson(run: dict[str, Any], lesson: Lesson) -> None:
    state = _safe_state()
    token = str(run["token"])
    if any(str(session.get("id")) == token for session in state["sessions"]):
        run["phase"] = "complete"
        return

    reading_correct = int(run.get("reading_correct") or 0)
    vocabulary_correct = int(run.get("vocabulary_correct") or 0)
    total_correct = reading_correct + vocabulary_correct
    earned_xp = 10 + total_correct * 2
    state["sessions"].append(
        {
            "id": token,
            "date": _today().isoformat(),
            "completed_at": _local_now().isoformat(timespec="seconds"),
            "lesson_id": lesson.id,
            "category": lesson.category,
            "reading_correct": reading_correct,
            "vocabulary_correct": vocabulary_correct,
            "total_correct": total_correct,
            "xp": earned_xp,
        }
    )
    state["sessions"] = state["sessions"][-400:]
    state["xp"] = int(state.get("xp") or 0) + earned_xp
    run["earned_xp"] = earned_xp
    run["phase"] = "complete"
    _persist()


def _top() -> str:
    wordmark()
    if "pending_nav" in st.session_state:
        st.session_state.main_nav = st.session_state.pop("pending_nav")
    with st.container(key="main_navigation"):
        selected = st.radio(
            "Navegación principal",
            NAV_ITEMS,
            horizontal=True,
            label_visibility="collapsed",
            key="main_nav",
        )
    return selected


def _storage_note() -> None:
    source = html.escape(str(st.session_state.storage_source))
    if source == "Supabase":
        copy = "Progreso guardado en Supabase."
    elif "respaldo" in source:
        copy = "Supabase no respondió; se está usando el respaldo local."
    else:
        copy = "Modo local de prueba. Para conservar el progreso en Streamlit Cloud, conecta Supabase."
    st.markdown(f'<div class="gp-storage"><strong>Datos:</strong> {source} · {html.escape(copy)}</div>', unsafe_allow_html=True)
    if st.session_state.storage_error:
        with st.expander("Ver detalle técnico del almacenamiento"):
            st.code(str(st.session_state.storage_error))


def _stats_html(state: dict[str, Any]) -> None:
    streak = current_streak(state, today=_today())
    week = lessons_this_week(state, today=_today())
    xp = int(state.get("xp") or 0)
    st.markdown(
        f"""
        <div class="gp-stats">
          <div class="gp-stat">
            <div class="gp-stat-label">Racha</div>
            <div class="gp-stat-value">{streak} días</div>
            <div class="gp-stat-note">Constancia antes que intensidad</div>
          </div>
          <div class="gp-stat">
            <div class="gp-stat-label">Esta semana</div>
            <div class="gp-stat-value">{week} / 7</div>
            <div class="gp-stat-note">Meta flexible: una sesión diaria</div>
          </div>
          <div class="gp-stat">
            <div class="gp-stat-label">Experiencia</div>
            <div class="gp-stat-value">{xp} XP</div>
            <div class="gp-stat-note">Se gana al completar, no al abrir</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    state = _safe_state()
    lesson = _today_lesson()
    due_count = len(due_word_ids(state["vocabulary"], today=_today()))

    st.markdown(
        """
        <section class="gp-hero">
          <h1 class="gp-greeting">Hallo Lula 🍂</h1>
          <p class="gp-subtitle">Kleine Schritte, große Fortschritte. Alemán útil, desde cero y sin apuro.</p>
          <span class="gp-level">Nivel actual · A1 inicial</span>
        </section>
        """,
        unsafe_allow_html=True,
    )
    _stats_html(state)

    st.markdown('<div class="gp-section-title">Lección de hoy</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <section class="gp-lesson-card">
          <div class="gp-lesson-accent"></div>
          <div class="gp-lesson-inner">
            <div class="gp-kicker">{html.escape(lesson.category)} · {lesson.level}</div>
            <div class="gp-lesson-title">{html.escape(lesson.title_de)}</div>
            <div class="gp-lesson-copy">{html.escape(lesson.title_es)}. Lectura breve, 10 preguntas de comprensión y 10 de vocabulario con ayuda en español.</div>
            <div class="gp-meta-row">
              <span class="gp-chip">{lesson.minutes} minutos</span>
              <span class="gp-chip">20 preguntas</span>
              <span class="gp-chip">Explicaciones en español</span>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([2, 1])
    if c1.button("Comenzar lección", type="primary", width="stretch"):
        _start_lesson(lesson)
    if c2.button("Cambiar tema", width="stretch"):
        st.session_state.home_nonce = uuid.uuid4().hex
        st.rerun()

    st.markdown('<div class="gp-section-title">Repaso inteligente</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="gp-card">
          <h3>{due_count} palabras para repasar</h3>
          <p class="gp-helper">Las palabras reaparecen según tus aciertos y errores. Las que cuestan vuelven antes; las dominadas se espacian.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Ir al repaso", width="stretch"):
        _go("Repaso")

    st.markdown('<div class="gp-section-title">Contextos A1</div>', unsafe_allow_html=True)
    category_counts: dict[str, int] = {}
    for item in LESSONS:
        category_counts[item.category] = category_counts.get(item.category, 0) + len(item.vocabulary)
    cards = "".join(
        f'<div class="gp-category"><div class="gp-cat-line"></div><strong>{html.escape(category)}</strong><span>{category_counts.get(category, 0)} palabras iniciales</span></div>'
        for category in CATEGORY_ORDER
    )
    st.markdown(f'<div class="gp-category-grid">{cards}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    _storage_note()


def _render_reading(run: dict[str, Any], lesson: Lesson) -> None:
    paragraphs = "".join(f"<p>{html.escape(paragraph)}</p>" for paragraph in lesson.paragraphs)
    st.markdown(
        f"""
        <div class="gp-card">
          <span class="gp-question-number">Paso 1 de 3</span>
          <h2>{html.escape(lesson.title_de)}</h2>
          <p class="gp-helper">Lee sin traducir palabra por palabra. Busca primero quién, dónde, cuándo y qué ocurre.</p>
          <div class="gp-reading">{paragraphs}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_help = bool(_safe_state()["preferences"].get("show_spanish_help", True))
    with st.expander("Ayuda en español", expanded=show_help):
        for paragraph in lesson.spanish_help:
            st.write(f"• {paragraph}")
        st.info(lesson.grammar_note)
    if st.button("Ya leí, comenzar comprensión", type="primary", width="stretch"):
        run["phase"] = "comprehension"
        run["index"] = 0
        st.rerun()


def _render_comprehension(run: dict[str, Any], lesson: Lesson) -> None:
    index = int(run["index"])
    question = lesson.questions[index]
    answer_key = f"reading:{index}"
    prior = run["answers"].get(answer_key)
    options = _shuffled(question.options, run["token"], lesson.id, index, "reading-options")

    st.markdown(
        f"""
        <div class="gp-card">
          <span class="gp-question-number">Comprensión · {index + 1} de 10</span>
          <div class="gp-question-title">{html.escape(question.prompt)}</div>
          <p class="gp-helper">Todas las alternativas están visibles. Elige una y luego presiona «Responder».</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    choice = st.radio(
        "Alternativas",
        options,
        index=None,
        label_visibility="collapsed",
        key=f"reading_choice_{run['token']}_{index}",
        disabled=prior is not None,
    )

    if prior is None:
        if st.button("Responder", type="primary", width="stretch"):
            if choice is None:
                st.warning("Selecciona una alternativa antes de responder.")
            else:
                is_correct = choice == question.answer
                run["answers"][answer_key] = {"choice": choice, "correct": is_correct}
                if is_correct:
                    run["reading_correct"] += 1
                st.rerun()
    else:
        if prior["correct"]:
            st.markdown(
                f'<div class="gp-feedback-ok"><strong>Correcto.</strong> {html.escape(question.explanation)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="gp-feedback-bad"><strong>Respuesta correcta:</strong> {html.escape(question.answer)}.<br>{html.escape(question.explanation)}</div>',
                unsafe_allow_html=True,
            )
        label = "Pasar a vocabulario" if index == 9 else "Siguiente pregunta"
        if st.button(label, type="primary", width="stretch"):
            if index == 9:
                run["phase"] = "vocabulary"
                run["index"] = 0
            else:
                run["index"] = index + 1
            st.rerun()


def _render_vocabulary(run: dict[str, Any], lesson: Lesson) -> None:
    index = int(run["index"])
    word_id = run["vocab_ids"][index]
    item = VOCABULARY_BY_ID[word_id]
    question = _vocab_question(item, token=run["token"], index=index)
    answer_key = f"vocabulary:{index}"
    prior = run["answers"].get(answer_key)

    st.markdown(
        f"""
        <div class="gp-card">
          <span class="gp-question-number">Vocabulario · {index + 1} de 10</span>
          <div class="gp-question-title">{html.escape(question['prompt'])}</div>
          <p class="gp-helper">No necesitas memorizar todo hoy. La aplicación volverá a mostrar cada palabra cuando corresponda.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    choice = st.radio(
        "Alternativas",
        question["options"],
        index=None,
        label_visibility="collapsed",
        key=f"vocab_choice_{run['token']}_{index}",
        disabled=prior is not None,
    )

    if prior is None:
        if st.button("Responder", type="primary", width="stretch"):
            if choice is None:
                st.warning("Selecciona una alternativa antes de responder.")
            else:
                is_correct = choice == question["answer"]
                run["answers"][answer_key] = {"choice": choice, "correct": is_correct}
                if is_correct:
                    run["vocabulary_correct"] += 1
                update_vocabulary_progress(
                    _safe_state()["vocabulary"],
                    item.id,
                    correct=is_correct,
                    today=_today(),
                )
                _persist()
                st.rerun()
    else:
        if prior["correct"]:
            feedback = '<div class="gp-feedback-ok"><strong>Correcto.</strong> Buen reconocimiento de la palabra.</div>'
        else:
            feedback = (
                f'<div class="gp-feedback-bad"><strong>Respuesta correcta:</strong> '
                f'{html.escape(question["answer"])}.<br>Esta palabra volverá antes en el repaso.</div>'
            )
        st.markdown(feedback, unsafe_allow_html=True)
        tip = f"<br><strong>Pista:</strong> {html.escape(item.tip)}" if item.tip else ""
        st.markdown(
            f"""
            <div class="gp-vocab-box">
              <div class="gp-vocab-word">{html.escape(item.german)} · {html.escape(item.spanish)}</div>
              <div class="gp-pronunciation">Pronunciación aproximada: /{html.escape(item.pronunciation)}/</div>
              <div class="gp-example">{html.escape(item.example_de)}<br>{html.escape(item.example_es)}{tip}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        label = "Finalizar lección" if index == 9 else "Siguiente palabra"
        if st.button(label, type="primary", width="stretch"):
            if index == 9:
                _complete_lesson(run, lesson)
            else:
                run["index"] = index + 1
            st.rerun()


def _render_complete(run: dict[str, Any], lesson: Lesson) -> None:
    reading = int(run.get("reading_correct") or 0)
    vocabulary = int(run.get("vocabulary_correct") or 0)
    total = reading + vocabulary
    earned = int(run.get("earned_xp") or (10 + total * 2))
    st.markdown(
        f"""
        <section class="gp-hero">
          <h1 class="gp-greeting">Sehr gut, Lula.</h1>
          <p class="gp-subtitle">Completaste «{html.escape(lesson.title_de)}» y sumaste {earned} XP.</p>
          <span class="gp-level">{total} de 20 respuestas correctas</span>
        </section>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    c1.metric("Comprensión", f"{reading}/10")
    c2.metric("Vocabulario", f"{vocabulary}/10")
    st.info("Equivocarse no rompe el progreso: las palabras difíciles ya quedaron programadas para reaparecer antes.")
    if st.button("Volver al inicio", type="primary", width="stretch"):
        _clear_lesson()


def render_lesson() -> None:
    if "lesson_run" not in st.session_state:
        lesson = _today_lesson()
        st.markdown(
            f"""
            <div class="gp-card">
              <h2>{html.escape(lesson.title_de)}</h2>
              <p class="gp-helper">No hay una lección en curso. Puedes iniciar la sugerida para hoy o volver al inicio.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Iniciar ahora", type="primary", width="stretch"):
            _start_lesson(lesson)
        return

    run = st.session_state.lesson_run
    lesson = LESSON_BY_ID.get(run.get("lesson_id"))
    if lesson is None:
        st.error("La lección guardada ya no existe. Se reinició de forma segura.")
        st.session_state.pop("lesson_run", None)
        return

    done, total = _lesson_progress(run)
    st.markdown(
        f'<div class="gp-progress-label"><span>{html.escape(lesson.title_es)}</span><span>{done}/{total}</span></div>',
        unsafe_allow_html=True,
    )
    st.progress(done / total if total else 0)

    phase = run.get("phase")
    if phase == "reading":
        _render_reading(run, lesson)
    elif phase == "comprehension":
        _render_comprehension(run, lesson)
    elif phase == "vocabulary":
        _render_vocabulary(run, lesson)
    elif phase == "complete":
        _render_complete(run, lesson)
    else:
        st.error("Estado de lección inválido. Puedes reiniciar sin perder el progreso ya guardado.")
        if st.button("Reiniciar lección", width="stretch"):
            _start_lesson(lesson)

    with st.expander("Opciones de la lección"):
        if st.button("Abandonar esta sesión", width="stretch"):
            st.session_state.pop("lesson_run", None)
            st.session_state.pending_nav = "Inicio"
            st.rerun()


def _make_review_queue() -> list[str]:
    state = _safe_state()
    due = [word_id for word_id in due_word_ids(state["vocabulary"], today=_today()) if word_id in VOCABULARY_BY_ID]
    return due[:20]


def _start_free_review() -> None:
    learned = [word_id for word_id in _safe_state()["vocabulary"] if word_id in VOCABULARY_BY_ID]
    pool = learned or [item.id for item in ALL_VOCABULARY]
    rng = random.Random(_seed(uuid.uuid4().hex, _today().isoformat(), "free-review"))
    queue = rng.sample(pool, min(5, len(pool)))
    st.session_state.review_run = {
        "token": uuid.uuid4().hex,
        "queue": queue,
        "index": 0,
        "answers": {},
        "correct": 0,
        "mode": "Práctica libre",
    }
    st.rerun()


def _start_due_review(queue: list[str]) -> None:
    st.session_state.review_run = {
        "token": uuid.uuid4().hex,
        "queue": queue,
        "index": 0,
        "answers": {},
        "correct": 0,
        "mode": "Repaso pendiente",
    }
    st.rerun()


def _render_review_run(run: dict[str, Any]) -> None:
    queue = [word_id for word_id in run.get("queue", []) if word_id in VOCABULARY_BY_ID]
    if not queue:
        st.warning("No quedan palabras válidas en esta ronda.")
        st.session_state.pop("review_run", None)
        return
    run["queue"] = queue
    index = min(int(run.get("index") or 0), len(queue) - 1)
    item = VOCABULARY_BY_ID[queue[index]]
    answer_key = str(index)
    prior = run["answers"].get(answer_key)
    rng = random.Random(_seed(run["token"], item.id, index, "review"))
    pool = [candidate for candidate in ALL_VOCABULARY if candidate.id != item.id]
    distractors = rng.sample(pool, 3)
    options = [item.spanish] + [candidate.spanish for candidate in distractors]
    rng.shuffle(options)

    st.markdown(
        f"""
        <div class="gp-card">
          <span class="gp-question-number">{html.escape(str(run.get('mode', 'Repaso')))} · {index + 1} de {len(queue)}</span>
          <div class="gp-question-title">¿Qué significa «{html.escape(item.german)}»?</div>
          <p class="gp-helper">El repaso usa solamente palabras existentes y filtra cualquier registro antiguo inválido.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    choice = st.radio(
        "Alternativas de repaso",
        options,
        index=None,
        label_visibility="collapsed",
        key=f"review_choice_{run['token']}_{index}",
        disabled=prior is not None,
    )
    if prior is None:
        if st.button("Responder", type="primary", width="stretch"):
            if choice is None:
                st.warning("Selecciona una alternativa.")
            else:
                correct = choice == item.spanish
                run["answers"][answer_key] = {"choice": choice, "correct": correct}
                run["correct"] = int(run.get("correct") or 0) + int(correct)
                update_vocabulary_progress(_safe_state()["vocabulary"], item.id, correct=correct, today=_today())
                _persist()
                st.rerun()
    else:
        feedback_class = "gp-feedback-ok" if prior["correct"] else "gp-feedback-bad"
        heading = "Correcto." if prior["correct"] else f"Respuesta correcta: {item.spanish}."
        st.markdown(
            f'<div class="{feedback_class}"><strong>{html.escape(heading)}</strong></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="gp-vocab-box">
              <div class="gp-vocab-word">{html.escape(item.german)} · {html.escape(item.spanish)}</div>
              <div class="gp-pronunciation">/{html.escape(item.pronunciation)}/</div>
              <div class="gp-example">{html.escape(item.example_de)}<br>{html.escape(item.example_es)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if index == len(queue) - 1:
            if st.button("Terminar repaso", type="primary", width="stretch"):
                st.session_state.review_summary = {
                    "correct": int(run.get("correct") or 0),
                    "total": len(queue),
                }
                st.session_state.pop("review_run", None)
                st.rerun()
        elif st.button("Siguiente palabra", type="primary", width="stretch"):
            run["index"] = index + 1
            st.rerun()


def render_review() -> None:
    state = _safe_state()
    if "review_summary" in st.session_state:
        summary = st.session_state.pop("review_summary")
        st.success(f"Repaso terminado: {summary['correct']} de {summary['total']} correctas.")

    if "review_run" in st.session_state:
        _render_review_run(st.session_state.review_run)
        return

    queue = _make_review_queue()
    learned_count = len(state["vocabulary"])
    mastery = mastery_percent(state["vocabulary"])
    st.markdown(
        f"""
        <section class="gp-hero">
          <h1 class="gp-greeting">Vokabel-Review</h1>
          <p class="gp-subtitle">Repaso breve, guiado en español y ajustado a lo que realmente cuesta.</p>
          <span class="gp-level">{len(queue)} pendientes · {learned_count} vistas · {mastery}% dominio</span>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if queue:
        st.markdown(
            '<div class="gp-card"><h3>Tu repaso está listo</h3><p class="gp-helper">Las palabras vencidas aparecen primero. Nunca se intenta abrir una palabra que ya no existe en el contenido.</p></div>',
            unsafe_allow_html=True,
        )
        if st.button(f"Repasar {len(queue)} palabras", type="primary", width="stretch"):
            _start_due_review(queue)
    else:
        st.markdown(
            '<div class="gp-card"><h3>No hay palabras pendientes</h3><p class="gp-helper">Eso no significa que todo esté memorizado: significa que el próximo repaso todavía no vence.</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("Practicar 5 palabras ahora", width="stretch"):
            _start_free_review()

    upcoming: list[tuple[str, str]] = []
    for word_id, progress in state["vocabulary"].items():
        if word_id in VOCABULARY_BY_ID and isinstance(progress, dict) and progress.get("next_due"):
            upcoming.append((str(progress["next_due"]), word_id))
    upcoming.sort()
    if upcoming:
        with st.expander("Próximos repasos"):
            for due_date, word_id in upcoming[:12]:
                item = VOCABULARY_BY_ID[word_id]
                st.write(f"**{item.german}** · {item.spanish} · {due_date}")


def _calendar_html(state: dict[str, Any]) -> str:
    done = completed_dates(state)
    today = _today()
    start = today - timedelta(days=27)
    cells: list[str] = []
    for offset in range(28):
        day = start + timedelta(days=offset)
        classes = ["gp-day"]
        if day in done:
            classes.append("done")
        if day == today:
            classes.append("today")
        cells.append(f'<div class="{" ".join(classes)}" title="{day.isoformat()}">{day.day}</div>')
    return '<div class="gp-calendar">' + "".join(cells) + "</div>"


def render_progress() -> None:
    state = _safe_state()
    sessions = state["sessions"]
    learned = len(state["vocabulary"])
    mastery = mastery_percent(state["vocabulary"])
    best_score = max((int(session.get("total_correct") or 0) for session in sessions), default=0)

    st.markdown(
        """
        <section class="gp-hero">
          <h1 class="gp-greeting">Fortschritt</h1>
          <p class="gp-subtitle">El progreso real es volver, comprender un poco más y mantenerlo en el tiempo.</p>
          <span class="gp-level">Nivel A1 · base en construcción</span>
        </section>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Lecciones", len(sessions))
    c2.metric("Palabras vistas", learned)
    c3.metric("Mejor resultado", f"{best_score}/20")

    st.markdown('<div class="gp-section-title">Últimos 28 días</div>', unsafe_allow_html=True)
    st.markdown(_calendar_html(state), unsafe_allow_html=True)

    st.markdown('<div class="gp-section-title">Dominio de vocabulario</div>', unsafe_allow_html=True)
    st.progress(mastery / 100 if mastery else 0)
    st.caption(f"{mastery}% según las cajas de repetición espaciada. Es una medida de práctica, no una certificación formal del nivel.")

    st.markdown('<div class="gp-section-title">Resultados recientes</div>', unsafe_allow_html=True)
    if not sessions:
        st.info("Aún no hay lecciones completadas.")
    else:
        rows = []
        for session in reversed(sessions[-10:]):
            lesson = LESSON_BY_ID.get(str(session.get("lesson_id")))
            rows.append(
                {
                    "Fecha": session.get("date", ""),
                    "Lección": lesson.title_es if lesson else session.get("lesson_id", ""),
                    "Resultado": f"{session.get('total_correct', 0)}/20",
                    "XP": session.get("xp", 0),
                }
            )
        st.dataframe(rows, width="stretch", hide_index=True)

    with st.expander("Preferencias y mantenimiento"):
        show_help = st.checkbox(
            "Abrir automáticamente la ayuda en español",
            value=bool(state["preferences"].get("show_spanish_help", True)),
        )
        if show_help != bool(state["preferences"].get("show_spanish_help", True)):
            state["preferences"]["show_spanish_help"] = show_help
            _persist()
            st.success("Preferencia guardada.")
        st.caption("El reinicio borra lecciones, vocabulario, racha y XP de Lula.")
        confirm = st.checkbox("Entiendo que se borrará todo el progreso", key="confirm_reset")
        if st.button("Reiniciar progreso", disabled=not confirm, width="stretch"):
            st.session_state.app_state = default_state()
            _persist()
            for key in ("lesson_run", "review_run", "review_summary"):
                st.session_state.pop(key, None)
            st.success("Progreso reiniciado.")
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    _storage_note()


_initialise()
with st.container():
    page = _top()
    if page == "Inicio":
        render_home()
    elif page == "Lección":
        render_lesson()
    elif page == "Repaso":
        render_review()
    else:
        render_progress()
