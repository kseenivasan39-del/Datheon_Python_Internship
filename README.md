# Datheon Python Internship Projects

Repository containing completed internship programming tasks for **Datheon Python Internship**.

---

## 📁 Projects Included

1. [Hangman Word Guessing Game (Console)](file:///d:/Programs/Daelton/hangman.py)
2. [Stock Portfolio Performance Tracker](file:///d:/Programs/Daelton/portfolio_tracker.py)

---

## 📈 Project 2: Stock Portfolio Performance Tracker

### 📌 Overview & Goal
Build an investment portfolio tracking utility in Python 3. The program calculates real-time portfolio valuation, tracks percentage gain/loss per holding, and automatically logs transactions and performance snapshots to external CSV files.

### 🛠️ Key Features
- **Holdings Management**: Add, average down, or sell shares for any stock ticker (e.g. `AAPL`, `NVDA`, `MSFT`, `TSLA`).
- **Real-Time Market Valuation**: Fetches live quotes via Yahoo Finance API with smooth fallback mechanisms.
- **Performance Analytics**: Calculates:
  - Total Invested Capital
  - Total Current Valuation
  - Individual Gain / Loss ($ and %)
  - Portfolio-wide Net Profit / Loss ($ and %)
- **Automated CSV Persistence**:
  - `portfolio_performance_log.csv`: Transaction-level audit trail (`BUY`, `SELL`, share counts, prices, timestamps).
  - `portfolio_summary_snapshots.csv`: Valuation summary snapshots logged on every report view.
- **Multi-session Storage**: Positions are persistently stored in `portfolio_data.json`.

### 🚀 How to Run the Portfolio Tracker

```bash
python portfolio_tracker.py
```

### 📸 Sample Dashboard Output

```text
===============================================================================================
                    INVESTMENT PORTFOLIO PERFORMANCE DASHBOARD
===============================================================================================
Symbol       Shares   Buy Price     Current     Invested    Cur Value   Gain/Loss($)    Gain(%)
-----------------------------------------------------------------------------------------------
AAPL          10.00     $180.00     $225.50    $1,800.00    $2,255.00       +$455.00    +25.28%
MSFT           5.00     $400.00     $430.20    $2,000.00    $2,151.00       +$151.00     +7.55%
NVDA          15.00     $115.50     $138.80    $1,732.50    $2,082.00       +$349.50    +20.17%
-----------------------------------------------------------------------------------------------
Total Invested Capital : $5,532.50
Current Portfolio Value: $6,488.00
Net Total Profit/Loss  : +$955.50 (+17.27%)
Active Holdings Count  : 3
===============================================================================================
✓ Summary snapshot logged to 'portfolio_summary_snapshots.csv'.
```

---

## 🎮 Project 1: Hangman Word Guessing Game

### 📌 Overview
An interactive, modular console game implementing string manipulation, sets, and control flow.

### 🛠️ Features
- **Visual ASCII Gallows Art**: 7 visual stages updating dynamically with each incorrect attempt (max 6 mistakes).
- **Masked Word Display**: Displays unrevealed letters as underscores (e.g., `_ A _ H E O N`).
- **Duplicate Guess Prevention**: Informs user of previously entered letters without penalty deduction.
- **Categorized Word Pool**: Predefined word bank with replayability.

### 🚀 How to Run Hangman

```bash
python hangman.py
```
