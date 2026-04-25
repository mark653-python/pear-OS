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
screen_w = 1400
screen_h = 850

# Set the default custom background
custom_bg_path = "OIP.jpg"
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

drag_data = {"tag": None, "x": 0, "y": 0}

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# ============================================
# FULLSCREEN & RESIZE HANDLING
# ============================================
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    return "break"

def end_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", False)
    return "break"

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)

def on_resize(event):
    global screen_w, screen_h
    if abs(event.width - screen_w) > 5 or abs(event.height - screen_h) > 5:
        screen_w = event.width
        screen_h = event.height
        if progress >= 100:  
            draw_background()
            redraw_ui_overlay()

canvas.bind('<Configure>', on_resize)

# ============================================
# HD GRAPHICS ENGINE
# ============================================
def draw_default_gradient():
    sky_h = max(1, int(screen_h * 0.7))
    for i in range(sky_h):
        r = int(51 + (102 - 51) * (i / sky_h))
        g = int(153 + (204 - 153) * (i / sky_h))
        b = 255
        canvas.create_line(0, i, screen_w, i, fill=f'#{r:02x}{g:02x}{b:02x}', tags='bg')

    ground_h = max(1, screen_h - sky_h)
    for i in range(ground_h):
        y = sky_h + i
        r = int(68 + (34 - 68) * (i / ground_h))
        g = int(221 + (153 - 221) * (i / ground_h))
        b = int(68 + (34 - 68) * (i / ground_h))
        canvas.create_line(0, y, screen_w, y, fill=f'#{r:02x}{g:02x}{b:02x}', tags='bg')

    cx, cy = screen_w / 2, screen_h / 2
    canvas.create_oval(cx - 400, cy - 325, cx + 400, cy + 275, fill='#33ccff', outline=aero_blue_light, width=4, stipple='gray50', tags='bg')

def draw_background():
    global bg_image_ref
    canvas.delete('bg')
    if custom_bg_path and os.path.exists(custom_bg_path):
        try:
            img = Image.open(custom_bg_path).resize((screen_w, screen_h), Image.Resampling.LANCZOS)
            bg_image_ref = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=bg_image_ref, anchor='nw', tags='bg')
        except: 
            draw_default_gradient()
    else: 
        draw_default_gradient()

    if open_apps:
        canvas.create_rectangle(0, 0, screen_w, screen_h, fill='black', stipple='gray50', tags='bg')
        
    canvas.tag_lower('bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    tb_y1, tb_y2 = screen_h - 90, screen_h - 25
    tb_width = 1200
    tb_x1 = max(50, (screen_w - tb_width) / 2)
    tb_x2 = min(screen_w - 50, (screen_w + tb_width) / 2)

    canvas.create_rectangle(tb_x1, tb_y1, tb_x2, tb_y2, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    apps = [
        ('🖥️', 'System', open_system), 
        ('🌐', 'PearWeb', open_browser),
        ('📁', 'Finder', lambda e: open_finder(None, '.')),
        ('⚙️', 'Settings', open_settings), 
        ('🎵', 'Tunes', open_music_player),
        ('🎥', 'PearTube', open_youtube_app),
        ('🐍', 'Snake', open_snake), 
        ('🍎', 'Catcher', open_apple_catcher), 
        ('🚀', 'Shooter', open_shooter_game),
        ('📟', 'Terminal', open_terminal), 
    ]

    num_apps = len(apps)
    start_x = tb_x1 + 60
    spacing = (tb_x2 - tb_x1 - 120) / max(1, num_apps - 1)

    for i, (emoji, name, func) in enumerate(apps):
        x = start_x + i * spacing
        obj = canvas.create_text(x, tb_y1 + 32, text=emoji, font=('Arial', 32), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, tb_y1 + 75, text=name, fill='white', font=('Segoe UI', 9), tags='ui')
        
    canvas.tag_raise('ui')

# ============================================
# SYSTEM FX & WINDOW MANAGER
# ============================================
def trigger_dance(e=None):
    try:
        pygame.mixer.music.load("random_dancing.mp3")
        pygame.mixer.music.play()
    except: pass
    def dance(count=20):
        if count > 0:
            canvas.configure(bg=random.choice(['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00']))
            root.after(100, lambda: dance(count - 1))
        else: root.destroy()
    dance()

def start_drag(event, tag):
    drag_data["tag"], drag_data["x"], drag_data["y"] = tag, event.x, event.y
    canvas.tag_raise(tag); canvas.tag_raise('ui')

def drag(event):
    tag = drag_data["tag"]
    if tag:
        dx, dy = event.x - drag_data["x"], event.y - drag_data["y"]
        canvas.move(tag, dx, dy)
        drag_data["x"], drag_data["y"] = event.x, event.y

def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '')
    draw_background()
    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', tags=tag)
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)
    title_tag = f'{tag}_title'
    canvas.create_rectangle(300, 150, 1000, 190, fill='#44ee44', stipple='gray75', tags=(tag, title_tag))
    canvas.create_text(650, 170, text=title, fill='white', font=('Segoe UI', 14, 'bold'), tags=(tag, title_tag))
    btn = canvas.create_oval(310, 160, 330, 180, fill='#ff4d4d', outline='white', tags=tag)
    canvas.tag_bind(btn, '<Button-1>', lambda e: close_window(tag, title))
    if 'Snake' not in title and 'Shooter' not in title:
        canvas.tag_bind(title_tag, '<ButtonPress-1>', lambda e, t=tag: start_drag(e, t))
        canvas.tag_bind(title_tag, '<B1-Motion>', drag)
        canvas.tag_bind(title_tag, '<ButtonRelease-1>', lambda e: drag_data.update({"tag": None}))
    return tag

def close_window(tag, title):
    global snake_game_running, catcher_game_running, shooter_game_running
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)
    snake_game_running = catcher_game_running = shooter_game_running = False
    draw_background(); redraw_ui_overlay()

# ============================================
# PEARTUBE (YOUTUBE APP)
# ============================================
def open_youtube_app(e=None):
    t = create_window('PearTube', '#ffffff')
    if not t: return

    # Header
    canvas.create_rectangle(300, 190, 1000, 240, fill='#ffffff', outline='#dddddd', tags=t)
    canvas.create_text(360, 215, text="🎥 PearTube", fill='#ff0000', font=('Arial', 16, 'bold'), tags=t)

    # Search Bar
    yt_v = tk.StringVar()
    yt_ent = tk.Entry(root, textvariable=yt_v, font=('Segoe UI', 10), width=40, relief='solid', bd=1)
    canvas.create_window(650, 215, window=yt_ent, tags=t)
    
    def yt_search(event=None):
        webbrowser.open(f"https://www.youtube.com/results?search_query={yt_v.get()}")
    yt_ent.bind('<Return>', yt_search)

    # Simulated Video Grid
    videos = [
        ("Frutiger Aero Aesthetics", "7.2M views", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"), # Placeholder
        ("Pear OS 2026 Tutorial", "150K views", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        ("Lo-Fi Study Beats", "45M views", "https://www.youtube.com/watch?v=jfKfPfyJRdk"),
        ("Python Coding ASMR", "800K views", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ]

    for i, (name, views, url) in enumerate(videos):
        col, row = i % 2, i // 2
        x, y = 350 + (col * 350), 300 + (row * 140)
        
        # Video Thumbnail Box
        box = canvas.create_rectangle(x, y, x+250, y+80, fill='#cccccc', outline='#aaaaaa', tags=t)
        canvas.create_text(x+125, y+40, text="▶ PLAY", font=('Arial', 12, 'bold'), fill='white', tags=t)
        
        # Info
        canvas.create_text(x, y+95, text=name, anchor='w', font=('Segoe UI', 10, 'bold'), tags=t)
        canvas.create_text(x, y+110, text=views, anchor='w', font=('Segoe UI', 9), fill='gray', tags=t)
        
        # Click to "Play" (Open in Browser)
        canvas.tag_bind(box, '<Button-1>', lambda e, link=url: webbrowser.open(link))

# ============================================
# OTHER APPS & GAMES
# ============================================
def open_browser(e=None):
    t = create_window('PearWeb Explorer', '#ffffff')
    if not t: return
    v = tk.StringVar()
    canvas.create_text(650, 320, text='PearGLE', font=('Arial', 64, 'bold'), fill='#4285F4', tags=t)
    ent = tk.Entry(root, textvariable=v, font=('Segoe UI', 14), width=45)
    canvas.create_window(630, 400, window=ent, tags=t)
    ent.bind('<Return>', lambda e: webbrowser.open(f"https://google.com/search?q={v.get()}"))

def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    canvas.create_text(350, 220, text="Personalization", font=('Segoe UI', 12, 'bold'), anchor='w', tags=t)
    wall_btn = canvas.create_rectangle(350, 250, 550, 290, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(450, 270, text="Change Wallpaper", tags=t)
    canvas.tag_bind(wall_btn, '<Button-1>', lambda e: [filedialog.askopenfilename(), draw_background()])

def open_shooter_game(e=None):
    global shooter_game_running
    tag = create_window('Space Shooter', '#000022')
    if not tag: return
    shooter_game_running = True
    score, player, bullets, enemies = [0], [650, 560], [], []
    def fire(e=None): bullets.append([player[0], player[1] - 20])
    def update():
        if not shooter_game_running or not canvas.find_withtag(tag): return
        if random.random() < 0.05: enemies.append([random.randint(320, 980), 200])
        canvas.delete('shooter_obj')
        canvas.create_polygon(player[0], player[1]-20, player[0]-20, player[1]+20, player[0]+20, player[1]+20, fill='#00ccff', tags=(tag, 'shooter_obj'))
        for b in bullets[:]:
            b[1] -= 15
            if b[1] < 200: bullets.remove(b)
            else: canvas.create_rectangle(b[0]-2, b[1]-8, b[0]+2, b[1]+8, fill='yellow', tags=(tag, 'shooter_obj'))
        for e in enemies[:]:
            e[1] += 5
            canvas.create_oval(e[0]-15, e[1]-15, e[0]+15, e[1]+15, fill='red', tags=(tag, 'shooter_obj'))
            if e[1] > 600: close_window(tag, 'Space Shooter'); return
        root.after(30, update)
    root.bind('<Left>', lambda e: player.__setitem__(0, max(330, player[0]-20)))
    root.bind('<Right>', lambda e: player.__setitem__(0, min(970, player[0]+20)))
    root.bind('<space>', fire); update()

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    canvas.create_text(320, 210, text="GaiaCore Kernel v1.0.4\nroot@pearos:~$ ", anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)

def open_music_player(e=None):
    t = create_window('Pear Tunes', '#1e1e1e')
    if not t: return
    canvas.create_text(650, 300, text="🎵 Pear Tunes", fill='white', font=('Segoe UI', 20), tags=t)

def open_finder(e=None, path='.'):
    t = create_window('Finder', '#f9f9f9')
    if not t: return
    canvas.create_text(320, 210, text=f"🏠 {os.path.abspath(path)}", anchor='nw', tags=t)

def open_snake(e=None):
    global snake_game_running
    tag = create_window('Snake Sphere', 'black')
    if not tag: return
    snake_game_running = True
    def move():
        if snake_game_running and canvas.find_withtag(tag): root.after(100, move)
    move()

def open_apple_catcher(e=None):
    tag = create_window('Apple Catcher', '#fce4ec')
    if not tag: return

# ============================================
# BOOT SEQUENCE
# ============================================
def init_bubbles():
    global bubbles
    blue_shades = ['#00008b', '#0000cd', '#4169e1', '#191970', '#0000ff']
    for _ in range(25):
        size = random.randint(8, 28)
        x, y = random.randint(50, screen_w - 50), random.randint(screen_h, screen_h + 500)
        b = canvas.create_oval(x, y, x+size, y+size, outline='#87cefa', fill=random.choice(blue_shades), stipple='gray25', tags='bubbles')
        bubbles.append({'id': b, 'x': x, 'y': y, 'size': size, 'speed': random.uniform(1.2, 3.5)})

def animate_bubbles():
    for b in bubbles:
        b['y'] -= b['speed']
        if b['y'] < -50: b['y'] = screen_h + 50
        canvas.coords(b['id'], b['x'], b['y'], b['x']+b['size'], b['y']+b['size'])
    root.after(16, animate_bubbles)

def boot():
    global progress
    canvas.delete('boot')
    progress += 5
    cx, cy = screen_w // 2, screen_h // 2
    canvas.create_rectangle(cx-250, cy+135, cx+250, cy+170, outline='white', tags='boot')
    canvas.create_rectangle(cx-248, cy+137, cx-248+(progress*5), cy+168, fill=data_cell_green, outline='', tags='boot')
    canvas.create_text(cx, cy-75, text='🍐', fill='white', font=('Arial', 120), tags='boot')
    canvas.create_text(cx, cy+75, text='GAIASPHERE HD 2026', fill='white', font=('Segoe UI', 14, 'bold'), tags='boot')
    if progress < 100: root.after(50, boot)
    else: canvas.delete('boot'); draw_background(); redraw_ui_overlay(); init_bubbles(); animate_bubbles()

boot()
root.mainloop()