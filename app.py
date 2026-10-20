import streamlit as st
import pandas as pd
from datetime import date
from core.db import get_conn
from core.scheduler import make_schedule

st.set_page_config(page_title="StudentOS", page_icon="🎓", layout="wide")
st.title("🎓 StudentOS")
st.write("One platform for your money, your time, and your career.")

conn = get_conn()

# ---------- Card 1: spending ----------
exp = pd.read_sql("SELECT * FROM expenses", conn)
total_spent = exp["amount"].sum() if not exp.empty else 0
top_cat = exp.groupby("category")["amount"].sum().idxmax() if not exp.empty else "None"

# ---------- Card 2: today's study hours ----------
tasks_df = pd.read_sql("SELECT * FROM tasks", conn)
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

# ---------- Card 3: task progress ----------
total_tasks = len(tasks_df)
done_tasks = int(tasks_df["done"].sum()) if total_tasks else 0

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total spent", f"₹{total_spent:,.0f}", f"Top: {top_cat}", delta_color="off")
c2.metric("📅 Study hours today", f"{today_hours:g} h", "at 4 h/day", delta_color="off")
c3.metric("🧭 Tasks completed", f"{done_tasks} / {total_tasks}")

st.divider()
st.subheader("What would you like to do?")
st.write("Use the sidebar to open a module:")
st.markdown(
    "- **Expenses**: track and categorize your spending\n"
    "- **Timetable**: plan your study schedule\n"
    "- **Career Roadmap**: find skill gaps and add learning to your timetable"
)