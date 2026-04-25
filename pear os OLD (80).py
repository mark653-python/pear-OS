def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if not t: return

    canvas.create_text(320, 220, text='Personalization', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    
    # --- Theme Section ---
    def set_theme(mode):
        global current_theme
        if mode == "Aero":
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else:
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#333333', 'taskbar': '#444444'}
        desktop() 

    canvas.create_text(320, 260, text="Color Presets:", font=('Segoe UI', 10), anchor='w', tags=t)
    btn_aero = canvas.create_rectangle(320, 280, 420, 310, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(370, 295, text="Aero Blue", tags=t)
    btn_dark = canvas.create_rectangle(430, 280, 530, 310, fill='#333333', outline='white', tags=t)
    canvas.create_text(480, 295, text="Night Mode", fill='white', tags=t)

    canvas.tag_bind(btn_aero, '<Button-1>', lambda e: set_theme("Aero"))
    canvas.tag_bind(btn_dark, '<Button-1>', lambda e: set_theme("Dark"))

    # --- NEW: Custom Background Section ---
    canvas.create_text(320, 340, text="Custom Wallpaper:", font=('Segoe UI', 10), anchor='w', tags=t)
    
    def pick_background():
        file_path = filedialog.askopenfilename(
            title="Select Wallpaper", 
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                # Load and resize image to fit screen
                img = Image.open(file_path)
                img = img.resize((1400, 850), Image.Resampling.LANCZOS)
                bg_img = ImageTk.PhotoImage(img)
                
                # Store in icon_images to prevent garbage collection
                icon_images['custom_bg'] = bg_img
                
                # Apply to desktop
                canvas.delete('all') # Clear current desktop
                canvas.create_image(700, 425, image=bg_img)
                
                # Re-draw the UI elements (taskbar, icons, etc)
                # We call a simplified version of desktop() logic here
                # or modify desktop() to check for custom_bg
                redraw_ui_overlay() 
            except Exception as ex:
                print(f"Error loading background: {ex}")

    btn_bg = canvas.create_rectangle(320, 360, 530, 390, fill='#eeeeee', outline='#cccccc', tags=t)
    canvas.create_text(425, 375, text="Browse for Image...", font=('Segoe UI', 9), tags=t)
    canvas.tag_bind(btn_bg, '<Button-1>', lambda e: pick_background())

    # --- Display Section ---
    canvas.create_text(320, 430, text="System Display", font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    fs_btn = canvas.create_rectangle(320, 460, 530, 500, fill=aero_blue_light, outline='white', tags=t)
    fs_txt = canvas.create_text(425, 480, text="Toggle Fullscreen (F11)", font=('Segoe UI', 10, 'bold'), tags=t)
    
    canvas.tag_bind(fs_btn, '<Button-1>', toggle_fullscreen)
    canvas.tag_bind(fs_txt, '<Button-1>', toggle_fullscreen)