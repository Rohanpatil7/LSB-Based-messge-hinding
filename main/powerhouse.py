import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cryptosteganography import CryptoSteganography
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import telegram

# Telegram Bot Token (Replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7636098514:AAHbDD7H4g6zKxHp8dXk2wHAE5N53jY-KmQ"

# Allowed Contacts (Replace with actual contact numbers & corresponding chat IDs)
ALLOWED_CONTACTS = {
    "9529440255": "7206195146",
    "9876543210": "CHAT_ID_FOR_9876543210"
}

# Function to send encryption key via Telegram if contact is authorized
def send_key_via_telegram(contact, key):
    if contact in ALLOWED_CONTACTS:
        try:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            bot.send_message(chat_id=ALLOWED_CONTACTS[contact], text=f"🔐 Your Encryption Key: {key}")
            messagebox.showinfo("Success", f"Key sent to Telegram for {contact}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send key: {e}")
    else:
        messagebox.showerror("Error", "Contact not authorized to receive the key.")

# AES-256 Encryption
def encrypt_message(message, key):
    key = key.ljust(32)[:32].encode()
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_bytes).decode()

# AES-256 Decryption
def decrypt_message(encrypted_message, key):
    try:
        key = key.ljust(32)[:32].encode()
        encrypted_data = base64.b64decode(encrypted_message)
        iv, encrypted_bytes = encrypted_data[:16], encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_bytes), AES.block_size).decode()
    except Exception:
        return None

# Hide Secret in Image
def hide_secret():
    if not input_image_path or not secret_message.get() or not encryption_key.get() or not contact_number.get():
        messagebox.showerror("Error", "Please select an image, enter a message, key, and contact number!")
        return

    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not output_image_path:
        return

    crypto_steg = CryptoSteganography("dummy_key")
    encrypted_message = encrypt_message(secret_message.get(), encryption_key.get())

    try:
        crypto_steg.hide(input_image_path, output_image_path, encrypted_message)
        send_key_via_telegram(contact_number.get(), encryption_key.get())  # Send key if contact is valid
        messagebox.showinfo("Success", "Message hidden successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide message: {e}")

# Extract Secret from Image
def extract_secret():
    image_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if not image_path or not encryption_key.get():
        messagebox.showerror("Error", "Please select an image and provide a key!")
        return

    crypto_steg = CryptoSteganography("dummy_key")
    encrypted_message = crypto_steg.retrieve(image_path)

    if encrypted_message:
        decrypted_message = decrypt_message(encrypted_message, encryption_key.get())
        if decrypted_message:
            messagebox.showinfo("Decrypted Message", decrypted_message)
        else:
            messagebox.showerror("Error", "Incorrect key! Unable to decrypt.")
    else:
        messagebox.showerror("Error", "No hidden message found!")

# Load and Display Image
def load_image():
    global input_image_path
    input_image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
    
    if input_image_path:
        img = Image.open(input_image_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

# GUI Setup
root = tk.Tk()
root.title("Steganography with AES-256 & Telegram")
root.geometry("400x550")
root.resizable(False, False)

input_image_path = ""

# Image Selection Button
tk.Button(root, text="Select Image", command=load_image).pack(pady=10)

# Image Display
image_label = tk.Label(root)
image_label.pack()

# Secret Message Entry
tk.Label(root, text="Secret Message:").pack()
secret_message = tk.Entry(root, width=40)
secret_message.pack(pady=5)

# Encryption Key Entry
tk.Label(root, text="Encryption Key:").pack()
encryption_key = tk.Entry(root, width=40, show="*")
encryption_key.pack(pady=5)

# Contact Number Entry
tk.Label(root, text="Enter Contact Number:").pack()
contact_number = tk.Entry(root, width=40)
contact_number.pack(pady=5)

# Hide and Extract Buttons
tk.Button(root, text="Hide Message", command=hide_secret).pack(pady=10)
tk.Button(root, text="Extract Message", command=extract_secret).pack(pady=5)

# Run the Application
root.mainloop()