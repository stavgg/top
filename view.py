from colorama import Fore, Style
from controller import controller
import os
from tabulate import tabulate
from securitiesmodel import *
import time

class view:    
    def __init__(self):
        self.controller = controller()
        self.db = self.controller.dbmodel
        
    def display_table(self):
        data = self.db.get_data()
        
        if not data:
            print(Fore.RED + "\n⚠️ No investments found in the portfolio.\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
            return

        table_data = [[k] + list(v.values()) for k, v in data.items()]
        headers = ["Key", "ID", "Name", "Base Value", "Amount"]

        print("\n📊 " + Fore.CYAN + "Portfolio Table:" + Style.RESET_ALL)
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)

    def display_risk_level(self):
        risk_level = self.db.calculate_portfolio_risk()
        print(f"\n⚠️ " + Fore.RED + f"Portfolio Risk Level: {risk_level}" + Style.RESET_ALL)
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)

    def print_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + "\n   Investment Portfolio Menu   " + Style.RESET_ALL)
        print(Fore.CYAN + "==================================" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Buy Security" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Sell Security" + Style.RESET_ALL)
        print(Fore.BLUE + "3. Get Investment Advice (AI)" + Style.RESET_ALL)
        print(Fore.YELLOW + "4. Show Portfolio (Table)" + Style.RESET_ALL)
        print(Fore.MAGENTA + "5. Show Portfolio Risk Level" + Style.RESET_ALL)
        print(Fore.RED + "6. Exit" + Style.RESET_ALL)

    def show(self):
        while True:
            self.print_menu()
            choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)

            if choice == '1':
                self.buy_security()

            elif choice == '2':
                self.sell_security()

            elif choice == '3':
                question = input("Ask your investment question: ")
                answer = self.controller.get_advice(question)
                print(Fore.GREEN + f"\nAI Advice: {answer}" + Style.RESET_ALL)
                input("Press Enter to continue...")

            elif choice == '4':
                self.display_table()

            elif choice == '5':
                self.display_risk_level()

            elif choice == '6':
                print(Fore.RED + "Exiting..." + Style.RESET_ALL)
                break

            else:
                print(Fore.RED + "Invalid input. Please try again." + Style.RESET_ALL)
                input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

    def buy_security(self):
        securities = {
            1: Stock(name="Apple", base_value=150, amount=10, industry="Technology", volatility="High"),
            2: Stock(name="Tesla", base_value=360, amount=8, industry="Transportation", volatility="Medium"),
            3: Bond(name="Israel Gov Bond", base_value=100, amount=5, issuer="Government", bond_type="Government"),
            4: Bond(name="Corporate Bond X", base_value=90, amount=12, issuer="Corporate", bond_type="Corporate"),
        }

        print("\nAvailable Securities to Buy:")
        for key, value in securities.items():
            print(f"{key}. {value.name}")

        choice = input(Fore.YELLOW + "Enter the number of the security you want to buy: " + Style.RESET_ALL)
        
        if choice.isdigit() and int(choice) in securities:
            security = securities[int(choice)]
            amount = input("How much do you want to buy? ")

            if amount.isdigit():
                amount = int(amount)
                print(Fore.BLUE + f"You chose to buy {amount} units of {security.name}." + Style.RESET_ALL)
                self.controller.buy(security, amount)
            else:
                print(Fore.RED + "Invalid amount entered. Please enter a number." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid choice. Please select a valid security." + Style.RESET_ALL)

        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

    def sell_security(self):
        data = self.db.get_data()
        securities = {str(k): v for k, v in data.items()
                      if 'name' in v and v['name'] and 'amount' in v and v['amount'] > 0}

        if not securities:
            print(Fore.RED + "\n⚠️ No investments available to sell.\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
            return

        print("\nAvailable Securities to Sell:")
        for key, value in securities.items():
            print(f"{key}. {value['name']} (Amount: {value['amount']})")

        choice = input(Fore.YELLOW + "Enter the number of the security you want to sell: " + Style.RESET_ALL)

        if choice in securities:
            security = securities[choice]['name']
            amount_available = securities[choice]['amount']

            amount = input(Fore.YELLOW + f"Enter the amount of {security} to sell (Available: {amount_available}): " + Style.RESET_ALL)

            if amount.isdigit() and 0 < int(amount) <= amount_available:
                amount = int(amount)
                print(Fore.BLUE + f"You chose to sell {amount} units of {security}." + Style.RESET_ALL)
                self.controller.sell(security, amount)
            else:
                print(Fore.RED + f"Invalid amount. You can sell between 1 and {amount_available} units." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid choice. Please select a valid security." + Style.RESET_ALL)

        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    v = view()
    v.show()

