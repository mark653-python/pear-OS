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
root.configure(bg='black')

is_fullscreen = False

current_theme = {
    'bg_top': '#3399ff',
    'bg_bottom': '#44dd44',
    'taskbar': 'white'
}

def toggle_fullscreen(e=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    if not is_fullscreen:
        root.geometry('1400x850')

root.bind('<F11>', toggle_fullscreen)

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'

# Global State
icon_images = {} 
progress = 0
bubbles = []
open_apps = {}
snake_game_running = False

# ============================================
# FX MODULES
# ============================================
def shake_window(count=10):
    if count > 0:
        x_shift = random.randint(-10, 10)
        y_shift = random.randint(-10, 10)
        root.geometry(f"+{root.winfo_x() + x_shift}+{root.winfo_y() + y_shift}")
        root.after(50, lambda: shake_window(count - 1))

def play_dance_sound():
    try:
        pygame.mixer.music.load("random_dancing.mp3")
        pygame.mixer.music.play()
    except:
        print("Sound file not found.")

def start_random_dancing(count=20):
    if count > 0:
        colors = ['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00']
        canvas.configure(bg=random.choice(colors))
        shake_window(2)
        root.after(100, lambda: start_random_dancing(count - 1))
    else:
        canvas.configure(bg='black')
        draw_background()

def trigger_dance(e=None):
    play_dance_sound()
    start_random_dancing()

def start_matrix_effect(count=50):
    t_tag = 'PearCommandPrompt'
    if t_tag not in open_apps: return
    chars = "0123456789ABCDEFHIJKLMNOPQRSTUVWXYZ$+-*/=%\"'#&_(),.;:?!"
    for _ in range(15):
        x = random.randint(320, 980)
        y = 200
        drop = canvas.create_text(x, y, text=random.choice(chars), fill='#00ff41', font=('Consolas', 10), tags=(t_tag, 'matrix_drop'))
        def fall(item=drop, x_pos=x, y_pos=y):
            if t_tag not in open_apps: return
            new_y = y_pos + 15
            if new_y < 580:
                canvas.coords(item, x_pos, new_y)
                canvas.itemconfig(item, text=random.choice(chars))
                root.after(50, lambda: fall(item, x_pos, new_y))
            else: canvas.delete(item)
        fall()
    if count > 0: root.after(200, lambda: start_matrix_effect(count - 1))

# ============================================
# APP WINDOW MANAGEMENT
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '').replace('-', '')
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
    if title in open_apps: open_apps.pop(title)
    if 'Snake' in title: snake_game_running = False

# ============================================
# APP MODULES
# ============================================
def open_browser(e=None):
    t = create_window('PearWeb Browser')
    if not t: return
    canvas.create_rectangle(320, 200, 980, 240, fill='#f0f0f0', tags=t)
    url_var = tk.StringVar(value="https://www.icarly.com")
    entry = tk.Entry(root, textvariable=url_var, font=('Segoe UI', 10), borderwidth=0)
    canvas.create_window(650, 220, window=entry, width=640, tags=t)
    canvas.create_text(650, 400, text="Interactive Web Rendering Not Supported\nIn Simulation Mode", font=('Segoe UI', 12), tags=t)

def open_music(e=None):
    t = create_window('Pear Tunes', '#111')
    if not t: return
    canvas.create_text(650, 300, text="🎵 Now Playing: Leave It All To Me", fill='white', font=('Segoe UI', 14), tags=t)
    play_btn = canvas.create_rectangle(600, 450, 700, 490, fill=data_cell_green, tags=t)
    canvas.create_text(650, 470, text="PLAY", font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(play_btn, '<Button-1>', lambda e: play_dance_sound())

def open_finder(e=None, path="."):
    t = create_window('Finder - ' + path)
    if not t: return
    try:
        files = os.listdir(path)[:10]
        for i, f in enumerate(files):
            canvas.create_text(350, 220 + (i*25), text=f"📄 {f}", anchor='nw', font=('Segoe UI', 10), tags=t)
    except:
        canvas.create_text(650, 350, text="Access Denied", tags=t)

def open_snake(e=None):
    global snake_game_running
    t = create_window('iSnake Game', 'black')
    if not t: return
    snake_game_running = True
    canvas.create_text(650, 210, text="Score: 0", fill='white', tags=(t, 'score'))
    # Simplified Snake Logic placeholder
    canvas.create_rectangle(450, 250, 850, 550, outline=data_cell_green, tags=t)
    canvas.create_text(650, 400, text="Use Arrow Keys to Play", fill='white', tags=t)

def open_terminal(e=None):
    t = create_window('Pear Command Prompt', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        log.append(f"root@pearos:~$ {cmd}")
        if cmd == 'help': log.append("Available: help, ls, party, matrix, shake, exit")
        elif cmd == 'ls': log.append("Applications/  Documents/  Games/  System/")
        elif cmd in ['party', 'random-dancing']: trigger_dance()
        elif cmd == 'matrix': start_matrix_effect()
        elif cmd == 'shake': shake_window()
        elif cmd == 'exit': close_window(t, 'Pear Command Prompt'); return
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process_command)

# ============================================
# BOOT & DESKTOP DRAWING
# ============================================
def load_icon(path, size=(50, 50)):
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except: return None

def draw_background():
    canvas.delete('bg')
    for i in range(1200):
        canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
    for i in range(400):
        canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(180, 760, 1220, 825, fill=current_theme['taskbar'], stipple='gray50', width=2, tags='ui')
    
    # Party Button
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    apps = [
        ('🖥️', 'System', lambda e: create_window('System Info')),
        ('🌐', 'PearWeb', open_browser),
        ('📁', 'Finder', lambda e: open_finder(None, '.')),
        ('🎵', 'Music', open_music),
        ('🐍', 'Snake', open_snake),
        ('📟', 'Terminal', open_terminal)
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 350 + i * 140
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 32), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

def desktop():
    canvas.delete('all')
    draw_background()
    redraw_ui_overlay()
    init_bubbles()
    animate_bubbles()

def init_bubbles():
    global bubbles
    bubbles = []
    for i in range(20):
        b = canvas.create_oval(0, 0, 18, 18, outline='white', tags='ui')
        bubbles.append([b, 100 + i * 65, 750])

def animate_bubbles():
    for b in bubbles:
        item, x, y = b
        y -= 1.5
        if y < 50: y = 780
        canvas.coords(item, x, y, x+18, y+18)
        b[2] = y
    root.after(40, animate_bubbles)

# Kickoff
desktop()
root.mainloop()