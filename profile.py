from __future__ import annotations

import streamlit as st

from .. import actions, i18n, report, state, ui
from .. import catalog as C
from ..components import card, esc, list_row, render, section
from ..i18n import t


def _closet_sub(c) -> str:
    sub = t(f"cl_{c.note}")
    if not c.detail:
        return sub
    return f"{sub} · {esc(c.detail)}" if c.note == "outfit" else f"{sub} · {ui.inr(int(c.detail))}"


def render_page() -> None:
    g, now = state.game(), state.now_local()
    li = g.level()
    name = ui.display_name()
    initial = esc((state.prefs()["name"].strip() or "S")[0].upper()) if not g.guest else "G"
    render(f"<div class='card' style='display:flex;gap:16px;align-items:center'><div class='avatar'>{initial}</div>"
           f"<div><div class='pname'>{name}</div><div class='muted'>🏅 {ui.level_name(li.key)} · {g.lifetime:,} {t('lifetime_pts')}</div></div></div>")

    swaps = [e for e in g.events if e.kind in ("swap", "skip", "keep")]
    render(card(f"<div class='eyebrow'>{t('your_choices')}</div><div style='margin-top:6px'>"
                f"🔄 {t('n_swaps', n=g.swaps)} · 🚫 {t('n_skips', n=g.skips)} · 📷 {t('n_scans', n=g.scans)}</div>"
                f"<div class='muted'>{t('choices_note', n=len(swaps))}</div>"))

    render(section(t("outfits_title"), t("outfits_sub")))
    for i, (key, ids) in enumerate(C.OUTFITS):
        items = [C.BY_ID[x] for x in ids]
        avg = round(sum(p.score for p in items) / len(items))
        render(card(list_row("👗", t(key), " + ".join(p.name for p in items), f"{avg}") + f"<div class='muted'>{t('avg_score')}</div>"))
        st.button(t("btn_save_outfit"), key=f"outfit_{i}", width="stretch", on_click=actions.save_outfit, args=(i,))

    render(section(t("closet_title"), t("closet_sub")))
    if g.closet:
        rows = "".join(list_row(c.emoji, t(c.name) if c.note == "outfit" else esc(c.name), _closet_sub(c)) for c in g.closet)
        render(card(rows))
    else:
        render(card(f"<b>{t('closet_empty_title')}</b><div class='muted'>{t('closet_empty_sub')}</div>"))

    render(section(t("settings_title")))
    state.bind(st.text_input, "name", t("set_name"), max_chars=24)
    state.bind(st.selectbox, "lang", t("set_lang"), options=list(i18n.LANGS), format_func=lambda k: i18n.LANGS[k])
    c1, c2 = st.columns(2)
    with c1:
        state.bind(st.selectbox, "size", t("set_size"), options=["any", *C.APPAREL_SIZES], format_func=ui.size_label)
    with c2:
        state.bind(st.selectbox, "shoe", t("set_shoe"), options=["any", *C.SHOE_SIZES], format_func=ui.size_label)
    state.bind(st.selectbox, "style", t("set_style"), options=["any", *C.STYLES], format_func=ui.style_label)
    state.bind(st.selectbox, "budget", t("set_budget"), options=[b for b, _ in C.BUDGETS], format_func=ui.budget_label)
    state.bind(st.toggle, "large", t("set_large"))
    state.bind(st.toggle, "reduce_motion", t("set_motion"))

    render(section(t("data_title")))
    if g.sample:
        render(f"<div class='muted'>{t('sample_note')}</div>")
    st.download_button(t("btn_export"), data=report.build_csv(g, now), file_name="sustainstyle_activity.csv", mime="text/csv",
                       icon=":material/download:", width="stretch", key="export")
    st.button(t("btn_clear"), icon=":material/delete:", width="stretch", key="clear", on_click=actions.clear_sample)
