# finance_stock_portfolio_Web_App_Flask

## Description
A web application that allows users to manage a virtual stock portfolio. Users can register accounts, look up real-time stock prices, “buy” and “sell” stocks, view their portfolio value, and track transaction history. This app simulates stock trading in a safe environment, making it ideal for learning investment strategies without financial risk.

## Features

User registration and authentication

Real-time stock price lookup

Buy and sell stocks with validation for cash and shares

View portfolio with current stock prices and total holdings

View transaction history (all buys and sells)

Optional personal enhancements: add cash, change password, quick buy/sell

## Technologies

Python 3 + Flask

SQLite database

HTML, CSS, Bootstrap for frontend

Jinja2 templating for dynamic content

CS50 SQL module for database operations

## Installation & Setup

### Windows / macOS / Linux
```bash
git clone https://github.com/USERNAME/finance-stock-portfolio.git

cd finance-stock-portfolio
```

(Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
```

Install dependencies

```bash
pip install -r requirements.txt
```

```bash
Run the Flask app
flask run
```

Open a browser and go to the displayed local URL (usually http://127.0.0.1:5000
).

## Example Session

Register a new user account

Log in

Look up the price of a stock (e.g., AAPL)

Buy 5 shares of AAPL

Visit the portfolio to see current holdings and total cash balance

Sell 2 shares of AAPL

Check the history page for a log of all transactions

## Notes

Stock prices are fetched via an API (IEX) and are updated in real time

All operations are simulated; no real money is used
