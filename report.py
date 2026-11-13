"""CSV export of the user's impact (pure Python, unit-tested)."""
from __future__ import annotations

import csv
import datetime as dt
import io

from .game import Game


def build_csv(game: Game, now: dt.datetime) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["SustainStyle impact report", now.isoformat(timespec="minutes")])
    w.writerow(["Sample data" if game.sample else "Your data"])
    for label, value in (("GreenPoints balance", game.balance), ("Lifetime points", game.lifetime), ("Scans", game.scans),
                         ("Swaps", game.swaps), ("Skipped purchases", game.skips), ("Water saved (L)", game.water_saved),
                         ("Money saved (Rs)", game.money_saved), ("CO2 avoided (kg)", game.co2_saved),
                         ("Streak (days)", game.streak(now.date()))):
        w.writerow([label, value])
    w.writerow([])
    w.writerow(["date", "type", "item", "points", "water_l_saved", "rupees_saved", "co2_kg_avoided"])
    for e in sorted(game.events, key=lambda ev: ev.ts):
        w.writerow([e.ts.strftime("%Y-%m-%d %H:%M"), e.kind, e.name, e.pts, e.water, e.money, round(e.co2, 1)])
    for s in sorted(game.spends, key=lambda sp: sp.ts):
        w.writerow([s.ts.strftime("%Y-%m-%d %H:%M"), "redeem", s.reward_index, -s.cost, 0, 0, 0])
    return buf.getvalue()
