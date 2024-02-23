from tkinter import ttk
import os
import subprocess
import pygame
import time
stopflag = False
def speed_up_audio(input_file, output_file=None, speed_factor=1.5, ffmpeg_path="C:\\ffmpeg\\ffmpeg.exe"):
    if output_file is None:
        root, ext = os.path.splitext(input_file)
        output_file = f"{root}_speedup{ext}"

    # Run FFmpeg to speed up the audio
    command = [
        ffmpeg_path,
        "-y",  # Add this option to automatically overwrite existing files
        "-i", input_file,
        "-filter:a", f"atempo={speed_factor},highpass=f=250, lowpass=f=3000",
        output_file
    ]

    subprocess.run(command, check=True)

    print(f"Audio speed-up completed. Output file: {output_file}")

class PlayButton(tk.Button):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.root = master

    def play(self):
        audio_thread = threading.Thread(target=self._play_audio)
        audio_thread.start()

    def _play_audio(self):
        # Get the text from the text entry
        text = text_entry.get("1.0", "end-1c").replace('\n', ' ')

        pygame.mixer.quit()
        # Save the text to a temporary file
        temp_file = "temp.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(temp_file)
        input_file_path = "temp.mp3"  # Replace with the actual path to your input MP3 file
        output_file_path = "output_speedup.mp3"  # Replace with the desired output path

        ffmpeg_executable_path = r"C:\\ffmpeg\\ffmpeg.exe"  # Replace with the actual path to your FFmpeg executable

        speed_up_audio(input_file_path, output_file_path, speed_factor=current_speed, ffmpeg_path=ffmpeg_executable_path)
        # Play the audio file
        #os.system("start " + output_file_path)
        # Initialize Pygame mixer

        pygame.mixer.init()

        # Load the speed-adjusted audio
        pygame.mixer.music.load(output_file_path)

        # Play the audio
        pygame.mixer.music.play()


def stop_audio():
    global stopflag
    stopflag =True
    pygame.mixer.quit()

def clear_text_box():
    text_entry.delete("1.0", tk.END)

def repeat_text():
    play_button.play()

def update_speed(new_speed):
    speed_label.config(text=f"Speed: {new_speed:.2f}")
    global current_speed
    current_speed = new_speed

def paste_text(event):
    try:
        text = root.clipboard_get()
        text_entry.insert(tk.INSERT, text)
    except tk.TclError:
        pass  # Handle the exception if there's nothing to paste

# Create the GUI window
root = tk.Tk()
root.title("Text-to-Speech with Speed Adjustment")

# Make window resizable
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.geometry("400x300")

# Text entry
text_entry = tk.Text(root, wrap=tk.WORD)
text_entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
text_entry.bind("<Button-3>", paste_text)

# Speed slider
speed_slider = ttk.Scale(root, from_=0.5, to=2.0, orient="horizontal", value=1.0)
speed_slider.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=10, pady=5)
speed_slider.bind("<Motion>", lambda event: update_speed(speed_slider.get()))

# Speed label
speed_label = tk.Label(root, text="Speed: 1.00")
speed_label.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

# Play button
play_button = PlayButton(root, text="Play", command=repeat_text)
play_button.grid(row=3, column=0, padx=10, pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_audio)
stop_button.grid(row=3, column=1, padx=10, pady=10)

# Clear Text Box button
clear_button = tk.Button(root, text="Clear Text Box", command=clear_text_box)
clear_button.grid(row=3, column=2, padx=10, pady=10)

# Repeat button
repeat_button = tk.Button(root, text="Repeat", command=repeat_text)
repeat_button.grid(row=3, column=3, padx=10, pady=10)

# Initialize current speed
current_speed = 1.0

# Keep window on top
root.attributes('-topmost', True)

# Run the GUI event loop
root.mainloop()
