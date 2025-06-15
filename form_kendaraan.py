import tkinter as tk
from tkinter import ttk
from database import connect_db

class FormKendaraan:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)
        tk.Label(self.frame, text="Data Kendaraan", font=("Arial", 14)).pack()

        self.tree = ttk.Treeview(self.frame, columns=("id", "plat", "merk", "model", "tahun"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack()
        self.load_data()

        tk.Button(self.frame, text="Kembali", command=self.kembali).pack(fill='x')

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_kendaraan, plat_nomor, merk, model, tahun FROM kendaraan")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

    def kembali(self):
        self.frame.destroy()
        from menu_admin import MenuAdmin
        MenuAdmin(self.root)
