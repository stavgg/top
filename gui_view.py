import tkinter as tk
from tkinter import messagebox, simpledialog
from view import view
from securitiesmodel import *
from tabulate import tabulate
from PIL import Image, ImageTk

class GUIView:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Portfolio")

        self.portfolio = view()

        # לוגו
        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((130, 130))
        logo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(root, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=5)

        # כותרת
        tk.Label(root, text="Investment Portfolio Menu", font=("Arial", 16, "bold"), fg="black").pack(pady=5)

        # עיצוב כפתורים אחיד
        button_style = {
            "width": 30,
            "relief": "flat",
            "highlightthickness": 0,
            "bd": 0
        }

        tk.Button(root, text="Buy Security", command=self.buy_security, **button_style).pack(pady=5)
        tk.Button(root, text="Sell Security", command=self.sell_security, **button_style).pack(pady=5)
        tk.Button(root, text="Get Investment Advice (AI)", command=self.get_advice, **button_style).pack(pady=5)
        tk.Button(root, text="Show Portfolio (Table)", command=self.display_table, **button_style).pack(pady=5)
        tk.Button(root, text="Show Portfolio Risk Level", command=self.display_risk, **button_style).pack(pady=5)
        tk.Button(root, text="Exit", command=self.root.quit, **button_style).pack(pady=10)

    def buy_security(self):
        options = {
        1: CommonStock(name="Apple", base_value=150, amount=10, industry="Technology", volatility="High", voting_rights=True),
        2: PreferredStock(name="Tesla", base_value=360, amount=8, industry="Transportation", volatility="Medium", fixed_dividend=0.05),
        3: GovernmentBond(name="Israel Gov Bond", base_value=100, amount=5, issuer="Government", maturity_years=10),
        4: CorporateBond(name="Corporate Bond X", base_value=90, amount=12, issuer="Corporate", credit_rating="BBB"),
    }
        choices_text = "\n".join([f"{k}. {v.name}" for k, v in options.items()])
        choice = simpledialog.askinteger("Buy Security", f"Choose a security to buy:\n{choices_text}")

        if choice in options:
            amount = simpledialog.askinteger("Amount", "How much do you want to buy?")
            if amount:
                self.portfolio.controller.buy(options[choice], amount)
                messagebox.showinfo("Success", f"Bought {amount} of {options[choice].name}")
        else:
            messagebox.showerror("Error", "Invalid choice.")

    def sell_security(self):
        data = self.portfolio.controller.dbmodel.get_data()
        if not data:
            messagebox.showwarning("No Investments", "⚠️ No investments found.")
            return

        choices = {k: v['name'] for k, v in data.items()}
        choices_text = "\n".join([f"{k}. {v}" for k, v in choices.items()])
        choice = simpledialog.askinteger("Sell Security", f"Choose a security to sell:\n{choices_text}")

        if choice in choices:
            amount = simpledialog.askinteger("Amount", "How much do you want to sell?")
            if amount is None or amount <= 0:
                messagebox.showerror("Error", "Invalid amount.")
                return

            result = self.portfolio.controller.sell(choices[choice], amount)
            if result == "not_enough":
                messagebox.showerror("Error", "❌ Not enough quantity to sell.")
            elif result == "not_found":
                messagebox.showerror("Error", "❌ Security not found.")
            else:
                messagebox.showinfo("Sold", f"✅ Sold {amount} of {choices[choice]}")
        else:
            messagebox.showerror("Error", "Invalid choice.")

    def get_advice(self):
        question = simpledialog.askstring("Ask AI", "Enter your investment question:")
        if question:
            answer = self.portfolio.controller.get_advice(question)
            messagebox.showinfo("AI Advice", answer)

    def display_table(self):
        data = self.portfolio.controller.dbmodel.get_data()

        if not data:
            messagebox.showwarning("Portfolio", "⚠️ No investments found in the portfolio.")
            return

        table_data = [[v["id"], v["name"], v["base_value"], v["amount"]] for v in data.values()]
        headers = ["ID", "Name", "Base Value", "Amount"]
        text = tabulate(table_data, headers=headers, tablefmt="grid")

        self._show_large_text("Portfolio Table", text)

    def display_risk(self):
        risk = self.portfolio.db.calculate_portfolio_risk()
        messagebox.showinfo("Portfolio Risk", f"⚠️ Risk Level: {risk}")

    def _show_large_text(self, title, content):
        window = tk.Toplevel(self.root)
        window.title(title)
        text_widget = tk.Text(window, wrap="word", width=80, height=20, bg="#F9F9F9", fg="black")
        text_widget.insert("1.0", content)
        text_widget.pack(expand=True, fill="both")
        tk.Button(window, text="Close", command=window.destroy, bg="#E0E0E0").pack(pady=5)
