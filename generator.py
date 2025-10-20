import uuid
import secrets
import base64
import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

def generate_license_key():
    parts = []
    for _ in range(4):
        part = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(4))
        parts.append(part)
    return '-'.join(parts)

def create_license(valid_days):
    license_key = generate_license_key()
    start_date = datetime.now()
    end_date = start_date + timedelta(days=valid_days)

    license_data = {
        'license_key': license_key,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    json_data = json.dumps(license_data)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

    current_dir = os.getcwd()
    file_name = os.path.join(current_dir, f"license_{license_key.replace('-', '')}.json")
    with open(file_name, 'w') as file:
        json.dump({'data': encoded_data}, file)

    return license_key, file_name

def generate_license():
    try:
        valid_days = int(entry_days.get())
        license_key, file_name = create_license(valid_days)
        messagebox.showinfo("Basarili", f"Lisans dosyasi olusturuldu:\n{file_name}\n\nLisans Anahtari:\n{license_key}")
    except ValueError:
        messagebox.showerror("Hata", "Gecerli bir sayi giriniz!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lisans Uretici")
    root.geometry("400x200")

    tk.Label(root, text="Gecerli Gun Sayisi:").pack(pady=10)
    entry_days = tk.Entry(root)
    entry_days.pack(pady=10)

    tk.Button(root, text="Lisans Olustur", command=generate_license).pack(pady=20)

    root.mainloop()
