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
            # Continue dancing
            root.after(100, lambda: dance(count - 1))
        else:
            # STOP dancing and CLOSE the OS
            canvas.configure(bg='black')
            root.destroy()  # This kills the mainloop and closes the window
    dance()