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


# Function to decrypt the key
MASTER_kEY = "NextCyber@2023"

# Telegram Bot Token (Replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7636098514:AAHbDD7H4g6zKxHp8dXk2wHAE5N53jY-KmQ"

# Allowed Contacts (Replace with actual contact numbers & corresponding chat IDs)
ALLOWED_CONTACTS = {
<<<<<<< Updated upstream
    "9529440255": "7206195146",
    "9876543210": "CHAT_ID_FOR_9876543210"
=======
    9529440255: 7206195146,
    9405895177: 8157014588,
>>>>>>> Stashed changes
}

# Function to send encryption key via Telegram if contact is authorized
async def send_key_via_telegram(contact, key):
    if contact in ALLOWED_CONTACTS:
        try:

            # Send the key to the authorized contact via Telegram
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            await bot.send_message(chat_id=ALLOWED_CONTACTS[contact], text=f"🔐 Your Encryption Key: {key}")
            messagebox.showinfo("Success", f"Key sent to Telegram for {contact}! \n 🔑 Use the app with your shared decryption key to decode this.")
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
    if not input_image_path or not secret_message.get("1.0", "end-1c") or not encryption_key.get() or not contact_number.get():
        messagebox.showerror("Error", "Please select an image, enter a message, key, and contact number!")
        return

    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not output_image_path:
        return

    crypto_steg = CryptoSteganography(encryption_key.get())
    encrypted_message = encrypt_message(secret_message.get("1.0", "end-1c"), encryption_key.get())

    try:
        crypto_steg.hide(input_image_path, output_image_path, encrypted_message)

        # Removed as output_image_path is not relevant in extract_secret
        contact = contact_number.get()
        if not contact.isdigit():
            messagebox.showerror("Error", "Contact number must be numeric!")
            return
        
        # 🔐 Encrypt the key with MASTER_KEY before sending
        encrypted_key_to_send = encrypt_message(encryption_key.get(), MASTER_kEY)
        asyncio.run(send_key_via_telegram(int(contact), encrypted_key_to_send ))

        messagebox.showinfo("Success", "Message hidden successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide message: {e}")

# Extract Secret from Image
def extract_secret():
    image_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if not image_path or not encryption_key.get():
        messagebox.showerror("Error", "Please select an image and provide a key!")
        return
    
    encrypted_input_key = encryption_key.get()

     # Step 1: Decrypt the encrypted key using MASTER_kEY
    actual_key = decrypt_message(encrypted_input_key, MASTER_kEY)

    if not actual_key:
        messagebox.showerror("Error", "Failed to decrypt the encryption key. Please check the encrypted key.")
        return 

    # key = encryption_key.get()
    crypto_steg = CryptoSteganography(actual_key)

    try:
        encrypted_message = crypto_steg.retrieve(image_path)
        if encrypted_message is None:
            messagebox.showerror("Error", "No hidden message found in the image!")
            return
    

        encrypted_message = crypto_steg.retrieve(image_path)
        print("Retrieved Encrypted Message:", encrypted_message)

        if encrypted_message is None:
            messagebox.showerror("Error", "No hidden message found in the image!")
            return

        decrypted_message = decrypt_message(encrypted_message, actual_key)
        if decrypted_message:
            messagebox.showinfo("Decrypted Message", decrypted_message)
        else:
            messagebox.showerror("Error", "Incorrect key! Unable to decrypt.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    
def combine_funcs(*funcs): 
   
    def inner_combined_func(*args, **kwargs): 
        for f in funcs: 
   
            f(*args, **kwargs) 
    
    return inner_combined_func 

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


# Decrypt Key Function
# def decrypt_key():
    # encrypted_input = encrypted_key_input.get()
    # print("Encrypted Key Input:", encrypted_input)

    # key_input = decryption_key_input.get()
    # if not encrypted_input:
    #     messagebox.showerror("Error", "Please enter both encrypted key and decryption key!")
    #     return

    # result = decrypt_message(encrypted_input, MASTER_kEY)
    # result2 = decrypt_message(encrypted_input, MASTER_kEY)
    # if result2:
    #     decrypted_password_label.config(text=f"Decrypted Password: {result2}")

    # else:
    #     messagebox.showerror("Error", "Decryption failed. Check your key or encrypted string.")
    # if result:
    #     decrypted_password_label.config(text=f"Decrypted Password: {result}")
    # else:
    #     messagebox.showerror("Error", "Decryption failed. Check your key or encrypted string.")



# GUI Setup
root = tk.Tk()
root.title("Steganography with AES-256 & Telegram")
root.geometry("800x550")
root.resizable(True, True)


input_image_path = ""

# Image Selection Button
png_icon = tk.PhotoImage(file="C:/Users/ytroh/OneDrive/Documents/GitHub/Stegnography/main/png_f.png")
tk.Button(root, text="Select Image", command=load_image, image=png_icon, compound="left",bd=1, relief="solid").pack(pady=10, padx=5)

# Image Display
image_label = tk.Label(root)
image_label.pack()

# Secret Message Entry
tk.Label(root, text="Secret Message:").pack()
secret_message = tk.Text(root, width=60, height=10, bd=1, relief="solid")
secret_message.pack(pady=5, padx=5, expand=True, fill=tk.Y)
Hovertip(secret_message, "Enter the message you want to hide in the image")

# Encryption Key Entry
tk.Label(root, text="Encryption Key:").pack()

encryption_key = tk.Entry(root, width=40, show="*", bd=1, relief="solid")
encryption_key.pack(pady=5)
# Hovertip for Encryption Key
Hovertip(encryption_key, "Enter your password to encode the massage as well as Enter Encrpted Key to decode the message")


# Contact Number Entry
tk.Label(root, text="Enter Contact Number:").pack()
contact_number = tk.Entry(root, width=40, bd=1, relief="solid")
contact_number.pack(pady=5)
Hovertip(contact_number, "Enter the contact number to send the encryption key via Telegram")

def delete_text():
    secret_message.delete("1.0", "end")
    encryption_key.delete(0, "end")
    contact_number.delete(0, "end")
    input_image_path.delete(0, "end")

    
# Hide and Extract Buttons
encryption_icon = tk.PhotoImage(file="C:/Users/ytroh/OneDrive/Documents/GitHub/Stegnography/main/lock.png")
tk.Button(root, text="Hide Message", command=combine_funcs(hide_secret, delete_text), image=encryption_icon, compound="left",bd=1, relief="solid").pack(pady=10)
extract_icon = tk.PhotoImage(file="C:/Users/ytroh/OneDrive/Documents/GitHub/Stegnography/main/text.png")
tk.Button(root, text=" Choose Image to extract message", command=extract_secret , image=extract_icon, compound="left",bd=1, relief="solid").pack(pady=5)

# Separator
tk.Label(root, text="----------------------------------------------------------------------------------").pack(pady=5)

# Encrypted Key Decryption Section
# tk.Label(root, text="Enter Encrypted Key:").pack()
# encrypted_key_input = tk.Entry(root, width=40,bd=1, relief="solid")
# encrypted_key_input.pack(pady=5)

# decryption_icon = tk.PhotoImage(file="C:/Users/ytroh/OneDrive/Documents/GitHub/Stegnography/main/shield.png")
# tk.Button(root, text="Decrypt Encrypted Key", command=decrypt_key, image=decryption_icon, compound="left", bd=1, relief="solid").pack(pady=10)


# tk.Label(root, text="Decryption Key:").pack()
# decryption_key_input = tk.Entry(root, width=40, show="*")
# decryption_key_input.pack(pady=5)

# Run the Application
root.mainloop()