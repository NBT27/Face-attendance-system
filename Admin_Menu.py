# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 23:10:22 2024

@author: batha
"""

import os
import requests

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageFilter
from Edit_Person import AddPersonWindow, DeletePersonWindow
from Export_data import ExportData

class AdminMenu:
    def __init__(self, root, show_menu_callback, token):
        icon_folder = "Picture"
        self.show_menu_callback = show_menu_callback
        self.token = token
        # print(self.token)

        self.root = root
        self.root.title('Admin')
        self.root.geometry("800x600")  # Đặt kích thước cửa sổ
        self.root.minsize(850, 500)
        
        # self.server_address = "127.0.0.1"  # Replace with actual server address
        # self.server_port = 5000  # Replace with actual server port
        self.server_address = '10.11.10.140'
        self.server_port = 5000
        
        # Load ảnh nền và icon ---------------------------------------------------------------------------------
        # Thêm hình nền
        self.background_image = Image.open(f"{icon_folder}/download.jpg")
        self.background_label = tk.Label(root)
        self.background_label.place(relwidth=1, relheight=1)
        
        # Load ảnh cho nút 
        add_person_image = Image.open(f"{icon_folder}/add-person.png")
        add_person_image = add_person_image.resize((50, 50), Image.LANCZOS)
        self.add_person_photo = ImageTk.PhotoImage(add_person_image)
        
        # Load ảnh cho nút 
        delete_person_image = Image.open(f"{icon_folder}/delete-person.png")
        delete_person_image = delete_person_image.resize((50, 50), Image.LANCZOS)
        self.delete_person_photo = ImageTk.PhotoImage(delete_person_image)
        
        # Load ảnh cho 
        file_export_image = Image.open(f"{icon_folder}/export.png")
        file_export_image = file_export_image.resize((50, 50), Image.LANCZOS)
        self.file_export_photo = ImageTk.PhotoImage(file_export_image)
        
        # Load ảnh cho nút 
        delete_account_image = Image.open(f"{icon_folder}/delete-person.png")
        delete_account_image = delete_account_image.resize((50, 50), Image.LANCZOS)
        self.delete_account_photo = ImageTk.PhotoImage(delete_account_image)
        
        exit_image = Image.open(f"{icon_folder}/emergency-exit_4008990.png")
        exit_image = exit_image.resize((50, 50), Image.LANCZOS)
        self.exit_photo = ImageTk.PhotoImage(exit_image)
        
        # Tạo kiểu cho button (style)
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Helvetica", 12), padding=5, relief="flat",
                                    background="#4CAF50", foreground="black")

        # Create buttons with equal size
        button_width = 250
        button_height = 80

        # Nút thêm nhân viên
        self.add_person_button = ttk.Button(root, text="Thêm nhân viên", image=self.add_person_photo,
                                            compound="left", style="TButton", command=self.add_person)
        self.add_person_button.place(relx=0.25, rely=0.35, anchor="center", width=button_width, height=button_height)
        
        # # Nút thêm nhân viên từ file
        # self.add_many_person_button = ttk.Button(root, text="Thêm nhân viên từ file", image=self.add_person_photo,
        #                                          compound="left", style="TButton", command=self.show_menu)
        # self.add_many_person_button.place(relx=0.75, rely=0.35, anchor="center", width=button_width, height=button_height)
        
        # Nút xóa nhân viên
        self.delete_person_button = ttk.Button(root, text="Xóa nhân viên", image=self.delete_person_photo,
                                                 compound="left", style="TButton", command=self.delete_person)
        self.delete_person_button.place(relx=0.25, rely=0.65, anchor="center", width=button_width, height=button_height)

        
        # Nút xuất file
        self.file_export_button = ttk.Button(root, text="Xuất dữ liệu", image=self.file_export_photo,
                                             compound="left", style="TButton", command=self.export_data)
        self.file_export_button.place(relx=0.25, rely=0.65, anchor="center", width=button_width, height=button_height)
        
        # Nút xóa tài khoản
        self.delete_account_button = ttk.Button(root, text="Xóa tài khoản", image=self.delete_account_photo, compound="left", style="TButton", command=self.confirm_delete_account)
        self.delete_account_button.place(relx=0.75, rely=0.65, anchor="center", width=button_width, height=button_height)
        
        # Nút thoát
        self.exit_button = ttk.Button(root, text="Exit", image=self.exit_photo, compound="left", style="TButton", command=self.show_menu)
        self.exit_button.place(relx=0.75, rely=0.65, anchor="center", width=button_width, height=button_height)
        
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
        # vertical_padding = (height - 4 * self.add_many_person_button.winfo_reqheight()) // 5
    
        # Tính toán tọa độ cho nút 
        self.add_person_button.place(relx=0.3, rely=0.25, anchor="center")
        # self.add_many_person_button.place(relx=0.7, rely=0.25, anchor="center")
        self.delete_person_button.place(relx=0.7, rely=0.25, anchor="center")
        self.file_export_button.place(relx=0.3, rely=0.5, anchor="center")
        self.delete_account_button.place(relx=0.7, rely=0.5, anchor="center")
        self.exit_button.place(relx=0.5, rely=0.75, anchor="center")

        
    def show_menu(self):
        self.root.destroy()
        self.show_menu_callback()
        
        
    def add_person(self):
        self.root.withdraw()
        add_person_window = tk.Toplevel(self.root)
        AddPersonWindow(add_person_window, self.show_menu_callback, self.token, self.root)
        
    def delete_person(self):
        self.root.withdraw()
        delete_person_window = tk.Toplevel(self.root)
        DeletePersonWindow(delete_person_window, self.show_menu_callback, self.token, self.root)
        
    def export_data(self):
        # self.root.withdraw()
        self.export_window = tk.Toplevel(self.root)
        ExportData(self.export_window, self.token, self.root)
        
    def confirm_delete_account(self):
        upload_url = f"http://{self.server_address}:{self.server_port}/delete_account"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        action = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa tài khoản không?")
        if action:
            response = requests.delete(upload_url, headers=headers)
            if response.status_code == 200:
                try:
                    os.remove("login data.json")
                except:
                    None
                messagebox.showinfo("Notification", "Đã xóa tài khoản")
                self.show_menu()    
            else:
                messagebox.showerror("Error", "Có lỗi khi xóa tài khoản")
        
def show_menu():
    print("show menu")
        
if __name__ == "__main__":
    root = tk.Tk()
    token = ""
    app = AdminMenu(root, show_menu, token)
    root.mainloop()