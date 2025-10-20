import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import json
from datetime import datetime
import subprocess
import os



def select_license_file():
    file_path = filedialog.askopenfilename(
        title="Lisans Dosyasini Sec",
        filetypes=[("JSON Files", "*.json")]
    )

    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = json.load(file)
                encoded_data = content.get('data', '')

            decoded_json = base64.b64decode(encoded_data).decode('utf-8')
            license_info = json.loads(decoded_json)

            license_key = license_info['license_key']
            start_date = datetime.strptime(license_info['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(license_info['end_date'], '%Y-%m-%d')
            today = datetime.now()

            if start_date <= today <= end_date:
                messagebox.showinfo("Gecerli Lisans", f"Lisans anahtari dogrulandi:\n{license_key}")
                # video_translator.py dosyasini calistir
                script_path = os.path.join(os.getcwd(), "init.py")
                subprocess.Popen(["python", script_path])
                root.destroy()
            else:
                messagebox.showerror("Suresi Dolmus", "Lisans suresi dolmus veya gecerli degil!")
                exit()

        except Exception as e:
            messagebox.showerror("Hata", f"Lisans dosyasi okunamadi: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ana Uygulama - Lisans Kontrol")
    root.geometry("400x200")

    tk.Button(root, text="Lisans Dosyasi Sec", command=select_license_file, width=25, height=2).pack(pady=60)

    root.mainloop()