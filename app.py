import streamlit as st
import time
from datetime import datetime

from data_store import DataStore
from services import AuthService, AppointmentService
from ai_assistant import ClinicAIAssistant


st.set_page_config(page_title="ClinicConnect", layout="wide")


def format_time(time_value):
    try:
        parsed_time = datetime.strptime(time_value, "%H:%M:%S")
        return parsed_time.strftime("%I:%M %p").lstrip("0")
    except ValueError:
        try:
            parsed_time = datetime.strptime(time_value, "%H:%M")
            return parsed_time.strftime("%I:%M %p").lstrip("0")
        except ValueError:
            return time_value


def get_time_options():
    times = []

    for hour in range(8, 19):
        for minute in [0, 15, 30, 45]:
            if hour == 18 and minute > 0:
                continue

            time_24 = f"{hour:02d}:{minute:02d}:00"
            time_display = format_time(time_24)
            times.append((time_display, time_24))

    return times


def show_message(result):
    if result["success"]:
        st.success(result["message"])
        time.sleep(1)
    else:
        st.error(result["message"])


def show_appointment_card(appointment, show_patient=False, show_doctor=False):
    with st.container(border=True):
        st.write("Appointment ID:", appointment["appointment_id"])

        if show_doctor:
            st.write("Doctor:", appointment["doctor_email"])

        if show_patient:
            st.write("Patient:", appointment["patient_email"])

        st.write("Date:", appointment["date"])
        st.write("Time:", format_time(appointment["time"]))
        st.write("Status:", appointment["status"].title())


def show_ai_assistant(user):
    st.divider()

    with st.container(border=True):
        st.subheader("ClinicConnect AI Assistant")

        if user["role"] == "Patient":
            st.write("Ask about preparing for appointments, what to bring, or how to use the app.")
            default_question = "What should I bring to my appointment?"
        else:
            st.write("Ask for help summarizing notes or thinking of follow-up questions.")
            default_question = "Suggest follow-up questions for a patient appointment."

        question = st.text_area(
            "Ask the assistant a question",
            value=default_question,
            key=f"ai_question_{user['role']}"
        )

        if st.button("Ask AI Assistant", key=f"ask_ai_{user['role']}"):
            with st.spinner("Thinking..."):
                result = ai_assistant.get_response(user["role"], question)

            if result["success"]:
                st.success("AI response generated.")
                st.write(result["message"])
            else:
                st.warning(result["message"])


# Data/service setup
store = DataStore()
users = store.load_users()
appointments = store.load_appointments()

auth_service = AuthService(users)
appointment_service = AppointmentService(appointments)
ai_assistant = ClinicAIAssistant()


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
            st.success("Logged in successfully.")
            time.sleep(1)
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
                time.sleep(1)
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

                    if len(available_appointments) == 0:
                        st.write("No available appointments")

                    for appointment in available_appointments:
                        show_appointment_card(appointment, show_doctor=True)
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

                            show_message(result)

                            if result["success"]:
                                store.save_appointments(appointments)
                                st.rerun()

            with col2:
                with st.container(border=True):
                    st.subheader("My Active Appointments")

                    active_appointments = appointment_service.get_patient_active_appointments(
                        user["email"]
                    )

                    if len(active_appointments) == 0:
                        st.write("No active appointments")

                    for appointment in active_appointments:
                        show_appointment_card(appointment, show_doctor=True)

                        if st.button(
                            f"Cancel {appointment['appointment_id']}",
                            key=f"cancel_{appointment['appointment_id']}"
                        ):
                            result = appointment_service.cancel_appointment(
                                appointment["appointment_id"],
                                user["email"]
                            )

                            show_message(result)

                            if result["success"]:
                                store.save_appointments(appointments)
                                st.rerun()

                st.divider()

                with st.container(border=True):
                    st.subheader("Completed Appointment History")

                    completed_appointments = appointment_service.get_patient_completed_appointments(
                        user["email"]
                    )

                    if len(completed_appointments) == 0:
                        st.write("No completed appointments yet")

                    for appointment in completed_appointments:
                        show_appointment_card(appointment, show_doctor=True)

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

                    time_options = get_time_options()
                    time_labels = []

                    for label, value in time_options:
                        time_labels.append(label)

                    selected_time_label = st.selectbox(
                        "Appointment Time",
                        time_labels,
                        key="appointment_time"
                    )

                    appointment_time = ""

                    for label, value in time_options:
                        if label == selected_time_label:
                            appointment_time = value
                            break

                    if st.button("Add Appointment Slot", key="add_appointment_slot_btn"):
                        result = appointment_service.create_appointment_slot(
                            user["email"],
                            appointment_date,
                            appointment_time
                        )

                        show_message(result)

                        if result["success"]:
                            store.save_appointments(appointments)
                            st.rerun()

                st.divider()

                with st.container(border=True):
                    st.subheader("Booked Appointments")

                    booked_appointments = appointment_service.get_doctor_booked_appointments(
                        user["email"]
                    )

                    if len(booked_appointments) == 0:
                        st.write("No booked appointments")

                    for appointment in booked_appointments:
                        show_appointment_card(appointment, show_patient=True)

                        if st.button(
                            f"Mark Completed {appointment['appointment_id']}",
                            key=f"complete_{appointment['appointment_id']}"
                        ):
                            result = appointment_service.complete_appointment(
                                appointment["appointment_id"],
                                user["email"]
                            )

                            show_message(result)

                            if result["success"]:
                                store.save_appointments(appointments)
                                st.rerun()

                st.divider()

                with st.container(border=True):
                    st.subheader("Completed Appointment History")

                    completed_appointments = appointment_service.get_doctor_completed_appointments(
                        user["email"]
                    )

                    if len(completed_appointments) == 0:
                        st.write("No completed appointments yet")

                    for appointment in completed_appointments:
                        show_appointment_card(appointment, show_patient=True)

            with col2:
                with st.container(border=True):
                    st.subheader("Your Appointment Slots")

                    doctor_appointments = appointment_service.get_doctor_appointments(
                        user["email"]
                    )

                    if len(doctor_appointments) == 0:
                        st.write("No appointment slots yet")

                    for appointment in doctor_appointments:
                        show_appointment_card(appointment)

                        if appointment["status"] == "available":
                            if st.button(
                                f"Delete {appointment['appointment_id']}",
                                key=f"delete_{appointment['appointment_id']}"
                            ):
                                result = appointment_service.delete_appointment_slot(
                                    appointment["appointment_id"],
                                    user["email"]
                                )

                                show_message(result)

                                if result["success"]:
                                    store.save_appointments(appointments)
                                    st.rerun()
                        elif appointment["status"] == "booked":
                            st.info("Booked appointments can be completed from the Booked Appointments section.")
                        elif appointment["status"] == "completed":
                            st.info("Completed appointments are locked and kept as history.")

        show_ai_assistant(user)