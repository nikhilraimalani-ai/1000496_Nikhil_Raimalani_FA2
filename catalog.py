"""Product catalogue (illustrative demo data) and static reference tables."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import scoring

APPAREL_SIZES = ("XS", "S", "M", "L", "XL")
SHOE_SIZES = ("6", "7", "8", "9", "10")
STYLES = ("Casual", "Formal", "Sport")
KINDS = ("new", "resale", "repair")
CATEGORIES = ("Tops", "Jeans", "Jackets", "Dresses", "Shoes", "Shirts")


@dataclass
class Product:
    id: str
    barcode: str
    name: str
    brand: str
    category: str
    kind: str                 # new | resale | repair
    price: int                # rupees
    emoji: str
    material: str
    materials_score: int
    co2_kg: float
    water_l: int
    labour_score: int
    certs: tuple = ()
    confidence: str = "Medium"   # High | Medium | Low
    styles: tuple = ("Casual",)
    sizes: tuple = APPAREL_SIZES
    # derived
    factors: dict = field(init=False)
    score: int = field(init=False)
    grade: str = field(init=False)
    tone: str = field(init=False)

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"{self.id}: bad kind {self.kind}")
        if self.category not in CATEGORIES:
            raise ValueError(f"{self.id}: bad category {self.category}")
        self.factors = scoring.factor_scores(self.materials_score, self.co2_kg, self.water_l, self.labour_score)
        self.score = scoring.eco_score(self.materials_score, self.co2_kg, self.water_l, self.labour_score)
        self.grade = scoring.grade_of(self.score)
        self.tone = scoring.tone_of(self.grade)

    @property
    def is_shoe(self) -> bool:
        return self.category == "Shoes"

    @property
    def barcode_digits(self) -> str:
        return "".join(ch for ch in self.barcode if ch.isdigit())


def _p(id, bc, name, brand, cat, kind, price, emoji, material, mat, co2, water, lab, certs=(), conf="Medium",
       styles=("Casual",), sizes=APPAREL_SIZES):
    return Product(id, bc, name, brand, cat, kind, price, emoji, material, mat, co2, water, lab, tuple(certs), conf,
                   tuple(styles), tuple(sizes))


_S, _M, _L, _XL, _XS = "S", "M", "L", "XL", "XS"

CATALOG = [
    # id, barcode, name, brand, category, kind, price, emoji, material, materials, kg CO2e, litres, labour, certs, confidence, styles, sizes
    _p("tee", "8901 1122 3344", "Everyday Tee", "FastTrend", "Tops", "new", 499, "👕", "100% conventional cotton", 30, 11, 2700, 40, (), "Medium", ("Casual", "Sport")),
    _p("tee_pre", "8901 2200 1101", "Pre-loved Tee", "ThriftLoop", "Tops", "resale", 249, "👕", "Cotton, second-hand", 85, 0.8, 40, 90, ("Pre-loved",), "High", ("Casual", "Sport"), (_S, _M, _L)),
    _p("tee_org", "8901 2200 1102", "Organic Cotton Tee", "Terra Basics", "Tops", "new", 549, "👚", "100% organic cotton", 85, 4.5, 900, 90, ("GOTS", "Fair Trade"), "High", ("Casual", "Sport")),
    _p("tee_lin", "8901 2200 1103", "Linen Blend Tee", "Northfield", "Tops", "new", 649, "👕", "Linen and organic cotton", 90, 3.5, 450, 85, ("OEKO-TEX",), "High", ("Casual", "Formal"), (_S, _M, _L, _XL)),
    _p("tee_rep", "8901 2200 1104", "Repair my old tee", "StitchUp", "Tops", "repair", 99, "🧵", "Keep what you own", 90, 0.5, 20, 95, ("Repair",), "High", STYLES),
    _p("jeans", "8901 7766 5544", "Skinny Stretch Jeans", "UrbanLoom", "Jeans", "new", 1799, "👖", "Cotton with 12% elastane", 35, 33, 3800, 45, (), "Medium", ("Casual", "Formal"), (_S, _M, _L, _XL)),
    _p("jeans_pre", "8901 3300 2201", "Pre-loved Denim", "ThriftLoop", "Jeans", "resale", 799, "👖", "Denim, second-hand", 80, 2, 150, 85, ("Pre-loved",), "High", ("Casual", "Formal"), (_M, _L)),
    _p("jeans_org", "8901 3300 2202", "Organic Rigid Denim", "Terra Basics", "Jeans", "new", 2199, "👖", "100% organic cotton denim", 85, 12, 1400, 90, ("GOTS", "Low water"), "High", ("Casual", "Formal"), (_S, _M, _L, _XL)),
    _p("jeans_rec", "8901 3300 2203", "Recycled Cotton Jeans", "Re:Wear", "Jeans", "new", 1899, "👖", "80% recycled cotton", 80, 9, 900, 80, ("Recycled",), "Medium", ("Casual",), (_XS, _S, _M, _L)),
    _p("jacket", "8901 5566 7788", "Polyester Puffer Jacket", "FastTrend", "Jackets", "new", 2999, "🧥", "100% virgin polyester", 15, 24, 800, 20, (), "Low", ("Casual", "Sport"), (_S, _M, _L, _XL)),
    _p("jacket_pre", "8901 4400 3301", "Pre-loved Puffer", "ThriftLoop", "Jackets", "resale", 1299, "🧥", "Polyester, second-hand", 70, 3, 100, 80, ("Pre-loved",), "High", ("Casual", "Sport"), (_M, _L, _XL)),
    _p("jacket_rec", "8901 4400 3302", "Recycled-fill Puffer", "Re:Wear", "Jackets", "new", 3299, "🧥", "Recycled polyester fill", 75, 10, 500, 85, ("rPET", "Bluesign"), "Medium", ("Casual", "Sport"), (_S, _M, _L)),
    _p("jacket_wool", "8901 4400 3303", "Wool-blend Coat", "Northfield", "Jackets", "new", 3799, "🧥", "Responsible wool blend", 80, 14, 700, 88, ("RWS wool",), "High", ("Formal", "Casual"), (_S, _M, _L, _XL)),
    _p("dress", "8901 9911 2233", "Floral Fast Dress", "FastTrend", "Dresses", "new", 899, "👗", "Viscose and polyester", 25, 17, 1500, 35, (), "Low", ("Casual", "Formal"), (_XS, _S, _M, _L)),
    _p("dress_pre", "8901 5500 4401", "Pre-loved Dress", "ThriftLoop", "Dresses", "resale", 449, "👗", "Mixed fibres, second-hand", 70, 1.5, 80, 85, ("Pre-loved",), "High", ("Casual", "Formal"), (_S, _M)),
    _p("dress_lin", "8901 5500 4402", "Linen Midi Dress", "Northfield", "Dresses", "new", 1199, "👗", "100% European linen", 90, 5, 500, 88, ("OEKO-TEX",), "High", ("Casual", "Formal")),
    _p("dress_ten", "8901 5500 4403", "Tencel Wrap Dress", "Re:Wear", "Dresses", "new", 1399, "👗", "100% Tencel lyocell", 88, 6, 400, 85, ("FSC",), "High", ("Formal", "Casual"), (_S, _M, _L)),
    _p("shoe", "8901 6677 8899", "Chunky Sneakers", "RushKicks", "Shoes", "new", 3499, "👟", "Synthetic leather and foam", 30, 14, 900, 40, (), "Medium", ("Casual", "Sport"), SHOE_SIZES),
    _p("shoe_pre", "8901 6600 5501", "Pre-loved Sneakers", "ThriftLoop", "Shoes", "resale", 1499, "👟", "Mixed, second-hand", 60, 2, 120, 80, ("Pre-loved",), "High", ("Casual", "Sport"), ("7", "8", "9")),
    _p("shoe_rec", "8901 6600 5502", "Recycled-knit Sneakers", "Re:Wear", "Shoes", "new", 3299, "👟", "Recycled ocean-plastic knit", 75, 6, 350, 85, ("rPET",), "Medium", ("Casual", "Sport"), SHOE_SIZES),
    _p("shoe_res", "8901 6600 5503", "Resole my sneakers", "StitchUp", "Shoes", "repair", 599, "🛠️", "Keep what you own", 70, 0.8, 30, 95, ("Repair",), "High", STYLES, SHOE_SIZES),
    _p("shirt", "8901 8800 6601", "Hemp Casual Shirt", "Terra Basics", "Shirts", "new", 1499, "👔", "100% hemp", 92, 3, 300, 92, ("GOTS", "Fair Trade"), "High", ("Formal", "Casual"), (_S, _M, _L, _XL)),
]
BY_ID = {p.id: p for p in CATALOG}
BY_BARCODE = {p.barcode_digits: p for p in CATALOG}
SAMPLE_IDS = ("tee", "jeans", "jacket", "dress", "shoe", "shirt")

LEVELS = (("seedling", 0), ("sprout", 200), ("sapling", 500), ("forest_friend", 1000), ("planet_hero", 2000))
REWARDS = (("🌳", "r_tree", 100), ("🛍️", "r_preloved", 200), ("🧵", "r_repair", 300), ("🚚", "r_ship", 450))
OUTFITS = (("o_weekend", ("tee_pre", "jeans_pre")), ("o_work", ("shirt", "jeans_org")), ("o_evening", ("dress_ten", "shoe_pre")))
FRIENDS = (("Meera", 910), ("Rohan", 620), ("Kabir", 285), ("Sana", 150))
BUDGETS = (("any", 10 ** 9), ("500", 500), ("1000", 1000), ("2000", 2000), ("4000", 4000))
BUDGET_CAP = dict(BUDGETS)
CHALLENGE_GOAL = 30
CHALLENGE_BONUS = 100

POINTS_SCAN = 10
POINTS_SWAP = 50
POINTS_SKIP = 30
POINTS_KEEP = 20


def find_by_barcode(text: str):
    """Look a product up from whatever the user typed (spaces and dashes ignored)."""
    digits = "".join(ch for ch in text if ch.isdigit())
    return BY_BARCODE.get(digits)


def alternatives_for(item: Product) -> list:
    """Same category, strictly higher score, best first (cheaper options ahead of dearer ones)."""
    alts = [p for p in CATALOG if p.category == item.category and p.id != item.id and p.score > item.score]
    alts.sort(key=lambda p: (p.price >= item.price, -p.score, p.price))
    return alts


def matches_preferences(p: Product, size: str, shoe_size: str, style: str, budget_key: str) -> bool:
    """True when the product suits the shopper's size, style and budget. 'any' means no restriction."""
    if p.price > BUDGET_CAP.get(budget_key, 10 ** 9):
        return False
    if style != "any" and style not in p.styles:
        return False
    if p.kind == "repair":
        return True  # a service, not a sized item
    if p.is_shoe:
        return shoe_size == "any" or shoe_size in p.sizes
    return size == "any" or size in p.sizes
