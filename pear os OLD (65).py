import tkinter as tk
import random
import webbrowser
import os
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
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
snake_game_running = True
catcher_game_running = True

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
    cx, cy = 700, 425
    
    canvas.create_rectangle(cx-250, cy+135, cx+250, cy+170, outline='white', width=2, tags='boot_bar')
    canvas.create_rectangle(cx-248, cy+137, cx-248 + progress * 5, cy+168,
                            fill=data_cell_green, outline='', tags='boot_bar')

    msgs = ['Syncing GaiaSphere...', 'Compiling Aero Core...', 'Loading Desktop...', 'Welcome.']
    msg_index = min(progress // 30, len(msgs)-1)

    canvas.create_text(cx, cy-75, text='🍐', fill='white', font=('Arial', 120), tags='boot_bar')
    canvas.create_text(cx, cy+75, text=msgs[msg_index], fill='white', font=('Segoe UI', 24), tags='boot_bar')

    if progress < 100:
        root.after(60, boot)
    else:
        root.after(500, login)

def login():
    canvas.delete('all')
    for i in range(850):
        c = min(255, 150 + i // 5)
        canvas.create_line(0, i, 2000, i, fill=f'#66cc{c:02x}', tags='login_ui')

    canvas.create_text(700, 180, text='Syncing To GaiaSphere', font=('Segoe UI', 48, 'bold'), fill='white', tags='login_ui')
    btn = canvas.create_rectangle(600, 550, 800, 610, fill='white', outline='white', tags='login_ui')
    txt = canvas.create_text(700, 580, text='Establish Connection', font=('Segoe UI', 16), fill='#333', tags='login_ui')

    canvas.tag_bind(btn, '<Button-1>', lambda e: desktop())
    canvas.tag_bind(txt, '<Button-1>', lambda e: desktop())

# ============================================
# DESKTOP ENVIRONMENT
# ============================================
def draw_background():
    canvas.delete('bg')
    for i in range(1200):
        canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
    for i in range(400):
        canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(220, 760, 1280, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')

    apps = [
        ('system.png', '🖥️', 'System', open_sys_info),
        ('browser.png', '🌐', 'PearWeb', open_browser),
        ('finder.png', '📁', 'Finder', lambda e: open_finder(None, '.')),
        ('music.png', '🎵', 'Music', open_music),
        ('snake.png', '🐍', 'Snake', open_snake),
        ('catcher.png', '🍎', 'Catcher', open_apple_catcher),
        ('terminal.png', '📟', 'Terminal', open_terminal),
        ('settings.png', '⚙️', 'Settings', open_settings),
        ('about.png', '🍐', 'About', open_about)
    ]

    for i, (img_path, emoji, name, func) in enumerate(apps):
        x = 280 + i * 110
        tk_img = load_icon(f"icons/{img_path}")
        if tk_img:
            icon_images[name] = tk_img
            obj = canvas.create_image(x, 792, image=tk_img, tags='ui')
        else:
            obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 38), tags='ui')

        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

def desktop():
    canvas.delete('all')
    draw_background()
    redraw_ui_overlay()
    init_bubbles()
    animate_bubbles()
    root.bind('<Escape>', lambda e: root.destroy())

# ============================================
# WINDOW MANAGER
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
    global snake_game_running, catcher_game_running
    canvas.delete(tag)
    if title in open_apps:
        open_apps.pop(title)
    if 'Snake' in title: 
        snake_game_running = False
    if 'Apple Catcher' in title:
        catcher_game_running = False

# ============================================
# SYSTEM APPS & THEMED CONTENT
# ============================================
def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    
    # Terminal History Log
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for a list of commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    
    # Input Entry Field
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, 
                         insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    
    # Place entry at the bottom of the window
    input_window = canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        
        log.append(f"root@pearos:~$ {cmd}")
        
        # Command Logic
        if cmd == 'help':
            log.append("Available commands: help, ls, date, clear, i-ready, random-dancing")
        elif cmd == 'ls':
            log.append("Applications/  Documents/  Games/  System/  secret_pear_recipe.txt")
        elif cmd == 'date':
            log.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif cmd == 'clear':
            log.clear()
        elif cmd == 'i-ready':
            log.append("Scanning curriculum... All lessons completed. 100% Mastery.")
        elif cmd == 'random-dancing':
            log.append("RANDOM DANCING! 💃🕺")
        else:
            log.append(f"Command not found: {cmd}")
        
        # Refresh display (show last 15 lines)
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")

    cmd_entry.bind('<Return>', process_command)

def open_apple_catcher(e=None):
    global catcher_game_running
    tag = create_window('Apple Catcher',