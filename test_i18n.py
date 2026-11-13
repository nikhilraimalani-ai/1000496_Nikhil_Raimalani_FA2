import glob
import re
import string

from sustainstyle import catalog as C
from sustainstyle.i18n import TEXT, t

SRC = {f: open(f, encoding="utf-8").read() for f in glob.glob("sustainstyle/**/*.py", recursive=True) + ["app.py"]
       if not f.endswith(("strings.py", "i18n.py"))}
ALL = "\n".join(SRC.values())


def fields(s):
    return {f for _, f, _, _ in string.Formatter().parse(s) if f}


def test_both_languages_complete_and_placeholders_match():
    for key, v in TEXT.items():
        assert v["en"].strip() and v["hi"].strip(), key
        assert fields(v["en"]) == fields(v["hi"]), key


def test_static_keys_exist():
    for m in re.finditer(r"""\bt\(\s*(["'])([a-z0-9_]+)\1""", ALL):
        assert m.group(2) in TEXT or m.group(2) == "key" or m.group(2).endswith("_"), m.group(2)


def test_dynamic_key_families_exist():
    keys = []
    keys += [f"lvl_{k}" for k, _ in C.LEVELS] + [f"verdict_{g}" for g in "ABCDE"]
    keys += [f"f_{f}" for f in ("materials", "carbon", "water", "labour")]
    keys += [f"flt_{f}" for f in ("all", "cheaper", "resale", "repair", "new")]
    keys += [f"kind_{k}" for k in C.KINDS] + [f"cat_{c.lower()}" for c in C.CATEGORIES] + [f"style_{s.lower()}" for s in C.STYLES]
    keys += [f"ev_{k}" for k in ("scan", "swap", "skip", "keep", "challenge", "redeem")]
    keys += [f"rw_sub_{k}" for k in ("swap", "skip", "keep", "challenge")]
    keys += [f"cl_{k}" for k in ("swapped", "saved", "booked", "skipped", "outfit")]
    keys += [c[1] for c in C.REWARDS] + [o[0] for o in C.OUTFITS]
    keys += [f"wd_{d}" for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun")]
    keys += ["greet_morning", "greet_afternoon", "greet_evening", "conf_high", "conf_med", "conf_low"]
    keys += ["bd_first", "bd_swap", "bd_water", "bd_streak", "bd_thrift", "bd_planet"]
    for k in keys:
        assert k in TEXT, k


def test_no_unused_keys():
    dynamic = re.compile(r"^(lvl|verdict|f|flt|kind|cat|style|ev|rw_sub|cl|wd|greet|conf|bd|nav|o|r|no_match|no_filter)_")
    for key in TEXT:
        if dynamic.match(key):
            continue
        assert f'"{key}"' in ALL or f"'{key}'" in ALL, f"unused: {key}"


def test_missing_key_returns_key_and_formats():
    assert t("zzz_missing") == "zzz_missing"
    assert "5" in t("streak_n", lang="hi", n=5)
