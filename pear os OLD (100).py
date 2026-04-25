def play_dance_sound():
        try:
            pygame.mixer.music.load("random_dancing.mp3")
            pygame.mixer.music.play()
        except:
            print("Sound file not found, skipping audio.")
    ```
  
  
    This function will rapidly swap background colors to create a "party" effect.
    ```python
    def start_random_dancing(count=10):
        if count > 0:
            # Flash random vibrant colors
            colors = ['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00']
            canvas.configure(bg=random.choice(colors))
            root.after(100, lambda: start_random_dancing(count - 1))
        else:
            # Reset to original black background
            canvas.configure(bg='black')
    ```
  
  
    Place this code before `root.mainloop()` to create the physical button on your Pear OS desktop.
    ```python
    dance_btn = canvas.create_rectangle(50, 50, 150, 150, fill='#ff66cc', outline='white', width=2, tags='ui')
    canvas.create_text(100, 100, text="RANDOM\nDANCING", fill='white', font=('Segoe UI', 10, 'bold'), justify='center', tags='ui')
    
    def trigger_dance(e):
        play_dance_sound()
        start_random_dancing()
        
    canvas.tag_bind(dance_btn, '', trigger_dance)
    ```