from tkinter import filedialog # Add this to your imports

def open_music(e=None):
    t = create_window('Core Rhythms')
    if not t: return

    # State for the current track
    current_track = tk.StringVar(value="No Track Loaded")
    
    # UI Elements
    canvas.create_text(650, 320, text='🎵', font=('Arial', 60), tags=t)
    track_label = canvas.create_text(650, 400, text="Ready to Sync", 
                                     font=('Segoe UI', 14), fill='#333', tags=t)

    def upload_file():
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        if file_path:
            # Extract just the filename from the full path
            filename = file_path.split('/')[-1]
            canvas.itemconfig(track_label, text=f"Now Playing: {filename}")
            # Note: To actually hear the music, you would integrate 'pygame.mixer' here

    # Upload Button
    btn_rect = canvas.create_rectangle(570, 450, 730, 490, fill=data_cell_green, 
                                       outline='white', width=2, tags=t)
    btn_text = canvas.create_text(650, 470, text='Load Local Track', 
                                  fill='black', font=('Segoe UI', 10, 'bold'), tags=t)

    # Bind the upload action
    for item in [btn_rect, btn_text]:
        canvas.tag_bind(item, '<Button-1>', lambda e: upload_file())