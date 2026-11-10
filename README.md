# Datheon Python Internship Projects

Repository containing completed internship programming tasks for **Datheon Python Internship**.

---

## 📁 Projects Included

1. [Hangman Word Guessing Game (Console)](file:///d:/Programs/Daelton/hangman.py)
2. [Stock Portfolio Performance Tracker](file:///d:/Programs/Daelton/portfolio_tracker.py)
3. [Automated File Organizer & Cleanup Utility](file:///d:/Programs/Daelton/organizer.py)
4. [Rule-Based Interactive Terminal Assistant / Chatbot](file:///d:/Programs/Daelton/chatbot.py)
5. [OOP Architecture: Enterprise Smart Inventory & Asset System](file:///d:/Programs/Daelton/inventory.py)

---

## 🏛️ Project 5: Enterprise Smart Inventory & Asset System (OOP)

### 📌 Overview & Goal
Architect a production-grade inventory and asset management system using strict Object-Oriented Programming (OOP) in Python. Demonstrates all major OOP paradigms: **Abstraction**, **Inheritance**, **Polymorphism**, **Encapsulation**, and **Magic / Dunder Methods**.

### 🛠️ Architecture & Core Components

- **`models.py`**:
  - **Abstract Base Class (`LibraryItem` / `Item`)**: Uses `abc.ABC` and `@abstractmethod` to enforce contracts for `calculate_fee()` and `display_metadata()`.
  - **Derived Classes**:
    - `Book`: Inherits `LibraryItem`, implements page length dunder (`__len__`), author, ISBN, and standard 14-day lending policies.
    - `Magazine`: Inherits `LibraryItem`, tracks issue numbers and periodic publication schedules.
    - `DigitalMedia`: Inherits `LibraryItem`, handles audio/video/ebook formats, megabyte file sizes, and accelerated digital lending windows.
  - **Strict Encapsulation**: Private attributes (`__price`, `__borrow_date`, `__is_checked_out`, `__borrower_name`) safeguarded with `@property` and `@setter` validation preventing invalid states (e.g., negative prices).
  - **Dunder / Magic Methods**:
    - `__str__`: User-friendly human-readable status representation.
    - `__repr__`: Developer-oriented representation for debugging.
    - `__len__`: Polymorphic length reflection (Book pages, Magazine issues, Digital megabytes).
    - `__eq__`: Identity equality matching on unique `item_id`.
    - `__lt__`: Natural sorting on title.

- **`inventory.py`**:
  - **`InventoryManager`**: Orchestrates checkout and return workflows, enforces borrowing rules, calculates late fees on returns, and generates structured tabular audit reports.
  - Built-in interactive terminal menu and automated OOP test suite (`Option 6`).

### 🚀 How to Run the Inventory System

```bash
python inventory.py
```

### 📸 Sample Tabular Audit Report

```text
===================================================================================================================
                     ENTERPRISE SMART INVENTORY AUDIT REPORT - DATHEON CORPORATE ENTERPRISE LIBRARY
===================================================================================================================
ID       Type           Title                               Price Status             Borrower           Len/Size  
-------------------------------------------------------------------------------------------------------------------
B-101    Book           Clean Code: Agile Software     $    45.00 CHECKED OUT        Alice Johnson      464 units 
D-302    DigitalMedia   Data Science Masterclass       $    65.00 AVAILABLE          -                  320 units 
B-103    Book           Design Patterns (GoF)          $    54.00 AVAILABLE          -                  395 units 
M-202    Magazine       Harvard Business Review        $    18.00 AVAILABLE          -                  118 units 
M-201    Magazine       IEEE Software Trends           $    15.00 AVAILABLE          -                  42 units  
D-301    DigitalMedia   Microservices Architecture     $    89.00 CHECKED OUT        Bob Smith          1450 units
B-102    Book           Python Crash Course            $    38.50 AVAILABLE          -                  544 units 
-------------------------------------------------------------------------------------------------------------------
Total Tracked Assets : 7
Active Checkouts     : 2 item(s)
Total Asset Valuation: $324.50
===================================================================================================================
```

---

## 🤖 Project 4: Rule-Based Interactive Terminal Assistant / Chatbot

### 📌 Overview & Goal
Build a responsive, conversational assistant with multi-intent recognition, keyword extraction, and regular expression pattern matching.

```bash
python chatbot.py
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
