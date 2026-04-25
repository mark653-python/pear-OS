import tkinter as tk
import random
import webbrowser
import os
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog
import pygame

# ============================================
# INITIALIZATION & THEME
# ============================================
pygame.mixer.init()

root = tk.Tk()
root.title('Pear OS Ultimate GaiaSphere')
root.geometry('1400x850')
root.resizable(False, False)
root.configure(bg='black')

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Colors
aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'
grass_green = '#228822'

# Global State
icon_images = {} 
progress = 0
bubbles = []
open_apps = {}
snake_game_running = True

# ============================================
# RESOURCE LOADER
# ============================================
def load_icon(path, size=(50, 50)):
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# ============================================
# BOOT & LOGIN
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

    canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120), tags='boot_bar')
    canvas.create_text(700, 500, text=msgs[msg_index], fill='white', font=('Segoe UI', 24), tags='boot_bar')

    if progress < 100:
        root.after(60, boot)
    else:
        root.after(500, login)

def login():
    canvas.delete('all')
    for i in range(850):
        c = min(255, 150 + i // 5)
        canvas.create_line(0, i, 1400, i, fill=f'#66cc{c:02x}')

    canvas.create_text(700, 180, text='Syncing To GaiaSphere', font=('Segoe UI', 48, 'bold'), fill='white')
    btn = canvas.create_rectangle(600, 550, 800, 610, fill='white', outline='white')
    txt = canvas.create_text(700, 580, text='Establish Connection', font=('Segoe UI', 16), fill='#333')

    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# ============================================
# DESKTOP ENVIRONMENT
# ============================================
def desktop():
    canvas.delete('all')
    # Aero Gradient Background
    for i in range(850):
        c = min(255, 100 + i // 4)
        canvas.create_line(0, i, 1400, i, fill=f'#3399{c:02x}')

    # Orb Decoration
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50')

    # Grass Floor
    for i in range(250):
        c = min(255, 120 + i // 2)
        canvas.create_line(0, 600+i, 1400, 600+i, fill=f'#{c:02x}dd{c:02x}')

    # Taskbar
    canvas.create_rectangle(280, 760, 1180, 825, fill='white', outline='white', stipple='gray50', width=2)

    apps = [
        ('system.png', '🖥️', 'System', open_sys_info),
        ('browser.png', '🌐', 'PearWeb', open_browser),
        ('finder.png', '📁', 'Finder', lambda e: open_finder(None, '.')),
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
# WINDOW MANAGER & APPS
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '')

    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', tags=tag)
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    canvas.create_rectangle(300, 150, 1000, 190, fill='#44ee44', outline=data_cell_green, stipple='gray75', tags=tag)
    canvas.create_text(650, 170, text=title, fill='white', font=('Segoe UI', 14, 'bold'), tags=tag)
    btn = canvas.create_oval(310, 160, 330, 180, fill='#ff4d4d', outline='white', tags=tag)
    canvas.tag_bind(btn, '<Button-1>', lambda e: close_window(tag, title))
    return tag

def close_window(tag, title):
    global snake_game_running
    canvas.delete(tag)
    open_apps.pop(title, None)
    if 'Snake' in title: snake_game_running = False

def open_music(e=None):
    t = create_window('Core Rhythms')
    if not t: return

    is_playing = [False]
    canvas.create_text(650, 300, text='🎵', font=('Arial', 80), tags=t)
    track_label = canvas.create_text(650, 400, text="No Track Loaded", font=('Segoe UI', 12), fill='#333', tags=t)

    def upload_file():
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            filename = file_path.split('/')[-1]
            canvas.itemconfig(track_label, text=f"Playing: {filename}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            is_playing[0] = True

    def toggle_play():
        if is_playing[0]:
            pygame.mixer.music.pause()
            is_playing[0] = False
        else:
            pygame.mixer.music.unpause()
            is_playing[0] = True

    btn_load = canvas.create_rectangle(520, 450, 620, 490, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(570, 470, text='Load', font=('Segoe UI', 10, 'bold'), tags=t)
    btn_play = canvas.create_rectangle(630, 450, 780, 490, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(705, 470, text='Play / Pause', font=('Segoe UI', 10, 'bold'), tags=t)

    canvas.tag_bind(btn_load, '<Button-1>', lambda e: upload_file())
    canvas.tag_bind(btn_play, '<Button-1>', lambda e: toggle_play())

def open_browser(e=None):
    t = create_window('PearWeb Explorer')
    if t:
        search_var = tk.StringVar()
        canvas.create_text(650, 320, text='PearGLE', fill='#4285F4', font=('Segoe UI', 48, 'bold'), tags=t)
        search_entry = tk.Entry(root, textvariable=search_var, font=('Segoe UI', 14), width=40)
        canvas.create_window(650, 400, window=search_entry, tags=t)
        
        def search(): webbrowser.open(f"https://www.google.com/search?q={search_var.get()}")
        btn = canvas.create_rectangle(580, 440, 720, 480, fill='#f8f9fa', outline='#dadce0', tags=t)
        canvas.create_text(650, 460, text='Pear Search', tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e: search())

# ============================================
# INTEGRATED FINDER (CODE FROM FILE 1)
# ============================================
def open_finder(e=None, path='.'):
    title = f'Finder - {os.path.basename(os.path.abspath(path)) or "Home"}'
    t = create_window(title, '#f9f9f9')
    if not t: return

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
        
        obj = canvas.create_text(x, y, text=icon, font=('Arial', 40), tags=t)
        lbl = canvas.create_text(x, y + 45, text=item[:12], font=('Segoe UI', 8), tags=t)

        def handle_click(p=full_path, folder=is_dir, tag=t, win_title=title):
            if folder:
                close_window(tag, win_title)
                open_finder(None, p)
            else:
                try:
                    os.startfile(p) if hasattr(os, 'startfile') else webbrowser.open(p)
                except Exception:
                    pass

        canvas.tag_bind(obj, '<Button-1>', lambda e, o=obj: canvas.itemconfig(o, fill='#66ccff'))
        canvas.tag_bind(obj, '<Double-Button-1>', lambda e, p=full_path, f=is_dir: handle_click(p, f))

def open_snake(e=None):
    global snake_game_running
    tag = create_window('Snake Sphere', '#000000')
    if not tag: return
    snake_game_running = True
    snake, direction, food = [[650, 350], [640, 350], [630, 350]], 'Right', [700, 400]

    def move():
        nonlocal direction, food
        if not snake_game_running: return
        head = list(snake[0])
        if direction == 'Up': head[1] -= 15
        elif direction == 'Down': head[1] += 15
        elif direction == 'Left': head[0] -= 15
        elif direction == 'Right': head[0] += 15

        if head[0] < 310 or head[0] > 990 or head[1] < 200 or head[1] > 590:
            close_window(tag, 'Snake Sphere'); return

        snake.insert(0, head)
        if abs(head[0]-food[0]) < 15 and abs(head[1]-food[1]) < 15:
            food = [random.randint(350, 950), random.randint(250, 550)]
        else: snake.pop()

        canvas.delete('snake')
        for s in snake: canvas.create_rectangle(s[0], s[1], s[0]+12, s[1]+12, fill=data_cell_green, tags=(tag, 'snake'))
        canvas.create_oval(food[0], food[1], food[0]+12, food[1]+12, fill='#ff4d4d', tags=(tag, 'snake'))
        root.after(100, move)

    root.bind('<w>', lambda e: set_dir('Up'))
    root.bind('<s>', lambda e: set_dir('Down'))
    root.bind('<a>', lambda e: set_dir('Left'))
    root.bind('<d>', lambda e: set_dir('Right'))
    def set_dir(d): nonlocal direction; direction = d
    move()

def open_sys_info(e=None):
    t = create_window('System Diagnostics')
    if t: canvas.create_text(650, 380, text='🍐\nGaiaCore OS v1.0\nMemory: 8GB Pearls\nStatus: Optimal', justify='center', font=('Segoe UI', 18), tags=t)

def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if t: canvas.create_text(400, 250, text='Display: High Gloss\nNetwork: Connected\nUpdate: v1.0 Installed', anchor='w', font=('Segoe UI', 14), tags=t)

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if t:
        log = f'GaiaCore Kernel v1.0.4-release\n[{datetime.now().strftime("%H:%M:%S")}] Connected\n> root@pearos:~# _'
        canvas.create_text(320, 210, text=log, anchor='nw', fill=data_cell_green, font=('Consolas', 12), tags=t)

def open_about(e=None):
    t = create_window('About')
    if t: canvas.create_text(650, 380, text='Pear OS Frutiger Edition\n2026 Simulation Core\nBuilt With Python + Tkinter', justify='center', font=('Segoe UI', 18), tags=t)

# ============================================
# BACKGROUND VISUALS
# ============================================
def init_bubbles():
    global bubbles
    bubbles = []
    for i in range(20):
        b = canvas.create_oval(0, 0, 18, 18, outline='white')
        bubbles.append([b, 100 + i * 65, 750])

def animate_bubbles():
    for b in bubbles:
        item, x, y = b
        y -= 1.5
        if y < 50: y = 780
        canvas.coords(item, x, y, x+18, y+18)
        b[2] = y
    root.after(40, animate_bubbles)

# ============================================
# RUN
# ============================================
boot()
root.mainloop()