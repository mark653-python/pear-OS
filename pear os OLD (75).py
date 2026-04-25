import tkinter as tk
import random
import webbrowser  # Added for browser functionality
from datetime import datetime
from PIL import Image, ImageTk

# ============================================
# PEAR OS ULTIMATE GAIASPHERE - CONSOLIDATED
# ============================================

root = tk.Tk()
root.title('Pear OS Ultimate GaiaSphere')
root.geometry('1400x850')
root.resizable(False, False)
root.configure(bg='black')

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# ---------- Theme & Assets ----------
aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'
grass_green = '#228822'

icon_images = {} # Prevents image garbage collection

# ---------- State ----------
progress = 0
bubbles = []
open_apps = {}
snake_game_running = True

# ============================================
# Resource Loader
# ============================================
def load_icon(path, size=(50, 50)):
    """Loads a PNG, resizes it, and returns a Tkinter-compatible image object."""
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        return None

# ============================================
# Boot Loader
# ============================================
def boot():
    global progress
    canvas.delete('boot_bar')
    progress += 4

    canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2, tags='boot_bar')
    canvas.create_rectangle(452, 562, 452 + progress * 5, 593,
                            fill=data_cell_green, outline='', tags='boot_bar')

    msgs = ['Syncing GaiaSphere...', 'Compiling Aero Core...', 'Loading Desktop...', 'Welcome.']
    msg_index = min(progress // 30, len(msgs)-1)

    canvas.create_text(700, 350, text='🍐', fill='white',
                       font=('Arial', 120), tags='boot_bar')
    canvas.create_text(700, 500, text=msgs[msg_index],
                       fill='white', font=('Segoe UI', 24), tags='boot_bar')

    if progress < 100:
        root.after(60, boot)
    else:
        root.after(500, login)

# ============================================
# Login Screen
# ============================================
def login():
    canvas.delete('all')
    for i in range(850):
        c = min(255, 150 + i // 5)
        canvas.create_line(0, i, 1400, i, fill=f'#66cc{c:02x}')

    canvas.create_text(700, 180, text='Syncing To GaiaSphere',
                       font=('Segoe UI', 48, 'bold'), fill='white')

    btn = canvas.create_rectangle(600, 550, 800, 610, fill='white', outline='white')
    txt = canvas.create_text(700, 580, text='Establish Connection', font=('Segoe UI', 16), fill='#333')

    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# ============================================
# Desktop Environment
# ============================================
def desktop():
    canvas.delete('all')
    for i in range(850):
        c = min(255, 100 + i // 4)
        canvas.create_line(0, i, 1400, i, fill=f'#3399{c:02x}')

    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50')

    for i in range(250):
        c = min(255, 120 + i // 2)
        canvas.create_line(0, 600+i, 1400, 600+i, fill=f'#{c:02x}dd{c:02x}')

    canvas.create_rectangle(280, 760, 1180, 825, fill='white', outline='white', stipple='gray50', width=2)

    apps = [
        ('system.png', '🖥️', 'System', open_sys_info),
        ('browser.png', '🌐', 'PearWeb', open_browser),
        ('finder.png', '📁', 'Finder', open_finder),
        ('music.png', '🎵', 'Music', open_music),
        ('snake.png', '🐍', 'Snake', open_snake),
        ('terminal.png', '📟', 'Terminal', open_terminal),
        ('settings.png', '⚙️', 'Settings', open_settings),
        ('about.png', '🍐', 'About', open_about)
    ]

    for i, (img_path, emoji, name, func) in enumerate(apps):
        x = 340 + i * 105
        tk_img = load_icon(f"icons/{img_path}")
        if tk_img:
            icon_images[name] = tk_img
            obj = canvas.create_image(x, 792, image=tk_img)
        else:
            obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 38))

        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9))

    init_bubbles()
    animate_bubbles()
    root.bind('<Escape>', lambda e: root.destroy())

# ============================================
# Window Manager & App Logic
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '')

    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', outline='', tags=tag)
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    canvas.create_rectangle(300, 150, 1000, 190, fill='#44ee44', outline=data_cell_green, stipple='gray75', tags=tag)
    canvas.create_text(650,