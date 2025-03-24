from colorama import Fore, Style
from controller import controller
from dbmodel import dbmodel
import os
from tabulate import tabulate  # נשאיר רק את Tabulate להצגת טבלה
from securitiesmodel import *

class view:    
    def __init__(self):
        self.controller = controller()  # יצירת מופע של Controller
        self.db = self.controller.dbmodel #(לגשת למסד נתונים)
        
    def display_table(self):
        # פונקציה להדפסת טבלה של כל הנתונים
        data = self.db.get_data()  # שליפת הנתונים מהמסד
        
        if not data:
            print(Fore.RED + "\n⚠️ No investments found in the portfolio.\n" + Style.RESET_ALL)
            return

        # המרת הנתונים לטבלה
        table_data = [[k] + list(v.values()) for k, v in data.items()]  # יצירת נתוני הטבלה
        headers = ["Key", "ID", "Name", "Base Value", "Amount"]  # כותרות הטבלה

        # הצגת הטבלה עם עיצוב
        print("\n📊 " + Fore.CYAN + "Portfolio Table:" + Style.RESET_ALL)
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))  # הדפסת הטבלה בעיצוב fancy
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)  # המתנה מהמשתמש להמשך
  
    def display_risk_level(self):
        """
        מציג את רמת הסיכון המשוקללת של התיק
        """
        risk_level = self.db.calculate_portfolio_risk()  # חישוב רמת הסיכון
        print(f"\n⚠️ " + Fore.RED + f"Portfolio Risk Level: {risk_level}" + Style.RESET_ALL)
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)

    def print_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # ניקוי המסך
        print(Fore.CYAN + "\n   Investment Portfolio Menu   " + Style.RESET_ALL)
        print(Fore.CYAN + "==================================" + Style.RESET_ALL)
        
        print(Fore.GREEN + "1. Buy Security" + Style.RESET_ALL)  # קנייה של נייר ערך
        print(Fore.GREEN + "2. Sell Security" + Style.RESET_ALL)  # מכירת נייר ערך
        print(Fore.BLUE + "3. Get Investment Advice (AI)" + Style.RESET_ALL)  # קבלת ייעוץ השקעות
        print(Fore.YELLOW + "4. Show Portfolio (Table)" + Style.RESET_ALL)  # הצגת התיק בטבלה
        print(Fore.MAGENTA + "5. Show Portfolio Risk Level" + Style.RESET_ALL)  # הצגת רמת הסיכון
        print(Fore.RED + "6. Exit" + Style.RESET_ALL)  # יציאה מהתוכנית

    def show(self):
        while True:
            self.print_menu()  # הצגת התפריט        
            choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)  # קלט מהמשתמש            

            if choice == '1':  # קנייה
                self.buy_security()

            elif choice == '2':  # מכירה
                self.sell_security()  # קריאה לפונקציה sell_security

            elif choice == '3':  # קבלת ייעוץ
                question = input("Ask your investment question: ")
                answer = self.controller.get_advice(question)
                print(Fore.GREEN + f"\nAI Advice: {answer}" + Style.RESET_ALL)
                input("Press Enter to continue...")

            elif choice == '4':  # הצגת טבלה
                self.display_table()

            elif choice == '5':  # הצגת רמת הסיכון
                self.display_risk_level()

            elif choice == '6':  # יציאה
                print(Fore.RED + "Exiting..." + Style.RESET_ALL)
                break  # יציאה מהלולאה

            else:
                print(Fore.RED + "Invalid input. Please try again." + Style.RESET_ALL)

    def buy_security(self):
        # הצגת האופציות לרכישת מניות או אג"ח
        securities = {
            1: Stock(name="Apple", base_value=150, amount=10, industry="Technology", volatility="High"),
            2: Stock(name="Tesla", base_value=360, amount=8, industry="Transportation", volatility="Medium"),
            3: Bond(name="Israel Gov Bond", base_value=100, amount=5, issuer="Government", bond_type="Government"),
            4: Bond(name="Corporate Bond X", base_value=90, amount=12, issuer="Corporate", bond_type="Corporate"),
        }

        print("\nAvailable Securities to Buy:")
        for key, value in securities.items():  # הצגת כל האפשרויות לרכישה
            print(f"{key}. {value.name}")

        choice = input(Fore.YELLOW + "Enter the number of the security you want to buy: " + Style.RESET_ALL)
        
        if choice.isdigit() and int(choice) in securities:
            security = securities[int(choice)]  # יצירת אובייקט של נייר הערך שנבחר
            amount = input("How much do you want to buy? ")  # קלט כמות ניירות הערך

            if amount.isdigit():
                amount = int(amount)  # המרת הכמות למספר
                print(Fore.BLUE + f"You chose to buy {security.name}." + Style.RESET_ALL)  # הודעה שהמשתמש בחר רכישה
                self.controller.buy(security, amount)  # קריאה לפונקציה לקנייה
            else:
                print(Fore.RED + "Invalid amount entered. Please enter a number." + Style.RESET_ALL)  # הודעה אם הכמות לא תקינה
        else:
            print(Fore.RED + "Invalid choice. Please select a valid security." + Style.RESET_ALL)

    def sell_security(self):
        # הצגת כל ניירות הערך הקיימים בתיק
        data = self.db.get_data()  # שליפת נתונים מהמסד
        if not data:
            print(Fore.RED + "\n⚠️ No investments found in the portfolio.\n" + Style.RESET_ALL)
            return

        # יצירת רשימה של כל השמות שנרכשו (ניירות ערך שרכשת)
        securities = {k: v['name'] for k, v in data.items()}  
        print("\nAvailable Securities to Sell:")
        for key, value in securities.items():  # הצגת כל האפשרויות למכירה
            print(f"{key}. {value}")

        choice = input(Fore.YELLOW + "Enter the number of the security you want to sell: " + Style.RESET_ALL)

        if choice.isdigit() and int(choice) in securities:
            security = securities[int(choice)]  # נייר הערך שנבחר
            print(Fore.BLUE + f"You chose to sell {security}." + Style.RESET_ALL)
            self.controller.sell(security)  # קריאה לפונקציה למכירה
        else:
            print(Fore.RED + "Invalid choice. Please select a valid security." + Style.RESET_ALL)

# הקוד הראשי שמפעיל את התוכנית
if __name__ == "__main__":
    v = view()  # יצירת מופע של מחלקת view
    v.show()  # הרצת הפונקציה שמריצה את התוכנית1
    
