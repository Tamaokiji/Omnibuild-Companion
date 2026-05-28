# OmniBuild Companion - User Manual & Setup Guide

Welcome to the **OmniBuild Companion**, a modular desktop utility built with Python and Flet. This application acts as a comprehensive build finder and companion dashboard for managing character gear, team compositions, and tracking profiles.

---

## 🛠️ System Requirements & Prerequisites

To run this application locally, you must have Python installed and configured correctly on your system environment.

### 1. Python Installation
* Download the official installer from [python.org/downloads](https://www.python.org/downloads/).
* **CRUCIAL SETUP STEP:** Run the installer and ensure you check the box at the very bottom that reads: **"Add python.exe to PATH"**. If this box is missed, the terminal will not recognize any layout execution commands.
* If prompted at the end of the installation window, select the option to **"Disable path length limit"** to prevent deep file-system nested path errors.

### 2. Windows Troubleshooting (If Python Command Fails)
If your terminal states that Python was not found or immediately opens the Microsoft Store when running a command:
1. Open the Windows **Start Menu** and search for **"Manage app execution aliases"**.
2. Scroll down to locate the toggles for `python.exe` and `python3.exe`.
3. Switch **both** toggles to **OFF**.
4. Completely close and reopen your terminal window to apply the change.

---

## 📥 Installation & Dependency Configuration

1. **Download the Project Repository:**
   * Download the repository ZIP file from GitHub.
   * Extract the contents of the ZIP completely to your local computer (e.g., your Desktop).

2. **Open the Terminal Workspace:**
   * Open your system terminal (PowerShell on Windows, or Terminal on macOS/Linux).
   * Navigate (`cd`) directly into the extracted project folder level where `main.py`, `app.py`, and `mobile_app.py` reside.

3. **Install Dependencies:**
   Run the following command to automatically install the required UI layout framework and HTTP utilities:
   ```bash
   python -m pip install flet httpx
