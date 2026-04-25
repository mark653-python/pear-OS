import os  # Required for real file system access

# ... [Keep the rest of your Pear OS code] ...

def open_finder(e=None):
    t = create_window('Finder', '#f9f9f9')
    if not t: return

    # Header
    canvas.create_text(320, 210, text="🏠 Home / Desktop", 
                       font=('Segoe UI', 10, 'bold'), anchor='nw', tags=t)
    
    # Get real files from the current directory
    try:
        files = os.listdir('.') # Lists files in the folder where the script is saved
    except Exception:
        files = ['Documents', 'Pictures', 'Sync_Logs', 'Core_Files'] # Fallback

    # Grid constants
    start_x, start_y = 360, 280
    row_gap, col_gap = 120, 150
    items_per_row = 4

    for i, item in enumerate(files[:12]):  # Limiting to 12 items for the UI grid
        col = i % items_per_row
        row = i // items_per_row
        x = start_x + (col * col_gap)
        y = start_y + (row * row_gap)

        # Determine icon based on file type
        icon = '📄' if '.' in item else '📁'
        
        # Create clickable icon
        obj = canvas.create_text(x, y, text=icon, font=('Arial', 40), tags=t)
        lbl = canvas.create_text(x, y + 45, text=item[:12], font=('Segoe UI', 8), tags=t)

        # Basic "Open" interaction (prints to console or opens file)
        def make_open_func(name=item):
            return lambda e: print(f"Opening: {name}")

        canvas.tag_bind(obj, '<Double-Button-1>', make_open_func())