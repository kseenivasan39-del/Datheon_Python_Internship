# Datheon Python Internship - Hangman Word Guessing Game

An interactive, modular console-based Hangman game built in Python 3 using only Python's standard library.

---

## 📌 Project Overview & Features
- **Visual ASCII Gallows Art**: Features 7 stages (0 to 6 incorrect guesses) reflecting each incorrect attempt.
- **Categorized Word Pool**: Randomly picks words across categories (*Programming*, *Animals*, *Countries*, *Science & Tech*).
- **Duplicate Guess Prevention**: Informs the user if a letter was previously guessed and does not penalize their attempts.
- **Input Validation**: Rejects numbers, special characters, and multi-letter inputs gracefully.
- **Attempt Tracking**: Limits incorrect guesses to 6 attempts and displays remaining chances and guessed letters.
- **Scoreboard & Replay Support**: Tracks wins across consecutive rounds.

---

## 🛠️ Requirements & Tech Stack
- **Language**: Python 3.x
- **Standard Library**: `random`, `os`
- **IDE**: VS Code / PyCharm / Any terminal

---

## 🚀 How to Run the Game

```bash
python hangman.py
```

---

## 📸 Sample Gameplay Preview

```text
=============================================
 Category: Programming
=============================================

       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    
Word: P Y T H _ N

Guessed letters: A, E, H, P, T, Y
Attempts remaining: 3/6
---------------------------------------------
Enter a letter guess: O

 Great guess! 'O' is in the word.

🎉 CONGRATULATIONS! YOU WON! 🎉
You correctly revealed the word: PYTHON
```

---

## 📤 Submission Instructions Checklist
1. **GitHub Repository**:
   - Initialize git and push to a repository named: `Datheon_Python_Internship`
   ```bash
   git init
   git add .
   git commit -m "feat: implement console-based hangman game"
   git remote add origin https://github.com/<your-username>/Datheon_Python_Internship.git
   git branch -M main
   git push -u origin main
   ```
2. **LinkedIn Share**:
   - Post a demo screenshot/video of your terminal gameplay.
   - Tag **@Datheon**.
