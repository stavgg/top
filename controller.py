from dbmodel import dbmodel
from ollamamodel import ollamamodel
from securitiesmodel import *

class controller:
    def __init__(self):
        self.dbmodel = dbmodel()
        self.ai_model = ollamamodel()

    def buy(self, whatsecurity, amount):
        print("🛒 Buying...")
        if isinstance(amount, int) and amount > 0:
            self.dbmodel.insert(whatsecurity, amount)
        else:
            print("❌ Invalid amount. Please enter a valid number.")

    def sell(self, name, amount): #מוכר נייר ערך לפי שם וכמות
        print(f"📉 Selling {amount} of {name}...")
        item = self.dbmodel.find_by_name(name)
        if not item: #אם לא קיים בכלל 
            print("❌ Security not found in portfolio.")
            return "not_found"

        current_amount = item[3]  # amount נמצא בעמודה 4
        if current_amount < amount: #אם הכמות קטנה ממה שיש 
            print("❌ Not enough quantity to sell.")
            return "not_enough"

        new_amount = current_amount - amount

        if new_amount == 0: #אם הכמות לאחר מכירה שווה לאפס 
            self.dbmodel.delete(name)
            print(f"✅ Sold all of {name}. Removed from portfolio.")
            return "deleted"
        else:
            # יצירת אובייקט חדש עם כמות מעודכנת
            base_value = item[2]  # base_value נמצא בעמודה 3
            if "bond" in name.lower():
                updated_security = Bond(name, base_value, new_amount, "Government", "Government")
            else:
                updated_security = Stock(name, base_value, new_amount, "Technology", "High")

            self.dbmodel.update(updated_security)
            print(f"✅ Updated {name} to new amount: {new_amount}")
            return "updated"

    def get_advice(self, question): #שואל את האולמה ומחזיר תשובה
        print("🤖 Consulting Ollama AI model...")
        return self.ai_model.get_advice(question)

