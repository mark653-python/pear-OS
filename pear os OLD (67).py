import tkinter as tk

# --- 1. Setup the Main Window ---
root = tk.Tk()
root.title("Pear OS - Frutiger Aero Edition")
root.geometry("1400x850")
root.resizable(False, False)
root.configure(bg='black')

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- Global Variables ---
progress = 0
bubbles = []
app_open = False # Tracks if our fake app is currently open

# --- 2. Fake Boot Sequence ---
logo = canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120))
status = canvas.create_text(700, 500, text='Booting Pear OS...', fill='white', font=('Segoe UI', 28))
bar_bg = canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2)
bar_fill = canvas.create_rectangle(452, 562, 452, 593, fill='#66ff99', outline='')

def boot():
    global progress
    progress += 4
    
    canvas.coords(bar_fill, 452, 562, 452 + progress * 5, 593)

    msgs = [
        'Loading Kernel...',
        'Mounting Pear Drive...',
        'Starting Aero Services...',
        'Loading Desktop...',
        'Welcome.'
    ]
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

    canvas.create_text(700, 180, text='Pear OS', font=('Segoe UI', 56, 'bold'), fill='white')
    canvas.create_oval(560, 260, 840, 540, fill='#d9ff77', outline='white', width=5)
    canvas.create_text(700, 400, text='🍐', font=('Arial', 100))

    canvas.create_rectangle(560, 610, 840, 670, fill='white', outline='#66ccff', width=3)
    canvas.create_text(700, 640, text='Click to Login', font=('Segoe UI', 24, 'bold'), fill='#333333')

    root.bind('<Button-1>', lambda e: desktop())

# --- 4. Frutiger Aero Desktop ---
def desktop():
    root.unbind('<Button-1>')
    canvas.delete('all')

    # Background
    for i in range(850):
        c = min(255, 150 + i // 5)
        color = f'#66cc{c:02x}'
        canvas.create_line(0, i, 1400, i, fill=color)

    canvas.create_oval(-200, 600, 700, 1200, fill='#66ff88', outline='')
    canvas.create_oval(600, 530, 1600, 1200, fill='#88ff99', outline='')

    canvas.create_text(250, 140, text='Pear OS', font=('Segoe UI', 48, 'bold'), fill='white')
    canvas.create_text(700, 50, text='Press Esc to shut down', font=('Segoe UI', 14), fill='white')

    # Desktop Icons
    desktop_icons = [(250, 'Network', '🌎'), (360, 'Recycle', '🗑️')]
    for y, name, icon in desktop_icons:
        canvas.create_text(1280, y, text=icon, font=('Arial', 40))
        canvas.create_text(1280, y + 45, text=name, bg='#7fd8ff', font=('Segoe UI', 12, 'bold'), fill='white')

    # Fake Finder Window (Static)
    canvas.create_rectangle(280, 220, 980, 600, fill='#ddffff', outline='white', width=3)
    canvas.create_rectangle(280, 220, 980, 260, fill='#99ccff', outline='white', width=2)
    canvas.create_text(630, 240, text='Finder', font=('Segoe UI', 16, 'bold'), fill='white')
    
    for i, name in enumerate(['Docs', 'Pics', 'Music', 'Apps']):
        canvas.create_text(420 + i * 130, 410, text='📁', font=('Arial', 46))
        canvas.create_text(420 + i * 130, 460, text=name, font=('Segoe UI', 14))

    # Glassy Dock
    canvas.create_rectangle(350, 760, 1100, 825, fill='white', outline='white', stipple='gray50', width=2)
    icons = ['🖥️', '🌐', '📁', '🎵', '⚙️', '🍐']
    
    for i, v in enumerate(icons):
        # Create the icon and save its ID
        icon_id = canvas.create_text(430 + i * 110, 792, text=v, font=('Arial', 38))
        
        # If it's the globe icon, make it clickable to open the browser
        if v == '🌐':
            canvas.tag_bind(icon_id, '<Button-1>', open_browser)
            canvas.create_text(430 + i * 110, 840, text='Web', font=('Segoe UI', 10), fill='white') # Tiny label

    # Bubbles
    global bubbles
    bubbles = []
    for i in range(8):
        b = canvas.create_oval(0, 0, 20, 20, fill='', outline='white', width=2)
        bubbles.append([b, 100 + i * 150, 700])
    
    animate_bubbles()
    root.bind('<Escape>', lambda e: shutdown())

# --- 5. Interactive App: PearWeb Explorer ---
def open_browser(event):
    global app_open
    if app_open: return # Prevent opening multiple windows
    app_open = True
    
    # We use a specific tag "browser" for all these elements so we can delete them all at once later
    
    # Browser Base
    canvas.create_rectangle(150, 100, 1250, 700, fill='#ffffff', outline='#66ccff', width=4, tags="browser")
    # Title Bar
    canvas.create_rectangle(150, 100, 1250, 140, fill='#80dfff', outline='', tags="browser")
    canvas.create_text(700, 120, text='PearWeb Explorer', font=('Segoe UI', 14, 'bold'), fill='white', tags="browser")
    
    # URL Bar
    canvas.create_rectangle(170, 150, 1150, 180, fill='#e6f9ff', outline='#b3ecff', tags="browser")
    canvas.create_text(180, 165, text='http://www.aero.pear/welcome', font=('Segoe UI', 12), fill='gray', anchor='w', tags="browser")
    
    # Fake Page Content
    canvas.create_text(700, 350, text='Welcome to the Aero Web.', font=('Segoe UI', 42, 'bold'), fill='#0077b3', tags="browser")
    canvas.create_text(700, 420, text='🌍 🦋 🫧 🐬 📱', font=('Arial', 60), tags="browser")
    canvas.create_text(700, 500, text='The internet is vast and glossy.', font=('Segoe UI', 20), fill='#333333', tags="browser")

    # Close Button (Red dot in top left corner like MacOS/PearOS)
    close_btn = canvas.create_oval(165, 110, 185, 130, fill='#ff4d4d', outline='white', width=2, tags="browser")
    
    # Bind the click event on the close button to the close_browser function
    canvas.tag_bind(close_btn, '<Button-1>', close_browser)
    # Add a hover text to the close button
    canvas.create_text(175, 120, text='x', font=('Arial', 10, 'bold'), fill='white', tags="browser")

def close_browser(event):
    global app_open
    app_open = False
    # Delete everything tagged with "browser"
    canvas.delete("browser")

# --- 6. Animations & Shutdown ---
def animate_bubbles():
    try:
        if not bubbles: return 
            
        for b in bubbles:
            item, x, y = b
            y -= 2
            if y < 100: y = 760 
            canvas.coords(item, x, y, x + 20, y + 20)
            b[2] = y
            
        root.after(40, animate_bubbles)
    except tk.TclError:
        pass 

def shutdown():
    global bubbles
    bubbles.clear() 
    root.unbind('<Escape>')
    
    canvas.delete('all')
    canvas.configure(bg='black')
    canvas.create_text(700, 390, text='Shutting Down...', fill='white', font=('Segoe UI', 42))
    canvas.create_text(700, 500, text='🍐', fill='white', font=('Arial', 80))
    
    root.after(3000, root.destroy)

# Start!
boot()
root.mainloop()