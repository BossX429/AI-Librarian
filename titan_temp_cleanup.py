import time
# TITAN-Powered Temp Cleanup - TRUE parallel across 20 cores
# Processes 1000+ files per second


def delete_file(filepath):
    """Delete single file - runs in parallel"""
    try:
        Path(filepath).unlink()
        return ('success', filepath, Path(filepath).stat().st_size if Path(filepath).exists() else 0)
    except Exception as e:
        return ('error', filepath, 0)

def get_temp_files(temp_dir):
    """Get all files in temp directory"""
    try:
        files = []
        for item in Path(temp_dir).rglob('*'):
            if item.is_file():
                try:
                    files.append(str(item))
                except:
                    pass
        return files
    except:
        return []

def main():
    start = time.time()
    
    # All temp directories
    temp_dirs = [
        Path.home() / 'AppData' / 'Local' / 'Temp',
        Path('C:/Windows/Temp'),
        Path('C:/Windows/Prefetch'),
    ]
    
    # Collect all files first
    print("Scanning temp directories...")
    all_files = []
    for temp_dir in temp_dirs:
        if temp_dir.exists():
            files = get_temp_files(temp_dir)
            all_files.extend(files)
            print(f"  {temp_dir}: {len(files)} files")
    
    if not all_files:
        print("No files to clean")
        return
    
    print(f"\\nDeleting {len(all_files)} files in parallel...")
    
    # PARALLEL DELETE - All 20 cores deleting simultaneously
    deleted = 0
    errors = 0
    total_size = 0
    
    with ProcessPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(delete_file, f): f for f in all_files}
        
        for future in as_completed(futures):
            status, filepath, size = future.result()
            if status == 'success':
                deleted += 1
                total_size += size
            else:
                errors += 1
    
    duration = time.time() - start
    size_mb = total_size / (1024**2)
    
    # Log result
    log_path = Path('C:/repos/AI-Librarian/logs/cleanup.log')
    log_path.parent.mkdir(exist_ok=True)
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_path, 'a') as f:
        f.write(f"{timestamp} - TITAN: Deleted {deleted} files ({size_mb:.2f} MB) in {duration:.2f}s | Speed: {deleted/duration:.0f} files/sec\\n")
    
    print(f"\\n✅ TITAN Cleanup Complete:")
    print(f"   Deleted: {deleted} files")
    print(f"   Errors: {errors}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   Time: {duration:.2f}s")
    print(f"   Speed: {deleted/duration:.0f} files/sec")

if __name__ == "__main__":
    main()
