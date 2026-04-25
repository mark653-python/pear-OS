# ============================================
# SYSTEM APPS & GAMES
# ============================================
def open_terminal(e=None):
    t = create_window('Pear Command Prompt', '#1a1a1a')
    if not t: return
    
    log = ["GaiaCore Kernel v1.0.4", "iCarly Mod: Online", "Type 'help' for a list of commands."]
    log_text = canvas.create_text(320, 210, text="\n".join(log), anchor='nw', fill=data_cell_green, font=('Consolas', 11), tags=t)
    
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, 
                         insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    
    canvas.create_window(650, 575, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        log.append(f"root@pearos:~$ {cmd}")
        
        if cmd == 'help':
            # Added 'whoami' to the help list
            log.append("Available: help, ls, date, clear, i-ready, random-dancing, cmd, whoami")
        elif cmd == 'ls':
            log.append("Applications/  Documents/  Games/  System/  secret_pear_recipe.txt")
        elif cmd == 'date':
            log.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif cmd == 'clear':
            log.clear()
        elif cmd == 'i-ready':
            log.append("Scanning curriculum... All lessons completed. 100% Mastery.")
        elif cmd == 'random-dancing':
            log.append("RANDOM DANCING! 💃🕺")
        elif cmd == 'cmd':
            log.append("Pear Command Line Interface [Version 1.0.4]")
        elif cmd == 'whoami':
            # New command added here
            log.append("TEST")
        else:
            log.append(f"Command not found: {cmd}")
        
        canvas.itemconfig(log_text, text="\n".join(log[-18:]))
        cmd_var.set("")

    cmd_entry.bind('<Return>', process_command)