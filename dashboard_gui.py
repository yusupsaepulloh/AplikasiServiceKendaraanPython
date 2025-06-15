import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import mysql.connector
from tkcalendar import DateEntry
import customtkinter as ctk

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="service_kendaraan"
    )
class DashboardApp:
    def __init__(self, root, role="admin", username=""):
        self.root = root
        self.root.title("Aplikasi Service Kendaraan")
        window_width = 1100
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.role = role
        self.username = username

        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#503f2c", width=200)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text=f"Halo, {self.role.capitalize()}", fg="white", bg="#503f2c", font=("Arial", 12, "bold"), pady=20).pack()

        tk.Button(self.sidebar, text="Dashboard", bg="#5e4934", fg="white", relief="flat", command=self.show_dashboard).pack(fill="x", padx=10, pady=5)

        if self.role == "admin":
            tk.Button(self.sidebar, text="Kelola Pelanggan", bg="#5e4934", fg="white", relief="flat", command=self.show_pelanggan).pack(fill="x", padx=10, pady=5)
            tk.Button(self.sidebar, text="Kelola Kendaraan", bg="#5e4934", fg="white", relief="flat", command=self.show_kendaraan).pack(fill="x", padx=10, pady=5)

        if self.role == "teknisi":
            tk.Button(self.sidebar, text="Data Kendaraan", bg="#5e4934", fg="white", relief="flat", command=self.show_kendaraan).pack(fill="x", padx=10, pady=5)

        tk.Button(self.sidebar, text="Servis", bg="#5e4934", fg="white", relief="flat", command=self.show_servis).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#c61c1c",
            hover_color="#a91414",
            text_color="white",
            height=28,
            width=25,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            command=self.logout
        ).pack(side="bottom", fill="x", padx=10, pady=10)


        # Header
        self.header = tk.Frame(self.root, height=50, bg="#db7634")
        self.header.pack(side="top", fill="x")
        today = datetime.date.today().strftime("%A, %d-%m-%Y")
        tk.Label(self.header, text=today, bg="#db7634", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=10, pady=10)

        # Konten utama
        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(fill="both", expand=True)

        self.show_dashboard()

    def logout(self):
        self.root.destroy()
        import login_frame
        root = tk.Tk()
        app = login_frame.LoginFrame(root)
        root.mainloop()
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    def show_dashboard(self):
        self.clear_content()
        tk.Label(self.content, text="Selamat Datang di Aplikasi Service Kendaraan ", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

    def show_pelanggan(self):
        self.clear_content()
        title = tk.Label(self.content, text="Manajemen Pelanggan", font=("Arial", 16, "bold"), bg="white")
        title.pack(pady=10)

        form_frame = tk.Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nama:").grid(row=0, column=0, sticky="w")
        nama_entry = tk.Entry(form_frame)
        nama_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Telepon:").grid(row=1, column=0, sticky="w")
        telp_entry = tk.Entry(form_frame)
        telp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Alamat:").grid(row=2, column=0, sticky="w")
        alamat_entry = tk.Entry(form_frame)
        alamat_entry.grid(row=2, column=1, padx=5, pady=5)

        def tambah():
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO pelanggan(nama, telepon, alamat) VALUES (%s, %s, %s)",
                           (nama_entry.get(), telp_entry.get(), alamat_entry.get()))
            db.commit()
            db.close()
            self.show_pelanggan()

        def hapus():
            selected = tree.selection()
            if not selected:
                return
            item = tree.item(selected)
            id_pelanggan = item['values'][0]
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (id_pelanggan,))
            db.commit()
            db.close()
            self.show_pelanggan()

        def update():
            selected = tree.selection()
            if not selected:
                return
            item = tree.item(selected)
            id_pelanggan = item['values'][0]

            db = connect_db()
            cursor = db.cursor()
            cursor.execute("UPDATE pelanggan SET nama=%s, telepon=%s, alamat=%s WHERE id=%s",
                           (nama_entry.get(), telp_entry.get(), alamat_entry.get(), id_pelanggan))
            db.commit()
            db.close()
            self.show_pelanggan()

        button_frame = tk.Frame(self.content, bg="white")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Tambah", bg="#27ae60", fg="white", width=10, command=tambah).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update", bg="#2980b9", fg="white", width=10, command=update).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Hapus", bg="#c0392b", fg="white", width=10, command=hapus).grid(row=0, column=2, padx=5)

        # Tabel pelanggan
        tabel_frame = tk.Frame(self.content)
        tabel_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        columns = ("ID", "Nama", "Telepon", "Alamat")

        # Scrollbars (opsional tapi disarankan jika data banyak)
        scroll_x = ttk.Scrollbar(tabel_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(tabel_frame, orient="vertical")

        tree = ttk.Treeview(
            tabel_frame,
            columns=columns,
            show="headings",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(command=tree.xview)
        scroll_y.config(command=tree.yview)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")

        # Heading dan ukuran kolom
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=200, stretch=True)  # stretch=True agar melebar

        tree.pack(fill=tk.BOTH, expand=True)

        # Isi data dari database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM pelanggan")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        db.close()

        def on_tree_select(event):
            selected = tree.selection()
            if not selected:
                return
            item = tree.item(selected)
            nama_entry.delete(0, tk.END)
            nama_entry.insert(0, item['values'][1])
            telp_entry.delete(0, tk.END)
            telp_entry.insert(0, item['values'][2])
            alamat_entry.delete(0, tk.END)
            alamat_entry.insert(0, item['values'][3])

        tree.bind("<<TreeviewSelect>>", on_tree_select)
        tree.pack()

    def show_kendaraan(self):
        self.clear_content()
        self.selected_id_kendaraan = None

        tk.Label(self.content, text="Data Kendaraan", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Form input
        form_frame = tk.Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="ID Pelanggan:").grid(row=0, column=0, sticky="w")
        id_pelanggan_entry = tk.Entry(form_frame)
        id_pelanggan_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Plat Nomor:").grid(row=1, column=0, sticky="w")
        plat_nomor_entry = tk.Entry(form_frame)
        plat_nomor_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Merk:").grid(row=2, column=0, sticky="w")
        merk_entry = tk.Entry(form_frame)
        merk_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Model:").grid(row=3, column=0, sticky="w")
        model_entry = tk.Entry(form_frame)
        model_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tahun:").grid(row=4, column=0, sticky="w")
        tahun_entry = tk.Entry(form_frame)
        tahun_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="ID Kategori:").grid(row=5, column=0, sticky="w")
        kategori_entry = tk.Entry(form_frame)
        kategori_entry.grid(row=5, column=1, padx=5, pady=5)

        # Pencarian
        search_frame = tk.Frame(self.content, bg="white")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Cari (Plat/Merk/Model):", bg="white").grid(row=0, column=0)
        search_entry = tk.Entry(search_frame)
        search_entry.grid(row=0, column=1, padx=5)

        # Tabel
        tabel_frame = tk.Frame(self.content)
        tabel_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        columns = ("ID Kendaraan", "ID Pelanggan", "Plat Nomor", "Merk", "Model", "Tahun", "Kategori")

        tree_scroll_y = ttk.Scrollbar(tabel_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")

        tree_scroll_x = ttk.Scrollbar(tabel_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        tree = ttk.Treeview(
            tabel_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fungsi refresh table
        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("""
                SELECT k.id_kendaraan, k.id_pelanggan, k.plat_nomor, k.merk, k.model, k.tahun, kk.nama_kategori
                FROM kendaraan k
                JOIN kategori_kendaraan kk ON k.id_kategori = kk.id_kategori
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            db.close()

        def reset_form():
            id_pelanggan_entry.delete(0, tk.END)
            plat_nomor_entry.delete(0, tk.END)
            merk_entry.delete(0, tk.END)
            model_entry.delete(0, tk.END)
            tahun_entry.delete(0, tk.END)
            kategori_entry.delete(0, tk.END)
            self.selected_id_kendaraan = None

        def simpan_kendaraan():
            if not all([id_pelanggan_entry.get(), plat_nomor_entry.get(), merk_entry.get(), model_entry.get(),
                        tahun_entry.get(), kategori_entry.get()]):
                messagebox.showwarning("Peringatan", "Semua field harus diisi.")
                return
            db = connect_db()
            cursor = db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO kendaraan (id_pelanggan, plat_nomor, merk, model, tahun, id_kategori)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    id_pelanggan_entry.get(),
                    plat_nomor_entry.get(),
                    merk_entry.get(),
                    model_entry.get(),
                    tahun_entry.get(),
                    kategori_entry.get()
                ))
                db.commit()
                messagebox.showinfo("Sukses", "Data kendaraan berhasil disimpan.")
                refresh_tree()
                reset_form()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                db.close()

        def update_kendaraan():
            if not self.selected_id_kendaraan:
                messagebox.showwarning("Peringatan", "Pilih data kendaraan yang ingin diperbarui.")
                return
            db = connect_db()
            cursor = db.cursor()
            try:
                cursor.execute("""
                    UPDATE kendaraan SET id_pelanggan=%s, plat_nomor=%s, merk=%s, model=%s, tahun=%s, id_kategori=%s
                    WHERE id_kendaraan=%s
                """, (
                    id_pelanggan_entry.get(),
                    plat_nomor_entry.get(),
                    merk_entry.get(),
                    model_entry.get(),
                    tahun_entry.get(),
                    kategori_entry.get(),
                    self.selected_id_kendaraan
                ))
                db.commit()
                messagebox.showinfo("Sukses", "Data kendaraan diperbarui.")
                refresh_tree()
                reset_form()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                db.close()

        def hapus_kendaraan():
            if not self.selected_id_kendaraan:
                messagebox.showwarning("Peringatan", "Pilih data kendaraan yang ingin dihapus.")
                return
            if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
                db = connect_db()
                cursor = db.cursor()
                try:
                    cursor.execute("DELETE FROM kendaraan WHERE id_kendaraan=%s", (self.selected_id_kendaraan,))
                    db.commit()
                    messagebox.showinfo("Sukses", "Data berhasil dihapus.")
                    refresh_tree()
                    reset_form()
                    self.selected_id_kendaraan = None
                except Exception as e:
                    if "1451" in str(e):
                        messagebox.showerror("Gagal",
                                             "Data tidak bisa dihapus karena digunakan di tabel lain (servis).")
                    else:
                        messagebox.showerror("Error", str(e))
                finally:
                    db.close()

        # Tombol CRUD
        tk.Button(form_frame, text="Simpan", bg="#27ae60", fg="white", width=10, command=simpan_kendaraan).grid(row=6,column=0,padx=5,pady=10)
        tk.Button(form_frame, text="Update", bg="#2980b9", fg="white", width=10, command=update_kendaraan).grid(row=6, column=1,padx=5,pady=10)
        tk.Button(form_frame, text="Delete", bg="#c0392b", fg="white", width=10, command=hapus_kendaraan).grid(row=6,column=2,padx=5,pady=10)



        def search_kendaraan():
            keyword = search_entry.get()
            for item in tree.get_children():
                tree.delete(item)
            db = connect_db()
            cursor = db.cursor()
            like = f"%{keyword}%"
            cursor.execute("""
                SELECT k.id_kendaraan, k.id_pelanggan, k.plat_nomor, k.merk, k.model, k.tahun, kk.nama_kategori
                FROM kendaraan k
                JOIN kategori_kendaraan kk ON k.id_kategori = kk.id_kategori
                WHERE k.plat_nomor LIKE %s OR k.merk LIKE %s OR k.model LIKE %s
            """, (like, like, like))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            db.close()

        def reset_search():
            search_entry.delete(0, tk.END)
            refresh_tree()

        tk.Button(search_frame, text="Cari", command=search_kendaraan).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Reset", command=reset_search).grid(row=0, column=3, padx=5)

        # Event untuk isi form dari tabel
        def on_tree_select(event):
            selected = tree.selection()
            if selected:
                data = tree.item(selected[0])["values"]
                self.selected_id_kendaraan = data[0]
                id_pelanggan_entry.delete(0, tk.END)
                id_pelanggan_entry.insert(0, data[1])
                plat_nomor_entry.delete(0, tk.END)
                plat_nomor_entry.insert(0, data[2])
                merk_entry.delete(0, tk.END)
                merk_entry.insert(0, data[3])
                model_entry.delete(0, tk.END)
                model_entry.insert(0, data[4])
                tahun_entry.delete(0, tk.END)
                tahun_entry.insert(0, data[5])

        tree.bind("<<TreeviewSelect>>", on_tree_select)

        refresh_tree()
        tree.pack()

    def show_servis(self):
        self.clear_content()
        self.selected_id_servis = None  # Simpan ID servis yang dipilih

        tk.Label(self.content, text="Riwayat Servis", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        form_frame = tk.Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        # Form input
        tk.Label(form_frame, text="ID Kendaraan:").grid(row=0, column=0, sticky="w")
        id_kendaraan_entry = tk.Entry(form_frame)
        id_kendaraan_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tanggal:").grid(row=1, column=0, sticky="w")
        tanggal_entry = DateEntry(form_frame, date_pattern="yyyy-mm-dd", width=18)
        tanggal_entry.set_date(datetime.date.today())
        tanggal_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Keluhan:").grid(row=2, column=0, sticky="w")
        keluhan_entry = tk.Entry(form_frame)
        keluhan_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tindakan:").grid(row=3, column=0, sticky="w")
        tindakan_entry = tk.Entry(form_frame)
        tindakan_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Biaya:").grid(row=4, column=0, sticky="w")
        biaya_entry = tk.Entry(form_frame)
        biaya_entry.grid(row=4, column=1, padx=5, pady=5)

        def refresh_tree():
            for i in tree.get_children():
                tree.delete(i)
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM servis")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            db.close()

        def reset_form():
            id_kendaraan_entry.delete(0, tk.END)
            tanggal_entry.set_date(datetime.date.today())
            keluhan_entry.delete(0, tk.END)
            tindakan_entry.delete(0, tk.END)
            biaya_entry.delete(0, tk.END)
            self.selected_id_servis = None

        def simpan_servis():
            db = connect_db()
            cursor = db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO servis(id_kendaraan, tanggal_servis, keluhan, tindakan, biaya)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    id_kendaraan_entry.get(),
                    tanggal_entry.get(),
                    keluhan_entry.get(),
                    tindakan_entry.get(),
                    biaya_entry.get()
                ))
                db.commit()
                messagebox.showinfo("Sukses", "Data servis berhasil disimpan.")
                refresh_tree()
                reset_form()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                db.close()

        def update_servis():
            if not self.selected_id_servis:
                messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui.")
                return
            db = connect_db()
            cursor = db.cursor()
            try:
                cursor.execute("""
                    UPDATE servis SET id_kendaraan=%s, tanggal_servis=%s, keluhan=%s, tindakan=%s, biaya=%s
                    WHERE id_servis=%s
                """, (
                    id_kendaraan_entry.get(),
                    tanggal_entry.get(),
                    keluhan_entry.get(),
                    tindakan_entry.get(),
                    biaya_entry.get(),
                    self.selected_id_servis
                ))
                db.commit()
                messagebox.showinfo("Sukses", "Data berhasil diperbarui.")
                refresh_tree()
                reset_form()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                db.close()

        def hapus_servis():
            if not self.selected_id_servis:
                messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus.")
                return
            confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
            if confirm:
                db = connect_db()
                cursor = db.cursor()
                try:
                    cursor.execute("DELETE FROM servis WHERE id_servis=%s", (self.selected_id_servis,))
                    db.commit()
                    messagebox.showinfo("Sukses", "Data berhasil dihapus.")
                    refresh_tree()
                    reset_form()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    db.close()

        # Tombol
        tk.Button(form_frame, text="Simpan", bg="#27ae60", fg="white", width=10, command=simpan_servis).grid(row=5, column=0,padx=5,pady=10)
        tk.Button(form_frame, text="Update", bg="#2980b9", fg="white",width=10, command=update_servis).grid(row=5, column=1,padx=5,pady=10)
        tk.Button(form_frame, text="Hapus", bg="#c0392b", fg="white", width=10, command=hapus_servis).grid(row=5, column=2, padx=5,pady=10)

        # Frame pencarian di bawah tabel
        search_frame = tk.Frame(self.content, bg="white")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Cari ID Kendaraan:", bg="white").grid(row=0, column=0, padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.grid(row=0, column=1, padx=5)

        def search_servis():
            id_kendaraan = search_entry.get()
            for i in tree.get_children():
                tree.delete(i)
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("""
                        SELECT * FROM servis WHERE id_kendaraan LIKE %s
                    """, ('%' + id_kendaraan + '%',))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            db.close()

        def reset_search():
            search_entry.delete(0, tk.END)
            refresh_tree()

        tk.Button(search_frame, text="Search", command=search_servis).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Reset", command=reset_search).grid(row=0, column=3, padx=5)

        # Tabel
        tabel_frame = tk.Frame(self.content)
        tabel_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "ID Kendaraan", "Tanggal", "Deskripsi", "Tindakan", "Biaya")
        tree = ttk.Treeview(tabel_frame, columns=columns, show="headings")

        tree_scroll_y = ttk.Scrollbar(tabel_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")

        tree_scroll_x = ttk.Scrollbar(tabel_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        tree = ttk.Treeview(
            tabel_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")  # Kamu bisa ubah width sesuai kebutuhan

        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        def on_tree_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                data = item["values"]
                self.selected_id_servis = data[0]
                id_kendaraan_entry.delete(0, tk.END)
                id_kendaraan_entry.insert(0, data[1])
                tanggal_entry.set_date(data[2])
                keluhan_entry.delete(0, tk.END)
                keluhan_entry.insert(0, data[3])
                tindakan_entry.delete(0, tk.END)
                tindakan_entry.insert(0, data[4])
                biaya_entry.delete(0, tk.END)
                biaya_entry.insert(0, data[5])

        tree.bind("<<TreeviewSelect>>", on_tree_select)

        refresh_tree()
        tree.pack()


# Fungsi untuk digunakan dari login_frame

def start_dashboard(role, username):
    root = tk.Tk()
    app = DashboardApp(root, role=role, username=username)
    root.mainloop()
