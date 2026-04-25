# --- Add to your Global State section ---
custom_bg_path = None
bg_image_ref = None  # Prevents garbage collection of the image

# --- Updated Background Engine ---
def draw_background():
    global bg_image_ref
    canvas.delete('bg')
    
    if custom_bg_path:
        try:
            # Open and resize the image to fit the window
            img = Image.open(custom_bg_path)
            img = img.resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_ref = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=bg_image_ref, anchor='nw', tags='bg')
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            draw_default_gradient()
    else:
        draw_default_gradient()

def draw_default_gradient():
    for i in range(1200): 
        canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
    for i in range(400): 
        canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

# --- Updated Settings App ---
def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    canvas.create_rectangle(300, 190, 450, 600, fill='#e0e0e0', outline='', tags=t)
    categories = ["Appearance", "Network", "Privacy", "System"]
    content_tags = f"{t}_content"

    def upload_bg():
        global custom_bg_path
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            custom_bg_path = path
            draw_background()
            redraw_ui_overlay() # Ensure taskbar stays on top
            messagebox.showinfo("Success", "Wallpaper updated!")

    def show_category(cat):
        canvas.delete(content_tags)
        if cat == "Appearance":
            canvas.create_text(470, 230, text="Personalization", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            
            # Theme Buttons
            aero_btn = canvas.create_rectangle(470, 270, 600, 310, fill='#66ccff', outline='white', tags=(t, content_tags))
            canvas.create_text(535, 290, text="Aero Blue", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(aero_btn, '<Button-1>', lambda e: set_theme("Aero"))
            
            dark_btn = canvas.create_rectangle(620, 270, 750, 310, fill='#333333', outline='white', tags=(t, content_tags))
            canvas.create_text(685, 290, text="Dark Mode", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(dark_btn, '<Button-1>', lambda e: set_theme("Dark"))

            # NEW: Custom Background Button
            upload_btn = canvas.create_rectangle(470, 330, 750, 370, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(610, 350, text="Upload Custom Background", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(upload_btn, '<Button-1>', lambda e: upload_bg())

        # ... (rest of categories remain the same)
        elif cat == "Network":
            canvas.create_text(470, 230, text="Network & Internet", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            canvas.create_text(470, 270, text="Wi-Fi: Connected (Gaia_5G)\nVPN: Disconnected", font=('Segoe UI', 11), anchor='nw', tags=(t, content_tags))
        elif cat == "Privacy":
            canvas.create_text(470, 230, text="Privacy & Security", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            audit_btn = canvas.create_rectangle(470, 270, 650, 310, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(560, 290, text="Audit Safety", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(audit_btn, '<Button-1>', lambda e: messagebox.showinfo("Safety", "System audit complete. No threats found."))
        elif cat == "System":
            canvas.create_text(470, 230, text="System Information", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            info = "OS: GaiaSphere 1.0.4\nKernel: PearCore-Py\nResolution: 1400x850"
            canvas.create_text(470, 270, text=info, font=('Segoe UI', 11), anchor='nw', tags=(t, content_tags))

    def set_theme(mode):
        global current_theme, custom_bg_path
        custom_bg_path = None # Reset custom bg when switching themes
        if mode == "Aero": current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else: current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#000000', 'taskbar': '#333333'}
        draw_background(); redraw_ui_overlay(); messagebox.showinfo("Settings", f"Theme: {mode}")

    for i, cat in enumerate(categories):
        btn = canvas.create_text(375, 230 + (i * 50), text=cat, font=('Segoe UI', 12), tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e, c=cat: show_category(c))
    show_category("Appearance")