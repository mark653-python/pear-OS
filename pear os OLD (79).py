# ============================================
# UPDATED SETTINGS & BACKGROUND ENGINE
# ============================================

def draw_background():
    global bg_image_ref
    canvas.delete('bg')
    
    # 1. Draw the actual background (Custom or Gradient)
    if custom_bg_path:
        try:
            img = Image.open(custom_bg_path)
            img = img.resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_ref = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=bg_image_ref, anchor='nw', tags='bg')
        except:
            draw_default_gradient()
    else:
        draw_default_gradient()

    # 2. Dimming Logic - Only dim if other apps are open, 
    # but don't let it lock the Settings window
    if len(open_apps) > 0:
        canvas.create_rectangle(0, 0, 1400, 850, fill='black', stipple='gray50', tags='bg')

def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    
    canvas.create_rectangle(300, 190, 450, 600, fill='#e0e0e0', outline='', tags=t)
    categories = ["Appearance", "Network", "Privacy", "System"]
    content_tags = f"{t}_content"

    def upload_bg():
        global custom_bg_path
        # The dialog used to hang because the canvas was 
        # trying to update while this was open
        path = filedialog.askopenfilename(
            parent=root,
            title="Select Wallpaper",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if path:
            custom_bg_path = path
            # Update background and then lift the settings window back to the top
            draw_background()
            canvas.tag_raise(t) 
            redraw_ui_overlay() 
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

            # Fix: Added a proper button call for the upload
            upload_btn = canvas.create_rectangle(470, 330, 750, 370, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(610, 350, text="Update Wallpaper", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(upload_btn, '<Button-1>', lambda e: upload_bg())
        
        # ... (rest of the categories stay the same)