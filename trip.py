import streamlit as st
import json
import os
import uuid
from datetime import date, datetime

st.set_page_config(page_title="OrbitDates", page_icon="🎂", layout="wide")

DATA_FILE = "orbitdates_data.json"

GIFT_IDEAS = {
    "Reading": ["A book from their favorite author", "A cozy reading nook blanket", "A personalized bookmark", "A subscription to a book box"],
    "Cooking": ["A specialty spice set", "A nice knife or kitchen gadget", "A cookbook from a cuisine they love", "A cooking class experience"],
    "Tech": ["Wireless earbuds", "A smart home gadget", "A phone/tablet accessory", "A charging stand"],
    "Fitness": ["Workout gear or apparel", "A fitness tracker", "A gym or class membership", "A yoga mat or accessories"],
    "Music": ["Concert tickets", "Vinyl records from favorite artists", "Headphones", "An instrument accessory"],
    "Outdoors": ["A camping/hiking gadget", "A nice water bottle", "Outdoor apparel", "A trip or day excursion"],
    "Art & Craft": ["Quality art supplies", "A class or workshop", "A custom commissioned piece", "A creative subscription box"],
    "Gaming": ["A new game they've wanted", "Gaming accessories", "A gift card to a gaming platform", "Merch from a favorite game"],
    "Fashion": ["A statement accessory", "A gift card to a favorite store", "A personalized item", "Seasonal apparel"],
    "Travel": ["A travel accessory (packing cubes, neck pillow)", "A gift card for flights/hotels", "A guidebook to a dream destination", "Luggage tags or a nice bag"],
}

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stApp { background: radial-gradient(ellipse at top, #2a1030 0%, #100a24 45%, #05040c 100%); }
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
        background: linear-gradient(90deg, #ff8ac6, #b487ff, #6ee7ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        margin-bottom: 0;
    }
    .cosmic-sub { color: rgba(255,255,255,0.65); font-size: 1.05rem; margin-top: 0; margin-bottom: 20px; }
    .days-badge {
        display: inline-block; padding: 4px 14px; border-radius: 999px; font-weight: 700; font-size: 0.9rem;
    }
    .days-soon { background: rgba(255,138,198,0.2); border: 1px solid rgba(255,138,198,0.5); color: #ff8ac6; }
    .days-normal { background: rgba(110,231,255,0.15); border: 1px solid rgba(110,231,255,0.4); color: #6ee7ff; }
    .stButton>button {
        background: linear-gradient(90deg, #ff8ac6, #b487ff); color: white; border: none;
        border-radius: 12px; padding: 0.5rem 1.2rem; font-weight: 600; transition: transform 0.15s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(180,135,255,0.35); }
    .gift-chip {
        background: rgba(180,135,255,0.12); border: 1px solid rgba(180,135,255,0.3); border-radius: 10px;
        padding: 8px 12px; margin-bottom: 6px; color: #e6d9ff;
    }
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
    return {"people": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "dates_data" not in st.session_state:
    st.session_state.dates_data = load_data()
data = st.session_state.dates_data

def days_until(month, day):
    today = date.today()
    try:
        next_date = date(today.year, month, day)
    except ValueError:
        next_date = date(today.year, 3, 1)  # handle Feb 29 fallback
    if next_date < today:
        try:
            next_date = date(today.year + 1, month, day)
        except ValueError:
            next_date = date(today.year + 1, 3, 1)
    return (next_date - today).days, next_date

st.markdown('<p class="cosmic-title">🎂 OrbitDates</p>', unsafe_allow_html=True)
st.markdown('<p class="cosmic-sub">Never miss a birthday or anniversary again — with gift ideas built in.</p>', unsafe_allow_html=True)

tabs = st.tabs(["📆 Upcoming Dates", "➕ Add Person", "🎁 Gift Ideas"])

# ---------------- UPCOMING DATES ----------------
with tabs[0]:
    if not data["people"]:
        st.info("No dates added yet. Add someone in the 'Add Person' tab!")
    else:
        enriched = []
        for p in data["people"]:
            d, next_date = days_until(p["month"], p["day"])
            enriched.append((d, next_date, p))
        enriched.sort(key=lambda x: x[0])

        for d, next_date, p in enriched:
            badge_class = "days-soon" if d <= 14 else "days-normal"
            day_text = "Today! 🎉" if d == 0 else ("Tomorrow!" if d == 1 else f"{d} days")
            st.markdown(f'''<div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b style="font-size:1.15rem;">{p["name"]}</b>
                        <span style="color:rgba(255,255,255,0.5); margin-left:8px;">{p["event_type"]} · {next_date.strftime("%B %d")}</span>
                    </div>
                    <span class="days-badge {badge_class}">{day_text}</span>
                </div>
            </div>''', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 1, 4])
            with c1:
                if st.button("🎁 Gift ideas", key=f"gift_{p['id']}"):
                    st.session_state["quick_gift_interest"] = p.get("interest", "Reading")
            with c2:
                if st.button("Delete", key=f"del_{p['id']}"):
                    data["people"] = [x for x in data["people"] if x["id"] != p["id"]]
                    save_data(data)
                    st.rerun()

        if st.session_state.get("quick_gift_interest"):
            interest = st.session_state["quick_gift_interest"]
            st.markdown(f"#### Gift ideas for {interest} lovers")
            for idea in GIFT_IDEAS.get(interest, []):
                st.markdown(f'<div class="gift-chip">🎁 {idea}</div>', unsafe_allow_html=True)

# ---------------- ADD PERSON ----------------
with tabs[1]:
    st.markdown("#### Add an important date")
    with st.form("add_person_form", clear_on_submit=True):
        name = st.text_input("Name")
        c1, c2 = st.columns(2)
        with c1:
            event_type = st.selectbox("Event type", ["Birthday", "Anniversary", "Other"])
        with c2:
            interest = st.selectbox("Interest (for gift ideas)", list(GIFT_IDEAS.keys()))
        event_date = st.date_input("Date (year doesn't matter, just month/day)", value=date.today())
        note = st.text_input("Note (optional)")
        submitted = st.form_submit_button("Add")
        if submitted:
            if name.strip():
                data["people"].append({
                    "id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "event_type": event_type,
                    "month": event_date.month,
                    "day": event_date.day,
                    "interest": interest,
                    "note": note
                })
                save_data(data)
                st.success(f"Added {name}!")
                st.rerun()
            else:
                st.warning("Please enter a name.")

# ---------------- GIFT IDEAS BROWSER ----------------
with tabs[2]:
    st.markdown("#### Browse gift ideas by interest")
    browse_interest = st.selectbox("Pick an interest", list(GIFT_IDEAS.keys()), key="browse_interest")
    for idea in GIFT_IDEAS[browse_interest]:
        st.markdown(f'<div class="gift-chip">🎁 {idea}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Generate a card message")
    card_name = st.text_input("Recipient name", key="card_name")
    card_occasion = st.selectbox("Occasion", ["Birthday", "Anniversary", "Congratulations", "Thank You"])
    card_tone = st.selectbox("Tone", ["Warm & Heartfelt", "Fun & Playful", "Short & Sweet"])
    if st.button("Generate message"):
        templates = {
            ("Birthday", "Warm & Heartfelt"): f"Happy Birthday, {card_name}! Wishing you a year filled with joy, laughter, and everything that makes you smile. So grateful to have you in my life.",
            ("Birthday", "Fun & Playful"): f"Happy Birthday, {card_name}! 🎉 Another trip around the sun — hope it's full of cake, surprises, and zero adulting responsibilities today.",
            ("Birthday", "Short & Sweet"): f"Happy Birthday, {card_name}! Hope your day is as wonderful as you are. 🎂",
            ("Anniversary", "Warm & Heartfelt"): f"Happy Anniversary! Celebrating you and the beautiful journey you've built together — here's to many more years of love and adventure.",
            ("Anniversary", "Fun & Playful"): f"Happy Anniversary! 🥂 Still going strong — you two make it look easy!",
            ("Anniversary", "Short & Sweet"): "Happy Anniversary! Wishing you continued love and happiness.",
            ("Congratulations", "Warm & Heartfelt"): f"Congratulations, {card_name}! Your hard work and dedication brought you here, and it's so well deserved.",
            ("Congratulations", "Fun & Playful"): f"Congrats, {card_name}! 🎊 Go celebrate, you earned it!",
            ("Congratulations", "Short & Sweet"): f"Congratulations, {card_name}! So happy for you.",
            ("Thank You", "Warm & Heartfelt"): f"Thank you, {card_name}, for everything you've done. Your kindness means more than words can say.",
            ("Thank You", "Fun & Playful"): f"Thanks a million, {card_name}! You're the best. 🙌",
            ("Thank You", "Short & Sweet"): f"Thank you so much, {card_name}!",
        }
        message = templates.get((card_occasion, card_tone), "Thinking of you today!")
        st.markdown(f'<div class="glass-card">{message}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.85rem;">Your data stays local · Part of the App Universe ✨</p>', unsafe_allow_html=True)
