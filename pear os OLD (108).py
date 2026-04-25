def open_about(e=None):
    t = create_window('About')
    if t: 
        # Main Title
        canvas.create_text(650, 350, text='Pear OS Frutiger Edition\n2026 Simulation Core', 
                           justify='center', font=('Segoe UI', 18, 'bold'), tags=t)
        # Credit Line
        canvas.create_text(650, 420, text='Built With Python + Tkinter by mark', 
                           fill='#44dd44', font=('Segoe UI', 14), tags=t)