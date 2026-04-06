<div align="center">

# 🎯 FOCUS STUDIO

**Level up your productivity. Gamify your grind.**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/Tkinter-Modern-orange?logo=python)](https://docs.python.org/3/library/tkinter.html)
[![Database](https://img.shields.io/badge/SQLite-Offline_First-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Active-success?logo=github)](https://github.com/)

🔥 **STOP SCROLLING. START GRINDING.** 🔥  
Focus Studio isn't just another boring Pomodoro timer-it’s a **high-octane, adrenaline-fueled Productivity RPG**. Transform your mundane study sessions into a relentless, interactive quest where **every second of your hyper-focus translates directly into raw XP, brutal leaderboard domination, and absolute academic supremacy!** If you're tired of losing to distractions, this is your ultimate weapon!

[**Features**](#-key-features) • [**Installation**](#-installation--setup) • [**Architecture**](#-system-architecture--file-structure)

</div>

---

## 📸 App Showcase

<!-- Update these with your actual image paths! For example: src="docs/timer.png" -->
<div align="center">
  <img src="https://via.placeholder.com/800x450.png?text=Main+Dashboard+%26+Timer+Screenshot+Here" width="800" alt="Dashboard">
  <br>
  <i>Focus Studio - Level up your focus.</i>
</div>

---

## 📸 App Showcase

<!-- Update these with your actual image paths! For example: src="docs/timer.png" -->
<div align="center">
  <img src="https://via.placeholder.com/800x450.png?text=Main+Dashboard+%26+Timer+Screenshot+Here" width="800" alt="Dashboard">
  <br>
  <i>Focus Studio - Level up your focus.</i>
</div>

---

## ✨ Key Features

Transform the way you work and study with our suite of built-in tools.

| Feature                    | The "Level Up" Factor                                                             |
| :------------------------- | :-------------------------------------------------------------------------------- |
| **⚔️ Quest Timer**         | Pomodoro-style clock that rewards you with XP. Level up as you master your focus. |
| **📅 Mission Planner**     | Organize subjects and schedule study blocks like a tactical quest log.            |
| **🎵 Integrated Jukebox**  | Built-in MP3 player to maintain "Flow State" without leaving the app.             |
| **🏆 Global Leaderboards** | Compare your "Focus Power" with friends and stay motivated through competition.   |
| **📊 Deep Analytics**      | Visual charts (via custom logic) to track your daily and weekly progress.         |
| **🛡️ Local Fortress**      | 100% offline. Your data stays on your machine in a secure SQLite database.        |

---

## 🏗️ System Architecture & File Structure

Here is exactly how the game engine (codebase) is structured. **This is for this, and that is for that:**

<details open>
<summary><b>📂 Root Files (The Core)</b></summary>
<br>

- **`run.py`**: The ultimate entry point. Run this file to boot up the application.
- **`run.spec`**: Configuration file used by PyInstaller if you want to build the app into a `.exe`.
- **`settings.json`**: Saves local application configurations dynamically.
- **`requirements.txt`**: The shopping list of Python packages required to run the project.
- **`focus_studio.db`**: Your offline SQLite database where all user data, XP, and stats are securely stored.
- **`PROJECT_REPORT.md`**: Formal academic documentation and write-up for the project.
- **`.gitignore`**: Tells Git which files (like caches or databases) to ignore when pushing to GitHub.
</details>

<details open>
<summary><b>🧠 <code>/logic</code> (The Brain Layer)</b></summary>
<br>

This folder contains background operations and math. It has zero graphical UI components.

- **`auth.py`**: Handles user login, registration, and session security.
- **`database.py`**: The engine for all SQLite CRUD (Create, Read, Update, Delete) operations.
- **`badges.py`**: The mathematical logic behind calculating XP, leveling up, and unlocking achievements.
- **`utils.py`**: A suite of helper functions (like time parsers or string formatters) used everywhere.
</details>

<details open>
<summary><b>🎨 <code>/views</code> (The UI Layer)</b></summary>
<br>

This folder contains the actual Tkinter screens you interact with.

- **`app.py`** & **`main.py`**: The main application controllers and window containers that route you between screens.
- **`timer.py`**: The heart of the app-the gamified interactive Pomodoro clock interface.
- **`analytics.py`**: Takes raw stats from the database and draws beautiful visual graphs for tracking.
- **`music.py`**: The UI and background threading controller for the built-in MP3 player.
- **`planner.py`**: The organizational UI for setting study blocks and quest logs.
- **`social.py`**: Interface for adding friends and managing social features.
- **`leaderboard.py`**: UI that ranks users based on their "Focus Power" and XP.
- **`settings.py`**: The screen where users can tweak application preferences.
</details>

<details open>
<summary><b>💄 <code>/styles</code> (The CSS Alternative)</b></summary>
<br>

- **`theme.py`**: The centralized styling manager. Instead of hardcoding hex colors everywhere, all visual assets, fonts, and dark mode colors are imported from here.
</details>

---

## 🛠️ Installation & Setup

Ready to start your first quest? Follow these steps to deploy Focus Studio.

### 1. Requirements

Ensure you have **Python 3.11 or higher** installed on your system.

### 2. Quick Start

Open your terminal, clone the repository, and run the following commands:

```bash
# Clone the repository
git clone https://github.com/yourusername/focus-studio.git
cd focus-studio

# Install dependencies
pip install -r requirements.txt

# Launch the application
python -m views.main
```

---

## 💡 Why Focus Studio?

Most study apps are clinical and boring. We built **Focus Studio** to bridge the gap between "needing to work" and "wanting to progress." By using local storage for privacy and a custom-styled UI for aesthetics, it provides a distraction-free environment where the hardest part of being a student-starting-becomes the most rewarding.

---

<div align="center">

_Created by **Saurabh Gandhi** | **SY ECM 18** | WIT Solapur_

**[⬆ Back to Top](#-focus-studio)**

</div>
