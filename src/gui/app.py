import tkinter as tk
from tkinter import messagebox
from src.database.db_manager import DatabaseManager
from src.gui.login_view import LoginView
from src.gui.dashboard_view import DashboardView

class FinanceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("900x650")
        
        self.db = DatabaseManager()
        self.current_user = None
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.show_login_view()

    def show_login_view(self):
        self._clear_container()
        LoginView(self.container, self)

    def show_dashboard_view(self):
        self._clear_container()
        DashboardView(self.container, self)
        
    def login_success(self, user):
        self.current_user = user
        self.show_dashboard_view()
        
    def logout(self):
        self.current_user = None
        self.show_login_view()
        
    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
