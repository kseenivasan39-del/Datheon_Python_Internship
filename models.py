"""
Enterprise Smart Inventory & Asset System - Domain Models
Internship Project: Datheon Python Internship

Demonstrates Core OOP Principles:
- Abstraction: Abstract Base Class 'LibraryItem' / 'Item' using 'abc.ABC' and '@abstractmethod'.
- Inheritance: Derived classes 'Book', 'Magazine', 'DigitalMedia' extending 'LibraryItem'.
- Polymorphism: Distinct implementations of 'calculate_fee()' and 'display_metadata()'.
- Encapsulation: Strict private attributes (e.g. __price, __borrow_date, __is_checked_out)
  with '@property' getters, setters, and validation logic.
- Dunder/Magic Methods: '__str__', '__repr__', '__len__', '__eq__', '__lt__'.
"""

from abc import ABC, abstractmethod
from datetime import datetime, date


class LibraryItem(ABC):
    """
    Abstract Base Class for all inventory assets.
    Defines common interface, encapsulated attributes, and enforced contracts.
    """

    def __init__(self, item_id: str, title: str, price: float):
        if not item_id or not isinstance(item_id, str):
            raise ValueError("item_id must be a non-empty string.")
        if not title or not isinstance(title, str):
            raise ValueError("title must be a non-empty string.")

        self._item_id = item_id.strip()
        self._title = title.strip()

        # Strict private attributes
        self.__price = 0.0
        self.__borrow_date = None
        self.__is_checked_out = False
        self.__borrower_name = None

        # Setter with validation
        self.price = price

    # --- Encapsulation: Properties & Setters ---

    @property
    def item_id(self) -> str:
        """Read-only property for item_id."""
        return self._item_id

    @property
    def title(self) -> str:
        """Read-only property for title."""
        return self._title

    @property
    def price(self) -> float:
        """Getter for encapsulated price."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Setter with validation for price."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Price must be a non-negative number. Got: {value}")
        self.__price = float(value)

    @property
    def is_checked_out(self) -> bool:
        """Getter for checkout status."""
        return self.__is_checked_out

    @property
    def borrow_date(self):
        """Getter for checkout date."""
        return self.__borrow_date

    @property
    def borrower_name(self):
        """Getter for current borrower."""
        return self.__borrower_name

    # --- Business Methods ---

    def checkout(self, borrower: str, borrow_date: date = None):
        """Checks out the item to a borrower."""
        if self.__is_checked_out:
            raise RuntimeError(f"Item '{self.title}' (ID: {self.item_id}) is already checked out to {self.__borrower_name}.")
        if not borrower or not isinstance(borrower, str):
            raise ValueError("Borrower name must be a non-empty string.")

        self.__is_checked_out = True
        self.__borrower_name = borrower.strip()
        self.__borrow_date = borrow_date or date.today()

    def return_item(self, return_date: date = None) -> float:
        """
        Marks item as returned, calculates late fees, and resets checkout state.
        Returns total late fee owed.
        """
        if not self.__is_checked_out:
            raise RuntimeError(f"Item '{self.title}' (ID: {self.item_id}) is not currently checked out.")

        ret_date = return_date or date.today()
        days_borrowed = (ret_date - self.__borrow_date).days
        fee = self.calculate_fee(max(0, days_borrowed))

        # Reset state
        self.__is_checked_out = False
        self.__borrower_name = None
        self.__borrow_date = None

        return fee

    # --- Abstraction: Enforced Polymorphic Contracts ---

    @abstractmethod
    def calculate_fee(self, days_held: int) -> float:
        """Computes late fee based on asset-specific lending rules."""
        pass

    @abstractmethod
    def display_metadata(self) -> str:
        """Returns asset-specific technical & inventory metadata."""
        pass

    # --- Dunder / Magic Methods ---

    def __eq__(self, other) -> bool:
        """Equality based on unique item_id."""
        if isinstance(other, LibraryItem):
            return self.item_id == other.item_id
        return False

    def __lt__(self, other) -> bool:
        """Sorting comparison based on item title."""
        if isinstance(other, LibraryItem):
            return self.title.lower() < other.title.lower()
        return NotImplemented

    def __repr__(self) -> str:
        """Developer inspection representation."""
        return f"{self.__class__.__name__}(item_id='{self.item_id}', title='{self.title}', price={self.price})"


# Backward-compatible alias for the suggested approach requirement
Item = LibraryItem


class Book(LibraryItem):
    """
    Derived class representing physical or reference books.
    Demonstrates inheritance, method overriding, and length dunder.
    """

    STANDARD_LENDING_PERIOD_DAYS = 14
    DAILY_LATE_FEE = 0.50

    def __init__(self, item_id: str, title: str, price: float, author: str, pages: int, isbn: str):
        super().__init__(item_id, title, price)
        self.author = author
        if not isinstance(pages, int) or pages <= 0:
            raise ValueError("pages must be a positive integer.")
        self.pages = pages
        self.isbn = isbn

    def calculate_fee(self, days_held: int) -> float:
        """Books allow 14 days free, then $0.50/day late fee."""
        overdue_days = max(0, days_held - self.STANDARD_LENDING_PERIOD_DAYS)
        return round(overdue_days * self.DAILY_LATE_FEE, 2)

    def display_metadata(self) -> str:
        return f"Type: Book | Author: {self.author} | Pages: {self.pages} | ISBN: {self.isbn}"

    def __len__(self) -> int:
        """Returns the number of pages for clean object inspection."""
        return self.pages

    def __str__(self) -> str:
        status = f"Checked out to {self.borrower_name}" if self.is_checked_out else "Available"
        return f"[Book] '{self.title}' by {self.author} ({self.pages} pp.) - Status: {status}"


class Magazine(LibraryItem):
    """
    Derived class representing periodic publications.
    Demonstrates specific lending periods and fee calculations.
    """

    STANDARD_LENDING_PERIOD_DAYS = 7
    DAILY_LATE_FEE = 1.00

    def __init__(self, item_id: str, title: str, price: float, issue_number: int, month: str):
        super().__init__(item_id, title, price)
        self.issue_number = issue_number
        self.month = month

    def calculate_fee(self, days_held: int) -> float:
        """Magazines allow 7 days free, then $1.00/day late fee."""
        overdue_days = max(0, days_held - self.STANDARD_LENDING_PERIOD_DAYS)
        return round(overdue_days * self.DAILY_LATE_FEE, 2)

    def display_metadata(self) -> str:
        return f"Type: Magazine | Issue: #{self.issue_number} | Month: {self.month}"

    def __len__(self) -> int:
        """Returns the issue number."""
        return self.issue_number

    def __str__(self) -> str:
        status = f"Checked out to {self.borrower_name}" if self.is_checked_out else "Available"
        return f"[Magazine] '{self.title}' (Issue #{self.issue_number}, {self.month}) - Status: {status}"


class DigitalMedia(LibraryItem):
    """
    Derived class representing digital assets (Audiobooks, eBooks, Video).
    Demonstrates overriding fee calculations and byte size dunder.
    """

    STANDARD_LENDING_PERIOD_DAYS = 3
    DAILY_LATE_FEE = 2.00

    def __init__(self, item_id: str, title: str, price: float, media_format: str, file_size_mb: int):
        super().__init__(item_id, title, price)
        self.media_format = media_format.upper()
        if not isinstance(file_size_mb, int) or file_size_mb <= 0:
            raise ValueError("file_size_mb must be a positive integer.")
        self.file_size_mb = file_size_mb

    def calculate_fee(self, days_held: int) -> float:
        """Digital media allows 3 days lending, then $2.00/day late fee."""
        overdue_days = max(0, days_held - self.STANDARD_LENDING_PERIOD_DAYS)
        return round(overdue_days * self.DAILY_LATE_FEE, 2)

    def display_metadata(self) -> str:
        return f"Type: DigitalMedia | Format: {self.media_format} | Size: {self.file_size_mb} MB"

    def __len__(self) -> int:
        """Returns the file size in megabytes."""
        return self.file_size_mb

    def __str__(self) -> str:
        status = f"Checked out to {self.borrower_name}" if self.is_checked_out else "Available"
        return f"[DigitalMedia] '{self.title}' [{self.media_format}, {self.file_size_mb}MB] - Status: {status}"
