# ============================================
# HD BACKGROUND & UI ENGINE
# ============================================
def draw_default_gradient():
    # HD Sky Gradient (Interpolated 1000-step transition)
    # Transitions from Deep Blue to Aero Light Blue
    for i in range(600):
        # Calculate color interpolation (r, g, b)
        r = int(51 + (102 - 51) * (i / 600))
        g = int(153 + (204 - 153) * (i / 600))
        b = int(255)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 1400, i, fill=color, tags='bg')

    # HD Grass/Ground Gradient
    # Transitions from Vibrant Green to Darker Earth Green
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