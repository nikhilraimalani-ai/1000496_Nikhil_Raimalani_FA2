import datetime as dt

import pytest

from sustainstyle import catalog as C
from sustainstyle.game import Game, level_info

NOW = dt.datetime(2026, 11, 12, 12, 0)
TODAY = NOW.date()


def day(n, hour=10):
    return (NOW - dt.timedelta(days=n)).replace(hour=hour)


def test_empty_game_is_all_zero():
    g = Game()
    assert (g.lifetime, g.balance, g.scans, g.swaps, g.skips) == (0, 0, 0, 0, 0)
    assert g.streak(TODAY) == 0
    assert g.weekly_points(TODAY) == [0] * 7
    assert g.level().key == "seedling" and g.level().to_next == 200 and g.level().fraction == 0
    assert g.redeem(0, NOW) is False


def test_scan_swap_flow_awards_and_measures_savings():
    g = Game()
    tee, pre = C.BY_ID["tee"], C.BY_ID["tee_pre"]
    g.scan(tee, NOW)
    r = g.swap(tee, pre, NOW)
    assert g.lifetime == C.POINTS_SCAN + C.POINTS_SWAP == g.balance
    assert (g.scans, g.swaps, g.resale_swaps) == (1, 1, 1)
    assert r.money == 250 and r.water == 2660 and r.co2 == pytest.approx(10.2)
    assert g.closet[0].name == "Pre-loved Tee" and g.closet[0].note == "swapped"
    assert g.money_saved == 250 and g.water_saved == 2660 and g.co2_saved == 10.2


def test_choosing_a_dearer_alternative_never_records_negative_savings():
    g = Game()
    r = g.swap(C.BY_ID["tee"], C.BY_ID["tee_lin"], NOW)       # Rs 150 more
    assert r.money == 0 and g.money_saved == 0
    assert g.water_saved > 0 and g.co2_saved > 0


def test_repair_is_noted_as_booked_and_save_only_as_saved():
    g = Game()
    g.swap(C.BY_ID["tee"], C.BY_ID["tee_rep"], NOW)
    g.swap(C.BY_ID["tee"], C.BY_ID["tee_org"], NOW, saved_only=True)
    assert [c.note for c in g.closet] == ["saved", "booked"]


def test_skip_and_keep():
    g = Game()
    r = g.skip(C.BY_ID["shoe"], NOW)
    assert r.pts == 30 and r.money == 3499 and g.skips == 1 and g.closet[0].note == "skipped"
    g.keep(C.BY_ID["shirt"], NOW)
    assert g.lifetime == 50


def test_redeem_spends_balance_but_never_lowers_level_or_lifetime():
    g = Game()
    for _ in range(25):
        g.scan(C.BY_ID["tee"], NOW)          # 250 lifetime
    assert g.level().key == "sprout"
    assert g.redeem(0, NOW) is True           # Rs tree: 100
    assert g.redeem(0, NOW) is False          # once only
    assert g.redeem(1, NOW) is False          # 200 > 150 balance
    assert g.balance == 150 and g.lifetime == 250 and g.level().key == "sprout"
    assert g.redeemed(0) and not g.redeemed(1)


def test_redeem_rejects_bad_index():
    g = Game()
    for _ in range(100):
        g.scan(C.BY_ID["tee"], NOW)
    assert g.redeem(-1, NOW) is False and g.redeem(99, NOW) is False


def test_level_up_is_reported_exactly_once():
    g = Game()
    for _ in range(19):
        g.scan(C.BY_ID["tee"], NOW)           # 190
    r = g.swap(C.BY_ID["tee"], C.BY_ID["tee_pre"], NOW)   # 240 -> crosses 200
    assert r.level_up == "sprout"
    r2 = g.swap(C.BY_ID["tee"], C.BY_ID["tee_pre"], NOW)
    assert r2.level_up is None


def test_level_info_edges():
    assert level_info(0).key == "seedling"
    assert level_info(199).key == "seedling" and level_info(199).to_next == 1
    assert level_info(200).key == "sprout" and level_info(200).fraction == 0
    top = level_info(5000)
    assert top.key == "planet_hero" and top.next_key is None and top.to_next is None and top.fraction == 1.0


def test_streak_counts_consecutive_days_and_tolerates_no_action_yet_today():
    g = Game()
    for n in (3, 2, 1):
        g.scan(C.BY_ID["tee"], day(n))
    assert g.streak(TODAY) == 3                # today empty: still alive through yesterday
    g.scan(C.BY_ID["tee"], day(0))
    assert g.streak(TODAY) == 4
    g2 = Game()
    g2.scan(C.BY_ID["tee"], day(2))
    assert g2.streak(TODAY) == 0               # yesterday missed: streak is broken
    g3 = Game()
    for n in (0, 1, 3):
        g3.scan(C.BY_ID["tee"], day(n))
    assert g3.streak(TODAY) == 2               # gap on day 2


def test_streak_ignores_spending_only_days():
    g = Game()
    for _ in range(30):
        g.scan(C.BY_ID["tee"], day(5))
    g.redeem(0, day(0))                        # spending is not an earning action
    assert g.streak(TODAY) == 0


def test_weekly_points_window_and_order():
    g = Game()
    g.scan(C.BY_ID["tee"], day(6))
    g.swap(C.BY_ID["tee"], C.BY_ID["tee_pre"], day(0))
    g.scan(C.BY_ID["tee"], day(7))             # outside the 7-day window
    assert g.weekly_points(TODAY) == [10, 0, 0, 0, 0, 0, 50]


def test_challenge_completes_once_with_bonus():
    g = Game()
    rewards = [g.log_wear(NOW) for _ in range(C.CHALLENGE_GOAL + 5)]
    assert g.wears == C.CHALLENGE_GOAL
    done = [r for r in rewards if r is not None]
    assert len(done) == 1 and done[0].pts == C.CHALLENGE_BONUS and g.lifetime == C.CHALLENGE_BONUS


def test_badges_progress():
    g = Game()
    b = {i: (cur, goal) for i, cur, goal in g.badges(TODAY)}
    assert b["first_scan"] == (0, 1)
    g.scan(C.BY_ID["tee"], NOW)
    assert {i: cur for i, cur, _ in g.badges(TODAY)}["first_scan"] == 1
    assert len(b) == 6


def test_outfit_saved_to_closet():
    g = Game()
    g.save_outfit("o_weekend", ("tee_pre", "jeans_pre"), NOW)
    c = g.closet[0]
    assert c.note == "outfit" and c.name == "o_weekend" and c.detail == "Pre-loved Tee + Pre-loved Denim"


def test_sample_data_is_consistent_and_resettable():
    g = Game.with_sample_data(NOW)
    assert g.sample and g.lifetime > 0 and g.balance == g.lifetime
    assert g.scans == 6 and g.swaps == 2 and g.skips == 2 and g.resale_swaps == 2
    assert g.streak(TODAY) == 5                # days 4, 3, 2, 1, 0 (day 5 empty)
    assert sum(g.weekly_points(TODAY)) == g.lifetime
    assert g.closet == sorted(g.closet, key=lambda c: c.ts, reverse=True)
    assert g.wears == 21
    g.reset()
    assert (g.lifetime, g.scans, g.wears, g.closet, g.sample) == (0, 0, 0, [], False)
    assert g.streak(TODAY) == 0
