from personal_finance import FinanceManager


def test_add_income() -> None:
    """
    Test that add_income correctly adds an income transaction and updates balance.
    """
    fm = FinanceManager()
    initial_transactions = len(fm.get_transactions())
    fm.add_income(1000.0, 'Salary')
    transactions = fm.get_transactions()
    assert len(transactions) == initial_transactions + 1, "Transaction count should increase by 1"
    last_trans = transactions[-1]
    assert last_trans['type'] == 'income', "Transaction type should be income"
    assert last_trans['amount'] == 1000.0, "Transaction amount should be 1000.0"
    assert last_trans['category'] == 'Salary', "Category should be Salary"
    balance = fm.calculate_balance()
    assert balance == 1000.0, "Balance should equal income when no expenses are logged"


def test_add_expense() -> None:
    """
    Test that add_expense correctly adds an expense transaction.
    """
    fm = FinanceManager()
    fm.add_expense(200.0, 'Food')
    transactions = fm.get_transactions()
    last_trans = transactions[-1]
    assert last_trans['type'] == 'expense', "Transaction type should be expense"
    assert last_trans['amount'] == 200.0, "Expense amount should be 200.0"
    assert last_trans['category'] == 'Food', "Category should be Food"
    balance = fm.calculate_balance()
    assert balance == -200.0, "Balance should be negative if only expense is logged"


def test_set_budget_and_alerts() -> None:
    """
    Test that setting a budget and exceeding it triggers an alert.
    """
    fm = FinanceManager()
    fm.set_budget('Entertainment', 100.0)
    # Log expense below budget
    fm.add_expense(50.0, 'Entertainment')
    alerts = fm.get_budget_alerts()
    assert len(alerts) == 0, "No alert should be triggered if budget is not exceeded"

    # Log expense that exceeds the remaining budget
    fm.add_expense(60.0, 'Entertainment')
    alerts = fm.get_budget_alerts()
    assert len(alerts) == 1, "Alert should be triggered when budget is exceeded"
    assert 'Entertainment' in alerts[0], "Alert message should mention the Entertainment category"


def test_calculate_balance_and_savings_rate() -> None:
    """
    Test balance and savings rate calculations with a mix of incomes and expenses.
    """
    fm = FinanceManager()
    fm.add_income(2000.0, 'Salary')
    fm.add_expense(500.0, 'Rent')
    fm.add_expense(300.0, 'Food')
    balance = fm.calculate_balance()
    expected_balance = 2000.0 - (500.0 + 300.0)
    assert balance == expected_balance, "Balance calculation is incorrect"

    savings_rate = fm.calculate_savings_rate()
    expected_rate = (2000.0 - 800.0) / 2000.0
    assert abs(savings_rate - expected_rate) < 1e-6, "Savings rate calculation is incorrect"


def test_get_top_spending_category() -> None:
    """
    Test that the category with the highest expense is correctly identified.
    """
    fm = FinanceManager()
    fm.add_expense(300.0, 'Food')
    fm.add_expense(400.0, 'Rent')
    fm.add_expense(200.0, 'Entertainment')
    top_category = fm.get_top_spending_category()
    assert top_category == 'Rent', "Top spending category should be Rent"


if __name__ == '__main__':
    test_add_income()
    print('test_add_income passed')
    test_add_expense()
    print('test_add_expense passed')
    test_set_budget_and_alerts()
    print('test_set_budget_and_alerts passed')
    test_calculate_balance_and_savings_rate()
    print('test_calculate_balance_and_savings_rate passed')
    test_get_top_spending_category()
    print('test_get_top_spending_category passed')
    print('All tests passed successfully.')
