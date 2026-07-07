import gradio as gr
from personal_finance import FinanceManager

# Create a single instance of FinanceManager to be shared across the app
manager = FinanceManager()


def fetch_dashboard_data():
    """
    Aggregates dashboard data including transactions, balance, savings rate, budget alerts, and top spending category.

    Returns:
        tuple: (transactions, balance, savings_rate, alerts (as string), top_spending_category)
    """
    transactions = manager.get_transactions()
    balance = manager.calculate_balance()
    savings_rate = manager.calculate_savings_rate()
    alerts_list = manager.get_budget_alerts()
    top_category = manager.get_top_spending_category()
    alerts = "\n".join(alerts_list)
    return transactions, balance, savings_rate, alerts, top_category


def log_income(category: str, amount: float):
    """
    Callback to log income and return updated dashboard data.

    Args:
        category (str): Category of income.
        amount (float): Income amount.

    Returns:
        tuple: Updated dashboard data.
    """
    manager.add_income(amount, category)
    return fetch_dashboard_data()


def log_expense(category: str, amount: float):
    """
    Callback to log an expense and return updated dashboard data.

    Args:
        category (str): Category of expense.
        amount (float): Expense amount.

    Returns:
        tuple: Updated dashboard data.
    """
    manager.add_expense(amount, category)
    return fetch_dashboard_data()


def set_budget(category: str, limit: float):
    """
    Callback to set or update a budget for a category. Returns a confirmation message and updated budget alerts.

    Args:
        category (str): The category to set the budget for.
        limit (float): The budget limit.

    Returns:
        tuple: (confirmation message, updated budget alerts as string).
    """
    manager.set_budget(category, limit)
    alerts_list = manager.get_budget_alerts()
    alerts = "\n".join(alerts_list)
    return f"Budget for {category} is set to {limit}", alerts


# Custom CSS for color palette and a professional look in both light and dark modes
custom_css = '''
body {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4, h5, h6 {
    color: #ecad0a; 
}

button {
    background-color: #753991;
    color: #ffffff;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #5e2f7a;
}

.gradio-container {
    border: 2px solid #209dd7;
    border-radius: 8px;
    padding: 10px;
}

/* Additional tweaks for dark mode support */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #222;
        color: #ddd;
    }
    .gradio-container {
        border-color: #209dd7;
    }
}
'''


# Build the Gradio app with a multi-tab layout
demo = gr.Blocks(css=custom_css, title="Personal Finance Dashboard")

with demo:
    gr.Markdown("# Personal Finance Dashboard")
    with gr.Tabs():
        # Tab 1: Financial Dashboard
        with gr.TabItem('Financial Dashboard'):
            with gr.Row():
                dashboard_button = gr.Button('Refresh Dashboard')
            with gr.Row():
                df_transactions = gr.Dataframe(label='Transactions')
            with gr.Row():
                balance_display = gr.Number(label='Total Balance')
                savings_rate_display = gr.Number(label='Savings Rate')
            with gr.Row():
                alerts_display = gr.Textbox(label='Budget Alerts')
                top_category_display = gr.Textbox(label='Top Spending Category')

            def dashboard_refresh():
                transactions, balance, savings_rate, alerts, top_category = fetch_dashboard_data()
                return transactions, balance, savings_rate, alerts, top_category

            dashboard_button.click(fn=dashboard_refresh, inputs=[], outputs=[df_transactions, balance_display, savings_rate_display, alerts_display, top_category_display])

        # Tab 2: Transaction Entry
        with gr.TabItem('Transaction Entry'):
            with gr.Row():
                with gr.Column():
                    gr.Markdown('### Log Income')
                    income_category = gr.Textbox(label='Income Category')
                    income_amount = gr.Number(label='Income Amount')
                    income_submit = gr.Button('Submit Income')
                with gr.Column():
                    gr.Markdown('### Log Expense')
                    expense_category = gr.Textbox(label='Expense Category')
                    expense_amount = gr.Number(label='Expense Amount')
                    expense_submit = gr.Button('Submit Expense')

            income_submit.click(fn=log_income, inputs=[income_category, income_amount], outputs=[df_transactions, balance_display, savings_rate_display, alerts_display, top_category_display])
            expense_submit.click(fn=log_expense, inputs=[expense_category, expense_amount], outputs=[df_transactions, balance_display, savings_rate_display, alerts_display, top_category_display])

        # Tab 3: Budget Settings
        with gr.TabItem('Budget Settings'):
            budget_category = gr.Textbox(label='Category')
            budget_limit = gr.Number(label='Budget Limit')
            budget_submit = gr.Button('Set Budget')
            budget_feedback = gr.Textbox(label='Feedback')
            budget_alerts = gr.Textbox(label='Budget Alerts')

            budget_submit.click(fn=set_budget, inputs=[budget_category, budget_limit], outputs=[budget_feedback, budget_alerts])

if __name__ == '__main__':
    demo.launch()
