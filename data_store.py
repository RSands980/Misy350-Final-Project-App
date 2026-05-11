import json
from pathlib import Path


class DataStore:
    def __init__(self, users_path="users.json", appointments_path="appointments.json"):
        self.users_path = Path(users_path)
        self.appointments_path = Path(appointments_path)

    def load_users(self):
        if self.users_path.exists():
            with open(self.users_path, "r") as file:
                return json.load(file)
        return []

    def save_users(self, users):
        with open(self.users_path, "w") as file:
            json.dump(users, file, indent=4)

    def load_appointments(self):
        if self.appointments_path.exists():
            with open(self.appointments_path, "r") as file:
                return json.load(file)
        return []

    def save_appointments(self, appointments):
        with open(self.appointments_path, "w") as file:
            json.dump(appointments, file, indent=4)