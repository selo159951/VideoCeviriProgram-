import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip
from faster_whisper import WhisperModel
import os
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
                                # Ses çıkarma fonksiyonu
                def extract_audio(video_path, audio_path="temp_audio.wav"):
                    video = VideoFileClip(video_path)
                    audio = video.audio
                    audio.write_audiofile(audio_path)
                    return audio_path

                # Zaman damgasını SRT formatına çevirme
                def format_timestamp(seconds):
                    hours = int(seconds // 3600)
                    minutes = int((seconds % 3600) // 60)
                    secs = int(seconds % 60)
                    millis = int((seconds - int(seconds)) * 1000)
                    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

                # Altyazı oluşturma fonksiyonu
                def transcribe_audio_to_srt(audio_path, srt_path="output.srt", model_size="base", language="auto"):
                    # CPU üzerinden çalışacak şekilde "compute_type" belirledik
                    model = WhisperModel(model_size, compute_type="int8")  # GPU yerine CPU kullanıyoruz

                    # Ses dosyasını transkribe et
                    segments, _ = model.transcribe(audio_path, language=language if language != "auto" else None)

                    with open(srt_path, "w", encoding="utf-8") as f:
                        for i, segment in enumerate(segments):
                            start = format_timestamp(segment.start)
                            end = format_timestamp(segment.end)
                            text = segment.text.strip()
                            f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")
                    return srt_path

                # Video dosyasını seçme fonksiyonu
                def select_video():
                    filepath = filedialog.askopenfilename(filetypes=[("Video Dosyaları", "*.mp4 *.mkv *.avi *.mov")])
                    if filepath:
                        entry_video_path.delete(0, tk.END)
                        entry_video_path.insert(0, filepath)

                # İşlem başlatma fonksiyonu
                def start_process():
                    video_path = entry_video_path.get()
                    model_choice = model_var.get()
                    lang_choice = lang_var.get()

                    if not os.path.isfile(video_path):
                        messagebox.showerror("Hata", "Geçerli bir video dosyası seçilmedi.")
                        return

                    try:
                        messagebox.showinfo("İşlem Başladı", "Lütfen bekleyin, altyazı oluşturuluyor...")
                        audio_path = extract_audio(video_path)
                        srt_path = os.path.splitext(video_path)[0] + ".srt"
                        transcribe_audio_to_srt(audio_path, srt_path, model_choice, lang_choice)
                        os.remove(audio_path)
                        messagebox.showinfo("Tamamlandı", f"Altyazı oluşturuldu:\n{srt_path}")
                    except Exception as e:
                        messagebox.showerror("Hata", f"Hata oluştu:\n{e}")

                # GUI oluşturma
                root = tk.Tk()
                root.title("🎬 Altyazı Oluşturucu (Faster-Whisper)")
                root.geometry("550x350")

                # Video dosyası seçme
                tk.Label(root, text="📁 Video Dosyası:").pack(pady=(10, 5))
                entry_video_path = tk.Entry(root, width=60)
                entry_video_path.pack(padx=20)
                tk.Button(root, text="Gözat", command=select_video).pack(pady=5)

                # Model seçimi
                tk.Label(root, text="🧠 Model Seç (tiny - large):").pack(pady=(15, 5))
                model_var = tk.StringVar(value="base")
                tk.OptionMenu(root, model_var, "tiny", "base", "small", "medium", "large").pack()

                # Dil seçimi
                tk.Label(root, text="🌍 Dil Seç (auto önerilir):").pack(pady=(15, 5))
                lang_var = tk.StringVar(value="auto")
                tk.OptionMenu(root, lang_var, "auto", "tr", "en", "de", "fr", "es", "ar").pack()

                # İşlem butonu
                tk.Button(root, text="🚀 Altyazıyı Oluştur", command=start_process, bg="#4CAF50", fg="white").pack(pady=20)

                # GUI çalıştırma
                root.mainloop()
                
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


