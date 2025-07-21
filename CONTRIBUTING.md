# Contributing to Farming Wisdom Archive

First off, thank you for considering contributing to **Farming Wisdom Archive**!
This project thrives on community participation, and we welcome contributions of all kinds: code, documentation, ideas, and outreach efforts focused on preserving Indian agricultural wisdom.

---

## How to Contribute

### 1. Fork & Clone the Repository
- Fork this repository to your account.
- Clone your fork locally:

    ```bash
    git clone https://code.swecha.org/soai2025/soai-hackathon/farming-wisdom-archive.git
    cd farming-wisdom-archive
    ```

---

### 2. Set Up the Development Environment
- Ensure you have **Python 3.9+** installed.
- Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

- Run the app locally:
    ```bash
    streamlit run app/main.py
    ```

---

### 3. Branch Workflow
- Create a new branch for your changes:
    ```bash
    git checkout -b feature/your-feature-name
    ```

- Commit your changes with a clear message:
    ```bash
    git commit -m "feat: Add new farming technique category"
    ```

- Push the branch:
    ```bash
    git push origin feature/your-feature-name
    ```

- Open a **Merge Request (MR)** on the main repository.

---

## Contribution Guidelines

### Code Style
- Follow **PEP 8** for Python.
- Keep code modular (use `helpers.py` for utilities).
- Add comments for clarity, especially for complex logic.

### Features & Fixes
- Discuss major features in **Issues** before coding.
- Each MR should focus on **a single purpose** (bug fix, feature, or improvement).

### Documentation
- Update **README.md** and **REPORT.md** if your changes affect them.
- Add docstrings for all functions and classes.

---

## Project Structure Reminder
```bash
farming-wisdom-archive/
├── app/
│   ├── main.py            # Main Streamlit app
│   └── helpers.py         # Utility functions
├── data_entries/          # Stores Submissions
├── README.md              # Overview
├── REPORT.md              # Detailed report
├── CONTRIBUTING.md        # This file
├── CHANGELOG.md           # Version history
├── requirements.txt       # Dependencies
├── LICENSE                # MIT License
```
---

## Testing Changes
- Test on **low-bandwidth conditions**.
- Validate offline mode using cached/temporary storage.
- Ensure app runs on **Streamlit 1.x** without breaking UI.

---

## Communication
- Use the **Issues** section for bugs and feature requests.
- For discussions, join the team communication channel.

---
