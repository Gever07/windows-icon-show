# 🎭 Windows Icon Show (`windows-icon-show`)

A fun Python script that takes control of your Windows desktop icons and animates them in real time into dynamic geometric shapes using the Win32 API and mathematical parametric equations.

---

## ⚠️ Important Prerequisite (Must Read Before Running!)

For the icons to move freely across the screen, **you must disable Windows' automatic icon grid alignment** before running the script:

1. **Right-click** on an empty area of your Desktop.
2. Hover over **View** (תצוגה).
3. **Uncheck** **Align icons to grid** (יישר סמלים לרשת)[cite: 5].
4. *(Optional)* Make sure **Auto arrange icons** (סדר סמלים באופן אוטומטי) is also **unchecked**.

> **Note:** If "Align icons to grid" remains enabled, Windows will snap the icons back into place and block the smooth animation.

---

## ✨ Features & Show Stages

The script automatically minimizes all open windows, saves your original icon layout, displays a topmost countdown HUD, and runs a 5-stage choreographed show:

1. **🌪️ CHAOS (5s):** Icons scatter randomly across the entire screen.
2. **😊 SMILE (4s):** Icons form a smiley face with eyes and a curved mouth.
3. **❤️ HEART (4s):** Icons arrange into a parametric heart curve.
4. **⭐ STAR (4s):** Icons form a 5-pointed mathematical star (rose curve).
5. **♾️ INFINITY (4s):** Icons trace a continuous Lemniscate of Bernoulli (infinity symbol).

At the end of the show, a popup dialog asks if you want to **automatically restore all your icons to their exact original positions**.

---

## 🛠️ Requirements & Installation

* **OS:** Windows 10 / Windows 11
* **Python:** Python 3.7+

### Install Dependencies
Open your terminal / Command Prompt and install the required libraries:

pip install pywin32 pyautogui

🚀 Usage
Make sure you have at least 10–15 icons on your desktop for the shapes to look clear and recognizable.

Uncheck Align icons to grid on your desktop (see instructions above)[cite: 5].

Run the script:

python desktop_show.py
(Note: Make sure the filename matches whatever you named your .py file).

🧠 How It Works Under the Hood
Win32 API (win32gui, commctrl): Locates the desktop's underlying SysListView32 handle (Progman -> SHELLDLL_DefView -> SysListView32).

Cross-Process Memory Reading (ctypes): Uses OpenProcess, VirtualAllocEx, and ReadProcessMemory to safely read LVM_GETITEMPOSITION coordinates from explorer.exe's memory space.

Real-Time Positioning: Sends LVM_SETITEMPOSITION messages at 20 FPS (0.05s intervals) to smoothly animate every icon.

Tkinter HUD: Creates a frameless, always-on-top overlay window showing the current stage and remaining time.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
