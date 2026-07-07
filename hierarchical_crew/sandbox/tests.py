import unittest
from backend import FinanceManager, Transaction

class TestFinanceManager(unittest.TestCase):
    def setUp(self):
        self.fm = FinanceManager()
        # Set up default category budgets for testing
        self.categories = ['Food', 'Rent', 'Entertainment', 'Savings']
        for cat in self.categories:
            # Set a high default budget so that initial tests pass unless we want an alert
            self.fm.set_budget(cat, 1000.0)

    def test_add_transaction(self):
        # Test adding income and expense
        income = Transaction('income', 'Savings', 500)
        expense = Transaction('expense', 'Food', 100)
        self.fm.add_transaction(income)
        self.fm.add_transaction(expense)
        self.assertEqual(len(self.fm.transactions), 2)

    def test_total_balance(self):
        income1 = Transaction('income', 'Savings', 1000)
        income2 = Transaction('income', 'Savings', 500)
        expense = Transaction('expense', 'Food', 300)
        self.fm.add_transaction(income1)
        self.fm.add_transaction(income2)
        self.fm.add_transaction(expense)
        total_balance = self.fm.get_total_balance()
        self.assertEqual(total_balance, 1200)

    def test_savings_rate(self):
        # Scenario with income and expense
        income = Transaction('income', 'Savings', 1000)
        expense = Transaction('expense', 'Food', 200)
        self.fm.add_transaction(income)
        self.fm.add_transaction(expense)
        savings_rate = self.fm.get_savings_rate()
        self.assertAlmostEqual(savings_rate, 0.8)
        
        # Scenario where income is zero should return 0 savings rate
        fm2 = FinanceManager()
        expense2 = Transaction('expense', 'Food', 200)
        fm2.add_transaction(expense2)
        self.assertEqual(fm2.get_savings_rate(), 0.0)

    def test_budget_alerts(self):
        # Expense within budget: no alert
        expense = Transaction('expense', 'Food', 500)
        self.fm.add_transaction(expense)
        alerts = self.fm.get_active_budget_alerts()
        self.assertEqual(alerts, [])

        # Expense that exceeds budget: alert is generated
        self.fm = FinanceManager()  # reset
        self.fm.set_budget('Food', 100)
        # Add expenses in multiple steps, so that final total exceeds budget
        expense1 = Transaction('expense', 'Food', 60)
        expense2 = Transaction('expense', 'Food', 50)
        self.fm.add_transaction(expense1)
        self.fm.add_transaction(expense2)
        alerts = self.fm.get_active_budget_alerts()
        self.assertTrue(len(alerts) > 0)
        self.assertIn('Food', alerts[0])

    def test_top_spending_category(self):
        # When no expenses, should return 'None'
        top_category = self.fm.get_top_spending_category()
        self.assertEqual(top_category, 'None')
        
        # Add expenses and determine top spending category
        expense_food = Transaction('expense', 'Food', 150)
        expense_rent = Transaction('expense', 'Rent', 700)
        expense_entertainment = Transaction('expense', 'Entertainment', 200)
        self.fm.add_transaction(expense_food)
        self.fm.add_transaction(expense_rent)
        self.fm.add_transaction(expense_entertainment)
        top_category = self.fm.get_top_spending_category()
        self.assertEqual(top_category, 'Rent')

if __name__ == '__main__':
    unittest.main()