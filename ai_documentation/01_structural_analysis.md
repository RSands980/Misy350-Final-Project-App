# 01 Structural Analysis

Author: Ryan Sanders  
Project: ClinicConnect  
Date: May 2026  

## Origin Prompt

I am working on Phase 2 of my MISY350 final project. Please analyze my current Phase 1 Streamlit app structure before I make changes. Do not rewrite the code yet. Identify the UI layer, data layer, service/business logic layer, models/classes that are missing, and important dependencies. Explain what should be protected before refactoring. Keep the analysis focused on structure, maintainability, and separation of concerns.

## Current Structure Summary

ClinicConnect is currently a working Phase 1 MVP. It includes login, registration, logout, session state, two user roles, JSON data storage, and appointment workflows. Patients can view available appointments, book appointments, view their booked appointments, and cancel appointments. Doctors can create appointment slots, view booked appointments, and delete appointment slots.

The app works, but most of the code is currently inside one file, `app.py`. This means the Streamlit UI, JSON file loading/saving, login and registration logic, appointment rules, and dashboard routing are all mixed together. This was acceptable for the MVP, but Phase 2 needs a cleaner structure using functions, classes, and separate layers.

## Layer Analysis

| Area | Current Location | Current Role | Structural Issue | Future Layer |
|---|---|---|---|---|
| `users_path` and `appointments_path` | Top of `app.py` | File path setup | File paths are directly tied to the app file | Data Layer / Config |
| Loading `users.json` | Top of `app.py` | Reads user data | JSON reading happens directly in the main app | Data Layer |
| Loading `appointments.json` | Top of `app.py` | Reads appointment data | JSON reading happens directly in the main app | Data Layer |
| Session state setup | Top of `app.py` | Tracks current page and logged-in user | This is Streamlit-specific state and should stay near UI/routing | UI Layer |
| Sidebar navigation | Top of `app.py` | Login/register/logout routing | Mostly UI work, but also clears user state | UI Layer |
| Login page | Main `if` block | Validates user and updates session | UI widgets and login validation are mixed | UI + Service |
| Registration page | `elif` block | Creates new users | UI, validation, duplicate checking, and JSON saving are mixed | UI + Service + Data |
| Patient dashboard | Dashboard block | Shows and books appointments | UI display, appointment filtering, status updates, and JSON saving are mixed | UI + Service + Data |
| Doctor dashboard | Dashboard block | Creates/deletes slots and views bookings | UI display, appointment creation/deletion, and JSON saving are mixed | UI + Service + Data |
| Appointment booking | Patient dashboard | Changes appointment from available to booked | Business rule is inside button code | Service Layer |
| Appointment canceling | Patient dashboard | Changes appointment back to available | Business rule and JSON save are inside UI code | Service + Data |
| Appointment slot creation | Doctor dashboard | Adds a new available slot | Creation logic and JSON save are inside UI code | Service + Data |
| Appointment deletion | Doctor dashboard | Removes appointment record | Delete logic is directly inside dashboard UI | Service + Data |

## Main Structural Problems

1. **UI, data, and service logic are mixed together.**  
   The app works, but button code directly changes appointment dictionaries and writes JSON files. This makes the app harder to maintain because one page is doing too many jobs.

2. **JSON loading and saving are repeated directly in the app.**  
   The app reads and writes `users.json` and `appointments.json` inside `app.py`. This should move into a data layer so the rest of the app does not need to know how files are stored.

3. **Authentication logic is mixed into the login/register pages.**  
   Login validation, duplicate email checking, and account creation are currently handled directly inside the Streamlit page code. These should move into a service layer.

4. **Appointment rules are mixed into dashboard buttons.**  
   Booking, canceling, creating slots, and deleting slots happen directly inside the UI. These actions should be handled by an appointment service so rules are easier to update.

5. **No clear object-oriented structure yet.**  
   Phase 2 requires functions, methods, classes, and clearer layers. The app should add classes such as a data manager, authentication service, appointment service, and AI assistant.

## Important Dependencies

- `streamlit` is used for the interface, session state, sidebar navigation, forms, buttons, containers, and columns.
- `json` is used to save and load users and appointments.
- `pathlib.Path` is used for file paths.
- `time` is used for small loading delays with spinners.
- `users.json` stores registered users and roles.
- `appointments.json` stores appointment slots, patient emails, doctor emails, dates, times, and statuses.

## What Should Be Protected Before Refactoring

- Registration should still work.
- Login and logout should still work.
- Patient and Doctor roles should still route to different dashboards.
- Users should still save to `users.json`.
- Appointments should still save to `appointments.json`.
- Patients should still be able to book and cancel appointments.
- Doctors should still be able to create appointment slots and manage their own slots.
- Existing sample data should stay usable.
- The Streamlit app link should still load after changes.
- The refactor should not break the current working appointment flow.

## My Review Note

This analysis matches what I see in my Phase 1 app. The app has the main MVP requirements working, but the structure is still too mixed because UI code, JSON saving/loading, authentication checks, and appointment rules are all in `app.py`. For Phase 2, I need to protect the working login, role routing, and appointment workflows while refactoring the code into clearer layers.

## Recommended Next Step

The next step should be to create a feature analysis document before changing the code. After that, I should create a structural improvement plan that separates:

- Data Layer: JSON loading and saving
- Service Layer: authentication and appointment rules
- UI Layer: Streamlit pages, buttons, forms, and dashboards
- AI Assistant Layer: OpenAI assistant logic added later