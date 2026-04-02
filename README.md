# ClinicConnect

- ClinicConnect is a simple appointment scheduling web app built using Streamlit. It allows patients and doctors to manage appointments through a role-based system.

## Progress Log

### Day 1
- Created GitHub repository
- Set up starter files (app.py, README, requirements, gitignore)

### Day 2
- Added JSON storage files (users, appointments)
- Built basic app layout with sidebar navigation
- Started login and registration interface
- Began session state setup for user tracking

### Day 3
- Implemented working registration logic and saved new users to users.json
- Added login validation using saved user credentials
- Updated session state to track the logged-in user
- Added dashboard routing after successful login
- Added logout functionality in the sidebar
- Added a basic role-based dashboard section for Patient and Doctor users

## Planning Notes

### App Name
ClinicConnect

### Purpose
A simple appointment scheduling app for a small clinic.

### Roles
- Patient
- Doctor

### JSON Files
- users.json stores user account information
- appointments.json will store appointment slot and booking information

### Current Development Approach
- Start with authentication first
- Then build role-based dashboards
- Then add appointment CRUD features