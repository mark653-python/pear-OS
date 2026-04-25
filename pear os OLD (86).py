def open_finder(e=None, path='.'):
    # If the window is already open, we refresh it instead of creating a new one
    t = create_window(f'Finder - {os.path.basename(os.path.abspath(path)) or "Home"}', '#f9f9f9')
    if not t: 
        # Logic to refresh existing window if needed could go here
        return

    # Breadcrumb Header
    canvas.create_text(320, 210, text=f"🏠 {os.path.abspath(path)}", 
                       font=('Segoe UI', 10, 'bold'), anchor='nw', tags=t)
    
    try:
        files = os.listdir(path)
    except Exception as err:
        files = [f"Error: {err}"]

    # Grid constants
    start_x, start_y = 360, 280
    row_gap, col_gap = 120, 150
    items_per_row = 4

    for i, item in enumerate(files[:12]):
        col = i % items_per_row
        row = i // items_per_row
        x = start_x + (col * col_gap)
        y = start_y + (row * row_gap)

        full_path = os.path.join(path, item)
        is_dir = os.path.isdir(full_path)
        icon = '📁' if is_dir else '📄'
        
        # Create visual item
        obj = canvas.create_text(x, y, text=icon, font=('Arial', 40), tags=t)
        lbl = canvas.create_text(x, y + 45, text=item[:12], font=('Segoe UI', 8), tags=t)

        # Functional click logic
        def handle_click(p=full_path, name=item, folder=is_dir, tag=t):
            if folder:
                # Close current and open new path
                close_window(tag, f'Finder - {os.path.basename(os.path.abspath(path)) or "Home"}')
                open_finder(None, p)
            else:
                print(f"Executing/Opening: {name}")
                # Try to open the file with the system default handler
                try:
                    os.startfile(p) if hasattr(os, 'startfile') else webbrowser.open(p)
                except Exception as e:
                    print(f"Could not open file: {e}")

        # Bind Single Click for selection (visual feedback) and Double Click to Open
        canvas.tag_bind(obj, '<Button-1>', lambda e, o=obj: canvas.itemconfig(o, fill='#66ccff'))
        canvas.tag_bind(obj, '<Double-Button-1>', lambda e: handle_click())