"""GreenPoints engine. Pure Python, no Streamlit, time is always passed in so it is testable.

Everything shown to the user (points, level, streak, weekly chart, totals, badges) is DERIVED from the
event log. There are no separate counters to drift out of sync.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import Optional

from . import catalog as C


@dataclass
class Event:
    kind: str                  # scan | swap | skip | keep | challenge
    name: str                  # product name (or "" for challenge)
    emoji: str
    pts: int
    ts: dt.datetime            # naive local time
    water: int = 0
    money: int = 0
    co2: float = 0.0
    resale: bool = False


@dataclass
class Spend:
    reward_index: int
    cost: int
    ts: dt.datetime


@dataclass
class ClosetItem:
    emoji: str
    name: str
    note: str                  # swapped | saved | booked | skipped | outfit
    detail: str = ""           # price text, or outfit contents
    ts: Optional[dt.datetime] = None


@dataclass
class Reward:
    """What the 'Great choice!' screen shows after an action."""
    kind: str
    name: str
    emoji: str
    pts: int
    water: int
    money: int
    co2: float
    level_up: Optional[str] = None


def level_index(lifetime: int) -> int:
    return max(i for i, (_, floor) in enumerate(C.LEVELS) if lifetime >= floor)


@dataclass
class LevelInfo:
    key: str
    index: int
    next_key: Optional[str]
    to_next: Optional[int]
    fraction: float


def level_info(lifetime: int) -> LevelInfo:
    i = level_index(lifetime)
    key = C.LEVELS[i][0]
    if i == len(C.LEVELS) - 1:
        return LevelInfo(key, i, None, None, 1.0)
    nxt_key, nxt_floor = C.LEVELS[i + 1]
    base = C.LEVELS[i][1]
    return LevelInfo(key, i, nxt_key, nxt_floor - lifetime, (lifetime - base) / (nxt_floor - base))


@dataclass
class Game:
    events: list = field(default_factory=list)
    spends: list = field(default_factory=list)
    closet: list = field(default_factory=list)
    wears: int = 0
    guest: bool = False
    sample: bool = False

    # ------------------------------------------------------------------ derived values
    @property
    def lifetime(self) -> int:
        return sum(e.pts for e in self.events if e.pts > 0)

    @property
    def spent(self) -> int:
        return sum(s.cost for s in self.spends)

    @property
    def balance(self) -> int:
        return self.lifetime - self.spent

    @property
    def scans(self) -> int:
        return sum(1 for e in self.events if e.kind == "scan")

    @property
    def swaps(self) -> int:
        return sum(1 for e in self.events if e.kind == "swap")

    @property
    def skips(self) -> int:
        return sum(1 for e in self.events if e.kind == "skip")

    @property
    def resale_swaps(self) -> int:
        return sum(1 for e in self.events if e.kind == "swap" and e.resale)

    @property
    def water_saved(self) -> int:
        return sum(e.water for e in self.events)

    @property
    def money_saved(self) -> int:
        return sum(e.money for e in self.events)

    @property
    def co2_saved(self) -> float:
        return round(sum(e.co2 for e in self.events), 1)

    def level(self) -> LevelInfo:
        return level_info(self.lifetime)

    def active_days(self) -> set:
        return {e.ts.date() for e in self.events if e.pts > 0}

    def streak(self, today: dt.date) -> int:
        """Consecutive days with an earning action, ending today (or yesterday if today has none yet)."""
        days = self.active_days()
        day = today if today in days else today - dt.timedelta(days=1)
        n = 0
        while day in days:
            n += 1
            day -= dt.timedelta(days=1)
        return n

    def weekly_points(self, today: dt.date) -> list:
        """Points earned on each of the last 7 days, oldest first, ending today."""
        out = []
        for back in range(6, -1, -1):
            d = today - dt.timedelta(days=back)
            out.append(sum(e.pts for e in self.events if e.pts > 0 and e.ts.date() == d))
        return out

    def badges(self, today: dt.date) -> list:
        """(id, current, goal)"""
        return [
            ("first_scan", self.scans, 1),
            ("swap_pro", self.swaps, 5),
            ("water_saver", self.water_saved, 10000),
            ("streak7", self.streak(today), 7),
            ("thrift_hero", self.resale_swaps, 3),
            ("planet_hero", self.lifetime, 2000),
        ]

    # ------------------------------------------------------------------ actions
    def _log(self, ev: Event) -> Reward:
        before = self.level().index
        self.events.append(ev)
        after = self.level().index
        return Reward(ev.kind, ev.name, ev.emoji, ev.pts, ev.water, ev.money, ev.co2,
                      C.LEVELS[after][0] if after > before else None)

    def scan(self, p: C.Product, now: dt.datetime) -> Event:
        ev = Event("scan", p.name, "📷", C.POINTS_SCAN, now)
        self._log(ev)
        return ev

    def swap(self, orig: C.Product, alt: C.Product, now: dt.datetime, saved_only: bool = False) -> Reward:
        """Choosing an alternative. Savings are measured against the item the shopper scanned."""
        ev = Event("swap", alt.name, alt.emoji, C.POINTS_SWAP, now,
                   water=max(orig.water_l - alt.water_l, 0), money=max(orig.price - alt.price, 0),
                   co2=max(orig.co2_kg - alt.co2_kg, 0.0), resale=alt.kind == "resale")
        reward = self._log(ev)
        note = "saved" if saved_only else "booked" if alt.kind == "repair" else "swapped"
        self.closet.insert(0, ClosetItem(alt.emoji, alt.name, note, f"{alt.price}", now))
        return reward

    def skip(self, p: C.Product, now: dt.datetime) -> Reward:
        ev = Event("skip", p.name, p.emoji, C.POINTS_SKIP, now, water=p.water_l, money=p.price, co2=p.co2_kg)
        reward = self._log(ev)
        self.closet.insert(0, ClosetItem(p.emoji, p.name, "skipped", f"{p.price}", now))
        return reward

    def keep(self, p: C.Product, now: dt.datetime) -> Reward:
        ev = Event("keep", p.name, p.emoji, C.POINTS_KEEP, now)
        reward = self._log(ev)
        self.closet.insert(0, ClosetItem(p.emoji, p.name, "saved", f"{p.price}", now))
        return reward

    def log_wear(self, now: dt.datetime) -> Optional[Reward]:
        """Returns a Reward only on the wear that completes the challenge."""
        if self.wears >= C.CHALLENGE_GOAL:
            return None
        self.wears += 1
        if self.wears == C.CHALLENGE_GOAL:
            return self._log(Event("challenge", "", "🏆", C.CHALLENGE_BONUS, now))
        return None

    def redeem(self, index: int, now: dt.datetime) -> bool:
        if not 0 <= index < len(C.REWARDS):
            return False
        cost = C.REWARDS[index][2]
        if self.balance < cost or any(s.reward_index == index for s in self.spends):
            return False
        self.spends.append(Spend(index, cost, now))
        return True

    def redeemed(self, index: int) -> bool:
        return any(s.reward_index == index for s in self.spends)

    def save_outfit(self, key: str, product_ids, now: dt.datetime) -> None:
        names = " + ".join(C.BY_ID[i].name for i in product_ids)
        self.closet.insert(0, ClosetItem("👗", key, "outfit", names, now))

    def reset(self) -> None:
        self.events, self.spends, self.closet = [], [], []
        self.wears = 0
        self.sample = False

    # ------------------------------------------------------------------ sample data
    @classmethod
    def with_sample_data(cls, now: dt.datetime) -> "Game":
        """Demo history so every screen has something to show. Clearly flagged via .sample."""
        g = cls(sample=True, wears=21)

        def at(days_ago: int, hour: int) -> dt.datetime:
            return (now - dt.timedelta(days=days_ago)).replace(hour=hour, minute=0, second=0, microsecond=0)

        def add(days_ago, hour, kind, orig_id, alt_id=None):
            orig = C.BY_ID[orig_id]
            when = at(days_ago, hour)
            if kind == "scan":
                g.events.append(Event("scan", orig.name, "📷", C.POINTS_SCAN, when))
            elif kind == "swap":
                alt = C.BY_ID[alt_id]
                g.events.append(Event("swap", alt.name, alt.emoji, C.POINTS_SWAP, when,
                                      water=max(orig.water_l - alt.water_l, 0), money=max(orig.price - alt.price, 0),
                                      co2=max(orig.co2_kg - alt.co2_kg, 0.0), resale=alt.kind == "resale"))
                g.closet.append(ClosetItem(alt.emoji, alt.name, "swapped", f"{alt.price}", when))
            elif kind == "skip":
                g.events.append(Event("skip", orig.name, orig.emoji, C.POINTS_SKIP, when,
                                      water=orig.water_l, money=orig.price, co2=orig.co2_kg))
            elif kind == "keep":
                g.events.append(Event("keep", orig.name, orig.emoji, C.POINTS_KEEP, when))
                g.closet.append(ClosetItem(orig.emoji, orig.name, "saved", f"{orig.price}", when))

        add(6, 18, "scan", "shirt")
        add(6, 18, "keep", "shirt")
        add(4, 12, "scan", "jeans")
        add(4, 12, "swap", "jeans", "jeans_pre")
        add(3, 19, "scan", "dress")
        add(3, 19, "skip", "dress")
        add(2, 17, "scan", "shoe")
        add(2, 17, "skip", "shoe")
        add(1, 11, "scan", "jacket")
        add(1, 11, "swap", "jacket", "jacket_pre")
        add(0, 9, "scan", "tee")
        g.closet.sort(key=lambda c: c.ts, reverse=True)
        return g
