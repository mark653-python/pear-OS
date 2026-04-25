import tkinter as tk
import random
from datetime import datetime

# ============================================
# PEAR OS ULTIMATE GAIASPHERE - MERGED EDITION
# ============================================

root = tk.Tk()
root.title('Pear OS Ultimate GaiaSphere Bootable Simulation')
root.geometry('1400x850')
root.resizable(False, False)
root.configure(bg='black')

canvas = tk.Canvas(
    root,
    width=1400,
    height=850,
    bg='black',
    highlightthickness=0
)
canvas.pack(fill='both', expand=True)

# ---------- Theme ----------
aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'
grass_green = '#228822'

# ---------- State ----------
progress = 0
bubbles = []
open_apps = {}
snake_game_running = False

# ============================================
# Boot Loader
# ============================================
def boot():
    global progress
    canvas.delete('boot_bar')
    progress += 4
    canvas.create_rectangle(
        450, 560, 950, 595,
        outline='white',
        width=2,
        tags='boot_bar'
    )
    canvas.create_rectangle(
        452,
        562,
        452 + progress * 5,
        593,
        fill=data_cell_green,
        outline='',
        tags='boot_bar'
    )
    
    msgs = [
        'Syncing GaiaSphere...',
        'Compiling Aero Core...',
        'Loading Desktop...',
        'Welcome.'
    ]
    
    msg_index = min(progress // 30, len(msgs)-1)
    canvas.create_text(
        700,
        350,
        text='🍐',
        fill='white',
        font=('Arial', 120),
        tags='boot_bar'
    )
    canvas.create_text(
        700,
        500,
        text=msgs[msg_index],
        fill='white',
        font=('Segoe UI', 24),
        tags='boot_bar'
    )
    
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
    
    canvas.create_text(
        700,
        180,
        text='Syncing To GaiaSphere',
        font=('Segoe UI', 48, 'bold'),
        fill='white'
    )
    
    btn = canvas.create_rectangle(
        600, 550, 800, 610,
        fill='white',
        outline='white'
    )
    txt = canvas.create_text(
        700,
        580,
        text='Establish Connection',
        font=('Segoe UI', 16),
        fill='#333'
    )
    
    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# ============================================
# Desktop
# ============================================
def desktop():
    canvas.delete('all')
    for i in range(850):
        c = min(255, 100 + i // 4)
        canvas.create_line(0, i, 1400, i, fill=f'#3399{c:02x}')
        
    canvas.create_oval(
        300, 100, 1100, 700,
        fill='#33ccff',
        outline=aero_blue_light,
        width=3,
        stipple='gray50'
    )
    
    for i in range(250):
        c = min(255, 120 + i // 2)
        canvas.create_line(0, 600 + i, 1400, 600 + i, fill=f'#{c:02x}dd{c:02x}')
        
    canvas.create_rectangle(
        280, 760, 1180, 825,
        fill='white',
        outline='white',
        stipple='gray50',
        width=2
    )
    
    apps = [
      ('🖥️', 'System', open_sys_info),
      ('🌐', 'PearWeb', open_browser),
      ('📁', 'Finder', open_finder),
      ('🎵', 'Music', open_music),
      ('🐍', 'Snake', open_snake),
      ('📟', 'Terminal', open_terminal),
      ('⚙️', 'Settings', open_settings),
      ('🍐', 'About', open_about)
    ]
    
    for i, (icon, name, func) in enumerate(apps):
        x = 340 + i * 105
        obj = canvas.create_text(x, 792, text=icon, font=('Arial', 38))
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9))
        
    global bubbles
    bubbles = []
    for i in range(20):
        b = canvas.create_oval(0, 0, 18, 18, outline='white')
        bubbles.append([b, 100 + i * 65, 750])
        
    animate_bubbles()
    root.bind('<Escape>', lambda e: root.destroy())

# ============================================
# Window Manager
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps:
        return None
    open_apps[title] = True
    tag = title.replace(' ', '')
    
    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', outline='', tags=tag)
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    canvas.create_rectangle(300, 150, 1000, 190, fill='#44ee44', outline=data_cell_green, stipple='gray75', tags=tag)
    
    canvas.create_text(650, 170, text=title, fill='white', font=('Segoe UI', 14, 'bold'), tags=tag)
    
    btn = canvas.create_oval(310, 160, 330, 180, fill='#ff4d4d', outline='white', tags=tag)
    canvas.tag_bind(btn, '<Button-1>', lambda e: close_window(tag, title))
    return tag

def close_window(tag, title):
    global snake_game_running
    canvas.delete(tag)
    if title in open_apps:
        del open_apps[title]
    if title == 'Snake Sphere':
        snake_game_running = False

# ============================================
# Apps
# ============================================
def open_browser(e=None):
    t = create_window('PearWeb Explorer')
    if t:
        canvas.create_text(650, 250, text='://gaiasphere.feed', fill=grass_green, font=('Courier New', 14), tags=t)
        canvas.create_text(650, 400, text='Welcome To The Glossy Web\n🌍 🫧 🐬', font=('Segoe UI', 30), justify='center', tags=t)

def open_finder(e=None):
    t = create_window('Finder', '#ddffff')
    if t:
        folders = ['Documents', 'Pictures', 'Sync_Logs', 'Core_Files']
        for i, f in enumerate(folders):
            x = 450 + (i % 2) * 250
            y = 300 + (i // 2) * 150
            canvas.create_text(x, y, text='📁', font=('Arial', 50), tags=t)
            canvas.create_text(x, y + 50, text=f, tags=t)

def open_music(e=None):
    t = create_window('Core Rhythms')
    if t:
        canvas.create_text(650, 350, text='Now Syncing: Aero Dreams.mp3', font=('Segoe UI', 18), tags=t)
        canvas.create_rectangle(450, 450, 850, 465, fill='#eee', tags=t)
        canvas.create_rectangle(450, 450, 700, 465, fill=data_cell_green, tags=t)

def open_sys_info(e=None):
    t = create_window('System Diagnostics')
    if t:
        canvas.create_text(650, 380, text='🍐\nGaiaCore OS v1.0\nMemory: 8GB Pearls\nStatus: Optimal', justify='center', font=('Segoe UI', 18), tags=t)

def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if t:
        canvas.create_text(400, 250, text='Display: High Gloss\nNetwork: Connected\nUpdate: v1.0 Installed', anchor='w', font=('Segoe UI', 14), tags=t)

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if t:
        log = (
            'GaiaCore Kernel v1.0.4-release\n'
            f'[{datetime.now().strftime("%H:%M:%S")}] Connected\n'
            '> root@pearos:~# _'
        )
        canvas.create_text(320, 210, text=log, anchor='nw', fill=data_cell_green, font=('Consolas', 12), tags=t)

def open_about(e=None):
    t = create_window('About')
    if t:
        canvas.create_text(650, 380, text='Pear OS Frutiger Edition\n2026 Simulation Core\nBuilt With Python + Tkinter', justify='center', font=('Segoe UI', 18), tags=t)

# ============================================
# Snake Game
# ============================================
def open_snake(e=None):
    global snake_game_running
    tag = create_window('Snake Sphere', '#000000')
    if not tag: return
    snake_game_running = True
    snake = [[650, 350], [640, 350], [630, 350]]
    direction = 'Right'
    food = [700, 400]

    def move_snake():
        nonlocal direction, food
        if not snake_game_running: return
        head = list(snake[0])
        if direction == 'Right': head[0] += 15
        elif direction == 'Left': head[0] -= 15
        elif direction == 'Up': head[1] -= 15
        elif direction == 'Down': head[1] += 15
        
        if (head[0] < 310 or head[0] > 990 or head[1] < 200 or head[1] > 590):
            close_window(tag, 'Snake Sphere')
            return
            
        snake.insert(0, head)
        if abs(head[0] - food[0]) < 15 and abs(head[1] - food[1]) < 15:
            food = [random.randint(350, 950), random.randint(250, 550)]
        else:
            snake.pop()
            
        canvas.delete('snake_p')
        for seg in snake:
            canvas.create_rectangle(seg[0], seg[1], seg[0] + 12, seg[1] + 12, fill=data_cell_green, tags=(tag, 'snake_p'))
        canvas.create_oval(food[0], food[1], food[0] + 12, food[1] + 12, fill='#ff4d4d', tags=(tag, 'snake_p'))
        root.after(100, move_snake)

    def set_dir(d):
        nonlocal direction
        direction = d
        
    root.bind('<w>', lambda e: set_dir('Up'))
    root.bind('<s>', lambda e: set_dir('Down'))
    root.bind('<a>', lambda e: set_dir('Left'))
    root.bind('<d>', lambda e: set_dir('Right'))
    move_snake()

# ============================================
# Bubble Animation
# ============================================
def animate_bubbles():
    for b in bubbles:
        item, x, y = b
        y -= 1.5
        if y < 50: y = 780
        canvas.coords(item, x, y, x + 18, y + 18)
        b[2] = y
    root.after(40, animate_bubbles)

# ============================================
# Start System
# ============================================
boot()
root.mainloop()