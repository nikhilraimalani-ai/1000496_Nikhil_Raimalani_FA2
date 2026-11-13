from __future__ import annotations

import streamlit as st

from .. import actions, state, ui
from .. import catalog as C
from ..components import hero, list_row, pill, render, section, tiles, card
from ..i18n import t


def render_page() -> None:
    g, now = state.game(), state.now_local()
    li = g.level()
    streak = g.streak(now.date())
    greet = "greet_morning" if now.hour < 12 else "greet_afternoon" if now.hour < 18 else "greet_evening"
    if li.next_key:
        footer = "🏅 " + t("level_progress", lvl=ui.level_name(li.key), n=li.to_next, nxt=ui.level_name(li.next_key))
    else:
        footer = "🏅 " + t("top_level", lvl=ui.level_name(li.key))
    chip = pill(f"🔥 {t('streak_n', n=streak)}" if streak else t("start_streak"), "lime")
    render(hero(top_left=f"<div class='hello'>{t(greet)}</div><div class='hname'>{ui.display_name()} 🌿</div>",
                top_right=chip, big=f"{g.balance:,}", big_label=t("to_spend"), frac=li.fraction, footer=footer))
    if g.sample:
        render(f"<div class='muted center' style='margin:8px 0 0'>{t('sample_note')}</div>")
    st.write("")
    st.button(t("btn_scan_tag"), icon=":material/qr_code_scanner:", type="primary", width="stretch", key="home_scan",
              on_click=state.go, args=("scan",))
    c1, c2 = st.columns(2)
    c1.button(t("btn_guest_on") if g.guest else t("btn_guest"), icon=":material/person:", width="stretch", key="guest_btn",
              on_click=actions.guest_on, disabled=g.guest)
    c2.button(t("btn_compare"), icon=":material/compare_arrows:", width="stretch", key="home_compare",
              on_click=actions.open_compare, args=("tee", "tee_pre", "home"))

    render(section(t("your_impact"), t("so_far")) + tiles([
        ("💧", f"{g.water_saved:,}", t("tile_water")), ("🪙", ui.inr(g.money_saved), t("tile_money")),
        ("☁️", f"{g.co2_saved:g} kg", t("tile_co2"))]))
    render(card(f"<div style='display:flex;gap:14px;align-items:center'><div style='font-size:34px'>💡</div>"
                f"<div><b>{t('did_you_know')}</b><div class='muted' style='color:#2d4a39'>{t('tip_text')}</div></div></div>", "tint"))

    render(section(t("quick_scan"), t("tap_to_scan")))
    ids = C.SAMPLE_IDS
    for i in range(0, len(ids), 2):
        cols = st.columns(2)
        for col, pid in zip(cols, ids[i:i + 2]):
            p = C.BY_ID[pid]
            col.button(f"{p.emoji} {p.name}", key=f"qs_{pid}", width="stretch", on_click=actions.quick_scan, args=(pid,))

    render(section(t("recent_activity"), t("latest")))
    rows = ui.timeline(3)
    if rows:
        render(card("".join(list_row(e, title, ui.rel_time(ts, now), f"{'+' if pts > 0 else ''}{pts}", pts < 0) for ts, e, title, pts in rows)))
    else:
        render(card(f"<b>{t('no_activity_title')}</b><div class='muted'>{t('no_activity_sub')}</div>"))
