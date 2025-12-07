"""
Autonomous Git Auto-Sync for AI-Librarian
==========================================
Automatically commits and pushes changes every run.
Designed to be called by scheduled task every 30 minutes.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPO_PATH = Path(__file__).parent

def run_git_command(cmd):
    """Execute git command and return output"""
    try:
        result = subprocess.run(
            cmd,
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_changes():
    """Check if there are any uncommitted changes"""
    success, stdout, stderr = run_git_command(["git", "status", "--porcelain"])
    if success and stdout.strip():
        return True, stdout
    return False, ""

def commit_changes():
    """Stage and commit all changes"""
    # Stage all changes
    success, stdout, stderr = run_git_command(["git", "add", "-A"])
    if not success:
        return False, f"Failed to stage: {stderr}"
    
    # Commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-sync: {timestamp}"
    
    success, stdout, stderr = run_git_command(["git", "commit", "-m", commit_msg])
    if success:
        return True, stdout
    return False, stderr

def push_changes():
    """Push commits to remote"""
    success, stdout, stderr = run_git_command(["git", "push", "origin", "main"])
    if success:
        return True, stdout
    return False, stderr

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Git Auto-Sync Starting...")
    
    # Check for changes
    has_changes, changes = check_changes()
    
    if not has_changes:
        print("✓ No changes detected. Repository is clean.")
        return 0
    
    print(f"✓ Changes detected:\n{changes}")
    
    # Commit changes
    print("→ Committing changes...")
    success, output = commit_changes()
    if not success:
        print(f"✗ Commit failed: {output}")
        return 1
    
    print(f"✓ Committed successfully")
    
    # Push to remote
    print("→ Pushing to remote...")
    success, output = push_changes()
    if not success:
        print(f"✗ Push failed: {output}")
        return 1
    
    print(f"✓ Pushed successfully")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Git Auto-Sync Complete!")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)
