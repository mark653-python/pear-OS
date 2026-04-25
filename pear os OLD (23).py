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
# SYSTEM APPS
# ============================================
def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for a list of commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, 
                         insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        log.append(f"root@pearos:~$ {cmd}")
        
        if cmd == 'help':
            log.append("Available: help, ls, date, clear, i-ready, random-dancing")
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
        
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")

    cmd_entry.bind('<Return>', process_command)

def open_apple_catcher(e=None):
    global catcher_game_running
    tag = create_window('Apple Catcher', '#fce4ec')
    if not tag: return
    
    catcher_game_running = True
    score = [0]
    basket = [650, 550]
    apples = [[random.randint(350, 950), 200] for _ in range(3)]
    
    canvas.create_text(650, 220, text="Help Carly catch 10 of Sam's apples!", font=('Segoe UI', 12, 'italic'), fill='#880e4f', tags=tag)
    score_text = canvas.create_text(350, 220, text="Apples: 0/10", font=('Segoe UI', 14, 'bold'), anchor='w', fill='#d81b60', tags=tag)
    
    def update():
        if not catcher_game_running or tag not in canvas.find_all(): return
        canvas.delete('game_obj')
        canvas.create_rectangle(basket[0]-40, basket[1], basket[0]+40, basket[1]+10, fill='#ba68c8', tags=(tag, 'game_obj'))
        canvas.create_text(basket[0], basket[1]+25, text="👩 Carly", font=('Segoe UI', 10, 'bold'), fill='#4a148c', tags=(tag, 'game_obj'))
        
        for p in apples:
            p[1] += 6
            canvas.create_oval(p[0]-12, p[1]-12, p[0]+12, p[1]+12, fill='#ff1744', outline='white', tags=(tag, 'game_obj'))
            if p[1] > 540 and abs(p[0] - basket[0]) < 50:
                score[0] += 1
                canvas.itemconfig(score_text, text=f"Apples: {score[0]}/10")
                p[1] = 200
                p[0] = random.randint(350, 950)
                if score[0] >= 10:
                    messagebox.showinfo("iCarly Win!", "You caught all 10 apples! Random dancing!")
                    close_window(tag, 'Apple Catcher')
                    return
            if p[1] > 600:
                p[1] = 200
                p[0] = random.randint(350, 950)
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
        if not snake_game_running: return
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

    root.bind('<w>', lambda e: set_dir('Up'))
    root.bind('<s>', lambda e: set_dir('Down'))
    root.bind('<a>', lambda e: set_dir('Left'))
    root.bind('<d>', lambda e: set_dir('Right'))
    def set_dir(d): nonlocal direction; direction = d
    move()

def open_music(e=None):
    t = create_window('Core Rhythms')
    if not t: return
    is_playing = [False]
    canvas.create_text(650, 300, text='🎵', font=('Arial', 80), tags=t)
    track_label = canvas.create_text(650, 400, text="No Track Loaded", font=('Segoe UI', 12), fill='#333', tags=t)
    def upload_file():
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            filename = file_path.split('/')[-1]
            canvas.itemconfig(track_label, text=f"Playing: {filename}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            is_playing[0] = True
    def toggle_play():
        if is_playing[0]: pygame.mixer.music.pause(); is_playing[0] = False
        else: pygame.mixer.music.unpause(); is_playing[0] = True
    btn_load = canvas.create_rectangle(520, 450, 620, 490, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(570, 470, text='Load', font=('Segoe UI', 10, 'bold'), tags=t)
    btn_play = canvas.create_rectangle(630, 450, 780, 490, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(705, 470, text='Play / Pause', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn_load, '<Button-1>', lambda e: upload_file())
    canvas.tag_bind(btn_play, '<Button-1>', lambda e: toggle_play())

def open_browser(e=None):
    t = create_window('PearWeb Explorer')
    if t:
        search_var = tk.StringVar()
        canvas.create_text(650, 320, text='PearGLE', fill='#4285F4', font=('Segoe UI', 48, 'bold'), tags=t)
        search_entry = tk.Entry(root, textvariable=search_var, font=('Segoe UI', 14), width=40)
        canvas.create_window(650, 400, window=search_entry, tags=t)
        def search(): webbrowser.open(f"https://www.google.com/search?q={search_var.get()}")
        btn = canvas.create_rectangle(580, 440, 720, 480, fill='#f8f9fa', outline='#dadce0', tags=t)
        canvas.create_text(650, 460, text='Pear Search', tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e: search())

def open_finder(e=None, path='.'):
    abs_path = os.path.abspath(path)
    title = f'Finder - {os.path.basename(abs_path) or "Home"}'
    t = create_window(title, '#f9f9f9')
    if not t: return
    canvas.create_text(320, 210, text=f"🏠 {abs_path}", font=('Segoe UI', 10, 'bold'), anchor='nw', tags=t)
    try: files = os.listdir(path)
    except: files = ["Error"]
    for i, item in enumerate(files[:12]):
        col, row = i % 4, i // 4
        x, y = 360 + (col * 150), 280 + (row * 120)
        full_path = os.path.join(path, item)
        is_dir = os.path.isdir(full_path)
        obj = canvas.create_text(x, y, text='📁' if is_dir else '📄', font=('Arial', 40), tags=t)
        canvas.create_text(x, y + 45, text=item[:12], font=('Segoe UI', 8), tags=t)
        def handle_click(p=full_path, folder=is_dir, tag=t, win_title=title):
            if folder: close_window(tag, win_title); open_finder(None, p)
            else: webbrowser.open(p)
        canvas.tag_bind(obj, '<Double-Button-1>', lambda e, p=full_path, f=is_dir: handle_click(p, f))

def open_sys_info(e=None):
    t = create_window('System Diagnostics')
    if t: canvas.create_text(650, 380, text='Pear OS v1.0\nUser: Carly Shay\nStatus: Optimal', justify='center', font=('Segoe UI', 18), tags=t)

def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if not t: return
    canvas.create_text(320, 220, text='Personalization', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)
    def set_theme(mode):
        global current_theme
        if mode == "Aero": current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else: current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#333333', 'taskbar': '#444444'}
        draw_background(); redraw_ui_overlay(); canvas.tag_lower('bg'); canvas.tag_lower('ui', 'bg')
    btn_aero = canvas.create_rectangle(320, 280, 420, 310, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(370, 295, text="Aero Blue", tags=t)
    canvas.tag_bind(btn_aero, '<Button-1>', lambda e: set_theme("Aero"))

def open_about(e=None):
    t = create_window('About')
    if t: canvas.create_text(650, 350, text='Pear OS Frutiger Edition\niCarly Character Mod Activated', justify='center', font=('Segoe UI', 18, 'bold'), tags=t)

# ============================================
# BACKGROUND VISUALS
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

# ============================================
# RUN
# ============================================
boot()
root.mainloop()