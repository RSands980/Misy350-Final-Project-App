# 08 AI Assistant Implementation Notes

Author: Ryan Sanders  
Project: ClinicConnect  
Date: May 2026  

## Origin Prompt

I asked AI to add an AI assistant layer to ClinicConnect after the structural refactor and feature/UI improvements were working. The goal was to connect the app to OpenAI, keep the AI logic separate from the rest of the app, and make the assistant useful for patient and doctor workflows.

## What Changed

The app now includes a ClinicConnect AI Assistant section inside the dashboard. The assistant is designed to connect to OpenAI using an API key stored through Streamlit secrets. It also includes fallback responses so the app still works if OpenAI access is unavailable.

### Files Added

- `ai_assistant.py`

### Files Updated

- `app.py`
- `requirements.txt`
- `.gitignore`

## AI Assistant Layer

| File | Layer | What Changed |
|---|---|---|
| `ai_assistant.py` | AI Assistant Layer | Added the `ClinicAIAssistant` class for OpenAI connection and fallback assistant responses |
| `app.py` | UI Layer | Added the assistant section to the patient and doctor dashboards |
| `requirements.txt` | Dependency File | Added the `openai` package |
| `.gitignore` | Security/Project Setup | Added `.streamlit/secrets.toml` and `.venv/` so API keys and virtual environment files are not committed |

## API Key Handling

The OpenAI API key is stored locally in:

`.streamlit/secrets.toml`

The key is not stored in `app.py`, `ai_assistant.py`, or GitHub. The `.gitignore` file was updated so the secrets file is excluded from commits.

This protects the API key while still allowing the app to read it locally during testing.

## App Context Added to Assistant

The assistant was updated so it can use current app data instead of only giving general answers.

For patients, the assistant can use context about:

- available appointments
- active appointments
- completed appointment history

For doctors, the assistant can use context about:

- booked appointments
- completed appointments
- all doctor appointment slots

This makes the assistant more useful because it can answer questions like:

- What appointments are available?
- What appointments are currently booked?
- What completed appointments do I have?
- How do I cancel an appointment?
- What does completed mean?

## Fallback Responses

During testing, the app reached the OpenAI API, but the API returned an insufficient quota message for my key. To keep the app usable, I added fallback responses.

The assistant now works like this:

1. Try to connect to OpenAI using the API key from Streamlit secrets.
2. Send the user's question and current app context.
3. If OpenAI works, show the OpenAI response.
4. If OpenAI is unavailable or quota is not active, show a built-in assistant response using app data.
5. Never crash the app during the demo.

## What Was Protected

The AI assistant update protected the existing app behavior:

- Registration still works
- Login still works
- Logout still works
- Patient and Doctor dashboards still work
- Appointment booking still works
- Appointment cancellation still works
- Doctor appointment creation still works
- Doctor appointment completion still works
- Completed appointments remain locked
- JSON persistence still works
- API key is not committed to GitHub

## What I Tested

### Patient Assistant Test

I logged in as the test patient and asked the assistant what appointments were available. The assistant used the current appointment data and showed the available appointment information.

### Doctor Assistant Test

I logged in as the test doctor and asked what appointments were currently booked. The assistant used the current app data and showed the booked appointment information.

### API Error Handling Test

I tested the assistant with an OpenAI API key. The app successfully reached OpenAI, but OpenAI returned an insufficient quota message. The app did not crash. Instead, it used the fallback response system.

### Security Test

I checked Git status and confirmed that `.streamlit/secrets.toml` was not included in the commit. This means the API key was kept out of GitHub.

## Result

The AI assistant layer was successfully added. The app now has an assistant section that is designed to connect to OpenAI, uses app context, and has fallback responses if OpenAI access is unavailable. This makes the app more useful during testing and safer for demos.

## Next Step

The next step is to confirm whether the class expects students to use personal OpenAI API billing credits or whether fallback responses are acceptable when API quota is unavailable. After that, the final work should focus on deployment testing and optional dashboard polish.