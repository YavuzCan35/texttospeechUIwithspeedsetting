import pyttsx3
import threading
import tkinter as tk
from tkinter import ttk
stopflag=False
class PlayPauseButton(tk.Button):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.paused = True
        self.audio_thread = None

    def toggle_play_pause(self):
        if self.paused:
            self.play()
        else:
            self.pause()

    def play(self):
        self.config(text="Pause")
        if self.paused:
            self.paused = False
            if not self.audio_thread or not self.audio_thread.is_alive():
                self.audio_thread = threading.Thread(target=self._play_audio)
                self.audio_thread.start()

    def _play_audio(self):
        global new_engine
        new_engine = pyttsx3.init()
        if not self.paused:
            new_engine.setProperty("rate", speed_slider.get() * 150)  # Adjust the factor as needed
            new_engine.say(text_entry.get("1.0", "end-1c"))
            new_engine.startLoop()
            while new_engine.iterate() and not self.paused:
                pass
        new_engine.setBusy(True)
        new_engine.endLoop()
        new_engine.stop()

    def pause(self):
        self.config(text="Play")
        self.paused = True
        if new_engine.isBusy():
            new_engine.endLoop()
def stop_audio():
    global stopflag
    stopflag ^= True

def update_speed(new_speed):
    speed_label.config(text=f"Speed: {new_speed:.2f}")
    global current_speed
    current_speed = new_speed

# Create the GUI window
root = tk.Tk()
root.title("Text-to-Speech with Speed Adjustment")

# Text entry
text_entry = tk.Text(root, wrap=tk.WORD, height=5, width=40)
text_entry.pack(padx=10, pady=10)

# Speed slider
speed_slider = ttk.Scale(root, from_=0.5, to=2.0, length=200, orient="horizontal", value=1.0)
speed_slider.pack(padx=10, pady=5)
speed_slider.bind("<Motion>", lambda event: update_speed(speed_slider.get()))

# Speed label
speed_label = tk.Label(root, text="Speed: 1.00")
speed_label.pack(padx=10, pady=5)

# Play/Pause button
play_button = PlayPauseButton(root, text="Play")
play_button.config(command=play_button.toggle_play_pause)  # Change the command to toggle_play_pause
play_button.pack(pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_audio)
stop_button.pack(pady=5)

# Initialize current speed and button
current_speed = 1.0
current_button = play_button

# Run the GUI event loop
root.mainloop()
