# Datheon Python Internship Projects

Repository containing completed internship programming tasks for **Datheon Python Internship**.

---

## 📁 Projects Included

1. [Hangman Word Guessing Game (Console)](file:///d:/Programs/Daelton/hangman.py)
2. [Stock Portfolio Performance Tracker](file:///d:/Programs/Daelton/portfolio_tracker.py)
3. [Automated File Organizer & Cleanup Utility](file:///d:/Programs/Daelton/organizer.py)

---

## 🗂️ Project 3: Automated File Organizer & Cleanup Utility

### 📌 Overview & Goal
Construct an autonomous desktop automation utility that organizes cluttered directories (such as the `Downloads` or `Desktop` folders) using Python's standard `os` and `shutil` libraries. The script inspects file extensions, creates dynamic category subfolders (`/Documents`, `/Images`, `/Videos`, `/Archives`, `/Code`, `/Audio`, `/Installers`), and relocates files safely with error handling and collision resolution.

### 🛠️ Key Features
- **Comprehensive Extension Mapping**: Categorizes files into `/Documents`, `/Images`, `/Videos`, `/Audio`, `/Archives`, `/Code`, and `/Installers`.
- **Safe Relocation**: Uses `os.scandir()` for fast traversal and `shutil.move()` for relocation.
- **Naming Collision Protection**: Detects existing destination files and renames automatically (e.g. `report (1).pdf`) instead of overwriting.
- **Robust Exception Handling**: Encapsulated in `try-except` blocks handling `PermissionError`, `FileExistsError`, and general `OSError`.
- **Dry-Run Preview**: Preview proposed file relocations prior to executing real file moves.
- **Built-in Demo Generator**: Creates a temporary `Demo_Cluttered_Folder` for testing.
- **Execution Summary Report**: Formatted terminal output detailing total scanned, relocated, skipped files, and breakdown per category.

### 🚀 How to Run the File Organizer

```bash
python organizer.py
```

### 📸 Sample Output

```text
Target Directory: C:\Users\User\Downloads
Mode: [LIVE EXECUTION - Moving Files]
-----------------------------------------------------------------
[MOVED] Quarterly_Report.pdf  --> /Documents/Quarterly_Report.pdf
[MOVED] screenshot_app.png    --> /Images/screenshot_app.png
[MOVED] demo_recording.mp4    --> /Videos/demo_recording.mp4
[MOVED] project_backup.zip    --> /Archives/project_backup.zip
[MOVED] script.py             --> /Code/script.py

=================================================================
           AUTOMATED FILE ORGANIZER - EXECUTION SUMMARY
=================================================================
Total Files Scanned      : 13
Total Files Relocated    : 13
Total Files Skipped      : 0
Errors Encountered       : 0
-----------------------------------------------------------------
Breakdown by Category:
  • /Documents       : 5 file(s)
  • /Images          : 2 file(s)
  • /Code            : 2 file(s)
  • /Videos          : 1 file(s)
  • /Archives        : 1 file(s)
  • /Audio           : 1 file(s)
  • /Installers      : 1 file(s)
=================================================================
✓ Directory cleanup completed successfully.
```

---

## 📈 Project 2: Stock Portfolio Performance Tracker

### 📌 Overview & Goal
An investment portfolio tracking utility that calculates real-time portfolio valuation, tracks percentage gain/loss per holding, and automatically logs transactions and performance snapshots to external CSV files.

### 🛠️ Key Features
- **Holdings Management**: Add, average down, or sell shares for any stock ticker (e.g. `AAPL`, `NVDA`, `MSFT`, `TSLA`).
- **Real-Time Market Valuation**: Fetches live quotes via Yahoo Finance API with smooth fallback mechanisms.
- **Performance Analytics**: Calculates cost basis, current market value, and percentage gain/loss.
- **Automated CSV Persistence**: Logs every transaction to `portfolio_performance_log.csv` and summary snapshots to `portfolio_summary_snapshots.csv`.

```bash
python portfolio_tracker.py
```

---

## 🎮 Project 1: Hangman Word Guessing Game

### 📌 Overview & Goal
An interactive, modular console game implementing string manipulation, sets, and control flow.

### 🛠️ Key Features
- **Visual ASCII Gallows Art**: 7 visual stages updating dynamically with each incorrect attempt (max 6 mistakes).
- **Masked Word Display**: Displays unrevealed letters as underscores (e.g., `_ A _ H E O N`).
- **Duplicate Guess Prevention**: Informs user of previously entered letters without penalty deduction.
- **Categorized Word Pool**: Predefined word bank with replayability.

```bash
python hangman.py
```
