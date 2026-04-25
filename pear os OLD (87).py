def open_terminal(e=None):
    t = create_window('Pear Terminal', '#1a1a1a')
    if not t: return

    # terminal_log stores the history of the session
    terminal_log = ["GaiaCore Kernel v1.0.4-release", f"[{datetime.now().strftime('%H:%M:%S')}] Connected", "Type 'help' for commands."]
    
    # Text display for the log
    log_text = canvas.create_text(320, 210, text="\n".join(terminal_log), 
                                  anchor='nw', fill=data_cell_green, font=('Consolas', 10), tags=t)

    # Input handling
    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(root, textvariable=cmd_var, bg='#1a1a1a', fg=data_cell_green, 
                         insertbackground=data_cell_green, font=('Consolas', 12), borderwidth=0)
    
    # Place the input entry at the bottom of the window
    entry_window = canvas.create_window(650, 580, window=cmd_entry, width=680, tags=t)
    cmd_entry.focus_set()

    def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        
        terminal_log.append(f"> root@pearos:~# {cmd}")
        
        # Command Logic
        if cmd == 'help':
            terminal_log.extend(['Available: help, ls, clear, date, whoami, exit'])
        elif cmd == 'ls':
            files = os.listdir('.')
            terminal_log.append("  ".join(files[:10]))
        elif cmd == 'date':
            terminal_log.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif cmd == 'whoami':
            terminal_log.append("pear_user_alpha")
        elif cmd == 'clear':
            terminal_log.clear()
            terminal_log.append("Terminal cleared.")
        elif cmd == 'exit':
            close_window(t, 'Pear Terminal')
            return
        else:
            terminal_log.append(f"Command not found: {cmd}")

        # Keep only the last 15 lines to avoid overflowing the window
        if len(terminal_log) > 18:
            terminal_log.pop(0)
            
        canvas.itemconfig(log_text, text="\n".join(terminal_log))
        cmd_var.set("") # Clear input

    cmd_entry.bind('<Return>', process_command)