"""Offline smoke test for environments where Streamlit is not installed."""
from __future__ import annotations

import runpy
import sys
import types
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class SessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


class Element:
    def button(self, *args, **kwargs):
        return False

    def metric(self, *args, **kwargs):
        return None

    def write(self, *args, **kwargs):
        return None


class StreamlitStub(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state = SessionState()
        self.secrets = {}

    def cache_resource(self, func=None, **kwargs):
        return func if func is not None else (lambda inner: inner)

    def set_page_config(self, *args, **kwargs):
        return None

    def markdown(self, *args, **kwargs):
        return None

    def radio(self, label, options, **kwargs):
        key = kwargs.get("key")
        value = self.session_state.get(key, options[0])
        self.session_state[key] = value
        return value

    @contextmanager
    def container(self, *args, **kwargs):
        yield Element()

    @contextmanager
    def expander(self, *args, **kwargs):
        yield Element()

    def columns(self, spec, *args, **kwargs):
        count = spec if isinstance(spec, int) else len(spec)
        return [Element() for _ in range(count)]

    def button(self, *args, **kwargs):
        return False

    def checkbox(self, label, value=False, **kwargs):
        return value

    def progress(self, *args, **kwargs):
        return None

    def caption(self, *args, **kwargs):
        return None

    def info(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def error(self, *args, **kwargs):
        return None

    def success(self, *args, **kwargs):
        return None

    def code(self, *args, **kwargs):
        return None

    def write(self, *args, **kwargs):
        return None

    def metric(self, *args, **kwargs):
        return None

    def dataframe(self, *args, **kwargs):
        return None

    def rerun(self):
        raise RuntimeError("No button should trigger rerun during smoke test")


stub = StreamlitStub()
sys.modules["streamlit"] = stub

for page in ("Inicio", "Lección", "Repaso", "Progreso"):
    stub.session_state.clear()
    stub.session_state["main_nav"] = page
    runpy.run_path(str(ROOT / "streamlit_app.py"), run_name=f"__smoke_{page}__")

print("OK: las cuatro pantallas principales arrancan con el stub de Streamlit")
