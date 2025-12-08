import sys
import time
import gc
import ctypes
import psutil
# TITAN-Powered RAM Flush
# Aggressive memory cleanup using parallel operations


def flush_process_working_set(pid):
    """Flush working set for a single process - runs in parallel"""
    try:
        proc = psutil.Process(pid)
        # Windows API call to empty working set
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x1F0FFF, False, pid)
        if handle:
            kernel32.SetProcessWorkingSetSize(handle, -1, -1)
            kernel32.CloseHandle(handle)
            return ('success', pid, proc.name())
    except:
        pass
    return ('skipped', pid, None)

def main():
    start = time.time()
    
    # Get memory before
    mem_before = psutil.virtual_memory()
    free_before_gb = mem_before.available / (1024**3)
    
    # Python GC first
    gc.collect()
    gc.collect()
    gc.collect()
    
    # Get all processes
    all_pids = [p.pid for p in psutil.process_iter()]
    
    print(f"Flushing working sets for {len(all_pids)} processes...")
    
    # PARALLEL FLUSH - All processes flushed simultaneously using thread pool
    # ThreadPool instead of ProcessPool because we're calling Windows API
    flushed = 0
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(flush_process_working_set, pid): pid for pid in all_pids}
        
        for future in futures:
            try:
                status, pid, name = future.result()
                if status == 'success':
                    flushed += 1
            except:
                pass
    
    # Get memory after
    mem_after = psutil.virtual_memory()
    free_after_gb = mem_after.available / (1024**3)
    freed_gb = free_after_gb - free_before_gb
    
    duration = time.time() - start
    
    # Log result
    log_path = Path('C:/repos/AI-Librarian/logs/ram_flush.log')
    log_path.parent.mkdir(exist_ok=True)
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_path, 'a') as f:
        f.write(f"{timestamp} - TITAN: Flushed {flushed} processes, freed {freed_gb:.2f} GB in {duration:.2f}s\\n")
    
    print(f"✅ TITAN RAM Flush:")
    print(f"   Processes: {flushed}")
    print(f"   Freed: {freed_gb:.2f} GB")
    print(f"   Time: {duration:.2f}s")
    print(f"   Speed: {flushed/duration:.0f} processes/sec")

if __name__ == "__main__":
    main()
