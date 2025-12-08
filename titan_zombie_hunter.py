# TITAN-Powered Zombie Process Hunter
# Parallel process analysis across all 20 cores

import sys
sys.path.append('C:/repos/TITAN-FS')

import psutil
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timedelta

def check_process(proc_info):
    """Check if process is a zombie - runs in parallel"""
    pid, name, started = proc_info
    try:
        proc = psutil.Process(pid)
        
        # Check if orphaned pythonw
        if name == 'pythonw.exe':
            parent = proc.parent()
            runtime = datetime.now() - datetime.fromtimestamp(started)
            
            if not parent and runtime > timedelta(hours=24):
                return ('orphan', pid, name, runtime.total_seconds())
        
        # Check high CPU processes (>50% for >30 min)
        if name not in ['claude.exe', 'ollama.exe', 'python.exe', 'pythonw.exe']:
            cpu_time = proc.cpu_times().user + proc.cpu_times().system
            if cpu_time > 1800:  # 30 minutes
                return ('high_cpu', pid, name, cpu_time)
                
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    
    return None

def main():
    start = time.time()
    
    # Get all processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            info = proc.info
            processes.append((info['pid'], info['name'], info['create_time']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # PARALLEL SCAN - All 20 cores checking processes simultaneously
    killed = []
    
    with ProcessPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_process, p): p for p in processes}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                zombie_type, pid, name, metric = result
                try:
                    proc = psutil.Process(pid)
                    proc.kill()
                    killed.append(f"{name} PID {pid} ({zombie_type})")
                except:
                    pass
    
    duration = time.time() - start
    
    # Log results
    log_path = Path('C:/repos/AI-Librarian/logs/zombie_hunter.log')
    log_path.parent.mkdir(exist_ok=True)
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_path, 'a') as f:
        if killed:
            f.write(f"{timestamp} - TITAN: Killed {len(killed)} zombies in {duration:.2f}s: {', '.join(killed)}\\n")
        else:
            f.write(f"{timestamp} - TITAN: No zombies found (scanned {len(processes)} processes in {duration:.2f}s)\\n")
    
    print(f"✅ TITAN Zombie Hunter: {len(killed)} killed, {len(processes)} scanned in {duration:.2f}s")

if __name__ == "__main__":
    main()
