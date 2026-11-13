from __future__ import annotations

import time

import streamlit as st

from .. import actions, state, ui
from .. import catalog as C
from ..components import render, viewfinder
from ..i18n import t


def _scan(item_id: str) -> None:
    """Simulated scan: short progress animation, then record it and open the result."""
    bar = st.progress(0, text=t("scanning_read"))
    for i in range(1, 11):
        time.sleep(0.06)
        bar.progress(i * 10, text=t("scanning_match") if i > 5 else t("scanning_read"))
    actions.register_scan(item_id)
    state.go("result")
    st.rerun()


def render_page() -> None:
    ui.back("home")
    render(f"<h2>{t('scan_title')}</h2><div class='muted'>{t('scan_sub')}</div>")
    item = C.BY_ID[st.session_state.sel]
    size = "–" if item.is_shoe else "M"
    render("<div style='height:10px'></div>" + viewfinder(f"{item.name} · {size} · {ui.inr(item.price)}", item.barcode, t("scan_hint")))
    st.write("")
    render(f"<div class='eyebrow' style='margin:6px 2px'>{t('sample_item')}</div>")
    state.bind_state(st.pills, "sel", t("sample_item"), options=list(C.SAMPLE_IDS), format_func=lambda i: f"{C.BY_ID[i].emoji} {C.BY_ID[i].name}",
                     label_visibility="collapsed")
    if st.button(t("btn_scan_now"), icon=":material/center_focus_strong:", type="primary", width="stretch", key="scan_now"):
        _scan(st.session_state.sel)

    with st.expander(t("barcode_exp")):
        code = st.text_input(t("barcode_exp"), placeholder="8901 1122 3344", label_visibility="collapsed", key="bc_in", max_chars=24)
        if st.button(t("btn_find"), key="bc_go", width="stretch"):
            hit = C.find_by_barcode(code)
            if hit:
                _scan(hit.id)
            st.error(t("bc_not_found"))

    with st.expander(t("search_exp")):
        picked = st.selectbox(t("search_exp"), [p.id for p in C.CATALOG], index=None, placeholder=t("search_ph"),
                              format_func=lambda i: f"{C.BY_ID[i].emoji} {C.BY_ID[i].name} · {C.BY_ID[i].brand}",
                              label_visibility="collapsed", key="search_item")
        if st.button(t("btn_scan_item"), key="search_go", width="stretch", disabled=picked is None):
            _scan(picked)

    with st.expander(t("cam_exp")):
        use_cam = st.toggle(t("cam_on"), key="cam_on")
        photo = st.camera_input(t("cam_label"), label_visibility="collapsed") if use_cam else None
        if photo is not None:
            st.caption(t("cam_note"))
            if st.button(t("btn_analyse"), key="photo_go", width="stretch"):
                _scan(st.session_state.sel)
