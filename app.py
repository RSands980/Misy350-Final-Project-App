import streamlit as st
import time

from data_store import DataStore
from services import AuthService, AppointmentService


st.set_page_config(page_title="ClinicConnect", layout="wide")

# Data/service setup
store = DataStore()
users = store.load_users()
appointments = store.load_appointments()

auth_service = AuthService(users)
appointment_service = AppointmentService(appointments)


# Session state setup
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = None


# Sidebar navigation
with st.sidebar:
    st.title("ClinicConnect")

    if st.button("Login", key="sidebar_login_btn"):
        st.session_state["page"] = "login"
        st.session_state["user"] = None
        st.rerun()

    if st.button("Register", key="sidebar_register_btn"):
        st.session_state["page"] = "register"
        st.session_state["user"] = None
        st.rerun()

    if st.session_state["user"] is not None:
        st.divider()
        st.write("Logged in as:")
        st.write(st.session_state["user"]["name"])

        if st.button("Logout", key="sidebar_logout_btn"):
            st.session_state["user"] = None
            st.session_state["page"] = "login"
            st.rerun()


# Login page
if st.session_state["page"] == "login":
    st.title("Login")

    with st.container(border=True):
        st.subheader("Test Accounts")
        st.write("Patient: patient@test.com / patient123")
        st.write("Doctor: doctor@test.com / doctor123")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_submit_btn"):
        with st.spinner("Logging in..."):
            time.sleep(1)
            found_user = auth_service.validate_login(email, password)

        if found_user is not None:
            st.session_state["user"] = found_user
            st.session_state["page"] = "dashboard"
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid email or password")


# Register page
elif st.session_state["page"] == "register":
    st.title("Register")

    name = st.text_input("Name", key="register_name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    role = st.selectbox("Role", ["Patient", "Doctor"], key="register_role")

    if st.button("Register", key="register_submit_btn"):
        with st.spinner("Creating account..."):
            time.sleep(1)
            result = auth_service.register_user(name, email, password, role)

            if result["success"]:
                store.save_users(users)
                st.success(result["message"])
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error(result["message"])


# Dashboard pages
if st.session_state["user"] is not None:
    user = st.session_state["user"]

    with st.container(border=True):
        if user["role"] == "Patient":
            st.title("Patient Dashboard")
        elif user["role"] == "Doctor":
            st.title("Doctor Dashboard")

        st.write("Welcome:", user["name"])
        st.write("Role:", user["role"])
        st.divider()

        # Patient dashboard
        if user["role"] == "Patient":
            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader("Available Appointments")

                    available_appointments = appointment_service.get_available_appointments()
                    available_ids = []

                    for appointment in available_appointments:
                        st.write(
                            "Appointment ID:", appointment["appointment_id"],
                            "Doctor:", appointment["doctor_email"],
                            "Date:", appointment["date"],
                            "Time:", appointment["time"]
                        )
                        available_ids.append(appointment["appointment_id"])

                    if len(available_ids) > 0:
                        selected_id = st.selectbox(
                            "Select Appointment ID to Book",
                            available_ids,
                            key="appointment_select"
                        )

                        if st.button("Book Appointment", key="book_appointment_btn"):
                            result = appointment_service.book_appointment(
                                selected_id,
                                user["email"]
                            )

                            if result["success"]:
                                store.save_appointments(appointments)
                                st.success(result["message"])
                                st.rerun()
                            else:
                                st.error(result["message"])
                    else:
                        st.write("No available appointments")

            with col2:
                with st.container(border=True):
                    st.subheader("My Booked Appointments")

                    patient_appointments = appointment_service.get_patient_appointments(
                        user["email"]
                    )

                    if len(patient_appointments) == 0:
                        st.write("No booked appointments")

                    for appointment in patient_appointments:
                        st.write(
                            "Doctor:", appointment["doctor_email"],
                            "Date:", appointment["date"],
                            "Time:", appointment["time"],
                            "Status:", appointment["status"]
                        )

                        if st.button(
                            f"Cancel {appointment['appointment_id']}",
                            key=f"cancel_{appointment['appointment_id']}"
                        ):
                            result = appointment_service.cancel_appointment(
                                appointment["appointment_id"],
                                user["email"]
                            )

                            if result["success"]:
                                store.save_appointments(appointments)
                                st.success(result["message"])
                                st.rerun()
                            else:
                                st.error(result["message"])

        # Doctor dashboard
        elif user["role"] == "Doctor":
            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader("Create Appointment Slot")

                    appointment_date = st.date_input(
                        "Appointment Date",
                        key="appointment_date"
                    )
                    appointment_time = st.time_input(
                        "Appointment Time",
                        key="appointment_time"
                    )

                    if st.button("Add Appointment Slot", key="add_appointment_slot_btn"):
                        result = appointment_service.create_appointment_slot(
                            user["email"],
                            appointment_date,
                            appointment_time
                        )

                        if result["success"]:
                            store.save_appointments(appointments)
                            st.success(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])

                st.divider()

                with st.container(border=True):
                    st.subheader("Booked Appointments")

                    booked_appointments = appointment_service.get_doctor_booked_appointments(
                        user["email"]
                    )

                    if len(booked_appointments) == 0:
                        st.write("No booked appointments")

                    for appointment in booked_appointments:
                        st.write(
                            "Patient:", appointment["patient_email"],
                            "Date:", appointment["date"],
                            "Time:", appointment["time"]
                        )

            with col2:
                with st.container(border=True):
                    st.subheader("Your Appointment Slots")

                    doctor_appointments = appointment_service.get_doctor_appointments(
                        user["email"]
                    )

                    if len(doctor_appointments) == 0:
                        st.write("No appointment slots yet")

                    for appointment in doctor_appointments:
                        st.write(
                            "Date:", appointment["date"],
                            "Time:", appointment["time"],
                            "Status:", appointment["status"]
                        )

                        if st.button(
                            f"Delete {appointment['appointment_id']}",
                            key=f"delete_{appointment['appointment_id']}"
                        ):
                            result = appointment_service.delete_appointment_slot(
                                appointment["appointment_id"],
                                user["email"]
                            )

                            if result["success"]:
                                store.save_appointments(appointments)
                                st.success(result["message"])
                                st.rerun()
                            else:
                                st.error(result["message"])