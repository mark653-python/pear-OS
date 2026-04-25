# ============================================
# SETTINGS MODULE
# ============================================
def open_settings(e=None):
    t = create_window('Settings', '#f0f2f5')
    if not t: return

    # --- CATEGORY: APPEARANCE (Personalization) ---
    canvas.create_text(320, 220, text='Appearance & Themes', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    
    def choose_custom_bg():
        """Lets the user change background with pictures from the PC"""
        global bg_image_obj
        file_path = filedialog.askopenfilename(
            title="Select Background Image from PC", 
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                img = Image.open(file_path).resize((1400, 850), Image.Resampling.LANCZOS)
                bg_image_obj = ImageTk.PhotoImage(img)
                draw_background()
                messagebox.showinfo("Settings", f"Workspace Wallpaper Applied: {os.path.basename(file_path)}")
            except Exception as err:
                messagebox.showerror("Error", f"Could not load image: {err}")

    # Button: Change Background from PC
    btn_bg = canvas.create_rectangle(320, 250, 520, 290, fill='#ffffff', outline='#cccccc', tags=t)
    canvas.create_text(420, 270, text="🖼️ Pick from PC", font=('Segoe UI', 10), tags=t)
    canvas.tag_bind(btn_bg, '<Button-1>', lambda e: choose_custom_bg())

    # --- CATEGORY: PRIVACY & SECURITY ---
    canvas.create_text(320, 330, text='Privacy & Security (Google Safety)', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    
    def security_audit():
        """Best Practice: Frequent privacy audits"""
        msg = ("Security Audit Recommendations:\n"
               "1. Turn off automatic login.\n"
               "2. Set screen timeout to 5 minutes.\n"
               "3. Manage ad tracking via Google Safety Center.")
        messagebox.showinfo("Google Help + Security", msg)

    btn_sec = canvas.create_rectangle(320, 360, 520, 400, fill='#e8f0fe', outline='#4285f4', tags=t)
    canvas.create_text(420, 380, text="🛡️ Run Security Audit", font=('Segoe UI', 10, 'bold'), fill='#1a73e8', tags=t)
    canvas.tag_bind(btn_sec, '<Button-1>', lambda e: security_audit())

    # --- CATEGORY: SYSTEM PRECEDENCE ---
    canvas.create_text(320, 440, text='Settings Precedence (Logic)', font=('Segoe UI', 12, 'italic'), anchor='w', tags=t)
    precedence_txt = ("Hierarchy: Default > User > Remote > Workspace > Folder > Policy")
    canvas.create_text(320, 470, text=precedence_txt, font=('Consolas', 9), anchor='w', fill='#666', tags=t)