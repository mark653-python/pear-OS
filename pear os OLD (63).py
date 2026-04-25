import tkinter as tk
import random
import webbrowser
import os
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import pygame

# ============================================
# INITIALIZATION & GLOBAL STATE
# ============================================
pygame.mixer.init()

root = tk.Tk()
root.title('Pear OS Ultimate GaiaSphere HD')
root.geometry('1400x850')
root.configure(bg='black')

is_fullscreen = False
custom_bg_path = None
bg_image_ref = None  
current_theme = {
    'bg_top': '#3399ff',
    'bg_bottom': '#44dd44',
    'taskbar': 'white'
}

progress = 0
bubbles = []
open_apps = {}
snake_game_running = False
catcher_game_running = False
shooter_game_running = False

aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# ============================================
# BACKGROUND & UI ENGINE
# ============================================
def draw_default_gradient():
    for i in range(1200): 
        canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
    for i in range(400): 
        canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def draw_background():
    global bg_image_ref
    canvas.delete('bg')
    
    if custom_bg_path:
        try:
            img = Image.open(custom_bg_path)
            img = img.resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_ref = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=bg_image_ref, anchor='nw', tags='bg')
        except:
            draw_default_gradient()
    else:
        draw_default_gradient()

    if len(open_apps) > 0:
        canvas.create_rectangle(0, 0, 1400, 850, fill='black', stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(150, 760, 1300, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    apps = [
        ('🖥️', 'System', open_system), ('🌐', 'Web', lambda e: webbrowser.open("https://google.com")),
        ('⚙️', 'Settings', open_settings), ('🐍', 'Snake', open_snake), 
        ('🍎', 'Catcher', open_apple_catcher), ('🔫', 'Shooter', open_pear_shooter),
        ('📟', 'Terminal', open_terminal), ('🍐', 'About', lambda e: messagebox.showinfo("Pear OS", "Ultimate GaiaSphere 2026 HD"))
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 220 + i * 115
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 32), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

# ============================================
# FX MODULES (SHAKE & DANCE)
# ============================================
def shake_window(count=10):
    if count > 0:
        x_shift = random.randint(-10, 10)
        y_shift = random.randint(-10, 10)
        root.geometry(f"+{root.winfo_x() + x_shift}+{root.winfo_y() + y_shift}")
        root.after(50, lambda: shake_window(count - 1))

def trigger_dance(e=None):
    try:
        pygame.mixer.music.load("random_dancing.mp3")
        pygame.mixer.music.play()
    except: pass
    
    def dance(count=20):
        if count > 0:
            colors = ['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00']
            canvas.configure(bg=random.choice(colors))
            shake_window(2)
            root.after(100, lambda: dance(count - 1))
        else:
            canvas.configure(bg='black')
            root.destroy()
    dance()

# ============================================
# HD BUBBLE SYSTEM
# ============================================
def init_bubbles():
    global bubbles
    bubbles = []
    # Create 25 HD bubbles with randomized depth and size
    for _ in range(25):
        size = random.randint(8, 28)
        x = random.randint(50, 1350)
        y = random.randint(700, 1200)
        speed = random.uniform(1.2, 3.5)
        
        # HD Effect: Semi-transparent glow outline with stippled fill
        b = canvas.create_oval(x, y, x+size, y+size, 
                               outline='#ffffff', width=1, 
                               fill='white', stipple='gray25', 
                               tags='ui')
        bubbles.append({'id': b, 'x': x, 'y': y, 'size': size, 'speed': speed})

def animate_bubbles():
    for b in bubbles:
        b['y'] -= b['speed']
        # Reset bubble to bottom when it floats off top
        if b['y'] < -50:
            b['y'] = 850
            b['x'] = random.randint(50, 1350)
        
        canvas.coords(b['id'], b['x'], b['y'], b['x']+b['size'], b['y']+b['size'])
    
    # Run at ~60fps
    root.after(16, animate_bubbles)

# ============================================
# WINDOW MANAGER & GAMES (CONSOLIDATED)
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '').replace('-', '')
    draw_background()
    
    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', tags=tag)
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    canvas.create_rectangle(300, 150, 1000, 190, fill='#44ee44', outline=data_cell_green, stipple='gray75', tags=tag)
    canvas.create_text(650, 170, text=title, fill='white', font=('Segoe UI', 14, 'bold'), tags=tag)
    btn = canvas.create_oval(310, 160, 330, 180, fill='#ff4d4d', outline='white', tags=tag)
    
    canvas.tag_bind(btn, '<Button-1>', lambda e: close_window(tag, title))
    return tag

def close_window(tag, title):
    global snake_game_running, catcher_game_running, shooter_game_running
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)
    draw_background()
    redraw_ui_overlay()
    if 'Snake' in title: snake_game_running = False
    if 'Apple Catcher' in title: catcher_game_running = False
    if 'Shooter' in title: shooter_game_running = False

# [GAMES AND APPS: PEAR SHOOTER, SNAKE, CATCHER, SETTINGS, TERMINAL REMAIN INTEGRATED]
# (Code logic for games and terminal remains identical to previous integrated version)

def open_pear_shooter(e=None):
    global shooter_game_running
    tag = create_window('Pear Shooter', '#121212')
    if not tag: return
    shooter_game_running, score, player_pos, bullets, enemies = True, [0], [650, 560], [], []
    score_text = canvas.create_text(320, 210, text="Score: 0", fill='white', font=('Segoe UI', 12), anchor='nw', tags=tag)
    
    def spawn_enemy():
        if shooter_game_running and canvas.find_withtag(tag):
            enemies.append([random.randint(320, 980), 200]); root.after(1500, spawn_enemy)
    def update_game():
        if not shooter_game_running or not canvas.find_withtag(tag): return
        canvas.delete('shooter_obj')
        canvas.create_text(player_pos[0], player_pos[1], text="🍐", font=('Arial', 24), tags=(tag, 'shooter_obj'))
        for b in bullets[:]:
            b[1] -= 10; canvas.create_oval(b[0]-3, b[1]-3, b[0]+3, b[1]+3, fill='yellow', tags=(tag, 'shooter_obj'))
            if b[1] < 200: bullets.remove(b)
        for en in enemies[:]:
            en[1] += 3; canvas.create_text(en[0], en[1], text="👾", font=('Arial', 20), tags=(tag, 'shooter_obj'))
            for b in bullets[:]:
                if abs(b[0] - en[0]) < 20 and abs(b[1] - en[1]) < 20:
                    score[0] += 10; canvas.itemconfig(score_text, text=f"Score: {score[0]}")
                    if en in enemies: enemies.remove(en)
                    if b in bullets: bullets.remove(b)
            if en[1] > 580: close_window(tag, 'Pear Shooter'); return
        root.after(30, update_game)
    root.bind('<Left>', lambda e: player_pos.__setitem__(0, max(320, player_pos[0]-25)))
    root.bind('<Right>', lambda e: player_pos.__setitem__(0, min(980, player_pos[0]+25)))
    root.bind('<space>', lambda e: bullets.append([player_pos[0], player_pos[1]-20]))
    spawn_enemy(); update_game()

def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    canvas.create_rectangle(30