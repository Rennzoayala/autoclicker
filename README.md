# KeepActive 🟢🔴

A lightweight, portable Windows system tray application that prevents PC lockouts and keeps Microsoft Teams, remote desktop sessions, and virtual machines active without interrupting your work.

[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-blue.svg)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- **System Tray Native:** Runs unobtrusively in the Windows taskbar system tray. No taskbar buttons, no terminal or console popups.
- **Visual Status Indicator:**
  - 🟢 **Green circle** = Idle (keep-alive paused)
  - 🔴 **Red circle** = Running (keep-alive active)
- **Configurable Intervals:** Right-click tray menu allows switching between **30s**, **1m**, **2m**, and **5m** intervals on the fly.
- **Settings Persistence:** Remembers your chosen interval across application restarts in a local `config.json`.
- **Invisible Signal:** Emulates a double `Scroll Lock` keypress (`keybd_event`). Because it is sent twice consecutively, the LED state remains unchanged and active typing/work is never disrupted.
- **Single Instance:** Uses a Windows named mutex (`Global\KeepActiveApp`) to prevent duplicate instances from running simultaneously.
- **Truly Portable:** Compiles into a single standalone `.exe` with zero external dependencies or runtimes required on target machines.

---

## 🚀 Quick Start

### Running the Pre-built Executable
1. Download `KeepActive.exe` from the [Releases](https://github.com) page (or compile your own via `build_exe.ps1`).
2. Double-click `KeepActive.exe`.
3. Locate the 🟢 green circle icon in your system tray (click the `^` overflow chevron if hidden).
4. **Right-click** the tray icon:
   - Click **Turn On** (or double-click the icon) to activate.
   - Adjust the **Interval** under the *Interval* submenu.
   - Click **Quit** to exit.

---

## 🛠️ Building from Source

### Prerequisites
- Windows 10 or 11
- Python 3.10+ installed and added to PATH
- PowerShell

### 1. Clone the repository
```bash
git clone https://github.com/your-username/keepactive.git
cd keepactive
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run directly with Python
```bash
python KeepActive.py
```

### 4. Build the standalone EXE
Run the PowerShell build script:
```powershell
.\build_exe.ps1
```
The output executable will be created at `dist\KeepActive.exe`.

---

## ⚙️ Configuration

`KeepActive.exe` saves user preferences in a `config.json` file located in the same directory as the executable:

```json
{
  "interval_sec": 60
}
```

If the file is deleted or missing, the application automatically falls back to the default of 60 seconds (1 minute).

---

## 📁 Repository Structure

```
keepactive/
├── .gitignore             # Standard Python / PyInstaller ignore rules
├── LICENSE                # MIT License
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── KeepActive.py          # Main application source code
├── build_exe.ps1          # Automated single-file build script
└── legacy/                # Original PowerShell & VBS implementations
    ├── Keep-LocalPCCloudActive.ps1
    ├── KeepActive-GUI.ps1
    └── KeepActive.vbs
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
