import streamlit as st
import json
from pathlib import Path
import time

st.set_page_config(page_title="ClinicConnect", layout="wide")

# file paths
users_path = Path("users.json")
appointments_path = Path("appointments.json")

# load users
if users_path.exists():
    with open(users_path, "r") as f:
        users = json.load(f)
else:
    users = []

# session state
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = None

# sidebar
with st.sidebar:
    if st.button("Login"):
        st.session_state["page"] = "login"
        st.rerun()

    if st.button("Register"):
        st.session_state["page"] = "register"
        st.rerun()

# LOGIN PAGE
if st.session_state["page"] == "login":
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with st.spinner("Logging in..."):
            time.sleep(1)

            found_user = None
            for u in users:
                if u["email"] == email and u["password"] == password:
                    found_user = u
                    break

        if found_user is not None:
            st.session_state["user"] = found_user
            st.success("Logged in successfully")
        else:
            st.error("Invalid email or password")

# REGISTER PAGE
elif st.session_state["page"] == "register":
    st.title("Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Patient", "Doctor"])

    if st.button("Register"):
        if name == "" or email == "" or password == "":
            st.warning("Please fill in all fields")
        else:
            email_exists = False
            for u in users:
                if u["email"] == email:
                    email_exists = True
                    break

            if email_exists:
                st.error("Email already exists")
            else:
                with st.spinner("Creating account..."):
                    time.sleep(1)

                    new_user = {
                        "user_id": str(len(users) + 1),
                        "name": name,
                        "email": email,
                        "password": password,
                        "role": role
                    }

                    users.append(new_user)

                    with open(users_path, "w") as f:
                        json.dump(users, f, indent=4)

                st.success("Account created successfully")

# SIMPLE DASHBOARD (STARTED, NOT FINISHED)
if st.session_state["user"] is not None:
    st.divider()

    user = st.session_state["user"]

    st.subheader("Dashboard")
    st.write("Welcome:", user["name"])
    st.write("Role:", user["role"])

    if user["role"] == "Patient":
        st.write("Patient features coming next")

    elif user["role"] == "Doctor":
        st.write("Doctor features coming next")