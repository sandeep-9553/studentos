import hashlib
import os
import streamlit as st
from core.db import get_conn
from core.ui import inject_css


def _hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 100_000
    ).hex()


def create_user(username, password):
    conn = get_conn()
    if conn.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
        return False
    salt = os.urandom(16).hex()
    conn.execute(
        "INSERT INTO users(username, salt, password_hash) VALUES (?,?,?)",
        (username, salt, _hash(password, salt)),
    )
    conn.commit()
    return True


def check_login(username, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, salt, password_hash FROM users WHERE username=?", (username,)
    ).fetchone()
    if row and _hash(password, row[1]) == row[2]:
        return row[0]
    return None


def login_form():
    left, mid, right = st.columns([1, 1.4, 1])
    with mid:
        tab1, tab2 = st.tabs(["Log in", "Sign up"])
        with tab1:
            u = st.text_input("Username", key="login_user")
            p = st.text_input("Password", type="password", key="login_pass")
            if st.button("Log in"):
                uid = check_login(u.strip(), p)
                if uid:
                    st.session_state["user_id"] = uid
                    st.session_state["username"] = u.strip()
                    st.rerun()
                else:
                    st.error("Wrong username or password")
        with tab2:
            u2 = st.text_input("Choose a username", key="signup_user")
            p2 = st.text_input("Choose a password (min 6 characters)",
                               type="password", key="signup_pass")
            if st.button("Create account"):
                if len(u2.strip()) < 3 or len(p2) < 6:
                    st.warning("Username needs 3+ characters and password 6+")
                elif create_user(u2.strip(), p2):
                    st.success("Account created. Now log in from the Log in tab.")
                else:
                    st.error("That username is already taken")


def require_login():
    """Call at the top of every page. Stops the page until the user logs in."""
    inject_css()
    if "user_id" in st.session_state:
        st.sidebar.write(f"👤 Logged in as **{st.session_state['username']}**")
        if st.sidebar.button("Log out"):
            st.session_state.clear()
            st.rerun()
        return st.session_state["user_id"]

    st.markdown('<div class="brand">🎓 StudentOS</div><hr class="nav-line">',
                unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Please log in to continue.</h2>',
                unsafe_allow_html=True)
    login_form()
    st.stop()