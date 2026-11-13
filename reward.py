from __future__ import annotations

import streamlit as st

from .. import state, ui
from ..components import card, pill, render, tiles
from ..i18n import t


def render_page() -> None:
    r = st.session_state.reward
    if r is None:
        state.go("home")
        st.rerun()
    if st.session_state.celebrate:
        st.balloons()
        st.session_state.celebrate = False
    g, now = state.game(), state.now_local()
    li = g.level()
    lvl = f"<div>{pill('🏅 ' + t('level_up', lvl=ui.level_name(r.level_up)), 'lime')}</div>" if r.level_up else ""
    render(f"<div class='celebrate'><div style='font-size:64px'>{r.emoji}</div><h1>{t('rw_title')}</h1>"
           f"<div class='muted'>{t('rw_sub_' + r.kind, name=r.name)}</div>{lvl}"
           f"<div class='bigpts' style='color:var(--g700);margin:14px 0 2px'>+{r.pts}</div><div class='eyebrow'>{t('rw_pts')}</div></div>")
    if r.water or r.money or r.co2:
        render(tiles([("💧", f"{r.water:,}", t("tile_water")), ("🪙", ui.inr(r.money), t("tile_money")), ("☁️", f"{r.co2:g} kg", t("tile_co2"))]))
    nxt = t("level_progress", lvl=ui.level_name(li.key), n=li.to_next, nxt=ui.level_name(li.next_key)) if li.next_key else t("top_level", lvl=ui.level_name(li.key))
    render(card(f"<div class='eyebrow'>{t('to_spend')}</div><div class='bigpts' style='font-size:36px'>{g.balance:,}</div>"
                f"<div class='muted'>🏅 {nxt}</div><div class='muted'>🔥 {t('streak_n', n=g.streak(now.date()))}</div>"))
    st.button(t("scan_another"), icon=":material/qr_code_scanner:", type="primary", width="stretch", key="rw_again", on_click=state.go, args=("scan",))
    st.button(t("nav_impact"), icon=":material/eco:", width="stretch", key="rw_impact", on_click=state.go, args=("impact",))
    with st.expander(t("share_title")):
        st.code(t("share_text", pts=g.lifetime, water=f"{g.water_saved:,}"), language=None)
