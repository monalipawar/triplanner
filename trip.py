import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════════
# THEME + SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
THEMES = {
    "Default":   "linear-gradient(160deg,#020617,#0f172a,#1e293b)",
    "Cyberpunk": "linear-gradient(160deg,#1a0030,#3333ff,#00ffee)",
    "Sunset":    "linear-gradient(160deg,#1a0a05,#ff5e62,#ffcc70)",
    "Ocean":     "linear-gradient(160deg,#0a1628,#2193b0,#38bdf8)",
    "Midnight":  "linear-gradient(160deg,#000000,#0f172a,#020617)",
}

for k, v in [("selected_theme", "Default")]:
    if k not in st.session_state:
        st.session_state[k] = v

st.set_page_config(page_title="App Launcher", page_icon="🚀", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# APPS
# ═══════════════════════════════════════════════════════════════════════════════
APPS = [
    {
        "name": "TimeKeeper",
        "url": "https://timekeeper1.streamlit.app/",
        "icon": "⏱️",
        "desc": "Track, manage and visualize your time with precision.",
        "tag": "Productivity",
        "color": "#38bdf8",
        "css_class": "card-blue",
    },
    {
        "name": "Solar AI",
        "url": "https://solai1.streamlit.app/",
        "icon": "🌌",
        "desc": "Explore NASA APOD, ISS tracking, asteroids & more.",
        "tag": "Space & AI",
        "color": "#a78bfa",
        "css_class": "card-purple",
    },
    {
        "name": "Nimbus AI",
        "url": "https://nimai10.streamlit.app/",
        "icon": "🌤️",
        "desc": "AI-powered weather intelligence and smart outfit picks.",
        "tag": "Weather & AI",
        "color": "#34d399",
        "css_class": "card-green",
    },
    {
        "name": "Dice Roller",
        "url": "https://diceroller1.streamlit.app/",
        "icon": "🎲",
        "desc": "Roll any dice combination for your tabletop adventures.",
        "tag": "Games",
        "color": "#fb923c",
        "css_class": "card-orange",
    },
    {
        "name": "Animal Dictionary",
        "url": "https://aniking.streamlit.app/",
        "icon": "🐾",
        "desc": "Explore facts, habitats & stats on animals from across the globe.",
        "tag": "Nature & Science",
        "color": "#4ade80",
        "css_class": "card-lime",
    },
    {
        "name": "Activity Finder",
        "url": "https://stuff-to-do.streamlit.app/",
        "icon": "🎈",
        "desc": "Answer a few fun questions and discover your next kid-friendly adventure!",
        "tag": "Kids & Fun",
        "color": "#f472b6",
        "css_class": "card-pink",
    },
    {
        "name": "Draw Finder",
        "url": "https://draw10.streamlit.app/",
        "icon": "🎨",
        "desc": "Answer a few fun questions and get a creative drawing challenge made just for you!",
        "tag": "Creativity",
        "color": "#facc15",
        "css_class": "card-yellow",
    },
    {
        "name": "Country Explorer",
        "url": "https://explorer1.streamlit.app/",
        "icon": "🌍",
        "desc": "Discover capitals, flags, facts & stats, then quiz yourself on world geography.",
        "tag": "Geography",
        "color": "#22d3ee",
        "css_class": "card-teal",
    },
    {
        "name": "CosmicChef",
        "url": "https://cooking1.streamlit.app/",
        "icon": "🍳",
        "desc": "Enter ingredients you have on hand and discover recipes to cook tonight.",
        "tag": "Food & Cooking",
        "color": "#ff8a5c",
        "css_class": "card-coral",
    },
    {
        "name": "NebulaWallet",
        "url": "https://wallet1.streamlit.app/",
        "icon": "💰",
        "desc": "Log income & expenses, track spending by category, and hit savings goals.",
        "tag": "Finance",
        "color": "#6ee7ff",
        "css_class": "card-indigo",
    },
    {
        "name": "OrbitMeals",
        "url": "https://orbitmeals1.streamlit.app/",
        "icon": "🍽️",
        "desc": "Plan your week, generate your shopping list, orbit your kitchen with ease.",
        "tag": "Meal Planning",
        "color": "#8affc1",
        "css_class": "card-mint",
    },
    {
        "name": "OrbitDates",
        "url": "https://orbitdates1.streamlit.app/",
        "icon": "🎂",
        "desc": "Never miss a birthday or anniversary again — with gift ideas built in.",
        "tag": "Reminders",
        "color": "#ff8ac6",
        "css_class": "card-rose",
    },
    {
        "name": "OrbitCountdown",
        "url": "https://orbitcountdown1.streamlit.app/",
        "icon": "🪐",
        "desc": "Track every countdown as a planet orbiting toward its moment.",
        "tag": "Countdowns",
        "color": "#6ee7ff",
        "css_class": "card-skyblue",
    },
    {
        "name": "Bibliocosm",
        "url": "https://bibliocosm1.streamlit.app/",
        "icon": "📚",
        "desc": "Track your reading universe, one book at a time.",
        "tag": "Reading",
        "color": "#b487ff",
        "css_class": "card-violet",
    },
    {
        "name": "VoyagerPlan",
        "url": "https://voyagerplan1.streamlit.app/",
        "icon": "🧳",
        "desc": "Plan every trip — itinerary, packing list, and budget in one orbit.",
        "tag": "Travel",
        "color": "#38bdf8",
        "css_class": "card-cerulean",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — single viewport, no scroll
# ═══════════════════════════════════════════════════════════════════════════════
bg = THEMES[st.session_state.selected_theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: {bg} !important;
    min-height: 100vh !important;
    font-family: 'Outfit', sans-serif !important;
}}
[data-testid="stAppViewContainer"] > .main {{
    background: transparent !important;
    padding: 0 !important;
}}
[data-testid="stMain"] {{
    padding: 0 !important;
}}
.main .block-container {{
    padding: 0.6rem 1.2rem 0.4rem !important;
    max-width: 100% !important;
}}
[data-testid="stHeader"] {{ background: transparent !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* Stars */
.stars-bg {{
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}}
.star {{
    position: absolute; border-radius: 50%; background: white;
    animation: twinkle var(--dur, 3s) ease-in-out infinite alternate;
    opacity: 0;
}}
@keyframes twinkle {{
    0%   {{ opacity: 0.1; transform: scale(0.8); }}
    100% {{ opacity: 0.85; transform: scale(1.2); }}
}}

/* Wrapper */
.launcher-wrap {{
    position: relative; z-index: 1;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0.5rem 1.5rem;
    box-sizing: border-box;
}}

/* Header */
.launcher-header {{
    text-align: center;
    margin-bottom: 1rem;
}}
.launcher-header h1 {{
    font-family: 'Outfit', sans-serif; font-weight: 800;
    font-size: clamp(1.4rem, 3vw, 2.2rem); letter-spacing: -0.02em;
    background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 0.2rem; line-height: 1.15;
}}
.launcher-header p {{
    font-family: 'Outfit', sans-serif; font-size: 0.85rem;
    color: rgba(148,163,184,0.85); font-weight: 300; letter-spacing: 0.04em; margin: 0;
}}

/* Cards row */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    flex: 0 0 auto;
}}

.app-card {{
    position: relative;
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 1.2rem 1rem 1rem;
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    text-decoration: none !important;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-height:240px;
    height:100%;
    transition: transform 0.28s cubic-bezier(.22,.68,0,1.2), box-shadow 0.28s ease, border-color 0.28s ease;
}}
.app-card:hover {{ transform: translateY(-5px) scale(1.015); }}

.card-orb {{
    position: absolute; top: -30px; right: -30px;
    width: 100px; height: 100px; border-radius: 50%;
    filter: blur(30px); pointer-events: none; opacity: 0.5;
    transition: opacity 0.3s ease;
}}
.app-card:hover .card-orb {{ opacity: 0.9; }}

.card-tag {{
    display: inline-block; font-family: 'Outfit', sans-serif;
    font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 2px 8px; border-radius: 20px; margin-bottom: 0.6rem;
    width: fit-content;
}}
.card-icon {{ font-size: 2rem; line-height: 1; margin-bottom: 0.5rem; display: block; }}
.card-name {{
    font-family: 'Outfit', sans-serif; font-weight: 700;
    font-size: 1.1rem; color: #f1f5f9; margin: 0 0 0.3rem; letter-spacing: -0.01em;
}}
.card-desc {{
    font-family: 'Outfit', sans-serif; font-size: 0.78rem;
    color: rgba(148,163,184,0.8); font-weight: 300; line-height: 1.5;
    margin: 0 0 0.8rem; flex: 1;
}}
.card-cta {{
    display: flex; align-items: center; gap: 5px;
    font-family: 'Outfit', sans-serif; font-size: 0.75rem;
    font-weight: 600; letter-spacing: 0.03em;
    transition: gap 0.2s ease;
    margin-top: auto;
}}
.app-card:hover .card-cta {{ gap: 9px; }}

/* Per-card accent colors */
.card-blue  {{ border-color: rgba(56,189,248,0.15); }}
.card-blue:hover  {{ border-color: #38bdf8; box-shadow: 0 0 0 1px #38bdf8, 0 16px 40px -8px rgba(56,189,248,0.3); }}
.card-blue  .card-tag {{ color: #38bdf8; }}
.card-blue  .card-cta {{ color: #38bdf8; }}
.card-blue  .card-orb {{ background: rgba(56,189,248,0.4); }}

.card-purple {{ border-color: rgba(167,139,250,0.15); }}
.card-purple:hover {{ border-color: #a78bfa; box-shadow: 0 0 0 1px #a78bfa, 0 16px 40px -8px rgba(167,139,250,0.3); }}
.card-purple .card-tag {{ color: #a78bfa; }}
.card-purple .card-cta {{ color: #a78bfa; }}
.card-purple .card-orb {{ background: rgba(167,139,250,0.4); }}

.card-green {{ border-color: rgba(52,211,153,0.15); }}
.card-green:hover {{ border-color: #34d399; box-shadow: 0 0 0 1px #34d399, 0 16px 40px -8px rgba(52,211,153,0.3); }}
.card-green .card-tag {{ color: #34d399; }}
.card-green .card-cta {{ color: #34d399; }}
.card-green .card-orb {{ background: rgba(52,211,153,0.4); }}

.card-orange {{ border-color: rgba(251,146,60,0.15); }}
.card-orange:hover {{ border-color: #fb923c; box-shadow: 0 0 0 1px #fb923c, 0 16px 40px -8px rgba(251,146,60,0.3); }}
.card-orange .card-tag {{ color: #fb923c; }}
.card-orange .card-cta {{ color: #fb923c; }}
.card-orange .card-orb {{ background: rgba(251,146,60,0.4); }}

.card-lime {{ border-color: rgba(74,222,128,0.15); }}
.card-lime:hover {{ border-color: #4ade80; box-shadow: 0 0 0 1px #4ade80, 0 16px 40px -8px rgba(74,222,128,0.3); }}
.card-lime .card-tag {{ color: #4ade80; }}
.card-lime .card-cta {{ color: #4ade80; }}
.card-lime .card-orb {{ background: rgba(74,222,128,0.4); }}

.card-pink {{ border-color: rgba(244,114,182,0.15); }}
.card-pink:hover {{ border-color: #f472b6; box-shadow: 0 0 0 1px #f472b6, 0 16px 40px -8px rgba(244,114,182,0.3); }}
.card-pink .card-tag {{ color: #f472b6; }}
.card-pink .card-cta {{ color: #f472b6; }}
.card-pink .card-orb {{ background: rgba(244,114,182,0.4); }}


.card-yellow {{ border-color: rgba(250,204,21,0.15); }}
.card-yellow:hover {{ border-color:#facc15; box-shadow:0 0 0 1px #facc15,0 16px 40px -8px rgba(250,204,21,.3);}}
.card-yellow .card-tag,.card-yellow .card-cta{{color:#facc15;}}
.card-yellow .card-orb{{background:rgba(250,204,21,.4);}}

.card-teal {{ border-color: rgba(34,211,238,0.15); }}
.card-teal:hover {{ border-color:#22d3ee; box-shadow:0 0 0 1px #22d3ee,0 16px 40px -8px rgba(34,211,238,.3);}}
.card-teal .card-tag,.card-teal .card-cta{{color:#22d3ee;}}
.card-teal .card-orb{{background:rgba(34,211,238,.4);}}

.card-coral {{ border-color: rgba(255,138,92,0.15); }}
.card-coral:hover {{ border-color:#ff8a5c; box-shadow:0 0 0 1px #ff8a5c,0 16px 40px -8px rgba(255,138,92,.3);}}
.card-coral .card-tag,.card-coral .card-cta{{color:#ff8a5c;}}
.card-coral .card-orb{{background:rgba(255,138,92,.4);}}

.card-indigo {{ border-color: rgba(110,231,255,0.15); }}
.card-indigo:hover {{ border-color:#6ee7ff; box-shadow:0 0 0 1px #6ee7ff,0 16px 40px -8px rgba(110,231,255,.3);}}
.card-indigo .card-tag,.card-indigo .card-cta{{color:#6ee7ff;}}
.card-indigo .card-orb{{background:rgba(110,231,255,.4);}}

.card-gold {{ border-color: rgba(255,211,110,0.15); }}
.card-gold:hover {{ border-color:#ffd36e; box-shadow:0 0 0 1px #ffd36e,0 16px 40px -8px rgba(255,211,110,.3);}}
.card-gold .card-tag,.card-gold .card-cta{{color:#ffd36e;}}
.card-gold .card-orb{{background:rgba(255,211,110,.4);}}

.card-mint {{ border-color: rgba(138,255,193,0.15); }}
.card-mint:hover {{ border-color:#8affc1; box-shadow:0 0 0 1px #8affc1,0 16px 40px -8px rgba(138,255,193,.3);}}
.card-mint .card-tag,.card-mint .card-cta{{color:#8affc1;}}
.card-mint .card-orb{{background:rgba(138,255,193,.4);}}

.card-rose {{ border-color: rgba(255,138,198,0.15); }}
.card-rose:hover {{ border-color:#ff8ac6; box-shadow:0 0 0 1px #ff8ac6,0 16px 40px -8px rgba(255,138,198,.3);}}
.card-rose .card-tag,.card-rose .card-cta{{color:#ff8ac6;}}
.card-rose .card-orb{{background:rgba(255,138,198,.4);}}

.card-skyblue {{ border-color: rgba(110,231,255,0.15); }}
.card-skyblue:hover {{ border-color:#6ee7ff; box-shadow:0 0 0 1px #6ee7ff,0 16px 40px -8px rgba(110,231,255,.3);}}
.card-skyblue .card-tag,.card-skyblue .card-cta{{color:#6ee7ff;}}
.card-skyblue .card-orb{{background:rgba(110,231,255,.4);}}

.card-violet {{ border-color: rgba(180,135,255,0.15); }}
.card-violet:hover {{ border-color:#b487ff; box-shadow:0 0 0 1px #b487ff,0 16px 40px -8px rgba(180,135,255,.3);}}
.card-violet .card-tag,.card-violet .card-cta{{color:#b487ff;}}
.card-violet .card-orb{{background:rgba(180,135,255,.4);}}

.card-cerulean {{ border-color: rgba(56,189,248,0.15); }}
.card-cerulean:hover {{ border-color:#38bdf8; box-shadow:0 0 0 1px #38bdf8,0 16px 40px -8px rgba(56,189,248,.3);}}
.card-cerulean .card-tag,.card-cerulean .card-cta{{color:#38bdf8;}}
.card-cerulean .card-orb{{background:rgba(56,189,248,.4);}}

/* Theme selector */
.theme-row {{
    margin-top: 0.9rem;
    display: flex;
    justify-content: center;
}}
[data-testid="stSelectbox"] > div > div {{
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important; backdrop-filter: blur(10px);
}}
[data-testid="stSelectbox"] label {{
    color: rgba(148,163,184,0.7) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.75rem !important; letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}}
</style>

<div class="stars-bg" id="starsContainer"></div>
<script>
(function() {{
    var c = document.getElementById('starsContainer');
    if (!c) return;
    for (var i = 0; i < 120; i++) {{
        var s = document.createElement('div');
        s.className = 'star';
        var size = Math.random() * 2.5 + 0.5;
        s.style.cssText = 'width:' + size + 'px;height:' + size + 'px;left:' + (Math.random()*100) + '%;top:' + (Math.random()*100) + '%;--dur:' + (Math.random()*3+2) + 's;animation-delay:' + (Math.random()*4) + 's';
        c.appendChild(s);
    }}
}})();
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RENDER ALL IN ONE HTML BLOCK — no scroll
# ═══════════════════════════════════════════════════════════════════════════════
html = """
<div class="launcher-wrap">
  <div class="launcher-header">
    <h1>✦ My App Universe</h1>
    <p>Select an app below to launch your experience</p>
  </div>
  <div class="cards-grid">
"""

for app in APPS:
    html += (
        '<a class="app-card ' + app["css_class"] + '" '
        'href="' + app["url"] + '" target="_blank">'
        '<div class="card-orb"></div>'
        '<div class="card-tag">' + app["tag"] + '</div>'
        '<span class="card-icon">' + app["icon"] + '</span>'
        '<div class="card-name">' + app["name"] + '</div>'
        '<div class="card-desc">' + app["desc"] + '</div>'
        '<div class="card-cta">Launch App '
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M5 12h14M12 5l7 7-7 7"/></svg>'
        '</div>'
        '</a>'
    )

html += '</div></div>'
st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# THEME SELECTOR
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col2:
    chosen = st.selectbox(
        "🎨 Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.selected_theme),
    )
    if chosen != st.session_state.selected_theme:
        st.session_state.selected_theme = chosen
        st.rerun()
