# Datheon Python Internship Projects

Repository containing completed internship programming tasks for **Datheon Python Internship**.

---

## 📁 Projects Included

1. [Hangman Word Guessing Game (Console)](file:///d:/Programs/Daelton/hangman.py)
2. [Stock Portfolio Performance Tracker](file:///d:/Programs/Daelton/portfolio_tracker.py)
3. [Automated File Organizer & Cleanup Utility](file:///d:/Programs/Daelton/organizer.py)
4. [Rule-Based Interactive Terminal Assistant / Chatbot](file:///d:/Programs/Daelton/chatbot.py)

---

## 🤖 Project 4: Rule-Based Interactive Terminal Assistant / Chatbot

### 📌 Overview & Goal
Build a responsive, conversational assistant with multi-intent recognition, keyword extraction, and regular expression pattern matching. The assistant parses queries regarding business hours, product FAQs, pricing plans, tech support, contact details, and refund policies, providing contextual responses, conversational state management, and fallback recovery.

### 🛠️ Key Features
- **Multi-Intent Recognition**: Hybrid approach combining regex pattern evaluation (weight: 3) and keyword token matching (weight: 1).
- **External Dataset (`chatbot_intents.json`)**: Predefined structured intents:
  - `greeting`
  - `business_hours`
  - `pricing_plans`
  - `product_features`
  - `technical_support`
  - `location_contact`
  - `refund_policy`
  - `feedback_thanks`
  - `exit`
- **Input Normalization**: Strips punctuation, trims whitespace, standardizes to lowercase, and extracts word tokens.
- **Dialogue State Machine**: Tracks state (`INIT` ➔ `ACTIVE` ➔ `AWAITING_CLARIFICATION` ➔ `TERMINATED`).
- **Confidence Scoring & Graceful Fallbacks**: Low confidence triggers helpful suggestions.
- **Interactive Help & Exit Commands**: Type `help` to inspect topics; exits cleanly on `bye`, `exit`, or `quit`.

### 🚀 How to Run the Chatbot

```bash
python chatbot.py
```

### 📸 Sample Chat Session

```text
=================================================================
      DATHEON ASSISTANT - CUSTOMER & PRODUCT SUPPORT
           Datheon Python Internship Project
=================================================================
Type 'help' to see supported topics, or 'exit' / 'bye' to quit.

Datheon Assistant: Hello! I'm your Datheon virtual support assistant. How can I assist you today?

You: What are your business hours?
Datheon Assistant: Our business hours are Monday through Friday, 9:00 AM - 6:00 PM EST.

You: How much is your subscription?
Datheon Assistant: We offer three flexible tiers:
  • Starter: Free 14-day trial
  • Professional: $49/month
  • Enterprise: Custom pricing with SLA guarantees.

You: exit
Datheon Assistant: Goodbye! Reach out anytime you need assistance with Datheon products.
[Chat session ended]
```

---

## 🗂️ Project 3: Automated File Organizer & Cleanup Utility

### 📌 Overview & Goal
An autonomous desktop automation utility that organizes cluttered directories (such as the `Downloads` or `Desktop` folders) using Python's standard `os` and `shutil` libraries.

```bash
python organizer.py
```

---

## 📈 Project 2: Stock Portfolio Performance Tracker

### 📌 Overview & Goal
An investment portfolio tracking utility that calculates real-time portfolio valuation, tracks percentage gain/loss per holding, and automatically logs transactions and performance snapshots to external CSV files.

```bash
python portfolio_tracker.py
```

---

## 🎮 Project 1: Hangman Word Guessing Game

### 📌 Overview & Goal
An interactive, modular console game implementing string manipulation, sets, and control flow with 7-stage ASCII gallows art.

```bash
python hangman.py
```
