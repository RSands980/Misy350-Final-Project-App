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

        if "completed" in question_lower:
            return (
                "Completed appointments are shown as history in ClinicConnect. "
                "Once an appointment is completed, it cannot be cancelled, deleted, or changed back. "
                "This protects the appointment record."
            )

        if "cancel" in question_lower:
            return (
                "Patients can cancel active booked appointments, but completed appointments are locked and cannot be cancelled. "
                "To cancel an appointment, go to the Patient Dashboard and use the cancel button under My Active Appointments."
            )

        if user_role == "Patient":
            return (
                "ClinicConnect helps patients view available appointments, book appointments, cancel active appointments, "
                "and view completed appointment history. For an appointment, you may want to bring your ID, insurance information if needed, "
                "and a short list of questions or concerns. For medical advice, contact a healthcare professional."
            )

        if user_role == "Doctor":
            return (
                "ClinicConnect helps doctors create appointment slots, view booked appointments, mark appointments as completed, "
                "and review completed appointment history. For follow-up questions, consider asking about symptoms, timing, severity, "
                "medications, and whether the patient needs another visit."
            )

        return (
            "ClinicConnect helps manage patient and doctor appointment workflows. "
            "You can use it to book, cancel, complete, and review appointments."
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
        active appointments, completed appointments, and basic app workflow.
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