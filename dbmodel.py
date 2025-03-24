import sqlite3
from securitiesmodel import *

class dbmodel:
    def __init__(self):
        print("DB connect")
        self.conn = sqlite3.connect ('investments.db')

        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                base_value REAL NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def find_by_name(self, name):
        self.cursor.execute('SELECT * FROM investments WHERE name = ?', (name,))
        return self.cursor.fetchone()

    def insert(self, security, amount):
        existing = self.find_by_name(security.name)
        if existing:
            current_amount = existing[3]
            new_amount = current_amount + amount
            self.cursor.execute(
                'UPDATE investments SET amount = ? WHERE name = ?',
                (new_amount, security.name)
            )
            print(f"🔄 Updated {security.name}: {current_amount} ➜ {new_amount}")
        else:
            self.cursor.execute(
                'INSERT INTO investments (name, base_value, amount) VALUES (?, ?, ?)',
                (security.name, security.base_value, amount)
            )
            print(f"🆕 Inserted {security.name} with amount {amount}")
        self.conn.commit()

    def update(self, security):
        self.cursor.execute(
            'UPDATE investments SET amount = ? WHERE name = ?',
            (security.amount, security.name)
        )
        self.conn.commit()
        print(f"✅ Updated {security.name} to amount {security.amount}")

    def delete(self, identifier):
        if isinstance(identifier, str):
            self.cursor.execute('DELETE FROM investments WHERE name = ?', (identifier,))
            self.conn.commit()
            print(f"❌ Deleted {identifier}")
        else:
            print("Invalid identifier for deletion. Use name (str).")

    def get_data(self):
        self.cursor.execute('SELECT * FROM investments')
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        return {row[0]: dict(zip(columns, row)) for row in rows}

    def calculate_portfolio_risk(self):
        self.cursor.execute('SELECT name, base_value, amount FROM investments')
        rows = self.cursor.fetchall()
        if not rows:
            return 0

        total_value = 0
        total_risk = 0
        for name, base_value, amount in rows:
            if "bond" in name.lower():
                security = Bond(name, base_value, amount, "Government", "Government")
            else:
                security = Stock(name, base_value, amount, "Technology", "High")

            value = security.get_value()
            risk = security.get_risk_level()

            total_value += value
            total_risk += value * risk

        return round(total_risk / total_value, 2) if total_value else 0

    def __del__(self):
        self.conn.close()
        print("DB disconnect")

