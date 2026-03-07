from datetime import datetime 
import json
from multiprocessing import connection
import sqlite3
class Expenses:
        counter = 00
        ausgabe : float
        expenses_list = []
        monthly_budget = 1000
        

        def __init__(self, ausgabe, kategorie, date_str):
        
                Expenses.counter += 1
                self.id = Expenses.counter
                self.ausgabe = ausgabe
                self.kategorie = kategorie
                self.datum = datetime.strptime(date_str, "%Y-%m-%d").date()
                myDict = {  

                        'id':self.id,
                        "Ausgabe": self.ausgabe ,
                        "Kategorie": self.kategorie,
                        "Datum": self.datum.isoformat()
                }
                Expenses.expenses_list.append(myDict)
        

        @classmethod
        def add_expense(cls, ausgabe, kategorie, date_str, user_id):
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO expenses (amount, category, date, user_id) VALUES (?, ?, ?, ?)", (ausgabe, kategorie, date_str, user_id))
                connection.commit()
                connection.close()

        @property
        def ausgabe(self):
                return self._ausgabe

        @ausgabe.setter
        def ausgabe(self, value):
                if value > 0.0:
                        self._ausgabe = value
                else:
                        raise ValueError("ausgabe muss > 0 sein")
                
        @classmethod              
        def get_expense_list(cls):
                return cls.expenses_list
        @classmethod
        def to_json(cls, filename = "data.json"):
                try:
                        with open(filename, "w", encoding="utf-8") as f:
                                json.dump(cls.get_expense_list(),f, ensure_ascii=False, indent=2)
                except FileNotFoundError:
                        with open(filename, "x", encoding="utf-8") as f:
                                json.dump(cls.get_expense_list(),f, ensure_ascii=False, indent=2)
 

        @classmethod
        def from_json(cls):
                with open("data.json", "r", encoding="utf-8") as f:
                        return json.load(f)

                                
        @classmethod
        def output_all(cls):
                for index in cls.get_expense_list():
                        print(index)

        
        def output(self):
                print(self.expenses_list[self.id - 1])


        @classmethod
        def total_expenses(cls, user_id):
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
                total = cursor.fetchone()[0]
                connection.close()
                return total if total else 0.0


        
        @classmethod 
        def total_by_category(cls, category, user_id):
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND category = ?", (user_id, category))
                total = cursor.fetchone()[0]
                connection.close()
                return total if total else 0.0

        @classmethod
        def avrg_expenses(cls, user_id):
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()
                cursor.execute("SELECT AVG(amount) FROM expenses WHERE user_id = ?", (user_id,))
                avg = cursor.fetchone()[0]
                connection.close()
                return avg if avg else 0.0

                
                
        @classmethod
        def output_by_categroy(cls, category):
                my_list = cls.from_json()
                list = []

                for item in my_list: 
                        if item["Kategorie"] == category:
                                list.append(item)

                return list
        
        @classmethod
        def output_by_date(cls, gesuchtes_datum):
                my_list = cls.from_json()
                list =  []

                for item in my_list: 
                        json_datum = datetime.strptime(item["Datum"], "%Y-%m-%d").date()
                        if json_datum == gesuchtes_datum:
                                list.append(item)
                return list
        
        @classmethod
        def get_min_max_expense(cls):
                conccention = sqlite3.connect("database.db")
                cursor = conccention.cursor()
                cursor.execute("SELECT MIN(amount), MAX(amount) FROM expenses") 
                min_val, max_val = cursor.fetchone()
                connection.close()
                return {"max": max_val, "min": min_val}
        
        @classmethod
        def get_budget_status(cls, user_id, income):
                connention = sqlite3.connect("database.db")
                cursor = connention.cursor()
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?",(user_id,))
                total_expenses = cursor.fetchone()[0] or 0.0
                connention.close()

                remaining_budget = income - total_expenses

                if remaining_budget < 45:
                        return {"status": "⚠ Achtung! Budget überschritten um 45 €", "remaining_budget": remaining_budget}
                else:
                        return {"status": "Budget in Ordnung", "remaining_budget": remaining_budget}

                
        @classmethod
        def delete_by_id(cls,id):
                # Delete from database
                try:
                        conn = sqlite3.connect("database.db")
                        cur = conn.cursor()
                        cur.execute("DELETE FROM expenses WHERE id = ?", (int(id),))
                        conn.commit()
                finally:
                        conn.close()

                # Also remove from in-memory list if present
                for index, item in enumerate(list(cls.expenses_list)):
                        if item.get("id") == int(id):
                                cls.expenses_list.pop(index)
                                break
                



        @classmethod    
        def totals_by_category(cls, user_id):
                return {
                        "Food": cls.total_by_category("Food", user_id),
                        "Rent": cls.total_by_category("Rent", user_id),
                        "Shopping": cls.total_by_category("Shopping", user_id),
                        "Transport": cls.total_by_category("Transport", user_id)
                }
