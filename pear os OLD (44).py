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
root.title('Pear OS Ultimate GaiaSphere 2026 HD')
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
aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# ============================================
# HD GRAPHICS ENGINE
# ============================================
def draw_default_gradient():
    """HD Sky & Ground Gradient with GaiaSphere Glass-morphism"""
    # HD Sky
    for i in range(600):
        r = int(51 + (102 - 51) * (i / 600))
        g = int(153 + (204 - 153) * (i / 600))
        b = 255
        canvas.create_line(0, i, 1400, i, fill=f'#{r:02x}{g:02x}{b:02x}', tags='bg')

    # HD Ground
    for i in range(250):
        y = 600 + i
        r = int(68 + (34 - 68) * (i / 250))
        g = int(221 + (153 - 221) * (i / 250))
        b = int(68 + (34 - 68) * (i / 250))
        canvas.create_line(0, y, 1400, y, fill=f'#{r:02x}{g:02x}{b:02x}', tags='bg')

    # GaiaSphere Glass Effect
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=4, stipple='gray50', tags='bg')
    canvas.create_oval(450, 150, 750, 300, fill='#ffffff', outline='', stipple='gray25', tags='bg')

def draw_background():
    global bg_image_ref
    canvas.delete('bg')
    if custom_bg_path:
        try:
            img = Image.open(custom_bg_path).resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_ref = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=bg_image_ref, anchor='nw', tags='bg')
        except: draw_default_gradient()
    else: draw_default_gradient()

def redraw_ui_overlay():
    canvas.delete('ui')
    # Taskbar
    canvas.create_rectangle(150, 760, 1300, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    # Random Dancing Button
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    apps = [
        ('🖥️', 'System', open_system), 
        ('🌐', 'Web', open_browser),
        ('📁', 'Finder', lambda e: open_finder(None, '.')),
        ('⚙️', 'Settings', open_settings), 
        ('🎵', 'Pear Tunes', open_music_player),
        ('🐍', 'Snake', open_snake), 
        ('🍎', 'Catcher', open_apple_catcher), 
        ('📟', 'Terminal', open_terminal), 
        ('🍐', 'About', lambda e: messagebox.showinfo("Pear OS", "Ultimate GaiaSphere 2026\nHD Media Integrated Edition"))
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 220 + i * 115
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 32), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

# ============================================
# SYSTEM FX
# ============================================
def shake_window(count=10):
    if count > 0:
        x_shift, y_shift = random.randint(-10, 10), random.randint(-10, 10)
        root.geometry(f"+{root.winfo_x() + x_shift}+{root.winfo_y() + y_shift}")
        root.after(50, lambda: shake_window(count - 1))

def trigger_dance(e=None):
    try:
        pygame.mixer.music.load("random_dancing.mp3")
        pygame.mixer.music.play()
    except: pass
    
    def dance(count=20):
        if count > 0:
            canvas.configure(bg=random.choice(['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00']))
            shake_window(2)
            root.after(100, lambda: dance(count - 1))
        else:
            canvas.configure(bg='black')
            draw_background(); redraw_ui_overlay()
    dance()

def init_bubbles():
    global bubbles
    bubbles = []
    for _ in range(25):
        size = random.randint(8, 28)
        x, y = random.randint(50, 1350), random.randint(700, 1200)
        speed = random.uniform(1.2, 3.5)
        b = canvas.create_oval(x, y, x+size, y+size, outline='#ffffff', width=1, fill='white', stipple='gray25', tags='ui')
        bubbles.append({'id': b, 'x': x, 'y': y, 'size': size, 'speed': speed})

def animate_bubbles():
    for b in bubbles:
        b['y'] -= b['speed']
        if b['y'] < -50: b['y'] = 850; b['x'] = random.randint(50, 1350)
        canvas.coords(b['id'], b['x'], b['y'], b['x']+b['size'], b['y']+b['size'])
    root.after(16, animate_bubbles)

# ============================================
# WINDOW MANAGER & APPS
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
    if title in open_apps: open_apps.pop(title)
    if 'Snake' in title: snake_game_running = False
    if 'Apple' in title: catcher_game_running = False
    draw_background(); redraw_ui_overlay()

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, borderwidth=0)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    
    def process(event):
        cmd = cmd_var.get().lower()
        log.append(f"root@pearos:~$ {cmd}")
        if cmd == 'help': log.append("Commands: music, shake, party, clear, ls")
        elif cmd == 'ls': log.append("Applications/  Games/  secret_pear_recipe.txt")
        elif cmd == 'party': trigger_dance()
        elif cmd == 'shake': shake_window()
        elif cmd == 'clear': log.clear()
        canvas.itemconfig(log_text, text="\n".join(log[-15:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)
    cmd_entry.focus_set()

def open_finder(e=None, path='.'):
    abs_path = os.path.abspath(path)
    t = create_window(f'Finder - {os.path.basename(abs_path) or "Home"}', '#f9f9f9')
    if not t: return
    canvas.create_text(320, 210, text=f"🏠 {abs_path}", font=('Segoe UI', 10, 'bold'), anchor='nw', tags=t)
    files = os.listdir(path) if os.path.exists(path) else ["Error"]
    for i, item in enumerate(files[:12]):
        col, row = i % 4, i // 4
        x, y = 360 + (col * 150), 280 + (row * 120)
        obj = canvas.create_text(x, y, text='📁' if os.path.isdir(os.path.join(path, item)) else '📄', font=('Arial', 40), tags=t)
        canvas.create_text(x, y + 45, text=item[:12], font=('Segoe UI', 8), tags=t)

def open_music_player(e=None):
    t = create_window('Pear Tunes', '#1e1e1e')
    if not t: return
    canvas.create_text(650, 250, text="🎵", font=('Arial', 80), fill=aero_blue_light, tags=t)
    label = canvas.create_text(650, 350, text="No Song Loaded", fill='white', font=('Segoe UI', 12), tags=t)
    def load():
        p = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3 *.wav")])
        if p:
            canvas.itemconfig(label, text=f"Playing: {os.path.basename(p)}")
            pygame.mixer.music.load(p); pygame.mixer.music.play()
    btn = canvas.create_rectangle(550, 420, 750, 460, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(650, 440, text="Add Music", font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn, '<Button-1>', lambda e: load())

def open_browser(e=None):
    t = create_window('PearWeb Explorer')
    if t:
        v = tk.StringVar()
        canvas.create_text(650, 320, text='PearGLE', fill='#4285F4', font=('Segoe UI', 48, 'bold'), tags=t)
        ent = tk.Entry(root, textvariable=v, font=('Segoe UI', 14), width=40)
        canvas.create_window(650, 400, window=ent, tags=t)
        btn = canvas.create_rectangle(580, 440, 720, 480, fill='#f8f9fa', outline='#dadce0', tags=t)
        canvas.create_text(650, 460, text='Pear Search', tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e: webbrowser.open(f"https://google.com/search?q={v.get()}"))

def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    def upload():
        global custom_bg_path
        p = filedialog.askopenfilename(filetypes=[("Image", "*.jpg *.png")])
        if p: custom_bg_path = p; draw_background(); redraw_ui_overlay()
    btn = canvas.create_rectangle(500, 250, 700, 290, fill=aero_blue_light, tags=t)
    canvas.create_text(600, 270, text="Change Wallpaper", tags=t)
    canvas.tag_bind(btn, '<Button-1>', lambda e: upload())

def open_system(e=None):
    t = create_window('System Diagnostics', '#f8f9fa')
    if not t: return
    cpu = canvas.create_text(330, 255, text="CPU Usage: 0%", font=('Consolas', 11), anchor='w', tags=t)
    def upd():
        if canvas.find_withtag(t):
            canvas.itemconfig(cpu, text=f"CPU Usage: {random.randint(5,25)}%")
            root.after(2000, upd)
    upd()

# ============================================
# GAMES (SNAKE & APPLE CATCHER)
# ============================================
def open_apple_catcher(e=None):
    global catcher_game_running
    tag = create_window('Apple Catcher', '#fce4ec')
    if not tag: return
    catcher_game_running = True
    score, basket = [0], [650, 550]
    apples = [[random.randint(350, 950), 200] for _ in range(3)]
    score_text = canvas.create_text(350, 220, text="Apples: 0/10", font=('Segoe UI', 14, 'bold'), fill='#d81b60', tags=tag)
    
    def update():
        if not catcher_game_running or tag not in canvas.find_all(): return
        canvas.delete('game_obj')
        canvas.create_rectangle(basket[0]-40, basket[1], basket[0]+40, basket[1]+10, fill='#ba68c8', tags=(tag, 'game_obj'))
        for p in apples:
            p[1] += 6
            canvas.create_oval(p[0]-12, p[1]-12, p[0]+12, p[1]+12, fill='#ff1744', tags=(tag, 'game_obj'))
            if p[1] > 540 and abs(p[0] - basket[0]) < 50:
                score[0] += 1
                canvas.itemconfig(score_text, text=f"Apples: {score[0]}/10")
                p[1], p[0] = 200, random.randint(350, 950)
                if score[0] >= 10: trigger_dance(); close_window(tag, 'Apple Catcher'); return
            if p[1] > 600: p[1], p[0] = 200, random.randint(350, 950)
        root.after(30, update)
    root.bind('<Left>', lambda e: basket.__setitem__(0, max(340, basket[0]-35)))
    root.bind('<Right>', lambda e: basket.__setitem__(0, min(960, basket[0]+35)))
    update()

def open_snake(e=None):
    global snake_game_running
    tag = create_window('Snake Sphere', 'black')
    if not tag: return
    snake_game_running = True
    snk, dr, fd = [[650, 350], [640, 350]], 'Right', [700, 400]
    def move():
        nonlocal dr, fd
        if not snake_game_running: return
        h = list(snk[0])
        if dr == 'Up': h[1] -= 15
        elif dr == 'Down': h[1] += 15
        elif dr == 'Left': h[0] -= 15
        elif dr == 'Right': h[0] += 15
        if h[0] < 310 or h[0] > 990 or h[1] < 200 or h[1] > 590: close_window(tag, 'Snake Sphere'); return
        snk.insert(0, h)
        if abs(h[0]-fd[0]) < 15 and abs(h[1]-fd[1]) < 15: fd = [random.randint(350, 950), random.randint(250, 550)]
        else: snk.pop()
        canvas.delete('snk_obj')
        for s in snk: canvas.create_rectangle(s[0], s[1], s[0]+12, s[1]+12, fill=data_cell_green, tags=(tag, 'snk_obj'))
        canvas.create_oval(fd[0], fd[1], fd[0]+12, fd[1]+12, fill='red', tags=(tag, 'snk_obj'))
        root.after(100, move)
    root.bind('<w>', lambda e: exec("nonlocal dr; dr='Up'", locals(), globals())) # Simplified for integration
    move()

# ============================================
# BOOT SEQUENCE
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
        draw_background(); redraw_ui_overlay(); init_bubbles(); animate_bubbles()

boot()
root.mainloop()