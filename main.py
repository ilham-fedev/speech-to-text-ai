import datetime
import os
import queue
import threading
import tkinter as tk
import warnings
from tkinter import filedialog, messagebox, scrolledtext, ttk

import speech_recognition as sr
import whisper


class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text AI App")
        self.root.geometry("800x600")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.whisper_model = None
        self.is_recording = False
        self.text_queue = queue.Queue()

        self.setup_ui()
        self.load_whisper_model()
        self.process_queue()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(
            main_frame, text="Speech to Text AI", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(
            row=1, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E)
        )

        self.record_button = ttk.Button(
            control_frame, text="Start Recording", command=self.toggle_recording
        )
        self.record_button.grid(row=0, column=0, padx=(0, 10))

        self.clear_button = ttk.Button(
            control_frame, text="Clear Text", command=self.clear_text
        )
        self.clear_button.grid(row=0, column=1, padx=(0, 10))

        self.export_button = ttk.Button(
            control_frame, text="Export Text", command=self.export_text
        )
        self.export_button.grid(row=0, column=2)

        ttk.Label(main_frame, text="Recognition Method:").grid(
            row=2, column=0, sticky=tk.W, pady=(10, 5)
        )

        self.method_var = tk.StringVar(value="basic")
        method_frame = ttk.Frame(main_frame)
        method_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        ttk.Radiobutton(
            method_frame,
            text="Basic (Google - Multi-language)",
            variable=self.method_var,
            value="basic",
        ).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(
            method_frame,
            text="AI Enhanced (Whisper)",
            variable=self.method_var,
            value="whisper",
        ).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))

        ttk.Label(main_frame, text="Language:").grid(
            row=4, column=0, sticky=tk.W, pady=(10, 5)
        )

        self.language_var = tk.StringVar(value="en-US")
        language_frame = ttk.Frame(main_frame)
        language_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        ttk.Radiobutton(
            language_frame, text="English", variable=self.language_var, value="en-US"
        ).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(
            language_frame, text="Indonesian", variable=self.language_var, value="id-ID"
        ).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))

        ttk.Label(main_frame, text="Transcribed Text:").grid(
            row=6, column=0, sticky=tk.W, pady=(10, 5)
        )

        self.text_area = scrolledtext.ScrolledText(main_frame, height=20, width=70)
        self.text_area.grid(
            row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=8, column=0, columnspan=3, sticky=tk.W)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)

    def load_whisper_model(self):
        try:
            self.status_label.config(
                text="Loading Whisper model...", foreground="orange"
            )
            self.root.update()

            warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
            self.whisper_model = whisper.load_model("tiny")
            self.status_label.config(
                text="Ready - Whisper model loaded", foreground="green"
            )
        except Exception as e:
            self.status_label.config(
                text="Whisper model failed to load - using basic mode only",
                foreground="red",
            )
            print(f"Whisper model error: {e}")

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_button.config(text="Stop Recording")
        self.status_label.config(text="Recording...", foreground="red")

        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.daemon = True
        recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(text="Start Recording")
        self.status_label.config(text="Processing...", foreground="orange")

    def record_audio(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 300

            while self.is_recording:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(
                            source, timeout=5, phrase_time_limit=10
                        )

                    if self.method_var.get() == "whisper" and self.whisper_model:
                        text = self.transcribe_with_whisper(audio)
                    else:
                        text = self.transcribe_with_google(audio)

                    if text:
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        self.text_queue.put(f"[{timestamp}] {text}\n")

                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    self.text_queue.put(("ERROR", f"Error: {e}"))
                    break
                except Exception as e:
                    print(f"Recording error: {e}")

        except Exception as e:
            self.text_queue.put(("ERROR", f"Microphone error: {e}"))
        finally:
            if not self.is_recording:
                self.text_queue.put(("STATUS", "Ready"))

    def transcribe_with_google(self, audio):
        try:
            language = self.language_var.get()
            return self.recognizer.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            raise

    def transcribe_with_whisper(self, audio):
        try:
            import tempfile

            audio_data = audio.get_wav_data()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name

            language = "id" if self.language_var.get() == "id-ID" else "en"
            result = self.whisper_model.transcribe(temp_file_path, language=language)
            os.remove(temp_file_path)
            return result["text"].strip()
        except Exception as e:
            print(f"Whisper error: {e}")
            return self.transcribe_with_google(audio)

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)

    def export_text(self):
        text_content = self.text_area.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showwarning("Warning", "No text to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                messagebox.showinfo("Success", f"Text exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def process_queue(self):
        try:
            while True:
                item = self.text_queue.get_nowait()
                if isinstance(item, tuple):
                    msg_type, msg = item
                    if msg_type == "ERROR":
                        self.status_label.config(text=msg, foreground="red")
                    elif msg_type == "STATUS":
                        self.status_label.config(text=msg, foreground="green")
                else:
                    self.text_area.insert(tk.END, item)
                    self.text_area.see(tk.END)
        except queue.Empty:
            pass

        self.root.after(100, self.process_queue)


def main():
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
