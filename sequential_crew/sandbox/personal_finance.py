from datetime import datetime


class FinanceManager:
    """
    A class to manage personal finance records including transactions and budgets.
    """
    def __init__(self) -> None:
        """
        Initialize the FinanceManager with empty transactions list and budgets dictionary.
        """
        self.transactions = []
        self.budgets = {}
        self._next_id = 1

    def add_transaction(self, trans_type: str, amount: float, category: str) -> None:
        """
        Log a transaction with a type (income or expense), category and amount.
        Generates a new transaction id and timestamp, then adds to the transactions list.
        
        Args:
            trans_type (str): 'income' or 'expense'
            amount (float): The amount of the transaction
            category (str): The category for the transaction
        """
        if trans_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be either 'income' or 'expense'.")
        transaction = {
            'id': self._next_id,
            'type': trans_type,
            'category': category,
            'amount': amount,
            'timestamp': datetime.now()
        }
        self.transactions.append(transaction)
        self._next_id += 1

    def add_income(self, amount: float, category: str) -> None:
        """
        Log an income transaction.
        
        Args:
            amount (float): Amount of income
            category (str): Category of income
        """
        self.add_transaction('income', amount, category)

    def add_expense(self, amount: float, category: str) -> None:
        """
        Log an expense transaction.
        
        Args:
            amount (float): Amount of expense
            category (str): Category of expense
        """
        self.add_transaction('expense', amount, category)

    def set_budget(self, category: str, limit: float) -> None:
        """
        Set or update the monthly budget limit for a given category.
        
        Args:
            category (str): The category to set the budget for
            limit (float): The budget limit amount
        """
        self.budgets[category] = limit

    def get_transactions(self) -> list:
        """
        Return the list of all transaction dictionaries.
        
        Returns:
            list: A list of transaction dictionaries
        """
        return self.transactions

    def calculate_balance(self) -> float:
        """
        Calculate the current balance as total income minus total expense.
        
        Returns:
            float: The net balance
        """
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        return total_income - total_expense

    def calculate_savings_rate(self) -> float:
        """
        Calculate the savings rate: (total income - total expense) / total income.
        Returns 0 if there is no income to avoid division by zero.
        
        Returns:
            float: The savings rate as a floating point number.
        """
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        if total_income == 0:
            return 0.0
        return (total_income - total_expense) / total_income

    def get_top_spending_category(self) -> str:
        """
        Identify and return the category with the highest total expense.
        If there are no expenses, returns an empty string.
        
        Returns:
            str: The category name with highest expense.
        """
        expense_totals = {}
        for t in self.transactions:
            if t['type'] == 'expense':
                expense_totals[t['category']] = expense_totals.get(t['category'], 0) + t['amount']
        if not expense_totals:
            return ""
        # find the category with maximum expense
        top_category = max(expense_totals, key=expense_totals.get)
        return top_category

    def get_budget_alerts(self) -> list:
        """
        Check if any category's summed expenses exceed the set budget and return a list of alert messages.
        
        Returns:
            list: A list of string alerts for categories exceeding their budget.
        """
        alerts = []
        # Calculate expenses per category
        expenses_by_category = {}
        for t in self.transactions:
            if t['type'] == 'expense':
                expenses_by_category[t['category']] = expenses_by_category.get(t['category'], 0) + t['amount']
        # Check against budgets
        for category, limit in self.budgets.items():
            if expenses_by_category.get(category, 0) > limit:
                alerts.append(f"Alert: Expenses for {category} have exceeded the budget limit of {limit}.")
        return alerts
