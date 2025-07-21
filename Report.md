# Project Report: Farming Wisdom Archive

## 1. Project Overview
The **Farming Wisdom Archive** is a multilingual, open-source Streamlit application designed to collect, preserve, and share traditional Indian agricultural knowledge. This includes practices like farming techniques, home remedies, local crop wisdom, and folk stories. The application is built with an **offline-first, low-bandwidth** design to ensure accessibility for contributors in under-connected regions. It also serves as a **corpus collection engine** for open-source AI research, aligning with the viswam.ai challenge.

The primary purpose of the project is to preserve India’s agricultural heritage by crowdsourcing ancestral farming wisdom in multiple Indian languages, contributing to an open dataset for language technology, agricultural studies, and AI models that understand Indian contexts.

## 2. Current Status & Key Achievements (MVP)

The project has achieved its Minimum Viable Product (MVP) stage and is actively being refined with recent updates.

### Key Features Implemented (MVP):
* **User Authentication:** Secure login and registration system for contributors.
* **Knowledge Submission:** Users can submit entries with titles, descriptions, and optional image/audio attachments.
* **Geospatial Tagging:** Auto-detection (via IP) with manual override for location coordinates.
* **Structured Categorization:** Entries are categorized into specific farming domains like Seed Selection, Soil Management, and Pest Control.
* **Multi-Language Support:** Designed to handle content in various Indian languages.
* **Accessibility Tools:** Integration of Speech-to-Text for input and Text-to-Speech for content playback.
* **Data Browse & Search:** Functionality to browse all entries and perform keyword searches with advanced filters.
* **Data Export:** Collected wisdom can be exported in JSONL and CSV formats for research and analysis.
* **Interactive Maps:** A dedicated page to visualize farming wisdom geographically using Folium.
* **Translation Hub:** A feature to translate farming knowledge between different Indian languages.

### Recent Milestones (as of 2025-07-18):
* MVP code has been updated and integrated into the repository.
* Initial work has commenced on backend compatibility for the MVP.
* Frontend UI/UX optimization for the MVP has begun.
* New repository documentation, including Issue Templates, a Code of Conduct, and Contribution Guidelines, have been added to streamline collaboration.

## 3. Technical Architecture & Stack

The application is built primarily with Python and utilizes the Streamlit framework for its interactive web interface.

### Core Technologies:
* **Python:** The primary programming language.
* **Streamlit:** For building the interactive web application.
* **Pandas:** For data manipulation and CSV export.
* **Folium & Streamlit-Folium:** For interactive geographical mapping. 
* **Pillow (PIL):** For image handling. 
* **Bcrypt:** For secure user password hashing and verification.

### AI/NLP Components:
* **`gTTS`:** Used for Text-to-Speech functionality.
* **`SpeechRecognition`:** Used for Speech-to-Text transcription.
* **`geopy`:** Utilized for geocoding location names into coordinates.
* **`deep_translator`:** Provides robust translation and language detection capabilities.

## 4. Team & Roles

The **Farming Wisdom Archive** project is driven by a dedicated team:

* **Venkat Chakradhar Reddy Y** - Project Manager
    * *Connect:* [GitLab Profile](https://code.swecha.org/ChakriYamasani)
* **Jitendra K** - Backend Developer
    * *Connect:* [GitLab Profile](https://code.swecha.org/jitendr21k)
* **Aditya J** - Frontend Lead
    * *Connect:* [GitLab Profile](https://code.swecha.org/Aditya_Tarun_J)
* **Harika P** - UI/UX Designer
    * *Connect:* [GitLab Profile](https://code.swecha.org/harika_putta)
* **HariCharan E** - Deployment & Testing
    * *Connect:* [GitLab Profile](https://code.swecha.org/HARICHARAN22)

## 5. Challenges & Solutions

The project faced a significant technical hurdle related to translation functionality, specifically an `AttributeError` from the `httpcore` module when using `googletrans`. 

This was successfully resolved by migrating the translation and language detection logic from the unstable `googletrans` library to `deep_translator`, and by explicitly pinning the `httpcore` dependency to a compatible version (`0.15.0`) in `requirements.txt`. 

An ongoing challenge is the ephemeral nature of locally stored data (`data_entries/`) when deployed on cloud platforms like Hugging Face Spaces' free tier. 

This necessitates a future migration to a persistent backend database.

## 6. Future Roadmap

The project has a clear roadmap for post-MVP development, focusing on enhancing features and ensuring long-term sustainability:
* Integration with a persistent backend database.
* Enhanced AI-powered summarization of entries.
* Improved microphone access and stability for Speech-to-Text in deployed environments.
* Advanced contributor profiles and community badges.
* Cloud sync for persistent corpus and media files.
* Real-time notifications for new entries (e.g., in user's area).

## 7. Conclusion
