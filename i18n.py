"""English and Hindi UI text. Product names, brands and certifications stay in English.

Use t("key", name=...) with {name}-style placeholders. tests/test_i18n.py checks that every key used in the
code exists in both languages, that no placeholder is lost in translation, and that no key is unused.
"""
from __future__ import annotations

LANGS = {"en": "English", "hi": "हिन्दी"}

TEXT: dict = {}


def _add(table: dict) -> None:
    for key, (en, hi) in table.items():
        TEXT[key] = {"en": en, "hi": hi}


def current_lang() -> str:
    try:
        import streamlit as st
        return st.session_state.prefs.get("lang", "en")
    except Exception:
        return "en"


def t(key: str, lang: str = "", **kw) -> str:
    lang = lang or current_lang()
    entry = TEXT.get(key)
    if entry is None:
        return key  # never crash a screen over a missing string; the tests catch it
    text = entry.get(lang) or entry["en"]
    return text.format(**kw) if kw else text


from . import strings  # noqa: E402,F401  (populates TEXT)
