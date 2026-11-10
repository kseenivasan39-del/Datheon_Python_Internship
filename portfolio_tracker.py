"""
Stock Portfolio Performance Tracker
Internship Project: Datheon Python Internship

Features:
- Track stock holdings: Ticker symbol, buy price, share quantity.
- Real-time or manual market price fetching/simulation.
- Live valuation: Current value, total investment, net profit/loss ($ and %).
- Per-holding performance breakdown with percentage gain/loss.
- Persistent performance logging & export to external CSV files.
- Persistent portfolio storage in JSON for multi-session usage.
"""

import csv
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

PORTFOLIO_FILE = "portfolio_data.json"
TRANSACTION_LOG_CSV = "portfolio_performance_log.csv"
SNAPSHOT_LOG_CSV = "portfolio_summary_snapshots.csv"

# Free public quotes fallback dictionary (simulated live prices if API is unavailable)
FALLBACK_PRICES = {
    "AAPL": 225.50,
    "MSFT": 430.20,
    "GOOGL": 178.90,
    "AMZN": 186.40,
    "TSLA": 252.10,
    "NVDA": 138.80,
    "META": 585.30,
    "NFLX": 710.00,
    "AMD": 155.60,
    "INTC": 23.40,
    "DATHEON": 150.00
}


def load_portfolio():
    """Loads existing portfolio positions from JSON file."""
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not parse portfolio file. Initializing empty portfolio.")
            return {}
    return {}


def save_portfolio(portfolio):
    """Saves portfolio positions to JSON file."""
    try:
        with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
            json.dump(portfolio, f, indent=4)
    except IOError as e:
        print(f"Error saving portfolio data: {e}")


def fetch_live_price(symbol):
    """
    Attempts to fetch live stock quote from Yahoo Finance API.
    Falls back gracefully to simulated fallback prices or user input.
    """
    symbol = symbol.upper().strip()
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            meta = data["chart"]["result"][0]["meta"]
            price = meta.get("regularMarketPrice")
            if price is not None and price > 0:
                return round(float(price), 2), "Live Yahoo Finance"
    except Exception:
        pass

    # Check fallback dictionary
    if symbol in FALLBACK_PRICES:
        return FALLBACK_PRICES[symbol], "Market Reference (Simulated)"

    return None, None


def get_current_price(symbol):
    """Retrieves price via fetch, or prompts user for the current market price."""
    price, source = fetch_live_price(symbol)
    if price is not None:
        return price, source

    while True:
        try:
            user_price = float(input(f"Enter current market price for {symbol}: $"))
            if user_price <= 0:
                print("Price must be greater than zero.")
                continue
            return round(user_price, 2), "Manual Entry"
        except ValueError:
            print("Invalid input. Please enter a numerical price value.")


def log_transaction_to_csv(action, symbol, shares, price, total_amount, notes=""):
    """Appends an individual transaction record to the external CSV file."""
    file_exists = os.path.exists(TRANSACTION_LOG_CSV)
    fieldnames = ["Timestamp", "Action", "Symbol", "Shares", "PricePerShare", "TotalAmount", "Notes"]

    try:
        with open(TRANSACTION_LOG_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Action": action.upper(),
                "Symbol": symbol.upper(),
                "Shares": f"{shares:.4f}",
                "PricePerShare": f"{price:.2f}",
                "TotalAmount": f"{total_amount:.2f}",
                "Notes": notes
            })
    except IOError as e:
        print(f"Error logging transaction to CSV: {e}")


def log_snapshot_to_csv(summary_data):
    """Logs the overall portfolio snapshot summary to an external CSV file."""
    file_exists = os.path.exists(SNAPSHOT_LOG_CSV)
    fieldnames = [
        "Timestamp", "TotalInvested", "TotalCurrentValue",
        "TotalGainLossDollars", "TotalGainLossPercent", "TotalHoldingsCount"
    ]

    try:
        with open(SNAPSHOT_LOG_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "TotalInvested": f"{summary_data['total_invested']:.2f}",
                "TotalCurrentValue": f"{summary_data['total_current_value']:.2f}",
                "TotalGainLossDollars": f"{summary_data['net_profit_loss']:.2f}",
                "TotalGainLossPercent": f"{summary_data['net_percentage']:.2f}%",
                "TotalHoldingsCount": summary_data['count']
            })
    except IOError as e:
        print(f"Error logging snapshot to CSV: {e}")


def add_stock(portfolio):
    """Handles adding a new position or averaging down into an existing holding."""
    print("\n--- [Add Stock Holding] ---")
    while True:
        symbol = input("Enter Stock Ticker Symbol (e.g. AAPL, TSLA, NVDA): ").strip().upper()
        if symbol.isalnum() and len(symbol) <= 10:
            break
        print("Invalid ticker symbol. Enter alphanumeric symbol up to 10 chars.")

    while True:
        try:
            shares = float(input(f"Enter quantity of shares for {symbol}: "))
            if shares <= 0:
                print("Quantity must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            buy_price = float(input(f"Enter purchase price per share for {symbol}: $"))
            if buy_price <= 0:
                print("Buy price must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    total_cost = shares * buy_price

    if symbol in portfolio:
        # Calculate weighted average cost basis
        old_shares = portfolio[symbol]["shares"]
        old_price = portfolio[symbol]["buy_price"]
        new_total_shares = old_shares + shares
        weighted_avg_price = ((old_shares * old_price) + total_cost) / new_total_shares

        portfolio[symbol]["shares"] = new_total_shares
        portfolio[symbol]["buy_price"] = weighted_avg_price
        print(f"\n Updated existing holding for {symbol}:")
        print(f"Total Shares: {new_total_shares:.4f} | New Average Cost Basis: ${weighted_avg_price:.2f}")
    else:
        portfolio[symbol] = {
            "shares": shares,
            "buy_price": buy_price,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        print(f"\n Successfully added {shares} shares of {symbol} at ${buy_price:.2f} each.")

    save_portfolio(portfolio)
    log_transaction_to_csv("BUY", symbol, shares, buy_price, total_cost, "Portfolio Addition")
    print(f" Transaction logged to '{TRANSACTION_LOG_CSV}'.")


def remove_stock(portfolio):
    """Allows selling or removing a stock holding from the portfolio."""
    print("\n--- [Sell / Remove Holding] ---")
    if not portfolio:
        print("Portfolio is currently empty.")
        return

    symbol = input("Enter Stock Ticker Symbol to remove/sell: ").strip().upper()
    if symbol not in portfolio:
        print(f"'{symbol}' is not in your current portfolio.")
        return

    current_shares = portfolio[symbol]["shares"]
    print(f"You currently hold {current_shares:.4f} shares of {symbol}.")

    while True:
        try:
            sell_qty = float(input(f"Enter number of shares to sell (Max: {current_shares:.4f}): "))
            if sell_qty <= 0 or sell_qty > current_shares:
                print(f"Invalid quantity. Must be between 0 and {current_shares:.4f}.")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric value.")

    sell_price, _ = get_current_price(symbol)
    proceeds = sell_qty * sell_price

    if sell_qty == current_shares:
        del portfolio[symbol]
        print(f" Entire holding of {symbol} sold for ${proceeds:,.2f}.")
    else:
        portfolio[symbol]["shares"] -= sell_qty
        print(f" Sold {sell_qty:.4f} shares. Remaining: {portfolio[symbol]['shares']:.4f} shares.")

    save_portfolio(portfolio)
    log_transaction_to_csv("SELL", symbol, sell_qty, sell_price, proceeds, "Holding Sale")
    print(f" Sell transaction logged to '{TRANSACTION_LOG_CSV}'.")


def calculate_portfolio_performance(portfolio):
    """Computes real-time valuation, gain/loss per holding, and totals."""
    if not portfolio:
        return None

    holdings_metrics = []
    total_invested = 0.0
    total_current_value = 0.0

    print("\nFetching real-time market data...")
    for symbol, details in portfolio.items():
        shares = details["shares"]
        buy_price = details["buy_price"]
        invested = shares * buy_price

        current_price, price_source = get_current_price(symbol)
        current_value = shares * current_price

        gain_loss_dollar = current_value - invested
        gain_loss_pct = ((current_price - buy_price) / buy_price) * 100 if buy_price > 0 else 0.0

        total_invested += invested
        total_current_value += current_value

        holdings_metrics.append({
            "symbol": symbol,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested": invested,
            "current_value": current_value,
            "gain_loss_dollar": gain_loss_dollar,
            "gain_loss_pct": gain_loss_pct,
            "source": price_source
        })

    net_profit_loss = total_current_value - total_invested
    net_percentage = (net_profit_loss / total_invested * 100) if total_invested > 0 else 0.0

    return {
        "holdings": holdings_metrics,
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "net_profit_loss": net_profit_loss,
        "net_percentage": net_percentage,
        "count": len(holdings_metrics)
    }


def view_portfolio_report(portfolio):
    """Displays formatted terminal table of performance breakdown."""
    if not portfolio:
        print("\nYour portfolio is currently empty. Add stocks using Option 1.")
        return

    data = calculate_portfolio_performance(portfolio)

    print("\n" + "=" * 95)
    print("                    INVESTMENT PORTFOLIO PERFORMANCE DASHBOARD")
    print("=" * 95)
    header = f"{'Symbol':<8} {'Shares':>9} {'Buy Price':>11} {'Current':>11} {'Invested':>12} {'Cur Value':>12} {'Gain/Loss($)':>14} {'Gain(%)':>10}"
    print(header)
    print("-" * 95)

    for item in data["holdings"]:
        dollar_str = f"{'+' if item['gain_loss_dollar'] >= 0 else ''}${item['gain_loss_dollar']:,.2f}"
        pct_str = f"{'+' if item['gain_loss_pct'] >= 0 else ''}{item['gain_loss_pct']:.2f}%"

        print(
            f"{item['symbol']:<8} "
            f"{item['shares']:>9.2f} "
            f"${item['buy_price']:>10.2f} "
            f"${item['current_price']:>10.2f} "
            f"${item['invested']:>11.2f} "
            f"${item['current_value']:>11.2f} "
            f"{dollar_str:>14} "
            f"{pct_str:>10}"
        )

    print("-" * 95)
    net_dollar_str = f"{'+' if data['net_profit_loss'] >= 0 else ''}${data['net_profit_loss']:,.2f}"
    net_pct_str = f"{'+' if data['net_percentage'] >= 0 else ''}{data['net_percentage']:.2f}%"

    print(f"Total Invested Capital : ${data['total_invested']:,.2f}")
    print(f"Current Portfolio Value: ${data['total_current_value']:,.2f}")
    print(f"Net Total Profit/Loss  : {net_dollar_str} ({net_pct_str})")
    print(f"Active Holdings Count  : {data['count']}")
    print("=" * 95)

    # Automatically save snapshot log
    log_snapshot_to_csv(data)
    print(f"✓ Summary snapshot logged to '{SNAPSHOT_LOG_CSV}'.")


def display_menu():
    """Prints user action menu."""
    print("\n" + "=" * 45)
    print("    STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("        Datheon Python Internship")
    print("=" * 45)
    print("1. View Portfolio Performance & Valuation")
    print("2. Add / Buy Stock Holding")
    print("3. Sell / Remove Stock Holding")
    print("4. View Transaction History CSV")
    print("5. Reset / Clear Portfolio")
    print("6. Exit")
    print("=" * 45)


def view_transaction_history():
    """Reads and prints logged CSV records in a clean tabular format."""
    if not os.path.exists(TRANSACTION_LOG_CSV):
        print("\nNo transaction history found yet. Buy or sell some stocks first.")
        return

    print("\n" + "=" * 80)
    print("                       TRANSACTION LOG HISTORY (CSV)")
    print("=" * 80)
    try:
        with open(TRANSACTION_LOG_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 6:
                    print(f"{row[0]:<20} | {row[1]:<6} | {row[2]:<8} | {row[3]:>8} shares | ${row[4]:>8} | Total: ${row[5]:>10}")
        print("=" * 80)
    except IOError as e:
        print(f"Error reading CSV file: {e}")


def reset_portfolio(portfolio):
    """Clears all holdings with confirmation."""
    confirm = input("\nAre you sure you want to delete all portfolio data? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        portfolio.clear()
        save_portfolio(portfolio)
        print("Portfolio cleared successfully.")
    else:
        print("Action cancelled.")


def main():
    """Application entry point."""
    portfolio = load_portfolio()

    # Prepopulate with sample holdings on first run if empty
    if not portfolio and not os.path.exists(PORTFOLIO_FILE):
        portfolio = {
            "AAPL": {"shares": 10.0, "buy_price": 180.00, "date_added": "2026-01-15"},
            "MSFT": {"shares": 5.0, "buy_price": 400.00, "date_added": "2026-02-10"},
            "NVDA": {"shares": 15.0, "buy_price": 115.50, "date_added": "2026-03-01"}
        }
        save_portfolio(portfolio)
        for sym, d in portfolio.items():
            log_transaction_to_csv("BUY", sym, d["shares"], d["buy_price"], d["shares"] * d["buy_price"], "Initial Portfolio Setup")

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            view_portfolio_report(portfolio)
        elif choice == "2":
            add_stock(portfolio)
        elif choice == "3":
            remove_stock(portfolio)
        elif choice == "4":
            view_transaction_history()
        elif choice == "5":
            reset_portfolio(portfolio)
        elif choice == "6":
            print("\nThank you for using Stock Portfolio Performance Tracker! Goodbye.\n")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1 through 6.")


if __name__ == "__main__":
    main()
