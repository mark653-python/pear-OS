def start_matrix_effect(count=50):
    # Get terminal window coordinates
    t_tag = 'PearCommandPrompt'
    if t_tag not in open_apps: return
    
    # Generate random 'drops' of characters
    chars = "0123456789ABCDEFHIJKLMNOPQRSTUVWXYZ$+-*/=%\"'#&_(),.;:?!"
    for _ in range(15):
        x = random.randint(320, 980)
        y = 200
        drop = canvas.create_text(x, y, text=random.choice(chars), 
                                  fill='#00ff41', font=('Consolas', 10), tags=(t_tag, 'matrix_drop'))
        
        def fall(item=drop, x_pos=x, y_pos=y):
            if t_tag not in open_apps: return
            new_y = y_pos + 15
            if new_y < 580:
                canvas.coords(item, x_pos, new_y)
                canvas.itemconfig(item, text=random.choice(chars))
                root.after(50, lambda: fall(item, x_pos, new_y))
            else:
                canvas.delete(item)

        fall()

    if count > 0:
        root.after(200, lambda: start_matrix_effect(count - 1))