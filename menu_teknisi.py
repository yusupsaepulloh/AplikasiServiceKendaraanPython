import tkinter as tk
from dashboard_gui import DashboardApp


def run(username):
    root = tk.Tk()
    root.title(f"Teknisi - {username}")
    app = DashboardApp(root, role="teknisi")
    root.mainloop()