# Detailed Design for Personal Finance Dashboard

Below is the complete design that meets the specified requirements. This design is divided into three parts based on modules and assignments to the engineers: backend, frontend, and tests.

---

## 1. Backend Module

**File:** backend.py  
**Assigned to:** backend_engineer

### Overview
The backend module will manage in-memory data structures and business logic. It will handle transactions, budgets, and calculate summary statistics like total balance, savings rate, and top spending category.

### Classes and Methods

#### Class: TransactionManager
This class manages all transactions and budget settings.

- **Attributes:**
  - `transactions: list[dict]`  
    A list where each element is a dictionary representing a transaction. Each transaction dictionary should have:
    - `type` (str): either "income" or "expense"
    - `amount` (float)
    - `category` (str)
    - `timestamp` (datetime, optional)

  - `budgets: dict[str, float]`  
    A dictionary mapping each category (e.g., "Food", "Rent") to its monthly budget limit.

- **Methods:**

  - `def __init__(self) -> None`  
    Initialize the `transactions` list and the `budgets` dictionary.

  - `def add_income(self, amount: float, category: str) -> None`  
    Adds an income transaction.  
    *Signature:*  
    `def add_income(self, amount: float, category: str) -> None`

  - `def add_expense(self, amount: float, category: str) -> bool`  
    Adds an expense transaction. Returns a boolean indicating whether a budget warning was triggered for this category.  
    *Signature:*  
    `def add_expense(self, amount: float, category: str) -> bool`

  - `def set_budget(self, category: str, amount: float) -> None`  
    Sets/updates the monthly budget limit for the given category.  
    *Signature:*  
    `def set_budget(self, category: str, amount: float) -> None`

  - `def calculate_total_balance(self) -> float`  
    Calculates the current total balance (sum of incomes minus sum of expenses).  
    *Signature:*  
    `def calculate_total_balance(self) -> float`

  - `def calculate_savings_rate(self) -> float`  
    Calculates the savings rate as a ratio or percentage (total income minus total expenses divided by total income). Ensure to handle cases when total income is zero.  
    *Signature:*  
    `def calculate_savings_rate(self) -> float`

  - `def calculate_top_spending_category(self) -> str`  
    Identifies the category with the highest total expense. Returns the category name.  
    *Signature:*  
    `def calculate_top_spending_category(self) -> str`

  - `def get_budget_alerts(self) -> dict[str, bool]`  
    Given a new transaction expense, check each category expense total against its corresponding budget. Returns a dictionary with keys as category names and booleans as alert states (True if the total expense exceeds the budgeting limit).  
    *Signature:*  
    `def get_budget_alerts(self) -> dict[str, bool]`

  - `def get_dashboard_data(self) -> dict`  
    Collects and returns all relevant dashboard data:
    - A list of transactions (as a dataframe/table format friendly structure)
    - Total balance (float)
    - Savings rate (float)
    - Current budget alerts (dictionary)
    - Top spending category (str)  
    *Signature:*  
    `def get_dashboard_data(self) -> dict`

---

## 2. Frontend Module

**File:** app.py  
**Assigned to:** frontend_engineer

### Overview
The frontend module will feature a Gradio app with a multi-tab layout based on Gradio 6 APIs. There will be three tabs:
- Tab 1: Financial Dashboard (displays a dynamically updated table with metrics)
- Tab 2: Transaction Entry (forms to log income and expense)
- Tab 3: Budget Settings (form to set budgets for each category)

### Gradio 6 API Guidance
- Use `gradio.Blocks()` as the main container.
- Use `gradio.Tab()` for each tab.
- For interactive forms, use components like `gradio.Number`, `gradio.Textbox`, `gradio.Dropdown`, and `gradio.Button`.
- For the table, use `gradio.Dataframe()` for displaying transactions and computed metrics.
- Ensure to call functions from the backend module on interactive events.
- Use updated method signatures and kwarg parameters specific to Gradio 6 (e.g., `live=True` attribute in inputs for dynamic updates if needed).

### Functions to be Exposed in the App

- `def log_income(amount: float, category: str) -> str:`  
  Wraps `TransactionManager.add_income`, updates the state, and returns a confirmation message.  
  *Signature:*  
  `def log_income(amount: float, category: str) -> str`

- `def log_expense(amount: float, category: str) -> str:`  
  Wraps `TransactionManager.add_expense`, checks if a budget alert is triggered, and returns a confirmation message with potential warning.  
  *Signature:*  
  `def log_expense(amount: float, category: str) -> str`

- `def update_budget(category: str, amount: float) -> str:`  
  Calls `TransactionManager.set_budget` and returns a confirmation message.  
  *Signature:*  
  `def update_budget(category: str, amount: float) -> str`

- `def refresh_dashboard() -> dict:`  
  Retrieves the current dashboard data by calling `TransactionManager.get_dashboard_data` and returns the data to update UI components.  
  *Signature:*  
  `def refresh_dashboard() -> dict`

### UI Layout
- **Tab Financial Dashboard:**  
  - Components:  
    - A DataFrame (table) for transactions.
    - Read-only fields/text displays for total balance, savings rate, top spending category.
    - An alert display for any budget warnings.
  - Dynamic updates: Use Gradio’s event triggers (e.g., on_click or live updates) to call `refresh_dashboard`.

- **Tab Transaction Entry:**  
  - Two separate sub-sections: one for Income and one for Expense.
  - For each section, have:
    - A numeric input for amount.
    - A dropdown for category selection (e.g., Food, Rent, Entertainment, Savings).
    - A submit button that triggers `log_income` or `log_expense` respectively.

- **Tab Budget Settings:**  
  - Input fields for each category:
    - A dropdown for selecting the category.
    - A numeric input for budget amount.
    - A button that triggers `update_budget`.

---

## 3. Test Module

**File:** test_backend.py  
**Assigned to:** test_engineer

### Overview
The test module will contain unit tests for the backend functionality. Use Python’s built-in `unittest` framework.

### Tests to Implement

- **Test Transaction Adding:**
  - Test that `add_income` correctly adds an income transaction.
  - Test that `add_expense` correctly adds an expense transaction, and returns a proper alert flag when applicable.

- **Test Balance Calculation:**
  - Verify that `calculate_total_balance` returns the correct total balance given a series of income and expense entries.

- **Test Savings Rate Calculation:**
  - Verify that `calculate_savings_rate` returns the correct percentage, and handles zero-income scenarios.

- **Test Top Spending Category Calculation:**
  - Verify that `calculate_top_spending_category` returns the correct category after several expense transactions.

- **Test Budget Alert Logic:**
  - Set budgets for one or more categories, add expense transactions, and verify that `get_budget_alerts` returns true for overspending and false otherwise.

### Example Unit Test Function Signatures

- `def test_add_income(self) -> None:`
- `def test_add_expense_with_alert(self) -> None:`
- `def test_calculate_total_balance(self) -> None:`
- `def test_calculate_savings_rate(self) -> None:`
- `def test_calculate_top_spending_category(self) -> None:`
- `def test_budget_alerts(self) -> None:`

---

## Summary of Assignments

- **backend_engineer (backend.py):**  
  Implement the TransactionManager class, its methods, and ensure complete in-memory management of transactions and budgets.

- **frontend_engineer (app.py):**  
  Develop a Gradio 6 app with three tabs (Dashboard, Transaction Entry, Budget Settings). Integrate it with the backend module ensuring dynamic data updates on any changes.

- **test_engineer (test_backend.py):**  
  Create a comprehensive suite of unit tests for the backend module using Python’s unittest framework.

This design should meet all the requirements while ensuring a clear separation of concerns. All modules reside in the same directory, and everything runs as a UV project with only Gradio installed as a third-party package.