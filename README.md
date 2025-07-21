# 🌾 Farming Wisdom Archive

A multilingual, open-source Streamlit application to collect, preserve, and share traditional Indian **agricultural knowledge** — including farming techniques, home remedies relevant to farming, local crop wisdom, and related folk stories or proverbs. Built for **offline-first, low-bandwidth** use so contributors in under-connected regions can participate. Also serves as a **corpus collection engine** for open-source AI research aligned with the viswam.ai challenge.

---
## 👥 Our Team

The **Farming Wisdom Archive** project is made possible by the dedicated efforts of the following individuals:

* **Venkat Chakradhar Reddy Y** -  Project Manager
    * *Connect:* [GitLab Profile](https://code.swecha.org/ChakriYamasani)

* **Jitendra K** - Backend Developer
    * *Connect:* [GitLab Profile](https://code.swecha.org/jitendr21k)

* **Aditya J** - Frontend Lead
    * *Connect:* [GitLab Profile](https://code.swecha.org/Aditya_Tarun_J)

* **Harika P** - UI/UX Designer
    * *Connect:* [GitLab Profile](https://code.swecha.org/harika_putta)

* **HariCharan E** - Deployment & Testing
    * *Connect:* [GitLab Profile](https://code.swecha.org/HARICHARAN22)
---
## 🌟 Purpose

Preserve India’s agricultural heritage by crowdsourcing ancestral farming wisdom in multiple Indian languages. Every submission helps build an open dataset for language technology, agricultural studies, and AI models that understand Indian contexts.

---

## ✅ Key Features (MVP)

- User contributions: title + description/body text
- **Geo Location**: auto-detected (IP) with manual override
- **User Details**: contributor name + optional email
- **Category selection** (Farming Technique, Home Remedy, Folk Story, Proverb, Other)
- Optional image/audio upload
- Local JSON storage (offline-friendly)
- Browse community entries
- Data export (JSONL / CSV) for corpus building
- Sidebar navigation + “Coming Soon” future features

---

## 📋 Mandatory Fields per Submission

1. Geo Location (automatic or manual)
2. User Details (Name + optional Email)
3. Category of corpus submitted
4. Title & Description (content body)
5. Optional media (image/audio)

---

## 🛠 Tech Stack

- Python + Streamlit
- JSON-based local storage (offline-first)
- Geolocation via `geocoder` or IP lookup fallback (`requests`)
- Media saved locally (future: cloud object storage)
- Deployment: Hugging Face Spaces (Streamlit template)
- Planned AI: language detection, translation, summarization, audio transcription

---

## 🚀 Getting Started

### Prerequisites

Python 3.9+ recommended.

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash

streamlit run app/main.py
```

## 📂 Project Structure

```bash

farming-wisdom-archive/
├── app/
│   ├── main.py             # Streamlit app (with Geo + User details)
│   └── helpers.py          # Utility functions (validation, geolocation helpers, etc.)
├── data_entries/           # JSON + media (created at runtime; may use /tmp on HF)
├── .streamlit/             # Optional Streamlit config
├── README.md               # Project overview (this file)
├── REPORT.md               # Full 4-week lifecycle + metrics
├── requirements.txt        # Python dependencies
├── CONTRIBUTING.md         # How to contribute
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT License
```

## 🧪 Week 2 Beta Testing Checklist
Collect at least 10 real submissions (different users)

Test low-bandwidth (hotspot / 2G)

Confirm geolocation writes to JSON

Confirm user name/email saved

Validate categories render in Browse view

Log bugs & fixes in CHANGELOG.md

## 📈 Weeks 3–4 Growth Strategy Snapshot
Share link via WhatsApp community groups

Partner with local schools / NGOs for collection drives

Run “Record your grandmother’s farming wisdom” campaign

Track metrics: unique users, entries, languages, media attachments, geo coverage

## 🔮 Roadmap (Post-MVP)
AI language auto-detect + suggested translation

Summaries for long agricultural narratives

Speech-to-text for oral histories

Contributor profiles & community badges
