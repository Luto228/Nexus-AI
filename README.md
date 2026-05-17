# Nexus-AI

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Status-Done-green?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/API-Gemini-orange?style=for-the-badge" alt="Gemini API">
</p>

## Description
Nexus-AI is a Python-based Telegram assistant powered by the Gemini API. The project combines an AI prompt engine with reminder scheduling and basic database persistence.

## Current State
- AI prompt engine implemented in `core/ai_engine.py`
- Telegram bot interface implemented in `main.py`
- Reminder storage and notification service implemented in `services/reminder_service.py`
- Database persistence implemented in `services/database_service.py`
- Basic message handling and action routing for chat, reminders, and record storage

## Known Limitations
- Conversational memory is not yet implemented
- The AI prompt format relies on valid JSON output from Gemini
- User-facing error handling is minimal

## Getting Started
1. Install dependencies (example):
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `config/env.py` with your `BOT_TOKEN` and `GEMINI_API_KEY`.
3. Run the bot:
   ```bash
   python main.py
   ```

## Planned Improvements
- Add structured conversational memory and long-term context
- Improve prompt validation and fallback handling
- Expand expense and fact query support
- Add a clean user interface or command layer

---

*This README now reflects the current implementation and removes outdated completion claims.*
