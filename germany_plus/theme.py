from __future__ import annotations

import streamlit as st


CSS = r"""
<style>
:root {
  --gp-ink: #151310;
  --gp-ink-soft: #413b36;
  --gp-muted: #6d645d;
  --gp-red: #ed1c24;
  --gp-red-dark: #bd1219;
  --gp-gold: #ffb515;
  --gp-orange: #f46b18;
  --gp-cream: #fffaf4;
  --gp-paper: #ffffff;
  --gp-line: #eadfd5;
  --gp-green: #149b58;
  --gp-green-soft: #eaf8ef;
  --gp-danger: #a8282e;
  --gp-danger-soft: #fff0f1;
  --gp-purple: #7551b8;
  --gp-shadow: 0 16px 42px rgba(52, 32, 18, .09);
  --gp-soft-shadow: 0 8px 24px rgba(52, 32, 18, .06);
}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background: var(--gp-cream) !important;
  color: var(--gp-ink) !important;
}

.stApp {
  background:
    radial-gradient(circle at 92% 3%, rgba(255,181,21,.18), transparent 23rem),
    radial-gradient(circle at 3% 18%, rgba(237,28,36,.055), transparent 18rem),
    linear-gradient(180deg, #fffdfa 0%, #fffaf4 60%, #fffdf9 100%) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer,
[data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; }

[data-testid="stAppViewContainer"] > .main { overflow: visible; }

.block-container {
  max-width: 900px;
  padding: .9rem 1rem 7.2rem;
}

/* Global contrast guard: light surfaces always receive dark text. */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stCaption, [data-testid="stCaptionContainer"],
[data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"],
[data-testid="stDataFrame"], [data-testid="stExpander"] summary,
[data-testid="stAlert"] p, [data-testid="stAlert"] li {
  color: var(--gp-ink) !important;
}

.gp-wordmark-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin: .2rem 0 .55rem;
}
.gp-wordmark {
  display: inline-flex;
  align-items: baseline;
  font-size: clamp(2rem, 6vw, 3rem);
  font-weight: 950;
  letter-spacing: -.065em;
  color: #0e0d0c !important;
  line-height: 1;
}
.gp-wordmark b { color: var(--gp-red) !important; font-weight: 950; }
.gp-top-badges { display: flex; align-items: center; gap: .58rem; }
.gp-streak-pill {
  display: inline-flex; align-items: center; gap: .35rem;
  min-height: 42px; padding: .45rem .75rem; border-radius: 15px;
  background: #fff4e9; border: 1px solid #f5e6d8; color: var(--gp-ink) !important;
  font-size: .95rem; font-weight: 900; box-shadow: var(--gp-soft-shadow);
}
.gp-avatar {
  width: 44px; height: 44px; display: grid; place-items: center;
  border-radius: 50%; color: white !important; font-weight: 950; font-size: 1.12rem;
  background: linear-gradient(145deg, var(--gp-orange), var(--gp-gold));
  box-shadow: 0 8px 20px rgba(244,107,24,.22);
}

.gp-home-header {
  position: relative; overflow: hidden; min-height: 205px;
  padding: 1.4rem 1.35rem 1.15rem; border-radius: 28px;
  background: linear-gradient(120deg, rgba(255,255,255,.98) 0 45%, rgba(255,247,235,.93) 100%);
  border: 1px solid rgba(234,223,213,.9); box-shadow: var(--gp-shadow);
}
.gp-header-skyline {
  position: absolute; right: -5%; bottom: -5px; width: 73%; max-height: 180px;
  object-fit: contain; object-position: right bottom; opacity: .96; pointer-events: none;
}
.gp-header-copy { position: relative; z-index: 2; width: 58%; }
.gp-greeting {
  margin: .15rem 0 0; color: #0f0e0d !important;
  font-size: clamp(2.2rem, 8vw, 4rem); line-height: .98;
  letter-spacing: -.06em; font-weight: 950;
}
.gp-subtitle { margin: .65rem 0 0; color: var(--gp-muted) !important; font-size: 1.02rem; line-height: 1.45; }
.gp-level {
  display: inline-flex; margin-top: .9rem; padding: .4rem .72rem; border-radius: 999px;
  background: #fff0c8; color: #6a4700 !important; border: 1px solid #f7d98c;
  font-size: .78rem; font-weight: 900;
}

.gp-section-title {
  margin: 1.35rem 0 .7rem; color: var(--gp-ink) !important;
  font-size: 1.2rem; font-weight: 950; letter-spacing: -.028em;
}

.gp-stats-panel {
  display: grid; grid-template-columns: 1.1fr 1.45fr .7fr; align-items: stretch;
  margin-top: .85rem; border-radius: 24px; overflow: hidden;
  background: rgba(255,255,255,.96); border: 1px solid var(--gp-line); box-shadow: var(--gp-shadow);
}
.gp-stat-block { padding: 1rem 1.08rem; min-width: 0; }
.gp-stat-block + .gp-stat-block { border-left: 1px solid var(--gp-line); }
.gp-stat-label { color: var(--gp-ink-soft) !important; font-size: .77rem; font-weight: 850; }
.gp-stat-value { margin-top: .18rem; color: var(--gp-ink) !important; font-size: 1.55rem; font-weight: 950; letter-spacing: -.045em; }
.gp-stat-note { margin-top: .12rem; color: var(--gp-muted) !important; font-size: .73rem; line-height: 1.35; }
.gp-stat-value .accent { color: var(--gp-red) !important; }
.gp-progress-track { height: 8px; margin-top: .65rem; border-radius: 99px; background: #eee9e5; overflow: hidden; }
.gp-progress-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--gp-red), var(--gp-gold)); }
.gp-xp { text-align: center; }
.gp-xp-star { color: var(--gp-gold) !important; font-size: 1.1rem; }

.gp-lesson-card {
  position: relative; overflow: hidden; min-height: 285px; border-radius: 27px;
  background: #171310; border: 1px solid #281c16; box-shadow: var(--gp-shadow); color: white !important;
}
.gp-lesson-art { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.gp-lesson-overlay { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(10,9,8,.98) 0%, rgba(19,15,12,.94) 42%, rgba(19,15,12,.2) 78%, rgba(19,15,12,.05) 100%); }
.gp-lesson-inner { position: relative; z-index: 2; width: 58%; padding: 1.3rem 1.35rem; }
.gp-today-pill { display: inline-flex; padding: .34rem .62rem; border-radius: 10px; background: linear-gradient(90deg, var(--gp-red), var(--gp-orange)); color: white !important; font-size: .72rem; font-weight: 950; }
.gp-kicker { margin-top: .8rem; color: #ffd86f !important; font-size: .72rem; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }
.gp-lesson-title { margin: .35rem 0 .35rem; color: white !important; font-size: clamp(1.65rem, 5vw, 2.35rem); line-height: 1.05; font-weight: 950; letter-spacing: -.04em; }
.gp-lesson-copy { color: rgba(255,255,255,.86) !important; line-height: 1.55; font-size: .96rem; }
.gp-meta-row { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .85rem; }
.gp-chip { padding: .34rem .58rem; border-radius: 999px; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.16); color: white !important; font-size: .74rem; font-weight: 800; }

.gp-card {
  padding: 1.15rem; border: 1px solid var(--gp-line); border-radius: 22px;
  background: rgba(255,255,255,.97); box-shadow: var(--gp-soft-shadow); color: var(--gp-ink) !important;
}
.gp-card h1, .gp-card h2, .gp-card h3, .gp-card h4,
.gp-card p, .gp-card span, .gp-card div, .gp-card strong { color: inherit; }
.gp-card h2, .gp-card h3 { margin-top: 0; color: var(--gp-ink) !important; }

.gp-feature-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .72rem; }
.gp-feature-card { min-height: 235px; padding: 1rem; border-radius: 22px; background: white; border: 1px solid var(--gp-line); box-shadow: var(--gp-soft-shadow); color: var(--gp-ink) !important; }
.gp-feature-card.gold { background: linear-gradient(180deg, #fffdfa, #fff8e6); border-color: #f3dfae; }
.gp-feature-card.red { background: linear-gradient(180deg, #fffdfc, #fff3f1); border-color: #f0d7d4; }
.gp-feature-card.purple { background: linear-gradient(180deg, #fff, #f7f3ff); border-color: #ddd3ef; }
.gp-feature-heading { display: flex; gap: .62rem; align-items: center; }
.gp-feature-icon { width: 40px; height: 40px; flex: 0 0 40px; display: grid; place-items: center; border-radius: 50%; color: white !important; font-size: 1.05rem; font-weight: 900; }
.gold .gp-feature-icon, .gp-feature-icon.gold-icon { background: var(--gp-gold); }
.red .gp-feature-icon, .gp-feature-icon.red-icon { background: var(--gp-red); }
.purple .gp-feature-icon, .gp-feature-icon.purple-icon { background: var(--gp-purple); }
.gp-feature-title { color: var(--gp-ink) !important; font-size: .92rem; font-weight: 950; line-height: 1.15; }
.gp-feature-subtitle { margin-top: .12rem; color: var(--gp-muted) !important; font-size: .74rem; }
.gp-mini-list, .gp-mini-reading, .gp-mini-quiz { margin-top: .75rem; padding: .72rem; border-radius: 15px; background: rgba(255,255,255,.9); border: 1px solid rgba(228,218,210,.9); }
.gp-mini-row { display: flex; justify-content: space-between; gap: .5rem; padding: .34rem 0; border-bottom: 1px solid #eee7e0; }
.gp-mini-row:last-child { border-bottom: 0; }
.gp-mini-row strong { display: block; color: var(--gp-ink) !important; font-size: .82rem; }
.gp-mini-row span { display: block; color: var(--gp-muted) !important; font-size: .68rem; }
.gp-mini-reading strong { color: var(--gp-ink) !important; font-size: .84rem; }
.gp-mini-reading p { color: var(--gp-ink-soft) !important; font-size: .73rem; line-height: 1.55; }
.gp-mini-question { color: var(--gp-ink) !important; font-size: .78rem; font-weight: 850; line-height: 1.35; }
.gp-mini-option { margin-top: .35rem; padding: .42rem .52rem; border-radius: 10px; border: 1px solid #e6dfd9; background: white; color: var(--gp-ink) !important; font-size: .72rem; }
.gp-mini-option.correct { border: 1.5px solid #25a765; background: #edfaf2; color: #145c39 !important; font-weight: 850; }

/* Home feature cards with a real, selectable quick quiz. */
.st-key-home_features [data-testid="stHorizontalBlock"] { align-items: stretch; gap: .72rem !important; }
.st-key-home_features [data-testid="stColumn"] {
  padding: 1rem; border-radius: 22px; background: white;
  border: 1px solid var(--gp-line); box-shadow: var(--gp-soft-shadow);
}
.st-key-home_features [data-testid="stColumn"]:nth-child(1) { background: linear-gradient(180deg, #fffdfa, #fff8e6); border-color: #f3dfae; }
.st-key-home_features [data-testid="stColumn"]:nth-child(2) { background: linear-gradient(180deg, #fffdfc, #fff3f1); border-color: #f0d7d4; }
.st-key-home_features [data-testid="stColumn"]:nth-child(3) { background: linear-gradient(180deg, #fff, #f7f3ff); border-color: #ddd3ef; }
.st-key-home_features [data-testid="stRadio"] label[data-baseweb="radio"] {
  min-height: 40px !important; padding: .48rem .58rem !important; margin-bottom: .28rem !important; border-radius: 11px !important;
}
.st-key-home_features [data-testid="stRadio"] label[data-baseweb="radio"] p { font-size: .72rem !important; line-height: 1.25 !important; }
.st-key-home_features .stButton > button { min-height: 42px !important; margin-top: .25rem; }
.gp-mini-feedback { margin: .45rem 0 0; padding: .68rem .72rem; font-size: .76rem; }

.gp-reading { color: var(--gp-ink) !important; font-size: 1.03rem; line-height: 1.72; }
.gp-reading p { margin: 0 0 .95rem; color: var(--gp-ink) !important; }
.gp-progress-label { display: flex; justify-content: space-between; color: var(--gp-muted) !important; font-size: .78rem; font-weight: 850; margin-bottom: .35rem; }
.gp-question-number { display: inline-block; padding: .35rem .58rem; border-radius: 999px; background: #f5ece5; color: #695f58 !important; font-size: .75rem; font-weight: 950; }
.gp-question-title { margin: .8rem 0 .25rem; color: var(--gp-ink) !important; font-size: clamp(1.25rem, 4vw, 1.68rem); line-height: 1.22; font-weight: 950; letter-spacing: -.025em; }
.gp-helper { color: var(--gp-muted) !important; font-size: .88rem; line-height: 1.5; }

.gp-feedback-ok, .gp-feedback-bad { padding: .95rem 1rem; border-radius: 17px; margin: .65rem 0; line-height: 1.5; font-size: .92rem; }
.gp-feedback-ok, .gp-feedback-ok * { color: #155b39 !important; }
.gp-feedback-ok { border: 1px solid #b8e3ca; }
.gp-feedback-bad, .gp-feedback-bad * { color: #85252b !important; }
.gp-feedback-bad { background: var(--gp-danger-soft); border: 1px solid #edc0c4; }

.gp-vocab-box { margin-top: .75rem; padding: .95rem; border-radius: 17px; background: #fff8df; border: 1px solid #efd47a; color: var(--gp-ink) !important; }
.gp-vocab-word { color: var(--gp-ink) !important; font-size: 1.12rem; font-weight: 950; }
.gp-pronunciation { color: #755600 !important; font-size: .85rem; font-weight: 850; }
.gp-example { margin-top: .35rem; color: #51473b !important; font-size: .9rem; line-height: 1.48; }

.gp-category-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .62rem; }
.gp-category { min-height: 116px; padding: .8rem; border-radius: 18px; border: 1px solid var(--gp-line); background: rgba(255,255,255,.93); box-shadow: var(--gp-soft-shadow); color: var(--gp-ink) !important; }
.gp-category-icon { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 50%; color: white !important; font-size: .95rem; font-weight: 900; background: linear-gradient(145deg, var(--gp-red), var(--gp-orange)); }
.gp-category strong { display: block; margin-top: .55rem; color: var(--gp-ink) !important; font-size: .82rem; }
.gp-category span { display: block; margin-top: .2rem; color: var(--gp-muted) !important; font-size: .69rem; }
.gp-cat-progress { height: 5px; margin-top: .7rem; border-radius: 999px; background: #eee8e2; overflow: hidden; }
.gp-cat-progress i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--gp-red), var(--gp-gold)); }

.gp-calendar { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .38rem; }
.gp-day { aspect-ratio: 1; display: grid; place-items: center; border-radius: 11px; background: #f4eee8; color: #776e67 !important; font-size: .73rem; font-weight: 850; }
.gp-day.done { background: linear-gradient(135deg, var(--gp-red), #ef5d43); color: white !important; box-shadow: 0 5px 12px rgba(217,40,47,.18); }
.gp-day.today { outline: 2px solid var(--gp-gold); outline-offset: 1px; }
.gp-storage { padding: .65rem .8rem; border-radius: 14px; background: rgba(255,255,255,.82); border: 1px solid var(--gp-line); color: var(--gp-muted) !important; font-size: .75rem; }
.gp-storage strong { color: var(--gp-ink) !important; }

/* Streamlit controls */
[data-testid="stProgress"] > div > div > div > div { background: linear-gradient(90deg, var(--gp-red), var(--gp-gold)) !important; }
[data-testid="stExpander"] { border: 1px solid var(--gp-line) !important; border-radius: 17px !important; background: rgba(255,255,255,.92) !important; }
[data-testid="stExpander"] details, [data-testid="stExpander"] summary, [data-testid="stExpander"] p { color: var(--gp-ink) !important; }

/* Fixed bottom navigation, visually close to the mockup. */
.st-key-main_navigation {
  position: fixed; z-index: 999; left: 50%; bottom: .45rem; transform: translateX(-50%);
  width: min(880px, calc(100vw - 1rem)); padding: .3rem;
  border: 1px solid rgba(230,220,211,.96); border-radius: 24px;
  background: rgba(255,255,255,.96); box-shadow: 0 14px 38px rgba(37,24,15,.14);
  backdrop-filter: blur(14px);
}
.st-key-main_navigation div[role="radiogroup"] { display: grid !important; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .2rem !important; width: 100% !important; }
.st-key-main_navigation div[role="radiogroup"] label {
  width: 100% !important; min-width: 0 !important; justify-content: center !important; padding: .72rem .18rem !important;
  border-radius: 17px; background: transparent !important; border: 0 !important;
}
.st-key-main_navigation div[role="radiogroup"] label > div:first-child { display: none !important; }
.st-key-main_navigation div[role="radiogroup"] label p { color: #625b55 !important; font-size: .76rem !important; font-weight: 850 !important; white-space: nowrap !important; word-break: keep-all !important; overflow-wrap: normal !important; line-height: 1 !important; text-align: center !important; margin: 0 !important; }
.st-key-main_navigation div[role="radiogroup"] label:has(input:checked) { background: #fff0ee !important; }
.st-key-main_navigation div[role="radiogroup"] label:has(input:checked) p { color: var(--gp-red) !important; }

/* Quiz options: force visible dark text on opaque cards in all states. */
[data-testid="stRadio"] > div[role="radiogroup"] { gap: .4rem !important; }
[data-testid="stRadio"] label[data-baseweb="radio"] {
  width: 100% !important; min-height: 50px !important; padding: .72rem .82rem !important;
  margin: 0 0 .42rem !important; border: 1.5px solid #ded5ce !important;
  border-radius: 15px !important; background: #ffffff !important; opacity: 1 !important;
  box-shadow: 0 3px 10px rgba(45,30,20,.03) !important;
}
[data-testid="stRadio"] label[data-baseweb="radio"]:hover { border-color: #baaaa0 !important; background: #fffaf6 !important; }
[data-testid="stRadio"] label[data-baseweb="radio"] p,
[data-testid="stRadio"] label[data-baseweb="radio"] span,
[data-testid="stRadio"] label[data-baseweb="radio"] div { color: #171412 !important; opacity: 1 !important; }
[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) { border-color: var(--gp-red) !important; background: #fff1f0 !important; }
[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p { color: #8d1016 !important; font-weight: 900 !important; }
[data-testid="stRadio"] label[data-baseweb="radio"][aria-disabled="true"],
[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:disabled) { opacity: 1 !important; background: #faf8f6 !important; }
[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:disabled) p { color: #2b2724 !important; opacity: 1 !important; }
.st-key-main_navigation [data-testid="stRadio"] label[data-baseweb="radio"] { min-height: auto !important; margin: 0 !important; padding: .7rem .2rem !important; border: 0 !important; box-shadow: none !important; background: transparent !important; }

.stButton > button, .stDownloadButton > button {
  min-height: 48px; border-radius: 15px !important; font-weight: 900 !important;
  border: 1px solid #201b18 !important; background: white !important; color: var(--gp-ink) !important;
}
.stButton > button p, .stDownloadButton > button p { color: inherit !important; font-weight: inherit !important; }
.stButton > button[kind="primary"] { background: linear-gradient(90deg, var(--gp-red), #f3312f) !important; border-color: var(--gp-red) !important; color: white !important; }
.stButton > button[kind="primary"] p { color: white !important; }
.stButton > button[kind="primary"]:hover { background: var(--gp-red-dark) !important; border-color: var(--gp-red-dark) !important; }

[data-testid="stAlert"] { border-radius: 16px !important; }
[data-testid="stAlert"] * { color: var(--gp-ink) !important; }

@media (max-width: 760px) {
  .block-container { padding: .55rem .72rem 6.8rem; }
  .gp-home-header { min-height: 190px; padding: 1.05rem; border-radius: 23px; }
  .gp-header-copy { width: 72%; }
  .gp-header-skyline { width: 82%; opacity: .72; }
  .gp-subtitle { max-width: 245px; font-size: .9rem; }
  .gp-stats-panel { grid-template-columns: 1fr 1.25fr .62fr; border-radius: 20px; }
  .gp-stat-block { padding: .78rem .65rem; }
  .gp-stat-value { font-size: 1.2rem; }
  .gp-stat-note { display: none; }
  .gp-lesson-card { min-height: 330px; }
  .gp-lesson-inner { width: 71%; padding: 1.05rem; }
  .gp-lesson-overlay { background: linear-gradient(90deg, rgba(10,9,8,.98) 0%, rgba(18,14,11,.92) 58%, rgba(18,14,11,.2) 100%); }
  .gp-feature-grid { grid-template-columns: 1fr; }
  .st-key-home_features [data-testid="stHorizontalBlock"] { display: block !important; }
  .st-key-home_features [data-testid="stColumn"] { margin-bottom: .72rem; width: 100% !important; }
  .gp-feature-card { min-height: auto; }
  .gp-category-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .gp-wordmark { font-size: 2.05rem; }
  .gp-streak-pill { min-height: 38px; padding: .38rem .62rem; }
  .gp-avatar { width: 40px; height: 40px; }
  .st-key-main_navigation div[role="radiogroup"] label p { font-size: .64rem !important; }
  .st-key-main_navigation div[role="radiogroup"] label { padding: .68rem .08rem !important; }
}

@media (max-width: 430px) {
  .gp-header-copy { width: 78%; }
  .gp-greeting { font-size: 2.25rem; }
  .gp-stats-panel { grid-template-columns: 1fr 1.2fr .65fr; }
  .gp-stat-label { font-size: .67rem; }
  .gp-stat-value { font-size: 1.02rem; }
  .gp-xp-star { font-size: .9rem; }
  .gp-lesson-inner { width: 77%; }
  .gp-lesson-copy { font-size: .88rem; }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def wordmark(*, streak: int = 0) -> None:
    st.markdown(
        f"""
        <div class="gp-wordmark-row">
          <div class="gp-wordmark">Germany<b>+</b></div>
          <div class="gp-top-badges">
            <div class="gp-streak-pill">🔥 {streak}</div>
            <div class="gp-avatar" aria-label="Perfil de Lula">L</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
