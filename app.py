from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "banksecret"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    conn = get_db()

    accounts = conn.execute(
    "SELECT * FROM accounts"
    ).fetchall()

    return render_template("dashboard.html",accounts=accounts)


@app.route("/create_account", methods=["GET","POST"])
def create_account():

    if request.method == "POST":

        name = request.form["name"]
        acc = request.form["account"]
        bal = request.form["balance"]

        conn = get_db()

        conn.execute(
        "INSERT INTO accounts (name,account_number,balance) VALUES (?,?,?)",
        (name,acc,bal)
        )

        conn.commit()

        return redirect("/dashboard")

    return render_template("create_account.html")


@app.route("/deposit/<int:id>", methods=["GET","POST"])
def deposit(id):

    conn = get_db()

    if request.method == "POST":

        amount = int(request.form["amount"])

        acc = conn.execute(
        "SELECT balance FROM accounts WHERE id=?",
        (id,)
        ).fetchone()

        new_balance = acc["balance"] + amount

        conn.execute(
        "UPDATE accounts SET balance=? WHERE id=?",
        (new_balance,id)
        )

        conn.execute(
        "INSERT INTO transactions (account_id,type,amount) VALUES (?,?,?)",
        (id,"Deposit",amount)
        )

        conn.commit()

        return redirect("/dashboard")

    return render_template("deposit.html")


@app.route("/withdraw/<int:id>", methods=["GET","POST"])
def withdraw(id):

    conn = get_db()

    if request.method == "POST":

        amount = int(request.form["amount"])

        acc = conn.execute(
        "SELECT balance FROM accounts WHERE id=?",
        (id,)
        ).fetchone()

        new_balance = acc["balance"] - amount

        conn.execute(
        "UPDATE accounts SET balance=? WHERE id=?",
        (new_balance,id)
        )

        conn.execute(
        "INSERT INTO transactions (account_id,type,amount) VALUES (?,?,?)",
        (id,"Withdraw",amount)
        )

        conn.commit()

        return redirect("/dashboard")

    return render_template("withdraw.html")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
        "INSERT INTO users (username,password) VALUES (?,?)",
        (username,password)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/transactions/<int:id>")
def transactions(id):

    conn = get_db()

    data = conn.execute(
    "SELECT * FROM transactions WHERE account_id=?",
    (id,)
    ).fetchall()

    return render_template("transactions.html",data=data)


if __name__ == "__main__":
    app.run(debug=True)