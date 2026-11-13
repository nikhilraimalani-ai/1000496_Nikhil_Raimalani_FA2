import csv
import datetime as dt
import io

from sustainstyle import catalog as C
from sustainstyle.game import Game
from sustainstyle.report import build_csv

NOW = dt.datetime(2026, 11, 12, 12, 0)


def rows(text):
    return list(csv.reader(io.StringIO(text)))


def test_empty_report_has_headers_and_no_events():
    r = rows(build_csv(Game(), NOW))
    assert r[0][0] == "SustainStyle impact report" and ["Scans", "0"] in r
    assert r[-1][0] == "date"


def test_report_lists_events_in_time_order_and_spends():
    g = Game()
    g.swap(C.BY_ID["tee"], C.BY_ID["tee_pre"], NOW)
    g.scan(C.BY_ID["tee"], NOW - dt.timedelta(days=1))
    for _ in range(20):
        g.scan(C.BY_ID["tee"], NOW)
    g.redeem(0, NOW)
    r = rows(build_csv(g, NOW))
    body = r[r.index(["date", "type", "item", "points", "water_l_saved", "rupees_saved", "co2_kg_avoided"]) + 1:]
    assert body[0][1] == "scan" and body[0][0] == "2026-11-11 12:00"
    assert body[-1][1] == "redeem" and body[-1][3] == "-100"
    assert ["Swaps", "1"] in r and ["Money saved (Rs)", "250"] in r
