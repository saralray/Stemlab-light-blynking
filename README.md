# Home Assistant Integration Project

This project connects to **Home Assistant** using its REST API with a **Long-Lived Access Token**.  
All sensitive credentials are stored securely using environment variables and are **not committed to git**.

---

## 🚀 Features

- Connects to Home Assistant via API
- Uses `.env` file for secrets (safe for version control)
- Easy setup for local development and deployment
- Token-based authentication (recommended by Home Assistant)

---

## 📦 Requirements

- Home Assistant (running and accessible)
- A Long-Lived Access Token from Home Assistant
- One of the following runtimes (depending on your project):
  - Python 3.9+
  - Node.js 18+
  - Docker (optional but recommended)

---

## 🔐 Environment Variables

This project uses a `.env` file for configuration.

### Required variables

```env
HA_URL=https://your-home-assistant-url
HA_TOKEN=your_long_lived_access_token
