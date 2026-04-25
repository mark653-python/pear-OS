import tkinter as tk

# --- 1. Setup the Main Window ---
root = tk.Tk()
root.title("Pear OS - Frutiger Aero Edition")
root.geometry("1400x850")
root.resizable(False, False)
root.configure(bg='black')

# Create the canvas where everything will be drawn
canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- Global Variables ---
progress = 0
bubbles = []

# --- 2. Fake Boot Sequence ---
# Initial Boot Screen Elements
logo = canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120))
status = canvas.create_text(700, 500, text='Booting Pear OS...', fill='white', font=('Segoe UI', 28))
bar_bg = canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2)
bar_fill = canvas.create_rectangle(452, 562, 452, 593, fill='#66ff99', outline='')

def boot():
    global progress
    progress += 4
    
    # Update progress bar
    canvas.coords(bar_fill, 452, 562, 452 + progress * 5, 593)

    # Status messages
    msgs = [
        'Loading Kernel...',
        'Mounting Pear Drive...',
        'Starting Aero Services...',
        'Loading Desktop...',
        'Welcome.'
    ]
    # Update text based on progress
    msg_index = min(progress // 20, len(msgs) - 1)
    canvas.itemconfig(status, text=msgs[msg_index])

    if progress < 100:
        root.after(120, boot)
    else:
        root.after(1000, login)

# --- 3. Login Screen ---
def login():
    canvas.delete('all')
    canvas.configure(bg='#7fd8ff')

    # Pear OS Header
    canvas.create_text(700, 180, text='Pear OS', font=('Segoe UI', 56, 'bold'), fill='white')
    
    # User Avatar Area
    canvas.create_oval(560, 260, 840, 540, fill='#d9ff77', outline='white', width=5)
    canvas.create_text(700, 400, text='🍐', font=('Arial', 100))

    # Login Button
    canvas.create_rectangle(560, 610, 840, 670, fill='white', outline='#66ccff', width=3)
    canvas.create_text(700, 640, text='Click to Login', font=('Segoe UI', 24, 'bold'), fill='#333333')

    # Bind click event anywhere to go to desktop
    root.bind('<Button-1>', lambda e: desktop())

# --- 4. Frutiger Aero Desktop ---
def desktop():
    root.unbind('<Button-1>')
    canvas.delete('all')

    # Background: Nature-inspired sky gradient
    for i in range(850):
        c = min(255, 150 + i // 5)
        color = f'#66cc{c:02x}'
        canvas.create_line(0, i, 1400, i, fill=color)

    # Background: Glossy green hills
    canvas.create_oval(-200, 600, 700, 1200, fill='#66ff88', outline='')
    canvas.create_oval(600, 530, 1600, 1200, fill='#88ff99', outline='')

    # Desktop Title
    canvas.create_text(250, 140, text='Pear OS', font=('Segoe UI', 48, 'bold'), fill='white')
    canvas.create_text(700, 50, text='Press Esc to shut down', font=('Segoe UI', 14), fill='white')

    # Desktop Icons (From the first code snippet)
    desktop_icons = [
        (250, 'Network', '🌎'),
        (360, 'Recycle', '🗑️')
    ]
    for y, name, icon in desktop_icons:
        canvas.create_text(1280, y, text=icon, font=('Arial', 40))
        canvas.create_text(1280, y + 45, text=name, bg='#7fd8ff', font=('Segoe UI', 12, 'bold'), fill='white')

    # Fake Finder Window
    # Window Base
    canvas.create_rectangle(280, 220, 980, 600, fill='#ddffff', outline='white', width=3)
    # Window Title Bar
    canvas.create_rectangle(280, 220, 980, 260, fill='#99ccff', outline='white', width=2)
    canvas.create_text(630, 240, text='Finder', font=('Segoe UI', 16, 'bold'), fill='white')

    # Finder Folders
    for i, name in enumerate(['Docs', 'Pics', 'Music', 'Apps']):
        canvas.create_text(420 + i * 130, 410, text='📁', font=('Arial', 46))
        canvas.create_text(420 + i * 130, 460, text=name, font=('Segoe UI', 14))

    # Glassy Dock
    # Note: Tkinter doesn't support true transparency, so we use a stipple to fake "glass"
    canvas.create_rectangle(350, 760, 1100, 825, fill='white', outline='white', stipple='gray50', width=2)
    icons = ['🖥️', '🌐', '📁', '🎵', '⚙️', '🍐']
    for i, v in enumerate(icons):
        canvas.create_text(430 + i * 110, 792, text=v, font=('Arial', 38))

    # --- 5. Floating Bubbles Animation ---
    global bubbles
    bubbles = []
    for i in range(8):
        b = canvas.create_oval(0, 0, 20, 20, fill='', outline='white', width=2)
        bubbles.append([b, 100 + i * 150, 700])
    
    animate_bubbles()

    # Bind Escape key to trigger shutdown
    root.bind('<Escape>', lambda e: shutdown())

def animate_bubbles():
    try:
        if not bubbles: 
            return # Stop animation if bubbles list is empty (shutdown)
            
        for b in bubbles:
            item, x, y = b
            y -= 2 # Move bubble up
            if y < 100:
                y = 760 # Reset to bottom when it floats too high
            canvas.coords(item, x, y, x + 20, y + 20)
            b[2] = y
            
        root.after(40, animate_bubbles)
    except tk.TclError:
        pass # Prevents errors if the window is closed forcefully

# --- 6. Shutdown Sequence ---
def shutdown():
    global bubbles
    bubbles.clear() # Stop the bubble animation loop
    root.unbind('<Escape>')
    
    canvas.delete('all')
    canvas.configure(bg='black')
    canvas.create_text(700, 390, text='Shutting Down...', fill='white', font=('Segoe UI', 42))
    canvas.create_text(700, 500, text='🍐', fill='white', font=('Arial', 80))
    
    # Close the window after 3 seconds
    root.after(3000, root.destroy)

# Start the boot sequence!
boot()

# Run the Tkinter main event loop
root.mainloop()