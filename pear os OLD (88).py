import tkinter as tk
import random
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog
import pygame  # Added for actual audio playback

# Initialize Pygame Mixer
pygame.mixer.init()

# ... [Keep your existing Pear OS setup code here] ...

def open_music(e=None):
    t = create_window('Core Rhythms')
    if not t: return

    # Track State
    is_playing = False
    
    # UI Elements
    canvas.create_text(650, 300, text='🎵', font=('Arial', 80), tags=t)
    track_label = canvas.create_text(650, 400, text="No Track Loaded", 
                                     font=('Segoe UI', 12), fill='#333', tags=t)

    def upload_file():
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        if file_path:
            filename = file_path.split('/')[-1]
            canvas.itemconfig(track_label, text=f"Loaded: {filename}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            nonlocal is_playing
            is_playing = True

    def toggle_play():
        nonlocal is_playing
        if is_playing:
            pygame.mixer.music.pause()
            is_playing = False
        else:
            pygame.mixer.music.unpause()
            is_playing = True

    # --- Controls ---
    # Load Button
    btn_load = canvas.create_rectangle(520, 450, 620, 490, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(570, 470, text='Load', font=('Segoe UI', 10, 'bold'), tags=t)
    
    # Play/Pause Button
    btn_play = canvas.create_rectangle(630, 450, 780, 490, fill='#66ccff', outline='white', tags=t)
    play_text = canvas.create_text(705, 470, text='Play / Pause', font=('Segoe UI', 10, 'bold'), tags=t)

    # Bindings
    canvas.tag_bind(btn_load, '<Button-1>', lambda e: upload_file())
    canvas.tag_bind(btn_play, '<Button-1>', lambda e: toggle_play())

# ... [Rest of your Pear OS code] ...