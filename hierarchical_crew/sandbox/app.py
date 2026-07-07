import gradio as gr
from backend import FinanceManager, Transaction

# Create a shared FinanceManager instance
finance_manager = FinanceManager()

# Define fixed categories
categories = ['Food', 'Rent', 'Entertainment', 'Savings']


def update_dashboard():
    """Retrieve transactions and financial summary information."""
    transactions = [t.to_dict() for t in finance_manager.get_all_transactions()]
    total_balance = finance_manager.get_total_balance()
    savings_rate = finance_manager.get_savings_rate()
    alerts = finance_manager.get_active_budget_alerts()
    top_spending = finance_manager.get_top_spending_category()

    dashboard_info = f"**Total Balance:** {total_balance:.2f}\n"
    dashboard_info += f"**Savings Rate:** {savings_rate * 100:.2f}%\n"
    dashboard_info += f"**Top Spending Category:** {top_spending}\n"
    if alerts:
        dashboard_info += "**Alerts:**\n" + "\n".join(alerts)
    else:
        dashboard_info += "**Alerts:** None"

    return transactions, dashboard_info


def submit_transaction(transaction_type: str, category: str, amount: float):
    """Submit a new transaction (income or expense) and update dashboard."""
    try:
        amount = float(amount)
    except ValueError:
        return "Invalid amount. Please enter a numeric value."
    if amount <= 0:
        return "Amount must be positive."

    txn = Transaction(transaction_type, category, amount)
    finance_manager.add_transaction(txn)
    # Update the dashboard after submission
    _, dashboard_info = update_dashboard()
    return dashboard_info


def submit_budget(category: str, limit: float):
    """Set or update the budget for a category and update dashboard."""
    try:
        limit = float(limit)
    except ValueError:
        return "Invalid limit. Please enter a numeric value."
    if limit <= 0:
        return "Budget limit must be positive."

    finance_manager.set_budget(category, limit)
    # Update the dashboard after setting the budget
    _, dashboard_info = update_dashboard()
    return dashboard_info


# Build the UI using Gradio Blocks (Gradio 6 API)
with gr.Blocks() as demo:
    gr.Markdown("## Personal Finance Dashboard")
    with gr.Tabs():
        with gr.TabItem("Financial Dashboard"):
            # Create a DataFrame to display transactions and a Markdown for summary
            transactions_table = gr.DataFrame(value=[], headers=['Type', 'Category', 'Amount'], interactive=False, datatype=['str', 'str', 'number'])
            dashboard_markdown = gr.Markdown("Dashboard summary will appear here...")
            refresh_btn = gr.Button("Refresh Dashboard")
            refresh_btn.click(fn=update_dashboard, inputs=[], outputs=[transactions_table, dashboard_markdown])

        with gr.TabItem("Transaction Entry"):
            with gr.Row():
                transaction_type_dropdown = gr.Dropdown(choices=['income', 'expense'], label='Transaction Type', value='income')
                category_dropdown = gr.Dropdown(choices=categories, label='Category')
                amount_input = gr.Number(label='Amount')
            submit_trans_btn = gr.Button("Submit Transaction")
            transaction_status_markdown = gr.Markdown("")
            submit_trans_btn.click(fn=submit_transaction, inputs=[transaction_type_dropdown, category_dropdown, amount_input], outputs=transaction_status_markdown)

        with gr.TabItem("Budget Settings"):
            with gr.Row():
                budget_category_dropdown = gr.Dropdown(choices=categories, label='Category')
                budget_limit_input = gr.Number(label='Budget Limit')
            submit_budget_btn = gr.Button("Set Budget")
            budget_status_markdown = gr.Markdown("")
            submit_budget_btn.click(fn=submit_budget, inputs=[budget_category_dropdown, budget_limit_input], outputs=budget_status_markdown)

    # Pre-load the dashboard information when the app loads
    demo.load(fn=update_dashboard, inputs=[], outputs=[transactions_table, dashboard_markdown])

if __name__ == '__main__':
    demo.launch()
