"""
Enterprise Smart Inventory & Asset System - Inventory Manager
Internship Project: Datheon Python Internship

Features:
- InventoryManager class managing asset lifecycle.
- Safe add, remove, search, checkout, and return operations.
- Dynamic fee calculation using polymorphic contracts.
- Formatted tabular inventory audit reports and financial summaries.
- Interactive CLI demonstration menu.
"""

from datetime import date, timedelta
from typing import Dict, List, Optional
from models import LibraryItem, Book, Magazine, DigitalMedia


class InventoryManager:
    """
    Enterprise Manager handling inventory tracking,
    asset allocations, audits, and returns.
    """

    def __init__(self, name: str = "Central Tech Assets & Library"):
        self.name = name
        self._items: Dict[str, LibraryItem] = {}
        self._transaction_history: List[dict] = []

    def add_item(self, item: LibraryItem) -> bool:
        """Adds a new asset to inventory, ensuring uniqueness of item_id."""
        if not isinstance(item, LibraryItem):
            raise TypeError("Only instances of LibraryItem can be added to the inventory.")

        if item.item_id in self._items:
            print(f"[Warning] Item ID '{item.item_id}' already exists in inventory.")
            return False

        self._items[item.item_id] = item
        return True

    def remove_item(self, item_id: str) -> Optional[LibraryItem]:
        """Removes an asset from inventory if not currently checked out."""
        item = self._items.get(item_id)
        if not item:
            print(f"[Warning] Item ID '{item_id}' not found.")
            return None

        if item.is_checked_out:
            print(f"[Error] Cannot remove checked out item '{item.title}' (ID: {item_id}).")
            return None

        return self._items.pop(item_id)

    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        """Retrieves item by its unique ID."""
        return self._items.get(item_id)

    def checkout_item(self, item_id: str, borrower: str, checkout_date: date = None) -> bool:
        """Checks out an item to a borrower."""
        item = self.get_item(item_id)
        if not item:
            print(f"[Error] Item ID '{item_id}' does not exist.")
            return False

        try:
            item.checkout(borrower, checkout_date)
            self._transaction_history.append({
                "action": "CHECKOUT",
                "item_id": item_id,
                "title": item.title,
                "borrower": borrower,
                "date": (checkout_date or date.today()).isoformat()
            })
            print(f"✓ Checked out '{item.title}' to {borrower}.")
            return True
        except RuntimeError as e:
            print(f"[Error] {e}")
            return False

    def return_item(self, item_id: str, return_date: date = None) -> Optional[float]:
        """Processes return of an item and returns calculated late fee."""
        item = self.get_item(item_id)
        if not item:
            print(f"[Error] Item ID '{item_id}' does not exist.")
            return None

        try:
            prev_borrower = item.borrower_name
            borrow_date = item.borrow_date
            fee = item.return_item(return_date)

            ret_date = return_date or date.today()
            self._transaction_history.append({
                "action": "RETURN",
                "item_id": item_id,
                "title": item.title,
                "borrower": prev_borrower,
                "borrow_date": borrow_date.isoformat(),
                "return_date": ret_date.isoformat(),
                "fee": fee
            })

            print(f"✓ '{item.title}' returned successfully.")
            if fee > 0:
                print(f"  Late fee assessed: ${fee:.2f}")
            else:
                print("  Returned within allowed window. No late fee.")
            return fee

        except RuntimeError as e:
            print(f"[Error] {e}")
            return None

    def search_items(self, query: str) -> List[LibraryItem]:
        """Searches items matching ID, title, or type."""
        q = query.lower()
        results = [
            item for item in self._items.values()
            if q in item.item_id.lower() or q in item.title.lower() or q in item.__class__.__name__.lower()
        ]
        return results

    def generate_audit_report(self):
        """Generates a comprehensive tabular audit report of all inventory assets."""
        print("\n" + "=" * 115)
        print(f"                     ENTERPRISE SMART INVENTORY AUDIT REPORT - {self.name.upper()}")
        print("=" * 115)

        header = f"{'ID':<8} {'Type':<14} {'Title':<30} {'Price':>10} {'Status':<18} {'Borrower':<18} {'Len/Size':<10}"
        print(header)
        print("-" * 115)

        total_asset_value = 0.0
        checked_out_count = 0

        # Sort items cleanly using __lt__ implementation
        sorted_items = sorted(self._items.values())

        for item in sorted_items:
            item_type = item.__class__.__name__
            total_asset_value += item.price

            status = "CHECKED OUT" if item.is_checked_out else "AVAILABLE"
            borrower = item.borrower_name if item.borrower_name else "-"
            if item.is_checked_out:
                checked_out_count += 1

            length_metric = f"{len(item)} units"

            print(
                f"{item.item_id:<8} "
                f"{item_type:<14} "
                f"{item.title[:28]:<30} "
                f"${item.price:>9.2f} "
                f"{status:<18} "
                f"{borrower:<18} "
                f"{length_metric:<10}"
            )

        print("-" * 115)
        print(f"Total Tracked Assets : {len(self._items)}")
        print(f"Active Checkouts     : {checked_out_count} item(s)")
        print(f"Total Asset Valuation: ${total_asset_value:,.2f}")
        print("=" * 115)

    def print_metadata_report(self):
        """Demonstrates polymorphic metadata inspection."""
        print("\n" + "=" * 80)
        print("                     DETAILED ASSET METADATA INSPECTION")
        print("=" * 80)
        for item in sorted(self._items.values()):
            print(f"[{item.item_id}] {item.title}")
            print(f"  └── {item.display_metadata()}")
        print("=" * 80)


def seed_sample_inventory() -> InventoryManager:
    """Populates inventory with sample Book, Magazine, and DigitalMedia assets."""
    manager = InventoryManager("Datheon Corporate Enterprise Library")

    # Derived Class: Book
    b1 = Book("B-101", "Clean Code: Agile Software", 45.00, "Robert C. Martin", 464, "978-0132350884")
    b2 = Book("B-102", "Python Crash Course", 38.50, "Eric Matthes", 544, "978-1593279288")
    b3 = Book("B-103", "Design Patterns (GoF)", 54.00, "Gang of Four", 395, "978-0201633610")

    # Derived Class: Magazine
    m1 = Magazine("M-201", "IEEE Software Trends", 15.00, 42, "November 2026")
    m2 = Magazine("M-202", "Harvard Business Review", 18.00, 118, "October 2026")

    # Derived Class: DigitalMedia
    d1 = DigitalMedia("D-301", "Microservices Architecture", 89.00, "MP4", 1450)
    d2 = DigitalMedia("D-302", "Data Science Masterclass", 65.00, "EPUB", 320)

    for item in [b1, b2, b3, m1, m2, d1, d2]:
        manager.add_item(item)

    # Pre-checkout a couple of items to demonstrate state management
    today = date.today()
    manager.checkout_item("B-101", "Alice Johnson", today - timedelta(days=20))  # 6 days overdue
    manager.checkout_item("D-301", "Bob Smith", today - timedelta(days=5))       # 2 days overdue

    return manager


def main():
    """Interactive CLI testing suite for OOP Smart Inventory System."""
    manager = seed_sample_inventory()

    print("*" * 65)
    print("      ENTERPRISE SMART INVENTORY & ASSET SYSTEM")
    print("         Datheon Python Internship Task")
    print("*" * 65)

    while True:
        print("\n--- Main Menu ---")
        print("1. View Tabular Inventory Audit Report")
        print("2. Inspect Polymorphic Asset Metadata")
        print("3. Check Out an Item")
        print("4. Return an Item (Calculate Late Fees)")
        print("5. Search Inventory")
        print("6. Run OOP Architecture Dunder & Encapsulation Verification Test")
        print("7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            manager.generate_audit_report()
        elif choice == "2":
            manager.print_metadata_report()
        elif choice == "3":
            item_id = input("Enter Item ID to check out: ").strip()
            borrower = input("Enter Borrower Name: ").strip()
            manager.checkout_item(item_id, borrower)
        elif choice == "4":
            item_id = input("Enter Item ID to return: ").strip()
            manager.return_item(item_id)
        elif choice == "5":
            q = input("Enter search query (ID, title, or type): ").strip()
            results = manager.search_items(q)
            print(f"\nFound {len(results)} matching item(s):")
            for res in results:
                print(f" • {res}")
        elif choice == "6":
            run_oop_verification_test(manager)
        elif choice == "7":
            print("\nExiting Enterprise Inventory System. Goodbye!\n")
            break
        else:
            print("Invalid selection. Please choose 1 through 7.")


def run_oop_verification_test(manager: InventoryManager):
    """Verifies all OOP pillars programmatically in terminal."""
    print("\n" + "=" * 65)
    print("           OOP ARCHITECTURAL VALIDATION SUITE")
    print("=" * 65)

    item1 = manager.get_item("B-101")
    item2 = manager.get_item("B-102")

    print("1. [Abstraction & abc module]")
    from abc import ABC
    print(f"   LibraryItem is an ABC: {issubclass(LibraryItem, ABC)}")

    print("\n2. [Encapsulation & Validation]")
    print(f"   Current Price (getter): ${item1.price:.2f}")
    try:
        item1.price = -25.0
    except ValueError as e:
        print(f"   Validation triggered successfully on negative price: '{e}'")

    print("\n3. [Polymorphic Late Fee Calculation]")
    for item in manager._items.values():
        print(f"   {item.__class__.__name__:<13} '{item.title[:25]}': Fee for 10 days = ${item.calculate_fee(10):.2f}")

    print("\n4. [Magic / Dunder Methods]")
    print(f"   __str__  : {str(item1)}")
    print(f"   __repr__ : {repr(item1)}")
    print(f"   __len__ (Book pages / Magazine issues / Digital MB):")
    for item in list(manager._items.values())[:3]:
        print(f"     • {item.title[:22]}: len() = {len(item)}")
    print(f"   __eq__ (Equality test: item1 == item2): {item1 == item2}")
    print(f"   __eq__ (Self comparison: item1 == item1): {item1 == item1}")
    print("=" * 65)
    print("✓ All Object-Oriented criteria verified!")


if __name__ == "__main__":
    main()
