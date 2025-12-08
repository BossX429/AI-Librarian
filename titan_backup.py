import sys
import time
import hashlib
import shutil
# TITAN-Powered Incremental Backup
# Parallel file copy across all 20 cores

sys.path.append('C:/repos/TITAN-FS')


def hash_file(filepath):
    """Fast file hashing for deduplication"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def copy_file_if_changed(args):
    """Copy file only if modified - runs in parallel"""
    src, dst = args
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        # Skip if destination exists and is identical
        if dst_path.exists():
            if src_path.stat().st_mtime <= dst_path.stat().st_mtime:
                return ('skipped', src)
        
        # Create parent directory
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(src, dst)
        return ('copied', src)
        
    except Exception as e:
        return ('error', src, str(e))

def main():
    start = time.time()
    
    source = Path('C:/repos')
    destination = Path('D:/Backups') / f"repos_{time.strftime('%Y-%m-%d')}"
    
    # Create backup directory
    destination.mkdir(parents=True, exist_ok=True)
    
    # Find all files to backup (exclude build artifacts)
    exclude_dirs = {'node_modules', '__pycache__', '.git', '.venv', 'venv', 'build', 'dist'}
    
    print("Scanning source directory...")
    files_to_backup = []
    
    for src_file in source.rglob('*'):
        if src_file.is_file():
            # Check if any parent is in exclude_dirs
            if not any(parent.name in exclude_dirs for parent in src_file.parents):
                rel_path = src_file.relative_to(source)
                dst_file = destination / rel_path
                files_to_backup.append((str(src_file), str(dst_file)))
    
    print(f"Found {len(files_to_backup)} files to process")
    
    # PARALLEL BACKUP - All 20 cores copying simultaneously
    copied = 0
    skipped = 0
    errors = 0
    
    with ProcessPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(copy_file_if_changed, args): args for args in files_to_backup}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            
            if result[0] == 'copied':
                copied += 1
            elif result[0] == 'skipped':
                skipped += 1
            elif result[0] == 'error':
                errors += 1
            
            # Progress update every 100 files
            if i % 100 == 0:
                print(f"Progress: {i}/{len(files_to_backup)} files processed")
    
    duration = time.time() - start
    
    # Calculate backup size
    total_size = sum(Path(dst).stat().st_size for _, dst in files_to_backup if Path(dst).exists())
    size_gb = total_size / (1024**3)
    
    # Log result
    log_path = Path('C:/repos/AI-Librarian/logs/backup.log')
    log_path.parent.mkdir(exist_ok=True)
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_path, 'a') as f:
        f.write(f"{timestamp} - TITAN Backup: {copied} copied, {skipped} skipped, {errors} errors | {size_gb:.2f} GB in {duration:.2f}s\\n")
    
    print(f"✅ TITAN Backup Complete:")
    print(f"   Copied: {copied} files")
    print(f"   Skipped: {skipped} files")
    print(f"   Errors: {errors}")
    print(f"   Size: {size_gb:.2f} GB")
    print(f"   Time: {duration:.2f}s")
    print(f"   Speed: {len(files_to_backup)/duration:.0f} files/sec")

if __name__ == "__main__":
    main()
