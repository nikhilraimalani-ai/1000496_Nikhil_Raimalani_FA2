"""SustainStyle: eco-score, greener swaps and GreenPoints (FA-2 prototype).

Six screens from the FA-1 storyboard plus a Closet tab, built with Streamlit.
Product names and numbers are made up.
"""
import time

import streamlit as st

st.set_page_config(page_title="SustainStyle", page_icon="🌿", layout="centered")

# ---------- data ----------
ITEM = {"name": "Everyday Tee", "price": 499, "meta": "100% cotton", "size": "M", "score": 38, "grade": "D",
        "label": "High impact", "confidence": "Medium"}
FACTORS = [
    ("Materials", 30, 35, "Conventional cotton uses a lot of pesticide and fertiliser."),
    ("Water", 50, 25, "Around 2,700 L of water to make one cotton tee."),
    ("Carbon", 28, 25, "Long shipping route and coal-powered mills."),
    ("Labour", 52, 15, "Factory is audited, but only some suppliers are known."),
]
PICKS = [
    {"id": "pre", "name": "Pre-loved Tee, Resale", "price": 249, "score": 94, "grade": "A", "tag": "Cheaper & greener",
     "emoji": "👕", "action": "Buy second-hand", "water": 2700, "co2": 6.1},
    {"id": "org", "name": "Organic Cotton Tee", "price": 549, "score": 81, "grade": "B", "tag": "",
     "emoji": "👚", "action": "Buy new", "water": 1800, "co2": 3.2},
    {"id": "rep", "name": "Repair my old tee", "price": 99, "score": 90, "grade": "A", "tag": "Keeps clothes in use",
     "emoji": "🧵", "action": "Book a repair", "water": 2700, "co2": 6.1},
]
BUDGETS = {"Under Rs 600": 600, "Under Rs 300": 300, "Any budget": 10**6}
VOUCHERS = [("Plant a tree", 100), ("10% off pre-loved", 200), ("Free Repair Voucher", 500)]
GOAL = 500
GREEN, DARK, MINT = "#1F7A45", "#17603A", "#DDF2E4"


def grade_colour(score):
    return "#2E9E5B" if score >= 70 else "#E5A823" if score >= 40 else "#D4493A"


# ---------- state ----------
DEFAULTS = dict(screen="home", pts=300, streak=3, scans=4, swaps=1, skips=1, wear=21, guest=False,
                scan_mode="Barcode", last=None, budget="Under Rs 600", size="M", style="Casual",
                redeemed=[], large=False, show_link=False,
                closet=[("Linen Shirt", "Pre-loved, Rs 320", "👔"), ("Denim Jacket", "Repaired, Rs 150", "🧥")])
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state


def go(screen):
    S.screen = screen


def toast(msg, icon="🌿"):
    st.toast(msg, icon=icon)


# ---------- style ----------
st.markdown(f"""
<style>
.block-container {{max-width: 430px; padding-top: 1.2rem; padding-bottom: 1rem;}}
#MainMenu, footer, header {{visibility: hidden;}}
.stButton {{width: 100%;}}
div[data-testid="stHorizontalBlock"] {{flex-wrap: nowrap !important; gap: .5rem;}}
div[data-testid="stColumn"] {{min-width: 0 !important; flex: 1 1 0 !important;}}
.stButton > button {{border-radius: 14px; font-weight: 700; padding: .6rem 1rem; width: 100%;}}
.stButton > button[kind="primary"] {{background: {GREEN}; border-color: {GREEN}; color: #fff;}}
.stButton > button[kind="primary"]:hover {{background: {DARK}; border-color: {DARK};}}
.brand {{font-style: italic; font-weight: 800; font-size: 1.6rem; color: {DARK};}}
.card {{background: #F1F5EC; border-radius: 16px; padding: 12px 14px; margin: 8px 0; color:#1B2B21;}}
.card.mint {{background: {MINT};}}
.pick {{border: 1px solid #D5DFCD; border-radius: 16px; padding: 10px 12px; display:flex; gap:12px; align-items:center; margin-bottom:6px; background:#fff; color:#1B2B21;}}
.pick .t {{flex:1;}} .pick b {{font-size: 1.02rem;}}
.badge {{width:48px;height:48px;border-radius:50%;border:3px solid #2E9E5B;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:800;color:#2E9E5B;line-height:1.05;}}
.deal {{background:#F6C453;color:#4A3500;font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:999px;}}
.ring {{width:130px;height:130px;border-radius:50%;display:grid;place-items:center;margin:auto;}}
.ring > div {{width:100px;height:100px;border-radius:50%;background:#fff;display:grid;place-items:center;text-align:center;font-weight:800;font-size:2rem;line-height:1;color:#1B2B21;}}
.ring small {{display:block;font-size:.75rem;font-weight:500;color:#5E6F62;}}
.grade {{font-size:3.6rem;font-weight:800;line-height:.9;}}
.plus {{background:{MINT};color:{DARK};border-radius:20px;padding:8px 26px;font-weight:800;font-size:2.6rem;text-align:center;line-height:1;margin:6px auto;width:fit-content;}}
.plus small {{display:block;font-size:1.1rem;}}
.streak {{background:#FBF0CF;border:1px solid #E5A823;border-radius:999px;padding:6px 18px;font-weight:700;text-align:center;margin:8px auto;width:fit-content;color:#4A3500;}}
.pill {{background:{MINT};color:{DARK};font-weight:700;font-size:.85rem;padding:3px 12px;border-radius:999px;}}
.center {{text-align:center;}}
{"html, body, [class*='css'] {font-size: 1.12rem;}" if S.large else ""}
</style>
""", unsafe_allow_html=True)


def nav():
    st.divider()
    cols = st.columns(4)
    items = [("Home", "home"), ("Scan", "scan"), ("Closet", "closet"), ("Rewards", "impact")]
    for c, (label, target) in zip(cols, items):
        c.button(label, key=f"nav_{target}_{S.screen}", on_click=go, args=(target,), use_container_width=True,
                 type="primary" if S.screen == target else "secondary")


def back(target):
    st.button("← Back", key=f"back_{S.screen}", on_click=go, args=(target,))


# ---------- screens ----------
def screen_home():
    c1, c2 = st.columns([3, 1])
    c1.markdown("<span class='brand'>SustainStyle</span>" + (" &nbsp;<span class='pill'>Guest</span>" if S.guest else ""),
                unsafe_allow_html=True)
    c2.button("⚙️", help="Customize", on_click=go, args=("impact",), key="gear")
    st.markdown("<h2 class='center'>Shopping today?</h2>", unsafe_allow_html=True)
    st.button("🔍  Scan a tag", type="primary", on_click=go, args=("scan",), key="bigscan", use_container_width=True)
    if st.button("🔗  Paste a product link", use_container_width=True):
        S.show_link = not S.show_link
    if S.show_link:
        link = st.text_input("Product link", placeholder="https://shop.example/everyday-tee")
        if st.button("Check this item"):
            if link.strip():
                S.scans += 1
                S.show_link = False
                go("score")
                st.rerun()
            else:
                st.warning("Paste a link first.")
    if st.button("👤  Continue as guest", use_container_width=True):
        S.guest = True
        toast("Guest mode on. No sign-up needed.")
        st.rerun()
    st.markdown("<div class='card'>🍃 &nbsp;<b>Tip:</b> Wearing a top 30 times cuts its footprint per wear</div>",
                unsafe_allow_html=True)


def screen_scan():
    back("home")
    st.markdown("<h3 class='center'>Point at barcode or care label</h3>", unsafe_allow_html=True)
    S.scan_mode = st.radio("Mode", ["Barcode", "Photo", "Type it"], horizontal=True, index=["Barcode", "Photo", "Type it"].index(S.scan_mode),
                           label_visibility="collapsed")
    if S.scan_mode == "Barcode":
        st.markdown(
            "<div style='background:#2A2D2B;border-radius:20px;padding:26px;text-align:center'>"
            "<div style='border:4px solid #4CD07A;border-radius:14px;padding:16px;display:inline-block'>"
            "<div style='background:#F6F6F2;border-radius:10px;padding:10px 16px;color:#222'>"
            "<div style='font-family:monospace;font-size:2.6rem;letter-spacing:-2px;line-height:1'>▌▌▐▌▐▐▌▌▐▌▐▌▌▐</div>"
            "<small><b>Everyday Tee - M - Rs 499</b></small></div></div></div>", unsafe_allow_html=True)
        if st.button("⚪ Capture", type="primary", use_container_width=True):
            with st.spinner("Scanning 8901 1122 3344…"):
                time.sleep(1.0)
            S.scans += 1
            go("score")
            st.rerun()
    elif S.scan_mode == "Photo":
        photo = st.camera_input("Take a photo of the care label")
        if photo is not None and st.button("Use this photo", type="primary"):
            S.scans += 1
            go("score")
            st.rerun()
    else:
        name = st.text_input("Item name", placeholder="e.g. Everyday Tee")
        if st.button("Find", type="primary"):
            if name.strip():
                S.scans += 1
                go("score")
                st.rerun()
            else:
                st.warning("Type an item name first.")
    nav()


def screen_score():
    back("scan")
    st.markdown(f"<div class='card'><b>{ITEM['name']}</b><br>Rs {ITEM['price']} - {ITEM['meta']}</div>", unsafe_allow_html=True)
    col = grade_colour(ITEM["score"])
    a, b = st.columns([1.2, 1])
    a.markdown(f"<div class='ring' style='background:conic-gradient({col} {ITEM['score']}%, #E6ECE0 0)'>"
               f"<div><span>{ITEM['score']}<small>/100</small></span></div></div>", unsafe_allow_html=True)
    b.markdown(f"<div class='grade' style='color:{col}'>{ITEM['grade']}</div><b>{ITEM['label']}</b>", unsafe_allow_html=True)
    st.markdown("#### Score breakdown")
    for name, val, _w, why in FACTORS:
        with st.expander(f"{name}: {val}/100"):
            st.progress(val / 100)
            st.caption(why)
    st.markdown(f"<div class='card center'>Data confidence: <b>{ITEM['confidence']}</b></div>", unsafe_allow_html=True)
    with st.expander("How is this calculated?"):
        st.write("The score (0 to 100) combines four factors. Higher is better.")
        st.table({"Factor": [f[0] for f in FACTORS], "Weight": [f"{f[2]}%" for f in FACTORS]})
        st.write("**Grades:** A 85 to 100 · B 70 to 84 · C 55 to 69 · D 30 to 54 · E below 30.")
        st.write("**Sources:** brand disclosures, public certification databases and industry averages. "
                 "Confidence is Medium because some supplier data is estimated.")
    st.button("See greener options", type="primary", on_click=go, args=("swaps",), key="greener")
    nav()


def finish(name, emoji, pill, pts, s1, s2):
    S.pts += pts
    S.streak += 1
    S.last = dict(name=name, emoji=emoji, pill=pill, pts=pts, s1=s1, s2=s2)
    go("done")


def choose(p, saved):
    S.swaps += 1
    S.closet.insert(0, (p["name"], f"{'Saved' if saved else p['action']}, Rs {p['price']}", p["emoji"]))
    diff = ITEM["price"] - p["price"]
    finish(p["name"], p["emoji"], "Saved to Closet", 50, (f"{p['water']:,} L", "water saved"),
           (f"Rs {diff}", "saved") if diff > 0 else (f"{p['co2']} kg", "CO₂ saved"))


def skip():
    S.skips += 1
    S.closet.insert(0, ("Everyday Tee", "Skipped, not bought", "🚫"))
    finish("Everyday Tee", "👕", "Skipped, nice self-control", 30, ("2,700 L", "water saved"), ("Rs 499", "saved"))


def screen_swaps():
    back("score")
    st.markdown("## Greener picks")
    f1, f2, f3 = st.columns(3)
    S.budget = f1.selectbox("Budget", list(BUDGETS), index=list(BUDGETS).index(S.budget))
    S.size = f2.selectbox("Size", ["S", "M", "L"], index=["S", "M", "L"].index(S.size))
    S.style = f3.selectbox("Style", ["Casual", "Formal", "Sport"], index=["Casual", "Formal", "Sport"].index(S.style))
    shown = [p for p in PICKS if p["price"] <= BUDGETS[S.budget]]
    if not shown:
        st.info("No picks under this budget. Try a higher budget.")
    for p in shown:
        deal = f"<br><span class='deal'>{p['tag']}</span>" if p["tag"] else ""
        st.markdown(f"<div class='pick'><div style='font-size:1.8rem'>{p['emoji']}</div>"
                    f"<div class='t'><b>{p['name']}</b><br>Rs {p['price']}{deal}</div>"
                    f"<div class='badge'>{p['score']}<small>{p['grade']}</small></div></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button(p["action"], key=f"act_{p['id']}", type="primary", on_click=choose, args=(p, False))
        c2.button("Save to Closet", key=f"save_{p['id']}", on_click=choose, args=(p, True))
    st.markdown("<div class='card'>🍃 &nbsp;Matched to your size, style and budget</div>", unsafe_allow_html=True)
    st.button("Pause & Skip: I won't buy it", on_click=skip, key="skip")
    nav()


def screen_done():
    d = S.last or dict(name="Pre-loved Tee, Resale", emoji="👕", pill="Saved to Closet", pts=50,
                       s1=("2,700 L", "water saved"), s2=("Rs 250", "saved"))
    st.markdown(f"<h1 class='center' style='color:{DARK};font-style:italic;font-size:2rem'>✨ Great choice! ✨</h1>"
                f"<div class='center' style='font-size:4rem'>{d['emoji']}</div>"
                f"<div class='center'><b>{d['name']}</b><br><span class='pill'>{d['pill']}</span></div>"
                f"<div class='plus'>+{d['pts']}<small>GreenPoints</small></div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("💧 " + d["s1"][1], d["s1"][0])
    m2.metric("🪙 " + d["s2"][1], d["s2"][0])
    st.markdown(f"<div class='streak'>🔥 {S.streak}-day eco streak</div>", unsafe_allow_html=True)
    st.button("Done", type="primary", on_click=go, args=("impact",), key="done_btn")
    with st.expander("Share my impact"):
        msg = f"I just chose {d['name']} on SustainStyle and saved {d['s1'][0]} {d['s1'][1]}."
        st.code(msg, language=None)


def redeem(k):
    S.pts -= VOUCHERS[k][1]
    S.redeemed.append(k)
    toast(f"Voucher redeemed: {VOUCHERS[k][0]}", "🎟️")


def log_wear():
    if S.wear < 30:
        S.wear += 1
        toast("Challenge complete!" if S.wear == 30 else "Wear logged", "🏆" if S.wear == 30 else "👕")


def screen_impact():
    st.markdown("<h1 class='center'>My Impact</h1>", unsafe_allow_html=True)
    pct = min(S.pts, GOAL) / GOAL * 100
    st.markdown(f"<div class='ring' style='width:160px;height:160px;background:conic-gradient({GREEN} {pct}%, #E6ECE0 0)'>"
                f"<div style='width:128px;height:128px'><span style='font-size:2.5rem'>{S.pts}"
                f"<small style='color:{DARK};font-weight:700'>GreenPoints</small></span></div></div>", unsafe_allow_html=True)
    left = GOAL - S.pts
    st.markdown(f"<div class='card mint center'>{f'{left} pts to Free Repair Voucher' if left > 0 else 'Free Repair Voucher unlocked!'}</div>",
                unsafe_allow_html=True)
    st.progress(pct / 100)
    st.markdown(f"<div class='card'>🍃 <b>This week:</b> {S.scans} scans, {S.swaps} swaps, {S.skips} item{'s' if S.skips != 1 else ''} skipped</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='card'>🏆 <b>Challenge:</b> Wear one item 30 times<br><small>Day {S.wear} of 30</small></div>", unsafe_allow_html=True)
    st.progress(S.wear / 30)
    st.button("Log a wear", on_click=log_wear, key="wear_btn", disabled=S.wear >= 30)
    st.markdown("#### Vouchers")
    for k, (name, cost) in enumerate(VOUCHERS):
        c1, c2 = st.columns([2, 1])
        c1.markdown(f"**{name}**<br><small>{cost} points</small>", unsafe_allow_html=True)
        done = k in S.redeemed
        label = "Redeemed" if done else "Redeem" if S.pts >= cost else f"{cost - S.pts} to go"
        c2.button(label, key=f"v{k}", disabled=done or S.pts < cost, on_click=redeem, args=(k,))
    st.markdown("#### Customize")
    st.selectbox("Language", ["English", "हिन्दी", "தமிழ்", "मराठी"], key="lang")
    S.budget = st.selectbox("Budget", list(BUDGETS), index=list(BUDGETS).index(S.budget), key="cust_budget")
    S.style = st.selectbox("Style", ["Casual", "Formal", "Sport"], index=["Casual", "Formal", "Sport"].index(S.style), key="cust_style")
    S.large = st.toggle("Accessibility: larger text", value=S.large)
    nav()


def screen_closet():
    st.markdown("<h1 class='center'>My Closet</h1>", unsafe_allow_html=True)
    st.caption("Saved and skipped items")
    for name, note, emoji in S.closet:
        st.markdown(f"<div class='pick'><div style='font-size:1.8rem'>{emoji}</div>"
                    f"<div class='t'><b>{name}</b><br><small>{note}</small></div></div>", unsafe_allow_html=True)
    nav()


{"home": screen_home, "scan": screen_scan, "score": screen_score, "swaps": screen_swaps,
 "done": screen_done, "impact": screen_impact, "closet": screen_closet}[S.screen]()
