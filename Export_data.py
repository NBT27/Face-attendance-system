import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkcalendar import DateEntry
from datetime import datetime
import requests
from tkinter import messagebox, filedialog
import csv

class ExportData:
    def __init__(self, root, token, admin_menu_window):
        self.token = token
        self.admin_menu_window = admin_menu_window
        self.date = ""
        self.month = ""
        self.year = ""
        self.start_date = ""
        self.end_date = ""
        self.selected_month = ""
        
        self.root = root
        self.root.title("Export File")
        self.root.minsize(400, 250)
        self.root.maxsize(500, 300)
                        
        # self.server_address = "127.0.0.1"  # Replace with actual server address
        # self.server_port = 5000  # Replace with actual server port
        
        self.server_address = '10.11.10.140'
        self.server_port = 5000
        self.url = f"http://{self.server_address}:{self.server_port}/data_export"

        # Configure the grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        # Combobox for export options
        self.option_label = ttk.Label(root, text="Chọn kiểu xuất file:")
        self.option_label.grid(row=0, column=0, padx=22, pady=10, sticky="w")

        self.options = ["Theo ngày", "Theo tháng", "Theo khoảng thời gian"]
        self.selected_option = tk.StringVar(value="Theo ngày")
        self.combobox = ttk.Combobox(root, textvariable=self.selected_option, values=self.options, width=25, state='readonly')
        self.combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.combobox.bind("<<ComboboxSelected>>", self.update_ui)  

        # Frame for the second line
        self.frame = ttk.Frame(root)
        self.frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Initialize second line
        self.update_ui()
        
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Helvetica", 10), padding=0, relief="flat",
                                    background="#4CAF50", foreground="black")

        # File save location
        self.filepath_label = ttk.Label(root, text="Chọn vị trí lưu file:")
        self.filepath_label.grid(row=2, column=0, padx=22, pady=10, sticky="w")

        self.filepath_var = tk.StringVar()
        self.filepath_entry = ttk.Entry(root, textvariable=self.filepath_var, width=28, state='readonly')
        self.filepath_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Add submit button
        self.submit_button = ttk.Button(root, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=3, column=0, columnspan=3, pady=10, sticky="n")
        # self.submit_button.place(relx=0.5, rely=0.9, anchor="center", width=80, height=25)

    def update_ui(self, event=None):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        selected = self.selected_option.get()

        if selected == "Theo ngày":
            self.date_label = ttk.Label(self.frame, text="Chọn ngày:")
            self.date_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.date_entry = DateEntry(self.frame, date_pattern='dd/mm/yyyy', width=25)
            self.date_entry.grid(row=0, column=1, padx=27, pady=10, sticky="w")
        
        elif selected == "Theo tháng":
            # Get current month and year
            now = datetime.now()
            current_month = now.strftime('%m')
            current_year = str(now.year)
            
            self.month_label = ttk.Label(self.frame, text="Chọn tháng:")
            self.month_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            

            # Combobox for month
            self.month_entry = ttk.Combobox(self.frame, values=[f"{m}" for m in range(1, 13)], width=9, state='readonly')
            self.month_entry.grid(row=0, column=1, padx=0, pady=10, sticky="w")
            self.month_entry.set(current_month)

            # Combobox for year
            self.year_entry = ttk.Combobox(self.frame, values=[str(year) for year in range(2000, 2031)], width=9, state='readonly')
            self.year_entry.grid(row=0, column=2, padx=10, pady=10, sticky="w")
            self.year_entry.set(current_year)
        
        elif selected == "Theo khoảng thời gian":
            self.start_label = ttk.Label(self.frame, text="Bắt đầu:")
            self.start_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.start_date = DateEntry(self.frame, date_pattern='dd/mm/yyyy', width=25)
            self.start_date.grid(row=0, column=1, padx=67, pady=10, sticky="w")

            self.end_label = ttk.Label(self.frame, text="Kết thúc:")
            self.end_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            self.end_date = DateEntry(self.frame, date_pattern='dd/mm/yyyy', width=25)
            self.end_date.grid(row=1, column=1, padx=67, pady=10, sticky="w")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

    def browse_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.csv"), ("All files", "*.*")])
        if filepath:
            self.filepath_var.set(filepath)
            
    def date_converter(self, date):
        day_temp, month_temp, year_temp = date.split('/')
        date_converted = f'{year_temp}-{month_temp}-{day_temp}'
        return date_converted

    def submit_action(self):
        selected = self.selected_option.get()
        filepath = self.filepath_var.get()
        
        if not filepath:
            messagebox.showwarning("Warning", "Please select a file save location.")
            return

        if selected == "Theo ngày":
            self.export_option = "date"
            date = self.date_entry.get()
            self.date = self.date_converter(date)
            
            print(f"Exporting data for date: {self.date} to {filepath}")
        elif selected == "Theo tháng":
            self.export_option = "month"
            self.month = self.month_entry.get()
            self.year = self.year_entry.get()
            self.selected_month = f'{self.year}-{self.month}'
            print(f"Exporting data for: {self.selected_month} to {filepath}")
        elif selected == "Theo khoảng thời gian":
            self.export_option = "period"
            start_date = self.start_date.get()
            self.start_date = self.date_converter(start_date)
            end_date = self.end_date.get()
            self.end_date = self.date_converter(end_date)
            print(f"Exporting data from {self.start_date} to {self.end_date} to {filepath}")

        self.export_request(filepath)
            
    def export_request(self, filepath):
        data = {
            'option': self.export_option,
            'date': self.date,
            'month': self.selected_month,
            'year': self.year,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        response = requests.get(self.url, data=data, headers={'Authorization': f'Bearer {self.token}'})
        if response.status_code != 200:
            messagebox.showerror("Error", "Có lỗi xảy ra")
        else:
            timekeeping_data = response.json()
            if timekeeping_data:
                # Specify the columns you want to write to the CSV file
                columns = ['date', 'employeeID', 'status', 'time']
                
                # Writing data to CSV file
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=columns)
                    writer.writeheader()
                    for row in timekeeping_data:
                        filtered_row = {key: row[key] for key in columns}
                        writer.writerow(filtered_row)
                messagebox.showinfo("Success", "Đã lưu dữ liệu")
                self.show_admin_menu()
            else:
                messagebox.showwarning("Attention", "Không có dữ liệu")
                
    def show_admin_menu(self):
        self.root.destroy()
        self.admin_menu_window.deiconify()
        
if __name__ == "__main__":
    root = tk.Tk()
    token = ""
    admin = ""
    app = ExportData(root, token, admin)
    root.mainloop()
