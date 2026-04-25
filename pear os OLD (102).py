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
        except:
            draw_default_gradient()
    else:
        draw_default_gradient()

    # 2. NEW: Apply Dimming Effect if windows are open
    if open_apps:
        # stipple='gray50' creates a semi-transparent mesh look in Tkinter
        canvas.create_rectangle(0, 0, 1400, 850, fill='black', stipple='gray50', tags='bg')