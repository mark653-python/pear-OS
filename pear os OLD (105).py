def redraw_ui_overlay():
    # Draws the UI elements without overwriting the custom background
    canvas.create_rectangle(280, 760, 1180, 825, fill=current_theme['taskbar'], stipple='gray50', width=2)
    
    # Note: For a fully clean implementation, you'd move the "App Icons" 
    # logic into its own function so desktop() and pick_background() 
    # can both call it. For now, calling desktop() will reset to 
    # theme colors, so use the "Browse" button to see your custom pic!
    desktop()