import json
import requests

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from Admin_Menu import AdminMenu


class LoginWindow:
    def __init__(self, root, show_menu_callback, title):
        self.show_menu_callback = show_menu_callback
        self.root = root 
        self.root.title(title)
        self.root.minsize(400, 400)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        try:
            img_path = "Picture/login.png"
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            photo = None
            print(f"Image loading error: {e}")

        if photo:
            self.img_label = tk.Label(self.main_frame, image=photo, bg="white")
            self.img_label.image = photo
            self.img_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        
        self.login_frame = tk.Frame(self.main_frame, bg="white")
        self.login_frame.grid(row=0, column=1, pady=20, padx=20)

        self.title_label = tk.Label(self.login_frame, text="User Login", font=("Arial", 20), bg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.username_label = tk.Label(self.login_frame, text="Email Id", font=("Arial", 10), bg="white")
        self.username_label.grid(row=1, column=0, sticky="w")

        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 10), width=30)
        self.username_entry.grid(row=2, column=0, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password", font=("Arial", 10), bg="white")
        self.password_label.grid(row=3, column=0, sticky="w")

        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 10), width=30)
        self.password_entry.grid(row=4, column=0, pady=5)

        try:
            self.show_photo = ImageTk.PhotoImage(Image.open("Picture/show.png").resize((20, 20), Image.LANCZOS))
            self.hide_photo = ImageTk.PhotoImage(Image.open("Picture/hide.png").resize((20, 20), Image.LANCZOS))
        except Exception as e:
            self.show_photo = self.hide_photo = None
            print(f"Icon loading error: {e}")

        if self.show_photo and self.hide_photo:
            self.show_password = False
            self.show_button = tk.Button(self.login_frame, image=self.hide_photo, command=self.toggle_password, bg="white", bd=0)
            self.show_button.grid(row=4, column=1, padx=(0, 10))

        self.login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 10), bg="green", fg="white", command=self.login)
        self.login_button.grid(row=5, column=0, pady=10)

        self.signup_label = tk.Label(self.login_frame, text="Sign Up", font=("Arial", 8), bg="white", fg="blue", cursor="hand2")
        self.signup_label.grid(row=6, column=0, pady=(0, 10))
        self.signup_label.bind("<Button-1>", self.signup)

        self.forgot_label = tk.Label(self.login_frame, text="Forgot Username / Password?", font=("Arial", 8), bg="white", fg="blue", cursor="hand2")
        self.forgot_label.grid(row=7, column=0, pady=(0, 10))
        self.forgot_label.bind("<Button-1>", self.forgot_password)

        self.exit_label = tk.Label(self.login_frame, text="Exit", font=("Arial", 10), bg="white", fg="blue", cursor="hand2")
        self.exit_label.grid(row=8, column=0, pady=(0, 10))
        self.exit_label.bind("<Button-1>", self.show_menu)
        
    def show_menu(self, event):
        self.root.destroy()
        self.show_menu_callback()

    def toggle_password(self):
        if self.show_password:
            self.password_entry.config(show="*")
            self.show_password = False
            self.show_button.config(image=self.hide_photo)
        else:
            self.password_entry.config(show="")
            self.show_password = True
            self.show_button.config(image=self.show_photo)        
        
    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        
        login_url = "http://10.11.10.140:5000/login"
        
        self.login_data = {
            'username': self.username,
            'password': self.password
        }
        
        self.login_response = requests.post(login_url, json=self.login_data)
        
        if self.login_response.status_code == 401:
            messagebox.showerror("Error", "Incorrect username or password")
        elif self.login_response.status_code != 200:
            messagebox.showerror("Error", f"Request failed: {self.login_response.status_code}")
        else:
            data = self.login_response.json()
            self.token = data.get('token','')
            
            # Ghi dữ liệu vào file JSON
            with open('login data.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            self.open_admin_menu()

    def signup(self, event):
        self.root.withdraw()  # Hide the current window
        signup_window = tk.Toplevel(self.root)
        SignUpWindow(signup_window, self.show_menu_callback, self.root)
        
    def forgot_password(self, event):
        messagebox.showinfo("Forgot Password", "Password recovery functionality will be implemented here.")

    def open_admin_menu(self):
        self.root.withdraw()
        admin_menu_window = tk.Toplevel(self.root)
        AdminMenu(admin_menu_window, self.show_menu_callback, self.token)


class SignUpWindow:
    def __init__(self, root, show_menu_callback, login_window):
        self.show_menu_callback = show_menu_callback
        self.login_window = login_window
        self.root = root
        self.root.title("Sign Up")
        self.root.minsize(400, 400)

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        try:
            img_path = "Picture/login.png"
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            photo = None
            print(f"Image loading error: {e}")
        
        if photo:
            self.img_label = tk.Label(self.main_frame, image=photo, bg="white")
            self.img_label.image = photo
            self.img_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)

        self.signup_frame = tk.Frame(self.main_frame, bg="white")
        self.signup_frame.grid(row=0, column=1, pady=20, padx=20)

        self.title_label = tk.Label(self.signup_frame, text="User Register", font=("Arial", 20), bg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.register_username_label = tk.Label(self.signup_frame, text="Email Id(*)", font=("Arial", 10), bg="white")
        self.register_username_label.grid(row=1, column=0, sticky="w")

        self.register_username_entry = tk.Entry(self.signup_frame, font=("Arial", 10), width=30)
        self.register_username_entry.grid(row=2, column=0, pady=5)

        self.register_password_label = tk.Label(self.signup_frame, text="Password(*)", font=("Arial", 10), bg="white")
        self.register_password_label.grid(row=3, column=0, sticky="w")

        self.register_password_entry = tk.Entry(self.signup_frame, show="*", font=("Arial", 10), width=30)
        self.register_password_entry.grid(row=4, column=0, pady=5)
        
        try:
            self.show_photo = ImageTk.PhotoImage(Image.open("Picture/show.png").resize((20, 20), Image.LANCZOS))
            self.hide_photo = ImageTk.PhotoImage(Image.open("Picture/hide.png").resize((20, 20), Image.LANCZOS))
        except Exception as e:
            self.show_photo = self.hide_photo = None
            print(f"Icon loading error: {e}")

        if self.show_photo and self.hide_photo:
            self.show_password = False
            self.show_button = tk.Button(self.signup_frame, image=self.hide_photo, command=self.toggle_password, bg="white", bd=0)
            self.show_button.grid(row=4, column=1, padx=(0, 10))

        self.register_confirm_password_label = tk.Label(self.signup_frame, text="Confirm Password(*)", font=("Arial", 10), bg="white")
        self.register_confirm_password_label.grid(row=5, column=0, sticky="w")

        self.register_confirm_password_entry = tk.Entry(self.signup_frame, show="*", font=("Arial", 10), width=30)
        self.register_confirm_password_entry.grid(row=6, column=0, pady=5)

        if self.show_photo and self.hide_photo:
            self.show_confirm_password = False
            self.show_confirm_button = tk.Button(self.signup_frame, image=self.hide_photo, command=self.toggle_confirm_password, bg="white", bd=0)
            self.show_confirm_button.grid(row=6, column=1, padx=(0, 10))

        self.hint_label = tk.Label(self.signup_frame, text="Hint", font=("Arial", 10), bg="white")
        self.hint_label.grid(row=7, column=0, sticky="w")

        self.hint_entry = tk.Entry(self.signup_frame, font=("Arial", 10), width=30)
        self.hint_entry.grid(row=8, column=0, pady=5)
        
        self.company_label = tk.Label(self.signup_frame, text="Company(*)", font=("Arial", 10), bg="white")
        self.company_label.grid(row=9, column=0, sticky="w")

        self.company_entry = tk.Entry(self.signup_frame, font=("Arial", 10), width=30)
        self.company_entry.grid(row=10, column=0, pady=5)
        
        self.signup_button = tk.Button(self.signup_frame, text="Sign up", font=("Arial", 10), bg="green", fg="white", command=self.signup)
        self.signup_button.grid(row=11, column=0, pady=10)
        
        self.forgot_label = tk.Label(self.signup_frame, text="Login", font=("Arial", 8), bg="white", fg="blue", cursor="hand2")
        self.forgot_label.grid(row=12, column=0, pady=(0, 10))
        self.forgot_label.bind("<Button-1>", self.show_login)
        
        self.exit_label = tk.Label(self.signup_frame, text="Exit", font=("Arial", 10), bg="white", fg="blue", cursor="hand2")
        self.exit_label.grid(row=13, column=0, pady=(0, 10))
        self.exit_label.bind("<Button-1>", self.show_menu)
        
    def show_menu(self, event):
        self.root.destroy()
        self.show_menu_callback()

    def show_login(self):
        self.root.destroy()
        self.login_window.deiconify()

    def toggle_password(self):
        if self.show_password:
            self.register_password_entry.config(show="*")
            self.show_password = False
            self.show_button.config(image=self.hide_photo)
        else:
            self.register_password_entry.config(show="")
            self.show_password = True
            self.show_button.config(image=self.show_photo)
            
    def toggle_confirm_password(self):
        if self.show_confirm_password:
            self.register_confirm_password_entry.config(show="*")
            self.show_confirm_password = False
            self.show_confirm_button.config(image=self.hide_photo)
        else:
            self.register_confirm_password_entry.config(show="")
            self.show_confirm_password = True
            self.show_confirm_button.config(image=self.show_photo)

    def signup(self):
        email = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.register_confirm_password_entry.get()
        hint = self.hint_entry.get()
        company = self.company_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Validate password length and whitespace
        elif len(password) < 8 or " " in password:
            messagebox.showerror("Error", "Password must be at least 8 characters long and cannot contain spaces")
            return
        else:
            signup_url = "http://10.11.10.140:5000/register"
            
            self.signup_data = {
                'username': email,
                'password': password,
                'hint': hint,
                'company': company
            }
            
            self.signup_response = requests.post(signup_url, json=self.signup_data)
            
            if self.signup_response.status_code == 409:
                messagebox.showerror("Error", "User already exists")
            elif self.signup_response.status_code == 201:
                messagebox.showinfo("Success", "User registered successfully")
                self.show_login()
            else:
                messagebox.showerror("Error", "Sign up error")
