import streamlit as st
import requests
import json
import os
import uuid
from datetime import date

st.set_page_config(page_title="VoyagerPlan", page_icon="🧳", layout="wide")

DATA_FILE = "voyagerplan_data.json"

DEFAULT_PACKING_TEMPLATE = [
    "Passport / ID", "Phone charger", "Toiletries", "Medications",
    "Weather-appropriate clothing", "Comfortable shoes", "Travel documents/tickets", "Reusable water bottle"
]

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stApp { background: radial-gradient(ellipse at top, #0d1f30 0%, #081420 45%, #040a10 100%); }
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
        opacity: 0.5; animation: twinkle 6s ease-in-out infinite alternate;
    }
    @keyframes twinkle { from { opacity: 0.3; } to { opacity: 0.7; } }
    .glass-card {
        background: rgba(255,255,255,0.06); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 18px; padding: 20px 22px;
        margin-bottom: 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }
    .cosmic-title {
        font-weight: 800; font-size: 2.6rem;
        background: linear-gradient(90deg, #6ee7ff, #8affc1, #ffd36e);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        margin-bottom: 0;
    }
    .cosmic-sub { color: rgba(255,255,255,0.65); font-size: 1.05rem; margin-top: 0; margin-bottom: 20px; }
    .trip-title { font-weight: 700; font-size: 1.4rem; color: #6ee7ff; margin-bottom: 4px; }
    .trip-dates { color: rgba(255,255,255,0.55); font-size: 0.9rem; margin-bottom: 10px; }
    .budget-item {
        background: rgba(255,255,255,0.04); border-radius: 8px; padding: 8px 12px;
        margin-bottom: 5px; display: flex; justify-content: space-between; color: rgba(255,255,255,0.85);
    }
    .stButton>button {
        background: linear-gradient(90deg, #6ee7ff, #8affc1); color: #040a10; border: none;
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
    return {"trips": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "trip_data" not in st.session_state:
    st.session_state.trip_data = load_data()
data = st.session_state.trip_data

@st.cache_data(ttl=1800)
def geocode_destination(name):
    try:
        r = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                          params={"name": name, "count": 1}, timeout=10)
        results = r.json().get("results")
        return results[0] if results else None
    except Exception:
        return None

@st.cache_data(ttl=1800)
def get_weather_forecast(lat, lon):
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast",
                          params={
                              "latitude": lat, "longitude": lon,
                              "daily": "temperature_2m_max,temperature_2m_min,weathercode",
                              "timezone": "auto"
                          }, timeout=10)
        return r.json()
    except Exception:
        return None

WEATHER_CODES = {
    0: "☀️ Clear", 1: "🌤️ Mostly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
    45: "🌫️ Fog", 51: "🌦️ Light drizzle", 61: "🌧️ Rain", 71: "🌨️ Snow",
    80: "🌦️ Showers", 95: "⛈️ Thunderstorm"
}

st.markdown('<p class="cosmic-title">🧳 VoyagerPlan</p>', unsafe_allow_html=True)
st.markdown('<p class="cosmic-sub">Plan every trip — itinerary, packing list, and budget in one orbit.</p>', unsafe_allow_html=True)

tabs = st.tabs(["🗺️ My Trips", "➕ New Trip"])

# ---------------- MY TRIPS ----------------
with tabs[0]:
    if not data["trips"]:
        st.info("No trips planned yet. Create one in the 'New Trip' tab!")
    else:
        trip_names = [f"{t['destination']} ({t['start_date']} to {t['end_date']})" for t in data["trips"]]
        selected_idx = st.selectbox("Select a trip", range(len(trip_names)), format_func=lambda i: trip_names[i])
        trip = data["trips"][selected_idx]

        st.markdown(f'''<div class="glass-card">
            <div class="trip-title">📍 {trip["destination"]}</div>
            <div class="trip-dates">{trip["start_date"]} → {trip["end_date"]}</div>
        </div>''', unsafe_allow_html=True)

        sub_tabs = st.tabs(["🌦️ Weather", "🎒 Packing List", "💵 Budget", "🗑️ Manage"])

        with sub_tabs[0]:
            geo = geocode_destination(trip["destination"])
            if geo:
                forecast = get_weather_forecast(geo["latitude"], geo["longitude"])
                if forecast and "daily" in forecast:
                    daily = forecast["daily"]
                    cols = st.columns(min(7, len(daily["time"])))
                    for i, col in enumerate(cols):
                        with col:
                            code = daily["weathercode"][i]
                            desc = WEATHER_CODES.get(code, "🌡️")
                            st.markdown(f'''<div class="glass-card" style="text-align:center; padding:12px;">
                                <div style="font-size:0.75rem; color:rgba(255,255,255,0.5);">{daily["time"][i][5:]}</div>
                                <div style="font-size:1.5rem;">{desc.split(" ")[0]}</div>
                                <div style="font-size:0.85rem;">{round(daily["temperature_2m_max"][i])}° / {round(daily["temperature_2m_min"][i])}°</div>
                            </div>''', unsafe_allow_html=True)
                else:
                    st.info("Couldn't load forecast data for this destination.")
            else:
                st.info("Couldn't find that destination for weather lookup. Try a more specific name (e.g. 'Paris, France').")

        with sub_tabs[1]:
            st.markdown("#### Packing checklist")
            for i, item in enumerate(trip["packing_list"]):
                checked = st.checkbox(item["name"], value=item["checked"], key=f"pack_{trip['id']}_{i}")
                if checked != item["checked"]:
                    item["checked"] = checked
                    save_data(data)
            new_item = st.text_input("Add item", key=f"new_pack_{trip['id']}")
            if st.button("Add to packing list", key=f"add_pack_{trip['id']}"):
                if new_item.strip():
                    trip["packing_list"].append({"name": new_item.strip(), "checked": False})
                    save_data(data)
                    st.rerun()

        with sub_tabs[2]:
            st.markdown("#### Budget estimate")
            total = sum(item["amount"] for item in trip["budget"])
            st.markdown(f"**Total estimated: ${total:,.2f}**")
            for item in trip["budget"]:
                st.markdown(f'''<div class="budget-item">
                    <span>{item["category"]}</span>
                    <span>${item["amount"]:,.2f}</span>
                </div>''', unsafe_allow_html=True)
            bc1, bc2, bc3 = st.columns([2, 1, 1])
            with bc1:
                b_cat = st.text_input("Category (e.g. Flights, Hotel, Food)", key=f"bcat_{trip['id']}")
            with bc2:
                b_amt = st.number_input("Amount ($)", min_value=0.0, step=10.0, key=f"bamt_{trip['id']}")
            with bc3:
                st.write("")
                st.write("")
                if st.button("Add", key=f"badd_{trip['id']}"):
                    if b_cat.strip() and b_amt > 0:
                        trip["budget"].append({"category": b_cat.strip(), "amount": b_amt})
                        save_data(data)
                        st.rerun()

        with sub_tabs[3]:
            if st.button("🗑️ Delete this trip", key=f"deltrip_{trip['id']}"):
                data["trips"] = [t for t in data["trips"] if t["id"] != trip["id"]]
                save_data(data)
                st.rerun()

# ---------------- NEW TRIP ----------------
with tabs[1]:
    st.markdown("#### Plan a new trip")
    with st.form("new_trip_form", clear_on_submit=True):
        destination = st.text_input("Destination (e.g. Tokyo, Japan)")
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input("Start date", value=date.today())
        with c2:
            end_date = st.date_input("End date", value=date.today())
        use_template = st.checkbox("Start with default packing checklist", value=True)
        submitted = st.form_submit_button("Create Trip")
        if submitted:
            if destination.strip():
                packing = [{"name": item, "checked": False} for item in DEFAULT_PACKING_TEMPLATE] if use_template else []
                data["trips"].append({
                    "id": str(uuid.uuid4()),
                    "destination": destination.strip(),
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "packing_list": packing,
                    "budget": []
                })
                save_data(data)
                st.success(f"Trip to {destination} created!")
                st.rerun()
            else:
                st.warning("Please enter a destination.")

st.markdown("---")
st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.85rem;">Weather by Open-Meteo · Your data stays local · Part of the App Universe ✨</p>', unsafe_allow_html=True)
