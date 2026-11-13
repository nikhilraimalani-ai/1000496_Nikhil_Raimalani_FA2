"""All CSS lives here. Font sizes are written in px for readability and converted to rem at import time,
so the 'Larger text' setting (which changes the root font size) scales the whole app, including Streamlit's own widgets."""
from __future__ import annotations

import re

_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
:root{--ink:#10281C;--muted:#566559;--g900:#0B3322;--g800:#0F3D2A;--g700:#1F7A45;--g500:#34A363;--lime:#C9F26B;--mint:#E3F4E6;
--sand:#F7F4EC;--line:#E4EAE0;--red:#E5533D;--amber:#F2A93B;--green:#2EAD62;--shadow:0 10px 30px rgba(15,61,42,.09);
--display:'Sora','Noto Sans Devanagari','Segoe UI',system-ui,-apple-system,sans-serif;
--body:'Plus Jakarta Sans','Noto Sans Devanagari','Segoe UI',system-ui,-apple-system,sans-serif;}
html,body,[class*="css"],.stApp{font-family:var(--body);color:var(--ink);}
.stApp{background:radial-gradient(1000px 500px at 50% -120px,#CFEBD3 0%,rgba(207,235,211,0) 70%),linear-gradient(180deg,#EDF7EE 0%,#F7F4EC 45%,#F7F4EC 100%);}
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
.block-container{max-width:430px;padding:1rem 1rem 8rem;}
h1,h2,h3,h4{font-family:var(--display);color:var(--ink);letter-spacing:-.02em;}
h2{font-size:24px;margin:.5rem 0 .2rem;padding:0;} h1{font-size:30px;padding:0;}
.sora{font-family:var(--display);}
:focus-visible{outline:3px solid #1F7A45;outline-offset:2px;border-radius:8px;}
[hidden]{display:none!important;}
/* buttons */
.stButton>button,.stDownloadButton>button{border-radius:16px;font-weight:700;font-family:var(--body);min-height:3rem;border:1.5px solid var(--line);background:#fff;color:var(--ink);box-shadow:0 2px 8px rgba(15,61,42,.05);transition:transform .12s,box-shadow .12s;}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--g500);color:var(--g700);transform:translateY(-1px);}
.stButton>button:active{transform:scale(.98);}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#1F7A45,#2E9A5A);border:0;color:#fff;box-shadow:0 8px 20px rgba(31,122,69,.32);}
.stButton>button[kind="primary"]:hover{color:#fff;box-shadow:0 10px 26px rgba(31,122,69,.42);}
.stButton>button:disabled{opacity:.5;}
.stTextInput input,.stSelectbox [data-baseweb="select"]>div{border-radius:14px;}
.stTextInput input{border:1.5px solid var(--line);padding:.7rem .9rem;background:#fff;}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:18px;background:#fff;box-shadow:0 2px 8px rgba(15,61,42,.04);margin-bottom:.4rem;}
[data-testid="stExpander"] summary{font-weight:700;}
[data-testid="stPills"] button{border-radius:999px;font-weight:600;}
[data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:.6rem;align-items:center;}
[data-testid="stColumn"]{min-width:0!important;}
.stElementContainer:has(iframe[height="0"]){display:none;}
body:after{content:"";position:fixed;left:0;right:0;bottom:0;height:96px;background:linear-gradient(180deg,rgba(247,244,236,0),#F7F4EC 70%);pointer-events:none;z-index:900;}
/* bottom nav */
.st-key-bottomnav{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);width:min(402px,calc(100vw - 20px));z-index:1000;background:rgba(255,255,255,.98);backdrop-filter:blur(14px);border-radius:28px;padding:8px;box-shadow:0 14px 44px rgba(15,61,42,.25);border:1px solid rgba(15,61,42,.07);}
.st-key-bottomnav [data-testid="stHorizontalBlock"]{gap:4px;}
.st-key-bottomnav .stButton>button{flex-direction:column;min-height:56px;padding:4px 2px;border:0;box-shadow:none;background:transparent;color:var(--muted);border-radius:20px;font-size:11px;gap:0;}
.st-key-bottomnav .stButton>button *{font-size:11px;}
.st-key-bottomnav .stButton>button [data-testid="stIconMaterial"]{font-size:24px!important;margin-bottom:2px;}
.st-key-bottomnav .stButton>button:hover{background:var(--mint);transform:none;}
.st-key-bottomnav .stButton>button[kind="primary"]{background:var(--mint);color:var(--g800);box-shadow:none;}
.st-key-bottomnav .stButton>button[kind="primary"] *{color:var(--g800);}
.st-key-backrow .stButton>button{min-height:2.4rem;width:auto;padding:0 .9rem;border-radius:999px;font-size:13px;}
/* motion */
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes grow{from{width:0}}
@keyframes arc{from{stroke-dashoffset:var(--c)}to{stroke-dashoffset:var(--t)}}
@keyframes sweep{0%{top:8%}100%{top:88%}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(201,242,107,.5)}50%{box-shadow:0 0 0 12px rgba(201,242,107,0)}}
@keyframes pop{0%{transform:scale(.6);opacity:0}70%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;}}
/* cards and text */
.card{background:#fff;border-radius:24px;padding:16px;box-shadow:var(--shadow);margin:10px 0;border:1px solid rgba(15,61,42,.04);animation:rise .5s ease both;}
.card.tint{background:var(--mint);box-shadow:none;}
.sec{font-family:var(--display);font-weight:700;font-size:17px;margin:22px 2px 8px;display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
.sec small{font-family:var(--body);font-weight:600;color:var(--muted);font-size:12px;}
.eyebrow{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;}
.muted{color:var(--muted);font-size:13px;line-height:1.4;}
.center{text-align:center;}
.pill{display:inline-block;padding:4px 10px;border-radius:999px;font-size:11.5px;font-weight:700;background:var(--mint);color:var(--g800);margin:2px 4px 2px 0;}
.pill.amber{background:#FDF0D5;color:#7A4E00;} .pill.red{background:#FBE0DA;color:#8F2A19;} .pill.lime{background:var(--lime);color:var(--g900);} .pill.warm{background:#FFE9D2;color:#7A3300;}
/* hero */
.hero{background:linear-gradient(145deg,#0B3322 0%,#14663B 55%,#2E9A5A 100%);border-radius:30px;padding:20px;color:#fff;position:relative;overflow:hidden;box-shadow:0 18px 40px rgba(15,61,42,.35);animation:rise .5s ease both;}
.hero:before{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(201,242,107,.35),rgba(201,242,107,0) 70%);}
.hero .row{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1;gap:10px;}
.hello{font-size:13px;opacity:.85;} .hname{font-family:var(--display);font-weight:700;font-size:22px;word-break:break-word;}
.chip{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;font-weight:700;font-size:12.5px;background:rgba(255,255,255,.16);}
.chip.lime{background:var(--lime);color:var(--g900);}
.bigpts{font-family:var(--display);font-weight:800;font-size:54px;line-height:1;letter-spacing:-.03em;}
.hbar{height:10px;background:rgba(255,255,255,.2);border-radius:999px;overflow:hidden;margin:14px 0 6px;position:relative;z-index:1;}
.hbar>div{height:100%;background:var(--lime);border-radius:999px;animation:grow 1s ease both;}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.tile{background:#fff;border-radius:20px;padding:12px 8px;text-align:center;box-shadow:var(--shadow);animation:rise .5s ease both;min-width:0;}
.tile .ic{font-size:20px;} .tile b{display:block;font-family:var(--display);font-size:16px;margin-top:2px;overflow-wrap:anywhere;} .tile span{font-size:11px;color:var(--muted);font-weight:600;}
.li{display:flex;gap:12px;align-items:center;padding:11px 0;border-bottom:1px solid var(--line);}
.li:last-child{border-bottom:0}
.li .ic{width:42px;height:42px;border-radius:14px;background:var(--mint);display:grid;place-items:center;font-size:20px;flex:none;}
.li .t{flex:1;min-width:0;font-weight:600;font-size:14px;line-height:1.25;overflow-wrap:anywhere;} .li .t small{display:block;color:var(--muted);font-weight:500;font-size:12px;}
.li .p{font-family:var(--display);font-weight:700;font-size:14px;color:var(--g700);white-space:nowrap;} .li .p.neg{color:#C0392B;}
/* scanner */
.vf{position:relative;height:260px;border-radius:28px;background:radial-gradient(circle at 50% 40%,#2E3A33,#111815 75%);overflow:hidden;display:grid;place-items:center;box-shadow:0 18px 40px rgba(0,0,0,.28);}
.vf .corner{position:absolute;width:44px;height:44px;border:4px solid var(--lime);}
.vf .c1{left:30px;top:30px;border-right:0;border-bottom:0;border-radius:14px 0 0 0}.vf .c2{right:30px;top:30px;border-left:0;border-bottom:0;border-radius:0 14px 0 0}
.vf .c3{left:30px;bottom:30px;border-right:0;border-top:0;border-radius:0 0 0 14px}.vf .c4{right:30px;bottom:30px;border-left:0;border-top:0;border-radius:0 0 14px 0}
.vf .tag{background:#F8F8F3;border-radius:14px 14px 20px 20px;padding:16px 14px 10px;width:200px;max-width:70%;text-align:center;color:#1b1b1b;animation:pulse 2s infinite;position:relative;}
.vf .tag:before{content:"";position:absolute;top:6px;left:50%;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#2a2f2c;}
.vf .bars{height:58px;margin:10px 4px 6px;background:repeating-linear-gradient(90deg,#111 0 2px,transparent 2px 4px,#111 4px 5px,transparent 5px 8px,#111 8px 11px,transparent 11px 13px);border-radius:2px;}
.vf .tag b{font-size:12px;display:block;} .vf .tag small{font-size:10.5px;color:#555;}
.vf .laser{position:absolute;left:44px;right:44px;height:3px;background:linear-gradient(90deg,transparent,#FF6B5B,transparent);box-shadow:0 0 18px #FF6B5B;animation:sweep 1.6s ease-in-out infinite alternate;}
.vf .hint{position:absolute;bottom:12px;left:0;right:0;text-align:center;color:#E8F0E6;font-size:12.5px;font-weight:600;opacity:.9;padding:0 12px;}
/* result */
.ptile{width:62px;height:62px;border-radius:20px;display:grid;place-items:center;font-size:32px;flex:none;background:linear-gradient(145deg,#E3F4E6,#fff);border:1px solid var(--line);}
.phead{display:flex;gap:12px;align-items:center;}
.phead .t{flex:1;min-width:0;} .pname{font-family:var(--display);font-weight:700;font-size:18px;line-height:1.15;overflow-wrap:anywhere;}
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
.fac .h{display:flex;justify-content:space-between;font-weight:700;font-size:14px;margin-bottom:6px;gap:8px;}
.track{height:12px;border-radius:999px;background:#EEF2EA;overflow:hidden;}
.fill{height:100%;border-radius:999px;animation:grow 1s ease both;}
.fill.g{background:linear-gradient(90deg,#2EAD62,#58C985)}.fill.y{background:linear-gradient(90deg,#F2A93B,#F7C46A)}.fill.r{background:linear-gradient(90deg,#E5533D,#F0806D)}
.fac .n{font-size:12px;color:var(--muted);margin-top:5px;}
.unit{display:flex;gap:12px;align-items:stretch;margin-top:10px;}
.unit .u{flex:1;background:var(--sand);border-radius:18px;padding:12px;font-size:12.5px;line-height:1.3;min-width:0;}
.unit .u b{display:block;font-family:var(--display);font-size:14px;margin:2px 0;}
.wtab{width:100%;border-collapse:collapse;font-size:13px;} .wtab td{padding:6px 2px;border-bottom:1px solid var(--line);} .wtab td:last-child{text-align:right;font-weight:700;}
/* alternatives */
[class*="st-key-alt_"]{background:#fff;border-radius:26px;padding:14px;box-shadow:var(--shadow);margin-bottom:14px;border:1px solid rgba(15,61,42,.04);animation:rise .5s ease both;}
.alt{display:flex;gap:12px;align-items:center;margin-bottom:10px;}
.alt .t{flex:1;min-width:0;} .alt .t b{font-family:var(--display);font-size:15.5px;line-height:1.2;display:block;overflow-wrap:anywhere;} .alt .t span{font-size:12.5px;color:var(--muted);}
.gb{width:54px;height:54px;border-radius:50%;display:grid;place-items:center;text-align:center;font-family:var(--display);font-weight:800;line-height:1;border:4px solid;flex:none;font-size:16px;}
.gb small{display:block;font-size:11px;margin-top:1px;}
.save{font-weight:800;color:var(--g700);} .more{font-weight:800;color:#9A6200;}
/* reward */
.celebrate{text-align:center;padding:10px 0 0;} .celebrate h1{font-size:30px;margin:6px 0;}
.plus{display:inline-block;background:linear-gradient(135deg,var(--lime),#9BE36A);color:var(--g900);font-family:var(--display);font-weight:800;font-size:56px;line-height:1;padding:14px 32px;border-radius:30px;animation:pop .6s ease both;box-shadow:0 14px 34px rgba(124,200,60,.4);}
.plus small{display:block;font-size:15px;font-weight:700;}
/* impact */
.badges{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.bdg{background:#fff;border-radius:20px;padding:12px 6px;text-align:center;box-shadow:var(--shadow);font-size:11.5px;font-weight:700;min-width:0;}
.bdg .e{font-size:28px;display:block;margin-bottom:4px;} .bdg small{display:block;color:var(--muted);font-weight:600;font-size:10.5px;margin-top:2px;}
.bdg.lock{opacity:.6;} .bdg.lock .e{filter:grayscale(1);}
.chart{display:flex;gap:8px;align-items:flex-end;height:130px;padding-top:6px;}
.chart .col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:6px;font-size:10.5px;color:var(--muted);font-weight:600;}
.chart .b{width:100%;border-radius:10px 10px 4px 4px;background:linear-gradient(180deg,#58C985,#1F7A45);animation:grow 1s ease both;min-height:4px;}
.chart .col.today .b{background:linear-gradient(180deg,#D9F77F,#8ED84F);}
.week{display:flex;justify-content:space-between;margin-top:10px;}
.dot{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700;background:#EEF2EA;color:var(--muted);}
.dot.on{background:linear-gradient(135deg,#FFB54D,#FF7A3D);color:#fff;}
.lb{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-weight:600;font-size:14px;} .lb:last-child{border:0}
.lb .rk{width:26px;height:26px;border-radius:50%;background:var(--sand);display:grid;place-items:center;font-size:12px;font-weight:800;flex:none;}
.lb.me{background:var(--mint);margin:0 -8px;padding:9px 8px;border-radius:14px;border:0;} .lb .pp{margin-left:auto;font-family:var(--display);font-weight:700;}
/* profile */
.avatar{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#34A363,#C9F26B);display:grid;place-items:center;font-family:var(--display);font-weight:800;font-size:30px;color:var(--g900);flex:none;}
.share{background:linear-gradient(145deg,#0B3322,#1F7A45);color:#fff;border-radius:26px;padding:20px;overflow:hidden;box-shadow:0 16px 36px rgba(15,61,42,.3);}
.share .sc{font-family:var(--display);font-weight:800;font-size:48px;line-height:1;} .share .sc small{font-size:18px;opacity:.7;}
.outfit .em{font-size:30px;letter-spacing:6px;}
/* compare */
.cmp{width:100%;border-collapse:collapse;font-size:13px;} .cmp td,.cmp th{padding:8px 4px;border-bottom:1px solid var(--line);text-align:center;} .cmp td:first-child,.cmp th:first-child{text-align:left;color:var(--muted);font-weight:600;}
.cmp .win{color:var(--g700);font-weight:800;}
.legend{display:flex;gap:14px;justify-content:center;font-size:12px;font-weight:700;margin-top:4px;flex-wrap:wrap;} .legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;}
.radar{display:block;margin:0 auto;max-width:100%;height:auto;}
"""


def _px_to_rem(css: str) -> str:
    return re.sub(r"font-size:\s*([\d.]+)px", lambda m: f"font-size:{float(m.group(1)) / 16:.4f}rem", css)


CSS = _px_to_rem(_CSS)


def build(large: bool = False, reduce_motion: bool = False) -> str:
    extra = ""
    if large:
        extra += "html{font-size:18px;}"
    if reduce_motion:
        extra += "*,*:before,*:after{animation:none!important;transition:none!important;}"
    return f"<style>{CSS}{extra}</style>"
