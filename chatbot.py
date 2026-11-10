"""
Rule-Based Interactive Terminal Assistant / Chatbot
Internship Project: Datheon Python Internship

Features:
- Multi-intent recognition using keyword scoring and regular expression pattern matching.
- JSON dataset with business hours, product FAQs, pricing, technical support, and contacts.
- Input normalization (lowercase, punctuation removal, whitespace trimming, regex tokenization).
- Conversational state management:
    INIT -> GREETING -> INTENT_RESOLUTION -> ESCALATION/EXIT
- Confidence scoring with graceful fallback responses.
- Quick exit triggers ('bye', 'exit', 'quit').
- Interactive 'help' command displaying supported topics.
"""

import json
import os
import random
import re
import sys

DATASET_FILE = "chatbot_intents.json"

# Fallback in-memory dataset in case JSON file is missing
DEFAULT_INTENTS = {
    "bot_name": "Datheon Assistant",
    "intents": [
        {
            "tag": "greeting",
            "patterns": [r"\b(hi|hello|hey|greetings|morning|evening)\b"],
            "keywords": ["hi", "hello", "hey", "greetings"],
            "responses": ["Hello! How can I assist you with Datheon products today?"]
        },
        {
            "tag": "business_hours",
            "patterns": [r"\b(business|office|working)\s*(hours|timing|time)\b", r"\b(when|open|close)\b"],
            "keywords": ["hours", "timings", "open", "close", "time"],
            "responses": ["We are open Monday to Friday, 9:00 AM - 6:00 PM EST."]
        },
        {
            "tag": "exit",
            "patterns": [r"\b(bye|exit|quit|goodbye)\b"],
            "keywords": ["bye", "exit", "quit"],
            "responses": ["Thank you for chatting with us. Goodbye!"]
        }
    ],
    "fallbacks": [
        "I'm sorry, I didn't quite catch that. You can ask about 'business hours', 'pricing', or 'products'."
    ]
}


class ConversationalState:
    """Manages the dialogue state throughout the user session."""
    INIT = "INIT"
    ACTIVE = "ACTIVE"
    AWAITING_CLARIFICATION = "AWAITING_CLARIFICATION"
    RESOLVED = "RESOLVED"
    TERMINATED = "TERMINATED"


class DatheonChatbot:
    """Rule-based conversational agent with multi-intent recognition."""

    def __init__(self, dataset_path=DATASET_FILE):
        self.state = ConversationalState.INIT
        self.dataset = self._load_dataset(dataset_path)
        self.bot_name = self.dataset.get("bot_name", "Datheon Assistant")
        self.intents = self.dataset.get("intents", [])
        self.fallbacks = self.dataset.get("fallbacks", [
            "I'm sorry, could you rephrase that? Try asking about hours, pricing, or product features."
        ])
        self.last_matched_intent = None
        self.interaction_count = 0

    def _load_dataset(self, path):
        """Loads intents and responses from JSON file or uses defaults."""
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Warning] Failed loading {path}: {e}. Using internal defaults.")
        return DEFAULT_INTENTS

    def normalize_input(self, text):
        """
        Normalizes raw user input:
        - Converts to lowercase
        - Strips whitespace
        - Removes special punctuation while keeping word boundaries
        """
        if not text:
            return ""
        text = text.lower().strip()
        # Clean up repeated punctuation
        cleaned = re.sub(r"[^\w\s\?]", " ", text)
        return " ".join(cleaned.split())

    def match_intent(self, user_text):
        """
        Determines the best matching intent using:
        1. Regular Expression patterns (high weight: +3)
        2. Keyword occurrences (weight: +1 per hit)

        Returns (best_intent, confidence_score)
        """
        best_intent = None
        highest_score = 0

        # Check for clean exit keywords first
        exit_tokens = {"bye", "exit", "quit", "q", "leave"}
        words = set(re.findall(r"\b\w+\b", user_text))
        if words.intersection(exit_tokens) and len(words) <= 3:
            for intent in self.intents:
                if intent["tag"] == "exit":
                    return intent, 10

        # Evaluate all intents
        for intent in self.intents:
            score = 0

            # 1. Regex Pattern Matching
            for pattern in intent.get("patterns", []):
                try:
                    if re.search(pattern, user_text, re.IGNORECASE):
                        score += 3
                except re.error:
                    continue

            # 2. Keyword Matching
            keywords = intent.get("keywords", [])
            for kw in keywords:
                if kw in words or re.search(rf"\b{re.escape(kw)}\b", user_text):
                    score += 1

            if score > highest_score:
                highest_score = score
                best_intent = intent

        return best_intent, highest_score

    def get_response(self, user_input):
        """
        Processes normalized user input, identifies intent,
        updates state machine, and returns contextual output.
        """
        self.interaction_count += 1
        normalized = self.normalize_input(user_input)

        if not normalized:
            return "It seems you didn't say anything. How can I assist you today?"

        # Help command
        if normalized in ["help", "options", "topics", "commands"]:
            return self._get_help_menu()

        # Intent classification
        matched_intent, confidence = self.match_intent(normalized)

        # Minimum confidence threshold (score >= 1)
        if matched_intent and confidence >= 1:
            self.last_matched_intent = matched_intent["tag"]

            if matched_intent["tag"] == "exit":
                self.state = ConversationalState.TERMINATED
            else:
                self.state = ConversationalState.ACTIVE

            # Pick a randomized response from intent's response pool
            responses = matched_intent.get("responses", [])
            return random.choice(responses) if responses else "How can I help you further?"

        # Fallback handling when confidence is low
        self.state = ConversationalState.AWAITING_CLARIFICATION
        return random.choice(self.fallbacks)

    def _get_help_menu(self):
        """Returns list of topics the chatbot can handle."""
        return (
            "Here are the topics I can help you with:\n"
            "  🕒 Business Hours       - Ask 'What are your working hours?'\n"
            "  📍 Location & Contact   - Ask 'Where are you located?' or 'Support contact email'\n"
            "  💳 Pricing & Plans      - Ask 'How much does it cost?' or 'Free trial info'\n"
            "  🚀 Product Features     - Ask 'What products do you offer?'\n"
            "  🔄 Refund Policy        - Ask 'What is your refund and cancellation policy?'\n"
            "  🛠️ Technical Support    - Ask 'I found a bug' or 'API not working'\n"
            "  🚪 Exit Assistant       - Type 'bye', 'exit', or 'quit'"
        )

    def run_cli(self):
        """Main conversational loop in terminal."""
        print("=" * 65)
        print(f"      {self.bot_name.upper()} - CUSTOMER & PRODUCT SUPPORT")
        print("           Datheon Python Internship Project")
        print("=" * 65)
        print("Type 'help' to see supported topics, or 'exit' / 'bye' to quit.\n")
        print(f"{self.bot_name}: Hello! I'm your Datheon virtual support assistant. How can I assist you today?")

        self.state = ConversationalState.ACTIVE

        while self.state != ConversationalState.TERMINATED:
            try:
                user_msg = input("\nYou: ").strip()
                if not user_msg:
                    continue

                reply = self.get_response(user_msg)
                print(f"\n{self.bot_name}: {reply}")

                if self.state == ConversationalState.TERMINATED:
                    print("\n[Chat session ended]")
                    break

            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{self.bot_name}: Goodbye! Have a great day.")
                break


def main():
    bot = DatheonChatbot()
    bot.run_cli()


if __name__ == "__main__":
    main()
