def process_command(event):
        cmd = cmd_var.get().strip().lower()
        if not cmd: return
        log.append(f"root@pearos:~$ {cmd}")
        
        # New command logic
        if cmd == 'help':
            log.append("Available: help, ls, date, clear, i-ready, party, whoami, exit")
        elif cmd == 'party' or cmd == 'random-dancing':
            log.append("RANDOM DANCING! 💃🕺")
            trigger_dance() # Calls the global function that handles sound and color
        elif cmd == 'ls':
            log.append("Applications/  Documents/  Games/  System/  secret_pear_recipe.txt")
        # ... (rest of your existing commands)