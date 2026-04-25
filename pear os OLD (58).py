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
progress = 0
bubbles = []
open_apps = {}
snake_game_running = False
catcher_game_running = False

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
            draw_background()
    dance()

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
    if title in open_apps: open_apps.pop(title)
    if 'Snake' in title: snake_game_running = False
    if 'Apple Catcher' in title: catcher_game_running = False

# ============================================
# UPDATED SETTINGS APP
# ============================================
def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return

    # Sidebar Navigation
    canvas.create_rectangle(300, 190, 450, 600, fill='#e0e0e0', outline='', tags=t)
    
    categories = ["Appearance", "Network", "Privacy", "System"]
    content_tags = f"{t}_content"

    def show_category(cat):
        canvas.delete(content_tags)
        
        if cat == "Appearance":
            canvas.create_text(470, 230, text="Personalization", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            # Theme Toggle
            aero_btn = canvas.create_rectangle(470, 270, 600, 310, fill='#66ccff', outline='white', tags=(t, content_tags))
            canvas.create_text(535, 290, text="Aero Blue", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(aero_btn, '<Button-1>', lambda e: set_theme("Aero"))

            dark_btn = canvas.create_rectangle(620, 270, 750, 310, fill='#333333', outline='white', tags=(t, content_tags))
            canvas.create_text(685, 290, text="Dark Mode", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(dark_btn, '<Button-1>', lambda e: set_theme("Dark"))

        elif cat == "Network":
            canvas.create_text(470, 230, text="Network & Internet", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            canvas.create_text(470, 270, text="Wi-Fi: Connected (Gaia_5G)\nVPN: Disconnected", font=('Segoe UI', 11), anchor='nw', tags=(t, content_tags))
            ping_btn = canvas.create_rectangle(470, 340, 600, 380, fill='#66b3ff', outline='white', tags=(t, content_tags))
            canvas.create_text(535, 360, text="Test Ping", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(ping_btn, '<Button-1>', lambda e: messagebox.showinfo("Network", "Pinging iCarly.com... 24ms"))

        elif cat == "Privacy":
            canvas.create_text(470, 230, text="Privacy & Security", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            audit_btn = canvas.create_rectangle(470, 270, 650, 310, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(560, 290, text="Audit Google Safety", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(audit_btn, '<Button-1>', lambda e: messagebox.showinfo("Safety Center", "Auditing search history and ad tracking... All clear!"))
            
            canvas.create_text(470, 330, text="Best Practice: Auto-login is OFF\nScreen Timeout: 5 Minutes", font=('Segoe UI', 10, 'italic'), anchor='nw', tags=(t, content_tags))

        elif cat == "System":
            canvas.create_text(470, 230, text="System Information", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            info = "OS: GaiaSphere 1.0.4\nKernel: PearCore-Py\nResolution: 1400x850\nPrecedence: Workspace > Policy"
            canvas.create_text(470, 270, text=info, font=('Segoe UI', 11), anchor='nw', tags=(t, content_tags))

    def set_theme(mode):
        global current_theme
        if mode == "Aero":
            current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else:
            current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#000000', 'taskbar': '#333333'}
        draw_background()
        redraw_ui_overlay()
        messagebox.showinfo("Settings", f"Theme updated to {mode}!")

    # Draw Sidebar Buttons
    for i, cat in enumerate(categories):
        btn = canvas.create_text(375, 230 + (i * 50), text=cat, font=('Segoe UI', 12), tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e, c=cat: show_category(c))
    
    show_category("Appearance")

# ============================================
# SYSTEM APPS & DESKTOP
# ============================================
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
        elif cmd in ['party', 'dance']: trigger_dance()
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")
    cmd_entry.bind('<Return>', process)

def draw_background():
    canvas.delete('bg')
    for i in range(1200): canvas.create_line(0, i, 2000, i, fill=current_theme['bg_top'], tags='bg')
    for i in range(400): canvas.create_line(0, 600+i, 2000, 600+i, fill=current_theme['bg_bottom'], tags='bg')
    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(220, 760, 1280, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    apps = [
        ('⚙️', 'Settings', open_settings), ('📟', 'Terminal', open_terminal),
        ('🌐', 'PearWeb', lambda e: webbrowser.open("https://google.com")),
        ('📁', 'Finder', lambda e: messagebox.showinfo("Finder", "GaiaDrive Online")),
        ('🍐', 'About', lambda e: messagebox.showinfo("Pear OS", "Edition 2026\nby mark"))
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 450 + i * 140
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 38), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

def boot():
    global progress
    canvas.delete('boot')
    progress += 4
    canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2, tags='boot')
    canvas.create_rectangle(452, 562, 452 + progress * 5, 593, fill=data_cell_green, outline='', tags='boot')
    canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120), tags='boot')
    if progress < 100: root.after(60, boot)
    else:
        canvas.delete('all')
        draw_background()
        redraw_ui_overlay()

boot()
root.mainloop()