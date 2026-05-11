# 07 Follow-Up Prompts and Refinement Log

Author: Ryan Sanders  
Project: ClinicConnect  
Date: May 2026  

## Purpose

This document records follow-up prompts, extra implementation requests, and small refinements made during the AI-assisted development process. The goal is to show what changed after the first analysis and planning steps, why those changes were made, and which project layer was affected.

## Follow-Up Prompt 1: Structural Refactor Implementation

### Prompt / Request

After creating the structural improvement plan, I asked AI to help implement the structural refactor by separating the original one-file app into clearer layers.

### Change Made

The project was updated from one mostly procedural `app.py` file into a clearer structure:

- `data_store.py` was added for JSON loading and saving.
- `services.py` was added for authentication and appointment rules.
- `app.py` was updated to focus more on Streamlit UI and user interaction.

### Layer Affected

- Data Layer
- Service Layer
- UI Layer

### Why It Mattered

This made the app easier to maintain because JSON logic, service rules, and Streamlit interface code were no longer all mixed together in one file.

---

## Follow-Up Prompt 2: Test Account Fix

### Prompt / Request

After adding visible test accounts to the login page, I noticed that the displayed test accounts needed to match the actual users saved in `users.json`.

### Change Made

The test users in `users.json` were updated so the login page credentials worked:

- Patient: `patient@test.com / patient123`
- Doctor: `doctor@test.com / doctor123`

### Layer Affected

- Data File
- UI Layer

### Why It Mattered

The final project instructions require visible test accounts on the login page. This change makes it easier for the professor or grader to immediately test both user roles.

---

## Follow-Up Prompt 3: Appointment Sample Data Fix

### Prompt / Request

After updating the official test accounts, I updated the appointment sample data so the appointments connected to the correct test doctor and patient accounts.

### Change Made

The appointment records in `appointments.json` were updated so `doctor@test.com` and `patient@test.com` had meaningful sample data.

### Layer Affected

- Data File

### Why It Mattered

This prevents empty dashboards during testing and makes the app easier to demo. When the professor logs in with the test accounts, both roles should immediately show useful appointment records.

---

## Follow-Up Prompt 4: Completed Appointment Workflow

### Prompt / Request

I asked AI to implement the first feature/UI improvement stage from the plan: completed appointment status, completed appointment locking, active/completed sections, and AM/PM time formatting.

### Change Made

The app now supports a completed appointment workflow:

- Doctors can mark booked appointments as completed.
- Patients can see completed appointments as history.
- Completed appointments cannot be cancelled or deleted.
- Appointment times display in AM/PM format.
- Dashboards are separated into clearer appointment sections.

### Layer Affected

- Service Layer
- UI Layer
- Data File

### Why It Mattered

This made the appointment workflow more realistic because appointments now have a full lifecycle:

available → booked → completed

It also added a stronger business rule because completed appointment records are protected.

---

## Follow-Up Prompt 5: AM/PM Time Dropdown

### Prompt / Request

After testing the doctor dashboard, I noticed that the appointment creation time picker still showed military time. I asked AI to change the doctor time selector to show AM/PM times from 8:00 AM to 6:00 PM.

### Change Made

The doctor appointment time input was changed from a raw time input to an AM/PM dropdown.

### Layer Affected

- UI Layer

### Why It Mattered

This made appointment creation easier to understand and more consistent with the AM/PM time display shown on appointment cards.

---

## Follow-Up Prompt 6: Dashboard Layout Observation

### Prompt / Request

After testing the new appointment workflow, I noticed that the dashboard still uses large appointment cards. If many appointments are created, the page may become harder to read.

### Change Made

No major layout change was made yet. I decided to finish the basic required improvements first before doing a second UI polish pass.

### Layer Affected

- UI Layer

### Why It Mattered

This helped keep the project scope under control. The current dashboard works, but a future improvement could use tabs, expanders, filters, or tables to make appointment lists easier to scan.

---

## Current Status

At this point, the structural refactor and first feature/UI improvement stage are working. The app currently has:

- separated data and service files
- working test accounts
- patient and doctor dashboards
- appointment booking and cancellation
- doctor appointment creation and deletion
- completed appointment workflow
- locked completed appointments
- AM/PM appointment display
- AM/PM doctor time selection
- sample data connected to the test accounts

## Remaining Follow-Up Work

The next follow-up work should focus on:

1. Adding the AI assistant layer.
2. Connecting the assistant to the app in a useful way.
3. Testing the assistant with patient or doctor questions.
4. Improving dashboard polish if time allows.
5. Final deployment testing.
6. Making sure the GitHub repo and Streamlit app link are up to date.

## My Review Note

This follow-up log shows that the project changed in stages instead of all at once. The most important refinements so far were the structural refactor, the completed appointment workflow, and the AM/PM time improvements. I chose not to do a full dashboard redesign yet because the main goal was to complete the required app behavior first and then polish the design after the core workflow was stable.