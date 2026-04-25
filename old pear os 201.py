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
phantom_game_running = False
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
    tb_width = 1250
    tb_x1 = max(50, (screen_w - tb_width) / 2)
    tb_x2 = min(screen_w - 50, (screen_w + tb_width) / 2)

    canvas.create_rectangle(tb_x1, tb_y1, tb_x2, tb_y2, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

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
        ('👻', 'Phantom', open_phantom_game),
        ('📟', 'Terminal', open_terminal), 
        ('🐙', 'GitHub', open_github),
        ('🍐', 'About', lambda e: messagebox.showinfo("About", "fake pear OS sim by mark on github"))
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
    
    # Disable dragging for games to keep internal coordinates accurate
    if 'Snake' not in title and 'Shooter' not in title and 'Apple' not in title and 'Phantom' not in title:
        canvas.tag_bind(title_tag, '<ButtonPress-1>', lambda e, t=tag: start_drag(e, t))
        canvas.tag_bind(title_tag, '<B1-Motion>', drag)
        canvas.tag_bind(title_tag, '<ButtonRelease-1>', lambda e: drag_data.update({"tag": None}))
    return tag

def close_window(tag, title):
    global snake_game_running, catcher_game_running, shooter_game_running, phantom_game_running
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)
    snake_game_running = catcher_game_running = shooter_game_running = phantom_game_running = False
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
        ("Frutiger Aero Aesthetics", "7.2M views", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"), 
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
# OTHER APPS
# ============================================
def open_github(e=None):
    webbrowser.open("https://github.com/mark653-python/pear-OS")

def open_browser(e=None):
    t = create_window('PearWeb Explorer', '#ffffff')
    if not t: return
    
    font_style = ('Arial', 64, 'bold')
    
    canvas.create_text(495, 290, text='G', fill='#4285F4', font=font_style, tags=t)
    canvas.create_text(555, 300, text='o', fill='#EA4335', font=font_style, tags=t)
    canvas.create_text(610, 300, text='o', fill='#FBBC05', font=font_style, tags=t)
    canvas.create_text(665, 300, text='g', fill='#4285F4', font=font_style, tags=t)
    canvas.create_text(705, 290, text='l', fill='#34A853', font=font_style, tags=t)
    canvas.create_text(745, 300, text='e', fill='#EA4335', font=font_style, tags=t)

    v = tk.StringVar()
    ent = tk.Entry(root, textvariable=v, font=('Segoe UI', 14), width=45, relief='solid', bd=1, highlightbackground='#dfe1e5')
    canvas.create_window(630, 400, window=ent, tags=t)
    
    def execute_search(event=None):
        query = v.get().strip()
        if query:
            webbrowser.open(f"https://google.com/search?q={query}")
            
    btn_search = canvas.create_rectangle(490, 450, 615, 485, fill='#f8f9fa', outline='#f8f9fa', tags=(t, 'btn'))
    txt_search = canvas.create_text(552, 467, text='Google Search', font=('Arial', 10), fill='#3c4043', tags=(t, 'btn'))
    
    btn_lucky = canvas.create_rectangle(630, 450, 765, 485, fill='#f8f9fa', outline='#f8f9fa', tags=(t, 'btn'))
    txt_lucky = canvas.create_text(697, 467, text="I'm Feeling Lucky", font=('Arial', 10), fill='#3c4043', tags=(t, 'btn'))
    
    canvas.tag_bind(btn_search, '<Button-1>', execute_search)
    canvas.tag_bind(txt_search, '<Button-1>', execute_search)
    canvas.tag_bind(btn_lucky, '<Button-1>', execute_search)
    canvas.tag_bind(txt_lucky, '<Button-1>', execute_search)
    ent.bind('<Return>', execute_search)

def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    
    def set_theme(mode):
        global current_theme, custom_bg_path
        if mode == "Aero": 
            custom_bg_path = None 
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else: 
            custom_bg_path = None
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#000000', 'taskbar': '#333333'}
        draw_background(); redraw_ui_overlay()

    def upload():
        global custom_bg_path
        p = filedialog.askopenfilename(filetypes=[("Image", "*.jpg *.png")])
        if p: custom_bg_path = p; draw_background(); redraw_ui_overlay()

    canvas.create_text(350, 220, text="Personalization", font=('Segoe UI', 12, 'bold'), anchor='w', tags=t)
    
    aero_btn = canvas.create_rectangle(350, 250, 480, 290, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(415, 270, text="Aero Blue", fill='white', tags=t)
    canvas.tag_bind(aero_btn, '<Button-1>', lambda e: set_theme("Aero"))

    dark_btn = canvas.create_rectangle(500, 250, 630, 290, fill='#333333', outline='white', tags=t)
    canvas.create_text(565, 270, text="Dark Mode", fill='white', tags=t)
    canvas.tag_bind(dark_btn, '<Button-1>', lambda e: set_theme("Dark"))

    wall_btn = canvas.create_rectangle(350, 310, 630, 350, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(490, 330, text="Custom Wallpaper", tags=t)
    canvas.tag_bind(wall_btn, '<Button-1>', lambda e: upload())

    canvas.create_text(700, 220, text="Pear OS System Files", font=('Segoe UI', 12, 'bold'), anchor='w', tags=t)
    canvas.create_rectangle(700, 240, 950, 560, fill='white', outline='#cccccc', tags=t)
    
    try:
        files = os.listdir('.')
    except:
        files = ["Access Denied"]

    y_offset = 255
    for i, item in enumerate(files[:14]):
        icon = '📁' if os.path.isdir(item) else '📄'
        canvas.create_text(715, y_offset + (i * 20), text=f"{icon} {item[:28]}", anchor='w', font=('Segoe UI', 9), tags=t)
    
    if len(files) > 14:
        canvas.create_text(715, y_offset + (14 * 20), text=f"... and {len(files)-14} more", anchor='w', font=('Segoe UI', 9, 'italic'), fill='gray', tags=t)

def open_system(e=None):
    t = create_window('System Diagnostics', '#f8f9fa')
    if not t: return
    cpu = canvas.create_text(330, 255, text="CPU Usage: 0%", font=('Consolas', 11), anchor='w', tags=t)
    ram = canvas.create_text(330, 285, text="RAM Load: 0%", font=('Consolas', 11), anchor='w', tags=t)
    
    def upd():
        if canvas.find_withtag(t):
            c_val, r_val = random.randint(5,25), random.randint(30, 55)
            canvas.itemconfig(cpu, text=f"CPU Usage: {c_val}% [|||       ]")
            canvas.itemconfig(ram, text=f"RAM Load:  {r_val}% [|||||     ]")
            root.after(2000, upd)
    upd()

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, borderwidth=0, insertbackground=data_cell_green)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    
    def process(event):
        cmd = cmd_var.get().lower().strip()
        log.append(f"root@pearos:~$ {cmd}")
        if cmd == 'help': log.append("Commands: music, shake, party, ls, clear")
        elif cmd == 'ls': log.append("Applications/  Games/  secret_pear_recipe.txt")
        elif cmd == 'party': trigger_dance()
        elif cmd == 'shake': shake_window()
        elif cmd == 'clear': log.clear(); log.append("Terminal Cleared.")
        canvas.itemconfig(log_text, text="\n".join(log[-15:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)
    cmd_entry.focus_set()

def open_finder(e=None, path='.'):
    abs_path = os.path.abspath(path)
    t = create_window(f'Finder - {os.path.basename(abs_path) or "Home"}', '#f9f9f9')
    if not t: return
    canvas.create_text(320, 210, text=f"🏠 {abs_path}", font=('Segoe UI', 10, 'bold'), anchor='nw', tags=t)
    try: files = os.listdir(path)
    except: files = ["Access Denied"]

    for i, item in enumerate(files[:12]):
        col, row = i % 4, i // 4
        x, y = 380 + (col * 150), 280 + (row * 120)
        icon = '📁' if os.path.isdir(os.path.join(path, item)) else '📄'
        canvas.create_text(x, y, text=icon, font=('Arial', 40), tags=t)
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
            pygame.mixer.music.load(p)
            pygame.mixer.music.play()

    btn = canvas.create_rectangle(550, 420, 750, 460, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(650, 440, text="Load Track", font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(btn, '<Button-1>', lambda e: load())

# ============================================
# GAMES
# ============================================

def open_phantom_game(e=None):
    global phantom_game_running
    tag = create_window('Phantom Hunt', '#0a0a0a')
    if not tag: return
    phantom_game_running = True
    
    score = [0]
    phantom_state = {"x": 0, "y": 0, "size": 0, "active": False}
    
    score_text = canvas.create_text(350, 220, text="Phantoms Banished: 0", font=('Segoe UI', 14, 'bold'), fill='#880000', tags=tag)
    
    def spawn_phantom():
        if not phantom_game_running or not canvas.find_withtag(tag): return
        phantom_state["x"] = random.randint(350, 950)
        phantom_state["y"] = random.randint(250, 550)
        phantom_state["size"] = 5
        phantom_state["active"] = True
    
    def click_phantom(event):
        if not phantom_game_running or not phantom_state["active"]: return
        px, py = phantom_state["x"], phantom_state["y"]
        s = phantom_state["size"]
        
        # Check if click is within bounds of the phantom
        if px - (s*1.5) <= event.x <= px + (s*1.5) and py - (s*1.5) <= event.y <= py + (s*1.5):
            phantom_state["active"] = False
            canvas.delete('phantom_obj')
            score[0] += 1
            canvas.itemconfig(score_text, text=f"Phantoms Banished: {score[0]}")
            # Spawn the next one faster as the game progresses
            root.after(max(200, random.randint(500, 2000) - (score[0] * 50)), spawn_phantom)

    def jumpscare(count=15):
        if count > 0 and canvas.find_withtag(tag):
            color = random.choice(['#ff0000', '#000000', '#ffffff'])
            canvas.create_rectangle(300, 190, 1000, 600, fill=color, tags=(tag, 'jump'))
            shake_window(2)
            root.after(40, lambda: jumpscare(count-1))
        else:
            messagebox.showinfo("YOU DIED", f"You survived {score[0]} phantoms before the darkness took you.")
            close_window(tag, 'Phantom Hunt')

    def update():
        if not phantom_game_running or not canvas.find_withtag(tag): return
        
        if phantom_state["active"]:
            canvas.delete('phantom_obj')
            px, py = phantom_state["x"], phantom_state["y"]
            s = phantom_state["size"]
            
            # Draw the phantom
            canvas.create_oval(px - s, py - s, px + s, py + s, fill='', outline='#aa0000', width=max(1, int(s/10)), tags=(tag, 'phantom_obj'))
            canvas.create_oval(px - s/2, py - s/4, px - s/4, py + s/4, fill='#ff0000', tags=(tag, 'phantom_obj'))
            canvas.create_oval(px + s/4, py - s/4, px + s/2, py + s/4, fill='#ff0000', tags=(tag, 'phantom_obj'))
            
            # Bind the click event to the phantom object
            canvas.tag_bind('phantom_obj', '<Button-1>', click_phantom)

            # Phantoms grow faster as you score more points
            phantom_state["size"] += 1.0 + (score[0] * 0.1)
            
            if phantom_state["size"] > 90:
                phantom_state["active"] = False
                jumpscare()
                return
                
        root.after(40, update)
        
    root.after(1500, spawn_phantom)
    update()

def open_shooter_game(e=None):
    global shooter_game_running
    tag = create_window('Space Shooter', '#000022')
    if not tag: return
    shooter_game_running = True
    score, player, bullets, enemies = [0], [650, 560], [], []
    score_text = canvas.create_text(350, 220, text="Score: 0", font=('Segoe UI', 14, 'bold'), fill='#00ff00', tags=tag)
    
    def fire(event=None):
        if shooter_game_running and canvas.find_withtag(tag): bullets.append([player[0], player[1] - 20])
            
    def update():
        if not shooter_game_running or not canvas.find_withtag(tag): return
        if random.random() < 0.05: enemies.append([random.randint(320, 980), 200])
            
        canvas.delete('shooter_obj')
        canvas.create_polygon(player[0], player[1]-20, player[0]-20, player[1]+20, player[0]+20, player[1]+20, fill='#00ccff', tags=(tag, 'shooter_obj'))
        
        for b in bullets[:]:
            b[1] -= 15
            if b[1] < 200: bullets.remove(b)
            else: canvas.create_rectangle(b[0]-3, b[1]-10, b[0]+3, b[1]+10, fill='#ffff00', tags=(tag, 'shooter_obj'))
                
        for e in enemies[:]:
            e[1] += 6
            if e[1] > 600:
                messagebox.showinfo("Game Over", f"Earth was invaded! Final Score: {score[0]}")
                close_window(tag, 'Space Shooter')
                return
            else: canvas.create_oval(e[0]-15, e[1]-15, e[0]+15, e[1]+15, fill='#ff0055', outline='white', tags=(tag, 'shooter_obj'))
                
        for b in bullets[:]:
            for e in enemies[:]:
                if abs(b[0] - e[0]) < 20 and abs(b[1] - e[1]) < 20:
                    if b in bullets: bullets.remove(b)
                    if e in enemies: enemies.remove(e)
                    score[0] += 10
                    canvas.itemconfig(score_text, text=f"Score: {score[0]}")
                    break 
                    
        root.after(30, update)
        
    root.bind('<Left>', lambda e: player.__setitem__(0, max(330, player[0]-20)))
    root.bind('<Right>', lambda e: player.__setitem__(0, min(970, player[0]+20)))
    root.bind('<space>', fire)
    update()

def open_apple_catcher(e=None):
    global catcher_game_running
    tag = create_window('Apple Catcher', '#fce4ec')
    if not tag: return
    catcher_game_running = True
    score, basket = [0], [650, 550]
    apples = [[random.randint(350, 950), 200] for _ in range(3)]
    score_text = canvas.create_text(350, 220, text="Apples: 0/10", font=('Segoe UI', 14, 'bold'), fill='#d81b60', tags=tag)
    
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
                p[1], p[0] = 200, random.randint(350, 950)
                if score[0] >= 10: 
                    messagebox.showinfo("Win", "Apple Harvest Complete!")
                    close_window(tag, 'Apple Catcher'); trigger_dance(); return
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
        if not snake_game_running or not canvas.find_withtag(tag): return
        h = list(snk[0])
        if dr == 'Up': h[1] -= 15
        elif dr == 'Down': h[1] += 15
        elif dr == 'Left': h[0] -= 15
        elif dr == 'Right': h[0] += 15
        
        if h[0] < 310 or h[0] > 990 or h[1] < 200 or h[1] > 590: 
            close_window(tag, 'Snake Sphere'); return
            
        snk.insert(0, h)
        if abs(h[0]-fd[0]) < 15 and abs(h[1]-fd[1]) < 15: 
            fd = [random.randint(350, 950), random.randint(250, 550)]
        else: 
            snk.pop()
            
        canvas.delete('snk_obj')
        for s in snk: 
            canvas.create_rectangle(s[0], s[1], s[0]+12, s[1]+12, fill=data_cell_green, tags=(tag, 'snk_obj'))
        canvas.create_oval(fd[0], fd[1], fd[0]+12, fd[1]+12, fill='red', tags=(tag, 'snk_obj'))
        root.after(100, move)

    root.bind('<w>', lambda e: set_dr('Up'))
    root.bind('<s>', lambda e: set_dr('Down'))
    root.bind('<a>', lambda e: set_dr('Left'))
    root.bind('<d>', lambda e: set_dr('Right'))
    def set_dr(new_dr): nonlocal dr; dr = new_dr
    move()

# ============================================
# BOOT SEQUENCE
# ============================================
def init_bubbles():
    global bubbles
    bubbles = []
    blue_shades = ['#00008b', '#0000cd', '#4169e1', '#191970', '#0000ff']
    
    for _ in range(25):
        size = random.randint(8, 28)
        x = random.randint(50, screen_w - 50)
        y = random.randint(screen_h, screen_h + 500)
        speed = random.uniform(1.2, 3.5)
        bubble_color = random.choice(blue_shades)
        
        b = canvas.create_oval(x, y, x+size, y+size, outline='#87cefa', width=1, fill=bubble_color, stipple='gray25', tags='bubbles')
        bubbles.append({'id': b, 'x': x, 'y': y, 'size': size, 'speed': speed})

def animate_bubbles():
    for b in bubbles:
        b['y'] -= b['speed']
        if b['y'] < -50: 
            b['y'] = screen_h + 50
            b['x'] = random.randint(50, screen_w - 50)
        canvas.coords(b['id'], b['x'], b['y'], b['x']+b['size'], b['y']+b['size'])
    root.after(16, animate_bubbles)

def boot():
    global progress
    canvas.delete('boot')
    progress += 5
    
    cx, cy = screen_w // 2, screen_h // 2
    bar_w = 500
    bar_x = cx - (bar_w // 2)
    bar_y = cy + 135
    
    canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + 35, outline='white', width=2, tags='boot')
    fill_w = int((progress / 100.0) * (bar_w - 4))
    canvas.create_rectangle(bar_x + 2, bar_y + 2, bar_x + 2 + fill_w, bar_y + 33, fill=data_cell_green, outline='', tags='boot')
    
    canvas.create_text(cx, cy - 75, text='🍐', fill='white', font=('Arial', 120), tags='boot')
    canvas.create_text(cx, cy + 75, text='GAIASPHERE HD 2026', fill='white', font=('Segoe UI', 14, 'bold'), tags='boot')
    
    if progress < 100: 
        root.after(50, boot)
    else:
        canvas.delete('all')
        draw_background()
        redraw_ui_overlay()
        init_bubbles()
        animate_bubbles()

boot()
root.mainloop()