from datetime import datetime
import socket
import threading

import cv2
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class AddPersonWindow:
    def __init__(self, root, show_menu_callback, token, admin_menu_window):
        self.show_menu_callback = show_menu_callback
        self.token = token
        self.admin_menu_window = admin_menu_window
        
        self.camera_window = root
        self.camera_window.title("Camera")
        self.camera_window.minsize(800, 550)
        root.protocol("WM_DELETE_WINDOW", self.disable_event)
        
        self.submitted = False  # Track submission state
        # self.server_address = "127.0.0.1"  # Replace with actual server address
        # self.server_port = 5000  # Replace with actual server port
        self.server_address = '10.11.10.140'
        self.server_port = 5000
        self.upload_url = f"http://{self.server_address}:{self.server_port}/add_person"
        
        
        self.setup_ui()
        self.cap = None  # Delay initialization of webcam
        
        # Start the video capture thread
        self.video_thread = threading.Thread(target=self.capture_video)
        self.video_thread.daemon = True
        self.video_thread.start()

    def setup_ui(self):
        # Fixed size for the camera frame
        self.camera_frame_width = 640
        self.camera_frame_height = 480

        # Create a colored background image for the waiting screen
        self.waiting_bg = Image.new("RGB", (self.camera_frame_width, self.camera_frame_height), "gray")
        self.waiting_bg_tk = ImageTk.PhotoImage(self.waiting_bg)

        # Camera frame in the Toplevel window
        self.video_frame = tk.Label(self.camera_window, text="Camera Frame", bg="black", fg="white", image=self.waiting_bg_tk)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create frame for information
        self.info_frame = ttk.Frame(self.camera_window)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # Employee ID
        self.label_id = ttk.Label(self.info_frame, text="Employee ID:")
        self.label_id.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_id = ttk.Entry(self.info_frame, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        # Name
        self.label_name = ttk.Label(self.info_frame, text="Name:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_name = ttk.Entry(self.info_frame, width=30)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        # Birthday
        self.label_birthday = ttk.Label(self.info_frame, text="Birthday:")
        self.label_birthday.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.cal = DateEntry(self.info_frame, width=27, date_pattern='dd/mm/yyyy')
        self.cal.grid(row=2, column=1, padx=5, pady=5)

        # Gender
        self.label_gender = ttk.Label(self.info_frame, text="Gender:")
        self.label_gender.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(self.info_frame, textvariable=self.gender_var, values=["Nam", "Nữ"], width=27, state='readonly')
        self.gender_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Address
        self.label_address = ttk.Label(self.info_frame, text="Address:")
        self.label_address.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_address = ttk.Entry(self.info_frame, width=30)
        self.entry_address.grid(row=4, column=1, padx=5, pady=5)

        # Phone
        self.label_phone = ttk.Label(self.info_frame, text="Phone:")
        self.label_phone.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.entry_phone = ttk.Entry(self.info_frame, width=30)
        self.entry_phone.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        self.submit_button = ttk.Button(self.info_frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Exit button
        self.exit_button = ttk.Button(self.info_frame, text="Exit", command=self.show_admin_menu)
        self.exit_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
        print(f'token:{self.token}')

    def capture_video(self):
        self.video_capture = cv2.VideoCapture(0)
        action = "check"
        
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            # Connect to the server
            client_socket.connect((self.server_address, self.server_port))
            print("Connected to server.")
            
            while True:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    continue
                
                _, img_encoded = cv2.imencode('.jpg', frame)
                
                if self.submitted:
                    locations, status = self.upload_new_image(img_encoded, action)
                    
                    if status == "turn left":
                        action = "turn right"
                    elif status == "turn right" and action == "turn right":
                        action = "straight"
                    elif status == "straight" and action == "straight":
                        action = action = "Done"
                    elif status == "Done":
                        print("Embedding creation completed")
                        self.submitted = False
                        action = "check"
                        # break
                        messagebox.showinfo("Success","Đã thêm nhân viên thành công!")
                    elif status == "Exists":
                        messagebox.showwarning("Attention", "Nhân viên đã tồn tại")  
                    elif status == "Error":
                        messagebox.showerror("Error", "Có lỗi xảy ra")
                    if action == "check" and status != "Exists":
                        (height, width) = frame.shape[:2]
                        (text_width, text_height), baseline = cv2.getTextSize("turn left", cv2.FONT_HERSHEY_DUPLEX, 1.0, 1)
                        start_x = (width - text_width) // 2
                        start_y = text_height + baseline + 10
                        cv2.putText(frame, action, (start_x, start_y), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 255), 1)
                    elif action == "check" and status != "Exists":
                        (height, width) = frame.shape[:2]
                        (text_width, text_height), baseline = cv2.getTextSize(action, cv2.FONT_HERSHEY_DUPLEX, 1.0, 1)
                        start_x = (width - text_width) // 2
                        start_y = text_height + baseline + 10
                        cv2.putText(frame, action, (start_x, start_y), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 255), 1)
                                        
                    if status is not None and status != "Done" and locations != []:
                        (top, right, bottom, left) = locations
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.putText(frame, status, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.video_frame.configure(image=frame)
                self.video_frame.image = frame
                self.camera_window.update()
                
            self.cap.release()
            cv2.destroyAllWindows()   
        
        except Exception as e:
            print("Cannot connect to server:", e)
        finally:
            client_socket.close()
            print("Connection closed.")

    def submit(self):
        self.employee_id = self.entry_id.get()
        self.name = self.entry_name.get()
        self.birthday = self.cal.get_date().strftime("%Y-%m-%d")
        self.gender = self.gender_var.get()
        self.address = self.entry_address.get()
        self.phone = self.entry_phone.get()
        self.submitted = True

    def upload_new_image(self, image_file, action):
        try:
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            files = {'image': ('image.jpg', image_file.tobytes(), 'image/jpeg')}
            data = {
                'ID': self.employee_id,
                'name': self.name,
                'birthday': self.birthday,
                'gender': self.gender,
                'address': self.address,
                'phone': self.phone,
                'action': action
            }
            
            response = requests.post(self.upload_url, headers=headers, files=files, data=data)
    
            if response.status_code == 401:
                self.submitted = False
                return [], "Exists"
            elif response.status_code != 200:
                data = response.json()
                error = data.get('error', '')
                print(f'Error: {error}')
                print("Request failed:", response.status_code)
                return [], "Error"
            
    
            data = response.json()
            locations = data.get('locations', [])
            status = data.get('status', '')
    
            return locations, status
        except Exception as e:
            print("An error occurred:", e)
            return [], "Error"
        
    def disable_event(self):
        pass
    
    def show_menu(self):
        self.camera_window.destroy()  # Xóa cửa sổ chấm công
        self.show_menu_callback()  # Hiển thị lại cửa sổ menu
        
    def show_admin_menu(self):
        self.camera_window.destroy()
        self.admin_menu_window.deiconify()
        
class DeletePersonWindow:
    def __init__(self, root, show_menu_callback, token, admin_menu_window):
       self.show_menu_callback = show_menu_callback
       self.token = token
       self.admin_menu_window = admin_menu_window
       
       self.root = root
       self.root.title("Xóa nhân viên")
       self.root.minsize(800, 550)
       # root.protocol("WM_DELETE_WINDOW", self.disable_event)
       
       # self.server_address = "127.0.0.1"  # Replace with actual server address
       # self.server_port = 5000  # Replace with actual server port
       
       self.server_address = '10.11.10.140'
       self.server_port = 5000
       
       self.setup_ui() 
       
    def setup_ui(self):
       # Create a frame to hold all widgets
       self.frame = tk.Frame(self.root)
       self.frame.pack(expand=True)  # Center the frame within the main window

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
       self.btn_delete_person.grid(row=6, column=1, pady=10, sticky="n")
       
       self.btn_back = tk.Button(self.frame, text="Back to menu", command=self.show_admin_menu)
       self.btn_back.grid(row=7, column=1, pady=10, sticky="n")
        
    def update_info(self):
        self.employee_id = self.entry_employee_id.get()
        data = {'employeeID': self.employee_id}
        search_url = f"http://{self.server_address}:{self.server_port}/search_person"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(search_url, headers=headers, data=data)
        info = response.json()  # Parse response as JSON
        if response.status_code == 200:
            self.label_name_value.config(text=info.get("name", "N/A"))
            # Convert date format
            dob_str = info.get("birthday", "")
            dob_dt = datetime.strptime(dob_str, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_dob = dob_dt.strftime('%d/%m/%Y')
            self.label_dob_value.config(text=formatted_dob)
            self.label_gender_value.config(text=info.get("gender", ""))
            self.label_address_value.config(text=info.get("address", "N/A"))
            self.label_phone_value.config(text=info.get("phone", "N/A"))
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin nhân viên")

    def delete_person(self):
        url = f"http://{self.server_address}:{self.server_port}/delete_person"
        data = {'employeeID': self.employee_id}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        action = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên không?")
        if action:
            response = requests.delete(url, headers=headers, data=data)
            if response.status_code == 200:
                messagebox.showinfo("Notification", "Đã xóa nhân viên")
                self.show_menu()    
            else:
                messagebox.showerror("Error", "Có lỗi khi xóa nhân viên")
        
    def show_admin_menu(self):
        self.root.destroy()
        self.admin_menu_window.deiconify()
       

