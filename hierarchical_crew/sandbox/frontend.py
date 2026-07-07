import gradio as gr
from backend import FinanceManager, Transaction

# Create a FinanceManager instance to be shared by frontend callbacks
finance_manager = FinanceManager()

# --- Callback functions ---

def submit_transaction(transaction_type: str, category: str, amount: float):
    try:
        amount = float(amount)
    except ValueError:
        return "Invalid amount. Please enter a numeric value."
    if amount <= 0:
        return "Amount must be positive."

    transaction = Transaction(transaction_type, category, amount)
    finance_manager.add_transaction(transaction)
    return update_dashboard()


def update_dashboard():
    # Prepare transactions data for gr.DataFrame display as list of dicts
    transactions = [t.to_dict() for t in finance_manager.get_all_transactions()]
    total_balance = finance_manager.get_total_balance()
    savings_rate = finance_manager.get_savings_rate()
    alerts = finance_manager.get_active_budget_alerts()
    top_spending = finance_manager.get_top_spending_category()

    dashboard_info = f"**Total Balance:** {total_balance:.2f}\n"
    dashboard_info += f"**Savings Rate:** {savings_rate*100:.2f}%\n"
    dashboard_info += f"**Top Spending Category:** {top_spending}\n"
    if alerts:
        dashboard_info += "**Alerts:**\n" + '\n'.join(alerts)
    else:
        dashboard_info += "**Alerts:** None"

    return transactions, dashboard_info


def submit_budget(category: str, limit: float):
    try:
        limit = float(limit)
    except ValueError:
        return "Invalid limit. Please enter a numeric value."
    if limit <= 0:
        return "Budget limit must be positive."

    finance_manager.set_budget(category, limit)
    return update_dashboard()

# --- Define categories ---
categories = ['Food', 'Rent', 'Entertainment', 'Savings']

# --- Build UI using Gradio Blocks ---
with gr.Blocks() as demo:
    with gr.Tab('Financial Dashboard'):
        dashboard_table = gr.DataFrame(label='All Transactions', headers=['Type', 'Category', 'Amount'], interactive=False, datatype=['str', 'str', 'number'])
        dashboard_info = gr.Markdown(label='Summary')
        # Refresh button to update dashboard manually
        refresh_btn = gr.Button('Refresh Dashboard')

        refresh_btn.click(fn=update_dashboard, inputs=[], outputs=[dashboard_table, dashboard_info])

    with gr.Tab('Transaction Entry'):
        with gr.Row():
            trans_type = gr.Dropdown(choices=['income', 'expense'], label='Transaction Type')
            category_input = gr.Dropdown(choices=categories, label='Category')
            amount_input = gr.Number(label='Amount')
        submit_trans_btn = gr.Button('Submit Transaction')
        trans_output = gr.Markdown(label='Transaction Submission Status')

        submit_trans_btn.click(fn=submit_transaction, 
                                 inputs=[trans_type, category_input, amount_input], 
                                 outputs=trans_output)

    with gr.Tab('Budget Settings'):
        with gr.Row():
            budget_category = gr.Dropdown(choices=categories, label='Category')
            budget_limit = gr.Number(label='Budget Limit')
        submit_budget_btn = gr.Button('Set Budget')
        budget_output = gr.Markdown(label='Budget Setting Status')

        submit_budget_btn.click(fn=submit_budget, 
                                  inputs=[budget_category, budget_limit], 
                                  outputs=budget_output)

    # Initialize dashboard on startup
    demo.load(fn=update_dashboard, inputs=[], outputs=[dashboard_table, dashboard_info])

if __name__ == '__main__':
    demo.launch()