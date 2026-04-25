def close_window(tag, title):
    global snake_game_running, catcher_game_running
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)
    
    # NEW: Redraw background to remove dim effect if no apps remain
    draw_background()
    redraw_ui_overlay()
    
    if 'Snake' in title: snake_game_running = False
    if 'Apple Catcher' in title: catcher_game_running = False