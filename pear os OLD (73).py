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
current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}

def toggle_fullscreen(e=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

root.bind('<F11>', toggle_fullscreen)
canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'

# Global State
progress = 0
open_apps = {}
bg_image_obj = None 

# ============================================
# CORE ENGINE: WINDOW MANAGEMENT
# ============================================
def create_window(title, bg='#ffffff'):
    if title in open_apps: return None
    
    # Window Group Tag
    t = f"win_{random.randint(1000,9999)}"
    open_apps[title] = t
    
    # Window Shadow & Body
    canvas.create_rectangle(305, 205, 1005, 605, fill='black', stipple='gray25', tags=t) # Shadow
    canvas.create_rectangle(300, 200, 1000, 600, fill=bg, outline=aero_blue_light, width=2, tags=t)
    
    # Title Bar
    canvas.create_rectangle(300, 200, 1000, 240, fill=aero_blue_light, outline='', tags=t)
    canvas.create_text(315, 220, text=title, anchor='w', font=('Segoe UI', 12, 'bold'), fill='white', tags=t)
    
    # Close Button
    close_btn = canvas.create_oval(970, 210, 990, 230, fill='#ff5555', outline='white', tags=t)
    canvas.tag_bind(close_btn, '<Button-1>', lambda e: close_window(title, t))
    
    return t

def close_window(title, tag):
    canvas.delete(tag)
    if title in open_apps: del open_apps[title]

# ============================================
# APPS & TERMINAL
# ============================================
def open_about(e=None):
    t = create_window('About')
    if t:
        about_txt = "Pear OS Frutiger Edition 2026\nSimulation Core Built With Python\nby mark"
        canvas.create_text(650, 400, text=about_txt, justify='center', font=('Segoe UI', 18, 'bold'), tags=t)

def open_terminal(e=None):
    t = create_window('Pear Command Prompt', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 250, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, insertbackground=data_cell_green, borderwidth=0)
    canvas.create_window(650, 580, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if cmd == 'help': log.append("help, ls, whoami, clear")
        elif cmd == 'whoami': log.append("mark - Administrator")
        elif cmd == 'ls': log.append("Applications/ Documents/ System/")
        elif cmd == 'clear': log.clear()
        else: log.append(f"Unknown command: {cmd}")
        canvas.itemconfig(log_text, text="\n".join(log[-12:]))
        cmd_var.set("")

    cmd_entry.bind('<Return>', process_command)

# ============================================
# BOOT & LOGIN
# ============================================
def boot():
    global progress
    canvas.delete('boot')
    progress += 5
    cx, cy = 700, 425
    canvas.create_rectangle(cx-200, cy+100, cx+200, cy+120, outline='white', tags='boot')
    canvas.create_rectangle(cx-198, cy+102, cx-198+(progress*3.96), cy+118, fill=data_cell_green, tags='boot')
    if progress < 100: root.after(50, boot)
    else: login_screen()

def login_screen():
    canvas.delete('all')
    canvas.create_rectangle(0, 0, 1400, 850, fill='#3399ff')
    btn = canvas.create_rectangle(600, 400, 800, 460, fill='white', outline='white')
    canvas.create_text(700, 430, text="Login", font=('Segoe UI', 14))
    canvas.tag_bind(btn, '<Button-1>', lambda e: desktop())

# ============================================
# DESKTOP (The missing function)
# ============================================
def draw_background():
    canvas.delete('bg')
    if bg_image_obj:
        canvas.create_image(700, 425, image=bg_image_obj, tags='bg')
    else:
        canvas.create_rectangle(0, 0, 1400, 600, fill=current_theme['bg_top'], outline='', tags='bg')
        canvas.create_rectangle(0, 600, 1400, 850, fill=current_theme['bg_bottom'], outline='', tags='bg')
    # Aero Sphere
    canvas.create_oval(400, 150, 1000, 750, outline=aero_blue_light, width=2, tags='bg')

def desktop():
    canvas.delete('all')
    draw_background()
    
    # Taskbar
    canvas.create_rectangle(200, 770, 1200, 830, fill='white', stipple='gray50', tags='ui')
    
    # Icons (Simple Text Buttons)
    apps = [("Terminal", open_terminal), ("About", open_about)]
    for i, (name, func) in enumerate(apps):
        x = 250 + (i * 100)
        btn = canvas.create_oval(x-25, 780, x+25, 820, fill=aero_blue_light, outline='white', tags='ui')
        canvas.create_text(x, 800, text=name[0], fill='white', font=('Arial', 12, 'bold'), tags='ui')
        canvas.tag_bind(btn, '<Button-1>', func)

boot()
root.mainloop()