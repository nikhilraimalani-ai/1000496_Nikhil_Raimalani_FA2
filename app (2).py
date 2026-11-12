"""SustainStyle: scan a tag, see the real impact, swap to something better, earn GreenPoints.

A mobile-first Streamlit app with a scoring engine, a product catalogue, animated
eco-score gauge, greener swaps, a GreenPoints dashboard (levels, streaks, badges,
rewards, leaderboard) and a profile with outfit ideas. Product data is made up.
"""
import datetime as dt
import html as _html
import time
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SustainStyle", page_icon="🌿", layout="centered", initial_sidebar_state="collapsed")

# ════════════════════════════════════════════════════════════════════════════
# DATA + SCORING ENGINE
# ════════════════════════════════════════════════════════════════════════════
WEIGHTS = {"Materials": 35, "Carbon": 25, "Water": 25, "Labour": 15}


def _item(id, bc, name, brand, cat, kind, price, emoji, material, mat, co2, water, lab, certs=(), conf="Medium"):
    cs = max(0, 100 - co2 * 4)          # carbon: 25 kg CO2e or more scores 0
    ws = max(0, 100 - water / 40)       # water: 4,000 L or more scores 0
    score = round((WEIGHTS["Materials"] * mat + WEIGHTS["Carbon"] * cs + WEIGHTS["Water"] * ws + WEIGHTS["Labour"] * lab) / 100)
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 30 else "E"
    tone = "g" if grade in "AB" else "y" if grade == "C" else "r"
    return dict(id=id, bc=bc, name=name, brand=brand, cat=cat, kind=kind, price=price, emoji=emoji, material=material,
                co2=co2, water=water, certs=certs, conf=conf, score=score, grade=grade, tone=tone,
                fac={"Materials": mat, "Carbon": round(cs), "Water": round(ws), "Labour": lab})


CATALOG = [
    # id, barcode, name, brand, category, kind, price, emoji, material, mat, co2, water, labour, certs, confidence
    _item("tee", "8901 1122 3344", "Everyday Tee", "FastTrend", "Tops", "new", 499, "👕", "100% conventional cotton", 30, 11, 2700, 40, (), "Medium"),
    _item("tee_pre", "8901 2200 1101", "Pre-loved Tee", "ThriftLoop", "Tops", "resale", 249, "👕", "Cotton, second-hand", 85, 0.8, 40, 90, ("Pre-loved",), "High"),
    _item("tee_org", "8901 2200 1102", "Organic Cotton Tee", "Terra Basics", "Tops", "new", 549, "👚", "100% organic cotton", 85, 4.5, 900, 90, ("GOTS", "Fair Trade"), "High"),
    _item("tee_lin", "8901 2200 1103", "Linen Blend Tee", "Northfield", "Tops", "new", 649, "👕", "Linen and organic cotton", 90, 3.5, 450, 85, ("OEKO-TEX",), "High"),
    _item("tee_rep", "8901 2200 1104", "Repair my old tee", "StitchUp", "Tops", "repair", 99, "🧵", "Keep what you own", 90, 0.5, 20, 95, ("Repair",), "High"),
    _item("jeans", "8901 7766 5544", "Skinny Stretch Jeans", "UrbanLoom", "Jeans", "new", 1799, "👖", "Cotton with 12% elastane", 35, 33, 3800, 45, (), "Medium"),
    _item("jeans_pre", "8901 3300 2201", "Pre-loved Denim", "ThriftLoop", "Jeans", "resale", 799, "👖", "Denim, second-hand", 80, 2, 150, 85, ("Pre-loved",), "High"),
    _item("jeans_org", "8901 3300 2202", "Organic Rigid Denim", "Terra Basics", "Jeans", "new", 2199, "👖", "100% organic cotton denim", 85, 12, 1400, 90, ("GOTS", "Low water"), "High"),
    _item("jeans_rec", "8901 3300 2203", "Recycled Cotton Jeans", "Re:Wear", "Jeans", "new", 1899, "👖", "80% recycled cotton", 80, 9, 900, 80, ("Recycled",), "Medium"),
    _item("jacket", "8901 5566 7788", "Polyester Puffer Jacket", "FastTrend", "Jackets", "new", 2999, "🧥", "100% virgin polyester", 15, 24, 800, 20, (), "Low"),
    _item("jacket_pre", "8901 4400 3301", "Pre-loved Puffer", "ThriftLoop", "Jackets", "resale", 1299, "🧥", "Polyester, second-hand", 70, 3, 100, 80, ("Pre-loved",), "High"),
    _item("jacket_rec", "8901 4400 3302", "Recycled-fill Puffer", "Re:Wear", "Jackets", "new", 3299, "🧥", "Recycled polyester fill", 75, 10, 500, 85, ("rPET", "Bluesign"), "Medium"),
    _item("jacket_wool", "8901 4400 3303", "Wool-blend Coat", "Northfield", "Jackets", "new", 3799, "🧥", "Responsible wool blend", 80, 14, 700, 88, ("RWS wool",), "High"),
    _item("dress", "8901 9911 2233", "Floral Fast Dress", "FastTrend", "Dresses", "new", 899, "👗", "Viscose and polyester", 25, 17, 1500, 35, (), "Low"),
    _item("dress_pre", "8901 5500 4401", "Pre-loved Dress", "ThriftLoop", "Dresses", "resale", 449, "👗", "Mixed fibres, second-hand", 70, 1.5, 80, 85, ("Pre-loved",), "High"),
    _item("dress_lin", "8901 5500 4402", "Linen Midi Dress", "Northfield", "Dresses", "new", 1199, "👗", "100% European linen", 90, 5, 500, 88, ("OEKO-TEX",), "High"),
    _item("dress_ten", "8901 5500 4403", "Tencel Wrap Dress", "Re:Wear", "Dresses", "new", 1399, "👗", "100% Tencel lyocell", 88, 6, 400, 85, ("FSC",), "High"),
    _item("shoe", "8901 6677 8899", "Chunky Sneakers", "RushKicks", "Shoes", "new", 3499, "👟", "Synthetic leather and foam", 30, 14, 900, 40, (), "Medium"),
    _item("shoe_pre", "8901 6600 5501", "Pre-loved Sneakers", "ThriftLoop", "Shoes", "resale", 1499, "👟", "Mixed, second-hand", 60, 2, 120, 80, ("Pre-loved",), "High"),
    _item("shoe_rec", "8901 6600 5502", "Recycled-knit Sneakers", "Re:Wear", "Shoes", "new", 3299, "👟", "Recycled ocean-plastic knit", 75, 6, 350, 85, ("rPET",), "Medium"),
    _item("shoe_res", "8901 6600 5503", "Resole my sneakers", "StitchUp", "Shoes", "repair", 599, "🛠️", "Keep what you own", 70, 0.8, 30, 95, ("Repair",), "High"),
    _item("shirt", "8901 8800 6601", "Hemp Casual Shirt", "Terra Basics", "Shirts", "new", 1499, "👔", "100% hemp", 92, 3, 300, 92, ("GOTS", "Fair Trade"), "High"),
]
BY_ID = {p["id"]: p for p in CATALOG}
SAMPLES = ["tee", "jeans", "jacket", "dress", "shoe", "shirt"]
LEVELS = [("Seedling", 0), ("Sprout", 200), ("Sapling", 500), ("Forest Friend", 1000), ("Planet Hero", 2000)]
BUDGETS = {"Any budget": 10**9, "Under Rs 500": 500, "Under Rs 1,000": 1000, "Under Rs 2,000": 2000, "Under Rs 4,000": 4000}
REWARDS = [("🌳", "Plant a tree", 100), ("🛍️", "10% off pre-loved", 200), ("🧵", "Free repair voucher", 300), ("🚚", "Free ThriftLoop shipping", 450)]
OUTFITS = [("Weekend casual", ["tee_pre", "jeans_pre"]), ("Work ready", ["shirt", "jeans_org"]), ("Evening out", ["dress_ten", "shoe_pre"])]
FRIENDS = [("Meera", 910), ("Rohan", 620), ("Kabir", 285), ("Sana", 150)]
COL = {"g": "#2EAD62", "y": "#F2A93B", "r": "#E5533D"}
VERDICT = {"A": "Excellent choice", "B": "Good choice", "C": "Moderate impact", "D": "High impact", "E": "Very high impact"}


def now_local():
    try:
        tz = st.context.timezone
        return dt.datetime.now(ZoneInfo(tz)) if tz else dt.datetime.now(dt.timezone.utc)
    except Exception:
        return dt.datetime.now(dt.timezone.utc)


def inr(n):
    return f"Rs {n:,.0f}"


def km_of(co2):
    return f"{co2 / 0.2:,.0f} km of driving"


def water_of(litres):
    days = litres / 3
    return f"{days / 365:.1f} years of drinking water" if days >= 365 else f"{days:,.0f} days of drinking water"


def factor_note(p, name, v):
    if name == "Materials":
        return (f"Low-impact fibre: {p['material']}" if v >= 70 else f"Mixed impact: {p['material']}" if v >= 40
                else f"High-impact fibre: {p['material']}")
    if name == "Carbon":
        return f"{p['co2']:g} kg CO₂e to make and ship"
    if name == "Water":
        return f"{p['water']:,} L of water used"
    return ("Fair-labour certified or traceable" if v >= 70 else "Partly audited supply chain" if v >= 40
            else "Little supplier transparency")


def level_info(pts):
    idx = max(i for i, (_, at) in enumerate(LEVELS) if pts >= at)
    name = LEVELS[idx][0]
    if idx == len(LEVELS) - 1:
        return name, idx, None, None, 1.0
    nxt, at_next = LEVELS[idx + 1]
    base = LEVELS[idx][1]
    return name, idx, nxt, at_next, (pts - base) / (at_next - base)


# ════════════════════════════════════════════════════════════════════════════
# STATE
# ════════════════════════════════════════════════════════════════════════════
DEFAULTS = dict(
    view="home", name="Eco Explorer", pts=340, life=340, wear=21, streak=4, streak_bumped=False, scans=7, swaps=2, skips=1, resale=1,
    water_saved=5400, money_saved=520, co2_saved=12.3, week=[20, 60, 0, 110, 50, 40, 60],
    sel="tee", cur="tee", last=None, celebrate=False, redeemed=[], large=False, notif=True,
    history=[("🔄", "Swapped to Pre-loved Denim", "Yesterday", 50), ("📷", "Scanned Floral Fast Dress", "Yesterday", 10),
             ("⏸️", "Skipped Chunky Sneakers", "2 days ago", 30), ("🔥", "3-day streak bonus", "3 days ago", 20)],
    closet=[("👖", "Pre-loved Denim", "Swapped, Rs 799"), ("👔", "Linen Shirt", "Saved, Rs 899")],
    filt="All", barcode_err="", sample=True, guest=False, budget="Any budget",
)
for _k, _v in DEFAULTS.items():
    st.session_state.setdefault(_k, _v)
S = st.session_state


def go(view):
    S.view = view


def H(html):
    st.markdown("".join(line.strip() for line in html.splitlines()), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# STYLE
# ════════════════════════════════════════════════════════════════════════════
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
:root{--ink:#10281C;--muted:#5B6B60;--g900:#0B3322;--g800:#0F3D2A;--g700:#1F7A45;--g500:#34A363;--lime:#C9F26B;--mint:#E3F4E6;
--display:'Sora','Segoe UI',system-ui,-apple-system,sans-serif;--body:'Plus Jakarta Sans','Segoe UI',system-ui,-apple-system,sans-serif;--sand:#F7F4EC;--line:#E4EAE0;--red:#E5533D;--amber:#F2A93B;--green:#2EAD62;--shadow:0 10px 30px rgba(15,61,42,.09);}
html,body,[class*="css"],.stApp{font-family:var(--body);color:var(--ink);}
.stApp{background:radial-gradient(1000px 500px at 50% -120px,#CFEBD3 0%,rgba(207,235,211,0) 70%),linear-gradient(180deg,#EDF7EE 0%,#F7F4EC 45%,#F7F4EC 100%);}
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
.block-container{max-width:430px;padding:1rem 1rem 7.5rem;}
h1,h2,h3,h4{font-family:var(--display);color:var(--ink);letter-spacing:-.02em;}
.sora{font-family:var(--display);}
/* buttons */
.stButton>button{border-radius:16px;font-weight:700;font-family:var(--body);min-height:3rem;border:1.5px solid var(--line);background:#fff;color:var(--ink);box-shadow:0 2px 8px rgba(15,61,42,.05);transition:transform .12s,box-shadow .12s;}
.stButton>button:hover{border-color:var(--g500);color:var(--g700);transform:translateY(-1px);}
.stButton>button:active{transform:scale(.98);}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#1F7A45,#2E9A5A);border:0;color:#fff;box-shadow:0 8px 20px rgba(31,122,69,.32);}
.stButton>button[kind="primary"]:hover{color:#fff;box-shadow:0 10px 26px rgba(31,122,69,.42);}
.stButton>button:disabled{opacity:.45;}
/* inputs */
.stTextInput input{border-radius:14px;border:1.5px solid var(--line);padding:.7rem .9rem;background:#fff;}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:18px;background:#fff;box-shadow:0 2px 8px rgba(15,61,42,.04);}
[data-testid="stExpander"] summary{font-weight:700;}
[data-testid="stPills"] button{border-radius:999px;font-weight:600;}
[data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:.6rem;align-items:center;}
[data-testid="stColumn"]{min-width:0!important;}
body:after{content:"";position:fixed;left:0;right:0;bottom:0;height:96px;background:linear-gradient(180deg,rgba(247,244,236,0),#F7F4EC 70%);pointer-events:none;z-index:900;}
.stElementContainer:has(iframe[height="0"]){display:none;}
/* bottom nav */
.st-key-bottomnav{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);width:min(402px,calc(100vw - 20px));z-index:1000;background:rgba(255,255,255,.98);backdrop-filter:blur(14px);border-radius:28px;padding:8px;box-shadow:0 14px 44px rgba(15,61,42,.25);border:1px solid rgba(15,61,42,.07);}
.st-key-bottomnav [data-testid="stHorizontalBlock"]{gap:4px;flex-wrap:nowrap;}
.st-key-bottomnav [data-testid="stColumn"]{min-width:0!important;}
.st-key-bottomnav .stButton>button{flex-direction:column;min-height:56px;padding:4px 2px;border:0;box-shadow:none;background:transparent;color:var(--muted);border-radius:20px;font-size:11px;gap:0;}
.st-key-bottomnav .stButton>button *{font-size:11px;}
.st-key-bottomnav .stButton>button [data-testid="stIconMaterial"]{font-size:24px!important;margin-bottom:2px;}
.st-key-bottomnav .stButton>button:hover{background:var(--mint);transform:none;}
.st-key-bottomnav .stButton>button[kind="primary"]{background:var(--mint);color:var(--g800);box-shadow:none;}
.st-key-bottomnav .stButton>button[kind="primary"] *{color:var(--g800);}
/* back button */
.st-key-backrow .stButton>button{min-height:2.4rem;width:auto;padding:0 .9rem;border-radius:999px;font-size:13px;}
/* cards */
.card{background:#fff;border-radius:24px;padding:16px;box-shadow:var(--shadow);margin:10px 0;border:1px solid rgba(15,61,42,.04);animation:rise .5s ease both;}
.card.flat{box-shadow:none;border:1px solid var(--line);}
.tint{background:var(--mint);}
.sec{font-family:var(--display);font-weight:700;font-size:17px;margin:22px 2px 8px;display:flex;justify-content:space-between;align-items:baseline;}
.sec small{font-family:var(--body);font-weight:600;color:var(--muted);font-size:12px;}
.eyebrow{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;}
.muted{color:var(--muted);font-size:13px;}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes grow{from{width:0}}
@keyframes arc{from{stroke-dashoffset:var(--c)}to{stroke-dashoffset:var(--t)}}
@keyframes sweep{0%{top:8%}100%{top:88%}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(201,242,107,.5)}50%{box-shadow:0 0 0 12px rgba(201,242,107,0)}}
@keyframes pop{0%{transform:scale(.6);opacity:0}70%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
/* hero */
.hero{background:linear-gradient(145deg,#0B3322 0%,#14663B 55%,#2E9A5A 100%);border-radius:30px;padding:20px;color:#fff;position:relative;overflow:hidden;box-shadow:0 18px 40px rgba(15,61,42,.35);animation:rise .5s ease both;}
.hero:before{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(201,242,107,.35),rgba(201,242,107,0) 70%);}
.hero .row{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1;}
.hello{font-size:13px;opacity:.8;} .hname{font-family:var(--display);font-weight:700;font-size:22px;}
.chip{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;font-weight:700;font-size:12.5px;background:rgba(255,255,255,.16);backdrop-filter:blur(6px);}
.chip.lime{background:var(--lime);color:var(--g900);}
.bigpts{font-family:var(--display);font-weight:800;font-size:54px;line-height:1;letter-spacing:-.03em;}
.hbar{height:10px;background:rgba(255,255,255,.2);border-radius:999px;overflow:hidden;margin:14px 0 6px;position:relative;z-index:1;}
.hbar>div{height:100%;background:var(--lime);border-radius:999px;animation:grow 1s ease both;}
/* stat tiles */
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.tile{background:#fff;border-radius:20px;padding:12px 10px;text-align:center;box-shadow:var(--shadow);animation:rise .5s ease both;}
.tile .ic{font-size:20px} .tile b{display:block;font-family:var(--display);font-size:17px;margin-top:2px;} .tile span{font-size:11px;color:var(--muted);font-weight:600;}
/* list rows */
.li{display:flex;gap:12px;align-items:center;padding:11px 0;border-bottom:1px solid var(--line);}
.li:last-child{border-bottom:0}
.li .ic{width:42px;height:42px;border-radius:14px;background:var(--mint);display:grid;place-items:center;font-size:20px;flex:none;}
.li .t{flex:1;min-width:0;font-weight:600;font-size:14px;line-height:1.25;} .li .t small{display:block;color:var(--muted);font-weight:500;font-size:12px;}
.li .p{font-family:var(--display);font-weight:700;font-size:14px;color:var(--g700);}
.li .p.neg{color:var(--red)}
/* scan */
.vf{position:relative;height:260px;border-radius:28px;background:radial-gradient(circle at 50% 40%,#2E3A33,#111815 75%);overflow:hidden;display:grid;place-items:center;box-shadow:0 18px 40px rgba(0,0,0,.28);}
.vf .corner{position:absolute;width:44px;height:44px;border:4px solid var(--lime);}
.vf .c1{left:34px;top:34px;border-right:0;border-bottom:0;border-radius:14px 0 0 0}.vf .c2{right:34px;top:34px;border-left:0;border-bottom:0;border-radius:0 14px 0 0}
.vf .c3{left:34px;bottom:34px;border-right:0;border-top:0;border-radius:0 0 0 14px}.vf .c4{right:34px;bottom:34px;border-left:0;border-top:0;border-radius:0 0 14px 0}
.vf .tag{background:#F8F8F3;border-radius:14px 14px 20px 20px;padding:16px 16px 10px;width:190px;text-align:center;color:#1b1b1b;animation:pulse 2s infinite;position:relative;}
.vf .tag:before{content:"";position:absolute;top:6px;left:50%;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#2a2f2c;}
.vf .bars{height:58px;margin:10px 4px 6px;background:repeating-linear-gradient(90deg,#111 0 2px,transparent 2px 4px,#111 4px 5px,transparent 5px 8px,#111 8px 11px,transparent 11px 13px);border-radius:2px;}
.vf .tag b{font-size:12px;display:block;} .vf .tag small{font-size:10.5px;color:#555;}
.vf .laser{position:absolute;left:44px;right:44px;height:3px;background:linear-gradient(90deg,transparent,#FF6B5B,transparent);box-shadow:0 0 18px #FF6B5B;animation:sweep 1.6s ease-in-out infinite alternate;}
.vf .hint{position:absolute;bottom:12px;left:0;right:0;text-align:center;color:#E8F0E6;font-size:12.5px;font-weight:600;opacity:.9;}
/* score */
.ptile{width:62px;height:62px;border-radius:20px;display:grid;place-items:center;font-size:32px;flex:none;background:linear-gradient(145deg,#E3F4E6,#fff);border:1px solid var(--line);}
.pname{font-family:var(--display);font-weight:700;font-size:18px;line-height:1.15;}
.gaugewrap{display:flex;align-items:center;gap:18px;}
.gauge{position:relative;width:150px;height:150px;flex:none;}
.gauge svg{transform:rotate(-90deg);width:150px;height:150px;}
.gauge .arc{stroke-dasharray:var(--c);animation:arc 1.2s cubic-bezier(.2,.8,.2,1) both;}
.gauge .num{position:absolute;inset:0;display:grid;place-items:center;text-align:center;font-family:var(--display);font-weight:800;font-size:44px;line-height:1;}
.gauge .num small{display:block;font-family:var(--body);font-size:12px;color:var(--muted);font-weight:600;margin-top:2px;}
.grade{font-family:var(--display);font-weight:800;font-size:68px;line-height:.9;animation:pop .6s .3s ease both;}
.light{display:inline-flex;gap:6px;background:#1c2420;padding:6px 9px;border-radius:999px;margin-top:8px;}
.light i{width:13px;height:13px;border-radius:50%;background:#3a443f;display:block;}
.light i.on.r{background:var(--red);box-shadow:0 0 10px var(--red)}.light i.on.y{background:var(--amber);box-shadow:0 0 10px var(--amber)}.light i.on.g{background:var(--green);box-shadow:0 0 10px var(--green)}
.fac{margin:14px 0;}
.fac .h{display:flex;justify-content:space-between;font-weight:700;font-size:14px;margin-bottom:6px;}
.track{height:12px;border-radius:999px;background:#EEF2EA;overflow:hidden;}
.fill{height:100%;border-radius:999px;animation:grow 1s ease both;}
.fill.g{background:linear-gradient(90deg,#2EAD62,#58C985)}.fill.y{background:linear-gradient(90deg,#F2A93B,#F7C46A)}.fill.r{background:linear-gradient(90deg,#E5533D,#F0806D)}
.fac .n{font-size:12px;color:var(--muted);margin-top:5px;}
.unit{display:flex;gap:12px;align-items:center;}
.unit .u{flex:1;background:var(--sand);border-radius:18px;padding:12px;font-size:12.5px;line-height:1.3;}
.unit .u b{display:block;font-family:var(--display);font-size:14px;margin:2px 0;}
.pill{display:inline-block;padding:4px 10px;border-radius:999px;font-size:11.5px;font-weight:700;background:var(--mint);color:var(--g800);margin:2px 4px 2px 0;}
.pill.amber{background:#FDF0D5;color:#8A5A00;}.pill.red{background:#FBE0DA;color:#9A2D1B;}.pill.lime{background:var(--lime);color:var(--g900);}
.wtab{width:100%;border-collapse:collapse;font-size:13px;} .wtab td{padding:6px 2px;border-bottom:1px solid var(--line);} .wtab td:last-child{text-align:right;font-weight:700;}
/* alternatives */
[class*="st-key-alt_"]{background:#fff;border-radius:26px;padding:14px;box-shadow:var(--shadow);margin-bottom:14px;border:1px solid rgba(15,61,42,.04);animation:rise .5s ease both;}
.alt{display:flex;gap:12px;align-items:center;margin-bottom:10px;}
.alt .t{flex:1;min-width:0;} .alt .t b{font-family:var(--display);font-size:15.5px;line-height:1.2;display:block;} .alt .t span{font-size:12.5px;color:var(--muted);}
.gb{width:54px;height:54px;border-radius:50%;display:grid;place-items:center;text-align:center;font-family:var(--display);font-weight:800;line-height:1;border:4px solid;flex:none;font-size:16px;}
.gb small{display:block;font-size:11px;margin-top:1px;}
.save{font-weight:800;color:var(--g700);} .more{font-weight:800;color:var(--amber);}
/* reward */
.celebrate{text-align:center;padding:10px 0 0;}
.celebrate h1{font-size:30px;margin:6px 0;}
.plus{display:inline-block;background:linear-gradient(135deg,var(--lime),#9BE36A);color:var(--g900);font-family:var(--display);font-weight:800;font-size:56px;line-height:1;padding:14px 32px;border-radius:30px;animation:pop .6s ease both;box-shadow:0 14px 34px rgba(124,200,60,.4);}
.plus small{display:block;font-size:15px;font-weight:700;}
/* badges */
.badges{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.bdg{background:#fff;border-radius:20px;padding:12px 6px;text-align:center;box-shadow:var(--shadow);font-size:11.5px;font-weight:700;}
.bdg .e{font-size:28px;display:block;margin-bottom:4px;} .bdg small{display:block;color:var(--muted);font-weight:600;font-size:10.5px;margin-top:2px;}
.bdg.lock{opacity:.55;} .bdg.lock .e{filter:grayscale(1);}
.chart{display:flex;gap:8px;align-items:flex-end;height:120px;padding-top:6px;}
.chart .col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:6px;font-size:10.5px;color:var(--muted);font-weight:600;}
.chart .b{width:100%;border-radius:10px 10px 4px 4px;background:linear-gradient(180deg,#58C985,#1F7A45);animation:grow 1s ease both;min-height:4px;}
.chart .col.today .b{background:linear-gradient(180deg,#D9F77F,#8ED84F);}
.week{display:flex;justify-content:space-between;margin-top:10px;}
.dot{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700;background:#EEF2EA;color:var(--muted);}
.dot.on{background:linear-gradient(135deg,#FFB54D,#FF7A3D);color:#fff;}
.lb{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-weight:600;font-size:14px;} .lb:last-child{border:0}
.lb .rk{width:26px;height:26px;border-radius:50%;background:var(--sand);display:grid;place-items:center;font-size:12px;font-weight:800;}
.lb.me{background:var(--mint);margin:0 -8px;padding:9px 8px;border-radius:14px;border:0;} .lb .pp{margin-left:auto;font-family:var(--display);font-weight:700;}
/* profile */
.avatar{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#34A363,#C9F26B);display:grid;place-items:center;font-family:var(--display);font-weight:800;font-size:30px;color:var(--g900);flex:none;}
.share{background:linear-gradient(145deg,#0B3322,#1F7A45);color:#fff;border-radius:26px;padding:20px;position:relative;overflow:hidden;box-shadow:0 16px 36px rgba(15,61,42,.3);}
.share .sc{font-family:var(--display);font-weight:800;font-size:48px;line-height:1;} .share .sc small{font-size:18px;opacity:.7;}
.outfit .em{font-size:30px;letter-spacing:6px;}
"""
st.markdown(f"<style>{CSS}{'.block-container{zoom:1.1}' if S.large else ''}</style>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ACTIONS
# ════════════════════════════════════════════════════════════════════════════
def add_history(emoji, title, sub, pts):
    S.history.insert(0, (emoji, title, sub, pts))
    S.week[-1] += max(pts, 0)


def register_scan(item_id):
    S.cur = item_id
    S.scans += 1
    S.pts += 10
    S.life += 10
    add_history("📷", f"Scanned {BY_ID[item_id]['name']}", "Just now", 10)
    st.toast("+10 GreenPoints for scanning", icon="🌿")


def finish(title, emoji, pill, pts, water, money, co2, closet_note=None, resale=False):
    before = level_info(S.life)[1]
    S.pts += pts
    S.life += pts
    if not S.streak_bumped:
        S.streak += 1
        S.streak_bumped = True
    S.water_saved += water
    S.money_saved += max(money, 0)
    S.co2_saved = round(S.co2_saved + co2, 1)
    if resale:
        S.resale += 1
    if closet_note:
        S.closet.insert(0, (emoji, title, closet_note))
    add_history(emoji, pill, "Just now", pts)
    after = level_info(S.life)[1]
    S.last = dict(title=title, emoji=emoji, pill=pill, pts=pts, water=water, money=money, co2=co2,
                  levelup=LEVELS[after][0] if after > before else None)
    S.celebrate = True
    go("reward")


def choose(alt):
    orig = BY_ID[S.cur]
    S.swaps += 1
    finish(alt["name"], alt["emoji"], f"Swapped to {alt['name']}", 50, max(orig["water"] - alt["water"], 0),
           orig["price"] - alt["price"], max(orig["co2"] - alt["co2"], 0), f"Swapped, {inr(alt['price'])}",
           resale=alt["kind"] == "resale")


def skip():
    p = BY_ID[S.cur]
    S.skips += 1
    finish(p["name"], p["emoji"], f"Skipped {p['name']}", 30, p["water"], p["price"], p["co2"])


def keep_green():
    p = BY_ID[S.cur]
    finish(p["name"], p["emoji"], f"Chose {p['name']}", 20, 0, 0, 0, f"Saved, {inr(p['price'])}")


def redeem(i):
    e, n, c = REWARDS[i]
    if S.pts >= c and i not in S.redeemed:
        S.pts -= c
        S.redeemed.append(i)
        S.history.insert(0, (e, f"Redeemed: {n}", "Just now", -c))
        st.toast(f"Redeemed: {n}", icon="🎟️")


def start_fresh():
    for k in ("pts", "life", "streak", "scans", "swaps", "skips", "resale", "wear", "water_saved", "money_saved", "co2_saved"):
        S[k] = 0
    S.week, S.history, S.closet, S.redeemed = [0] * 7, [], [], []
    S.streak_bumped = False
    S.sample = False
    st.toast("Cleared sample data. You're starting fresh.", icon="🌱")


def log_wear():
    if S.wear >= 30:
        return
    S.wear += 1
    if S.wear == 30:
        S.pts += 100
        S.life += 100
        add_history("🏆", "Challenge complete: wore one item 30 times", "Just now", 100)
        st.toast("Challenge complete! +100 GreenPoints", icon="🏆")
    else:
        st.toast(f"Wear logged: day {S.wear} of 30", icon="👕")


def go_guest():
    S.guest = True
    st.toast("Guest mode on. No sign-up needed.", icon="👤")


def save_outfit(name, ids):
    S.closet.insert(0, ("👗", f"Outfit: {name}", " + ".join(BY_ID[i]["name"] for i in ids)))
    st.toast("Outfit saved to your closet", icon="👗")


# ════════════════════════════════════════════════════════════════════════════
# COMPONENTS
# ════════════════════════════════════════════════════════════════════════════
def back(target, label="Back"):
    with st.container(key="backrow"):
        st.button(label, icon=":material/arrow_back:", key=f"back_{S.view}", on_click=go, args=(target,))


def nav():
    active = {"home": "home", "scan": "scan", "result": "scan", "alts": "scan", "reward": "scan", "impact": "impact", "profile": "profile"}[S.view]
    tabs = [("home", "Home", ":material/home:"), ("scan", "Scan", ":material/qr_code_scanner:"),
            ("impact", "Impact", ":material/eco:"), ("profile", "Profile", ":material/person:")]
    with st.container(key="bottomnav"):
        cols = st.columns(4)
        for col, (key, label, icon) in zip(cols, tabs):
            col.button(label, icon=icon, key=f"nav_{key}", on_click=go, args=(key,), width="stretch",
                       type="primary" if active == key else "secondary")


def ring_svg(frac, size=84, stroke=9, color="#C9F26B", track="rgba(255,255,255,.2)"):
    r = (size - stroke) / 2
    c = 2 * 3.14159 * r
    return (f"<svg width='{size}' height='{size}' style='transform:rotate(-90deg)'><circle cx='{size/2}' cy='{size/2}' r='{r}' fill='none' stroke='{track}' stroke-width='{stroke}'/>"
            f"<circle cx='{size/2}' cy='{size/2}' r='{r}' fill='none' stroke='{color}' stroke-width='{stroke}' stroke-linecap='round' "
            f"stroke-dasharray='{c:.1f}' style='--c:{c:.1f};--t:{c*(1-frac):.1f};animation:arc 1.2s ease both;stroke-dashoffset:{c*(1-frac):.1f}'/></svg>")


def history_rows(n):
    if not S.history:
        H("<div class='card'><b>No activity yet.</b><div class='muted'>Scan your first tag to earn points.</div></div>")
        return
    rows = "".join(
        f"<div class='li'><div class='ic'>{e}</div><div class='t'>{t}<small>{s}</small></div>"
        f"<div class='p{' neg' if p < 0 else ''}'>{'+' if p > 0 else ''}{p}</div></div>" for e, t, s, p in S.history[:n])
    H(f"<div class='card'>{rows}</div>")


# ════════════════════════════════════════════════════════════════════════════
# PAGES
# ════════════════════════════════════════════════════════════════════════════
def page_home():
    lvl, _, nxt, at_next, frac = level_info(S.life)
    hour = now_local().hour
    greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    left = f"{at_next - S.life} lifetime pts to {nxt}" if nxt else "Top level reached"
    H(f"""<div class='hero'><div class='row'><div><div class='hello'>{greet}</div><div class='hname'>{'Guest' if S.guest else _html.escape(S.name)} 🌿</div></div>
    <span class='chip lime'>🔥 {S.streak}-day streak</span></div>
    <div class='row' style='margin-top:18px'><div><div class='bigpts'>{S.pts}</div><div class='hello'>GreenPoints to spend</div></div>
    <div style='position:relative;width:84px;height:84px'>{ring_svg(frac)}<div style='position:absolute;inset:0;display:grid;place-items:center;font-size:26px'>🌱</div></div></div>
    <div class='hbar'><div style='width:{frac*100:.0f}%'></div></div><div class='hello' style='position:relative;z-index:1'>🏅 {lvl} · {left}</div></div>""")
    if S.sample:
        H("<div class='muted' style='text-align:center;margin:8px 0 0'>Sample data shown. Reset in Profile → Settings.</div>")
    st.write("")
    st.button("Scan a tag", icon=":material/qr_code_scanner:", type="primary", width="stretch", key="home_scan", on_click=go, args=("scan",))
    st.button("Guest mode on · no sign-up needed" if S.guest else "Continue as guest", icon=":material/person:", width="stretch",
              key="guest_btn", on_click=go_guest, disabled=S.guest)
    H(f"""<div class='sec'>Your impact <small>so far</small></div><div class='tiles'>
    <div class='tile'><div class='ic'>💧</div><b>{S.water_saved:,}</b><span>litres saved</span></div>
    <div class='tile'><div class='ic'>🪙</div><b>{inr(S.money_saved)}</b><span>money saved</span></div>
    <div class='tile'><div class='ic'>☁️</div><b>{S.co2_saved:g} kg</b><span>CO₂ avoided</span></div></div>""")
    H("""<div class='card tint' style='display:flex;gap:14px;align-items:center'><div style='font-size:34px'>💡</div>
    <div><b>Did you know?</b><div class='muted' style='color:#2d4a39'>Wearing a top 30 times instead of 10 cuts its production footprint per wear to a third.</div></div></div>""")
    H("<div class='sec'>Recent activity <small>latest</small></div>")
    history_rows(3)
    H("<div class='sec'>Try a swap <small>popular</small></div>")
    cards = "".join(
        f"<div style='background:#fff;border-radius:22px;padding:14px;box-shadow:var(--shadow)'><div style='font-size:30px'>{BY_ID[i]['emoji']}</div>"
        f"<div style='font-weight:700;font-size:13.5px;margin:6px 0 2px'>{BY_ID[i]['name']}</div><div class='muted'>{inr(BY_ID[i]['price'])}</div>"
        f"<span class='pill lime'>{BY_ID[i]['grade']} · {BY_ID[i]['score']}</span></div>" for i in ("tee_pre", "jeans_pre", "dress_lin", "tee_rep"))
    H(f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px'>{cards}</div>")


def page_scan():
    back("home")
    H("<h2 style='margin:.6rem 0 .2rem'>Scan a tag</h2><div class='muted'>Point at the barcode or care label.</div>")
    p = BY_ID[S.sel]
    H(f"""<div class='vf'><div class='corner c1'></div><div class='corner c2'></div><div class='corner c3'></div><div class='corner c4'></div>
    <div class='tag'><div class='bars'></div><b>{p['name']} · M · {inr(p['price'])}</b><small>{p['bc']}</small></div><div class='laser'></div>
    <div class='hint'>Hold steady. Auto-detecting…</div></div>""")
    st.write("")
    H("<div class='eyebrow' style='margin:6px 2px'>Pick a sample item to scan</div>")
    pick = st.pills("Sample item", SAMPLES, default=S.sel, format_func=lambda i: f"{BY_ID[i]['emoji']} {BY_ID[i]['name']}",
                    label_visibility="collapsed", key="pill_sel")
    if pick and pick != S.sel:
        S.sel = pick
        st.rerun()
    if st.button("Scan now", icon=":material/center_focus_strong:", type="primary", width="stretch", key="scan_now"):
        bar = st.progress(0, text="Reading barcode…")
        for i in range(1, 11):
            time.sleep(0.07)
            bar.progress(i * 10, text="Matching with product database…" if i > 5 else "Reading barcode…")
        register_scan(S.sel)
        go("result")
        st.rerun()
    with st.expander("Type a barcode instead"):
        code = st.text_input("Barcode", placeholder="e.g. 8901 1122 3344", label_visibility="collapsed", key="bc_in")
        if st.button("Find item", key="bc_go", width="stretch"):
            digits = "".join(ch for ch in code if ch.isdigit())
            hit = next((x for x in CATALOG if x["bc"].replace(" ", "") == digits), None)
            if hit:
                register_scan(hit["id"])
                go("result")
                st.rerun()
            st.error("No item with that barcode. Try one from the sample list.")
    with st.expander("Use the camera or upload a photo"):
        use_cam = st.toggle("Turn on camera", key="cam_tg")
        photo = st.camera_input("Photograph the care label", label_visibility="collapsed") if use_cam else None
        if photo is not None:
            st.success("Label read. Matching to the selected sample item.")
            if st.button("Analyse photo", key="photo_go", width="stretch"):
                register_scan(S.sel)
                go("result")
                st.rerun()


def page_result():
    p = BY_ID[S.cur]
    back("scan", "Scan another")
    certs = "".join(f"<span class='pill'>{c}</span>" for c in p["certs"]) or "<span class='pill amber'>No certifications</span>"
    H(f"""<div class='card' style='margin-top:6px'><div class='alt' style='margin:0'><div class='ptile'>{p['emoji']}</div>
    <div class='t'><div class='pname'>{p['name']}</div><span class='muted'>{p['brand']} · {inr(p['price'])}<br>{p['material']}</span></div></div><div style='margin-top:10px'>{certs}</div></div>""")
    col = COL[p["tone"]]
    c = 2 * 3.14159 * 64
    lights = "".join(f"<i class='{'on ' + t if p['tone'] == t else ''}'></i>" for t in ("r", "y", "g"))
    H(f"""<div class='card'><div class='gaugewrap'><div class='gauge'><svg viewBox='0 0 150 150'><circle cx='75' cy='75' r='64' fill='none' stroke='#EEF2EA' stroke-width='14'/>
    <circle class='arc' cx='75' cy='75' r='64' fill='none' stroke='{col}' stroke-width='14' stroke-linecap='round' style='--c:{c:.1f};--t:{c*(1-p['score']/100):.1f};stroke-dashoffset:{c*(1-p['score']/100):.1f}'/></svg>
    <div class='num'><div>{p['score']}<small>out of 100</small></div></div></div>
    <div><div class='grade' style='color:{col}'>{p['grade']}</div><div style='font-weight:700;margin-top:4px'>{VERDICT[p['grade']]}</div><div class='light'>{lights}</div></div></div></div>""")
    H(f"""<div class='card'><div class='eyebrow'>This item in everyday terms</div><div class='unit' style='margin-top:10px'>
    <div class='u'>☁️ Carbon<b>{km_of(p['co2'])}</b>{p['co2']:g} kg CO₂e</div><div class='u'>💧 Water<b>{water_of(p['water'])}</b>{p['water']:,} litres</div></div></div>""")
    rows = ""
    for name, v in p["fac"].items():
        t = "g" if v >= 70 else "y" if v >= 40 else "r"
        rows += (f"<div class='fac'><div class='h'><span>{name} <span class='muted'>· {WEIGHTS[name]}%</span></span><span>{v}</span></div>"
                 f"<div class='track'><div class='fill {t}' style='width:{v}%'></div></div><div class='n'>{factor_note(p, name, v)}</div></div>")
    conf_cls = {"High": "", "Medium": "amber", "Low": "red"}[p["conf"]]
    H(f"<div class='card'><div style='display:flex;justify-content:space-between;align-items:center'><b class='sora'>Score breakdown</b><span class='pill {conf_cls}'>Data confidence: {p['conf']}</span></div>{rows}</div>")
    with st.expander("How is this calculated?"):
        H("<table class='wtab'>" + "".join(f"<tr><td>{k}</td><td>{v}%</td></tr>" for k, v in WEIGHTS.items()) + "</table>")
        st.caption("Score = weighted average of the four factors, 0 to 100. Carbon: 25 kg CO₂e or more scores 0. "
                   "Water: 4,000 L or more scores 0. Grades: A 85+, B 70+, C 55+, D 30+, E below 30. "
                   "Demo app: product figures are illustrative. A live version would use brand disclosures and certification databases.")
    has_alts = any(x["cat"] == p["cat"] and x["score"] > p["score"] and x["id"] != p["id"] for x in CATALOG)
    if p["tone"] != "g" and has_alts:
        st.button("See greener alternatives", icon=":material/eco:", type="primary", width="stretch", key="to_alts", on_click=go, args=("alts",))
        st.button("Pause & skip: I won't buy it", icon=":material/pause_circle:", width="stretch", key="skip_btn", on_click=skip)
    else:
        H("<div class='card tint'><b>Already a great pick.</b><div class='muted' style='color:#2d4a39'>This item scores well. Keep it and earn points.</div></div>")
        st.button("Keep it · +20 points", icon=":material/check_circle:", type="primary", width="stretch", key="keep_btn", on_click=keep_green)
        if has_alts:
            st.button("Compare alternatives", width="stretch", key="to_alts2", on_click=go, args=("alts",))


def page_alts():
    p = BY_ID[S.cur]
    back("result", "Back to result")
    H(f"<h2 style='margin:.6rem 0 .2rem'>Better {p['cat'].lower()}</h2><div class='muted'>Instead of {p['name']} ({inr(p['price'])}, grade {p['grade']})</div>")
    S.filt = st.pills("Filter", ["All", "In budget", "Cheaper", "Pre-loved", "Repair", "New"], default=S.filt, label_visibility="collapsed", key="pill_f") or "All"
    alts = [x for x in CATALOG if x["cat"] == p["cat"] and x["id"] != p["id"] and x["score"] > p["score"]]
    f = S.filt
    alts = [x for x in alts if f == "All" or (f == "In budget" and x["price"] <= BUDGETS[S.budget]) or (f == "Cheaper" and x["price"] < p["price"]) or (f == "Pre-loved" and x["kind"] == "resale")
            or (f == "Repair" and x["kind"] == "repair") or (f == "New" and x["kind"] == "new")]
    alts.sort(key=lambda x: (-(x["price"] < p["price"]), -x["score"]))
    if not alts:
        H("<div class='card'><b>No matches for this filter.</b><div class='muted'>Try another filter.</div></div>")
    for x in alts:
        diff = p["price"] - x["price"]
        money = f"<span class='save'>Save {inr(diff)}</span>" if diff > 0 else f"<span class='more'>{inr(-diff)} more</span>"
        tags = "".join(f"<span class='pill'>{c}</span>" for c in x["certs"])
        tags += "<span class='pill lime'>Cheaper &amp; greener</span>" if diff > 0 else ""
        with st.container(key=f"alt_{x['id']}"):
            H(f"""<div class='alt'><div class='ptile'>{x['emoji']}</div><div class='t'><b>{x['name']}</b><span>{x['brand']} · {inr(x['price'])} · {money}</span></div>
            <div class='gb' style='color:{COL[x['tone']]};border-color:{COL[x['tone']]}'>{x['score']}<small>{x['grade']}</small></div></div>
            <div>{tags}</div><div class='muted' style='margin:8px 0 10px'>Saves {max(p['water'] - x['water'], 0):,} L of water and {max(p['co2'] - x['co2'], 0):.1f} kg CO₂e vs {p['name']}</div>""")
            st.button(f"{'Book it' if x['kind'] == 'repair' else 'Choose this'} · +50 pts", key=f"choose_{x['id']}", type="primary", width="stretch", on_click=choose, args=(x,))
    H("<div class='card tint'>🍃 <b>Matched to your style and budget.</b></div>")
    st.button("Pause & skip: I won't buy it", icon=":material/pause_circle:", width="stretch", key="skip_alts", on_click=skip)


def page_reward():
    d = S.last or dict(title="Pre-loved Tee", emoji="👕", pill="Swapped", pts=50, water=2660, money=250, co2=10.2, levelup=None)
    if S.celebrate:
        st.balloons()
        S.celebrate = False
    lvl, _, nxt, at_next, frac = level_info(S.life)
    up = f"<div style='margin-top:10px'><span class='pill lime'>🎉 Level up: {d['levelup']}</span></div>" if d["levelup"] else ""
    money = f"{inr(d['money'])}" if d["money"] > 0 else "–"
    H(f"""<div class='celebrate'><div style='font-size:56px'>{d['emoji']}</div><h1>Great choice!</h1><div class='muted'>{d['pill']}</div>{up}
    <div style='margin:18px 0 6px'><div class='plus'>+{d['pts']}<small>GreenPoints</small></div></div></div>""")
    H(f"""<div class='tiles' style='margin-top:14px'><div class='tile'><div class='ic'>💧</div><b>{d['water']:,} L</b><span>water saved</span></div>
    <div class='tile'><div class='ic'>🪙</div><b>{money}</b><span>saved</span></div><div class='tile'><div class='ic'>☁️</div><b>{d['co2']:.1f} kg</b><span>CO₂ avoided</span></div></div>""")
    left = f"{at_next - S.life} lifetime pts to {nxt}" if nxt else "Top level reached"
    H(f"""<div class='card'><div style='display:flex;justify-content:space-between;font-weight:700'><span>{lvl}</span><span>{S.life} lifetime pts</span></div>
    <div class='track' style='margin:10px 0 6px'><div class='fill g' style='width:{frac*100:.0f}%'></div></div><div class='muted'>{left}</div>
    <div style='margin-top:12px'><span class='pill' style='background:#FFE9D2;color:#8A3B00'>🔥 {S.streak}-day eco streak</span></div></div>""")
    st.button("View my impact", icon=":material/eco:", type="primary", width="stretch", key="r_impact", on_click=go, args=("impact",))
    st.button("Scan another item", icon=":material/qr_code_scanner:", width="stretch", key="r_scan", on_click=go, args=("scan",))
    with st.expander("Share my impact"):
        st.code(f"I just chose {d['title']} on SustainStyle and earned {d['pts']} GreenPoints! 🌿", language=None)


def badge_defs():
    return [("🌱", "First Scan", S.scans, 1), ("🔄", "Swap Pro", S.swaps, 5), ("💧", "Water Saver", S.water_saved, 10000),
            ("🔥", "7-day Streak", S.streak, 7), ("🛍️", "Thrift Hero", S.resale, 3), ("🌍", "Planet Hero", S.life, 2000)]


def page_impact():
    lvl, _, nxt, at_next, frac = level_info(S.life)
    left = f"{at_next - S.life} lifetime pts to {nxt}" if nxt else "Top level reached"
    H("<h2 style='margin:.4rem 0 .6rem'>My Impact</h2>")
    H(f"""<div class='hero'><div class='row'><div><div class='hello'>GreenPoints to spend</div><div class='bigpts'>{S.pts}</div></div>
    <div style='position:relative;width:96px;height:96px'>{ring_svg(frac, 96, 10)}<div style='position:absolute;inset:0;display:grid;place-items:center;font-size:30px'>🌱</div></div></div>
    <div class='hbar'><div style='width:{frac*100:.0f}%'></div></div>
    <div class='row'><span class='chip'>🏅 {lvl}</span><span class='hello'>{left}</span></div></div>""")
    days = [(now_local().date() - dt.timedelta(days=6 - i)) for i in range(7)]
    mx = max(max(S.week), 1)
    cols = "".join(f"<div class='col{' today' if i == 6 else ''}'><span>{v}</span><div class='b' style='height:{max(v/mx*84, 4):.0f}px'></div>{d.strftime('%a')[:2]}</div>" for i, (v, d) in enumerate(zip(S.week, days)))
    dots = "".join(f"<div class='dot{' on' if i >= 7 - min(S.streak, 7) else ''}'>{'🔥' if i >= 7 - min(S.streak, 7) else d.strftime('%a')[0]}</div>" for i, d in enumerate(days))
    H(f"<div class='card'><div class='eyebrow'>Points this week</div><div class='chart'>{cols}</div></div>")
    H(f"<div class='card'><div style='display:flex;justify-content:space-between'><b class='sora'>🔥 {S.streak}-day streak</b><span class='muted'>Keep it going</span></div><div class='week'>{dots}</div></div>")
    done_ch = S.wear >= 30
    H(f"""<div class='card'><div style='display:flex;justify-content:space-between'><b class='sora'>🏆 Challenge</b><span class='muted'>Day {S.wear} of 30</span></div>
    <div class='muted' style='margin:4px 0 10px'>Wear one item 30 times. Reward: +100 GreenPoints.</div>
    <div class='track'><div class='fill g' style='width:{S.wear / 30 * 100:.0f}%'></div></div></div>""")
    st.button("Challenge complete 🎉" if done_ch else "Log a wear", icon=":material/add_circle:", key="wear_btn", on_click=log_wear, disabled=done_ch, width="stretch")
    H(f"""<div class='tiles' style='margin-top:12px'><div class='tile'><div class='ic'>📷</div><b>{S.scans}</b><span>scans</span></div><div class='tile'><div class='ic'>🔄</div><b>{S.swaps}</b><span>swaps</span></div>
    <div class='tile'><div class='ic'>⏸️</div><b>{S.skips}</b><span>skipped</span></div></div>""")
    done = sum(1 for _, _, v, g in badge_defs() if v >= g)
    H(f"<div class='sec'>Badges <small>{done} of {len(badge_defs())} earned</small></div>")
    b = "".join(f"<div class='bdg{'' if v >= g else ' lock'}'><span class='e'>{e}</span>{n}<small>{'Earned' if v >= g else f'{min(v, g):,} / {g:,}'}</small></div>" for e, n, v, g in badge_defs())
    H(f"<div class='badges'>{b}</div>")
    H("<div class='sec'>Rewards <small>spend your points</small></div>")
    for i, (e, n, c) in enumerate(REWARDS):
        got = i in S.redeemed
        c1, c2 = st.columns([2.2, 1])
        c1.markdown(f"<div class='li' style='border:0;padding:4px 0'><div class='ic'>{e}</div><div class='t'>{n}<small>{c} points</small></div></div>", unsafe_allow_html=True)
        c2.button("Redeemed" if got else "Redeem" if S.pts >= c else f"{c - S.pts} to go", key=f"rd_{i}", disabled=got or S.pts < c,
                  on_click=redeem, args=(i,), width="stretch", type="primary" if (S.pts >= c and not got) else "secondary")
    H("<div class='sec'>Community <small>sample friends</small></div>")
    board = sorted(FRIENDS + [("You", S.life)], key=lambda x: -x[1])
    rows = "".join(f"<div class='lb{' me' if n == 'You' else ''}'><span class='rk'>{i+1}</span>{n}<span class='pp'>{p}</span></div>" for i, (n, p) in enumerate(board))
    H(f"<div class='card'>{rows}</div>")
    H("<div class='sec'>Recent actions <small>history</small></div>")
    history_rows(6)


def eco_score():
    return min(99, 52 + S.swaps * 6 + S.skips * 3 + min(S.streak, 10) * 2 + S.resale * 2)


def page_profile():
    lvl = level_info(S.life)[0]
    H(f"""<div class='card' style='display:flex;gap:16px;align-items:center'><div class='avatar'>{_html.escape(S.name[:1].upper())}</div>
    <div><div class='sora' style='font-weight:700;font-size:20px'>{_html.escape(S.name)}</div><span class='pill lime'>🏅 {lvl}</span><div class='muted'>{S.scans} scans · {S.swaps} swaps</div></div></div>""")
    H(f"""<div class='share'><div class='eyebrow' style='color:#C9F26B'>My Eco Impact Score</div><div class='sc'>{eco_score()}<small> / 100</small></div>
    <div style='opacity:.85;margin:6px 0 12px'>Based on your swaps, skips, thrift buys and streak.</div>
    <span class='chip'>💧 {S.water_saved:,} L</span> <span class='chip'>☁️ {S.co2_saved:g} kg</span> <span class='chip'>🪙 {inr(S.money_saved)}</span></div>""")
    with st.expander("Share my Eco Impact Score"):
        st.code(f"My Eco Impact Score on SustainStyle is {eco_score()}/100. I've saved {S.water_saved:,} L of water! 🌿", language=None)
    H("<div class='sec'>Style swap <small>outfit ideas</small></div>")
    for n, ids in OUTFITS:
        items = [BY_ID[i] for i in ids]
        total = sum(i["price"] for i in items)
        avg = round(sum(i["score"] for i in items) / len(items))
        H(f"""<div class='card outfit' style='margin-bottom:6px'><div class='em'>{''.join(i['emoji'] for i in items)}</div><b class='sora'>{n}</b>
        <div class='muted'>{' + '.join(i['name'] for i in items)}</div><div style='margin-top:6px'><span class='pill lime'>Avg score {avg}</span><span class='pill'>{inr(total)}</span></div></div>""")
        st.button("Save outfit", key=f"of_{n}", on_click=save_outfit, args=(n, ids), width="stretch")
    H("<div class='sec'>My closet <small>saved items</small></div>")
    rows = "".join(f"<div class='li'><div class='ic'>{e}</div><div class='t'>{n}<small>{s}</small></div></div>" for e, n, s in S.closet[:8])
    H(f"<div class='card'>{rows}</div>" if rows else "<div class='card'><b>Your closet is empty.</b><div class='muted'>Swapped and saved items appear here.</div></div>")
    with st.expander("Settings"):
        new_name = st.text_input("Your name", value=S.name, key="name_in", max_chars=24).strip() or "Eco Explorer"
        if new_name != S.name:
            S.name = new_name
            st.rerun()
        S.budget = st.selectbox("My budget (used by the In budget filter)", list(BUDGETS), index=list(BUDGETS).index(S.budget), key="budget_sel")
        S.large = st.toggle("Larger text", value=S.large, key="large_tg")
        S.notif = st.toggle("Weekly impact summary", value=S.notif, key="notif_tg")
        st.button("Clear sample data and start fresh", key="fresh", on_click=start_fresh, width="stretch", disabled=not S.sample)


PAGES = dict(home=page_home, scan=page_scan, result=page_result, alts=page_alts, reward=page_reward, impact=page_impact, profile=page_profile)
PAGES[S.view]()
nav()
if S.get("_shown") != S.view:
    S._shown = S.view
    components.html(f"<script>/*{S.view}-{time.time()}*/const m=window.parent.document.querySelector('[data-testid=\"stMain\"]');if(m){{m.scrollTo({{top:0}});}}</script>", height=0)
