# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter

from Timekeeping_Window import TimekeepingWindow
from Login_Window import LoginWindow

class MainWindow:
    def __init__(self, root):
        icon_folder = "Picture"
        
        self.root = root
        self.root.title('Hệ thống chấm công')
        self.root.geometry("800x600")  # Đặt kích thước cửa sổ
        self.root.minsize(850,500)
        
        # Load ảnh nền và icon ---------------------------------------------------------------------------------
        # Thêm hình nền
        self.background_image = Image.open(f"{icon_folder}/download.jpg")
        self.background_label = tk.Label(root)
        self.background_label.place(relwidth=1, relheight=1)
        
        # Load ảnh cho nút Check in
        check_in_image = Image.open(f"{icon_folder}/check-in.png")
        check_in_image = check_in_image.resize((50, 50), Image.LANCZOS)
        self.check_in_photo = ImageTk.PhotoImage(check_in_image)
        
        # Load ảnh cho nút Check out
        check_out_image = Image.open(f"{icon_folder}/check-out.png")
        check_out_image = check_out_image.resize((50, 50), Image.LANCZOS)
        self.check_out_photo = ImageTk.PhotoImage(check_out_image)
        
        # Load ảnh cho login
        login_image = Image.open(f"{icon_folder}/login.png")
        login_image = login_image.resize((50,50), Image.LANCZOS)
        self.login_photo = ImageTk.PhotoImage(login_image)
        
        # Tạo kiểu cho button (style)
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Helvetica", 12), padding=5, relief="flat",
                                    background="#4CAF50", foreground="black")

        # Nút Check in với ảnh
        self.check_in_button = ttk.Button(root, text="Check-in", image=self.check_in_photo,
                                           compound="left", style="TButton", command=self.check_in)

        # Nút Check out với ảnh 
        self.check_out_button = ttk.Button(root, text="Check-out", image=self.check_out_photo,
                                            compound="left", style="TButton", command=self.check_out)

        # Nút login
        self.login_button = ttk.Button(root, text="Login", image=self.login_photo,
                                       compound="left", style="TButton", command=self.login)
        
        # Gắn sự kiện thay đổi kích thước cửa sổ
        self.root.bind("<Configure>", self.on_window_resize)

        # Tắt tự động điều chỉnh kích thước của widget
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def on_window_resize(self, event):
        # Khi kích thước cửa sổ thay đổi, cập nhật kích thước và phủ mờ lại background
        width = self.root.winfo_width()
        height = self.root.winfo_height()
    
        # Thay đổi kích thước hình nền
        resized_image = self.background_image.resize((width, height), Image.LANCZOS)
        blurred_background_image = resized_image.filter(ImageFilter.BLUR)
        blurred_background_photo = ImageTk.PhotoImage(blurred_background_image)
    
        # Cập nhật background phủ mờ
        self.background_label.config(image=blurred_background_photo)
        self.background_label.image = blurred_background_photo
    
        # Căn giữa theo chiều dọc
        vertical_padding = (height - 4 * self.check_out_button.winfo_reqheight()) // 5
    
        # Tính toán tọa độ cho nút Check-in
        self.check_in_button.place(relx=0.5, rely=0.35, anchor="center")
    
        # Tính toán tọa độ cho nút Check-out
        self.check_out_button.place(relx=0.5, rely=0.55, anchor="center")
    
        # Tính toán tọa độ cho nút Thêm nhân viên
        self.login_button.place(relx=0.5, rely=0.75, anchor="center")
            
        
    def check_in(self):
        self.root.withdraw()
        check_in_window = tk.Toplevel(self.root)
        title = 'Check-in'
        print(title)
        TimekeepingWindow(check_in_window, self.show_menu, title)
        
    def check_out(self):
        self.root.withdraw()
        check_out_window = tk.Toplevel(self.root)
        title = 'Check-out'
        print(title)
        TimekeepingWindow(check_out_window, self.show_menu, title)
                         
    def login(self):
        self.root.withdraw()
        login_window = tk.Toplevel(self.root)
        title = 'Login'
        print(title)
        LoginWindow(login_window, self.show_menu, title)
        
    def show_menu(self):
        self.root.deiconify()  # Hiển thị lại cửa sổ menu
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()