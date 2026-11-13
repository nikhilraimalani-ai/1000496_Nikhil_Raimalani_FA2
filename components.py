"""HTML builders. Each returns a string; nothing here touches Streamlit except render().

Rule: every string that did not come from this codebase (names typed by the user) goes through esc().
Strings passed in are assumed to be already translated.
"""
from __future__ import annotations

import html as _html
import math

COL = {"g": "#2EAD62", "y": "#F2A93B", "r": "#E5533D"}


def esc(value) -> str:
    return _html.escape(str(value), quote=True)


def collapse(markup: str) -> str:
    """Strip indentation and newlines so Markdown never mistakes indented HTML for a code block."""
    return "".join(line.strip() for line in markup.splitlines())


def render(markup: str) -> None:
    import streamlit as st  # local import keeps the builders importable without Streamlit running
    st.markdown(collapse(markup), unsafe_allow_html=True)


def pill(text: str, cls: str = "") -> str:
    return f"<span class='pill {cls}'>{text}</span>"


def section(title: str, small: str = "") -> str:
    return f"<div class='sec'><span>{title}</span><small>{small}</small></div>"


def card(inner: str, cls: str = "", style: str = "") -> str:
    return f"<div class='card {cls}' style='{style}'>{inner}</div>"


def tiles(items) -> str:
    """items: (emoji, value, label)"""
    cells = "".join(f"<div class='tile'><div class='ic'>{e}</div><b>{v}</b><span>{lbl}</span></div>" for e, v, lbl in items)
    return f"<div class='tiles'>{cells}</div>"


def list_row(emoji: str, title: str, sub: str = "", right: str = "", neg: bool = False) -> str:
    sub_html = f"<small>{sub}</small>" if sub else ""
    right_html = f"<div class='p{' neg' if neg else ''}'>{right}</div>" if right else ""
    return f"<div class='li'><div class='ic'>{emoji}</div><div class='t'>{title}{sub_html}</div>{right_html}</div>"


def ring_svg(frac: float, size: int = 84, stroke: int = 9, color: str = "#C9F26B", track: str = "rgba(255,255,255,.2)") -> str:
    frac = max(0.0, min(1.0, frac))
    r = (size - stroke) / 2
    c = 2 * math.pi * r
    off = c * (1 - frac)
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}' style='transform:rotate(-90deg)' aria-hidden='true'>"
            f"<circle cx='{size / 2}' cy='{size / 2}' r='{r:.1f}' fill='none' stroke='{track}' stroke-width='{stroke}'/>"
            f"<circle cx='{size / 2}' cy='{size / 2}' r='{r:.1f}' fill='none' stroke='{color}' stroke-width='{stroke}' stroke-linecap='round' "
            f"stroke-dasharray='{c:.1f}' style='--c:{c:.1f};--t:{off:.1f};animation:arc 1.2s ease both;stroke-dashoffset:{off:.1f}'/></svg>")


def hero(*, top_left: str, top_right: str, big: str, big_label: str, frac: float, footer: str, ring_emoji: str = "🌱") -> str:
    return (f"<div class='hero'><div class='row'><div>{top_left}</div><div>{top_right}</div></div>"
            f"<div class='row' style='margin-top:16px'><div><div class='bigpts'>{big}</div><div class='hello'>{big_label}</div></div>"
            f"<div style='position:relative;width:84px;height:84px;flex:none'>{ring_svg(frac)}"
            f"<div style='position:absolute;inset:0;display:grid;place-items:center;font-size:26px'>{ring_emoji}</div></div></div>"
            f"<div class='hbar'><div style='width:{frac * 100:.0f}%'></div></div>"
            f"<div class='hello' style='position:relative;z-index:1'>{footer}</div></div>")


def viewfinder(tag_line: str, barcode: str, hint: str) -> str:
    return (f"<div class='vf' role='img' aria-label='{esc(tag_line)}'><div class='corner c1'></div><div class='corner c2'></div>"
            f"<div class='corner c3'></div><div class='corner c4'></div>"
            f"<div class='tag'><div class='bars'></div><b>{esc(tag_line)}</b><small>{esc(barcode)}</small></div>"
            f"<div class='laser'></div><div class='hint'>{esc(hint)}</div></div>")


def traffic_light(tone: str) -> str:
    lights = "".join(f"<i class='{'on ' + t if tone == t else ''}'></i>" for t in ("r", "y", "g"))
    return f"<div class='light' aria-hidden='true'>{lights}</div>"


def gauge(score: int, tone: str, out_of: str, aria: str) -> str:
    c = 2 * math.pi * 64
    off = c * (1 - max(0, min(100, score)) / 100)
    return (f"<div class='gauge' role='img' aria-label='{esc(aria)}'><svg viewBox='0 0 150 150' aria-hidden='true'>"
            f"<circle cx='75' cy='75' r='64' fill='none' stroke='#EEF2EA' stroke-width='14'/>"
            f"<circle class='arc' cx='75' cy='75' r='64' fill='none' stroke='{COL[tone]}' stroke-width='14' stroke-linecap='round' "
            f"style='--c:{c:.1f};--t:{off:.1f};stroke-dashoffset:{off:.1f}'/></svg>"
            f"<div class='num'><div>{score}<small>{out_of}</small></div></div></div>")


def factor_row(label: str, weight: str, value: int, tone: str, note: str) -> str:
    return (f"<div class='fac'><div class='h'><span>{label} <span class='muted'>· {weight}</span></span><span>{value}</span></div>"
            f"<div class='track' role='progressbar' aria-valuemin='0' aria-valuemax='100' aria-valuenow='{value}' aria-label='{esc(label)}'>"
            f"<div class='fill {tone}' style='width:{value}%'></div></div><div class='n'>{note}</div></div>")


def product_head(emoji: str, name: str, sub: str, chips: str = "") -> str:
    chip_row = f"<div style='margin-top:10px'>{chips}</div>" if chips else ""
    return (f"<div class='card' style='margin-top:6px'><div class='phead'><div class='ptile'>{emoji}</div>"
            f"<div class='t'><div class='pname'>{name}</div><span class='muted'>{sub}</span></div></div>{chip_row}</div>")


def grade_badge(score: int, grade: str, tone: str) -> str:
    return f"<div class='gb' style='color:{COL[tone]};border-color:{COL[tone]}'>{score}<small>{grade}</small></div>"


def alt_header(emoji: str, name: str, sub: str, badge: str) -> str:
    return f"<div class='alt'><div class='ptile'>{emoji}</div><div class='t'><b>{name}</b><span>{sub}</span></div>{badge}</div>"


def bar_chart(values, labels, today_index: int = -1) -> str:
    top = max(max(values), 1)
    cols = "".join(
        f"<div class='col{' today' if i == today_index else ''}'><span>{v}</span>"
        f"<div class='b' style='height:{max(v / top * 84, 4):.0f}px'></div>{lbl}</div>"
        for i, (v, lbl) in enumerate(zip(values, labels)))
    return f"<div class='chart' role='img' aria-label='{esc(', '.join(f'{lbl} {v}' for v, lbl in zip(values, labels)))}'>{cols}</div>"


def week_dots(labels, streak_days: int) -> str:
    n = len(labels)
    on = max(0, min(streak_days, n))
    dots = "".join(f"<div class='dot{' on' if i >= n - on else ''}'>{'🔥' if i >= n - on else lbl}</div>" for i, lbl in enumerate(labels))
    return f"<div class='week'>{dots}</div>"


def badge_grid(items) -> str:
    """items: (emoji, name, sub, earned)"""
    cells = "".join(f"<div class='bdg{'' if earned else ' lock'}'><span class='e'>{e}</span>{name}<small>{sub}</small></div>"
                    for e, name, sub, earned in items)
    return f"<div class='badges'>{cells}</div>"


def leaderboard(rows) -> str:
    """rows: (name, points, is_me), already sorted."""
    body = "".join(f"<div class='lb{' me' if me else ''}'><span class='rk'>{i + 1}</span>{name}<span class='pp'>{pts}</span></div>"
                   for i, (name, pts, me) in enumerate(rows))
    return f"<div class='card'>{body}</div>"


def radar_svg(labels, series, size: int = 260) -> str:
    """Four-axis radar. series: list of (values 0-100, colour, accessible name)."""
    n = len(labels)
    cx = cy = size / 2
    rad = size / 2 - 66
    angle = lambda i: -math.pi / 2 + i * 2 * math.pi / n  # noqa: E731  (axis 0 points up)
    pt = lambda i, v: (cx + rad * v / 100 * math.cos(angle(i)), cy + rad * v / 100 * math.sin(angle(i)))  # noqa: E731
    grid = ""
    for ring in (25, 50, 75, 100):
        grid += "<polygon points='" + " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, ring) for i in range(n))) + "' fill='none' stroke='#DDE6D8' stroke-width='1'/>"
    axes = "".join(f"<line x1='{cx}' y1='{cy}' x2='{pt(i, 100)[0]:.1f}' y2='{pt(i, 100)[1]:.1f}' stroke='#DDE6D8' stroke-width='1'/>" for i in range(n))
    texts = ""
    for i, lbl in enumerate(labels):
        x, y = cx + (rad + 14) * math.cos(angle(i)), cy + (rad + 14) * math.sin(angle(i))
        anchor = "middle" if abs(math.cos(angle(i))) < 0.3 else "start" if math.cos(angle(i)) > 0 else "end"
        texts += f"<text x='{x:.1f}' y='{y + 4:.1f}' text-anchor='{anchor}' font-size='12' font-weight='700' fill='#566559'>{esc(lbl)}</text>"
    shapes = ""
    for values, colour, _name in series:
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, v) for i, v in enumerate(values)))
        shapes += f"<polygon points='{poly}' fill='{colour}' fill-opacity='.22' stroke='{colour}' stroke-width='2.5' stroke-linejoin='round'/>"
        shapes += "".join(f"<circle cx='{pt(i, v)[0]:.1f}' cy='{pt(i, v)[1]:.1f}' r='3.5' fill='{colour}'/>" for i, v in enumerate(values))
    aria = "; ".join(f"{name}: " + ", ".join(f"{lbl} {v}" for lbl, v in zip(labels, values)) for values, _c, name in series)
    return (f"<svg class='radar' viewBox='0 0 {size} {size}' width='{size}' height='{size}' role='img' aria-label='{esc(aria)}'>"
            f"{grid}{axes}{shapes}{texts}</svg>")


def legend(entries) -> str:
    """entries: (colour, label)"""
    return "<div class='legend'>" + "".join(f"<span><i style='background:{c}'></i>{lbl}</span>" for c, lbl in entries) + "</div>"
