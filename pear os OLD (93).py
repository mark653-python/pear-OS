import tkinter as tk
from PIL import Image, ImageTk  # Add these imports

# --- Resource Loader Configuration ---
# Create a dictionary to hold the photo objects (to prevent garbage collection)
icon_images = {}

def load_icon(path, size=(50, 50)):
    """Loads a PNG, resizes it, and returns a Tkinter-compatible image object."""
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

# --- Modified Desktop Function Snippet ---
def desktop():
    # ... [previous background code] ...

    apps = [
        ('system.png', 'System', open_sys_info),
        ('browser.png', 'PearWeb', open_browser),
        # ... [rest of your apps] ...
    ]

    for i, (img_path, name, func) in enumerate(apps):
        x = 340 + i * 105
        
        # 1. Load the image
        tk_img = load_icon(f"icons/{img_path}") # Assumes icons are in an 'icons' folder
        
        if tk_img:
            # Store reference so Python doesn't delete the image from memory
            icon_images[name] = tk_img 
            
            # 2. Draw image instead of text
            obj = canvas.create_image(x, 792, image=tk_img)
        else:
            # Fallback to emoji if file is missing
            obj = canvas.create_text(x, 792, text='🍐', font=('Arial', 38))

        canvas.tag_bind(obj, '<Button-1>', func)
        canvas.create_text(x, 835, text=name, fill='white', font=('Segoe UI', 9))