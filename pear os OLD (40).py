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
root.title('Pear OS Ultimate GaiaSphere')
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
        ('📟', 'Terminal', open_terminal), ('🍐', 'About', lambda e: messagebox.showinfo("Pear OS", "Ultimate GaiaSphere 2026"))
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 220 + i * 115
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 32), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

# ============================================
# FX MODULES
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
# WINDOW MANAGER
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

# ============================================
# NEW: PEAR SHOOTER GAME
# ============================================
def open_pear_shooter(e=None):
    global shooter_game_running
    tag = create_window('Pear Shooter', '#121212')
    if not tag: return
    
    shooter_game_running = True
    score = [0]
    player_pos = [650, 560]
    bullets = []
    enemies = []
    
    score_text = canvas.create_text(320, 210, text="Score: 0", fill='white', font=('Segoe UI', 12), anchor='nw', tags=tag)
    
    def spawn_enemy():
        if shooter_game_running and canvas.find_withtag(tag):
            enemies.append([random.randint(320, 980), 200])
            root.after(1500, spawn_enemy)

    def fire_bullet(e=None):
        if shooter_game_running:
            bullets.append([player_pos[0], player_pos[1]-20])

    def update_game():
        if not shooter_game_running or not canvas.find_withtag(tag): return
        canvas.delete('shooter_obj')
        
        # Draw Player
        canvas.create_text(player_pos[0], player_pos[1], text="🍐", font=('Arial', 24), tags=(tag, 'shooter_obj'))
        
        # Update Bullets
        for b in bullets[:]:
            b[1] -= 10
            canvas.create_oval(b[0]-3, b[1]-3, b[0]+3, b[1]+3, fill='yellow', tags=(tag, 'shooter_obj'))
            if b[1] < 200: bullets.remove(b)
            
        # Update Enemies
        for en in enemies[:]:
            en[1] += 3
            canvas.create_text(en[0], en[1], text="👾", font=('Arial', 20), tags=(tag, 'shooter_obj'))
            
            # Collision Check
            for b in bullets[:]:
                if abs(b[0] - en[0]) < 20 and abs(b[1] - en[1]) < 20:
                    score[0] += 10
                    canvas.itemconfig(score_text, text=f"Score: {score[0]}")
                    if en in enemies: enemies.remove(en)
                    if b in bullets: bullets.remove(b)
            
            if en[1] > 580:
                messagebox.showinfo("Game Over", f"System Breach! Score: {score[0]}")
                close_window(tag, 'Pear Shooter')
                return

        root.after(30, update_game)

    root.bind('<Left>', lambda e: player_pos.__setitem__(0, max(320, player_pos[0]-25)))
    root.bind('<Right>', lambda e: player_pos.__setitem__(0, min(980, player_pos[0]+25)))
    root.bind('<space>', fire_bullet)
    
    spawn_enemy()
    update_game()

# ============================================
# SYSTEM APPS (SETTINGS, TERMINAL, ETC.)
# ============================================
def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    canvas.create_rectangle(300, 190, 450, 600, fill='#e0e0e0', outline='', tags=t)
    categories = ["Appearance", "System"]
    content_tags = f"{t}_content"

    def show_category(cat):
        canvas.delete(content_tags)
        if cat == "Appearance":
            canvas.create_text(470, 230, text="Personalization", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            upload_btn = canvas.create_rectangle(470, 270, 700, 310, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(585, 290, text="Upload Wallpaper", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(upload_btn, '<Button-1>', lambda e: upload_bg())

    def upload_bg():
        global custom_bg_path
        path = filedialog.askopenfilename(filetypes=[("Image", "*.jpg *.png *.bmp")])
        if path:
            custom_bg_path = path
            draw_background(); redraw_ui_overlay()

    for i, cat in enumerate(categories):
        btn = canvas.create_text(375, 230 + (i * 50), text=cat, font=('Segoe UI', 12), tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e, c=cat: show_category(c))
    show_category("Appearance")

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()
    def process(event):
        cmd = cmd_var.get().strip().lower()
        log.append(f"root@pearos:~$ {cmd}")
        if cmd == 'help': log.append("help, clear, shooter")
        elif cmd == 'shooter': open_pear_shooter()
        elif cmd == 'clear': log.clear()
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)

# ============================================
# LEGACY GAMES (SNAKE & CATCHER)
# ============================================
def open_apple_catcher(e=None):
    global catcher_game_running
    tag = create_window('Apple Catcher', '#fce4ec')
    if not tag: return
    catcher_game_running, score, basket = True, [0], [650, 550]
    apples = [[random.randint(350, 950), 200] for _ in range(3)]
    score_text = canvas.create_text(350, 220, text="Apples: 0/10", font=('Segoe UI', 14, 'bold'), anchor='w', fill='#d81b60', tags=tag)
    def update():
        if not catcher_game_running or not canvas.find_withtag(tag): return
        canvas.delete('game_obj')
        canvas.create_rectangle(basket[0]-40, basket[1], basket[0]+40, basket[1]+10, fill='#ba68c8', tags=(tag, 'game_obj'))
        for p in apples:
            p[1] += 6
            canvas.create_oval(p[0]-12, p[1]-12, p[0]+12, p[1]+12, fill='#ff1744', outline='white', tags=(tag, 'game_obj'))
            if p[1] > 540 and abs(p[0] - basket[0]) < 50:
                score[0] += 1
                canvas.itemconfig(score_text, text=f"Apples: {score[0]}/10")
                p[1] = 200; p[0] = random.randint(350, 950)
                if score[0] >= 10:
                    messagebox.showinfo("Win!", "Random dancing!"); close_window(tag, 'Apple Catcher'); trigger_dance(); return
            if p[1] > 600: p[1] = 200; p[0] = random.randint(350, 950)
        root.after(30, update)
    root.bind('<Left>', lambda e: basket.__setitem__(0, max(340, basket[0] - 35)))
    root.bind('<Right>', lambda e: basket.__setitem__(0, min(960, basket[0] + 35)))
    update()

def open_snake(e=None):
    global snake_game_running
    tag = create_window('Snake Sphere', '#000000')
    if not tag: return
    snake_game_running = True
    snake, direction, food = [[650, 350], [640, 350], [630, 350]], 'Right', [700, 400]
    def move():
        nonlocal direction, food
        if not snake_game_running or not canvas.find_withtag(tag): return
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
    root.bind('<w>', lambda e: set_dir('Up')); root.bind('<s>', lambda e: set_dir('Down'))
    root.bind('<a>', lambda e: set_dir('Left')); root.bind('<d>', lambda e: set_dir('Right'))
    def set_dir(d): nonlocal direction; direction = d
    move()

def open_system(e=None):
    t = create_window('System Diagnostics', '#f8f9fa')
    if not t: return
    cpu_label = canvas.create_text(330, 255, text="CPU Usage: 0%", font=('Consolas', 11), anchor='w', tags=t)
    def update_stats():
        if not canvas.find_withtag(t): return
        cpu = random.randint(5, 45)
        canvas.itemconfig(cpu_label, text=f"CPU Usage: {cpu}% [||||      ]")
        root.after(1500, update_stats)
    update_stats()

# ============================================
# BOOT
# ============================================
def boot():
    global progress
    canvas.delete('boot')
    progress += 5
    canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2, tags='boot')
    canvas.create_rectangle(452, 562, 452 + progress * 5, 593, fill=data_cell_green, outline='', tags='boot')
    canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120), tags='boot')
    if progress < 100: root.after(50, boot)
    else:
        canvas.delete('all')
        draw_background(); redraw_ui_overlay()

boot()
root.mainloop()