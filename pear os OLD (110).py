def open_about(e=None):
    t = create_window('About')
    if t: 
        # Updated text to include "by mark"
        canvas.create_text(650, 380, 
                           text='Pear OS Frutiger Edition\n2026 Simulation Core\nBuilt With Python + Tkinter by mark', 
                           justify='center', font=('Segoe UI', 18), tags=t)