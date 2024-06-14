import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox,ttk
import os
import asyncio
import aiohttp
import threading
from thuvien import *
from concurrent.futures import ThreadPoolExecutor

def select_folder(var):
    folder_selected = filedialog.askdirectory()
    var.set(folder_selected)

def open_folder(var):
    folder = var.get()
    if os.path.isdir(folder):
        os.startfile(folder)
    else:
        messagebox.showerror("Lỗi", "Thư mục không hợp lệ")

def HandleURL(url,num):
    urlHandle = ""
    if(url.find("[@Num]")!= -1):
        url2 = url.split("[@Num]")
        urlHandle+=url2[0]
        urlHandle+=str(num)
        urlHandle+=url2[1]
           
        return urlHandle
    else:
        messagebox.showerror("Cảnh báo", "Trong đường dẫn url không tìm thấy ký tự [@Num]")
        return ""


def start_download():
    if(url_entry.get() == ""):
        messagebox.showerror("Cảnh báo", "Chưa chọn url")
        return
    url = url_entry.get()
    if(start_entry.get() == "" or end_entry.get() == ""):
        messagebox.showerror("Cảnh báo", "Chưa chọn chỉ số bắt đầu hoặc kết thúc")
        return
    start_num = int(start_entry.get())
    end_num = int(end_entry.get())
    if(folder_path1.get() == ""):
        messagebox.showerror("Cảnh báo", "Chưa chọn đường dẫn lưu file")
        return
    folder = folder_path1.get()
    
    if(name_entry1.get() == ""):
        messagebox.showerror("Cảnh báo", "Chưa nhập tên file")
        return
    name = name_entry1.get()
    
    ngonngu = language_combobox1.get()
    mode_ngonngu = "vi"
    if(ngonngu =="Tiếng Việt"):
        mode_ngonngu = 'vi'
    else:
       mode_ngonngu = 'en'
    name_label1.config(text=name)
    messagebox.showinfo("Thông tin tải", f"Tên: {name}\nURL: {url}\nSố bắt đầu: {start_num}\nSố kết thúc: {end_num}\nThư mục: {folder}")

    def download(i):
        url2 = HandleURL(url, i)
        # Giả sử rằng hàm render là async và đã được định nghĩa ở đâu đó trong mã của bạn
        asyncio.run(render(url2, name + str(i), mode_ngonngu,folder))

    messagebox.showinfo("Thông báo", "Đang bắt đầu xử lý")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download, i) for i in range(start_num, end_num + 1)]
        executor.shutdown(wait=True)
    messagebox.showinfo("Thông báo", "Tải thành công")


def download_fixed_urls():
    urls = url_textbox.get("1.0", tk.END).strip().split('\n')
    urls = [url for url in urls if url.strip() != '']  # Loại bỏ các dòng trống

    if(len(urls)<=0):
        messagebox.showerror("Cảnh báo", "Chưa có đường dẫn ")
        return
    
    
    if(folder_path2.get() == ""):
        messagebox.showerror("Cảnh báo", "Chưa chọn đường dẫn lưu file")
        return
    if(name_entry2.get() == ""):
        messagebox.showerror("Cảnh báo", "Chưa nhập tên file")
        return
    folder = folder_path2.get()
    name = name_entry2.get()
    name_label2.config(text=name)
    ngonngu = language_combobox2.get()
    mode_ngonngu2 = "vi"
    if(ngonngu =="Tiếng Việt"):
        mode_ngonngu2 = 'vi'
    else:
       mode_ngonngu2 = 'en'
    print(urls)
    print("mode cbb2 : "+mode_ngonngu2)
    def download(i,url2):
       
        # Giả sử rằng hàm render là async và đã được định nghĩa ở đâu đó trong mã của bạn
        asyncio.run(render(url2, name + str(i+1),mode_ngonngu2,folder))

    messagebox.showinfo("Thông báo", "Đang bắt đầu xử lý")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download, i,urls[i]) for i in range(len(urls))]
        executor.shutdown(wait=True)
    messagebox.showinfo("Thông báo", "Tải thành công")
# Tạo cửa sổ chính
root = tk.Tk()
root.title("Trình tải tệp")
root.resizable(False, False)  # Không cho phép thay đổi kích thước cửa sổ

# Tạo Groupbox 1
groupbox1 = tk.LabelFrame(root, text="Tải theo số thứ tự")
groupbox1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(groupbox1, text="Tên:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry1 = tk.Entry(groupbox1, width=50)
name_entry1.grid(row=0, column=1, padx=5, pady=5)
name_label1 = tk.Label(groupbox1, text="")
name_label1.grid(row=0, column=2, padx=5, pady=5)

tk.Label(groupbox1, text="URL:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
url_entry = tk.Entry(groupbox1, width=50)
url_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(groupbox1, text="Số bắt đầu:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
start_entry = tk.Entry(groupbox1)
start_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(groupbox1, text="Số kết thúc:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
end_entry = tk.Entry(groupbox1)
end_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

folder_path1 = tk.StringVar()
tk.Button(groupbox1, text="Chọn thư mục", command=lambda: select_folder(folder_path1)).grid(row=4, column=0, padx=5, pady=5)
tk.Label(groupbox1, textvariable=folder_path1).grid(row=4, column=1, padx=5, pady=5)
tk.Button(groupbox1, text="Mở thư mục", command=lambda: open_folder(folder_path1)).grid(row=4, column=2, padx=5, pady=5)


tk.Label(groupbox1,text="Ngôn ngữ Dịch Sang :").grid(row=6, column=0, padx=5, pady=5, sticky="e")
language_combobox1 = ttk.Combobox(groupbox1, values=["Tiếng Anh", "Tiếng Việt"])
language_combobox1.grid(row=6, column=1, padx=5, pady=5, sticky="w")
language_combobox1.set("Tiếng Việt") 

tk.Button(groupbox1, text="Bắt đầu tải", command=start_download).grid(row=7, column=0, columnspan=3, pady=10)

# Tạo Groupbox 2
groupbox2 = tk.LabelFrame(root, text="Tải theo đường dẫn cố định")
groupbox2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(groupbox2, text="Tên:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry2 = tk.Entry(groupbox2, width=50)
name_entry2.grid(row=0, column=1, padx=5, pady=5)
name_label2 = tk.Label(groupbox2, text="")
name_label2.grid(row=0, column=2, padx=5, pady=5)

url_textbox = scrolledtext.ScrolledText(groupbox2, width=50, height=10)
url_textbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

folder_path2 = tk.StringVar()
tk.Button(groupbox2, text="Chọn thư mục", command=lambda: select_folder(folder_path2)).grid(row=2, column=0, padx=5, pady=5)
tk.Label(groupbox2, textvariable=folder_path2).grid(row=2, column=1, padx=5, pady=5)
tk.Button(groupbox2, text="Mở thư mục", command=lambda: open_folder(folder_path2)).grid(row=2, column=2, padx=5, pady=5)
tk.Label(groupbox2, text="Ngôn ngữ:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

tk.Label(groupbox2, text="Ngôn ngữ Dịch Sang :").grid(row=4, column=0, padx=5, pady=5, sticky="e")
language_combobox2 = ttk.Combobox(groupbox2, values=["Tiếng Anh", "Tiếng Việt"])
language_combobox2.grid(row=4, column=1, padx=5, pady=5, sticky="w")
language_combobox2.set("Tiếng Việt")  # Thiết lập giá trị mặc định

tk.Button(groupbox2, text="Bắt Đầu Tải", command=download_fixed_urls).grid(row=5, column=0, columnspan=3, pady=10)

# Chạy giao diện
root.mainloop()
