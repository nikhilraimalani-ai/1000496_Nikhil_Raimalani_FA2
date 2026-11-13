"""Button callbacks. Each one changes the game, then navigates. Callbacks run before the next render,
so they never need st.rerun()."""
from __future__ import annotations

import streamlit as st

from . import catalog as C
from . import state
from .i18n import t


def _finish(reward) -> None:
    st.session_state.reward = reward
    st.session_state.celebrate = True
    state.go("reward")


def register_scan(item_id: str) -> None:
    item = C.BY_ID[item_id]
    state.game().scan(item, state.now_local())
    st.session_state.cur = item_id
    st.toast(t("toast_scan", pts=C.POINTS_SCAN), icon="🌿")


def quick_scan(item_id: str) -> None:
    """Home screen shortcut: scan a sample straight away."""
    register_scan(item_id)
    state.go("result")


def choose(alt_id: str, saved_only: bool = False) -> None:
    orig = C.BY_ID[st.session_state.cur]
    alt = C.BY_ID[alt_id]
    _finish(state.game().swap(orig, alt, state.now_local(), saved_only=saved_only))


def skip_current() -> None:
    _finish(state.game().skip(C.BY_ID[st.session_state.cur], state.now_local()))


def keep_current() -> None:
    _finish(state.game().keep(C.BY_ID[st.session_state.cur], state.now_local()))


def log_wear() -> None:
    g = state.game()
    before = g.wears
    reward = g.log_wear(state.now_local())
    if reward is not None:
        st.toast(t("toast_challenge", pts=C.CHALLENGE_BONUS), icon="🏆")
    elif g.wears > before:
        st.toast(t("toast_wear", n=g.wears, goal=C.CHALLENGE_GOAL), icon="👕")


def redeem(index: int) -> None:
    if state.game().redeem(index, state.now_local()):
        st.toast(t("toast_redeemed", name=t(C.REWARDS[index][1])), icon="🎟️")


def save_outfit(index: int) -> None:
    key, ids = C.OUTFITS[index]
    state.game().save_outfit(key, ids, state.now_local())
    st.toast(t("toast_outfit"), icon="👗")


def clear_sample() -> None:
    state.game().reset()
    st.toast(t("toast_cleared"), icon="🌱")


def guest_on() -> None:
    state.game().guest = True
    st.toast(t("toast_guest"), icon="👤")


def open_compare(a_id: str, b_id: str, origin: str) -> None:
    st.session_state.cmp_a, st.session_state.cmp_b, st.session_state.cmp_from = a_id, b_id, origin
    state.go("compare")
