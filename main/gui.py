import tkinter as tk

from tkinter import ttk,Text
from tkinter.ttk import Label
from tkinter import Frame
from tkinter.messagebox import showinfo
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.title('Messege Hinding In Image')
root.geometry('1024x650+50+50')
root.resizable(False, False)

def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        load_image(file_path)

def load_image(file_path):
    global img_display  # Prevent garbage collection from deleting the image reference
    img = Image.open(file_path)

    img_width, img_height = img.size
    

    max_width, max_height = 390, 280  # The display size

    ratio = min(max_width / img_width, max_height / img_height)

    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    img_display = ImageTk.PhotoImage(img)
    image_label.config(image=img_display)

    x_offset = (max_width - new_width) // 2
    y_offset = (max_height - new_height) // 2
    image_label.place(x=x_offset, y=y_offset, width=new_width, height=new_height)

choose_img_btn = ttk.Button(root, text="Choose Image", command=choose_image)
choose_img_btn.place(x=200, y=325, width=120, height=40)

# Frame for Image (Same size & position as messagebox1)
image_frame1 = Frame(root, width=400, height=280, relief="solid", borderwidth=2)
image_frame1.place(x=100, y=20)  # Aligned with messagebox1

# Image Label (inside frame)
image_label = Label(image_frame1)
image_label.place(x=150, y=400, width=300, height=100)

message_label1 = Label(root, text='Message')
message_label1.place(x=80,y=400)

messagebox1= tk.Text(root, wrap="word", width=40, height=5)
messagebox1.place(x=150,y=400,width=300, height=100)

button1 = ttk.Button(root, text="Encrypt")
button1.place(x=250,y=530,width=120, height=60)

message_label2 = Label(root, text='Secrete Message')
message_label2.place(x=480,y=400)

messagebox2= tk.Text(root, wrap="word", width=40, height=5)
messagebox2.place(x=580,y=400,width=300, height=100,)

button2 = ttk.Button(root, text="Decrypt")
button2.place(x=650,y=530,width=120, height=60)

password_label = Label(root, text='Password')
password_label.place(x=80,y=600)
password = ttk.Entry(root, show="*")
password.place(x=150,y=600,width=700, height=30)

# message = tk.StringVar()
# message_label = tk.Label(text="Secrete Message:")

# message_entry = tk.Entry(message_label, textvariable=message)
# message_entry.pack(fill='x', expand=True)
# message_entry.focus()

# encrypt_button = tk.Button(text="Encrypt", command=lambda: showinfo('Success', 'Message Encrypted'))
# encrypt_button.pack(fill='x', expand=True, pady=10)
root.mainloop()
