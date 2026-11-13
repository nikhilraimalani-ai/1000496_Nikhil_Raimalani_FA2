"""Eco-score maths. Pure functions, no Streamlit, fully unit-tested.

score = 0.35 x materials + 0.25 x carbon + 0.25 x water + 0.15 x labour   (each factor 0 to 100)
carbon factor = 100 - 4 x kg CO2e         (25 kg or more scores 0)
water factor  = 100 - litres / 40         (4,000 L or more scores 0)
"""
from __future__ import annotations

FACTORS = ("Materials", "Carbon", "Water", "Labour")
WEIGHTS = {"Materials": 35, "Carbon": 25, "Water": 25, "Labour": 15}
CARBON_ZERO_AT_KG = 25.0
WATER_ZERO_AT_L = 4000.0
GRADE_BANDS = (("A", 85), ("B", 70), ("C", 55), ("D", 30), ("E", 0))
KG_CO2_PER_KM_DRIVING = 0.2
LITRES_DRINKING_PER_DAY = 3.0


def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))


def carbon_factor(co2_kg: float) -> float:
    """Higher is better. 0 kg scores 100, 25 kg or more scores 0."""
    return clamp(100.0 - co2_kg * (100.0 / CARBON_ZERO_AT_KG))


def water_factor(litres: float) -> float:
    """Higher is better. 0 L scores 100, 4,000 L or more scores 0."""
    return clamp(100.0 - litres * (100.0 / WATER_ZERO_AT_L))


def factor_scores(materials: float, co2_kg: float, water_l: float, labour: float) -> dict:
    """The four 0-100 factor scores, rounded for display."""
    return {
        "Materials": int(clamp(materials) + 0.5),
        "Carbon": int(carbon_factor(co2_kg) + 0.5),
        "Water": int(water_factor(water_l) + 0.5),
        "Labour": int(clamp(labour) + 0.5),
    }


def eco_score(materials: float, co2_kg: float, water_l: float, labour: float) -> int:
    """Weighted 0-100 score (half-up rounding, not banker's rounding)."""
    raw = (
        WEIGHTS["Materials"] * clamp(materials)
        + WEIGHTS["Carbon"] * carbon_factor(co2_kg)
        + WEIGHTS["Water"] * water_factor(water_l)
        + WEIGHTS["Labour"] * clamp(labour)
    ) / 100.0
    return int(raw + 0.5)


def grade_of(score: float) -> str:
    for letter, floor in GRADE_BANDS:
        if score >= floor:
            return letter
    return "E"


def tone_of(grade: str) -> str:
    """Traffic light: g (A, B), y (C), r (D, E)."""
    return "g" if grade in ("A", "B") else "y" if grade == "C" else "r"


def factor_tone(value: float) -> str:
    return "g" if value >= 70 else "y" if value >= 40 else "r"


def km_driving(co2_kg: float) -> float:
    return co2_kg / KG_CO2_PER_KM_DRIVING


def drinking_days(litres: float) -> float:
    return litres / LITRES_DRINKING_PER_DAY


def cost_per_wear(price: float, wears: int) -> float:
    if wears < 1:
        raise ValueError("wears must be at least 1")
    return price / wears


def impact_per_wear(total: float, wears: int) -> float:
    if wears < 1:
        raise ValueError("wears must be at least 1")
    return total / wears
