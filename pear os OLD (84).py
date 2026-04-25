# Update these sections in your unified script:

# 1. Update the Colors section to include a 'current_theme'
current_theme = {
    'bg_top': '#3399ff',
    'bg_bottom': '#44dd44',
    'taskbar': 'white'
}

# 2. Replace the open_settings function with this version:
def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if not t: return

    canvas.create_text(320, 220, text='Personalization', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    
    # --- Theme Toggle ---
    def set_theme(mode):
        global current_theme
        if mode == "Aero":
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else:
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#333333', 'taskbar': '#444444'}
        desktop() # Refresh desktop to apply colors

    canvas.create_text(320, 260, text="Desktop Theme:", font=('Segoe UI', 10), anchor='w', tags=t)
    
    btn_aero = canvas.create_rectangle(320, 280, 420, 310, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(370, 295, text="Aero Blue", tags=t)
    
    btn_dark = canvas.create_rectangle(430, 280, 530, 310, fill='#333333', outline='white', tags=t)
    canvas.create_text(480, 295, text="Night Mode", fill='white', tags=t)

    canvas.tag_bind(btn_aero, '<Button-1>', lambda e: set_theme("Aero"))
    canvas.tag_bind(btn_dark, '<Button-1>', lambda e: set_theme("Dark"))

    # --- System Controls ---
    canvas.create_text(320, 360, text="System Display", font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    
    fs_btn = canvas.create_rectangle(320, 390, 530, 430, fill=aero_blue_light, outline='white', tags=t)
    fs_txt = canvas.create_text(425, 410, text="Toggle Fullscreen (F11)", font=('Segoe UI', 10, 'bold'), tags=t)
    
    canvas.tag_bind(fs_btn, '<Button-1>', toggle_fullscreen)
    canvas.tag_bind(fs_txt, '<Button-1>', toggle_fullscreen)

# 3. Modify the desktop() function to use the current_theme variables:
def desktop():
    canvas.delete('all')
    # Use theme colors for the background gradient
    for i in range(1200):
        c = min(255, 100 + i // 4)
        canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'])

    # Grass Floor/Bottom Gradient
    for i in range(400):
        canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'])

    # Taskbar
    canvas.create_rectangle(280, 760, 1180, 825, fill=current_theme['taskbar'], stipple='gray50', width=2)
    
    # ... rest of the desktop() app loading code remains the same ...