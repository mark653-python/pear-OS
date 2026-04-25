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

# Combined Theme State from Settings and Main Script
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

def start_matrix_effect(t_tag):
    chars = "0123456789ABCDEFHIJKLMNOPQRSTUVWXYZ$+-*/=%\"'#&_(),.;:?!"
    for _ in range(15):
        x = random.randint(320, 980)
        drop = canvas.create_text(x, 200, text=random.choice(chars), fill='#00ff41', font=('Consolas', 10), tags=(t_tag, 'matrix'))
        def fall(item=drop, x_pos=x, y_pos=200):
            if not canvas.find_withtag(t_tag): return
            new_y = y_pos + 15
            if new_y < 580:
                canvas.coords(item, x_pos, new_y)
                canvas.itemconfig(item, text=random.choice(chars))
                root.after(50, lambda: fall(item, x_pos, new_y))
            else: canvas.delete(item)
        fall()

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
    if 'Snake' in title: snake_game_running = False
    if 'Apple Catcher' in title: catcher_game_running = False

# ============================================
# SYSTEM & SETTINGS APPS
# ============================================
def open_settings(e=None):
    t = create_window('System Settings', '#eeeeee')
    if not t: return

    canvas.create_text(330, 220, text="Personalization", font=('Segoe UI', 16, 'bold'), anchor='w', fill='#333', tags=t)
    
    def set_theme(mode):
        global current_theme
        if mode == "Aero":
            current_theme['bg_top'] = '#3399ff'
            current_theme['bg_bottom'] = '#44dd44'
            current_theme['taskbar'] = 'white'
        else: # Dark Mode
            current_theme['bg_top'] = '#1a1a1a'
            current_theme['bg_bottom'] = '#000000'
            current_theme['taskbar'] = '#333333'
        
        draw_background()
        redraw_ui_overlay()
        messagebox.showinfo("Settings", f"Theme updated to {mode}!")

    aero_btn = canvas.create_rectangle(330, 260, 480, 300, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(405, 280, text="Aero Blue", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(aero_btn, '<Button-1>', lambda e: set_theme("Aero"))

    dark_btn = canvas.create_rectangle(500, 260, 650, 300, fill='#333333', outline='white', tags=t)
    canvas.create_text(575, 280, text="Dark Mode", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(dark_btn, '<Button-1>', lambda e: set_theme("Dark"))

    canvas.create_text(330, 340, text="System Info", font=('Segoe UI', 16, 'bold'), anchor='w', fill='#333', tags=t)
    canvas.create_text(330, 370, text="OS Version: GaiaSphere 1.0.4\nResolution: 1400x850\nKernel: PearCore-Py", 
                       font=('Segoe UI', 11), anchor='nw', fill='#555', tags=t)

def open_system(e=None):
    t = create_window('System Diagnostics', '#f8f9fa')
    if not t: return

    canvas.create_text(330, 220, text="Hardware Overview", font=('Segoe UI', 14, 'bold'), anchor='w', fill='#333', tags=t)
    cpu_label = canvas.create_text(330, 255, text="CPU Usage: 0%", font=('Consolas', 11), anchor='w', fill='#555', tags=t)
    ram_label = canvas.create_text(330, 280, text="RAM Load: 0%", font=('Consolas', 11), anchor='w', fill='#555', tags=t)

    def update_stats():
        if not canvas.find_withtag(t): return
        cpu = random.randint(5, 45)
        ram = random.randint(20, 60)
        canvas.itemconfig(cpu_label, text=f"CPU Usage: {cpu}% [||||      ]")
        canvas.itemconfig(ram_label, text=f"RAM Load: {ram}%  [||||||    ]")
        root.after(1500, update_stats)
    update_stats()

    btn1 = canvas.create_rectangle(330, 350, 500, 390, fill='#ff9966', outline='white', tags=t)
    canvas.create_text(415, 370, text="Purge Temp", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn1, '<Button-1>', lambda e: [messagebox.showinfo("System", "Purging GaiaSphere cache..."), shake_window(5)])

    btn2 = canvas.create_rectangle(520, 350, 690, 390, fill='#66b3ff', outline='white', tags=t)
    canvas.create_text(605, 370, text="Ping Test", fill='white', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn2, '<Button-1>', lambda e: messagebox.showinfo("Network", "Pinging iCarly.com... 24ms"))

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process(event):
        cmd = cmd_var.get().strip().lower()
        log.append(f"root@pearos:~$ {cmd}")
        if cmd == 'help': log.append("help, ls, matrix, shake, party")
        elif cmd == 'ls': log.append("Applications/  Documents/  secret_recipe.txt")
        elif cmd == 'matrix': start_matrix_effect(t)
        elif cmd == 'shake': shake_window()
        elif cmd in ['party', 'dance']: trigger_dance()
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)

# ============================================
# GAMES & MEDIA
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

# ============================================
# DESKTOP ENGINE
# ============================================
def open_browser(e=None):
    t = create_window('PearWeb Explorer')
    if t:
        search_var = tk.StringVar()
        canvas.create_text(650, 320, text='PearGLE', fill='#4285F4', font=('Segoe UI', 48, 'bold'), tags=t)
        search_entry = tk.Entry(root, textvariable=search_var, font=('Segoe UI', 14), width=40)
        canvas.create_window(650, 400, window=search_entry, tags=t)
        btn = canvas.create_rectangle(580, 440, 720, 480, fill='#f8f9fa', outline='#dadce0', tags=t)
        canvas.create_text(650, 460, text='Pear Search', tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e: webbrowser.open(f"https://www.google.com/search?q={search_var.get()}"))

def open_about(e=None):
    t = create_window('About')
    if t: 
        text = "pear OS Frutiger Edition 2026\nSimulation Core Built With Python + Tkinter\nby mark"
        canvas.create_text(650, 350, text=text, justify='center', font=('Segoe UI', 18, 'bold'), tags=t)

def boot():
    global progress
    canvas.delete('boot')
    progress += 4
    canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2, tags='boot')
    canvas.create_rectangle(452, 562, 452 + progress * 5, 593, fill=data_cell_green, outline='', tags='boot')
    canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120), tags='boot')
    if progress < 100: root.after(60, boot)
    else: desktop()

def draw_background():
    canvas.delete('bg')
    for i in range(1200): canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
    for i in range(400): canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(220, 760, 1280, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    # Added Settings to the apps list
    apps = [
        ('🖥️', 'System', open_system), ('🌐', 'PearWeb', open_browser),
        ('📁', 'Finder', lambda e: messagebox.showinfo("Finder", "GaiaDrive Online")),
        ('⚙️', 'Settings', open_settings),
        ('🐍', 'Snake', open_snake), ('🍎', 'Catcher', open_apple_catcher),
        ('📟', 'Terminal', open_terminal), ('🍐', 'About', open_about)
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 280 + i * 120 # Adjusted spacing for the extra icon
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
        canvas.coords(item, x, y, x+18, y+18); b[2] = y
    root.after(40, animate_bubbles)

boot()
root.mainloop()