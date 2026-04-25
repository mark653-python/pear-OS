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
snake_game_running = True

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
        print("Sound file not found, skipping audio.")

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
        drop = canvas.create_text(x, y, text=random.choice(chars), 
                                  fill='#00ff41', font=('Consolas', 10), tags=(t_tag, 'matrix_drop'))
        
        def fall(item=drop, x_pos=x, y_pos=y):
            if t_tag not in open_apps: return
            new_y = y_pos + 15
            if new_y < 580:
                canvas.coords(item, x_pos, new_y)
                canvas.itemconfig(item, text=random.choice(chars))
                root.after(50, lambda: fall(item, x_pos, new_y))
            else:
                canvas.delete(item)
        fall()

    if count > 0:
        root.after(200, lambda: start_matrix_effect(count - 1))

# ============================================
# BOOT & DESKTOP
# ============================================
def load_icon(path, size=(50, 50)):
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        return None

def boot():
    global progress
    canvas.delete('boot_bar')
    progress += 4
    cx, cy = 700, 425
    canvas.create_rectangle(cx-250, cy+135, cx+250, cy+170, outline='white', width=2, tags='boot_bar')
    canvas.create_rectangle(cx-248, cy+137, cx-248 + progress * 5, cy+168, fill=data_cell_green, tags='boot_bar')
    
    msgs = ['Syncing GaiaSphere...', 'Compiling Aero Core...', 'Welcome.']
    msg_index = min(progress // 34, len(msgs)-1)
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
    btn = canvas.create_rectangle(600, 550, 800, 610, fill='white', tags='login_ui')
    txt = canvas.create_text(700, 580, text='Establish Connection', font=('Segoe UI', 16), tags='login_ui')
    canvas.tag_bind(btn, '<Button-1>', lambda e: desktop())
    canvas.tag_bind(txt, '<Button-1>', lambda e: desktop())

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
    
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    apps = [
        ('system.png', '🖥️', 'System', open_sys_info),
        ('icarly.png', '⭐️', 'iCarly', open_icarly),
        ('music.png', '🎵', 'Music', open_music),
        ('terminal.png', '📟', 'Terminal', open_terminal),
        ('about.png', '🍐', 'About', open_about)
    ]

    for i, (img_path, emoji, name, func) in enumerate(apps):
        x = 240 + i * 115
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 38), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

def desktop():
    canvas.delete('all')
    draw_background()
    redraw_ui_overlay()
    init_bubbles()
    animate_bubbles()

# ============================================
# WINDOWS & APPS
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '')
    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', tags=tag)
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    canvas.create_rectangle(300, 150, 1000, 190, fill='#44ee44', stipple='gray75', tags=tag)
    canvas.create_text(650, 170, text=title, fill='white', font=('Segoe UI', 14, 'bold'), tags=tag)
    btn = canvas.create_oval(310, 160, 330, 180, fill='#ff4d4d', outline='white', tags=tag)
    canvas.tag_bind(btn, '<Button-1>', lambda e: close_window(tag, title))
    return tag

def close_window(tag, title):
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)

def open_terminal(e=None):
    t = create_window('Pear Command Prompt', '#1e1e1e')
    if not t: return
    log = ["Pear OS [Version 1.0.4]", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), fill='#00ff41', 
                                  font=('Consolas', 10), anchor='nw', tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='black', fg='white', insertbackground='white', font=('Consolas', 10), borderwidth=0)
    canvas.create_window(650, 570, window=cmd_entry, width=650, tags=t)

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        log.append(f"root@pearos:~$ {cmd}")
        if cmd == 'help': log.append("Available: help, ls, party, matrix, shake, clear, exit")
        elif cmd in ['party', 'random-dancing']: 
            log.append("RANDOM DANCING! 💃🕺")
            trigger_dance()
        elif cmd == 'matrix':
            log.append("Initializing Matrix...")
            start_matrix_effect()
        elif cmd == 'shake':
            log.append("Shaking core...")
            shake_window()
        elif cmd == 'clear': log.clear()
        elif cmd == 'exit': close_window(t, 'Pear Command Prompt'); return
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process_command)

def open_icarly(e=None): webbrowser.open("https://www.google.com/search?q=iCarly+Official+Website")
def open_sys_info(e=None): create_window('System Information')
def open_music(e=None): create_window('Core Rhythms')
def open_about(e=None):
    t = create_window('About')
    if t:
        canvas.create_text(650, 350, text='Pear OS Frutiger Edition\n2026 Simulation Core', justify='center', font=('Segoe UI', 18, 'bold'), tags=t)

def init_bubbles():
    global bubbles
    for i in range(20):
        b = canvas.create_oval(0, 0, 18, 18, outline='white', tags='ui')
        bubbles.append([b, 100 + i * 65, 750])

def animate_bubbles():
    for b_data in bubbles:
        b_data[2] -= random.randint(1, 3)
        if b_data[2] < -20: b_data[2] = 870
        canvas.coords(b_data[0], b_data[1], b_data[2], b_data[1]+15, b_data[2]+15)
    root.after(50, animate_bubbles)

boot()
root.mainloop()