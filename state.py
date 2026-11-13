"""Session state, navigation and preference binding."""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

import streamlit as st

from . import catalog as C
from .game import Game

PREF_DEFAULTS = dict(name="", lang="en", size="M", shoe="8", style="any", budget="any",
                     match=True, large=False, reduce_motion=False)
VIEWS = ("home", "scan", "result", "alts", "compare", "reward", "impact", "profile")


def now_local() -> dt.datetime:
    """Naive datetime in the visitor's own timezone (falls back to UTC if the browser did not report one)."""
    zone = dt.timezone.utc
    try:
        name = st.context.timezone
        if name:
            zone = ZoneInfo(name)
    except Exception:  # unknown zone name, or running outside a browser session
        zone = dt.timezone.utc
    return dt.datetime.now(zone).replace(tzinfo=None)


def init() -> None:
    s = st.session_state
    if "game" not in s:
        s.game = Game.with_sample_data(now_local())
    if "prefs" not in s:
        s.prefs = dict(PREF_DEFAULTS)
    for key, default in dict(view="home", sel="tee", cur="tee", reward=None, celebrate=False, cmp_a="tee", cmp_b="tee_pre",
                             cmp_from="home", alt_filter="all", shown_view=None).items():
        s.setdefault(key, default)


def game() -> Game:
    return st.session_state.game


def prefs() -> dict:
    return st.session_state.prefs


def go(view: str) -> None:
    if view not in VIEWS:
        raise ValueError(f"unknown view {view}")
    st.session_state.view = view


# ---- preference widgets -------------------------------------------------------------------------
# Streamlit deletes the state of a widget that is not rendered on a run. To make settings survive page
# changes, the value lives in prefs[name]; the widget key mirrors it and is re-seeded before every render.

def _sync(name: str) -> None:
    value = st.session_state[f"w_{name}"]
    if value is not None:
        st.session_state.prefs[name] = value


def bind(widget, name: str, label: str, **kwargs):
    """Create a widget whose value is stored in prefs[name]. `widget` is st.selectbox, st.toggle, st.pills ..."""
    key = f"w_{name}"
    st.session_state[key] = st.session_state.prefs[name]
    return widget(label, key=key, on_change=_sync, args=(name,), **kwargs)


def bind_state(widget, state_key: str, label: str, **kwargs):
    """Same idea for plain session keys such as the selected sample item."""
    key = f"w_{state_key}"
    st.session_state[key] = st.session_state[state_key]

    def sync():
        value = st.session_state[key]
        if value is not None:
            st.session_state[state_key] = value

    return widget(label, key=key, on_change=sync, **kwargs)


def budget_cap() -> int:
    return C.BUDGET_CAP[prefs()["budget"]]
