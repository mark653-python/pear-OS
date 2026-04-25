import tkinter as tk
from tkinter import font as tkfont
import json

# --- 1. System Setup & Configuration ---
root = tk.Tk()
root.title("Pear OS - Interactive GaiaSphere Edition")
root.geometry("1400x850")
root.resizable(False, False)
root.configure(bg='black')

# Create the canvas and paint the new background scene
canvas = tk.Canvas(root, width=1400, height=850, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Define a palette derived from the target image
aero_blue_dark = '#0055ff'
aero_blue_light = '#66ccff'
grass_green = '#228822'
data_pearl_white = '#ffffff'
data_cell_green = '#66ff99'

# Set up some custom fonts for an integrated look
default_font = tkfont.Font(family="Segoe UI", size=10)
title_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
os_font = tkfont.Font(family="Segoe UI", size=48, weight="bold")
pearl_font = tkfont.Font(family="Arial", size=120)

# --- 2. Global State Variables ---
progress = 0
bubbles = []
open_apps = {}  # Track open app windows for click handling
icon_ids = {} # To keep track of dock icon IDs for making them clickable

# --- 3. Enhanced Boot Sequence ---
# Start by creating a centered, simplified graphic on a black background
logo = canvas.create_text(700, 350, text='🍐', fill='white', font=pearl_font, tags="boot")
status = canvas.create_text(700, 500, text='Initializing GaiaCore...', fill='white', font=('Segoe UI', 28), tags="boot")
bar_bg = canvas.create_rectangle(450, 560, 950, 595, outline='white', width=2, tags="boot")
bar_fill = canvas.create_rectangle(452, 562, 452, 593, fill=data_cell_green, outline='', tags="boot")

def boot():
    global progress
    progress += 4
    canvas.coords(bar_fill, 452, 562, 452 + progress * 5, 593)

    msgs = [
        'Syncing GaiaSphere Feed...',
        'Compiling Aero Core v1.0...',
        'Optimizing Data-Pearls...',
        'Calibrating Green Hills...',
        'Initializing interactive OS...'
    ]
    msg_index = min(progress // 20, len(msgs) - 1)
    canvas.itemconfig(status, text=msgs[msg_index])

    if progress < 100:
        root.after(80, boot)
    else:
        root.after(1000, login)

# --- 4. Interactive Login Screen ---
def login():
    canvas.delete('all')
    canvas.configure(bg=aero_blue_light)

    # Simple background gradient
    for i in range(850):
        c = min(255, 150 + i // 5)
        color = f'#66cc{c:02x}'
        canvas.create_line(0, i, 1400, i, fill=color)

    # Login details
    canvas.create_text(700, 180, text='Syncing to GaiaSphere', font=os_font, fill='white')
    btn = canvas.create_rectangle(600, 600, 800, 660, fill='white', outline='white', width=2)
    txt = canvas.create_text(700, 630, text='Establish Connection', font=('Segoe UI', 20), fill='#333')

    # Make the entire connection area clickable
    for item in [btn, txt]:
        canvas.tag_bind(item, '<Button-1>', lambda e: desktop())

# --- 5. Redesigned Desktop & Interface ---
def desktop():
    root.unbind('<Button-1>') # Unbind the general screen click
    canvas.delete('all')

    # --- Static Background Scene: Paint the scene directly with enhanced fidelity ---
    # The new procedurally painted world
    # Sky
    for i in range(850):
        c = min(255, 100 + i // 4)
        canvas.create_line(0, i, 1400, i, fill=f'#3399{c:02x}')

    # Distant Gaiasphere
    gaiasphere_fill = '#33ccff' # Soft, slightly transparent blue
    canvas.create_oval(300, 100, 1100, 700, fill=gaiasphere_fill, outline=aero_blue_light, width=3, stipple='gray50')

    # Green Hills and waterway
    for i in range(250):
        c = min(255, 120 + i // 2)
        canvas.create_line(0, 600+i, 1400, 600+i, fill=f'#{c:02x}dd{c:02x}')

    # Treeline
    canvas.create_oval(-100, 550, 400, 750, fill=grass_green, outline='')
    canvas.create_oval(300, 530, 800, 680, fill=grass_green, outline='')
    canvas.create_oval(1000, 560, 1500, 720, fill=grass_green, outline='')

    # Waterway and butterfly
    canvas.create_rectangle(500, 680, 900, 850, fill=aero_blue_dark, outline='')
    canvas.create_text(700, 760, text='🦋', font=('Arial', 60))

    # --- UI Elements: Functional and integrated ---
    canvas.create_text(250, 140, text='GaiaCore OS', font=os_font, fill='white')
    canvas.create_text(700, 50, text='Active Session | Press Esc to disconnect', font=default_font, fill='white')

    # App Icons (Right side)
    desktop_icons = [(250, 'System Network', '🌎', open_sys_info), (360, 'Recycle Bin', '🗑️', open_about)]
    for y, name, icon, func in desktop_icons:
        icon_id = canvas.create_text(1280, y, text=icon, font=('Arial', 40))
        canvas.tag_bind(icon_id, '<Button-1>', func)
        canvas.create_text(1280, y + 45, text=name, font=('Segoe UI', 12, 'bold'), fill='white')

    # --- Redesigned Glassy Dock: More integrated and functional ---
    # The base of interlocking "data-cells"
    # Using multiple translucent layers to create depth
    canvas.create_rectangle(350, 760, 1100, 825, fill='white', outline='white', stipple='gray50', width=2)
    canvas.create_rectangle(350, 760, 1100, 825, fill=data_cell_green, outline='white', stipple='gray25')

    # Define the apps: (Icon, Name, Click Function)
    apps_data = [
        ('🖥️', 'Gaiasphere', open_sys_info),
        ('🌐', 'PearWeb', open_browser),
        ('📁', 'Data_Pearl_Manager', open_finder),
        ('🎵', 'Core_Rhythms', open_music),
        ('⚙️', 'Calibration_Panel', open_settings),
        ('🍐', 'GaiaCore', open_about)
    ]

    global icon_ids
    icon_ids = {}

    for i, (icon, name, func) in enumerate(apps_data):
        x = 430 + i * 110
        # The icon pearl
        icon_pearl_id = canvas.create_text(x, 792, text=icon, font=('Arial', 38))
        icon_ids[name] = icon_pearl_id # Store the ID
        canvas.tag_bind(icon_pearl_id, '<Button-1>', func)

        # The data-pearl label with dynamic effect
        label_pearl = canvas.create_text(x, 835, text=name, font=('Segoe UI', 9), fill='white', tags="dock_pearl")
        canvas.tag_bind(label_pearl, '<Button-1>', func)

    # --- 6. New Dynamic Bubble Animation: Integrates the high-fidelity effect ---
    # Using more dynamic particles to achieve the target image's look
    global bubbles
    bubbles = []
    # Using more bubbles for a richer effect
    for i in range(25):
        x = 100 + i * (1200 / 25) + 50
        # More varied start height for a flowing pattern
        y = 700 + (i % 5) * 20
        # Creating layered iridescent bubbles
        iridescent_layer = canvas.create_oval(0, 0, 18, 18, fill='', outline=aero_blue_light, width=2)
        bubble_outline = canvas.create_oval(0, 0, 20, 20, fill='', outline='white', width=1)
        bubbles.append([bubble_outline, x, y, iridescent_layer])

    animate_bubbles()

    # --- 7. Window Management System ---
    # Global to manage window interaction (e.g., closing a single window)
    global close_handlers
    close_handlers = {}

def create_window(title, color="#ffffff"):
    # Prevent multiple windows of the same app
    if title in open_apps:
        # If open, highlight its dock icon pearl
        canvas.itemconfig(icon_ids[title], fill=aero_blue_light)
        root.after(300, lambda: canvas.itemconfig(icon_ids[title], fill='black'))
        return
    open_apps[title] = True

    # Use unique tags based on title for targeted close/delete
    tag = title.replace(" ", "")

    # Define common aer-aesthetic visual parameters for the windows
    header_fill = '#44ee44' # Soft translucent green
    soft_glow_outline = '#66ff99'

    # --- Base layers for the integrated visual effect ---
    # Shadow/Border for depth
    canvas.create_rectangle(305, 155, 1005, 605, fill='black', stipple='gray25', outline='', tags=tag)
    # The core, defined white content area
    canvas.create_rectangle(300, 150, 1000, 600, fill=color, outline='white', width=2, tags=tag)

    # --- Intergrated Title Bar with Aero glow ---
    canvas.create_rectangle(300, 150, 1000, 190, fill=header_fill, outline=soft_glow_outline, stipple='gray75', tags=tag)
    canvas.create_text(650, 170, text=title, font=title_font, fill='white', tags=tag)

    # The integrated Pearl OS "About" watermark
    canvas.create_text(1010, 610, text='🍐 GaiaCore OS', font=('Segoe UI', 8), justify='left', anchor='se', fill='#aaa', tags=tag)

    # The functional data-pearl button to close
    # Using a soft green data-pearl with a subtle 'x'
    close_button = canvas.create_oval(310, 160, 330, 180, fill=data_cell_green, outline='white', tags=tag)
    canvas.create_text(320, 170, text='×', font=('Arial', 10, 'bold'), fill='white', tags=tag)
    # Add a data-pearl glow on hover
    # (Simplified for this format, but possible with more complex logic)

    # Add targeted close logic and ensure the window interaction is correct
    canvas.tag_bind(close_button, '<Button-1>', lambda e: close_window(tag, title))

    return tag

def close_window(tag, title):
    canvas.delete(tag)
    # Re-enable app logic
    if title in open_apps:
        del open_apps[title]

# --- 8. The "Data-Pearls" (The functional apps) ---
def open_browser(e):
    tag = create_window("PearWeb Explorer")
    if not tag: return

    # Redesign for integrated GaiaCore look
    canvas.create_text(650, 240, text="Establishing Core Link...", font=title_font, fill=grass_green, justify='center', tags=tag)
    # The interactive "GaiaSphere" search bar
    canvas.create_rectangle(350, 280, 950, 310, fill=aero_blue_light, outline=data_cell_green, stipple='gray50', width=2, tags=tag)
    # The interactive 'GaiaSearch' button
    btn_pearl = canvas.create_oval(880, 285, 940, 305, fill='white', outline=aero_blue_light, width=2, tags=tag)
    txt_pearl = canvas.create_text(910, 295, text='GaiaSearch', font=('Segoe UI', 10), fill='#333', tags=tag)

    # The search term 'GaiaSphere feed' with interactive hint
    canvas.create_text(360, 295, text="://gaiasphere.feed (Query active)", anchor='w', font=('Courier New', 11), fill='#ddd', tags=tag)
    canvas.create_text(360, 320, text="(Click pearl to initiate data query)", anchor='w', font=('Segoe UI', 9), fill='#aaa', tags=tag)

    # Binding search button
    for item in [btn_pearl, txt_pearl]:
        canvas.tag_bind(item, '<Button-1>', lambda e: canvas.itemconfig(910, text="Querying..."))

def open_finder(e):
    tag = create_window("Data Pearl Manager", "#ddffff")
    if not tag: return
    folders_data = [('Documents', 'Data_Archive_v12'), ('Pictures', 'GAIA_Imaging_v2'), ('Downloads', 'Sync_Log_8a'), ('Pear_Work', 'AeroCore_v1.0')]
    for i, (name, core_id) in enumerate(folders_data):
        x = 400 + (i % 2) * 250
        y = 300 + (i // 2) * 150
        pearl_icon = canvas.create_text(x, y, text='📁', font=('Arial', 50), tags=tag)
        canvas.create_text(x, y+50, text=name, font=default_font, tags=tag)
        canvas.create_text(x, y+70, text=core_id, font=('Segoe UI', 8), fill='#888', tags=tag)

def open_music(e):
    tag = create_window("Core Rhythms")
    if not tag: return
    # Redesign to feel like an Aero Core simulation
    canvas.create_text(650, 300, text="Calibrating Rhythms", font=title_font, justify='center', tags=tag)
    canvas.create_text(650, 330, text="AeroCore Simulation v1.0", font=('Segoe UI', 12), fill='#888', tags=tag)

    canvas.create_text(650, 420, text="Now Syncing: Syncing with Gaiasphere.core", font=default_font, tags=tag)
    canvas.create_rectangle(450, 480, 850, 490, fill='#eee', outline='#bbb', tags=tag)
    canvas.create_rectangle(450, 480, 600, 490, fill=data_cell_green, outline='', tags=tag) # Progress

def open_settings(e):
    tag = create_window("Calibration Panel", "#f5f5f5")
    if not tag: return
    settings_items = [
        ('Calibration', 'AeroCore Display Calib.'),
        ('Gaiasphere', 'Gaiasphere Data Sync (Connected)'),
        ('Sound', 'Core_Rhythms Calibration'),
        ('OS v1.0', 'Active Session']
    for i, (label, value) in enumerate(settings_items):
        canvas.create_text(450, 250 + i * 50, text=label, font=('Segoe UI', 12, 'bold'), anchor='w', tags=tag)
        # Create interactive value pearls
        btn = canvas.create_oval(750, 240 + i * 50, 950, 260 + i * 50, fill='white', outline='#aaa', tags=tag)
        canvas.create_text(850, 250 + i * 50, text=value, font=default_font, fill='#333', tags=tag)
        # Binding example setting
        if label == 'Display Calibration':
            canvas.tag_bind(btn, '<Button-1>', lambda e: canvas.itemconfig(850, text='Display re-sync...'))

def open_sys_info(e):
    tag = create_window("System Diagnostics")
    if not tag: return
    # The central, clickable Gaiasphere pear logo
    pearl_logo = canvas.create_text(650, 350, text="🍐", font=pearl_font, fill=data_cell_green, tags=tag)
    canvas.create_text(650, 380, text="System: GaiaCore OS v1.0\nMemory: 8.0 GB Data Pearls\nProcessor: P1 Data Core", font=title_font, justify='center', tags=tag)

def open_about(e):
    tag = create_window("About GaiaSphere OS")
    if not tag: return
    canvas.create_text(650, 380, text="Aero Aesthetics Simulation\nBuilt on the original Pear OS logic\nIntegrated with the request to simulate the target image environment\nv1.0 Interactive Edition", justify='center', tags=tag)

# --- 9. Enhanced Animation Logic ---
def animate_bubbles():
    for b in bubbles:
        item_outline, x, y, item_iridescent = b
        # Faster, varied rise effect and dynamic movement
        y -= (1 + (b[0] % 3)) # Variation in speed based on outline ID
        x += ((b[3] % 2) - 1) * 0.2 # Slight wobble based on layer ID

        if y < 50:
            y = 800
        canvas.coords(item_outline, x, y, x+20, y+20)
        canvas.coords(item_iridescent, x+1, y+1, x+19, y+19)
        b[2] = y
        b[1] = x
    root.after(40, animate_bubbles)

# Bind Escape key to disconnect (shutdown) simulation
root.bind('<Escape>', lambda e: root.destroy())

# --- Start! ---
boot()
root.mainloop()