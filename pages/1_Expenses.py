import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from core.db import get_conn
from core.auth import require_login
from core.categorizer import categorize
from core.ui import navbar

user_id = require_login()
navbar()  

st.title("💰 Expense Organizer")
conn = get_conn()

categories = ["Food", "Travel", "Shopping", "Recharge/Bills",
              "Education", "Entertainment", "Others"]

# ---------- Add one expense ----------
st.subheader("Add an expense")
c1, c2, c3 = st.columns(3)
exp_date = c1.date_input("Date", date.today())
desc = c2.text_input("Description")
amount = c3.number_input("Amount (₹)", min_value=0.0, step=10.0)

if st.button("Add expense"):
    if desc.strip() and amount > 0:
        conn.execute(
            "INSERT INTO expenses(user_id, date, description, amount, category) VALUES (?,?,?,?,?)",
            (user_id, str(exp_date), desc, amount, categorize(desc)),
        )
        conn.commit()
        st.success("Expense added")
    else:
        st.warning("Enter a description and an amount greater than 0")

# ---------- Load sample data / Clear data ----------
b1, b2 = st.columns(2)

if b1.button("Load sample data"):
    sample = pd.read_csv("data/sample_expenses.csv")
    for _, row in sample.iterrows():
        conn.execute(
            "INSERT INTO expenses(user_id, date, description, amount, category) VALUES (?,?,?,?,?)",
            (user_id, row["date"], row["description"], row["amount"],
             categorize(row["description"])),
        )
    conn.commit()
    st.success("Sample data loaded")

if b2.button("Clear all expenses"):
    conn.execute("DELETE FROM expenses WHERE user_id=?", (user_id,))
    conn.commit()
    st.rerun()

# ---------- Show all expenses ----------
st.subheader("Your expenses")
df = pd.read_sql(
    "SELECT id, date, description, amount, category FROM expenses "
    "WHERE user_id=? ORDER BY date DESC",
    conn, params=(user_id,),
)

if df.empty:
    st.info("No expenses yet. Add one above or click 'Load sample data'.")
else:
    edited = st.data_editor(
        df,
        use_container_width=True,
        disabled=["id", "date", "description", "amount"],
        column_config={
            "category": st.column_config.SelectboxColumn("category", options=categories)
        },
        key="expense_editor",
    )

    if st.button("Save category changes"):
        for _, row in edited.iterrows():
            conn.execute("UPDATE expenses SET category=? WHERE id=? AND user_id=?",
                         (row["category"], int(row["id"]), user_id))
        conn.commit()
        st.success("Categories saved")
        st.rerun()

    st.metric("Total spent", f"₹{df['amount'].sum():,.0f}")

    # ---------- Charts and insight ----------
    by_cat = df.groupby("category")["amount"].sum().reset_index()

    left, right = st.columns(2)
    with left:
        st.subheader("Spending by category")
        fig = px.pie(by_cat, names="category", values="amount")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Amount per category")
        fig2 = px.bar(by_cat, x="category", y="amount")
        st.plotly_chart(fig2, use_container_width=True)

    top_row = by_cat.loc[by_cat["amount"].idxmax()]
    pct = top_row["amount"] / by_cat["amount"].sum() * 100
    st.info(f"💡 {top_row['category']} is {pct:.0f}% of your spending.")

    # ---------- Budget ----------
    st.subheader("Monthly budget")
    budget = st.number_input("Set your monthly budget (₹)", min_value=0.0,
                             value=3000.0, step=100.0)
    total = df["amount"].sum()
    st.progress(min(total / budget, 1.0) if budget > 0 else 0.0)

    if budget > 0 and total > budget:
        st.error(f"⚠️ Over budget by ₹{total - budget:,.0f}")
    elif budget > 0 and total > 0.8 * budget:
        st.warning(f"You have used {total / budget * 100:.0f}% of your budget")
    elif budget > 0:
        st.success(f"You are within budget. ₹{budget - total:,.0f} left")