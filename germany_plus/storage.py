from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import streamlit as st


USER_ID = "lula"
LOCAL_STATE_PATH = Path(".local/germany_plus_state.json")


def default_state() -> dict[str, Any]:
    return {
        "version": 1,
        "xp": 0,
        "sessions": [],
        "vocabulary": {},
        "preferences": {
            "show_spanish_help": True,
            "daily_goal": 1,
        },
    }


def _normalise_state(raw: Any) -> dict[str, Any]:
    base = default_state()
    if not isinstance(raw, dict):
        return base
    base.update({key: value for key, value in raw.items() if key in base})
    if not isinstance(base.get("sessions"), list):
        base["sessions"] = []
    if not isinstance(base.get("vocabulary"), dict):
        base["vocabulary"] = {}
    if not isinstance(base.get("preferences"), dict):
        base["preferences"] = default_state()["preferences"]
    base["xp"] = int(base.get("xp") or 0)
    return base


def _supabase_config() -> tuple[str, str] | None:
    try:
        url = str(st.secrets.get("SUPABASE_URL", "")).strip().rstrip("/")
        key = str(st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")).strip()
    except Exception:
        return None
    if not url or not key:
        return None
    return url, key


def _headers(key: str, *, prefer: str | None = None) -> dict[str, str]:
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers


def _read_remote() -> dict[str, Any] | None:
    config = _supabase_config()
    if config is None:
        return None
    url, key = config
    response = requests.get(
        f"{url}/rest/v1/germany_plus_state",
        headers=_headers(key),
        params={"user_id": f"eq.{USER_ID}", "select": "state", "limit": "1"},
        timeout=8,
    )
    response.raise_for_status()
    rows = response.json()
    if not rows:
        return default_state()
    return _normalise_state(rows[0].get("state"))


def _write_remote(state: dict[str, Any]) -> None:
    config = _supabase_config()
    if config is None:
        raise RuntimeError("Supabase no está configurado.")
    url, key = config
    payload = {
        "user_id": USER_ID,
        "state": state,
        "updated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    response = requests.post(
        f"{url}/rest/v1/germany_plus_state",
        headers=_headers(key, prefer="resolution=merge-duplicates,return=minimal"),
        params={"on_conflict": "user_id"},
        json=payload,
        timeout=8,
    )
    response.raise_for_status()


def _read_local() -> dict[str, Any]:
    if not LOCAL_STATE_PATH.exists():
        return default_state()
    try:
        return _normalise_state(json.loads(LOCAL_STATE_PATH.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError):
        return default_state()


def _write_local(state: dict[str, Any]) -> None:
    LOCAL_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = LOCAL_STATE_PATH.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(LOCAL_STATE_PATH)


@st.cache_resource
def storage_mode() -> str:
    """Return the active persistence mode without exposing secrets."""
    return "Supabase" if _supabase_config() else "Local"


def load_state() -> tuple[dict[str, Any], str, str | None]:
    """Load state, preferring Supabase and falling back to the local JSON file."""
    if _supabase_config():
        try:
            state = _read_remote()
            if state is not None:
                return deepcopy(state), "Supabase", None
        except Exception as exc:  # pragma: no cover - network-dependent
            local = _read_local()
            return local, "Local de respaldo", str(exc)
    return _read_local(), "Local", None


def save_state(state: dict[str, Any]) -> tuple[str, str | None]:
    """Persist state remotely when possible and always maintain a local backup."""
    clean_state = _normalise_state(state)
    local_error: str | None = None
    try:
        _write_local(clean_state)
    except Exception as exc:  # pragma: no cover - filesystem-dependent
        local_error = str(exc)

    if _supabase_config():
        try:
            _write_remote(clean_state)
            return "Supabase", local_error
        except Exception as exc:  # pragma: no cover - network-dependent
            detail = str(exc)
            if local_error:
                detail = f"Supabase: {detail}. Respaldo local: {local_error}"
            return "Local de respaldo", detail

    return "Local", local_error
