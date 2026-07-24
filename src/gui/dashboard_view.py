import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils.exporter import export_to_csv
from src.gui.charts_view import ChartsView

class DashboardView:
    def __init__(self, parent, controller):
        self.controller = controller
        
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        
        self.user = self.controller.current_user
        
        self._build_ui()
        self._load_transactions()
        
    def _build_ui(self):
        # Top Bar
        top_bar = tk.Frame(self.frame, bg="#e0e0e0")
        top_bar.pack(fill="x", pady=5)
        
        tk.Label(top_bar, text=f"Welcome, {self.user['username']}!", font=("Helvetica", 14), bg="#e0e0e0").pack(side="left", padx=10, pady=5)
        tk.Button(top_bar, text="Logout", command=self.controller.logout).pack(side="right", padx=10, pady=5)
        
        # Main Layout: Left (Form + Search), Right (Table + Charts)
        content_frame = tk.Frame(self.frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(content_frame, width=300)
        left_frame.pack(side="left", fill="y", padx=5)
        
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # --- LEFT FRAME ---
        # Add Transaction Form
        form_label = tk.Label(left_frame, text="Add Transaction", font=("Helvetica", 14, "bold"))
        form_label.pack(pady=10)
        
        tk.Label(left_frame, text="Type:").pack(anchor="w")
        self.type_var = tk.StringVar(value="Expense")
        type_dropdown = ttk.Combobox(left_frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly")
        type_dropdown.pack(fill="x", pady=5)
        type_dropdown.bind("<<ComboboxSelected>>", self._update_categories)
        
        tk.Label(left_frame, text="Category:").pack(anchor="w")
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(left_frame, textvariable=self.category_var, state="readonly")
        self.category_dropdown.pack(fill="x", pady=5)
        self._update_categories()
        
        tk.Label(left_frame, text="Amount:").pack(anchor="w")
        self.amount_entry = tk.Entry(left_frame)
        self.amount_entry.pack(fill="x", pady=5)
        
        tk.Label(left_frame, text="Date (YYYY-MM-DD):").pack(anchor="w")
        self.date_entry = tk.Entry(left_frame)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.pack(fill="x", pady=5)
        
        tk.Label(left_frame, text="Description:").pack(anchor="w")
        self.desc_entry = tk.Entry(left_frame)
        self.desc_entry.pack(fill="x", pady=5)
        
        tk.Button(left_frame, text="Add Transaction", bg="#4CAF50", fg="black", command=self._add_transaction).pack(fill="x", pady=15)
        
        # Separator
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Search
        tk.Label(left_frame, text="Search Transactions", font=("Helvetica", 12, "bold")).pack(pady=5)
        self.search_entry = tk.Entry(left_frame)
        self.search_entry.pack(fill="x", pady=5)
        tk.Button(left_frame, text="Search", command=self._search_transactions).pack(fill="x", pady=5)
        tk.Button(left_frame, text="Clear Search", command=self._load_transactions).pack(fill="x")
        
        # Export
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10)
        tk.Button(left_frame, text="Export to CSV", command=self._export_csv).pack(fill="x")
        
        # Charts button
        tk.Button(left_frame, text="View Charts", command=self._open_charts).pack(fill="x", pady=10)
        
        # --- RIGHT FRAME ---
        # Treeview for Transactions
        columns = ("date", "type", "category", "amount", "description")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        
        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("description", text="Description")
        
        self.tree.column("date", width=100)
        self.tree.column("type", width=80)
        self.tree.column("category", width=120)
        self.tree.column("amount", width=100)
        self.tree.column("description", width=200)
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def _update_categories(self, event=None):
        t_type = self.type_var.get()
        if t_type == "Income":
            cats = ["Salary", "Freelance", "Investment", "Gift", "Other"]
        else:
            cats = ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Shopping", "Health", "Other"]
        
        self.category_dropdown['values'] = cats
        if cats:
            self.category_dropdown.current(0)

    def _add_transaction(self):
        t_type = self.type_var.get()
        category = self.category_var.get()
        amount_str = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()
        desc = self.desc_entry.get().strip()
        
        if not amount_str or not date:
            messagebox.showerror("Error", "Amount and Date are required.")
            return
            
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return
            
        success, msg = self.controller.db.add_transaction(self.user['id'], t_type, category, amount, date, desc)
        if success:
            messagebox.showinfo("Success", msg)
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self._load_transactions()
        else:
            messagebox.showerror("Error", msg)

    def _load_transactions(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        transactions = self.controller.db.get_transactions(self.user['id'])
        for t in transactions:
            self.tree.insert("", "end", values=(t['date'], t['type'], t['category'], f"${t['amount']:.2f}", t['description']))

    def _search_transactions(self):
        query = self.search_entry.get().strip()
        if not query:
            self._load_transactions()
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        transactions = self.controller.db.search_transactions(self.user['id'], query)
        for t in transactions:
            self.tree.insert("", "end", values=(t['date'], t['type'], t['category'], f"${t['amount']:.2f}", t['description']))

    def _export_csv(self):
        transactions = self.controller.db.get_transactions(self.user['id'])
        if not transactions:
            messagebox.showinfo("Export", "No transactions to export.")
            return
            
        success, msg = export_to_csv(transactions)
        if success:
            messagebox.showinfo("Export Success", msg)
        else:
            messagebox.showerror("Export Failed", msg)

    def _open_charts(self):
        transactions = self.controller.db.get_transactions(self.user['id'])
        if not transactions:
            messagebox.showinfo("Charts", "No data to display.")
            return
        ChartsView(self.frame, transactions)
