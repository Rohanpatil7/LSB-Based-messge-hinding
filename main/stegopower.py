# Cleaned and Fixed Version of Your Code
import tkinter as tk
from idlelib.tooltip import Hovertip
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cryptosteganography import CryptoSteganography
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import telegram
import asyncio

# Constants
MASTER_KEY = "NextCyber@2023"
TELEGRAM_BOT_TOKEN = "7636098514:AAHbDD7H4g6zKxHp8dXk2wHAE5N53jY-KmQ"
ALLOWED_CONTACTS = {
    9529440255: 7206195146,
    9405895177: 8157014588,
}

# Encryption/Decryption Functions
def encrypt_message(message, key):
    key = key.ljust(32)[:32].encode()
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_bytes).decode()

def decrypt_message(encrypted_message, key):
    try:
        key = key.ljust(32)[:32].encode()
        encrypted_data = base64.b64decode(encrypted_message)
        iv, encrypted_bytes = encrypted_data[:16], encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_bytes), AES.block_size).decode()
    except Exception as e:
        print("Decryption failed:", e)
        return None

# Telegram Function
async def send_key_via_telegram(contact, key):
    if contact in ALLOWED_CONTACTS:
        try:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            await bot.send_message(chat_id=ALLOWED_CONTACTS[contact], text=f"\U0001F510 Your Encryption Key: {key}")
            messagebox.showinfo("Success", f"Key sent to Telegram for {contact}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send key: {e}")
    else:
        messagebox.showerror("Error", "Contact not authorized to receive the key.")

# GUI Functions
def hide_secret():
    if not input_image_path or not secret_message.get("1.0", "end-1c") or not encryption_key.get() or not contact_number.get():
        messagebox.showerror("Error", "Please complete all fields!")
        return

    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not output_image_path:
        return

    aes_key = encryption_key.get()
    crypto_steg = CryptoSteganography(aes_key)
    encrypted_text = encrypt_message(secret_message.get("1.0", "end-1c"), aes_key)

    try:
        crypto_steg.hide(input_image_path, output_image_path, encrypted_text)
        encrypted_key_to_send = encrypt_message(aes_key, MASTER_KEY)
        asyncio.run(send_key_via_telegram(int(contact_number.get()), encrypted_key_to_send))
        messagebox.showinfo("Success", "Message hidden successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide message: {e}")


def extract_secret():
    image_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if not image_path or not encryption_key.get():
        messagebox.showerror("Error", "Select an image and enter the encrypted key.")
        return

    encrypted_input_key = encryption_key.get()
    actual_key = decrypt_message(encrypted_input_key, MASTER_KEY)

    if not actual_key:
        messagebox.showerror("Error", "Invalid encrypted key.")
        return

    crypto_steg = CryptoSteganography(actual_key)
    try:
        encrypted_message = crypto_steg.retrieve(image_path)
        if not encrypted_message:
            messagebox.showerror("Error", "No hidden message found!")
            return
        decrypted_message = decrypt_message(encrypted_message, actual_key)
        if decrypted_message:
            messagebox.showinfo("Decrypted Message", decrypted_message)
        else:
            messagebox.showerror("Error", "Failed to decrypt the message.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def load_image():
    global input_image_path
    input_image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
    if input_image_path:
        img = Image.open(input_image_path).resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk


def clear_fields():
    secret_message.delete("1.0", "end")
    encryption_key.delete(0, "end")
    contact_number.delete(0, "end")

# GUI Setup
root = tk.Tk()
root.title("AES Steganography with Telegram")
root.geometry("800x600")

input_image_path = ""

# Widgets
img_icon = tk.PhotoImage(file="main/png_f.png")
lock_icon = tk.PhotoImage(file="main/lock.png")
text_icon = tk.PhotoImage(file="main/text.png")

tk.Button(root, text="Select Image", command=load_image, image=img_icon, compound="left").pack(pady=10)
image_label = tk.Label(root)
image_label.pack()

tk.Label(root, text="Secret Message:").pack()
secret_message = tk.Text(root, width=60, height=10)
secret_message.pack()
Hovertip(secret_message, "Enter your secret message")

tk.Label(root, text="Encryption Key:").pack()
encryption_key = tk.Entry(root, width=40, show="*")
encryption_key.pack()
Hovertip(encryption_key, "Enter encryption key or encrypted key for retrieval")

tk.Label(root, text="Contact Number:").pack()
contact_number = tk.Entry(root, width=40)
contact_number.pack()
Hovertip(contact_number, "Telegram contact number")

tk.Button(root, text="Hide Message", command=hide_secret, image=lock_icon, compound="left").pack(pady=10)
tk.Button(root, text="Extract Message", command=extract_secret, image=text_icon, compound="left").pack(pady=10)

root.mainloop()
