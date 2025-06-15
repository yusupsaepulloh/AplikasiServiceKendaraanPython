import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class FormPelanggan:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Data Pelanggan", font=("Arial", 14)).pack()

        self.tree = ttk.Treeview(self.frame, columns=("id", "nama", "telepon", "alamat"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack()
        self.tree.bind("<Double-1>", self.on_item_select)

        self.entry_nama = tk.Entry(self.frame)
        self.entry_telepon = tk.Entry(self.frame)
        self.entry_alamat = tk.Entry(self.frame)
        for label, entry in zip(["Nama", "Telepon", "Alamat"], [self.entry_nama, self.entry_telepon, self.entry_alamat]):
            tk.Label(self.frame, text=label).pack()
            entry.pack(fill='x')

        tk.Button(self.frame, text="Tambah", command=self.tambah).pack(fill='x')
        tk.Button(self.frame, text="Hapus", command=self.hapus).pack(fill='x')
        tk.Button(self.frame, text="Kembali", command=self.kembali).pack(fill='x')

        self.load_data()

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM pelanggan")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

    def tambah(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO pelanggan(nama, telepon, alamat) VALUES (%s, %s, %s)",
                       (self.entry_nama.get(), self.entry_telepon.get(), self.entry_alamat.get()))
        db.commit()
        self.load_data()

    def hapus(self):
        selected = self.tree.selection()
        if not selected: return
        item = self.tree.item(selected)
        id_pelanggan = item['values'][0]
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan=%s", (id_pelanggan,))
        db.commit()
        self.load_data()

    def on_item_select(self, event):
        item = self.tree.item(self.tree.selection())
        self.entry_nama.delete(0, tk.END)
        self.entry_telepon.delete(0, tk.END)
        self.entry_alamat.delete(0, tk.END)
        self.entry_nama.insert(0, item['values'][1])
        self.entry_telepon.insert(0, item['values'][2])
        self.entry_alamat.insert(0, item['values'][3])

    def kembali(self):
        self.frame.destroy()
        from menu_admin import MenuAdmin
        MenuAdmin(self.root)