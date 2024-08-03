# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:03:33 2024

@author: batha
"""

import socket
import time
import uuid
import csv
import json

import requests
import cv2

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import threading

class TimekeepingWindow:
    process_current_frame = True
    face_names = ""
    face_locations = [] 
    
    def __init__(self, root, show_menu_callback, title):
        
        self.show_menu_callback = show_menu_callback
        self.title = title
        
        
        
        # Cửa sổ giao diện:
        self.root = root
        self.root.title(title)
        self.root.minsize(1350,800)
        # Vô hiệu hóa chức năng của nút đóng cửa sổ
        root.protocol("WM_DELETE_WINDOW", self.disable_event)
        
        self.company_check()
        
        # Tạo và cấu hình video feed
        self.cap = cv2.VideoCapture(0)
        self.video_frame = tk.Label(root)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)

        # Tạo frame cho thông tin 
        self.info_frame = ttk.Frame(root)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10)
        
        self.employeeID_label = ttk.Label(self.info_frame, text="Xin chào:", foreground="blue")
        self.employeeID_label.grid(row=1, column=0, pady=10)
        self.employeeID_label.config(font=("Arial", 20))  # Thiết lập kích thước chữ là 16
        
        self.status_label = ttk.Label(self.info_frame, text="Trạng thái:")
        self.status_label.grid(row=3, column=0, pady=10)
        self.status_label.config(font=("Arial", 18))  # Thiết lập kích thước chữ là 16
        
        self.time_label = ttk.Label(self.info_frame, text="Thời gian:")
        self.time_label.grid(row=4, column=0, pady=10)
        self.time_label.config(font=("Arial", 18)) 
        
        self.back_button = ttk.Button(self.info_frame, text="Quay lại", command=self.show_menu)
        self.back_button.grid(row=5, column=0, pady=10)
        
        self.run_recognition()
        
    def company_check(self):
        try:
            # Mở file JSON và đọc dữ liệu
            with open('login data.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            self.company = data.get('company','')
        except:
            messagebox.showerror("Error", "Bạn cần đăng nhập hệ thống trước")
            self.root.destroy()  # Xóa cửa sổ chấm công
            self.show_menu_callback()   # Hiển thị lại cửa sổ menu
        
    def show_menu(self):
        requests.post(self.upload_url, files=None, data='Exit')
        self.root.destroy()  # Xóa cửa sổ chấm công
        self.show_menu_callback()  # Hiển thị lại cửa sổ menu
        
    def disable_event(self):
        pass
        
    def upload_image(self,image_file, action, company, upload_url):
        try:
    
           # Gửi frame lên server
            files = {'image': ('image.jpg', image_file.tostring(), 'image/jpeg')}  # Chuyển đổi mảng NumPy thành byte
            
            data = {
                'type': action,
                'collection': company
            }
            
            # Gửi request POST đến server
            response = requests.post(upload_url, files=files, data=data)
    
            # Kiểm tra nếu phản hồi không hợp lệ
            if response.status_code != 200:
                print("Lỗi khi gửi request:", response.status_code)
                return [], []
        
            # Lấy dữ liệu JSON từ phản hồi
            data = response.json()
            if data is None:
                print("Phản hồi không hợp lệ")
                return [], []
        
            face_names = data.get('face_names', [])
            locations = data.get('locations', [])
            times = data.get('time', [])
        
            return face_names, locations, times
    
        except Exception as e:
            print("Có lỗi xảy ra:", e)
        
    def run_recognition(self):
        
        self.current_employee = None
        self.employeeID_label['text'] = "Mã nhân viên: "
        self.status_label['text'] = "Trạng thái: "

        # Tạo một đối tượng socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.upload_url = 'http://10.11.10.140:5000/timekeeping'
        server_address = '10.11.10.140'
        server_port = 5000
        
        self.skip_frame = 0
            
        try:
            # Kết nối đến server
            client_socket.connect((server_address, server_port))
            print("Đã kết nối đến server.")
            
            # Khởi tạo webcam
            video_capture = cv2.VideoCapture(0)
            
            while True:
                current_employee = []
                # start_time = time.time()
                
                # Chụp frame từ video
                ret, frame = video_capture.read()
                
                if not ret or frame is None or frame.size == 0:
                    print("Không thể chụp frame từ video. Dừng lại.")
                    break
                
                # Write the original frame to the video file
                # out.write(frame)
            
                # Chuyển đổi frame thành định dạng hình ảnh JPEG
                _, img_encoded = cv2.imencode('.jpg', frame)
                
                big_frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)
                frame = big_frame
                            
                # Chuyển đổi hình ảnh để hiển thị trên widget Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.video_frame.configure(image=frame)
                self.video_frame.image = frame
                
                self.root.update()
                
                if self.skip_frame == 0:
                   self.skip_frame = 20
                   # Start a new thread to handle the image upload and recognition
                   threading.Thread(target=self.handle_recognition, args=(img_encoded,)).start()
               
                self.skip_frame -= 1
               
                self.root.update()
                                                
            self.cap.release()
            cv2.destroyAllWindows()    
            
        except Exception as e:
            print(f"Lỗi kết nối đến server: {e}")

        finally:
            client_socket.close()
            print("đã đóng kết nối socket")
            
    def handle_recognition(self, img_encoded):
        # Gửi request và nhận về kết quả
        face_names, locations, time_checked = self.upload_image(img_encoded, self.title, self.company, self.upload_url)
        if face_names and 'Unknown' not in face_names:# and 'fake' not in face_names:
            self.employeeID_label['text'] = f"Xin chào: {face_names}"
            self.status_label['text'] = f"Trạng thái: Đã {self.title}"
            self.time_label['text'] = f"Thời gian: {time_checked}"
            
        # elif 'fake' in face_names:
        #     self.employeeID_label['text'] = "Xin chào:"
        #     self.status_label['text'] = "Trạng thái:"
        #     self.time_label['text'] = "Thời gian:"
        print(face_names)
        
        