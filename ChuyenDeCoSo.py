import tkinter as tk
from tkinter import messagebox
import requests
from PIL import ImageTk, Image
from bs4 import BeautifulSoup, SoupStrainer
import tkinter.ttk as ttk

def test_xss():
    target_url = url_entry.get()
    if not target_url:
        messagebox.showwarning("Lỗi", "Vui lòng nhập URL đích!")
        return
    xss_payloads = []
    with open(r'C:\\Users\\ASUS\\Attack-XSS.txt', 'r') as filehandle:
        for line in filehandle:
            xss_payload = line.strip()
            xss_payloads.append(xss_payload)
    
    response = requests.get(target_url)
    results = []
    for payload in xss_payloads:
        data = {}
        for field in BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer('input')):
            if field.has_attr('name'):
                if field['name'].lower() == 'submit':
                    data[field['name']] = 'submit'
                else:
                    data[field['name']] = payload

        response = requests.post(target_url, data=data)
        if payload in response.text:
            results.append((payload, True))
        else:
            results.append((payload, False))
    
    display_results(results)

def test_sql_injection():
    target_url = url_entry.get()
    if not target_url:
        messagebox.showwarning("Lỗi", "Vui lòng nhập URL đích!")
        return
    sql_payloads = []
    with open(r'C:\\Users\\ASUS\\sql-attack-vector.txt', 'r') as filehandle:
        for line in filehandle:
            sql_payload = line.strip()
            sql_payloads.append(sql_payload)
    
    results = []
    for payload in sql_payloads:
        response = requests.post(target_url + payload)
        if 'mysql' in response.text.lower():
            results.append((payload, True))
        elif 'native client' in response.text.lower():
            results.append((payload, True))
        elif 'syntax error' in response.text.lower():
            results.append((payload, True))
        elif 'ORA' in response.text.lower():
            results.append((payload, True))
        else:
            results.append((payload, False))
    
    display_results(results)
def csrf_scan():
    target_url = url_entry.get()
    if not target_url:
        messagebox.showwarning("Lỗi", "Vui lòng nhập URL đích!")
        return

    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    input_fields = soup.find_all('input')

    missing_csrf_fields = []
    for field in input_fields:
        if 'csrf' not in field.get('name', '').lower():
            missing_csrf_fields.append(field.get('name', ''))

    if missing_csrf_fields:
        missing_fields_str = ', '.join(missing_csrf_fields)
        messagebox.showinfo("CSRF Scan", f"Các trường thiếu CSRF token: {missing_fields_str}")
    else:
        messagebox.showinfo("CSRF Scan", "Không tìm thấy trường thiếu CSRF token")

def display_results(results):
    result_window = tk.Toplevel(window)
    result_window.title("Kết quả")
    result_window.geometry("600x400")
    result_window.configure(bg='#FFFFFF')

    table = ttk.Treeview(result_window)
    table['columns'] = ('payload', 'result')
    table.column('#0', width=0, stretch='no')
    table.column('payload', anchor='center', width=300)
    table.column('result', anchor='center', width=300)
    table.heading('#0', text='', anchor='center')
    table.heading('payload', text='Payload', anchor='center')
    table.heading('result', text='Kết quả', anchor='center')
    
    for result in results:
        payload, success = result
        if success:
            success_text = 'Thành công'
            table.insert('', 'end', values=(payload, success_text), tags='success')
        else:
            success_text = 'Thất bại'
            table.insert('', 'end', values=(payload, success_text), tags='failure')
    
    table.tag_configure('success', background='#C8E6C9')
    table.tag_configure('failure', background='#FFCDD2')
    
    table.pack(fill='both', expand=True)

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Trình kiểm tra lỗ hổng Web")
window.geometry("700x350")
window.configure(bg='#FFFFFF')

# Ảnh logo
logo_image = ImageTk.PhotoImage(Image.open('C:\\Users\\ASUS\\Downloads\\logo.png').resize((100, 100), Image.ANTIALIAS))
logo_label = tk.Label(window, image=logo_image, bg='#FFFFFF')
logo_label.place(x=10, y=10)

# Thông tin tác giả
author_text = tk.Text(window, font=("Arial", 12), bg='#FFFFFF', fg='#333333', width=17, height=5)
author_text.insert(tk.END, "Tác giả:Đỗ Hữu Tú")
author_text.configure(state='disabled')
author_text.place(x=10, y=150, anchor='nw')

# Frame chứa nội dung
content_frame = tk.Frame(window, bg='#FFFFFF', bd=5)
content_frame.place(relx=0.2, rely=0.1, relwidth=0.8, relheight=0.8)

# Tiêu đề
title_label = tk.Label(content_frame, text="Trình kiểm tra lỗ hổng Web", font=("Arial Rounded MT Bold", 20), bg='#FFFFFF', fg='#333333')
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 20))

# Khung URL
url_frame = tk.Frame(content_frame, bg='#FFFFFF')
url_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

url_label = tk.Label(url_frame, text="URL đích:", font=("Arial", 12), bg='#FFFFFF', fg='#333333')
url_label.grid(row=0, column=0, padx=(5, 10), pady=5)

url_entry = tk.Entry(url_frame, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=(0, 5), pady=5, sticky='we')

# Khung nút
button_frame = tk.Frame(content_frame, bg='#FFFFFF')
button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

xss_button = tk.Button(button_frame, text="Kiểm tra XSS", font=("Arial", 12), command=test_xss, bg='#4CAF50', fg='#FFFFFF')
xss_button.grid(row=0, column=0, padx=(0, 10))

sql_button = tk.Button(button_frame, text="Kiểm tra SQL Injection", font=("Arial", 12), command=test_sql_injection, bg='#FF5722', fg='#FFFFFF')
sql_button.grid(row=0, column=1, padx=(10, 0))

csrf_button = tk.Button(button_frame, text="Kiểm tra CSRF", font=("Arial", 12), command=csrf_scan, bg='#2196F3', fg='#FFFFFF')
csrf_button.grid(row=0, column=2, padx=(10, 0))
# Cấu hình trọng số hàng và cột để các thành phần tự động thay đổi kích thước theo cửa sổ
content_frame.grid_rowconfigure(3, weight=1)
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)


# Chạy ứng dụng GUI
window.mainloop()
