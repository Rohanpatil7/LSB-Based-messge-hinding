import gui
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import os
import time
import tkinter as tk

def encrypt_and_hide():
    key = gui.password.get().encode()[:32]  # Ensure 32-byte key for AES-256
    secret_text =gui.messagebox1.get("1.0", tk.END).strip()

    if not secret_text:
        gui.showinfo("Error", "Please enter a secret message!")
        return

    encrypted_text = gui.encrypt_message(secret_text, key)
    
    image_path = gui.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        gui.showinfo("Error", "Please select an image file.")
        return
    
     # Show progress bar
    gui.progress["value"] = 20
    gui.root.update_idletasks()
    time.sleep(0.5)

    # Let the user choose where to save the output
    output_path = gui.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])

    gui.progress["value"] = 100
    gui.root.update_idletasks()
    time.sleep(0.5)

    if output_path:
        gui.hide_text_in_image(image_path, encrypted_text, output_path)
        gui.showinfo("Success", f"Message encrypted and saved in {output_path}!")
        gui.progress["value"] = 0  # Reset progress bar
    
def extract_and_decrypt():
    key = gui.password.get().encode()[:32]  # Ensure 32-byte key
    image_path = gui.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if not image_path:
        gui.showinfo("Error", "Please select an image file.")
        return

    gui.progress["value"] = 20
    gui.root.update_idletasks()
    time.sleep(0.5)

    extracted_encrypted_text = gui.extract_text_from_image(image_path)
    
    gui.progress["value"] = 50
    gui.root.update_idletasks()
    time.sleep(0.5)

    decrypted_text = gui.decrypt_message(extracted_encrypted_text, key)
    
    gui.progress["value"] = 100
    gui.root.update_idletasks()
    time.sleep(0.5)

    gui.messagebox2.delete("1.0", tk.END)
    gui.messagebox2.insert(tk.END, decrypted_text)

    gui.showinfo("Success", "Message extracted and decrypted successfully!")
    gui.progress["value"] = 0  # Reset progress bar
