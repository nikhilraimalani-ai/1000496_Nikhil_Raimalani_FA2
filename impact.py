from __future__ import annotations

import streamlit as st

from .. import actions, state, ui
from .. import catalog as C
from ..components import badge_grid, bar_chart, card, hero, leaderboard, list_row, render, section, tiles, week_dots
from ..i18n import t

WEEKDAYS = ("wd_mon", "wd_tue", "wd_wed", "wd_thu", "wd_fri", "wd_sat", "wd_sun")
BADGE_INFO = {"first_scan": "bd_first", "swap_pro": "bd_swap", "water_saver": "bd_water", "streak7": "bd_streak",
              "thrift_hero": "bd_thrift", "planet_hero": "bd_planet"}


def render_page() -> None:
    g, now = state.game(), state.now_local()
    today = now.date()
    li = g.level()
    render(hero(top_left=f"<div class='hello'>{t('impact_title')}</div><div class='hname'>{ui.level_name(li.key)}</div>", top_right="",
                big=f"{g.lifetime:,}", big_label=t("lifetime_pts"), frac=li.fraction,
                footer="🏅 " + (t("level_progress", lvl=ui.level_name(li.key), n=li.to_next, nxt=ui.level_name(li.next_key)) if li.next_key else t("top_level", lvl=ui.level_name(li.key)))))
    st.write("")
    render(tiles([("💧", f"{g.water_saved:,}", t("tile_water")), ("🪙", ui.inr(g.money_saved), t("tile_money")), ("☁️", f"{g.co2_saved:g} kg", t("tile_co2"))]))

    week = g.weekly_points(today)
    days = [today.fromordinal(today.toordinal() - 6 + i) for i in range(7)]
    render(section(t("this_week"), t("pts_per_day")) + card(bar_chart(week, [t(WEEKDAYS[d.weekday()]) for d in days], 6)))
    streak = g.streak(today)
    render(section(t("streak_title"), t("streak_n", n=streak)) + card(week_dots([str(d.day) for d in days], streak)))

    render(section(t("challenge_title"), f"{g.wears}/{C.CHALLENGE_GOAL}"))
    render(card(f"<b>{t('challenge_name')}</b><div class='muted'>{t('challenge_sub', n=C.CHALLENGE_BONUS)}</div>"))
    st.progress(min(g.wears / C.CHALLENGE_GOAL, 1.0), text=t("challenge_progress", n=g.wears, goal=C.CHALLENGE_GOAL))
    done = g.wears >= C.CHALLENGE_GOAL
    st.button(t("challenge_done") if done else t("btn_log_wear"), icon=":material/checkroom:", width="stretch", key="wear_btn",
              disabled=done, on_click=actions.log_wear)

    render(section(t("badges_title")))
    items = []
    for bid, cur, goal in g.badges(today):
        items.append((ui.BADGE_EMOJI[bid], t(BADGE_INFO[bid]), f"{min(cur, goal):,}/{goal:,}", cur >= goal))
    render(badge_grid(items))

    render(section(t("rewards_title"), t("to_spend") + f": {g.balance:,}"))
    for i, (emoji, key, cost) in enumerate(C.REWARDS):
        done_r = g.redeemed(i)
        render(card(list_row(emoji, t(key), t("costs_pts", n=cost) if not done_r else t("redeemed"), "✓" if done_r else "")))
        short = cost - g.balance
        label = t("redeemed") if done_r else t("btn_redeem") if short <= 0 else t("to_go", n=short)
        st.button(label, key=f"redeem_{i}", width="stretch", disabled=done_r or short > 0, on_click=actions.redeem, args=(i,))

    render(section(t("community"), t("sample_friends")))
    name = ui.display_name()
    rows = sorted(list(C.FRIENDS) + [(f"{name} ({t('you')})", g.lifetime)], key=lambda r: -r[1])
    render(leaderboard([(n, p, n.endswith(f"({t('you')})")) for n, p in rows]))

    render(section(t("activity"), ""))
    rows_t = ui.timeline(5)
    if rows_t:
        render(card("".join(list_row(e, title, ui.rel_time(ts, now), f"{'+' if p > 0 else ''}{p}", p < 0) for ts, e, title, p in rows_t)))
        full = ui.timeline()
        if len(full) > 5:
            with st.expander(t("all_activity")):
                render("".join(list_row(e, title, ui.rel_time(ts, now), f"{'+' if p > 0 else ''}{p}", p < 0) for ts, e, title, p in full[5:]))
    else:
        render(card(f"<b>{t('no_activity_title')}</b><div class='muted'>{t('no_activity_sub')}</div>"))
