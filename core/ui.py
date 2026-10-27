import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=DM+Sans:wght@400;500;600&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F8F6F1; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1180px; padding-top: 1.5rem; }

h1, h2, h3, .serif {
    font-family: 'Fraunces', serif !important;
    color: #1B3D33; letter-spacing: -0.02em;
}
.brand { font-family: 'Fraunces', serif; font-size: 1.35rem; font-weight: 600; color: #1D5545; }
.nav-line { border: none; border-top: 1px solid #E4E1D6; margin: 0.5rem 0 2rem; }

.eyebrow {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: #A4583B; margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Fraunces', serif; font-weight: 600; color: #1B3D33;
    font-size: clamp(2.8rem, 6vw, 5rem); line-height: 1.02; letter-spacing: -0.03em; margin: 0;
}
.hero-title em { color: #1D5545; font-style: italic; font-weight: 500; }
.lead { font-size: 1.1rem; color: #5C6F66; line-height: 1.7; max-width: 34rem; margin-top: 1.2rem; }
.section-title {
    font-family: 'Fraunces', serif; font-weight: 600; color: #1B3D33;
    font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.08; margin: 0 0 1rem;
}
.section-title em { color: #6E8B7D; font-style: italic; font-weight: 500; }

.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin: 2rem 0 3rem; }
.card { background: #FCFBF7; border: 1px solid #E8E5DA; border-radius: 28px; padding: 1.6rem 1.6rem 2rem; }
.card .num { font-size: 0.75rem; color: #8A978F; letter-spacing: 0.1em; }
.card .tag { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #A4583B; margin: 2.2rem 0 0.5rem; }
.card h3 { font-size: 1.6rem; line-height: 1.15; margin: 0 0 0.7rem; }
.card p { color: #5C6F66; font-size: 0.95rem; line-height: 1.65; margin: 0; }
.card .dot { float: right; width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; font-size: 1.2rem; }

.dark { background: #1D4D40; border-radius: 32px; padding: 3rem; display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-bottom: 3rem; }
.dark .eyebrow { color: #E3EC62; }
.dark .section-title { color: #F8F6F1; }
.dark .section-title em { color: #E3EC62; }
.dark p, .dark .item p { color: #CFE0D8; line-height: 1.65; }
.dark .item { border-top: 1px solid rgba(255,255,255,0.18); padding: 1.1rem 0; }
.dark .item h4 { font-family: 'Fraunces', serif; color: #F8F6F1; font-size: 1.25rem; margin: 0 0 0.3rem; }
.dark .item p { font-size: 0.9rem; margin: 0; }

.center { text-align: center; padding: 1rem 0 2rem; }
.footer { border-top: 1px solid #E4E1D6; padding: 1.5rem 0; color: #8A978F; font-size: 0.85rem; text-align: center; }

.stButton > button, .stFormSubmitButton > button {
    border-radius: 999px; background: #1D5545; color: #fff; border: none;
    padding: 0.55rem 1.6rem; font-weight: 600;
}
.stButton > button:hover { background: #164236; color: #fff; }
[data-testid="stMetric"] { background: #FCFBF7; border: 1px solid #E8E5DA; border-radius: 22px; padding: 1rem 1.3rem; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 24px; background: #FCFBF7; }
a[data-testid="stPageLink-NavLink"] { border-radius: 999px; }

@media (max-width: 800px) {
    .cards, .dark { grid-template-columns: 1fr; }
    .dark { padding: 1.8rem; }
}
</style>
"""

HERO_SVG = """
<svg viewBox="0 0 480 480" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:460px">
<circle cx="240" cy="240" r="230" fill="#EDEEDD"/>
<circle cx="240" cy="240" r="130" fill="none" stroke="#D5D8C4" stroke-dasharray="4 6"/>
<circle cx="240" cy="240" r="85" fill="#1D5545"/>
<circle cx="215" cy="215" r="38" fill="#E3EC62"/>
<circle cx="150" cy="130" r="14" fill="#D9B8F0"/>
<circle cx="372" cy="160" r="13" fill="#E8895B"/>
<circle cx="260" cy="382" r="22" fill="#D5E04F"/>
<circle cx="125" cy="260" r="8" fill="#4A7D6B"/>
<polygon points="330,95 340,120 366,122 346,138 353,163 330,149 307,163 314,138 294,122 320,120" fill="#E3EC62"/>
</svg>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def set_background(*args, **kwargs):
    """Kept so older page code still works. The new style replaces pictures."""
    inject_css()


def navbar():
    c0, c1, c2, c3, c4 = st.columns([2.2, 1, 1, 1, 1.4])
    c0.markdown('<div class="brand">🎓 StudentOS</div>', unsafe_allow_html=True)
    c1.page_link("app.py", label="Home")
    c2.page_link("pages/1_Expenses.py", label="Expenses")
    c3.page_link("pages/2_Timetable.py", label="Timetable")
    c4.page_link("pages/3_Career_Roadmap.py", label="Career Roadmap")
    st.markdown('<hr class="nav-line">', unsafe_allow_html=True)


def landing_html():
    return f"""
<div class="brand" style="margin-bottom:0.5rem">🎓 StudentOS</div>
<hr class="nav-line">
<div style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:2rem;align-items:center;margin-bottom:3rem">
<div>
<div class="eyebrow">● A student toolkit, in one place</div>
<h1 class="hero-title">Plan smarter.<br><em>Study calmer.</em></h1>
<p class="lead">StudentOS brings your study timetable, career roadmap and daily spending together, so it is easier to see your next step and make it your own.</p>
<p style="color:#8A978F;font-size:0.85rem;margin-top:1.5rem">Made for student life in India. Scroll down to log in or sign up.</p>
</div>
<div style="text-align:center">{HERO_SVG}</div>
</div>
<div class="eyebrow">The toolkit</div>
<h2 class="section-title">Three parts of life.<br><em>One place to begin.</em></h2>
<div class="cards">
<div class="card"><span class="dot" style="background:#DCEBE2">📅</span><div class="num">01</div><div class="tag">Study timetable</div><h3>A study plan that fits your day</h3><p>Add subjects, deadlines and the hours you have. The planner schedules the most urgent work first and warns you when time is short.</p></div>
<div class="card"><span class="dot" style="background:#EBDFF5">🧭</span><div class="num">02</div><div class="tag">Career roadmap</div><h3>A next step for the path you choose</h3><p>Pick a role and the skills you know. Get staged milestones, practice projects and resources, then add them to your timetable.</p></div>
<div class="card"><span class="dot" style="background:#F9E1D4">💰</span><div class="num">03</div><div class="tag">Expense organizer</div><h3>A clearer picture of everyday spending</h3><p>Record expenses, review the categories and set a monthly budget. Charts and a short insight show where your money goes.</p></div>
</div>
<div class="dark">
<div>
<div class="eyebrow">Simple rules you can check</div>
<h2 class="section-title">Clear logic.<br><em>Always editable.</em></h2>
<p>StudentOS uses plain, explainable rules instead of black boxes. You can review every result and change it.</p>
</div>
<div>
<div class="item"><h4>Categories you can correct</h4><p>Expenses are sorted by keywords, and you can change any category.</p></div>
<div class="item"><h4>Plans stay practical</h4><p>Schedules are checked against the hours you have, and the app warns you if a plan is not possible.</p></div>
<div class="item"><h4>Goals become tasks</h4><p>A career roadmap can be added to your timetable in one click.</p></div>
</div>
</div>
<div class="center">
<div class="eyebrow">Ready when you are</div>
<h2 class="section-title">Log in or create an account.</h2>
</div>
"""


def footer():
    st.markdown('<div class="footer">🎓 StudentOS · Thoughtfully made for student life in India</div>',
                unsafe_allow_html=True)