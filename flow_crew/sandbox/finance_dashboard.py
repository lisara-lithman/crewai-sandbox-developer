import datetime

class Transaction:
    def __init__(self, trans_type, category, amount, date=None):
        self.trans_type = trans_type  # 'income' or 'expense'
        self.category = category
        self.amount = amount
        self.date = date if date else datetime.datetime.now()

    def to_dict(self):
        return {
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': self.trans_type,
            'category': self.category,
            'amount': self.amount
        }

class FinanceManager:
    def __init__(self):
        # Store transactions as a list of Transaction objects
        self.transactions = []
        # Budgets stored as a dict mapping categories to monthly limits
        self.budgets = {}

    # Add income transaction
    def log_income(self, category, amount):
        if amount <= 0:
            raise ValueError('Income amount must be positive.')
        trans = Transaction('income', category, amount)
        self.transactions.append(trans)
        return trans

    # Add expense transaction; checks budget setting and returns an alert if necessary
    def log_expense(self, category, amount):
        if amount <= 0:
            raise ValueError('Expense amount must be positive.')
        trans = Transaction('expense', category, amount)
        self.transactions.append(trans)
        alert = self._check_budget_alert(category)
        return trans, alert

    # Set or update a monthly budget for a given category
    def set_budget(self, category, limit):
        if limit <= 0:
            raise ValueError('Budget limit must be positive.')
        self.budgets[category] = limit
        return {category: limit}

    # Get all transactions as list of dictionaries
    def get_transactions(self):
        return [t.to_dict() for t in self.transactions]

    # Calculate total balance = sum(incomes) - sum(expenses)
    def get_total_balance(self):
        total_income = sum(t.amount for t in self.transactions if t.trans_type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.trans_type == 'expense')
        return total_income - total_expense

    # Calculate savings rate as (total income - total expense) / total income (if income > 0) else 0
    def get_savings_rate(self):
        total_income = sum(t.amount for t in self.transactions if t.trans_type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.trans_type == 'expense')
        if total_income > 0:
            return (total_income - total_expense) / total_income
        return 0

    # Identify the top spending category, i.e. the category with the highest total expenses
    def get_top_spending_category(self):
        expense_totals = {}
        for t in self.transactions:
            if t.trans_type == 'expense':
                expense_totals[t.category] = expense_totals.get(t.category, 0) + t.amount
        if not expense_totals:
            return None
        # Get category with max expense
        top_category = max(expense_totals, key=expense_totals.get)
        return top_category, expense_totals[top_category]

    # Check if the current month's expenses in the category exceed the set budget
    def _check_budget_alert(self, category):
        # If no budget is set for the category, no alert
        if category not in self.budgets:
            return None
        # Sum expenses for this category in the current month
        now = datetime.datetime.now()
        current_month = now.month
        current_year = now.year
        total_expense = 0
        for t in self.transactions:
            if t.trans_type == 'expense' and t.category == category:
                if t.date.year == current_year and t.date.month == current_month:
                    total_expense += t.amount
        if total_expense > self.budgets[category]:
            return f"Alert: Category '{category}' has exceeded its budget of {self.budgets[category]}. Current expense: {total_expense}."
        return None

    # Method to get dashboard data
    def get_dashboard_data(self):
        data = {
            'transactions': self.get_transactions(),
            'total_balance': self.get_total_balance(),
            'savings_rate': self.get_savings_rate(),
            'budget_alerts': self.get_budget_alerts(),
            'top_spending_category': self.get_top_spending_category()
        }
        return data

    # Get all budget alerts for categories that have a budget set
    def get_budget_alerts(self):
        alerts = []
        for category in self.budgets:
            alert = self._check_budget_alert(category)
            if alert:
                alerts.append(alert)
        return alerts

# The following main section is for demo purposes and simple testing of the backend logic.
if __name__ == '__main__':
    fm = FinanceManager()

    # Set up budgets for some categories
    fm.set_budget('Food', 500)
    fm.set_budget('Rent', 1500)
    fm.set_budget('Entertainment', 300)
    fm.set_budget('Savings', 1000)  # Though Savings isn't expense, we keep it for demo

    # Log some transactions:
    fm.log_income('Salary', 4000)
    fm.log_income('Freelance', 500)
    
    # Some expenses
    trans, alert = fm.log_expense('Food', 200)
    if alert:
        print(alert)

    trans, alert = fm.log_expense('Rent', 1400)
    if alert:
        print(alert)

    trans, alert = fm.log_expense('Entertainment', 350)
    if alert:
        print(alert)

    trans, alert = fm.log_expense('Food', 350)  # This should trigger budget alert for Food total > 500
    if alert:
        print(alert)

    # Print dashboard data
    dashboard = fm.get_dashboard_data()
    print('\nDashboard Data:')
    print(f"Total Balance: {dashboard['total_balance']}")
    print(f"Savings Rate: {dashboard['savings_rate'] * 100:.2f}%")
    print(f"Top Spending Category: {dashboard['top_spending_category']}")
    print('Transactions:')
    for t in dashboard['transactions']:
        print(t)
    print('Budget Alerts:')
    for alert in dashboard['budget_alerts']:
        print(alert)
