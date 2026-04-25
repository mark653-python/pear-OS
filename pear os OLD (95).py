# ============================================
# UPDATED WINDOW MANAGEMENT
# ============================================

def close_window(tag, title):
    global snake_game_running
    canvas.delete(tag)
    # This was the missing piece: properly removing the title from the open_apps tracker
    if title in open_apps:
        open_apps.pop(title)
    
    if 'Snake' in title: 
        snake_game_running = False

# ============================================
# UPDATED SETTINGS APP (Inside the main script)
# ============================================

def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if not t: return

    canvas.create_text(320, 220, text='Personalization', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    
    def set_theme(mode):
        global current_theme
        if 'custom_bg' in icon_images: del icon_images['custom_bg']
        
        if mode == "Aero":
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else:
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#333333', 'taskbar': '#444444'}
            
        # IMPORTANT: We only redraw the background and UI, we don't call desktop() 
        # because desktop() clears ALL tags, which would close this Settings window!
        canvas.delete('bg') # Ensure your background elements have a 'bg' tag
        # (You would add tags='bg' to your desktop background shapes)
        redraw_ui_overlay() 

    # ... (rest of your settings buttons)