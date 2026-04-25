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
    # If a custom image exists, draw it; otherwise, draw theme colors
    if bg_image_obj:
        canvas.create_image(700, 425, image=bg_image_obj, tags='bg')
    else:
        for i in range(1200):
            canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
        for i in range(400):
            canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    
    # Frutiger Aero sphere overlay
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(220, 760, 1280, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    # Apps logic would follow here...

# ============================================
# SYSTEM APPS & SETTINGS
# ============================================
def open_settings(e=None):
    t = create_window('Settings', '#f0f0f0')
    if not t: return
    
    canvas.create_text(320, 220, text='Personalization', font=('Segoe UI', 14, 'bold'), anchor='w', tags=t)

    # Function to pick a custom image
    def choose_custom_bg():
        global bg_image_obj
        file_path = filedialog.askopenfilename(title="Select Background", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_obj = ImageTk.PhotoImage(img)
            draw_background()
            canvas.tag_lower('bg') 

    # Theme toggle logic
    def set_theme(mode):
        global current_theme, bg_image_obj
        bg_image_obj = None 
        if mode == "Aero": 
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else: 
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#333333', 'taskbar': '#444444'}
        draw_background()
        redraw_ui_overlay()
        canvas.tag_lower('bg')

    # UI Buttons for Theme and Custom Image
    btn_aero = canvas.create_rectangle(320, 280, 420, 310, fill='#66ccff', outline='white', tags=t)
    canvas.create_text(370, 295, text="Aero Blue", tags=t)
    canvas.tag_bind(btn_aero, '<Button-1>', lambda e: set_theme("Aero"))

    btn_custom = canvas.create_rectangle(440, 280, 560, 310, fill=data_cell_green, outline='white', tags=t)
    canvas.create_text(500, 295, text="Custom Image", tags=t)
    canvas.tag_bind(btn_custom, '<Button-1>', lambda e: choose_custom_bg())

def open_about(e=None):
    t = create_window('About')
    if t:
        # Updated About text including "by mark"
        about_text = "pear OS Frutiger Edition 2026\nSimulation Core Built With Python + Tkinter\nby mark"
        canvas.create_text(650, 350, text=about_text, justify='center', font=('Segoe UI', 18, 'bold'), tags=t)

# ============================================
# TERMINAL
# ============================================
def open_terminal(e=None):
    t = create_window('Pear Command Prompt', '#1a1a1a')
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
            # Includes 'whoami' and 'cmd'
            log.append("Available: help, ls, date, clear, i-ready, random-dancing, cmd, whoami")
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
        elif cmd == 'cmd':
            log.append("Pear Command Line Interface [Version 1.0.4]")
        elif cmd == 'whoami':
            log.append("User: mark | Role: GaiaSphere Administrator")
        else:
            log.append(f"Command not found: {cmd}")
        
        canvas.itemconfig(log_text, text="\n".join(log[-15:]))
        cmd_var.set("")

    cmd_entry.bind('<Return>', process_command)

# Rest of the OS infrastructure (desktop(), create_window(), etc.) goes here...
boot()
root.mainloop()