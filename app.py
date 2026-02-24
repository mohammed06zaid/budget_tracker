from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import Expenses
import os
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("register.html")

# Beim Start die Daten aus data.json laden
if os.path.exists("data.json"):
    try:
        Expenses.Expenses.expenses_list = Expenses.Expenses.from_json()
    except:
        pass
    
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/expenses", methods=["GET"])
def get_expenses():
    try:
        # Falls data.json aktueller ist, neu laden
        if os.path.exists("data.json"):
            Expenses.Expenses.expenses_list = Expenses.Expenses.from_json()
        return jsonify(Expenses.Expenses.expenses_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/expenses/categories', methods = ["GET"])
def totals_by_category():
    try:
        if os.path.exists("data.json"):
            Expenses.Expenses.expenses_list = Expenses.Expenses.from_json()
            return jsonify(Expenses.Expenses.totals_by_category())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/expenses", methods=["POST"])
def add_expense():
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "Invalid or missing JSON data. Ensure Content-Type is 'application/json'."}), 400

        # Neue Ausgabe mit Expenses-Klasse erstellen
        expense = Expenses.Expenses(
            ausgabe=float(data["ausgabe"]),
            kategorie=data["kategorie"],
            date_str=data["datum"]
        )

        # In JSON-Datei speichern
        Expenses.Expenses.to_json()

        # Letzte hinzugefügte Ausgabe zurückgeben
        return jsonify(Expenses.Expenses.expenses_list[-1]), 201
    except Exception as e:
        return jsonify({"error": "Invalid JSON data: " + str(e)}), 400

@app.route("/expenses/<id>", methods = ["DELETE"])
def delete_expenses(id):
    try:
        Expenses.Expenses.delete_by_id(id)

        return "", 204
    except:
        return "", 404
    
@app.route("/expenses/max_min", methods = ["GET"])
def max_min():
    try: 
        result = Expenses.Expenses.get_min_max_expense()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    


@app.route("/income", methods = ["POST"])
def save_income():
    try:
        data = request.get_json()

        # Validate input data
        if not data or "income" not in data:
            return jsonify({"error": "Invalid input. 'income' field is required."}), 400

        try:
            amount = float(data["income"])
            if amount <= 0:
                return jsonify({"error": "Income must be a positive number."}), 400
        except ValueError:
            return jsonify({"error": "Income must be a valid number."}), 400

        # Validate session
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "User not logged in."}), 401

        # Save income to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO incomes (user_id, amount, date) VALUES (?, ?, datetime('now'))",
            (user_id, amount),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Income saved"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/expenses/status", methods = ["GET"])
def get_status():
    user_id = session.get("user_id")

    connenction = sqlite3.connect("database.db")
    cursor = connenction.cursor()   

    cursor.execute("select amount from incomes where user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    current_income = cursor.fetchone()

    if current_income is None:
        connenction.close()
        return jsonify({"error": "No income found for user"}), 404

    income = current_income[0]   

    resukt = Expenses.Expenses.get_budget_status(user_id, income)
    return jsonify(resukt), 200 

    
def init_db():
    connection = sqlite3.connect("database.db")
    
    cursor = connection.cursor()

    #Table for Useres
    create_users_table_sql =  """
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL
                )"""

    cursor.execute(create_users_table_sql)

    #Table for incomms 
    create_incomes_table_sql = """
            CREATE TABLE IF NOT EXISTS incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )"""
    cursor.execute(create_incomes_table_sql)

    #Table for Expenses 
    create_expenses_table_sql = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            category TEXT,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )"""
    
    cursor.execute(create_expenses_table_sql)

    connection.commit()
    connection.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "Benutzername und Passwort sind erforderlich."
        else:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Überprüfen, ob der Benutzer existiert
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                # Benutzer existiert, Passwort überprüfen
                stored_password = user[0]
                if not check_password_hash(stored_password, password):
                    error = "Falsches Passwort. Bitte versuchen Sie es erneut."
                else:
                    return redirect(url_for("home"))
            else:
                error = "Benutzer existiert nicht. Bitte registrieren Sie sich."

    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Username or password are required", 400

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Überprüfen, ob der Benutzer existiert
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            return "User already exists. Please log in.", 400
        else:
            # Benutzer existiert nicht, registrieren
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("home"))

    return render_template("register.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=9000)
