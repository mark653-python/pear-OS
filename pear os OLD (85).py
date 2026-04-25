def draw_background():
    canvas.delete('bg')
    # If a custom image exists, draw it; otherwise, draw the theme colors
    if bg_image_obj:
        canvas.create_image(700, 425, image=bg_image_obj, tags='bg')
    else:
        for i in range(1200):
            canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
        for i in range(400):
            canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    
    # Keep the Frutiger Aero sphere overlay
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if not t: return
    
    canvas.create_text(320, 220, text='Personalization', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)

    # Function to pick a custom image
    def choose_custom_bg():
        global bg_image_obj
        file_path = filedialog.askopenfilename(title="Select Background", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_obj = ImageTk.PhotoImage(img)
            draw_background()
            canvas.tag_lower('bg') # Ensure it stays behind apps

    # Theme toggle logic
    def set_theme(mode):
        global current_theme, bg_image_obj
        bg_image_obj = None # Clear custom image when switching back to themes
        if mode == "Aero": 
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else: 
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#333333', 'taskbar': '#444444'}
        draw_background()
        redraw_ui_overlay()
        canvas.tag_lower('bg')

    # UI Buttons
    btn_aero = canvas.create_rectangle(320, 280, 420, 310, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(370, 295, text="Aero Blue", tags=t)
    canvas.tag_bind(btn_aero, '<Button-1>', lambda e: set_theme("Aero"))

    btn_custom = canvas.create_rectangle(440, 280, 560, 310, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(500, 295, text="Custom Image", tags=t)
    canvas.tag_bind(btn_custom, '<Button-1>', lambda e: choose_custom_bg())