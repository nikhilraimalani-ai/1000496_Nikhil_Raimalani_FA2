"""SustainStyle – scan a clothing tag, see its eco-score, swap to better, earn GreenPoints."""
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).resolve().parent))  # make the sustainstyle/ folder importable

from sustainstyle import state, theme, ui
from sustainstyle.pages import alts, compare, home, impact, profile, result, reward, scan

st.set_page_config(page_title="SustainStyle", page_icon="🌿", layout="centered", initial_sidebar_state="collapsed")
state.init()
prefs = state.prefs()
st.markdown(theme.build(large=prefs["large"], reduce_motion=prefs["reduce_motion"]), unsafe_allow_html=True)

PAGES = dict(home=home, scan=scan, result=result, alts=alts, compare=compare, reward=reward, impact=impact, profile=profile)
PAGES[st.session_state.view].render_page()
ui.nav()

# After navigating, start the new screen at the top (Streamlit keeps the old scroll position).
if st.session_state.shown_view != st.session_state.view:
    st.session_state.shown_view = st.session_state.view
    components.html("<script>const m=window.parent.document.querySelector('[data-testid=\"stMain\"]');if(m){m.scrollTo(0,0);}</script>", height=0)
