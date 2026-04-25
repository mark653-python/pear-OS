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
bg_image_ref = None  # Prevents garbage collection of the image
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
    
    # 1. Draw the actual background (Custom or Gradient)
    if custom_bg_path:
        try:
            img = Image.open(custom_bg_path)
            img = img.resize((1400, 850), Image.Resampling.LANCZOS)
            bg_image_ref = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=bg_image_ref, anchor='nw', tags='bg')
        except Exception as e:
            draw_default_gradient()
    else:
        draw_default_gradient()

    # 2. Apply Dimming Effect if windows are open
    if open_apps:
        canvas.create_rectangle(0, 0, 1400, 850, fill='black', stipple='gray50', tags='bg')

def redraw_ui_overlay():
    canvas.delete('ui')
    canvas.create_rectangle(220, 760, 1280, 825, fill=current_theme['taskbar'], stipple='gray25', width=2, tags='ui')
    
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    canvas.tag_bind(dance_btn, '<Button-1>', trigger_dance)

    apps = [
        ('🖥️', 'System', open_system), ('🌐', 'PearWeb', lambda e: webbrowser.open("https://google.com")),
        ('📁', 'Finder', lambda e: messagebox.showinfo("Finder", "GaiaDrive Online")),
        ('⚙️', 'Settings', open_settings), ('🐍', 'Snake', open_snake), 
        ('🍎', 'Catcher', open_apple_catcher), ('📟', 'Terminal', open_terminal), 
        ('🍐', 'About', lambda e: messagebox.showinfo("Pear OS", "Ultimate GaiaSphere 2026\nby mark"))
    ]

    for i, (emoji, name, func) in enumerate(apps):
        x = 280 + i * 120
        obj = canvas.create_text(x, 792, text=emoji, font=('Arial', 38), tags='ui')
        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9), tags='ui')

# ============================================
# WINDOW MANAGER
# ============================================
def create_window(title, color='#ffffff'):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(' ', '').replace('-', '')

    # Apply dimming because a window is now open
    draw_background()
    
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
    
    # Redraw background to remove dim effect if no apps remain
    draw_background()
    redraw_ui_overlay()
    
    if 'Snake' in title: snake_game_running = False
    if 'Apple Catcher' in title: catcher_game_running = False

# ============================================
# SYSTEM APPS
# ============================================
def open_settings(e=None):
    t = create_window('System Settings', '#f0f0f0')
    if not t: return
    canvas.create_rectangle(300, 190, 450, 600, fill='#e0e0e0', outline='', tags=t)
    categories = ["Appearance", "Network", "Privacy", "System"]
    content_tags = f"{t}_content"

    def upload_bg():
        global custom_bg_path
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            custom_bg_path = path
            draw_background()
            redraw_ui_overlay() 
            messagebox.showinfo("Success", "Wallpaper updated!")

    def show_category(cat):
        canvas.delete(content_tags)
        if cat == "Appearance":
            canvas.create_text(470, 230, text="Personalization", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            
            # Theme Buttons
            aero_btn = canvas.create_rectangle(470, 270, 600, 310, fill='#66ccff', outline='white', tags=(t, content_tags))
            canvas.create_text(535, 290, text="Aero Blue", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(aero_btn, '<Button-1>', lambda e: set_theme("Aero"))
            
            dark_btn = canvas.create_rectangle(620, 270, 750, 310, fill='#333333', outline='white', tags=(t, content_tags))
            canvas.create_text(685, 290, text="Dark Mode", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(dark_btn, '<Button-1>', lambda e: set_theme("Dark"))

            # Custom Background Button
            upload_btn = canvas.create_rectangle(470, 330, 750, 370, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(610, 350, text="Upload Custom Background", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(upload_btn, '<Button-1>', lambda e: upload_bg())

        elif cat == "Network":
            canvas.create_text(470, 230, text="Network & Internet", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            canvas.create_text(470, 270, text="Wi-Fi: Connected (Gaia_5G)\nVPN: Disconnected", font=('Segoe UI', 11), anchor='nw', tags=(t, content_tags))
        elif cat == "Privacy":
            canvas.create_text(470, 230, text="Privacy & Security", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            audit_btn = canvas.create_rectangle(470, 270, 650, 310, fill='#44ee44', outline='white', tags=(t, content_tags))
            canvas.create_text(560, 290, text="Audit Safety", fill='white', font=('Segoe UI', 10, 'bold'), tags=(t, content_tags))
            canvas.tag_bind(audit_btn, '<Button-1>', lambda e: messagebox.showinfo("Safety", "System audit complete. No threats found."))
        elif cat == "System":
            canvas.create_text(470, 230, text="System Information", font=('Segoe UI', 16, 'bold'), anchor='w', tags=(t, content_tags))
            info = "OS: GaiaSphere 1.0.4\nKernel: PearCore-Py\nResolution: 1400x850"
            canvas.create_text(470, 270, text=info, font=('Segoe UI', 11), anchor='nw', tags=(t, content_tags))

    def set_theme(mode):
        global current_theme, custom_bg_path
        custom_bg_path = None # Reset custom bg when switching themes
        if mode == "Aero": current_theme = {'bg_top': '#3399ff', 'bg_bottom': '#44dd44', 'taskbar': 'white'}
        else: current_theme = {'bg_top': '#1a1a1a', 'bg_bottom': '#000000', 'taskbar': '#333333'}
        draw_background(); redraw_ui_overlay(); messagebox.showinfo("Settings", f"Theme: {mode}")

    for i, cat in enumerate(categories):
        btn = canvas.create_text(375, 230 + (i * 50), text=cat, font=('Segoe UI', 12), tags=t)
        canvas.tag_bind(btn, '<Button-1>', lambda e, c=cat: show_category(c))
    show_category("Appearance")

# ... (Include other apps like open_system, open_terminal, open_apple_catcher, open_snake from original script)
# [Omitted for brevity but should be pasted here in the full version]

# ============================================
# FX & BOOT
# ============================================
def trigger_dance(e=None):
    try:
        pygame.mixer.music.load("random_dancing.mp3")
        pygame.mixer.music.play()
    except: pass
    
    def dance(count=20):
        if count > 0:
            colors = ['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00']
            canvas.configure(bg=random.choice(colors))
            root.after(100, lambda: dance(count - 1))
        else:
            canvas.configure(bg='black')
            root.destroy()
    dance()

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
        draw_background(); redraw_ui_overlay(); init_bubbles(); animate_bubbles()

boot()
root.mainloop()