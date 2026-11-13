from __future__ import annotations

import streamlit as st

from .. import actions, state, ui
from .. import catalog as C
from ..components import alt_header, grade_badge, pill, render, section
from ..i18n import t

FILTERS = ("all", "cheaper", "resale", "repair", "new")


def _passes(p: C.Product, orig: C.Product, flt: str) -> bool:
    return {"all": True, "cheaper": p.price < orig.price, "resale": p.kind == "resale",
            "repair": p.kind == "repair", "new": p.kind == "new"}[flt]


def render_page() -> None:
    ui.back("result")
    orig = C.BY_ID[st.session_state.cur]
    render(f"<h2>{t('better_cat', cat=t('cat_' + orig.category.lower()))}</h2><div class='muted'>{t('instead_of', name=orig.name, score=orig.score)}</div>")
    pr = state.prefs()
    state.bind(st.toggle, "match", t("match_toggle"))
    state.bind_state(st.pills, "alt_filter", t("flt_label"), options=list(FILTERS), format_func=lambda f: t(f"flt_{f}"),
                     label_visibility="collapsed")
    alts = C.alternatives_for(orig)
    if not alts:
        render(f"<div class='card'><b>{t('no_alts_title')}</b><div class='muted'>{t('no_alts_sub')}</div></div>")
        return
    shown = [p for p in alts if _passes(p, orig, st.session_state.alt_filter)]
    hidden_by_match = False
    if pr["match"]:
        fits = [p for p in shown if C.matches_preferences(p, pr["size"], pr["shoe"], pr["style"], pr["budget"])]
        hidden_by_match = bool(shown) and not fits
        shown = fits
    if not shown:
        key = "no_match" if hidden_by_match else "no_filter"
        render(f"<div class='card'><b>{t(key + '_title')}</b><div class='muted'>{t(key + '_sub')}</div></div>")
    if shown:
        render(section(t("n_options", n=len(shown)), t("sorted_by")))
    for p in shown:
        with st.container(key=f"alt_{p.id}"):
            sub = f"{p.brand} · {ui.inr(p.price)}"
            render(alt_header(p.emoji, p.name, sub, grade_badge(p.score, p.grade, p.tone)))
            chips = pill(t(f"kind_{p.kind}"), "lime" if p.kind != "new" else "")
            if not pr["match"]:
                if p.price > C.BUDGET_CAP[pr["budget"]]:
                    chips += pill(t("over_budget"), "amber")
                if pr["style"] != "any" and pr["style"] not in p.styles:
                    chips += pill(t("other_style"), "amber")
            diff = orig.price - p.price
            money = t("save_money", n=f"{diff:,}") if diff > 0 else t("more_money", n=f"{-diff:,}")
            saves = t("saves_line", water=f"{max(orig.water_l - p.water_l, 0):,}", co2=f"{max(orig.co2_kg - p.co2_kg, 0):g}", money=money)
            render(f"<div>{chips}</div><div class='muted' style='margin-top:6px'>{saves}</div>")
            label = t("btn_book") if p.kind == "repair" else t("btn_choose")
            st.button(label, icon=":material/check:", type="primary", width="stretch", key=f"choose_{p.id}",
                      on_click=actions.choose, args=(p.id,))
            st.button(t("btn_compare_this"), icon=":material/compare_arrows:", width="stretch", key=f"cmpa_{p.id}",
                      on_click=actions.open_compare, args=(orig.id, p.id, "alts"))
