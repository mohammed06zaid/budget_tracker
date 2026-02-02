from Expenses import Expenses
import json

# Test: totals_by_category Methode
print("=" * 50)
print("TEST: totals_by_category()")
print("=" * 50)

# Aktuelle Daten von JSON laden
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"\nDaten in data.json: {len(data)} Einträge")
for item in data:
    print(f"  - {item['Kategorie']}: {item['Ausgabe']}€ ({item['Datum']})")

# Methode testen
result = Expenses.totals_by_category()

print(f"\nErgebnis von totals_by_category():")
for category, total in result.items():
    print(f"  {category}: {total}€")

print("=" * 50)

    