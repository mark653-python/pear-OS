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
    canvas.create_rectangle(cx-248, cy+137, cx-248 + progress * 5, cy+168, fill=data_cell_green, outline='', tags='boot_bar')
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
    canvas.create_rectangle(280, 760, 1180, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    apps = [
        ('system.png', '🖥️', 'System', open_sys_info),
        ('browser.png', '🌐', 'PearWeb', open_browser),
        ('catcher.png', '🍎', 'Apple Catcher', open_apple_catcher),
        ('terminal.png', '📟', 'Terminal', open_terminal),
        ('about.png', '🍐', 'About', open_about)
    ]
    for i, (img_path, emoji, name, func) in enumerate(apps):
        x = 340 + i * 110
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
    global catcher_game_running
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)
    if 'Apple Catcher' in title: catcher_game_running = False

# ============================================
# THEMED APP: APPLE CATCHER (iCarly Edition)
# ============================================
def open_apple_catcher(e=None):
    global catcher_game_running
    tag = create_window('Apple Catcher', '#fce4ec')
    if not tag: return
    
    catcher_game_running = True
    score = [0]
    win_score = 10
    basket = [650, 550] # Carly (The Catcher)
    apples = [[random.randint(350, 950), 200] for _ in range(3)] # Sam's drops
    
    # UI Elements
    canvas.create_text(650, 220, text="Help Carly catch 10 of Sam's apples!", font=('Segoe UI', 12, 'italic'), fill='#880e4f', tags=tag)
    score_text = canvas.create_text(350, 220, text="Apples: 0/10", font=('Segoe UI', 14, 'bold'), anchor='w', fill='#d81b60', tags=tag)
    
    # Visual markers for Sam at the top
    sam_label = canvas.create_text(650, 205, text="👱‍♀️ Sam is dropping apples!", font=('Segoe UI', 10), fill='#333', tags=tag)

    def update():
        if not catcher_game_running or tag not in canvas.find_all(): return
        
        canvas.delete('game_obj')
        
        # Draw Carly (Player)
        canvas.create_rectangle(basket[0]-40, basket[1], basket[0]+40, basket[1]+10, fill='#ba68c8', tags=(tag, 'game_obj'))
        canvas.create_text(basket[0], basket[1]+25, text="👩 Carly", font=('Segoe UI', 10, 'bold'), fill='#4a148c', tags=(tag, 'game_obj'))
        
        for p in apples:
            p[1] += 6 # Gravity
            # Draw Apple
            canvas.create_oval(p[0]-12, p[1]-12, p[0]+12, p[1]+12, fill='#ff1744', outline='white', tags=(tag, 'game_obj'))
            
            # Catch Logic
            if p[1] > 540 and abs(p[0] - basket[0]) < 50:
                score[0] += 1
                canvas.itemconfig(score_text, text=f"Apples: {score[0]}/10")
                p[1] = 200
                p[0] = random.randint(350, 950)
                
                # Win Condition
                if score[0] >= win_score:
                    messagebox.showinfo("iCarly Win!", "You caught all 10 apples! Random dancing!")
                    close_window(tag, 'Apple Catcher')
                    return
            
            # Reset if missed
            if p[1] > 600:
                p[1] = 200
                p[0] = random.randint(350, 950)

        root.after(30, update)

    def move_left(e): basket[0] = max(340, basket[0] - 35)
    def move_right(e): basket[0] = min(960, basket[0] + 35)
    
    root.bind('<Left>', move_left)
    root.bind('<Right>', move_right)
    update()

# ============================================
# SYSTEM APPS
# ============================================
def open_browser(e=None):
    t = create_window('PearWeb')
    if t:
        canvas.create_text(650, 350, text='Welcome to iCarly.com\n(Simulation)', font=('Segoe UI', 24), fill='#4285F4', tags=t)

def open_terminal(e=None):
    t = create_window('Terminal', '#1a1a1a')
    if t:
        canvas.create_text(320, 210, text="root@pearos:~# iCarly --version\niCarly OS Kernel v1.0.4", anchor='nw', fill=data_cell_green, font=('Consolas', 10), tags=t)

def open_sys_info(e=None):
    t = create_window('System Info')
    if t: canvas.create_text(650, 380, text='Pear OS v1.0\nUser: Carly Shay\nStatus: Online', justify='center', font=('Segoe UI', 18), tags=t)

def open_about(e=None):
    t = create_window('About')
    if t: canvas.create_text(650, 350, text='Pear OS: Frutiger Edition\niCarly Character Mod Activated', justify='center', font=('Segoe UI', 16, 'bold'), tags=t)

# ============================================
# UTILS
# ============================================
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