import gradio as gr
import datetime

# Import the backend FinanceManager from the backend module
# Assuming the backend code is in a file called backend.py in the same directory
# If the backend code is in the same file, you can remove this import and use the classes directly.

try:
    from backend import FinanceManager
except ImportError:
    # If backend.py is not available, define the classes here as a fallback
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

# Create a global instance of FinanceManager
fm = FinanceManager()

# Custom CSS for theming using provided palette
custom_css = '''
/* Light Mode */
body { background-color: #f0f0f0; color: #303030; }

/* Dark Mode */
.dark body { background-color: #303030; color: #f0f0f0; }

.gradio-container { font-family: Arial, sans-serif; }
header { color: #ecad0a; font-weight: bold; }

/* Buttons styling */
button { background-color: #209dd7; border: none; border-radius: 4px; padding: 8px 16px; color: white; }
button:hover { background-color: #753991; }

/* Tab titles */
.tab-title { font-size: 18px; font-weight: bold; color: #753991 !important; }

/* Input fields */
input, .input_text { border: 1px solid #ccc; border-radius: 4px; padding: 6px; }
''' 

# ==========================
# Define functions for UI callbacks
# ==========================

def update_dashboard():
    data = fm.get_dashboard_data()
    transactions = data['transactions']
    total_balance = data['total_balance']
    savings_rate = data['savings_rate'] * 100  # convert to percentage
    top_spending = data['top_spending_category']
    if top_spending:
        top_category, top_amount = top_spending
        top_text = f"{top_category} ($ {top_amount})"
    else:
        top_text = "N/A"
    alerts = data['budget_alerts']
    if not alerts:
        alerts_text = "No alerts."
    else:
        alerts_text = "\n".join(alerts)
    return transactions, f"$ {total_balance}", f"{savings_rate:.2f}%", top_text, alerts_text


def log_income_fn(category, amount):
    try:
        fm.log_income(category, float(amount))
        return f"Income of $ {amount} in category '{category}' logged successfully."
    except Exception as e:
        return str(e)


def log_expense_fn(category, amount):
    try:
        trans, alert = fm.log_expense(category, float(amount))
        msg = f"Expense of $ {amount} in category '{category}' logged successfully."
        if alert:
            msg += f"\n{alert}"
        return msg
    except Exception as e:
        return str(e)


def set_budget_fn(category, limit):
    try:
        fm.set_budget(category, float(limit))
        return f"Budget for category '{category}' set to $ {limit}."
    except Exception as e:
        return str(e)

# ==========================
# Build Gradio UI
# ==========================

def create_ui():
    with gr.Blocks(css=custom_css, title='Personal Finance Dashboard') as demo:
        gr.Markdown("# Personal Finance Dashboard")
        with gr.Tabs():
            # Tab 1: Financial Dashboard
            with gr.TabItem('Dashboard'):
                with gr.Row():
                    refresh_btn = gr.Button('Refresh Dashboard')
                with gr.Row():
                    transactions_df = gr.Dataframe(label='Transactions', headers=["date", "type", "category", "amount"])
                with gr.Row():
                    total_balance_txt = gr.Textbox(label='Total Balance', interactive=False)
                    savings_rate_txt = gr.Textbox(label='Savings Rate', interactive=False)
                with gr.Row():
                    top_spending_txt = gr.Textbox(label='Top Spending Category', interactive=False)
                with gr.Row():
                    alerts_txt = gr.Textbox(label='Budget Alerts', interactive=False)

                refresh_btn.click(fn=update_dashboard, outputs=[transactions_df, total_balance_txt, savings_rate_txt, top_spending_txt, alerts_txt])
                # Auto-refresh dashboard on page load
                demo.load(fn=update_dashboard, outputs=[transactions_df, total_balance_txt, savings_rate_txt, top_spending_txt, alerts_txt])

            # Tab 2: Transaction Entry
            with gr.TabItem('Transaction Entry'):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown('## Log Income')
                        income_category = gr.Textbox(label='Income Category', placeholder='e.g., Salary')
                        income_amount = gr.Number(label='Amount', value=0)
                        income_btn = gr.Button('Log Income')
                        income_output = gr.Textbox(label='Status', interactive=False)
                        income_btn.click(fn=log_income_fn, inputs=[income_category, income_amount], outputs=income_output)
                    with gr.Column():
                        gr.Markdown('## Log Expense')
                        expense_category = gr.Textbox(label='Expense Category', placeholder='e.g., Food, Rent')
                        expense_amount = gr.Number(label='Amount', value=0)
                        expense_btn = gr.Button('Log Expense')
                        expense_output = gr.Textbox(label='Status', interactive=False)
                        expense_btn.click(fn=log_expense_fn, inputs=[expense_category, expense_amount], outputs=expense_output)

            # Tab 3: Budget Settings
            with gr.TabItem('Budget Settings'):
                gr.Markdown('## Set Budget for a Category')
                with gr.Row():
                    budget_category = gr.Textbox(label='Category', placeholder='e.g., Food, Rent')
                    budget_limit = gr.Number(label='Monthly Limit', value=0)
                budget_btn = gr.Button('Set Budget')
                budget_output = gr.Textbox(label='Status', interactive=False)
                budget_btn.click(fn=set_budget_fn, inputs=[budget_category, budget_limit], outputs=budget_output)

    return demo

# If this module is run directly, launch the app
if __name__ == '__main__':
    ui = create_ui()
    ui.launch()
