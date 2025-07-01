import whisper
import argparse
import tkinter as tk
from tkinter import scrolledtext
import sounddevice as sd
import numpy as np
import wave
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Voice-to-Text Transcription")
        self.pack()
        self.create_widgets()
        self.is_recording = False
        self.frames = []

    def create_widgets(self):
        self.record_button = tk.Button(self)
        self.record_button["text"] = "Record"
        self.record_button["command"] = self.toggle_recording
        self.record_button.pack(side="top")

        self.transcribe_button = tk.Button(self, text="Transcribe", command=self.transcribe_audio_file)
        self.transcribe_button.pack(side="top")

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=10)
        self.output_text.pack(side="bottom")

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_button["text"] = "Stop Recording"
        self.frames = []
        self.stream = sd.InputStream(samplerate=16000, channels=1, callback=self.audio_callback, dtype='int16')
        self.stream.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button["text"] = "Record"
        self.stream.stop()
        self.stream.close()
        self.save_audio()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.frames.append(indata.copy())

    def save_audio(self):
        if not self.frames:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.INSERT, "No audio to save.")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, "Saving audio...")
        sound_file = wave.open("recorded_audio.wav", "wb")
        sound_file.setnchannels(1)
        audio_data = np.concatenate(self.frames, axis=0)
        sound_file.setsampwidth(audio_data.dtype.itemsize)
        sound_file.setframerate(16000)
        sound_file.writeframes(audio_data.tobytes())
        sound_file.close()
        self.output_text.insert(tk.INSERT, "\nAudio saved as recorded_audio.wav")


    def transcribe_audio_file(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, "Transcribing audio...")

        def run_transcription():
            try:
                model = whisper.load_model("base")
                result = model.transcribe("recorded_audio.wav")
                print(f"Transcription result: {result}")
                self.master.after(0, self.update_output_text, result["text"])
            except Exception as e:
                print(f"Transcription error: {e}")
                self.master.after(0, self.update_output_text, f"Error: {e}")

        transcription_thread = threading.Thread(target=run_transcription)
        transcription_thread.start()

    def update_output_text(self, text):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.INSERT, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()