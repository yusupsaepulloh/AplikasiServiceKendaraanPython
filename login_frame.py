import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import menu_admin
import menu_teknisi

class LoginFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Aplikasi Service Kendaraan")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        window_width = 720
        window_height = 480
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        # Frame putih tengah
        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color="white",
            width=440,
            height=360
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Judul
        ctk.CTkLabel(self.main_frame, text="LOGIN", text_color="#bc4f1e",
                     font=ctk.CTkFont("Segoe UI", 20, "bold")).pack(pady=15)

        # Username
        ctk.CTkLabel(self.main_frame, text="Username", text_color="black",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=40)
        self.username_entry = ctk.CTkEntry(self.main_frame, width=280)
        self.username_entry.pack(padx=40, pady=(0, 15))

        # Password
        ctk.CTkLabel(self.main_frame, text="Password", text_color="black",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=40)
        self.password_entry = ctk.CTkEntry(self.main_frame, show="*", width=280)
        self.password_entry.pack(padx=40, pady=(0, 10))

        # Remember me
        self.remember_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self.main_frame, text="Remember me", variable=self.remember_var, checkbox_width=18, checkbox_height=18, font=ctk.CTkFont(size=13)).pack(anchor="w", padx=40)

        # Tombol Login bulat
        ctk.CTkButton(self.main_frame, text="Login", text_color="white", command=self.login,
                      width=200, corner_radius=20, fg_color="#db6434", hover_color="#b95729").pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="service_kendaraan"
            )
            cursor = db.cursor()
            cursor.execute("SELECT role FROM akun_login WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            db.close()

            if result:
                role = result[0]
                self.root.destroy()
                if role == "admin":
                    menu_admin.run(username)
                elif role == "teknisi":
                    menu_teknisi.run(username)
                else:
                    messagebox.showerror("Error", "Role tidak dikenal!")
            else:
                messagebox.showerror("Gagal", "Username atau password salah!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal koneksi database:\n{e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginFrame(root)
    root.mainloop()
