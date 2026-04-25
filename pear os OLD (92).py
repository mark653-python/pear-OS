import webbrowser  # Add this to your imports at the very top

def open_browser(e=None):
    t = create_window('PearWeb Explorer')
    if t:
        # URL Bar area
        canvas.create_text(650, 220, text='https://www.google.pear', 
                           fill=grass_green, font=('Courier New', 12), tags=t)
        
        # Logo
        canvas.create_text(650, 320, text='PearGLE', 
                           fill='#4285F4', font=('Segoe UI', 48, 'bold'), tags=t)
        
        # Create a search entry (input box)
        search_var = tk.StringVar()
        search_entry = tk.Entry(root, textvariable=search_var, font=('Segoe UI', 14),
                                width=40, bd=0, highlightthickness=1)
        
        # We must place the entry on the canvas using a window object
        search_window = canvas.create_window(650, 400, window=search_entry, tags=t)

        def perform_search():
            query = search_var.get()
            if query:
                # This opens the user's ACTUAL web browser to a google search
                webbrowser.open(f"https://www.google.com/search?q={query}")

        # Search Button
        btn_rect = canvas.create_rectangle(580, 440, 720, 480, fill='#f8f9fa', outline='#dadce0', tags=t)
        btn_text = canvas.create_text(650, 460, text='Pear Search', fill='#3c4043', font=('Segoe UI', 10), tags=t)

        # Bind search action
        for item in [btn_rect, btn_text]:
            canvas.tag_bind(item, '<Button-1>', lambda e: perform_search())
        
        # Allow pressing "Enter" to search
        search_entry.bind('<Return>', lambda e: perform_search())