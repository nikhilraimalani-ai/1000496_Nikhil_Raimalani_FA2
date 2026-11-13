"""Shared UI helpers used by several pages."""
from __future__ import annotations

import datetime as dt

import streamlit as st

from . import actions, scoring, state
from . import catalog as C
from .components import esc
from .i18n import t

BADGE_EMOJI = {"first_scan": "🌱", "swap_pro": "🔄", "water_saver": "💧", "streak7": "🔥", "thrift_hero": "🛍️", "planet_hero": "🌍"}


def inr(n) -> str:
    return f"Rs {n:,.0f}"


def level_name(key: str) -> str:
    return t(f"lvl_{key}")


def verdict(grade: str) -> str:
    return t(f"verdict_{grade}")


def factor_label(name: str) -> str:
    return t(f"f_{name.lower()}")


def display_name() -> str:
    if state.game().guest:
        return t("guest")
    name = state.prefs()["name"].strip()
    return esc(name) if name else t("explorer")


def km_text(co2_kg: float) -> str:
    return t("km_driving", n=f"{scoring.km_driving(co2_kg):,.0f}")


def water_text(litres: float) -> str:
    days = scoring.drinking_days(litres)
    return t("years_water", n=f"{days / 365:.1f}") if days >= 365 else t("days_water", n=f"{days:,.0f}")


def rel_time(ts: dt.datetime, now: dt.datetime) -> str:
    if 0 <= (now - ts).total_seconds() < 120:
        return t("rel_now")
    days = (now.date() - ts.date()).days
    return t("rel_today") if days <= 0 else t("rel_yesterday") if days == 1 else t("rel_days", n=days)


def event_title(kind: str, name: str) -> str:
    return t(f"ev_{kind}", name=name)


def budget_label(key: str) -> str:
    return t("budget_any") if key == "any" else t("budget_under", n=f"{C.BUDGET_CAP[key]:,}")


def style_label(key: str) -> str:
    return t("style_any") if key == "any" else t(f"style_{key.lower()}")


def size_label(key: str) -> str:
    return t("size_any") if key == "any" else key


def timeline(limit: int = 0):
    """Earning events and redemptions merged, newest first: (ts, emoji, title, points)."""
    g = state.game()
    rows = [(e.ts, e.emoji, event_title(e.kind, e.name), e.pts) for e in g.events]
    rows += [(s.ts, C.REWARDS[s.reward_index][0], event_title("redeem", t(C.REWARDS[s.reward_index][1])), -s.cost) for s in g.spends]
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows[:limit] if limit else rows


def back(target: str, label_key: str = "back") -> None:
    with st.container(key="backrow"):
        st.button(t(label_key), icon=":material/arrow_back:", key=f"back_{st.session_state.view}", on_click=state.go, args=(target,))


NAV = (("home", "nav_home", ":material/home:"), ("scan", "nav_scan", ":material/qr_code_scanner:"),
       ("impact", "nav_impact", ":material/eco:"), ("profile", "nav_profile", ":material/person:"))
NAV_ACTIVE = {"home": "home", "scan": "scan", "result": "scan", "alts": "scan", "compare": "scan", "reward": "scan",
              "impact": "impact", "profile": "profile"}


def nav() -> None:
    active = NAV_ACTIVE[st.session_state.view]
    with st.container(key="bottomnav"):
        for col, (view, label_key, icon) in zip(st.columns(4), NAV):
            col.button(t(label_key), icon=icon, key=f"nav_{view}", on_click=state.go, args=(view,), width="stretch",
                       type="primary" if active == view else "secondary")


def compare_partner(p: C.Product) -> C.Product:
    """A sensible default second item to compare against: the best alternative, else the next-best in the category."""
    alts = C.alternatives_for(p)
    if alts:
        return alts[0]
    others = sorted((x for x in C.CATALOG if x.category == p.category and x.id != p.id), key=lambda x: -x.score)
    return others[0] if others else p


def compare_button(p: C.Product, origin: str, key: str) -> None:
    other = compare_partner(p)
    st.button(t("btn_compare_other"), icon=":material/compare_arrows:", key=key, width="stretch",
              on_click=actions.open_compare, args=(p.id, other.id, origin))
