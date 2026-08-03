from __future__ import annotations

import streamlit as st


CSS = r"""
<style>
:root {
  --gp-black: #171412;
  --gp-red: #d9282f;
  --gp-red-dark: #a9141b;
  --gp-gold: #f4b51f;
  --gp-gold-soft: #fff3c8;
  --gp-cream: #fffaf4;
  --gp-paper: #ffffff;
  --gp-muted: #6d655f;
  --gp-line: #eadfd5;
  --gp-green: #278a5b;
  --gp-shadow: 0 12px 36px rgba(45, 30, 20, .08);
}

html, body, [class*="css"] {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
  background:
    radial-gradient(circle at 92% 2%, rgba(244,181,31,.17), transparent 23rem),
    radial-gradient(circle at 5% 18%, rgba(217,40,47,.07), transparent 18rem),
    var(--gp-cream);
  color: var(--gp-black);
}

[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
  visibility: hidden;
}

[data-testid="stAppViewContainer"] > .main {
  overflow: visible;
}

.block-container {
  max-width: 860px;
  padding-top: 1rem;
  padding-bottom: 6rem;
}

.gp-shell { max-width: 820px; margin: 0 auto; }

.gp-wordmark {
  display: inline-flex;
  align-items: baseline;
  gap: 0;
  font-size: clamp(1.55rem, 5vw, 2.15rem);
  font-weight: 900;
  letter-spacing: -0.055em;
  color: var(--gp-black);
  margin-bottom: .55rem;
}
.gp-wordmark b { color: var(--gp-red); font-weight: 900; }

.gp-hero {
  position: relative;
  overflow: hidden;
  padding: 1.25rem 1.25rem 1.05rem;
  border: 1px solid rgba(234,223,213,.9);
  border-radius: 26px;
  background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(255,248,238,.96));
  box-shadow: var(--gp-shadow);
}
.gp-hero::after {
  content: "";
  position: absolute;
  right: -28px;
  top: -42px;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: conic-gradient(from 20deg, var(--gp-black) 0 33%, var(--gp-red) 33% 66%, var(--gp-gold) 66% 100%);
  opacity: .09;
}
.gp-greeting {
  position: relative;
  z-index: 1;
  margin: 0;
  font-size: clamp(2rem, 8vw, 3.45rem);
  line-height: 1.02;
  letter-spacing: -.055em;
  font-weight: 900;
}
.gp-subtitle {
  position: relative;
  z-index: 1;
  margin: .55rem 0 0;
  color: var(--gp-muted);
  font-size: 1rem;
}
.gp-level {
  display: inline-flex;
  margin-top: .85rem;
  padding: .38rem .68rem;
  border-radius: 999px;
  background: var(--gp-gold-soft);
  color: #6a4a00;
  font-weight: 800;
  font-size: .78rem;
}

.gp-section-title {
  margin: 1.3rem 0 .65rem;
  font-size: 1.13rem;
  font-weight: 900;
  letter-spacing: -.025em;
}

.gp-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .75rem;
  margin-top: .9rem;
}
.gp-stat {
  padding: .9rem;
  border-radius: 19px;
  border: 1px solid var(--gp-line);
  background: rgba(255,255,255,.86);
  box-shadow: 0 7px 22px rgba(45,30,20,.045);
}
.gp-stat-label { color: var(--gp-muted); font-size: .76rem; font-weight: 700; }
.gp-stat-value { margin-top: .15rem; font-size: 1.45rem; font-weight: 900; letter-spacing: -.04em; }
.gp-stat-note { margin-top: .08rem; color: var(--gp-muted); font-size: .72rem; }

.gp-lesson-card {
  overflow: hidden;
  border-radius: 25px;
  border: 1px solid rgba(23,20,18,.8);
  background:
    linear-gradient(110deg, rgba(10,9,8,.96), rgba(45,25,19,.91)),
    var(--gp-black);
  color: white;
  box-shadow: var(--gp-shadow);
}
.gp-lesson-accent { height: 5px; background: linear-gradient(90deg, var(--gp-black) 0 33%, var(--gp-red) 33% 66%, var(--gp-gold) 66%); }
.gp-lesson-inner { padding: 1.25rem; }
.gp-kicker { color: #ffd66a; font-size: .72rem; font-weight: 900; letter-spacing: .09em; text-transform: uppercase; }
.gp-lesson-title { margin: .4rem 0 .3rem; font-size: clamp(1.5rem, 5vw, 2rem); line-height: 1.05; font-weight: 900; }
.gp-lesson-copy { color: rgba(255,255,255,.72); line-height: 1.55; }
.gp-meta-row { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .8rem; }
.gp-chip { padding: .35rem .58rem; border-radius: 999px; background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.12); color: rgba(255,255,255,.9); font-size: .75rem; font-weight: 700; }

.gp-card {
  padding: 1.15rem;
  border: 1px solid var(--gp-line);
  border-radius: 23px;
  background: rgba(255,255,255,.9);
  box-shadow: var(--gp-shadow);
}
.gp-card h2, .gp-card h3 { margin-top: 0; color: var(--gp-black); }

.gp-reading {
  font-size: 1.03rem;
  line-height: 1.72;
}
.gp-reading p { margin: 0 0 .95rem; }

.gp-progress-label {
  display: flex;
  justify-content: space-between;
  color: var(--gp-muted);
  font-size: .78rem;
  font-weight: 800;
  margin-bottom: .35rem;
}

.gp-question-number {
  display: inline-block;
  padding: .35rem .58rem;
  border-radius: 999px;
  background: #f5ece5;
  color: var(--gp-muted);
  font-size: .75rem;
  font-weight: 900;
}
.gp-question-title {
  margin: .8rem 0 .25rem;
  font-size: clamp(1.25rem, 4vw, 1.65rem);
  line-height: 1.2;
  font-weight: 900;
  letter-spacing: -.025em;
}
.gp-helper { color: var(--gp-muted); font-size: .88rem; line-height: 1.5; }

.gp-feedback-ok, .gp-feedback-bad {
  padding: .9rem 1rem;
  border-radius: 16px;
  margin: .65rem 0;
  line-height: 1.48;
}
.gp-feedback-ok { background: #e9f7ef; border: 1px solid #bce3cc; color: #185c3c; }
.gp-feedback-bad { background: #fff0f0; border: 1px solid #f0c3c5; color: #8a1d23; }

.gp-vocab-box {
  margin-top: .75rem;
  padding: .9rem;
  border-radius: 16px;
  background: #fff8df;
  border: 1px solid #f1d982;
}
.gp-vocab-word { font-size: 1.12rem; font-weight: 900; }
.gp-pronunciation { color: #795b00; font-size: .85rem; font-weight: 800; }
.gp-example { margin-top: .35rem; color: #5f5241; font-size: .9rem; }

.gp-category-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: .65rem;
}
.gp-category {
  min-height: 102px;
  padding: .8rem;
  border-radius: 18px;
  border: 1px solid var(--gp-line);
  background: rgba(255,255,255,.82);
}
.gp-category strong { display: block; font-size: .9rem; }
.gp-category span { display: block; margin-top: .25rem; color: var(--gp-muted); font-size: .72rem; }
.gp-cat-line { width: 36px; height: 4px; margin-bottom: .55rem; border-radius: 999px; background: linear-gradient(90deg, var(--gp-red), var(--gp-gold)); }

.gp-calendar { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .38rem; }
.gp-day { aspect-ratio: 1; display: grid; place-items: center; border-radius: 11px; background: #f4eee8; color: #8a817a; font-size: .73rem; font-weight: 800; }
.gp-day.done { background: linear-gradient(135deg, var(--gp-red), #ef5d43); color: white; box-shadow: 0 5px 12px rgba(217,40,47,.18); }
.gp-day.today { outline: 2px solid var(--gp-gold); outline-offset: 1px; }

.gp-storage {
  padding: .65rem .8rem;
  border-radius: 14px;
  background: rgba(255,255,255,.72);
  border: 1px solid var(--gp-line);
  color: var(--gp-muted);
  font-size: .75rem;
}

/* Top navigation */
.st-key-main_navigation div[role="radiogroup"] {
  display: flex;
  gap: .35rem;
  padding: .34rem;
  margin: .75rem 0 1rem;
  border: 1px solid var(--gp-line);
  border-radius: 16px;
  background: rgba(255,255,255,.86);
  box-shadow: 0 8px 24px rgba(45,30,20,.05);
}
.st-key-main_navigation div[role="radiogroup"] label {
  flex: 1 1 0;
  min-width: 0;
  justify-content: center;
  padding: .55rem .3rem !important;
  border-radius: 12px;
  font-size: .78rem;
  font-weight: 800;
}
.st-key-main_navigation div[role="radiogroup"] label:has(input:checked) {
  background: var(--gp-black);
  color: white !important;
}
.st-key-main_navigation div[role="radiogroup"] label:has(input:checked) p { color: white !important; }

/* Quiz alternatives remain vertical and fully visible. */
[data-testid="stRadio"] label[data-baseweb="radio"] {
  width: 100%;
  padding: .72rem .8rem;
  margin-bottom: .38rem;
  border: 1px solid var(--gp-line);
  border-radius: 14px;
  background: #fff;
}
.st-key-main_navigation [data-testid="stRadio"] label[data-baseweb="radio"] {
  margin-bottom: 0;
  border: 0;
  background: transparent;
}

.stButton > button, .stDownloadButton > button {
  min-height: 46px;
  border-radius: 14px;
  font-weight: 850;
  border: 1px solid var(--gp-black);
}
.stButton > button[kind="primary"] {
  background: var(--gp-red);
  border-color: var(--gp-red);
  color: white;
}
.stButton > button[kind="primary"]:hover {
  background: var(--gp-red-dark);
  border-color: var(--gp-red-dark);
}

[data-testid="stExpander"] {
  border: 1px solid var(--gp-line);
  border-radius: 16px;
  background: rgba(255,255,255,.75);
}

@media (max-width: 680px) {
  .block-container { padding: .65rem .72rem 5rem; }
  .gp-hero { border-radius: 22px; padding: 1.05rem; }
  .gp-stats { gap: .45rem; }
  .gp-stat { padding: .72rem .62rem; border-radius: 16px; }
  .gp-stat-value { font-size: 1.18rem; }
  .gp-stat-note { display: none; }
  .gp-category-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .st-key-main_navigation div[role="radiogroup"] label { font-size: .72rem; }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def wordmark() -> None:
    st.markdown('<div class="gp-wordmark">Germany<b>+</b></div>', unsafe_allow_html=True)
