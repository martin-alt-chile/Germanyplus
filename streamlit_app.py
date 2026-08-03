from __future__ import annotations

import base64
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


NAV_ITEMS = ["Inicio", "Aprender", "Repaso", "Progreso"]
NAV_LABELS = {
    "Inicio": "⌂ Inicio",
    "Aprender": "▤ Aprender",
    "Repaso": "↻ Repaso",
    "Progreso": "▥ Progreso",
}

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
    st.session_state.pending_nav = "Aprender"
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
    wordmark(streak=current_streak(_safe_state(), today=_today()))
    if "pending_nav" in st.session_state:
        st.session_state.main_nav = st.session_state.pop("pending_nav")
    with st.container(key="main_navigation"):
        selected = st.radio(
            "Navegación principal",
            NAV_ITEMS,
            horizontal=True,
            format_func=lambda item: NAV_LABELS[item],
            label_visibility="collapsed",
            key="main_nav",
        )
    return selected



def _asset_data_uri(filename: str) -> str:
    """Return a local SVG/PNG as a data URI so Streamlit Cloud needs no static server."""
    path = Path(__file__).resolve().parent / "assets" / filename
    suffix = path.suffix.lower()
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(suffix, "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _friendly_explanation(text: str) -> str:
    """Make short A1 feedback sound like a tutor, not a database answer key."""
    cleaned = text.strip()
    exact = {
        "El texto dice que Lula es nueva en un curso de alemán.": "Al comienzo se cuenta que Lula acaba de entrar a un curso de alemán.",
        "El texto dice «Brot mit Käse».": "En el desayuno aparece «Brot mit Käse», que significa «pan con queso».",
        "El texto dice «Sie essen Suppe».": "La frase «Sie essen Suppe» significa que comen sopa.",
        "El texto dice «erster Tag» en la oficina.": "«Erster Tag» significa «primer día», y la escena ocurre en la oficina.",
        "El texto dice «um zehn Uhr».": "«Um zehn Uhr» significa «a las diez».",
        "El texto dice «Lula trifft Ana».": "«Lula trifft Ana» significa que Lula se encuentra con Ana.",
        "El texto dice «Das Café ist ruhig».": "«Das Café ist ruhig» significa que el café es tranquilo.",
        "El texto dice «sehr müde».": "«Sehr müde» significa «muy cansada».",
        "El texto dice «zwei Freunde».": "«Zwei Freunde» significa «dos amigos».",
    }
    if cleaned in exact:
        return exact[cleaned]
    if cleaned.startswith("El texto dice «"):
        return cleaned.replace("El texto dice", "En la lectura aparece", 1)
    if cleaned.startswith("El texto dice que "):
        return "La lectura cuenta que " + cleaned[len("El texto dice que "):]
    if cleaned.startswith("La última frase dice que "):
        return "Al final se cuenta que " + cleaned[len("La última frase dice que "):]
    return cleaned


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
    progress = max(0, min(100, round((week / 7) * 100)))
    st.markdown(
        f"""
        <div class="gp-stats-panel">
          <div class="gp-stat-block">
            <div class="gp-stat-label">🔥 Tu racha</div>
            <div class="gp-stat-value">{streak} días</div>
            <div class="gp-stat-note">Un poco cada día vale más que estudiar todo de golpe.</div>
          </div>
          <div class="gp-stat-block">
            <div class="gp-stat-label">Tu progreso semanal</div>
            <div class="gp-stat-value"><span class="accent">{week}</span> / 7 lecciones</div>
            <div class="gp-progress-track"><div class="gp-progress-fill" style="width:{progress}%"></div></div>
          </div>
          <div class="gp-stat-block gp-xp">
            <div class="gp-xp-star">★</div>
            <div class="gp-stat-value">{xp}</div>
            <div class="gp-stat-note">XP</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    state = _safe_state()
    lesson = _today_lesson()
    due_count = len(due_word_ids(state["vocabulary"], today=_today()))
    skyline = _asset_data_uri("berlin_skyline.svg")
    lesson_art = _asset_data_uri("lesson_scene.svg")

    st.markdown(
        f"""
        <section class="gp-home-header">
          <img class="gp-header-skyline" src="{skyline}" alt="Silueta ilustrada de Berlín">
          <div class="gp-header-copy">
            <h1 class="gp-greeting">Hallo Lula 🍂</h1>
            <p class="gp-subtitle">Pequeños pasos, grandes progresos. Alemán A1 con apoyo claro en español.</p>
            <span class="gp-level">A1 · recién comenzando</span>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    _stats_html(state)

    st.markdown('<div class="gp-section-title">Lección diaria</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <section class="gp-lesson-card">
          <img class="gp-lesson-art" src="{lesson_art}" alt="Escritorio otoñal con bandera alemana">
          <div class="gp-lesson-overlay"></div>
          <div class="gp-lesson-inner">
            <span class="gp-today-pill">HOY</span>
            <div class="gp-kicker">{html.escape(lesson.category)} · {lesson.level}</div>
            <div class="gp-lesson-title">{html.escape(lesson.title_de)}</div>
            <div class="gp-lesson-copy"><strong style="color:white">Tema:</strong> {html.escape(lesson.title_es)}.<br>Lectura corta, preguntas simples y ayudas en español cuando hagan falta.</div>
            <div class="gp-meta-row">
              <span class="gp-chip">◷ {lesson.minutes} min</span>
              <span class="gp-chip">20 preguntas</span>
              <span class="gp-chip">A1 guiado</span>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([2, 1])
    if c1.button("Comenzar", type="primary", width="stretch"):
        _start_lesson(lesson)
    if c2.button("Cambiar tema", width="stretch"):
        st.session_state.home_nonce = uuid.uuid4().hex
        st.rerun()

    sample_words = list(lesson.vocabulary[:4])
    vocab_rows = "".join(
        f'<div class="gp-mini-row"><div><strong>{html.escape(item.german)}</strong><span>{html.escape(item.spanish)}</span></div></div>'
        for item in sample_words
    )

    first_q = lesson.questions[0]
    quiz_token = f"{lesson.id}_{st.session_state.home_nonce}"
    quiz_result_key = f"home_quiz_result_{quiz_token}"
    quiz_result = st.session_state.get(quiz_result_key)
    quiz_options = _shuffled(first_q.options, quiz_token, "home-quiz")

    with st.container(key="home_features"):
        vocab_col, reading_col, quiz_col = st.columns(3, gap="small")
        vocab_col.markdown(
            f"""
            <div class="gp-feature-heading"><div class="gp-feature-icon gold-icon">Aa</div><div><div class="gp-feature-title">Repaso de vocabulario</div><div class="gp-feature-subtitle">Palabras clave con traducción</div></div></div>
            <div class="gp-mini-list">{vocab_rows}</div>
            """,
            unsafe_allow_html=True,
        )
        reading_col.markdown(
            f"""
            <div class="gp-feature-heading"><div class="gp-feature-icon red-icon">≡</div><div><div class="gp-feature-title">Leer y entender</div><div class="gp-feature-subtitle">Textos cortos para principiantes</div></div></div>
            <div class="gp-mini-reading"><strong>{html.escape(lesson.title_es)}</strong><p>{html.escape(lesson.spanish_help[0])}</p></div>
            """,
            unsafe_allow_html=True,
        )
        quiz_col.markdown(
            f"""
            <div class="gp-feature-heading"><div class="gp-feature-icon purple-icon">?</div><div><div class="gp-feature-title">Quiz rápido</div><div class="gp-feature-subtitle">Elige una alternativa</div></div></div>
            <div class="gp-mini-question">{html.escape(first_q.prompt)}</div>
            """,
            unsafe_allow_html=True,
        )
        home_choice = quiz_col.radio(
            "Alternativas del quiz rápido",
            quiz_options,
            index=None,
            label_visibility="collapsed",
            key=f"home_quiz_choice_{quiz_token}",
            disabled=quiz_result is not None,
        )
        if quiz_result is None:
            if quiz_col.button("Responder", key=f"home_quiz_button_{quiz_token}", width="stretch"):
                if home_choice is None:
                    quiz_col.warning("Elige una alternativa primero.")
                else:
                    st.session_state[quiz_result_key] = {
                        "choice": home_choice,
                        "correct": home_choice == first_q.answer,
                    }
                    st.rerun()
        else:
            explanation = html.escape(_friendly_explanation(first_q.explanation))
            if quiz_result.get("correct"):
                message = f'<div class="gp-feedback-ok gp-mini-feedback"><strong>¡Bien!</strong> {explanation}</div>'
            else:
                message = f'<div class="gp-feedback-bad gp-mini-feedback"><strong>Casi.</strong> La alternativa correcta es «{html.escape(first_q.answer)}». {explanation}</div>'
            quiz_col.markdown(message, unsafe_allow_html=True)

    st.markdown('<div class="gp-section-title">Repaso inteligente</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="gp-card"><h3>{due_count} palabras para repasar</h3><p class="gp-helper">Las palabras que cuestan vuelven antes. Las que ya manejas aparecen con menos frecuencia.</p></div>',
        unsafe_allow_html=True,
    )
    if st.button("Ir al repaso", width="stretch"):
        _go("Repaso")

    st.markdown('<div class="gp-section-title">Categorías</div>', unsafe_allow_html=True)
    category_counts: dict[str, int] = {}
    for item in LESSONS:
        category_counts[item.category] = category_counts.get(item.category, 0) + len(item.vocabulary)
    icons = {"Vida diaria": "☀", "Conversación": "💬", "Universidad": "A", "Trabajo": "▣", "Viajes": "✈", "Comida": "◉", "Salud": "+", "Tiempo libre": "♪"}
    cards = "".join(
        f'<div class="gp-category"><div class="gp-category-icon">{icons.get(category, "A")}</div><strong>{html.escape(category)}</strong><span>{category_counts.get(category, 0)} palabras A1</span><div class="gp-cat-progress"><i style="width:{min(85, 18 + idx * 7)}%"></i></div></div>'
        for idx, category in enumerate(CATEGORY_ORDER)
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
        explanation = html.escape(_friendly_explanation(question.explanation))
        answer = html.escape(question.answer)
        if prior["correct"]:
            st.markdown(
                f'<div class="gp-feedback-ok"><strong>¡Bien!</strong> {explanation}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="gp-feedback-bad"><strong>Casi.</strong> La respuesta es «{answer}». {explanation}</div>',
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
        word_pair = f'«{html.escape(item.german)}» significa «{html.escape(item.spanish)}».'
        if prior["correct"]:
            feedback = f'<div class="gp-feedback-ok"><strong>¡Eso es!</strong> {word_pair}</div>'
        else:
            feedback = f'<div class="gp-feedback-bad"><strong>Casi.</strong> {word_pair} La volverás a ver pronto para fijarla mejor.</div>'
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
          <p class="gp-helper">Elige la traducción que mejor corresponde. Después verás un ejemplo sencillo.</p>
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
        if prior["correct"]:
            message = f'<strong>¡Bien!</strong> «{html.escape(item.german)}» significa «{html.escape(item.spanish)}».'
        else:
            message = f'<strong>Casi.</strong> «{html.escape(item.german)}» significa «{html.escape(item.spanish)}». La practicaremos de nuevo más adelante.'
        st.markdown(
            f'<div class="{feedback_class}">{message}</div>',
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
    elif page == "Aprender":
        render_lesson()
    elif page == "Repaso":
        render_review()
    else:
        render_progress()
