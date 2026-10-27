import streamlit as st
import pandas as pd
from datetime import date
from core.db import get_conn
from core.auth import require_login, login_form
from core.scheduler import make_schedule
from core.ui import inject_css, navbar, landing_html, footer

st.set_page_config(page_title="StudentOS", page_icon="🎓", layout="wide")
inject_css()

# ---------- Visitors who are not logged in see the landing page ----------
if "user_id" not in st.session_state:
    st.markdown(landing_html(), unsafe_allow_html=True)
    login_form()
    footer()
    st.stop()

user_id = require_login()
navbar()

st.markdown('<div class="eyebrow">Your dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<h1 class="hero-title" style="font-size:3rem">Welcome back, '
            f'<em>{st.session_state["username"]}.</em></h1>', unsafe_allow_html=True)
st.write("")

conn = get_conn()

exp = pd.read_sql("SELECT * FROM expenses WHERE user_id=?", conn, params=(user_id,))
total_spent = exp["amount"].sum() if not exp.empty else 0
top_cat = exp.groupby("category")["amount"].sum().idxmax() if not exp.empty else "None"

tasks_df = pd.read_sql("SELECT * FROM tasks WHERE user_id=?", conn, params=(user_id,))
today_hours = 0.0
if not tasks_df.empty:
    pending = tasks_df[tasks_df["done"] == 0]
    tasks = [{
        "subject": r["subject"],
        "deadline": pd.to_datetime(r["deadline"]).date(),
        "priority": r["priority"],
        "hours_needed": r["hours_needed"],
    } for _, r in pending.iterrows()]
    if tasks:
        plan, _ = make_schedule(tasks, 4)
        today_hours = sum(p["hours"] for p in plan if p["date"] == date.today())

total_tasks = len(tasks_df)
done_tasks = int(tasks_df["done"].sum()) if total_tasks else 0

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total spent", f"₹{total_spent:,.0f}", f"Top: {top_cat}", delta_color="off")
c2.metric("📅 Study hours today", f"{today_hours:g} h", "at 4 h/day", delta_color="off")
c3.metric("🧭 Tasks completed", f"{done_tasks} / {total_tasks}")

st.write("")
st.markdown('<h2 class="section-title">Open a module</h2>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.markdown("### 💰 Expenses")
        st.write("Track and categorize your spending.")
        st.page_link("pages/1_Expenses.py", label="Open Expenses →")
with m2:
    with st.container(border=True):
        st.markdown("### 📅 Timetable")
        st.write("Plan your study schedule around deadlines.")
        st.page_link("pages/2_Timetable.py", label="Open Timetable →")
with m3:
    with st.container(border=True):
        st.markdown("### 🧭 Career Roadmap")
        st.write("Find skill gaps and add learning to your timetable.")
        st.page_link("pages/3_Career_Roadmap.py", label="Open Roadmap →")

footer()