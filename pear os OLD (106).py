def process_command(event):
    cmd = cmd_var.get().strip().lower()
    if not cmd: return
    log.append(f"root@pearos:~$ {cmd}")
    
    if cmd == 'help':
        log.append("Available: help, ls, date, clear, i-ready, party, matrix, whoami, exit")
    elif cmd == 'matrix':
        log.append("Initializing Matrix sequence...")
        start_matrix_effect()
    elif cmd == 'party':
        log.append("RANDOM DANCING! 💃🕺")
        trigger_dance()
    # ... existing commands (ls, date, etc.)