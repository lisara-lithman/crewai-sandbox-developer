---------------------
# Detailed Design for Personal Finance Dashboard

## Overview

The system consists of three main modules implemented in separate files: `backend.py`, `frontend.py`, and `tests.py`. All data is maintained in active memory only (no persistent storage). The backend processes transactions and calculates financial summaries. The frontend provides a Gradio 6-based multi-tab UI for interacting with the system. The tests ensure the backend logic is functioning as expected.

## Module: backend.py

### Classes

1. **Transaction**
   - Represents a single financial transaction.
   - Attributes:
     • `transaction_type: str` — either 'income' or 'expense'
     • `category: str` — e.g., Food, Rent, Entertainment, Savings
     • `amount: float`
   - Constructor Signature:
     • `def __init__(self, transaction_type: str, category: str, amount: float) -> None`

2. **FinanceManager**
   - Manages transactions and budget settings, as well as performs financial calculations.
   - Attributes:
     • `transactions: List[Transaction]` — list of all transactions
     • `budgets: Dict[str, float]` — mapping from category to its monthly budget limit
   - Methods:
     • `def add_transaction(self, transaction: Transaction) -> None`
       - Adds a new transaction and, if it's an expense, immediately checks if it exceeds the budget for its category.
     • `def set_budget(self, category: str, limit: float) -> None`
       - Sets or updates the monthly budget for a given category.
     • `def get_total_balance(self) -> float`
       - Returns the net balance (sum of incomes minus sum of expenses).
     • `def get_savings_rate(self) -> float`
       - Computes the savings rate as: (total income - total expense) / total income (handle division by zero appropriately).
     • `def get_active_budget_alerts(self) -> List[str]`
       - Returns a list of warning messages for any category where the recorded expense exceeds the budget limit.
     • `def get_top_spending_category(self) -> str`
       - Identifies the category with the highest expense.
     • `def get_all_transactions(self) -> List[Transaction]`
       - Retrieves all transactions.

## Module: frontend.py

### Gradio 6 UI Specification

The frontend module uses the Gradio 6 API to create a multi-tab layout with three distinct tabs:
  
1. **Tab 1: Financial Dashboard**
   - Displays a dynamic table of all transactions using `gr.DataFrame`.
   - Displays current total balance, savings rate, and active budget alerts (e.g., using `gr.Markdown` or `gr.Textbox`).
   - Should automatically update when transactions change.
  
2. **Tab 2: Transaction Entry**
   - Contains interactive forms for logging an income or an expense.
   - Widgets include:
     • A dropdown (`gr.Dropdown`) for selecting category.
     • A numeric input (`gr.Number`) for entering the amount.
     • A button to submit the transaction.
   - A callback function `submit_transaction(transaction_type: str, category: str, amount: float) -> Any` should add a new transaction via the backend.

3. **Tab 3: Budget Settings**
   - Allows the user to set monthly budget limits.
   - Contains:
     • A dropdown (`gr.Dropdown`) for selecting a category.
     • A numerical input (`gr.Number`) for entering the budget limit.
     • A button to apply the budget setting.
   - Connected callback: `submit_budget(category: str, limit: float) -> Any` that calls the backend’s `set_budget` method.

### Gradio 6 API Guidance for Frontend Engineer

- Use `gr.Blocks()` for the main container.
- Create tabs with `with gr.Tab('Tab Name'):`. In Gradio 6, the `label` parameter can be passed as a positional argument in some cases.
- Ensure callback functions attached to buttons use the latest method signature (for example, use `btn.click(fn=submit_transaction, inputs=[...], outputs=[...])`).
- Take note of the updated kwargs for widgets by consulting the Gradio 6 documentation (e.g., correct parameters for `gr.DataFrame`, `gr.Dropdown`, `gr.Number`, and `gr.Markdown`).

### Essential Frontend Function Signatures

• `def submit_transaction(transaction_type: str, category: str, amount: float) -> Any`
  
• `def update_dashboard() -> dict`
   - Returns updated values: transactions table, total balance, savings rate, and alerts.
  
• `def submit_budget(category: str, limit: float) -> Any`

## Module: tests.py

### Testing Strategy (using Python’s unittest)

Create unit tests for the backend features, especially for:

1. **Transaction Addition**
   - Verify that adding income and expense transactions works correctly.
  
2. **Total Balance Calculation**
   - Confirm that the balance reflects incomes minus expenses.
  
3. **Savings Rate Calculation**
   - Verify correct computation of the savings rate, including handling of division by zero.
  
4. **Budget Alerts**
   - Ensure that when a new expense pushes a category over its budget, an alert is generated.
  
5. **Top Spending Category**
   - Check that the category with the maximum expenses is correctly determined.

### Test Class Structure

• `class TestFinanceManager(unittest.TestCase):`
   - `def setUp(self) -> None`
     - Initialize a FinanceManager object with a clean state.
   - `def test_add_transaction(self) -> None`
   - `def test_total_balance(self) -> None`
   - `def test_savings_rate(self) -> None`
   - `def test_budget_alerts(self) -> None`
   - `def test_top_spending_category(self) -> None`

---------------------

## Assignment to Engineers

• **backend_engineer:**
   - Implement `backend.py` with the `Transaction` class and `FinanceManager` class including all described methods.
   - Ensure that all data is maintained in memory and that logic for budget checking and alerting is correctly executed.

• **frontend_engineer:**
   - Develop `frontend.py` using Gradio 6 to build a multi-tab interface.
   - Create:
     - A "Financial Dashboard" tab that shows a dynamic transaction table, total balance, savings rate, and alerts.
     - A "Transaction Entry" tab with forms to log income and expense.
     - A "Budget Settings" tab to allow users to set and update budgets.
   - Connect UI widgets to backend functions using the latest Gradio 6 API conventions (check documentation for any updated parameter names and structure, e.g., for `gr.Blocks` and `gr.Tab`).
  
• **test_engineer:**
   - Write `tests.py` using Python’s unittest framework.
   - Provide comprehensive tests covering transaction addition, balance calculation, savings rate, budget alert generation, and identification of the top spending category.

---------------------

This detailed design provides a roadmap for implementing the Personal Finance Dashboard system per the requirements. All modules are in the same directory and are structured to run in a uv project with Gradio installed.