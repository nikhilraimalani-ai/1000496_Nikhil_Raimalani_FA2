import pytest

from sustainstyle import catalog as C
from sustainstyle import scoring as S


def test_weights_sum_to_100():
    assert sum(S.WEIGHTS.values()) == 100
    assert set(S.WEIGHTS) == set(S.FACTORS)


@pytest.mark.parametrize("co2,expected", [(0, 100), (25, 0), (30, 0), (12.5, 50), (-3, 100)])
def test_carbon_factor(co2, expected):
    assert S.carbon_factor(co2) == pytest.approx(expected)


@pytest.mark.parametrize("litres,expected", [(0, 100), (4000, 0), (9000, 0), (2000, 50)])
def test_water_factor(litres, expected):
    assert S.water_factor(litres) == pytest.approx(expected)


@pytest.mark.parametrize("score,grade", [(100, "A"), (85, "A"), (84, "B"), (70, "B"), (69, "C"), (55, "C"), (54, "D"),
                                        (30, "D"), (29, "E"), (0, "E")])
def test_grade_bands(score, grade):
    assert S.grade_of(score) == grade


def test_tones():
    assert [S.tone_of(g) for g in "ABCDE"] == ["g", "g", "y", "r", "r"]
    assert S.factor_tone(70) == "g" and S.factor_tone(69) == "y" and S.factor_tone(40) == "y" and S.factor_tone(39) == "r"


def test_score_is_half_up_and_bounded():
    assert S.eco_score(100, 0, 0, 100) == 100
    assert S.eco_score(0, 99, 99999, 0) == 0
    # inputs outside 0-100 are clamped, never producing scores outside 0-100
    assert 0 <= S.eco_score(500, -5, -5, 500) <= 100


def test_per_wear_maths():
    assert S.cost_per_wear(499, 10) == pytest.approx(49.9)
    assert S.impact_per_wear(30, 30) == pytest.approx(1)
    with pytest.raises(ValueError):
        S.cost_per_wear(100, 0)
    with pytest.raises(ValueError):
        S.impact_per_wear(100, 0)


def test_units():
    assert S.km_driving(11) == pytest.approx(55)
    assert S.drinking_days(2700) == pytest.approx(900)


# ---- catalogue integrity ----
def test_ids_and_barcodes_unique():
    assert len({p.id for p in C.CATALOG}) == len(C.CATALOG)
    assert len({p.barcode_digits for p in C.CATALOG}) == len(C.CATALOG)
    assert all(len(p.barcode_digits) == 12 for p in C.CATALOG)


def test_every_product_is_sane():
    for p in C.CATALOG:
        assert 0 <= p.score <= 100 and p.grade in "ABCDE"
        assert p.price > 0 and p.co2_kg >= 0 and p.water_l >= 0
        assert p.confidence in ("High", "Medium", "Low")
        assert p.styles and set(p.styles) <= set(C.STYLES)
        assert p.sizes
        valid = set(C.SHOE_SIZES) if p.is_shoe else set(C.APPAREL_SIZES)
        assert set(p.sizes) <= valid, p.id
        assert set(p.factors) == set(S.FACTORS)


def test_samples_exist_and_are_poor_scores_except_shirt():
    for pid in C.SAMPLE_IDS:
        assert pid in C.BY_ID
    assert [C.BY_ID[i].tone for i in C.SAMPLE_IDS] == ["r", "r", "r", "r", "r", "g"]


def test_every_poor_item_has_better_alternatives_in_every_filter_family():
    for pid in C.SAMPLE_IDS[:-1]:
        item = C.BY_ID[pid]
        alts = C.alternatives_for(item)
        assert alts, pid
        assert all(a.score > item.score and a.category == item.category for a in alts)
        assert any(a.kind == "resale" for a in alts), pid
        assert any(a.price < item.price for a in alts), pid


def test_alternatives_order_cheaper_first_then_score():
    alts = C.alternatives_for(C.BY_ID["tee"])
    cheaper = [a for a in alts if a.price < C.BY_ID["tee"].price]
    assert alts[:len(cheaper)] == cheaper
    assert [a.score for a in cheaper] == sorted((a.score for a in cheaper), reverse=True)


def test_best_item_has_no_alternatives_but_does_not_crash():
    assert C.alternatives_for(C.BY_ID["tee_rep"]) == []


def test_barcode_lookup_ignores_formatting():
    assert C.find_by_barcode("8901 1122 3344").id == "tee"
    assert C.find_by_barcode("8901-1122-3344").id == "tee"
    assert C.find_by_barcode(" 890111223344 ").id == "tee"
    assert C.find_by_barcode("123") is None
    assert C.find_by_barcode("") is None


def test_preference_matching():
    tee_pre, shoe_pre, rep = C.BY_ID["tee_pre"], C.BY_ID["shoe_pre"], C.BY_ID["tee_rep"]
    assert C.matches_preferences(tee_pre, "M", "8", "Casual", "any")
    assert not C.matches_preferences(tee_pre, "XL", "8", "Casual", "any")      # no XL in stock
    assert C.matches_preferences(tee_pre, "any", "any", "any", "any")
    assert not C.matches_preferences(tee_pre, "M", "8", "Formal", "any")       # style mismatch
    assert C.matches_preferences(tee_pre, "M", "8", "Casual", "500")           # Rs 249 fits a Rs 500 budget
    assert not C.matches_preferences(C.BY_ID["jeans_org"], "M", "8", "any", "1000")  # over budget
    assert C.matches_preferences(shoe_pre, "XS", "8", "any", "any")            # shoes ignore apparel size
    assert not C.matches_preferences(shoe_pre, "M", "6", "any", "any")         # shoe size missing
    assert C.matches_preferences(rep, "XL", "10", "Formal", "any")             # repairs always fit
