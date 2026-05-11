import os
from openai import OpenAI


class ClinicAIAssistant:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def is_configured(self):
        return self.client is not None

    def get_response(self, user_role, question):
        if not self.is_configured():
            return {
                "success": False,
                "message": "AI assistant is not configured yet. Add OPENAI_API_KEY to use this feature.",
            }

        if question.strip() == "":
            return {
                "success": False,
                "message": "Please enter a question first.",
            }

        system_message = """
        You are the ClinicConnect assistant for a student-built appointment scheduling app.
        Help users understand appointment preparation, appointment workflow, and basic app usage.
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
                    {"role": "user", "content": question},
                ],
            )

            answer = response.choices[0].message.content

            return {
                "success": True,
                "message": answer,
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"AI assistant error: {error}",
            }