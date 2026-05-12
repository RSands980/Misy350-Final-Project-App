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


def get_appointment_label(appointment):
    return (
        f"Appointment {appointment['appointment_id']} — "
        f"{appointment['date']} at {format_time(appointment['time'])} "
        f"({appointment['status'].title()})"
    )


def show_appointment_details(appointment, show_patient=False, show_doctor=False):
    st.write("Appointment ID:", appointment["appointment_id"])

    if show_doctor:
        st.write("Doctor:", appointment["doctor_email"])

    if show_patient:
        st.write("Patient:", appointment["patient_email"])

    st.write("Date:", appointment["date"])
    st.write("Time:", format_time(appointment["time"]))
    st.write("Status:", appointment["status"].title())


# Data/service setup
store = DataStore()
users = store.load_users()
appointments = store.load_appointments()

auth_service = AuthService(users)
appointment_service = AppointmentService(appointments)
ai_assistant = ClinicAIAssistant()


def build_ai_context(user):
    role = user["role"]

    if role == "Patient":
        available = appointment_service.get_available_appointments()
        active = appointment_service.get_patient_active_appointments(user["email"])
        completed = appointment_service.get_patient_completed_appointments(user["email"])

        context_lines = ["Current ClinicConnect data for this patient:"]

        context_lines.append("\nAvailable appointments:")
        if len(available) == 0:
            context_lines.append("- No available appointments right now.")
        else:
            for appointment in available:
                context_lines.append(
                    f"- Appointment {appointment['appointment_id']} with {appointment['doctor_email']} "
                    f"on {appointment['date']} at {format_time(appointment['time'])}"
                )

        context_lines.append("\nPatient active appointments:")
        if len(active) == 0:
            context_lines.append("- No active appointments.")
        else:
            for appointment in active:
                context_lines.append(
                    f"- Appointment {appointment['appointment_id']} with {appointment['doctor_email']} "
                    f"on {appointment['date']} at {format_time(appointment['time'])}"
                )

        context_lines.append("\nPatient completed appointments:")
        if len(completed) == 0:
            context_lines.append("- No completed appointments.")
        else:
            for appointment in completed:
                context_lines.append(
                    f"- Appointment {appointment['appointment_id']} with {appointment['doctor_email']} "
                    f"on {appointment['date']} at {format_time(appointment['time'])}"
                )

        return "\n".join(context_lines)

    if role == "Doctor":
        booked = appointment_service.get_doctor_booked_appointments(user["email"])
        completed = appointment_service.get_doctor_completed_appointments(user["email"])
        all_slots = appointment_service.get_doctor_appointments(user["email"])

        context_lines = ["Current ClinicConnect data for this doctor:"]

        context_lines.append("\nBooked appointments:")
        if len(booked) == 0:
            context_lines.append("- No booked appointments.")
        else:
            for appointment in booked:
                context_lines.append(
                    f"- Appointment {appointment['appointment_id']} with patient {appointment['patient_email']} "
                    f"on {appointment['date']} at {format_time(appointment['time'])}"
                )

        context_lines.append("\nCompleted appointments:")
        if len(completed) == 0:
            context_lines.append("- No completed appointments.")
        else:
            for appointment in completed:
                context_lines.append(
                    f"- Appointment {appointment['appointment_id']} with patient {appointment['patient_email']} "
                    f"on {appointment['date']} at {format_time(appointment['time'])}"
                )

        context_lines.append("\nAll doctor appointment slots:")
        if len(all_slots) == 0:
            context_lines.append("- No appointment slots.")
        else:
            for appointment in all_slots:
                context_lines.append(
                    f"- Appointment {appointment['appointment_id']} on {appointment['date']} "
                    f"at {format_time(appointment['time'])}, status: {appointment['status']}"
                )

        return "\n".join(context_lines)

    return "No app context available."


def show_ai_assistant(user):
    with st.container(border=True):
        st.subheader("ClinicConnect AI Assistant")

        if user["role"] == "Patient":
            st.write("Ask about available appointments, appointment preparation, or how to use the app.")
            default_question = "What appointments are available?"
        else:
            st.write("Ask about booked appointments, completed appointments, or follow-up questions.")
            default_question = "What appointments are currently booked?"

        question = st.text_area(
            "Ask the assistant a question",
            value=default_question,
            key=f"ai_question_{user['role']}"
        )

        if st.button("Ask AI Assistant", key=f"ask_ai_{user['role']}"):
            app_context = build_ai_context(user)

            with st.spinner("Thinking..."):
                result = ai_assistant.get_response(
                    user["role"],
                    question,
                    app_context
                )

            if result["success"]:
                st.success("Assistant response:")
                st.write(result["message"])
            else:
                st.warning(result["message"])


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
            available_tab, active_tab, completed_tab, assistant_tab = st.tabs(
                [
                    "Available Appointments",
                    "My Active Appointments",
                    "Completed History",
                    "AI Assistant",
                ]
            )

            with available_tab:
                st.subheader("Available Appointments")
                st.write("Choose an available appointment slot to book.")

                available_appointments = appointment_service.get_available_appointments()
                available_ids = []

                if len(available_appointments) == 0:
                    st.info("No available appointments right now.")

                for appointment in available_appointments:
                    available_ids.append(appointment["appointment_id"])

                    with st.expander(get_appointment_label(appointment)):
                        show_appointment_details(appointment, show_doctor=True)

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

            with active_tab:
                st.subheader("My Active Appointments")
                st.write("These are appointments you have booked but have not completed yet.")

                active_appointments = appointment_service.get_patient_active_appointments(
                    user["email"]
                )

                if len(active_appointments) == 0:
                    st.info("No active appointments.")

                for appointment in active_appointments:
                    with st.expander(get_appointment_label(appointment)):
                        show_appointment_details(appointment, show_doctor=True)

                        if st.button(
                            f"Cancel Appointment {appointment['appointment_id']}",
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

            with completed_tab:
                st.subheader("Completed Appointment History")
                st.write("Completed appointments are locked and kept as history.")

                completed_appointments = appointment_service.get_patient_completed_appointments(
                    user["email"]
                )

                if len(completed_appointments) == 0:
                    st.info("No completed appointments yet.")

                for appointment in completed_appointments:
                    with st.expander(get_appointment_label(appointment)):
                        show_appointment_details(appointment, show_doctor=True)
                        st.info("This appointment is completed and cannot be changed.")

            with assistant_tab:
                show_ai_assistant(user)

        # Doctor dashboard
        elif user["role"] == "Doctor":
            create_tab, booked_tab, slots_tab, completed_tab, assistant_tab = st.tabs(
                [
                    "Create Slot",
                    "Booked Appointments",
                    "All Slots",
                    "Completed History",
                    "AI Assistant",
                ]
            )

            with create_tab:
                st.subheader("Create Appointment Slot")
                st.write("Create a new appointment slot for patients to book.")

                with st.container(border=True):
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

            with booked_tab:
                st.subheader("Booked Appointments")
                st.write("These appointments have been booked by patients and can be marked completed.")

                booked_appointments = appointment_service.get_doctor_booked_appointments(
                    user["email"]
                )

                if len(booked_appointments) == 0:
                    st.info("No booked appointments.")

                for appointment in booked_appointments:
                    with st.expander(get_appointment_label(appointment)):
                        show_appointment_details(appointment, show_patient=True)

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

            with slots_tab:
                st.subheader("All Appointment Slots")
                st.write("Review all of your available, booked, and completed appointment slots.")

                doctor_appointments = appointment_service.get_doctor_appointments(
                    user["email"]
                )

                if len(doctor_appointments) == 0:
                    st.info("No appointment slots yet.")

                for appointment in doctor_appointments:
                    with st.expander(get_appointment_label(appointment)):
                        show_appointment_details(appointment)

                        if appointment["status"] == "available":
                            if st.button(
                                f"Delete Appointment {appointment['appointment_id']}",
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
                            st.info("Booked appointments can be completed from the Booked Appointments tab.")
                        elif appointment["status"] == "completed":
                            st.info("Completed appointments are locked and kept as history.")

            with completed_tab:
                st.subheader("Completed Appointment History")
                st.write("Completed appointments are stored as history and cannot be changed back.")

                completed_appointments = appointment_service.get_doctor_completed_appointments(
                    user["email"]
                )

                if len(completed_appointments) == 0:
                    st.info("No completed appointments yet.")

                for appointment in completed_appointments:
                    with st.expander(get_appointment_label(appointment)):
                        show_appointment_details(appointment, show_patient=True)
                        st.info("This appointment is completed and locked.")

            with assistant_tab:
                show_ai_assistant(user)