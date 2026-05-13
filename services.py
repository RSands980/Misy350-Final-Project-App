class AuthService:
    def __init__(self, users):
        self.users = users

    def find_user_by_email(self, email):
        for user in self.users:
            if user["email"] == email:
                return user
        return None

    def validate_login(self, email, password):
        for user in self.users:
            if user["email"] == email and user["password"] == password:
                return user
        return None

    def email_exists(self, email):
        return self.find_user_by_email(email) is not None

    def register_user(self, name, email, password, role):
        if name == "" or email == "" or password == "":
            return {
                "success": False,
                "message": "Please fill in all fields",
                "user": None,
            }

        if "@" not in email or " " in email:
            return {
                "success": False,
                "message": "Please enter a valid email",
                "user": None,
            }

        if len(password) < 6:
            return {
                "success": False,
                "message": "Password must be at least 6 characters",
                "user": None,
            }

        if self.email_exists(email):
            return {
                "success": False,
                "message": "Email already exists",
                "user": None,
            }

        new_user = {
            "user_id": str(len(self.users) + 1),
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        }

        self.users.append(new_user)

        return {
            "success": True,
            "message": "Account created successfully",
            "user": new_user,
        }


class AppointmentService:
    def __init__(self, appointments):
        self.appointments = appointments

    def get_next_appointment_id(self):
        highest_id = 0

        for appointment in self.appointments:
            current_id = int(appointment["appointment_id"])

            if current_id > highest_id:
                highest_id = current_id

        return str(highest_id + 1)

    def get_available_appointments(self):
        available = []

        for appointment in self.appointments:
            if appointment["status"] == "available":
                available.append(appointment)

        return available

    def get_patient_active_appointments(self, patient_email):
        active = []

        for appointment in self.appointments:
            if (
                appointment["patient_email"] == patient_email
                and appointment["status"] == "booked"
            ):
                active.append(appointment)

        return active

    def get_patient_completed_appointments(self, patient_email):
        completed = []

        for appointment in self.appointments:
            if (
                appointment["patient_email"] == patient_email
                and appointment["status"] == "completed"
            ):
                completed.append(appointment)

        return completed

    def get_patient_appointments(self, patient_email):
        patient_appointments = []

        for appointment in self.appointments:
            if appointment["patient_email"] == patient_email:
                patient_appointments.append(appointment)

        return patient_appointments

    def get_doctor_appointments(self, doctor_email):
        doctor_appointments = []

        for appointment in self.appointments:
            if appointment["doctor_email"] == doctor_email:
                doctor_appointments.append(appointment)

        return doctor_appointments

    def get_doctor_booked_appointments(self, doctor_email):
        booked = []

        for appointment in self.appointments:
            if (
                appointment["doctor_email"] == doctor_email
                and appointment["status"] == "booked"
            ):
                booked.append(appointment)

        return booked

    def get_doctor_completed_appointments(self, doctor_email):
        completed = []

        for appointment in self.appointments:
            if (
                appointment["doctor_email"] == doctor_email
                and appointment["status"] == "completed"
            ):
                completed.append(appointment)

        return completed

    def book_appointment(self, appointment_id, patient_email):
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["status"] != "available":
                    return {
                        "success": False,
                        "message": "This appointment is not available.",
                    }

                appointment["patient_email"] = patient_email
                appointment["status"] = "booked"

                return {
                    "success": True,
                    "message": "Appointment booked successfully.",
                }

        return {
            "success": False,
            "message": "Appointment was not found.",
        }

    def cancel_appointment(self, appointment_id, patient_email):
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["patient_email"] != patient_email:
                    return {
                        "success": False,
                        "message": "You can only cancel your own appointment.",
                    }

                if appointment["status"] == "completed":
                    return {
                        "success": False,
                        "message": "Completed appointments cannot be cancelled.",
                    }

                if appointment["status"] != "booked":
                    return {
                        "success": False,
                        "message": "Only booked appointments can be cancelled.",
                    }

                appointment["patient_email"] = ""
                appointment["status"] = "available"

                return {
                    "success": True,
                    "message": "Appointment cancelled successfully.",
                }

        return {
            "success": False,
            "message": "Appointment was not found.",
        }

    def create_appointment_slot(self, doctor_email, appointment_date, appointment_time):
        new_appointment = {
            "appointment_id": self.get_next_appointment_id(),
            "doctor_email": doctor_email,
            "patient_email": "",
            "date": str(appointment_date),
            "time": str(appointment_time),
            "status": "available",
        }

        self.appointments.append(new_appointment)

        return {
            "success": True,
            "message": "Appointment slot added successfully.",
            "appointment": new_appointment,
        }

    def delete_appointment_slot(self, appointment_id, doctor_email):
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["doctor_email"] != doctor_email:
                    return {
                        "success": False,
                        "message": "You can only delete your own appointment slot.",
                    }

                if appointment["status"] == "completed":
                    return {
                        "success": False,
                        "message": "Completed appointments cannot be deleted.",
                    }

                if appointment["status"] == "booked":
                    return {
                        "success": False,
                        "message": "Booked appointments should be completed or cancelled, not deleted.",
                    }

                self.appointments.remove(appointment)

                return {
                    "success": True,
                    "message": "Appointment slot deleted successfully.",
                }

        return {
            "success": False,
            "message": "Appointment was not found.",
        }

    def complete_appointment(self, appointment_id, doctor_email):
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["doctor_email"] != doctor_email:
                    return {
                        "success": False,
                        "message": "You can only complete your own appointments.",
                    }

                if appointment["status"] == "completed":
                    return {
                        "success": False,
                        "message": "This appointment is already completed.",
                    }

                if appointment["status"] != "booked":
                    return {
                        "success": False,
                        "message": "Only booked appointments can be completed.",
                    }

                appointment["status"] = "completed"

                return {
                    "success": True,
                    "message": "Appointment marked as completed.",
                }

        return {
            "success": False,
            "message": "Appointment was not found.",
        }