import tkinter as tk
from src.gui.app import FinanceTrackerApp
from src.gui.charts_view import ChartsView

app = FinanceTrackerApp()
# Mock login
app.db.register_user('test', 'test')
success, user = app.db.authenticate_user('test', 'test')
app.login_success(user)

# Add transaction
app.db.add_transaction(user['id'], 'Expense', 'Food', 10.5, '2023-10-10', 'Lunch')
app.db.add_transaction(user['id'], 'Income', 'Salary', 1000, '2023-10-11', 'Paycheck')

# Test charts view
transactions = app.db.get_transactions(user['id'])
ChartsView(app.container, transactions)
print("GUI test passed")
app.update()
