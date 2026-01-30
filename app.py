from flask import Flask, jsonify, render_template, request
import Expenses
import os

app = Flask(__name__)

# Beim Start die Daten aus data.json laden
if os.path.exists("data.json"):
    try:
        Expenses.Expenses.expenses_list = Expenses.Expenses.from_json()
    except:
        pass

@app.route("/")
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

@app.route("/expenses", methods=["POST"])
def add_expense():
    try:
        data = request.get_json()
        
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
        return jsonify({"error": str(e)}), 400

@app.route("/expenses/<id>", methods = ["DELETE"])
def delete_expenses(id):
    try:
        Expenses.Expenses.delete_by_id(id)

        return "", 204
    except:
        return "", 404







if __name__ == "__main__":
    app.run(debug=True, port=9000)
