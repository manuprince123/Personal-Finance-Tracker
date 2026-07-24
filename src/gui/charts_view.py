import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartsView:
    def __init__(self, parent, transactions):
        self.top = tk.Toplevel(parent)
        self.top.title("Financial Charts")
        self.top.geometry("800x500")
        
        self.transactions = transactions
        self.df = pd.DataFrame(transactions)
        
        self._build_ui()
        
    def _build_ui(self):
        # Create a frame for the charts
        chart_frame = tk.Frame(self.top)
        chart_frame.pack(fill="both", expand=True)
        
        # Matplotlib Figure
        fig = Figure(figsize=(10, 4), dpi=100)
        
        # 1. Expense Pie Chart
        ax1 = fig.add_subplot(121)
        expense_df = self.df[self.df['type'] == 'Expense']
        if not expense_df.empty:
            expense_by_cat = expense_df.groupby('category')['amount'].sum()
            ax1.pie(expense_by_cat, labels=expense_by_cat.index, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Expenses by Category")
        else:
            ax1.text(0.5, 0.5, "No Expense Data", ha='center', va='center')
            ax1.set_title("Expenses by Category")
            
        # 2. Income vs Expense Bar Chart
        ax2 = fig.add_subplot(122)
        income_total = self.df[self.df['type'] == 'Income']['amount'].sum()
        expense_total = self.df[self.df['type'] == 'Expense']['amount'].sum()
        
        bars = ax2.bar(['Income', 'Expense'], [income_total, expense_total], color=['#4CAF50', '#F44336'])
        ax2.set_title("Income vs Expense")
        ax2.set_ylabel("Amount ($)")
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, yval + (max(income_total, expense_total) * 0.01), round(yval, 2), ha='center', va='bottom')
            
        fig.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
