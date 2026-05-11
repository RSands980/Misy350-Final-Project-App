import os
import streamlit as st
from openai import OpenAI


class ClinicAIAssistant:
    def __init__(self):
        self.api_key = self.get_api_key()

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def get_api_key(self):
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]

        return os.getenv("OPENAI_API_KEY")

    def is_configured(self):
        return self.client is not None

    def get_fallback_response(self, user_role, question, app_context):
        question_lower = question.lower()

        if "available" in question_lower and "appointment" in question_lower:
            return (
                "Here is what I found from the current app data:\n\n"
                f"{app_context}\n\n"
                "You can use the appointment ID shown in the dashboard to book one of the available appointments."
            )

        if "booked" in question_lower and "appointment" in question_lower:
            return (
                "Here is what I found from the current app data:\n\n"
                f"{app_context}\n\n"
                "Booked appointments can be reviewed in the dashboard. Doctors can mark booked appointments as completed."
            )

        if "active" in question_lower and "appointment" in question_lower:
            return (
                "Here is what I found from the current app data:\n\n"
                f"{app_context}\n\n"
                "Active appointments are appointments that are currently booked but not completed yet."
            )

        if "completed" in question_lower and "appointment" in question_lower:
            return (
                "Here is what I found from the current app data:\n\n"
                f"{app_context}\n\n"
                "Completed appointments are locked and kept as history. They cannot be cancelled, deleted, or changed back."
            )

        if "cancel" in question_lower:
            return (
                "Patients can cancel active booked appointments, but completed appointments are locked and cannot be cancelled. "
                "To cancel an appointment, go to the Patient Dashboard and use the cancel button under My Active Appointments."
            )

        if user_role == "Patient":
            return (
                "ClinicConnect helps patients view available appointments, book appointments, cancel active appointments, "
                "and view completed appointment history.\n\n"
                f"Current app data:\n\n{app_context}"
            )

        if user_role == "Doctor":
            return (
                "ClinicConnect helps doctors create appointment slots, view booked appointments, mark appointments as completed, "
                "and review completed appointment history.\n\n"
                f"Current app data:\n\n{app_context}"
            )

        return (
            "ClinicConnect helps manage patient and doctor appointment workflows.\n\n"
            f"Current app data:\n\n{app_context}"
        )

    def get_response(self, user_role, question, app_context):
        if question.strip() == "":
            return {
                "success": False,
                "message": "Please enter a question first.",
            }

        if not self.is_configured():
            return {
                "success": True,
                "message": self.get_fallback_response(user_role, question, app_context),
                "used_fallback": True,
            }

        system_message = """
        You are the ClinicConnect assistant for a student-built appointment scheduling app.
        Use the provided app context to answer questions about available appointments,
        active appointments, booked appointments, completed appointments, and basic app workflow.
        Do not provide medical diagnosis, treatment plans, medication instructions, or emergency advice.
        If the user asks for medical advice, tell them to contact a healthcare professional.
        Keep answers short, clear, and helpful.
        """

        role_context = f"The current user role is: {user_role}."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": role_context},
                    {"role": "user", "content": f"Current app data:\n{app_context}"},
                    {"role": "user", "content": question},
                ],
            )

            answer = response.choices[0].message.content

            return {
                "success": True,
                "message": answer,
                "used_fallback": False,
            }

        except Exception:
            return {
                "success": True,
                "message": self.get_fallback_response(user_role, question, app_context),
                "used_fallback": True,
            }