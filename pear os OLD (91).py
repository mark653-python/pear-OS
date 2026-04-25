# ============================================
# SETTINGS APP
# ============================================
def open_settings(e=None):
    t = create_window('System Settings', '#eeeeee')
    if not t: return

    canvas.create_text(330, 220, text="Personalization", font=('Segoe UI', 16, 'bold'), anchor='w', fill='#333', tags=t)
    
    # Theme Toggle Logic
    def set_theme(mode):
        global current_theme
        if mode == "Aero":
            current_theme['bg_top'] = '#3399ff'
            current_theme['bg_bottom'] = '#44dd44'
            current_theme['taskbar'] = 'white'
        else: # Dark Mode
            current_theme['bg_top'] = '#1a1a1a'
            current_theme['bg_bottom'] = '#000000'
            current_theme['taskbar'] = '#333333'
        
        draw_background()
        redraw_ui_overlay()
        messagebox.showinfo("Settings", f"Theme updated to {mode}!")

    # UI Buttons for Settings
    aero_btn = canvas.create_rectangle(330, 260, 480, 300, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(405, 280, text="Aero Blue", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(aero_btn, '<Button-1>', lambda e: set_theme("Aero"))

    dark_btn = canvas.create_rectangle(500, 260, 650, 300, fill='#333333', outline='white', tags=t)
    canvas.create_text(575, 280, text="Dark Mode", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(dark_btn, '<Button-1>', lambda e: set_theme("Dark"))

    # Wallpaper Info
    canvas.create_text(330, 340, text="System Info", font=('Segoe UI', 16, 'bold'), anchor='w', fill='#333', tags=t)
    canvas.create_text(330, 370, text="OS Version: GaiaSphere 1.0.4\nResolution: 1400x850\nKernel: PearCore-Py", 
                       font=('Segoe UI', 11), anchor='nw', fill='#555', tags=t)