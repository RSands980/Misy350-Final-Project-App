# 05 Feature and UI Improvement Plan

Author: Ryan Sanders  
Project: ClinicConnect  
Date: May 2026  

## Origin Prompt

I asked AI to create a feature and UI improvement plan for my Phase 2 ClinicConnect app after the structural refactor was completed. The goal was to plan visible improvements before changing the code again. The plan should focus on missing features, usability improvements, appointment workflow improvements, Streamlit layout improvements, user actions, feedback messages, and AI assistant integration. The plan should not implement code yet.

## Current App Status

ClinicConnect is now structurally improved compared to the Phase 1 version. The app was refactored so that app.py focuses more on the Streamlit interface, data_store.py handles JSON loading and saving, services.py handles authentication and appointment rules, users.json includes working test accounts, and appointments.json includes sample appointment data connected to the test accounts.

The main Phase 1 workflows still work. Patients can log in, view available appointments, book appointments, view their appointments, and cancel appointments. Doctors can log in, create appointment slots, view appointments, and delete appointment slots.

## Main Feature/UI Problems To Improve

| Area | Current Issue | Planned Improvement |
|---|---|---|
| Test accounts | Test accounts are visible now, but the login page can still be clearer | Keep test accounts visible and easy to copy/use |
| Appointment workflow | Appointments only move between available and booked | Add a completed status so appointments have a final state |
| Completed records | Completed appointments are not currently protected | Lock completed appointments so they cannot be changed back |
| Patient dashboard | Booked/current appointments and history are not clearly separated | Separate active appointments from completed appointment history |
| Doctor dashboard | Doctors can view booked appointments, but cannot complete them | Add a button for doctors to mark booked appointments as completed |
| Appointment time display | Times show in raw 24-hour style | Format times in AM/PM style for readability |
| Success messages | Some success messages disappear quickly because the app reruns | Add a short delay or message handling so users can notice successful actions |
| Dashboard layout | The dashboard works but still feels basic | Improve headings, containers, columns, and status-based sections |
| AI assistant | No OpenAI assistant exists yet | Add a simple assistant connected to OpenAI that fits the app purpose |

## Planned Feature Improvements

### 1. Completed Appointment Status

Add a new appointment status called completed.

Doctors should be able to mark a booked appointment as completed. This gives the appointment process a clear ending point.

The workflow should become: available → booked → completed.

This is better than only having available/booked because it lets the app keep appointment history.

### 2. Lock Completed Appointments

Completed appointments should be protected.

Rules:
- A completed appointment cannot be cancelled by a patient.
- A completed appointment cannot be deleted as if it were still an open slot.
- A completed appointment cannot be changed back to available or booked.
- Completed appointments should stay visible as history.

This rule belongs in the service layer because it is business logic, not just a display choice.

### 3. Improve Patient Dashboard

The Patient dashboard should be clearer.

Planned sections:
- Available Appointments
- My Active Appointments
- Completed Appointment History

Patients should be able to book available appointments and cancel active booked appointments. Completed appointments should be shown as history only.

### 4. Improve Doctor Dashboard

The Doctor dashboard should be clearer.

Planned sections:
- Create Appointment Slot
- Booked Appointments
- Appointment Slots / Appointment History

Doctors should be able to create available slots, view booked appointments, mark booked appointments as completed, and manage open appointment slots. Completed appointments should stay visible but should not be treated like open slots.

### 5. Format Appointment Times in AM/PM

Appointment times should be easier to read. Instead of showing times like 13:15:00, the app should show times like 1:15 PM.

This is a simple usability improvement that makes the dashboard feel more polished.

### 6. Improve Success Messages

Some success messages disappear quickly when st.rerun() happens immediately after an action. This can make it hard for users to know whether booking, canceling, creating, deleting, or completing an appointment worked.

Planned improvement:
- Show clearer success/error messages after each action.
- Use a short delay if needed before rerunning.
- Keep messages simple and easy to understand.

This should be done carefully so the app still refreshes after data changes.

### 7. Improve Dashboard Layout

The current dashboards work, but Phase 2 should look more polished.

Planned layout improvements:
- Use clearer section headers.
- Keep patient and doctor workflows separated.
- Use containers for appointment cards/sections.
- Use columns to avoid one long vertical page.
- Use dividers between major actions.
- Avoid showing raw dictionaries to users.

The goal is not to redesign the whole app, but to make it easier to understand during the demo.

### 8. Add AI Assistant

Add a simple AI assistant connected to OpenAI.

The assistant should fit the purpose of ClinicConnect. It should not be random or unrelated to the app.

Possible assistant use cases:
- Patient: ask questions about preparing for an appointment.
- Patient: ask what information to bring to a clinic visit.
- Doctor: summarize appointment notes or suggest follow-up questions.

The first version can be simple. It should include:
- a clear assistant section in the UI
- a text input or chat-style input
- a response from OpenAI
- safe handling if the API key is missing

The OpenAI logic should be kept separate from appointment rules and JSON storage.

## Files Expected To Change

| File | Expected Change | Layer |
|---|---|---|
| services.py | Add completed appointment logic, lock completed appointments, add helper filters if needed | Service Layer |
| app.py | Update dashboard sections, buttons, messages, time display, and AI assistant UI section | UI Layer |
| ai_assistant.py | Add OpenAI assistant logic | AI Assistant Layer |
| appointments.json | Add or update sample records with available, booked, and completed statuses | Data File |
| requirements.txt | Add OpenAI dependency if needed | Dependency File |

## What Should Be Protected

The following working features should not break:
- Registration
- Login
- Logout
- Patient role routing
- Doctor role routing
- JSON persistence
- Patient appointment booking
- Patient appointment cancellation for active appointments
- Doctor appointment slot creation
- Doctor appointment viewing
- Doctor appointment deletion for open slots
- Existing test accounts
- Existing deployed Streamlit app link

## Testing Plan

After implementation, test:
1. Log in as the test patient.
2. Confirm available appointments appear.
3. Book an appointment.
4. Confirm the appointment moves to the patient's active appointments.
5. Cancel an active appointment.
6. Confirm it becomes available again.
7. Log in as the test doctor.
8. Create a new appointment slot.
9. Confirm the slot appears.
10. Book a doctor slot from the patient account.
11. Log back in as the doctor.
12. Mark the booked appointment as completed.
13. Confirm completed appointments cannot be cancelled, deleted, or changed back.
14. Confirm appointment times display in AM/PM format.
15. Test the AI assistant with a basic ClinicConnect-related question.
16. Confirm JSON files still save the correct data.

## My Review Note

This plan fits my Phase 2 goals because it improves the existing ClinicConnect app instead of starting over. The most important feature improvement is the completed appointment workflow because it makes the app feel more realistic and adds stronger service-layer logic. The AM/PM time formatting and clearer dashboard sections improve usability without making the project too large. The AI assistant should be added after the appointment workflow is stable so it does not get mixed into the wrong layer.

## Next Step

The next step is to implement these feature and UI improvements in stages. The first implementation should focus on appointment status improvements, completed appointment locking, AM/PM time display, and dashboard organization. The AI assistant should be added after the core workflow is stable.