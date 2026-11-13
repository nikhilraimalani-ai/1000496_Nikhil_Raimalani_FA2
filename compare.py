from __future__ import annotations

import streamlit as st

from .. import state, ui
from .. import catalog as C
from ..components import COL, esc, legend, radar_svg, render
from ..i18n import t

ROWS = ("score", "carbon", "water", "price")


def _fmt_ids(i: str) -> str:
    p = C.BY_ID[i]
    return f"{p.emoji} {p.name} · {p.brand}"


def render_page() -> None:
    ui.back(st.session_state.cmp_from)
    render(f"<h2>{t('cmp_title')}</h2><div class='muted'>{t('cmp_sub')}</div>")
    ids = [p.id for p in C.CATALOG]
    state.bind_state(st.selectbox, "cmp_a", t("cmp_item_a"), options=ids, format_func=_fmt_ids)
    state.bind_state(st.selectbox, "cmp_b", t("cmp_item_b"), options=ids, format_func=_fmt_ids)
    a, b = C.BY_ID[st.session_state.cmp_a], C.BY_ID[st.session_state.cmp_b]
    if a.id == b.id:
        render(f"<div class='card'><b>{t('cmp_same')}</b></div>")
        return
    labels = [ui.factor_label(n) for n in a.factors]
    render(f"<div class='card center'>{radar_svg(labels, [(list(a.factors.values()), COL['g'], a.name), (list(b.factors.values()), COL['y'], b.name)])}"
           f"{legend([(COL['g'], esc(a.name)), (COL['y'], esc(b.name))])}</div>")
    spec = [  # label key, a value, b value, higher is better, formatter
        ("cmp_score", a.score, b.score, True, str),
        ("cmp_co2", a.co2_kg, b.co2_kg, False, lambda v: f"{v:g} kg"),
        ("cmp_water", a.water_l, b.water_l, False, lambda v: f"{v:,} L"),
        ("cmp_price", a.price, b.price, False, ui.inr),
    ]
    body = ""
    for key, va, vb, high, fmt in spec:
        wa = (va > vb) if high else (va < vb)
        wb = (vb > va) if high else (vb < va)
        body += (f"<tr><td>{t(key)}</td><td class='{'win' if wa else ''}'>{fmt(va)}{' ✓' if wa else ''}</td>"
                 f"<td class='{'win' if wb else ''}'>{fmt(vb)}{' ✓' if wb else ''}</td></tr>")
    render(f"<div class='card'><table class='cmp'><tr><th></th><th>{esc(a.name)}</th><th>{esc(b.name)}</th></tr>{body}</table></div>")
    best, other = (a, b) if a.score >= b.score else (b, a)
    if a.score == b.score:
        verdict = t("cmp_tie")
    else:
        verdict = t("cmp_verdict", win=esc(best.name), lose=esc(other.name), diff=best.score - other.score)
    render(f"<div class='card tint'>🏁 {verdict}</div>")
