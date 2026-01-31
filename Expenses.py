from datetime import datetime 
import json
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
        def total_expenses(cls):
                my_list = cls.from_json()
                totel = 0.0

                for item in my_list:
                        totel += item["Ausgabe"]
                
                return totel
        
        @classmethod 
        def total_by_category(cls, category):
                my_list = cls.from_json()
                totel = 0.0

                for item in my_list: 
                        if item["Kategorie"] == category:
                                totel += item["Ausgabe"]
                
                return totel

        @classmethod
        def avrg_expenses(cls):
                my_list = cls.from_json()
                count = 0 
                totel = 0.0

                for item in my_list:
                        totel += item["Ausgabe"]
                        count +=1

                return totel / count
                
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
                my_list = cls.from_json()
                list = []
                for item in my_list: 
                        list.append(item["Ausgabe"]) 
                max = max(list)
                min = min(list)
                return (max, min)
        
        @classmethod
        def get_budget_status(cls,): 
                my_list = cls.from_json()
                ausgabe_sum = 0.0

                for item in my_list: 
                        ausgabe_sum += item["Ausgabe"] 
                
                restgeld = cls.monthly_budget - ausgabe_sum

                if restgeld <= 45: 
                        return ("⚠ Achtung! Budget überschritten um 45 € ", restgeld)
                else: 
                        return restgeld 
                
        @classmethod
        def delete_by_id(cls,id):
                # Aus der Memory-Liste löschen
                for index, item in enumerate(cls.expenses_list): 
                        if(item["id"] == int(id)):
                                cls.expenses_list.pop(index)
                                break
                # In JSON-Datei speichern
                cls.to_json()
                



        @classmethod    
        def totals_by_category(cls):
                return {
                        "Food": cls.total_by_category("Food"),
                        "Rent": cls.total_by_category("Rent"),
                        "Shopping": cls.total_by_category("Shopping"),
                        "Transport": cls.total_by_category("Transport")
                }
