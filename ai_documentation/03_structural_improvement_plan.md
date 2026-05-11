# 03 Structural Improvement Plan

Author: Ryan Sanders  
Project: ClinicConnect  
Date: May 2026  

## Origin Prompt

I am working on Phase 2 of my MISY350 final project. Based on my structural analysis and feature analysis, please create a structural improvement plan for my current ClinicConnect app. Do not rewrite the code yet. Focus on improving organization, layering, maintainability, and separation of concerns. The plan should explain what should move into the UI layer, data layer, service/business logic layer, and AI assistant layer. It should also explain what should stay protected so the working Phase 1 app does not break.

## Current Problem

The current Phase 1 app works, but most of the code is inside `app.py`. The app currently mixes Streamlit UI code, JSON loading/saving, authentication logic, appointment rules, and dashboard routing in one file.

Phase 2 requires a cleaner structure with functions, methods, classes, and separate layers. The goal is not to rebuild the app from scratch. The goal is to protect the working MVP while making the project easier to maintain and expand.

## Proposed File Structure

```text
MISY350 FINAL PROJECT/
├── app.py
├── data_store.py
├── services.py
├── ai_assistant.py
├── users.json
├── appointments.json
├── requirements.txt
├── README.md
├── .gitignore
└── ai_documentation/
    ├── 01_structural_analysis.md
    ├── 02_feature_analysis.md
    └── 03_structural_improvement_plan.md