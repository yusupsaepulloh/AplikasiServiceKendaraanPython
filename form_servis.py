import tkinter as tk
from tkinter import ttk
from database import connect_db

class FormServis:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)
        tk.Label(self.frame, text="Riwayat Servis", font=("Arial", 14)).pack()

        self.tree = ttk.Treeview(self.frame, columns=("id", "kendaraan", "tanggal", "keluhan", "tindakan", "biaya"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack()
        self.load_data()

        tk.Button(self.frame, text="Kembali", command=self.kembali).pack(fill='x')

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_servis, id_kendaraan, tanggal_servis, keluhan, tindakan, biaya FROM servis")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

    def kembali(self):
        self.frame.destroy()
        from login_frame import LoginFrame
        LoginFrame(self.root)