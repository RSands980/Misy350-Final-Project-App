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

# Load appointments
if appointments_path.exists():
    with open(appointments_path, "r") as f:
        appointments = json.load(f)
else:
    appointments = []

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
    
    if st.session_state["user"] is not None:
        if st.button("Logout"):
            st.session_state["user"] = None
            st.session_state["page"] = "login"
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
            st.session_state["page"] = "dashboard"
            st.success("Logged in successfully")
            st.rerun()
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
                st.session_state["page"] = "login"
                st.rerun()

# SIMPLE DASHBOARD (STARTED, NOT FINISHED)
if st.session_state["user"] is not None:
    st.divider()

    user = st.session_state["user"]

    with st.container(border=True):
        st.subheader("Dashboard")
        st.write("Welcome:", user["name"])
        st.write("Role:", user["role"])

        if user["role"] == "Patient":
            st.subheader("Available Appointments")

            for appointment in appointments:
                if appointment["status"] == "available":
                    st.write(
                        "Doctor:", appointment["doctor_email"],
                        "Date:", appointment["date"],
                        "Time:", appointment["time"]
                    )
            available_ids = []
            for appointment in appointments:
                if appointment["status"] == "available":
                    available_ids.append(appointment["appointment_id"])

            if len(available_ids) > 0:
                selected_id = st.selectbox("Select Appointment ID to Book", available_ids)

                if st.button("Book Appointment"):
                    for appointment in appointments:
                        if appointment["appointment_id"] == selected_id:
                            appointment["patient_email"] = user["email"]
                            appointment["status"] = "booked"
                            break

                    with open(appointments_path, "w") as f:
                        json.dump(appointments, f, indent=4)

                    st.success("Appointment booked successfully")
                    st.rerun()

            st.subheader("My Booked Appointments")
            for appointment in appointments:
                if appointment["patient_email"] == user["email"]:
                    st.write(
                        "Doctor:", appointment["doctor_email"],
                        "Date:", appointment["date"],
                        "Time:", appointment["time"],
                        "Status:", appointment["status"]
                    )

                    if st.button(f"Cancel {appointment['appointment_id']}"):
                        appointment["patient_email"] = ""
                        appointment["status"] = "available"

                        with open(appointments_path, "w") as f:
                            json.dump(appointments, f, indent=4)

                        st.success("Appointment cancelled successfully")
                        st.rerun()

        elif user["role"] == "Doctor":
            st.subheader("Create Appointment Slot")
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")
            if st.button("Add Appointment Slot"):
                new_appointment = {
                    "appointment_id": str(len(appointments) + 1),
                    "doctor_email": user["email"],
                    "patient_email": "",
                    "date": str(appointment_date),
                    "time": str(appointment_time),
                    "status": "available"
                 }
                
                appointments.append(new_appointment)

                with open(appointments_path, "w") as f:
                    json.dump(appointments, f, indent=4)

                st.success("Appointment slot added successfully")
                st.rerun()

            st.subheader("Your Appointment Slots")
            for appointment in appointments:
                if appointment["doctor_email"] == user["email"]:
                    st.write(
                        "Date", appointment["date"],
                        "Time", appointment["time"],
                        "Status", appointment["status"]
                    )
                    