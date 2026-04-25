def open_pear_catcher(e=None):
    tag = create_window('Pear Catcher', '#e0f7fa')
    if not tag: return
    
    score = [0]
    game_active = [True]
    # [x, y] positions
    basket = [650, 550]
    pears = [[random.randint(350, 950), 200] for _ in range(3)]
    
    score_text = canvas.create_text(350, 220, text="Score: 0", font=('Segoe UI', 12, 'bold'), anchor='w', tags=tag)

    def update():
        if not game_active[0] or tag not in canvas.find_all(): return
        
        canvas.delete('game_obj')
        # Draw Basket
        canvas.create_rectangle(basket[0]-30, basket[1], basket[0]+30, basket[1]+20, fill='#8d6e63', tags=(tag, 'game_obj'))
        
        for p in pears:
            p[1] += 5 # Falling speed
            # Draw Pear
            canvas.create_oval(p[0]-10, p[1]-10, p[0]+10, p[1]+10, fill='#44dd44', tags=(tag, 'game_obj'))
            
            # Catch logic
            if p[1] > 540 and abs(p[0] - basket[0]) < 40:
                score[0] += 1
                canvas.itemconfig(score_text, text=f"Score: {score[0]}")
                p[1] = 200
                p[0] = random.randint(350, 950)
            
            # Reset if missed
            if p[1] > 600:
                p[1] = 200
                p[0] = random.randint(350, 950)

        root.after(30, update)

    def move_left(e): basket[0] = max(340, basket[0] - 25)
    def move_right(e): basket[0] = min(960, basket[0] + 25)
    
    root.bind('<Left>', move_left)
    root.bind('<Right>', move_right)
    update()