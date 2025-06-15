import tkinter as tk
from login_frame import LoginFrame

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Aplikasi Service Kendaraan")
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    LoginFrame(root)
    root.mainloop()

