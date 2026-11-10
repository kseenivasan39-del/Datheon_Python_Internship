"""
Hangman Word Guessing Game (Console)
Internship Project: Datheon Python Internship

Features:
- Visual ASCII gallows art updating with each incorrect guess (6 attempts).
- Random word selection from predefined categories.
- Tracks guessed letters (correct & incorrect).
- Prevents duplicate guesses without deducting penalties.
- Input validation (single alphabetic characters only).
- Clean, modular structure with replay option.
"""

import random
import os

# ASCII art stages corresponding to incorrect guesses (0 to 6)
HANGMAN_STAGES = [
    # 0 incorrect guesses (Initial empty gallows)
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    # 1 incorrect guess (Head)
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    # 2 incorrect guesses (Head + Torso)
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    # 3 incorrect guesses (Head + Torso + One Arm)
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    # 4 incorrect guesses (Head + Torso + Both Arms)
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    # 5 incorrect guesses (Head + Torso + Both Arms + One Leg)
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    # 6 incorrect guesses (Full body - Game Over)
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

# Word bank categorized for replayability
WORDS_BY_CATEGORY = {
    "Programming": [
        "PYTHON", "VARIABLE", "FUNCTION", "LOOP", "SYNTAX",
        "STRING", "INTEGER", "BOOLEAN", "DICTIONARY", "COMPILER"
    ],
    "Animals": [
        "ELEPHANT", "GIRAFFE", "DOLPHIN", "KANGAROO", "PENGUIN",
        "PANTHER", "OCTOPUS", "CHEETAH", "SQUIRREL", "FLAMINGO"
    ],
    "Countries": [
        "CANADA", "BRAZIL", "GERMANY", "JAPAN", "AUSTRALIA",
        "FRANCE", "INDIA", "MEXICO", "EGYPT", "ITALY"
    ],
    "Science & Tech": [
        "GRAVITY", "QUANTUM", "NEURON", "GALAXY", "ROBOTICS",
        "ALGORITHM", "SATELLITE", "MICROSCOPE", "FUSION", "ELECTRON"
    ]
}

MAX_INCORRECT_ATTEMPTS = 6


def get_random_word():
    """Selects and returns a random category and word."""
    category = random.choice(list(WORDS_BY_CATEGORY.keys()))
    word = random.choice(WORDS_BY_CATEGORY[category])
    return category, word


def display_game_status(stage_index, guessed_letters, secret_word, category):
    """Renders the gallows, word progress, and tracked guesses."""
    print("\n" + "=" * 45)
    print(f" Category: {category}")
    print("=" * 45)
    print(HANGMAN_STAGES[stage_index])

    # Display word with revealed letters and underscores
    revealed = [letter if letter in guessed_letters else "_" for letter in secret_word]
    print("Word: " + " ".join(revealed))

    # Display tracked letters
    sorted_guesses = sorted(list(guessed_letters))
    guessed_str = ", ".join(sorted_guesses) if sorted_guesses else "None"
    print(f"\nGuessed letters: {guessed_str}")
    remaining_attempts = MAX_INCORRECT_ATTEMPTS - stage_index
    print(f"Attempts remaining: {remaining_attempts}/{MAX_INCORRECT_ATTEMPTS}")
    print("-" * 45)


def get_player_guess(already_guessed):
    """
    Prompts player for input and validates:
    - Must be a single character
    - Must be an alphabetical letter
    - Checks if already guessed (informs player without deducting penalty)
    """
    while True:
        user_input = input("Enter a letter guess: ").strip().upper()

        if len(user_input) != 1 or not user_input.isalpha():
            print(">> Invalid input. Please enter a single alphabetic letter (A-Z).")
            continue

        if user_input in already_guessed:
            print(f">> You already guessed '{user_input}'. No penalty deducted. Try another letter!")
            continue

        return user_input


def play_round():
    """Executes a single round of the Hangman game."""
    category, secret_word = get_random_word()
    guessed_letters = set()
    incorrect_guesses = 0
    unique_secret_letters = set(secret_word)

    print("\nWelcome to Hangman!")
    print(f"Guess the secret word letter-by-letter before the gallows is complete ({MAX_INCORRECT_ATTEMPTS} attempts).")

    while incorrect_guesses < MAX_INCORRECT_ATTEMPTS:
        display_game_status(incorrect_guesses, guessed_letters, secret_word, category)

        # Check win condition before next guess
        if unique_secret_letters.issubset(guessed_letters):
            print("\n🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"You correctly revealed the word: {secret_word}")
            return True

        guess = get_player_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in unique_secret_letters:
            print(f"\n Great guess! '{guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print(f"\n Incorrect! '{guess}' is not in the word.")

    # Final display for game over
    display_game_status(incorrect_guesses, guessed_letters, secret_word, category)
    print("\n💀 GAME OVER! YOU RAN OUT OF ATTEMPTS. 💀")
    print(f"The secret word was: {secret_word}")
    return False


def main():
    """Main game loop with replay option and score tracking."""
    print("*" * 45)
    print("      HANGMAN WORD GUESSING GAME")
    print("    Datheon Python Internship Task")
    print("*" * 45)

    rounds_played = 0
    rounds_won = 0

    while True:
        rounds_played += 1
        won = play_round()
        if won:
            rounds_won += 1

        print(f"\nScoreboard: {rounds_won} Win(s) / {rounds_played} Round(s) Played")

        # Ask to replay
        while True:
            choice = input("\nWould you like to play again? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                break
            elif choice in ['n', 'no']:
                print("\nThanks for playing Hangman! Have a great day!")
                return
            else:
                print("Please enter 'y' for Yes or 'n' for No.")


if __name__ == "__main__":
    main()
