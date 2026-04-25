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
aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# ============================================
# HD BACKGROUND & UI ENGINE
# ============================================
def draw_default_gradient():
    """Integrated HD Gradient Engine with GaiaSphere Glass-morphism"""
    # HD Sky Gradient (Deep Blue to Aero Light Blue)
    for i in range(600):
        r = int(51 + (102 - 51) * (i / 600))
        g = int(153 + (204 - 153) * (i / 600))
        b = int(255)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 1400, i, fill=color, tags='bg')

    # HD Grass/Ground Gradient
    for i in range(250):
        y = 600 + i
        r = int(68 + (34 - 68) * (i / 250))
        g = int(221 + (153 - 221) * (i / 250))
        b = int(68 + (34 - 68) * (i / 250))
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, y, 1400, y, fill=color, tags='bg')

    # THE GAIASPHERE (HD Glass-morphism Effect)
    # Outer Glow
    canvas.create_oval(290, 90, 1110, 710, outline='#ffffff', width=1, stipple='gray12', tags='bg')
    # Main Sphere with Aero Blue Light
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=4, stipple='gray50', tags='bg')
    # High-light Shine (Simulates HD depth)
    canvas.create_oval(450, 150, 750, 300, fill='#ffffff', outline='', stipple='gray25', tags='bg')

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
        canvas.create_rectangle(0, 0, 1400, 850, fill='black', stipple='gray25', tags='bg')

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
        ('🌐', 'Web', lambda e: webbrowser.open("https://google.com")),
        ('⚙️', 'Settings', open_settings), 
        ('🎵', 'Pear Tunes', open_music_player),
        ('🐍', 'Snake', open_snake), 
        ('🍎', 'Catcher', open_apple_catcher), 
        ('🔫', 'Shooter', open_pear_shooter),
        ('📟', 'Terminal', open_terminal), 
        ('🍐', 'About', lambda e: messagebox.showinfo("Pear OS", "Ultimate GaiaSphere 2026\nHD Media Integrated Edition"))
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 220 + i * 115
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 32), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

# ============================================
# FX & BUBBLE SYSTEMS
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

def init_bubbles():
    global bubbles
    bubbles = []
    for _ in range(25):
        size = random.randint(8, 28)
        x = random.randint(50, 1350)
        y = random.randint(700, 1200)
        speed = random.uniform(1.2, 3.5)
        b = canvas.create_oval(x, y, x+size, y+size, outline='#ffffff', width=1, fill='white', stipple='gray25', tags='ui')
        bubbles.append({'id': b, 'x': x, 'y': y, 'size': size, 'speed': speed})

def animate_bubbles():
    for b in bubbles:
        b['y'] -= b['speed']
        if b['y'] < -50:
            b['y'] = 850
            b['x'] = random.randint(50, 1350)
        canvas.coords(b['id'], b['x'], b['y'], b['x']+b['size'], b['y']+b['size'])
    root.after(16, animate_bubbles)

# ============================================
# APPS & WINDOW MANAGER
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
    canvas.delete(tag)
    if title in open_apps: open_apps.pop(title)
    draw_background()
    redraw_ui_overlay()

def open_music_player(e=None):
    t = create_window('Pear Tunes', '#1e1e1e')
    if not t: return
    canvas.create_text(650, 250, text="🎵", font=('Arial', 80), fill=aero_blue_light, tags=t)
    song_label = canvas.create_text(650, 350, text="No Song Loaded", fill='white', font=('Segoe UI', 12), tags=(t, 'song_name'))
    
    def load_music():
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if path:
            filename = os.path.basename(path)
            canvas.itemconfig(song_label, text=f"Playing: {filename}")
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    load_btn = canvas.create_rectangle(550, 420, 750, 460, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(650, 440, text="Add Music File", fill='black', font=('Segoe UI', 10, 'bold'), tags=t)
    canvas.tag_bind(load_btn, '<Button-1>', lambda e: load_music())

def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return
    log = ["PearOS GaiaSphere HD Terminal", "Type 'help' for commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, borderwidth=0)
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    def process(event):
        cmd = cmd_var.get().lower()
        log.append(f"> {cmd}")
        if cmd == 'help': log.append("Commands: music, exit")
        elif cmd == 'music': open_music_player()
        canvas.itemconfig(log_text, text="\n".join(log[-15:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)
    cmd_entry.focus_set()

def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    def upload_bg():
        global custom_bg_path
        path = filedialog.askopenfilename(filetypes=[("Image", "*.jpg *.png *.bmp")])
        if path:
            custom_bg_path = path
            draw_background(); redraw_ui_overlay()
    btn = canvas.create_rectangle(500, 250, 700, 290, fill=aero_blue_light, tags=t)
    canvas.create_text(600, 270, text="Change Wallpaper", tags=t)
    canvas.tag_bind(btn, '<Button-1>', lambda e: upload_bg())

def open_system(e=None):
    t = create_window('System Diagnostics', '#f8f9fa')
    if not t: return
    cpu_label = canvas.create_text(330, 255, text="CPU Usage: 0%", font=('Consolas', 11), anchor='w', tags=t)
    def update():
        if canvas.find_withtag(t):
            canvas.itemconfig(cpu_label, text=f"CPU Usage: {random.randint(5,25)}%")
            root.after(2000, update)
    update()

def open_snake(e=None): create_window('Snake Sphere', 'black')
def open_apple_catcher(e=None): create_window('Apple Catcher', 'white')
def open_pear_shooter(e=None): create_window('Pear Shooter', '#121212')

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