# 02 Feature Analysis

Author: Ryan Sanders  
Project: ClinicConnect  
Date: May 2026  

## Origin Prompt

I am working on Phase 2 of my MISY350 final project. Please analyze the current features in my Phase 1 ClinicConnect app before I make changes. Do not rewrite the code yet. Identify what the app currently does, what features are missing or incomplete, usability issues, role-based workflow issues, and areas for improvement. Keep the focus on app features and user experience, not code structure.

## Current Feature Summary

ClinicConnect currently has a working Phase 1 MVP with two roles: Patient and Doctor.

Current features include:

- User registration
- User login
- Logout through the sidebar
- Session state for tracking the logged-in user and current page
- Role-based dashboard routing
- JSON data storage for users and appointments
- Patient dashboard
- Doctor dashboard
- Appointment booking
- Appointment cancellation
- Doctor appointment slot creation
- Doctor appointment slot deletion

The app has the core Phase 1 features working, but Phase 2 should make the workflows clearer, more complete, and more polished.

## Current Features

| Feature | Current Status | Notes |
|---|---|---|
| Registration | Working | Users can create Patient or Doctor accounts |
| Login | Working | Users can log in with email and password |
| Logout | Working | Sidebar logout clears the user and returns to login |
| Role-based routing | Working | Patients and Doctors see different dashboards |
| JSON data storage | Working | Users and appointments are saved to JSON files |
| Patient appointment booking | Working | Patients can book available appointment slots |
| Patient appointment cancellation | Working | Patients can cancel booked appointments |
| Doctor slot creation | Working | Doctors can create appointment slots |
| Doctor slot deletion | Working | Doctors can delete their appointment slots |
| Doctor booked appointment view | Working but basic | Doctors can see booked appointments, but cannot complete them yet |
| Completed appointment workflow | Missing | Appointments do not currently have a final completed state |
| AI assistant | Missing | Phase 2 requires an OpenAI-connected assistant |
| Test accounts on login page | Missing | Final app must visibly show test accounts |
| AM/PM time formatting | Needs improvement | Appointment times should be easier to read |
| Better user messages | Needs improvement | Some actions work but could explain results more clearly |
| Better dashboard layout | Needs improvement | Dashboards work, but could be more polished and organized |

## Missing or Incomplete Features

1. **Completed appointment status is missing.**  
   Appointments currently move between `available` and `booked`, but there is no final `completed` status. A completed status would make the appointment workflow more realistic.

2. **Completed appointments should be locked.**  
   Once an appointment is completed, it should not be changed back to available or booked. This protects appointment history and makes the workflow clearer.

3. **Doctor workflow needs a stronger update action.**  
   Doctors can create and delete slots, but they should also be able to mark booked appointments as completed.

4. **Patient appointment history should be clearer.**  
   Patients should be able to see upcoming/booked appointments separately from completed or cancelled appointments.

5. **The login page needs visible test accounts.**  
   The final instructions require test account information for each role on the login page.

6. **The AI assistant is not added yet.**  
   The app needs an AI assistant connected to OpenAI that provides useful support inside the app.

7. **Appointment times need better formatting.**  
   Appointment times should display in AM/PM format so they are easier for users to understand.

## Usability Issues

- The app works, but some pages still feel like a basic MVP.
- Appointment records are displayed with simple `st.write()` calls instead of cleaner cards, tables, or organized sections.
- The Patient and Doctor dashboards could use clearer headings and sections.
- Users do not see test credentials on the login page yet.
- Doctors cannot complete appointments yet.
- Completed appointment history is not separated from active appointment actions.
- Some actions could have clearer success/error messages.

## Feature Improvements To Protect

Before making improvements, these working features should be protected:

- Registration should still create a user and save to `users.json`.
- Login should still validate existing users.
- Logout should still clear the session.
- Patients should still be able to book appointments.
- Patients should still be able to cancel appointments that are not completed.
- Doctors should still be able to create appointment slots.
- Doctors should still be able to view booked appointments.
- Doctors should still be able to manage their own appointment slots.
- JSON persistence should still work after each action.
- Role-based routing should not break.

## Recommended Feature/UI Improvements

1. **Add visible test accounts to the login page.**  
   This is required for final submission and makes the app easier to test.

2. **Add a completed appointment workflow.**  
   Doctors should be able to mark a booked appointment as completed.

3. **Lock completed appointments.**  
   Completed appointments should not be cancelled, deleted, or changed back to available.

4. **Improve appointment time display.**  
   Times should show in AM/PM format.

5. **Improve dashboard organization.**  
   Use containers, columns, headers, dividers, and status-based sections.

6. **Add an AI assistant.**  
   The assistant should fit the app purpose. A simple version could help patients prepare for appointments or help doctors summarize appointment notes.

7. **Improve sample data.**  
   The app should include test users and appointments so both roles show meaningful data immediately.

## My Review Note

The current Phase 1 app has the main MVP features working, but Phase 2 needs to make the app more complete and professional. The biggest feature improvements should be adding test accounts, adding a completed appointment status, improving time formatting, improving dashboard layout, and adding a useful AI assistant. I should avoid adding too many new dashboards or roles because Patient and Doctor already satisfy the two-role requirement. The goal should be to improve the existing workflows rather than start over.

## Recommended Next Step

The next step should be to create a structural improvement plan. That plan should focus on separating the current app into clearer files/layers before adding the AI assistant or major UI changes.