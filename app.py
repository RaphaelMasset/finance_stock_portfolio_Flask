import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #return apology("TODyO")
    return render_template("portofolio.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:  #elif request.method == "POST":   #like i did in register
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("gimme a symbol!")

        share = lookup(symbol)  # Render an apology if the input is blank or the symbol does not exist (as per the return value of lookup).
        if share == None:
            return apology("This symbol doesn't exist")

        nbshares = float(request.form.get("shares"))
        #test = str(isinstance(int(nbshares) ,int))

        #return apology(f"numb is {test}")
        if not isinstance(nbshares ,float) or nbshares < 0:
            return apology("need positiv interger")
        actualuserid = session["user_id"]

        shareprice = share["price"]
        price = shareprice * nbshares
        money = db.execute("SELECT cash FROM users WHERE id = ? ", actualuserid)

        #return apology(f"it cost {price}")

        if price > money[0]["cash"]:
            return apology("you're to poor bro")  #Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price.

        newbalance =  money[0]["cash"] - price
        #return apology(f"you have {updatedmoney}")
        date = datetime.datetime.now()  #datetime.datetime.now(pytz.timezone("US/Eastern"))
        #return apology(f" {actualuserid} // {newbalance}")

        db.execute("UPDATE users SET cash = ? WHERE id = ? ", newbalance, actualuserid)
        db.execute("INSERT INTO transactions (user_id, symbol, nbshares, price, date) VALUES (?, ?, ?, ?, ?)", actualuserid, symbol, nbshares, shareprice, date) #change symbol for share["symbol"]

        return redirect("/")   #Upon completion, redirect the user to the home page.
        #return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":   #like i did in register
        symbol = request.form.get("symbol")

        if symbol is False:  #maybe delate the is False
            return apology("symbol is null")
        if (len(symbol) != 4) or not symbol.isupper() :
            return apology("symbol incorrect")
        if not symbol:
            return apology("must provide symbol")

    share = lookup(symbol) #maybe use the .upper() function  and maybe return an error is ahere is invalid

    return render_template("share.html",name = share["name"] , price = share["price"], symbol = share["symbol"])

    #return apology("TODO")
    #28-58

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #session.clear()
    if request.method == "POST":
        username = request.form.get("username")  #request.form.post() raises an error if the field is not present or if the request method is not POST, while request.form.get() returns None instead of raising an error. Using request.form.get() allows you to handle cases where the form field might not be present more gracefully.
        password = request.form.get("password")  #IDK why ,post dont work here...
        confirmation = request.form.get("confirmation")

        if not username or not password:
            return apology("must provide password/username")
        if confirmation != password:
            return apology("passwords do not match")
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("Username already exist")

        hash = generate_password_hash(request.form.get("password"))
        # insert username and hash into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # redirect to login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
