import streamlit as st
import json
import os
import uuid
from datetime import datetime, date

st.set_page_config(page_title="OrbitCountdown", page_icon="🪐", layout="wide")

DATA_FILE = "orbitcountdown_data.json"

COLOR_OPTIONS = {
    "Cyan": "#6ee7ff",
    "Purple": "#b487ff",
    "Pink": "#ff8ac6",
    "Gold": "#ffd36e",
    "Green": "#8affc1",
    "Orange": "#ff8a5c",
}

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stApp { background: radial-gradient(ellipse at top, #0f1030 0%, #08081e 45%, #030308 100%); }
    #starfield {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
        background-image:
            radial-gradient(2px 2px at 20px 30px, white, transparent),
            radial-gradient(1.5px 1.5px at 90px 150px, white, transparent),
            radial-gradient(2px 2px at 160px 60px, white, transparent),
            radial-gradient(1px 1px at 250px 200px, white, transparent),
            radial-gradient(1.5px 1.5px at 310px 100px, white, transparent),
            radial-gradient(2px 2px at 400px 250px, white, transparent);
        background-repeat: repeat; background-size: 420px 420px;
        opacity: 0.55; animation: twinkle 6s ease-in-out infinite alternate;
    }
    @keyframes twinkle { from { opacity: 0.35; } to { opacity: 0.75; } }
    .glass-card {
        background: rgba(255,255,255,0.06); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 18px; padding: 20px 22px;
        margin-bottom: 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }
    .cosmic-title {
        font-weight: 800; font-size: 2.6rem;
        background: linear-gradient(90deg, #6ee7ff, #b487ff, #ffd36e);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        margin-bottom: 0;
    }
    .cosmic-sub { color: rgba(255,255,255,0.65); font-size: 1.05rem; margin-top: 0; margin-bottom: 20px; }
    .orbit-track {
        position: relative; height: 70px; width: 100%; margin: 10px 0 4px;
    }
    .orbit-line {
        position: absolute; top: 50%; left: 0; right: 0; height: 2px;
        background: rgba(255,255,255,0.12); transform: translateY(-50%);
    }
    .orbit-sun {
        position: absolute; right: 0; top: 50%; transform: translate(50%, -50%);
        font-size: 1.8rem;
    }
    .orbit-planet {
        position: absolute; top: 50%; transform: translateY(-50%); font-size: 1.6rem;
        transition: left 0.4s ease;
    }
    .countdown-num { font-size: 2.2rem; font-weight: 800; }
    .stButton>button {
        background: linear-gradient(90deg, #6ee7ff, #b487ff); color: #08081e; border: none;
        border-radius: 12px; padding: 0.5rem 1.2rem; font-weight: 700; transition: transform 0.15s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(110,231,255,0.35); }
    </style>
    <div id="starfield"></div>
    """, unsafe_allow_html=True)

load_css()

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"events": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "countdown_data" not in st.session_state:
    st.session_state.countdown_data = load_data()
data = st.session_state.countdown_data

st.markdown('<p class="cosmic-title">🪐 OrbitCountdown</p>', unsafe_allow_html=True)
st.markdown('<p class="cosmic-sub">Track every countdown as a planet orbiting toward its moment.</p>', unsafe_allow_html=True)

tabs = st.tabs(["🌌 Active Countdowns", "➕ New Countdown"])

# ---------------- ACTIVE COUNTDOWNS ----------------
with tabs[0]:
    if not data["events"]:
        st.info("No countdowns yet. Add one in the 'New Countdown' tab!")
    else:
        today = date.today()
        enriched = []
        for e in data["events"]:
            target = datetime.strptime(e["date"], "%Y-%m-%d").date()
            days_left = (target - today).days
            enriched.append((days_left, target, e))
        enriched.sort(key=lambda x: x[0])

        for days_left, target, e in enriched:
            color = COLOR_OPTIONS.get(e.get("color", "Cyan"), "#6ee7ff")
            status = "🎉 It's today!" if days_left == 0 else ("Passed" if days_left < 0 else f"{days_left} days left")
            # progress: assume a 60-day orbit window for visual purposes, capped
            orbit_span = max(e.get("orbit_span", 60), 1)
            progress_pct = max(0, min(100, 100 - (days_left / orbit_span * 100))) if days_left >= 0 else 100

            st.markdown(f'''<div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b style="font-size:1.2rem; color:{color};">{e["label"]}</b>
                        <div style="color:rgba(255,255,255,0.5); font-size:0.85rem;">{target.strftime("%B %d, %Y")}</div>
                    </div>
                    <span class="countdown-num" style="color:{color};">{status}</span>
                </div>
                <div class="orbit-track">
                    <div class="orbit-line"></div>
                    <div class="orbit-sun">☀️</div>
                    <div class="orbit-planet" style="left:{progress_pct}%;">🪐</div>
                </div>
            </div>''', unsafe_allow_html=True)

            if st.button("Delete", key=f"del_{e['id']}"):
                data["events"] = [x for x in data["events"] if x["id"] != e["id"]]
                save_data(data)
                st.rerun()

# ---------------- NEW COUNTDOWN ----------------
with tabs[1]:
    st.markdown("#### Create a new countdown")
    with st.form("new_countdown_form", clear_on_submit=True):
        label = st.text_input("Label (e.g. Trip to Japan, Project Deadline)")
        c1, c2 = st.columns(2)
        with c1:
            target_date = st.date_input("Target date", value=date.today())
        with c2:
            color_choice = st.selectbox("Color", list(COLOR_OPTIONS.keys()))
        orbit_span = st.slider("Orbit visual window (days, purely visual pacing)", min_value=7, max_value=365, value=60)
        submitted = st.form_submit_button("Add Countdown")
        if submitted:
            if label.strip():
                data["events"].append({
                    "id": str(uuid.uuid4()),
                    "label": label.strip(),
                    "date": str(target_date),
                    "color": color_choice,
                    "orbit_span": orbit_span
                })
                save_data(data)
                st.success(f"Added countdown for {label}!")
                st.rerun()
            else:
                st.warning("Please enter a label.")

st.markdown("---")
st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.85rem;">Your data stays local · Part of the App Universe ✨</p>', unsafe_allow_html=True)
