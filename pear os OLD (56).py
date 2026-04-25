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
snake_game_running = False
catcher_game_running = False
bg_image_obj = None

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
        pass

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

# ============================================
# SYSTEM APP (UPDATED)
# ============================================
def open_system(e=None):
    t = create_window('System Diagnostics', '#f8f9fa')
    if not t: return

    # Stats section
    canvas.create_text(330, 220, text="Hardware Overview", font=('Segoe UI', 14, 'bold'), anchor='w', fill='#333', tags=t)
    cpu_label = canvas.create_text(330, 255, text="CPU Usage: 0%", font=('Consolas', 11), anchor='w', fill='#555', tags=t)
    ram_label = canvas.create_text(330, 280, text="RAM Load: 0%", font=('Consolas', 11), anchor='w', fill='#555', tags=t)

    def update_stats():
        if t not in open_apps.get('System Diagnostics', ''): 
            # Check if tag still exists in canvas
            if not canvas.find_withtag(t): return
        
        cpu = random.randint(5, 45)
        ram = random.randint(20, 60)
        canvas.itemconfig(cpu_label, text=f"CPU Usage: {cpu}% [||||      ]")
        canvas.itemconfig(ram_label, text=f"RAM Load: {ram}%  [||||||    ]")
        root.after(1500, update_stats)

    update_stats()

    # Functional Buttons
    def purge_temp():
        messagebox.showinfo("System", "Purging temporary GaiaSphere cache...")
        shake_window(5)
        messagebox.showinfo("Success", "1.4 GB cleared!")

    def run_ping():
        messagebox.showinfo("Network", "Pinging iCarly.com servers...\nResponse: 24ms (Stable)")

    # Button 1: Purge
    btn1 = canvas.create_rectangle(330, 350, 500, 390, fill='#ff9966', outline='white', tags=t)
    canvas.create_text(415, 370, text="Purge Temp", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn1, '<Button-1>', lambda e: purge_temp())

    # Button 2: Ping
    btn2 = canvas.create_rectangle(520, 350, 690, 390, fill='#66b3ff', outline='white', tags=t)
    canvas.create_text(605, 370, text="Ping Test", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn2, '<Button-1>', lambda e: run_ping())

    # Button 3: Refresh
    btn3 = canvas.create_rectangle(710, 350, 880, 390, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(795, 370, text="Re-Sync UI", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn3, '<Button-1>', lambda e: redraw_ui_overlay())

# ============================================
# APPS (SNAKE, CATCHER, TERMINAL, ETC.)
# ============================================
# [Functions remain same as previous version...]
def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "Type 'help' for a list of commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()
    def process(event):
        c = cmd_var.get().strip().lower()
        log.append(f"root@pearos:~$ {c}")
        if c == 'help': log.append("help, ls, matrix, shake, party")
        elif c == 'matrix': start_matrix_effect(t)
        elif c == 'shake': shake_window()
        elif c == 'party': trigger_dance()
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)

def start_matrix_effect(t_tag):
    chars = "0123456789ABCDEF"
    for _ in range(10):
        x = random.randint(320, 980)
        drop = canvas.create_text(x, 200, text=random.choice(chars), fill='#00ff41', font=('Consolas', 10), tags=(t_tag, 'matrix'))
        def fall(item=drop, x_pos=x, y_pos=200):
            if not canvas.find_withtag(t_tag): return
            ny = y_pos + 15
            if ny < 580:
                canvas.coords(item, x_pos, ny)
                root.after(50, lambda: fall(item, x_pos, ny))
            else: canvas.delete(item)
        fall()

# ============================================
# DESKTOP ENGINE
# ============================================
def open_about(e=None):
    t = create_window('About')
    if t: 
        text = "pear OS Frutiger Edition 2026\nSimulation Core Built With Python + Tkinter\nby mark"
        canvas.create_text(650, 350, text=text, justify='center', font=('Segoe UI', 18, 'bold'), tags=t)

def draw_background():
    canvas.delete('bg')
    if bg_image_obj:
        canvas.create_image(700, 425, image=bg_image_obj, tags='bg')
    else:
        for i in range(1200):
            canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
        for i in range(400):
            canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(220, 760, 1280, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    apps = [
        ('🖥️', 'System', open_system),
        ('🌐', 'PearWeb', lambda e: messagebox.showinfo("Web", "PearGLE Online")),
        ('📁', 'Finder', lambda e: messagebox.showinfo("Finder", "Accessing GaiaDrive...")),
        ('📟', 'Terminal', open_terminal),
        ('🍐', 'About', open_about)
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 350 + i * 160
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

boot()
root.mainloop()