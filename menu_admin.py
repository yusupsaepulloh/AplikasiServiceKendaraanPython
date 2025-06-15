import tkinter as tk
from dashboard_gui import DashboardApp

def run(username):
    root = tk.Tk()
    root.title(f"Admin - {username}")
    app = DashboardApp(root, role="admin")
    root.mainloop()