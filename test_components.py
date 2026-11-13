from html.parser import HTMLParser

import pytest

from sustainstyle import components as K
from sustainstyle import theme

VOID = {"br", "img", "input", "hr", "meta", "link", "circle", "line", "polygon", "path"}


class Balance(HTMLParser):
    """Fails on any unbalanced non-void tag."""

    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unexpected </{tag}> with stack {self.stack[-3:]}")
        else:
            self.stack.pop()


def assert_balanced(markup):
    p = Balance()
    p.feed(K.collapse(markup))
    assert not p.errors, p.errors
    assert not p.stack, f"unclosed: {p.stack}"


SAMPLES = {
    "tiles": lambda: K.tiles([("💧", "5,400", "litres"), ("🪙", "Rs 520", "saved"), ("☁️", "12.3 kg", "CO2")]),
    "list_row": lambda: K.list_row("📷", "Scanned a tee", "Yesterday", "+10") + K.list_row("🎟️", "Redeemed", "Now", "-100", neg=True),
    "ring": lambda: K.ring_svg(0.47),
    "hero": lambda: K.hero(top_left="<b>Hi</b>", top_right=K.pill("🔥 4", "lime"), big="340", big_label="to spend", frac=0.5, footer="Sprout"),
    "viewfinder": lambda: K.viewfinder("Everyday Tee · M · Rs 499", "8901 1122 3344", "Hold steady"),
    "traffic": lambda: "".join(K.traffic_light(t) for t in "rgy"),
    "gauge": lambda: K.gauge(38, "r", "/100", "Score 38 of 100"),
    "factor": lambda: K.factor_row("Water", "25%", 50, "y", "2,700 L"),
    "product_head": lambda: K.product_head("👕", "Everyday Tee", "FastTrend · Rs 499", K.pill("GOTS")),
    "alt": lambda: K.alt_header("👕", "Pre-loved Tee", "ThriftLoop · Rs 249", K.grade_badge(92, "A", "g")),
    "bar_chart": lambda: K.bar_chart([0, 60, 0, 110, 50, 40, 60], list("MTWTFSS"), 6),
    "week_dots": lambda: K.week_dots(list("MTWTFSS"), 3),
    "badges": lambda: K.badge_grid([("🌱", "First Scan", "Earned", True), ("🌍", "Planet", "1 / 2", False)]),
    "leaderboard": lambda: K.leaderboard([("Meera", 910, False), ("You", 340, True)]),
    "radar": lambda: K.radar_svg(["Materials", "Carbon", "Water", "Labour"], [([30, 56, 32, 40], "#E5533D", "A"), ([85, 82, 77, 90], "#2EAD62", "B")]),
    "legend": lambda: K.legend([("#E5533D", "A"), ("#2EAD62", "B")]),
    "section_card": lambda: K.section("Title", "small") + K.card("x", "tint", "margin:0"),
}


@pytest.mark.parametrize("name", sorted(SAMPLES))
def test_builders_return_balanced_markup(name):
    assert_balanced(SAMPLES[name]())


def test_esc_neutralises_html():
    assert "<" not in K.esc("<script>alert(1)</script>") and "&lt;script&gt;" in K.esc("<script>")
    assert K.esc("a'b\"c") == "a&#x27;b&quot;c"


def test_user_text_is_escaped_in_attributes():
    evil = "x' onload='alert(1)"
    assert "onload='alert" not in K.viewfinder(evil, evil, evil)
    assert "onload='alert" not in K.radar_svg([evil] * 4, [([1, 2, 3, 4], "#000", evil)])
    assert "onload='alert" not in K.gauge(5, "r", "/100", evil)


def test_collapse_removes_newlines_and_indentation():
    assert K.collapse("<div>\n    <b>x</b>\n  </div>") == "<div><b>x</b></div>"


def test_ring_and_gauge_clamp_out_of_range():
    assert "stroke-dashoffset:0.0" in K.ring_svg(5.0)
    assert K.gauge(150, "g", "/100", "x") and K.gauge(-5, "r", "/100", "x")


def test_chart_with_all_zero_does_not_divide_by_zero():
    assert_balanced(K.bar_chart([0] * 7, list("MTWTFSS"), 6))


def test_theme_converts_font_sizes_to_rem_and_supports_large_and_reduced_motion():
    assert "px" not in " ".join(part for part in theme.CSS.split(";") if "font-size" in part)
    assert "font-size:18px" in theme.build(large=True)
    assert "animation:none" in theme.build(reduce_motion=True)
    assert theme.build().startswith("<style>") and theme.build().endswith("</style>")
