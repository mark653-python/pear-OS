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

    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# ============================================
# DESKTOP ENVIRONMENT
# ============================================
def draw_background():
    """Draws only the background layers with the 'bg' tag"""
    canvas.delete('bg')
    if 'custom_bg' in icon_images:
        canvas.create_image(700, 425, image=icon_images['custom_bg'], tags='bg')
    else:
        # Default Gradient
        for i in range(1200):
            canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
        for i in range(400):
            canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
        # Aero Circle
        canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    """Draws taskbar and icons with the 'ui' tag"""
    canvas.delete('ui')
    # Taskbar
    canvas.create_rectangle(280, 760, 1180, 825, fill=current_theme['taskbar'], stipple='gray50', width=2, tags='ui')

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
# WINDOW MANAGER & APPS
# ============================================
def create_