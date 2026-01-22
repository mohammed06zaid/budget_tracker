import json
from Expenses import Expenses

def main():
    e1 = Expenses(20.5, "Food", "2025-02-15")
    e2 = Expenses(10.0, "Transport", "2025-02-16")
    e3 = Expenses(50.0, "Shopping", "2025-02-10")
    Expenses(20.5, "Food", "2025-02-15")
    Expenses(10.0, "Transport", "2025-02-16")
    Expenses(50.0, "Shopping", "2025-02-10")
    Expenses(12.5, "Food", "2025-02-18")
    Expenses(30.0, "Food", "2025-02-20")
    Expenses(850.0, "Rent", "2025-02-01")
    # Januar
    Expenses(12.5, "Food", "2025-01-03")
    Expenses(850.0, "Rent", "2025-01-01")
    Expenses(45.0, "Transport", "2025-01-05")
    Expenses(18.9, "Food", "2025-01-07")
    Expenses(60.0, "Leisure", "2025-01-10")

    # Februar
    Expenses(20.5, "Food", "2025-02-15")
    Expenses(10.0, "Transport", "2025-02-16")
    Expenses(50.0, "Shopping", "2025-02-10")
    Expenses(12.5, "Food", "2025-02-18")
    Expenses(30.0, "Food", "2025-02-20")
    Expenses(850.0, "Rent", "2025-02-01")
    Expenses(25.0, "Leisure", "2025-02-22")

    # März
    Expenses(14.0, "Food", "2025-03-02")
    Expenses(850.0, "Rent", "2025-03-01")
    Expenses(55.0, "Transport", "2025-03-06")
    Expenses(75.0, "Shopping", "2025-03-09")
    Expenses(22.0, "Food", "2025-03-11")
    Expenses(40.0, "Leisure", "2025-03-15")

    # April
    Expenses(16.5, "Food", "2025-04-04")
    Expenses(850.0, "Rent", "2025-04-01")
    Expenses(48.0, "Transport", "2025-04-08")
    Expenses(90.0, "Shopping", "2025-04-12")
    Expenses(28.0, "Food", "2025-04-18")
    Expenses(35.0, "Leisure", "2025-04-21")


    print(Expenses.output_all()) 
    print(Expenses.total_expenses()) 
    print(Expenses.avrg_expenses()) 
    print(Expenses.total_by_category("Food")) 

    print(Expenses.output_by_categroy("Food"))






    

main()
