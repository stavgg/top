# מחלקת בסיס לניירות ערך
class Security:
    def __init__(self, name, base_value, amount):  # אתחול תכונות כלליות
        self.name = name
        self.base_value = base_value
        self.amount = amount

    def get_value(self):  # מחזיר את הערך הכולל של נייר הערך
        return self.base_value * self.amount

    def __str__(self):  # מציג את פרטי נייר הערך
        return f"Security: {self.name}, Value: {self.get_value()}"


# מחלקת מניה - יורשת מנייר ערך
class Stock(Security):
    def __init__(self, name, base_value, amount, industry, volatility):
        super().__init__(name, base_value, amount)
        self.industry = industry
        self.volatility = volatility

    def get_risk_level(self):  # קביעת רמת הסיכון של המניה לפי הענף והתנודתיות
        industry_risk = {
            "Technology": 6,
            "Transportation": 5,
            "Energy & Health": 4,
            "Industry & Finance": 3,
            "Real Estate": 2,
            "Consumer": 1
        }
        risk_score = industry_risk.get(self.industry, 1) * (2 if self.volatility == "High" else 1)
        return risk_score

    def __str__(self):  # מציג את פרטי המניה
        return f"Stock: {self.name}, Industry: {self.industry}, Risk Level: {self.get_risk_level()}"


# מחלקה מניה רגילה
class CommonStock(Stock):
    def __init__(self, name, base_value, amount, industry, volatility, voting_rights=True):
        super().__init__(name, base_value, amount, industry, volatility)
        self.voting_rights = voting_rights

    def __str__(self):
        return f"Common Stock: {self.name}, Industry: {self.industry}, Voting Rights: {self.voting_rights}, Risk Level: {self.get_risk_level()}"


# מחלקה מניה מועדפת
class PreferredStock(Stock):
    def __init__(self, name, base_value, amount, industry, volatility, fixed_dividend):
        super().__init__(name, base_value, amount, industry, volatility)
        self.fixed_dividend = fixed_dividend

    def __str__(self):
        return f"Preferred Stock: {self.name}, Industry: {self.industry}, Fixed Dividend: {self.fixed_dividend}, Risk Level: {self.get_risk_level()}"


# מחלקת אג״ח - יורשת מנייר ערך
class Bond(Security):
    def __init__(self, name, base_value, amount, issuer, bond_type):
        super().__init__(name, base_value, amount)
        self.issuer = issuer
        self.bond_type = bond_type

    def get_risk_level(self):  # קביעת רמת הסיכון של האג״ח לפי סוג ההנפקה
        if self.bond_type == "Government":
            return 1
        elif self.bond_type == "Corporate":
            return 5
        return 3  # ערך ברירת מחדל

    def __str__(self):  # מציג את פרטי האג״ח
        return f"Bond: {self.name}, Issuer: {self.issuer}, Type: {self.bond_type}, Risk Level: {self.get_risk_level()}"


# אג"ח ממשלתי
class GovernmentBond(Bond):
    def __init__(self, name, base_value, amount, issuer, maturity_years):
        super().__init__(name, base_value, amount, issuer, bond_type="Government")
        self.maturity_years = maturity_years

    def __str__(self):
        return f"Government Bond: {self.name}, Issuer: {self.issuer}, Maturity: {self.maturity_years} years, Risk Level: {self.get_risk_level()}"


# אג"ח קונצרני
class CorporateBond(Bond):
    def __init__(self, name, base_value, amount, issuer, credit_rating):
        super().__init__(name, base_value, amount, issuer, bond_type="Corporate")
        self.credit_rating = credit_rating

    def __str__(self):
        return f"Corporate Bond: {self.name}, Issuer: {self.issuer}, Credit Rating: {self.credit_rating}, Risk Level: {self.get_risk_level()}"