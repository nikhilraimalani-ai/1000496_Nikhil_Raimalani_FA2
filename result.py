from __future__ import annotations

import streamlit as st

from .. import actions, scoring, state, ui
from .. import catalog as C
from ..components import card, factor_row, gauge, grade_badge, pill, product_head, render, section, traffic_light
from ..i18n import t

WEIGHT = {"Materials": "35%", "Carbon": "25%", "Water": "25%", "Labour": "15%"}


def factor_note(name: str, p: C.Product) -> str:
    if name == "Materials":
        return p.material
    if name == "Carbon":
        return f"{p.co2_kg:g} kg CO₂ · {ui.km_text(p.co2_kg)}"
    if name == "Water":
        return f"{p.water_l:,} L · {ui.water_text(p.water_l)}"
    return t("note_labour")


def render_page() -> None:
    ui.back("scan")
    p = C.BY_ID[st.session_state.cur]
    kind = {"new": "kind_new", "resale": "kind_resale", "repair": "kind_repair"}[p.kind]
    chips = pill(t(kind), "lime" if p.kind != "new" else "") + "".join(pill(f"✔ {c}") for c in p.certs)
    render(product_head(p.emoji, p.name, f"{p.brand} · {ui.inr(p.price)}", chips))
    conf = {"High": "conf_high", "Medium": "conf_med", "Low": "conf_low"}[p.confidence]
    verdict = ui.verdict(p.grade)
    render(card(f"<div style='display:flex;gap:16px;align-items:center'>{gauge(p.score, p.tone, t('out_of'), f'{p.score} {t('out_of')}')}"
                f"<div style='flex:1;min-width:0'>{grade_badge(p.score, p.grade, p.tone)}"
                f"<div style='font-weight:700;margin-top:6px'>{verdict}</div>{traffic_light(p.tone)}"
                f"<div class='muted' style='margin-top:6px'>{t(conf)}</div></div></div>"))
    render(card(f"<div class='eyebrow'>{t('everyday')}</div><div style='margin-top:6px'>🚗 {ui.km_text(p.co2_kg)}<br>💧 {ui.water_text(p.water_l)}</div>"))
    render(section(t("why_score"), t("weights")) + "".join(
        factor_row(ui.factor_label(n), WEIGHT[n], int(round(v)), scoring.factor_tone(v), factor_note(n, p)) for n, v in p.factors.items()))
    with st.expander(t("how_calc")):
        st.markdown(t("how_calc_body"))
    with st.expander(t("cpw_title")):
        wears = st.slider(t("cpw_wears"), 1, 100, 30, key=f"cpw_{p.id}")
        st.metric(t("cpw_cost"), ui.inr(scoring.cost_per_wear(p.price, wears)))
        st.caption(t("cpw_water", n=f"{scoring.impact_per_wear(p.water_l, wears):,.0f}", co2=f"{scoring.impact_per_wear(p.co2_kg, wears):.2f}"))

    st.write("")
    if p.grade in ("A", "B"):
        st.button(t("btn_keep"), icon=":material/favorite:", type="primary", width="stretch", key="keep", on_click=actions.keep_current)
        if C.alternatives_for(p):
            st.button(t("btn_alts_better"), icon=":material/swap_horiz:", width="stretch", key="alts_better", on_click=state.go, args=("alts",))
    else:
        st.button(t("btn_alts"), icon=":material/swap_horiz:", type="primary", width="stretch", key="alts", on_click=state.go, args=("alts",))
        st.button(t("btn_skip"), icon=":material/block:", width="stretch", key="skip", on_click=actions.skip_current)
    ui.compare_button(p, "result", "res_compare")
    st.button(t("scan_another"), icon=":material/qr_code_scanner:", width="stretch", key="again", on_click=state.go, args=("scan",))
