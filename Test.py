import tkinter as tk

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Information")
        self.setup_ui()

    def setup_ui(self):
        # Create a frame to hold all widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)  # Center the frame within the main window

        # self.frame.columnconfigure(0, weight=1)
        # self.frame.columnconfigure(1, weight=1)
        # self.frame.columnconfigure(2, weight=1)
        # self.frame.rowconfigure(0, weight=1)
        # self.frame.rowconfigure(1, weight=1)
        # self.frame.rowconfigure(2, weight=1)
        # self.frame.rowconfigure(3, weight=1)
        # self.frame.rowconfigure(4, weight=1)
        # self.frame.rowconfigure(5, weight=1)
        # self.frame.rowconfigure(6, weight=1)
        # self.frame.rowconfigure(7, weight=1)

        # Nhập mã nhân viên
        tk.Label(self.frame, text="Mã nhân viên:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_employee_id = tk.Entry(self.frame, width=30)
        self.entry_employee_id.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Nút để lấy thông tin nhân viên
        self.btn_get_info = tk.Button(self.frame, text="Lấy thông tin", command=self.update_info)
        self.btn_get_info.grid(row=0, column=2, padx=10, pady=10)
        
        # Hiển thị thông tin nhân viên
        tk.Label(self.frame, text="Họ tên:").grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_name_value = tk.Label(self.frame, text="")
        self.label_name_value.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.frame, text="Ngày sinh:").grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_dob_value = tk.Label(self.frame, text="")
        self.label_dob_value.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.frame, text="Giới tính:").grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_gender_value = tk.Label(self.frame, text="")
        self.label_gender_value.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.frame, text="Địa chỉ:").grid(row=4, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_address_value = tk.Label(self.frame, text="")
        self.label_address_value.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.frame, text="Điện thoại:").grid(row=5, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_phone_value = tk.Label(self.frame, text="")
        self.label_phone_value.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        
        self.btn_delete_person = tk.Button(self.frame, text="Xóa nhân viên", command=self.delete_person)
        self.btn_delete_person.grid(row=1, column=2, columnspan=3, pady=10, sticky=tk.NSEW)
        
        self.btn_back = tk.Button(self.frame, text="Back to menu", command=self.show_admin_menu)
        self.btn_back.grid(row=2, column=2, columnspan=3, pady=10, sticky="n")

    def update_info(self):
        # Function to update employee info
        pass

    def delete_person(self):
        # Function to delete employee
        pass

    def show_admin_menu(self):
        # Function to show admin menu
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # Set a default window size
    app = EmployeeApp(root)
    root.mainloop()
