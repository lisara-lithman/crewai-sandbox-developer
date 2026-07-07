from typing import List, Dict

class Transaction:
    def __init__(self, transaction_type: str, category: str, amount: float) -> None:
        if transaction_type not in ['income', 'expense']:
            raise ValueError("transaction_type must be either 'income' or 'expense'")
        self.transaction_type = transaction_type
        self.category = category
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            'Type': self.transaction_type,
            'Category': self.category,
            'Amount': self.amount
        }


class FinanceManager:
    def __init__(self) -> None:
        self.transactions: List[Transaction] = []
        self.budgets: Dict[str, float] = {}

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        # Immediately check if this expense exceeds the current budget (if applicable)
        if transaction.transaction_type == 'expense':
            if transaction.category in self.budgets:
                total_expense = sum(t.amount for t in self.transactions 
                                    if t.transaction_type == 'expense' and t.category == transaction.category)
                if total_expense > self.budgets[transaction.category]:
                    # Could log or handle an alert, but alerts are generated in get_active_budget_alerts
                    pass

    def set_budget(self, category: str, limit: float) -> None:
        self.budgets[category] = limit
        # Optionally re-check transactions for alerting in UI (alerts computed dynamically in get_active_budget_alerts)

    def get_total_balance(self) -> float:
        total_income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return total_income - total_expense

    def get_savings_rate(self) -> float:
        total_income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        if total_income == 0:
            return 0.0
        return (total_income - total_expense) / total_income

    def get_active_budget_alerts(self) -> List[str]:
        alerts = []
        # For each budget, check the total expense
        for category, limit in self.budgets.items():
            total_expense = sum(t.amount for t in self.transactions if t.transaction_type == 'expense' and t.category == category)
            if total_expense > limit:
                excess = total_expense - limit
                alerts.append(f"Alert: {category} expenses exceed budget by {excess:.2f}")
        return alerts

    def get_top_spending_category(self) -> str:
        spending: Dict[str, float] = {}
        for t in self.transactions:
            if t.transaction_type == 'expense':
                spending[t.category] = spending.get(t.category, 0.0) + t.amount
        if not spending:
            return "None"
        # Return category with maximum expense
        top_category = max(spending, key=spending.get)
        return top_category

    def get_all_transactions(self) -> List[Transaction]:
        return self.transactions
