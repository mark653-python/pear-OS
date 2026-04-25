import tkinter as tk
from tkinter import font as tkfont
import random

# --- 1. System Setup ---
root = tk.Tk()
root.title("Pear OS - Ultimate GaiaSphere Edition")
root.geometry("1400x850")
root.resizable(False, False)
root.configure(bg='black')

canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- 2. Styling & State ---
aero_blue_light = '#66ccff'
data_cell_green = '#66ff99'
grass_green = '#228822'

progress = 0
bubbles = []
open_apps = {} 
snake_game_running = False

# --- 3. Boot & Login ---
def boot():
    global progress
    canvas.delete("boot_bar")
    progress += 4
    
    canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2, tags="boot_bar")
    canvas.create_rectangle(452, 562, 452 + progress * 5, 593, fill=data_cell_green, outline='', tags="boot_bar")

    msgs = ['Syncing GaiaSphere...', 'Compiling Aero Core...', 'Loading Desktop...', 'Welcome.']
    msg_index = min(progress // 30, len(msgs) - 1)
    
    canvas.delete("status_text")
    canvas.create_text(700, 500, text=msgs[msg_index], fill='white', font=('Segoe UI', 24), tags=("boot_bar", "status_text"))
    canvas.create_text(700, 350, text='🍐', fill='white', font=('Arial', 120), tags="boot_bar")

    if progress < 100:
        root.after(60, boot)
    else:
        root.after(500, login)

def login():
    canvas.delete('all')
    for i in range(850):
        c = min(255, 150 + i // 5)
        canvas.create_line(0, i, 1400, i, fill=f'#66cc{c:02x}')

    canvas.create_text(700, 180, text='Syncing to GaiaSphere', font=('Segoe UI', 48, 'bold'), fill='white')
    btn = canvas.create_rectangle(600, 550, 800, 610, fill='white', outline='white', width=2)
    txt = canvas.create_text(700, 580, text='Establish Connection', font=('Segoe UI', 16), fill='#333')

    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# --- 4. Desktop Logic ---
def desktop():
    canvas.delete('all')
    
    for i in range(850):
        c = min(255, 100 + i // 4)
        canvas.create_line(0, i, 1400, i, fill=f'#3399{c:02x}') 

    canvas.create_oval(300, 100, 1100, 700, fill='#33ccff', outline=aero_blue_light, width=3, stipple='gray50') 
    
    for i in range(250):
        c = min(255, 120 + i // 2)
        canvas.create_line(0, 600+i, 1400, 600+i, fill=f'#{c:02x}dd{c:02x}') 

    canvas.create_rectangle(320, 760, 1130, 825, fill='white', outline='white', stipple='gray50', width=2)
    
    apps_data = [
        ('🖥️', 'System', open_sys_info),
        ('🌐', 'PearWeb', open_browser),
        ('📁', 'Finder', open_finder),
        ('🎵', 'Music', open_music),
        ('🐍', 'Snake', open_snake),
        ('⚙️', 'Settings', open_settings),
        ('🍐', 'About', open_about)
    ]

    for i, (icon, name, func) in enumerate(apps_data):
        x = 380 + i * 110
        id = canvas.create_text(x, 792, text=icon, font=('Arial', 38))
        canvas.tag_bind(id, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, font=('Segoe UI', 9), fill='white')

    global bubbles
    for i in range(20):
        b = canvas.create_oval(0, 0, 18, 18, outline='white', width=1)
        bubbles.append([b, 100 + i * 65, 750])
    
    animate_bubbles()
    root.bind('<Escape>', lambda e: root.destroy())

# --- 5. Windowing System ---
def create_window(title, color="#ffffff"):
    if title in open_apps: return None
    open_apps[title] = True
    tag = title.replace(" ", "")

    canvas.create_rectangle(305, 155, 1