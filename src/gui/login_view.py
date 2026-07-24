import tkinter as tk
from tkinter import messagebox

class LoginView:
    def __init__(self, parent, controller):
        self.controller = controller
        
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        
        self._build_ui()
        
    def _build_ui(self):
        # Title
        tk.Label(self.frame, text="Personal Finance Tracker", font=("Helvetica", 24, "bold")).pack(pady=40)
        
        # Form frame
        form_frame = tk.Frame(self.frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 14))
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Password:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 14))
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Buttons
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Login", font=("Helvetica", 12), width=10, command=self.handle_login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Sign Up", font=("Helvetica", 12), width=10, command=self.handle_signup).pack(side="left", padx=10)
        
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
            
        success, result = self.controller.db.authenticate_user(username, password)
        if success:
            self.controller.login_success(result)
        else:
            messagebox.showerror("Login Failed", result)
            
    def handle_signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
            
        success, msg = self.controller.db.register_user(username, password)
        if success:
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
        else:
            messagebox.showerror("Registration Failed", msg)
