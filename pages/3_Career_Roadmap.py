import streamlit as st
import pandas as pd
from datetime import date, timedelta
from core.db import get_conn
from core.roadmap import load_roles, build_roadmap

st.title("🧭 Career Roadmap Generator")
conn = get_conn()
roles = load_roles()

# ---------- Choose role and current skills ----------
role = st.selectbox("Target role", list(roles.keys()))

# all skills that appear in this role, so the user can tick what they know
role_skills = [s["skill"] for s in roles[role]]
current = st.multiselect("Skills you already have", role_skills)

missing, known = build_roadmap(role, current, roles)

# ---------- Progress ----------
total = len(roles[role])
st.progress(len(known) / total)
st.caption(f"You already know {len(known)} of {total} skills for {role}")

# ---------- Roadmap ----------
st.subheader(f"Your roadmap to become a {role}")

if not missing:
    st.success("🎉 You already have all the skills for this role!")
    st.stop()

rows = []
for i, s in enumerate(missing, start=1):
    rows.append({
        "Stage": i,
        "Skill": s["skill"],
        "Resource": s["resource"],
        "Practice project": s["project"],
        "Hours": s["hours"],
    })
road_df = pd.DataFrame(rows)
st.dataframe(road_df, use_container_width=True, hide_index=True)

st.info(f"Estimated total study time: {road_df['Hours'].sum()} hours")

# ---------- Send roadmap to the timetable ----------
st.subheader("Add this roadmap to your timetable")
days_per_skill = st.number_input(
    "Days you want to give each skill", min_value=1, value=3, step=1
)

if st.button("Add roadmap to my timetable"):
    added = 0
    skipped = 0
    deadline = date.today()
    for s in missing:
        deadline = deadline + timedelta(days=int(days_per_skill))
        name = f"{role}: {s['skill']}"
        exists = conn.execute(
            "SELECT 1 FROM tasks WHERE subject=? AND done=0", (name,)
        ).fetchone()
        if exists:
            skipped += 1
            continue
        conn.execute(
            "INSERT INTO tasks(subject, deadline, priority, hours_needed) VALUES (?,?,?,?)",
            (name, str(deadline), "Medium", s["hours"]),
        )
        added += 1
    conn.commit()
    st.success(f"Added {added} skills to your timetable. Skipped {skipped} already added.")
    st.caption("Open the Timetable page to see them scheduled.")