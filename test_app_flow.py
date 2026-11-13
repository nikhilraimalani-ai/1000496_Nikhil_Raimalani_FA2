"""Headless end-to-end runs of the real app with Streamlit's AppTest."""
import pathlib

import pytest
from streamlit.testing.v1 import AppTest


def fresh():
    at = AppTest.from_file(str(pathlib.Path(__file__).resolve().parent.parent / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    return at


def click(at, key):
    at.button(key=key).click().run()
    assert not at.exception, [e.value for e in at.exception]


def test_home_renders():
    at = fresh()
    assert at.session_state.view == "home"


def test_scan_to_swap_flow_updates_points():
    at = fresh()
    before = at.session_state.game.lifetime
    click(at, "qs_jeans")
    assert at.session_state.view == "result" and at.session_state.cur == "jeans"
    click(at, "alts")
    assert at.session_state.view == "alts"
    choose = [b for b in at.button if b.key and b.key.startswith("choose_")]
    assert choose
    choose[0].click().run()
    assert not at.exception
    assert at.session_state.view == "reward"
    assert at.session_state.game.lifetime == before + 10 + 50


def test_skip_flow():
    at = fresh()
    click(at, "qs_shoe")
    click(at, "skip")
    assert at.session_state.view == "reward"


def test_keep_flow_on_green_item():
    at = fresh()
    click(at, "qs_shirt")
    p = at.session_state.cur
    from sustainstyle import catalog as C
    if C.BY_ID[p].grade in "AB":
        click(at, "keep")
        assert at.session_state.view == "reward"


@pytest.mark.parametrize("view", ["home", "scan", "impact", "profile", "compare"])
def test_every_page_in_both_languages(view):
    at = fresh()
    at.session_state.prefs["lang"] = "hi"
    at.session_state.view = view
    at.run()
    assert not at.exception, [e.value for e in at.exception]


def test_compare_page_from_home():
    at = fresh()
    click(at, "home_compare")
    assert at.session_state.view == "compare"


def test_log_wear_and_challenge():
    at = fresh()
    at.session_state.view = "impact"
    at.run()
    n = at.session_state.game.wears
    click(at, "wear_btn")
    assert at.session_state.game.wears == n + 1


def test_redeem_reduces_balance_not_level():
    at = fresh()
    g = at.session_state.game
    g.events.append(type(g.events[0])("scan", "x", "📷", 500, g.events[0].ts))
    at.session_state.view = "impact"
    at.run()
    level, bal = g.level().key, g.balance
    click(at, "redeem_0")
    assert at.session_state.game.balance == bal - 100
    assert at.session_state.game.level().key == level


def test_scan_page_barcode_and_navigation():
    at = fresh()
    click(at, "nav_scan")
    assert at.session_state.view == "scan"
    click(at, "back_scan")
    assert at.session_state.view == "home"


def test_clear_sample_data_and_empty_states():
    at = fresh()
    at.session_state.view = "profile"
    at.run()
    click(at, "clear")
    assert not at.session_state.game.events
    for v in ("home", "impact", "profile"):
        at.session_state.view = v
        at.run()
        assert not at.exception, (v, [e.value for e in at.exception])


def test_settings_persist_across_pages():
    at = fresh()
    at.session_state.view = "profile"
    at.run()
    at.selectbox(key="w_budget").select("500").run()
    assert at.session_state.prefs["budget"] == "500"
    at.session_state.view = "home"
    at.run()
    at.session_state.view = "profile"
    at.run()
    assert at.selectbox(key="w_budget").value == "500"


def test_guest_mode():
    at = fresh()
    click(at, "guest_btn")
    assert at.session_state.game.guest
