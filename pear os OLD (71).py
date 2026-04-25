import tkinter as tk

# --- 1. Setup the Main Window ---
root = tk.Tk()
root.title("Pear OS - Interactive Edition")
root.geometry("1400x850")
root.resizable(False, False)
root.configure(bg='black')

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- Global Variables ---
progress = 0
bubbles = []
open_apps = {}  # Tracks open app windows

# --- 2. Boot & Login (Skip for brevity or keep for vibe) ---
logo = canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120))
status = canvas.create_text(700, 500, text='Booting Pear OS...', fill='white', font=('Segoe UI', 28))
bar_bg = canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2)
bar_fill = canvas.create_rectangle(452, 562, 452, 593, fill='#66ff99', outline='')

def boot():
    global progress
    progress += 5
    canvas.coords(bar_fill, 452, 562, 452 + progress * 5, 593)
    if progress < 100:
        root.after(50, boot)
    else:
        login()

def login():
    canvas.delete('all')
    canvas.configure(bg='#7fd8ff')
    canvas.create_text(700, 180, text='Pear OS', font=('Segoe UI', 56, 'bold'), fill='white')
    btn = canvas.create_rectangle(600, 600, 800, 660, fill='white', outline='white', width=2)
    txt = canvas.create_text(700, 630, text='Login', font=('Segoe UI', 20), fill='#333')
    
    # Make login button clickable
    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# --- 3. Desktop Management ---
def desktop():
    canvas.delete('all')
    # Background Gradient
    for i in range(850):
        c = min(255, 150 + i // 5)
        canvas.create_line(0, i, 1400, i, fill=f'#66cc{c:02x}')
    
    # Glassy Dock
    canvas.create_rectangle(350, 760, 1100, 825, fill='white', outline='white', stipple='gray50')
    
    # App definitions: (Icon, Name, Function)
    apps = [
        ('🖥️', 'System', open_sys_info),
        ('🌐', 'PearWeb', open_browser),
        ('📁', 'Finder', open_finder),
        ('🎵', 'Music', open_music),
        ('⚙️', 'Settings', open_settings),
        ('🍐', 'About', open_about)
    ]
    
    for i, (icon, name, func) in enumerate(apps):
        x = 430 + i * 110
        item = canvas.create_text(x, 792, text=icon, font=('Arial', 38))
        canvas.tag_bind(item, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, font=('Segoe UI', 9), fill='white')

    # Start bubbles
    global bubbles
    for i in range(10):
        b = canvas.create_oval(0, 0, 15, 15, outline='white')
        bubbles.append([b, 100 + i * 130, 800])
    animate_bubbles()
    root.bind('<Escape>', lambda e: root.destroy())

# --- 4. Windowing System ---
def create_window(title, color="#ffffff"):
    if title in open_apps: return
    open_apps[title] = True
    
    tag = title.replace(" ", "")
    # Shadow/Border
    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', outline='', tags=tag)
    # Main Body
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    # Header
    canvas.create_rectangle(300, 150, 1000, 190, fill='#99ccff', outline='white', tags=tag)
    canvas.create_text(650, 170, text=title, font=('Segoe UI', 14, 'bold'), fill='white', tags=tag)
    
    # Close Button
    close = canvas.create_oval(310, 160, 330, 180, fill='#ff4d4d', outline='white', tags=tag)
    canvas.tag_bind(close, '<Button-1>', lambda e: close_window(tag, title))
    
    return tag

def close_window(tag, title):
    canvas.delete(tag)
    if title in open_apps: del open_apps[title]

# --- 5. The "Apps" ---
def open_browser(e):
    tag = create_window("PearWeb Explorer")
    if not tag: return
    canvas.create_text(650, 350, text="Welcome to the Web", font=('Segoe UI', 30), fill='#0077b3', tags=tag)
    canvas.create_rectangle(350, 210, 950, 240, fill='#f0f0f0', outline='#ccc', tags=tag)
    canvas.create_text(360, 225, text="http://pear.aero/home", anchor='w', tags=tag)

def open_finder(e):
    tag = create_window("Finder", "#ddffff")
    if not tag: return
    folders = ['Documents', 'Pictures', 'Downloads', 'Work']
    for i, f in enumerate(folders):
        x = 400 + (i % 2) * 250
        y = 300 + (i // 2) * 150
        canvas.create_text(x, y, text='📁', font=('Arial', 50), tags=tag)
        canvas.create_text(x, y+50, text=f, font=('Segoe UI', 12), tags=tag)

def open_music(e):
    tag = create_window("PearMusic")
    if not tag: return
    canvas.create_text(650, 300, text="Now Playing: Aero Dreams", font=('Segoe UI', 18), tags=tag)
    canvas.create_rectangle(450, 450, 850, 460, fill='#eee', outline='#bbb', tags=tag)
    canvas.create_rectangle(450, 450, 600, 460, fill='#66ff99', outline='', tags=tag) # Progress

def open_settings(e):
    tag = create_window("Settings", "#f5f5f5")
    if not tag: return
    canvas.create_text(450, 250, text="Display Settings", font=('Segoe UI', 14, 'bold'), anchor='w', tags=tag)
    canvas.create_text(450, 300, text="Network: Connected (PearAir)", font=('Segoe UI', 12), anchor='w', tags=tag)

def open_sys_info(e):
    tag = create_window("System Info")
    if not tag: return
    canvas.create_text(650, 380, text="🍐\nPear OS v1.0\nMemory: 8192 MB\nProcessor: P1 Chip", 
                      font=('Segoe UI', 16), justify='center', tags=tag)

def open_about(e):
    tag = create_window("About This OS")
    if not tag: return
    canvas.create_text(650, 380, text="Frutiger Aero Aesthetic\nBuilt with Python & Tkinter\n2026", 
                      justify='center', tags=tag)

# --- 6. Final Animation Logic ---
def animate_bubbles():
    for b in bubbles:
        item, x, y = b
        y -= 1
        if y < 50: y = 800
        canvas.coords(item, x, y, x+15, y+15)
        b[2] = y
    root.after(50, animate_bubbles)

boot()
root.mainloop()