import streamlit as st
import pandas as pd
from datetime import date, timedelta
from core.db import get_conn
from core.scheduler import make_schedule

st.title("📅 Smart Timetable Planner")
conn = get_conn()

# ---------- Add a task ----------
st.subheader("Add a task")
c1, c2, c3, c4 = st.columns(4)
subject = c1.text_input("Subject")
deadline = c2.date_input("Deadline", date.today() + timedelta(days=3))
priority = c3.selectbox("Priority", ["High", "Medium", "Low"])
hours = c4.number_input("Hours needed", min_value=0.5, value=4.0, step=0.5)

if st.button("Add task"):
    name = subject.strip()
    exists = conn.execute(
        "SELECT 1 FROM tasks WHERE subject=? AND done=0", (name,)
    ).fetchone()
    if not name:
        st.warning("Enter a subject name")
    elif exists:
        st.warning("A pending task with this name already exists. Use a different name.")
    else:
        conn.execute(
            "INSERT INTO tasks(subject, deadline, priority, hours_needed) VALUES (?,?,?,?)",
            (name, str(deadline), priority, hours),
        )
        conn.commit()
        st.success("Task added")
        st.rerun()

# ---------- Sample data / Clear ----------
b1, b2 = st.columns(2)

if b1.button("Load sample tasks"):
    today = date.today()
    samples = [
        ("DSA", today + timedelta(days=1), "High", 4),
        ("Python", today + timedelta(days=3), "Medium", 5),
        ("Computer Networks", today + timedelta(days=5), "Medium", 6),
        ("Cloud Computing", today + timedelta(days=7), "High", 8),
    ]
    for s, d, p, h in samples:
        conn.execute(
            "INSERT INTO tasks(subject, deadline, priority, hours_needed) VALUES (?,?,?,?)",
            (s, str(d), p, h),
        )
    conn.commit()
    st.rerun()

if b2.button("Clear all tasks"):
    conn.execute("DELETE FROM tasks")
    conn.commit()
    st.rerun()

# ---------- Task list ----------
st.subheader("Your tasks")
df = pd.read_sql("SELECT * FROM tasks ORDER BY deadline", conn)

if df.empty:
    st.info("No tasks yet. Add one above or click 'Load sample tasks'.")
    st.stop()

df["done"] = df["done"].astype(bool)

edited = st.data_editor(
    df,
    use_container_width=True,
    disabled=["id", "subject", "deadline", "priority", "hours_needed"],
    column_config={"done": st.column_config.CheckboxColumn("Done")},
    key="task_editor",
)

if st.button("Save progress"):
    for _, row in edited.iterrows():
        conn.execute("UPDATE tasks SET done=? WHERE id=?",
                     (int(row["done"]), int(row["id"])))
    conn.commit()
    st.success("Progress saved")
    st.rerun()

done_count = int(df["done"].sum())
st.progress(done_count / len(df))
st.caption(f"{done_count} of {len(df)} tasks completed")

# ---------- Generate schedule ----------
st.subheader("Your study schedule")
hours_per_day = st.slider("Hours available per day", 1.0, 10.0, 4.0, 0.5)

pending = df[~df["done"]]

if pending.empty:
    st.success("🎉 All tasks completed!")
    st.stop()

tasks = []
for _, r in pending.iterrows():
    tasks.append({
        "subject": r["subject"],
        "deadline": pd.to_datetime(r["deadline"]).date(),
        "priority": r["priority"],
        "hours_needed": r["hours_needed"],
    })

# warn about deadlines that already passed
for t in tasks:
    if t["deadline"] < date.today():
        st.error(f"⚠️ The deadline for {t['subject']} has already passed.")

plan, unscheduled = make_schedule(tasks, hours_per_day)

if unscheduled:
    for subj, left in unscheduled.items():
        st.warning(
            f"Not enough time for {subj}: {left:g} hours left unscheduled. "
            "Increase daily hours or move the deadline."
        )

if plan:
    plan_df = pd.DataFrame(plan)

    today_plan = plan_df[plan_df["date"] == date.today()]
    st.markdown("**📌 Today's plan**")
    if today_plan.empty:
        st.write("Nothing scheduled for today.")
    else:
        for _, r in today_plan.iterrows():
            st.write(f"- {r['subject']}: {r['hours']:g} hours")

    st.markdown("**Full schedule (you can edit the hours)**")
    st.data_editor(plan_df, use_container_width=True,
                   disabled=["date", "subject"], key="plan_editor")

    st.markdown("**Study hours per day**")
    per_day = plan_df.groupby("date")["hours"].sum()
    st.bar_chart(per_day)