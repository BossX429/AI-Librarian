#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous AI Librarian - Background Orchestrator
Runs everything automatically in the background with ZERO manual intervention.

What it does:
1. Watches for new/updated log files
2. Auto-compresses logs every 5 minutes
3. Auto-runs Curator after compression
4. Runs 24/7 silently in background

Logger runs independently - this just handles compression/curation.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Set, Optional
import json

# Fix Windows console encoding (only if console exists)
if sys.platform == 'win32' and sys.stdout is not None:
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class AutonomousLibrarian:
    """
    Orchestrates AI Librarian compression and curation autonomously.
    Runs forever in background, managing everything automatically.
    """
    
    def __init__(self) -> None:
        self.project_root: Path = Path(__file__).parent.parent
        self.logger_dir: Path = self.project_root / "logger"
        self.compressor_dir: Path = self.project_root / "compressor"
        self.curator_dir: Path = self.project_root / "curator"
        self.raw_logs_dir: Path = self.logger_dir / "raw_logs"
        self.compressed_dir: Path = self.compressor_dir / "compressed"
        
        # Tracking
        self.last_compression_time: Optional[datetime] = None
        self.last_curation_time: Optional[datetime] = None
        self.processed_files: Set[str] = set()
        
        # Configuration
        self.compression_interval: int = 300  # 5 minutes
        self.check_interval: int = 30  # Check every 30 seconds
        self.min_file_age = 60  # Wait 60 seconds before processing new files
        
        # Ensure directories exist
        self.raw_logs_dir.mkdir(exist_ok=True)
        self.compressed_dir.mkdir(exist_ok=True)
        
        # Log file
        self.log_file = self.project_root / "orchestrator" / "orchestrator.log"
        
    def log(self, message: str) -> None:
        """Log message to both console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        
        # Print only if console exists
        if sys.stdout is not None:
            print(log_msg)
        
        # Rotate log if too large (>10MB)
        try:
            if self.log_file.exists() and self.log_file.stat().st_size > 10 * 1024 * 1024:
                # Rotate: orchestrator.log -> orchestrator.log.1
                backup = self.log_file.with_suffix('.log.1')
                if backup.exists():
                    backup.unlink()
                self.log_file.rename(backup)
        except Exception:
            pass  # If rotation fails, just continue
        
        # Append to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except (IOError, OSError) as e:
            # Log write failures - only print if console exists
            if sys.stdout is not None:
                print(f"Warning: Could not write to log file: {e}")
    
    def get_unprocessed_logs(self) -> List[Path]:
        """Find raw log files that haven't been compressed yet."""
        if not self.raw_logs_dir.exists():
            return []
        
        unprocessed = []
        current_time = datetime.now()
        
        for log_file in self.raw_logs_dir.glob("*.jsonl"):
            # Skip if already processed
            if log_file.name in self.processed_files:
                continue
            
            # Skip if file is too new (might still be writing)
            file_age = current_time - datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_age.total_seconds() < self.min_file_age:
                continue
            
            # Check if compressed version already exists
            compressed_name = f"compressed_{log_file.name}"
            compressed_path = self.compressed_dir / compressed_name
            
            if not compressed_path.exists():
                unprocessed.append(log_file)
        
        return unprocessed
    
    def run_compressor(self) -> bool:
        """Run the Compressor on unprocessed logs."""
        unprocessed = self.get_unprocessed_logs()
        
        if not unprocessed:
            return False
        
        self.log(f" Compressing {len(unprocessed)} log file(s)...")
        
        compressor_script = self.compressor_dir / "delta_compressor.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(compressor_script), "compress"],
                cwd=str(self.compressor_dir),
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                self.log(" Compression complete")
                # Mark files as processed
                for f in unprocessed:
                    self.processed_files.add(f.name)
                self.last_compression_time = datetime.now()
                return True
            else:
                self.log(f" Compression warning: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(" Compression timeout (took >2 minutes)")
            return False
        except Exception as e:
            self.log(f" Compression error: {e}")
            return False
    
    def run_curator(self) -> bool:
        """Run the Curator to update database."""
        self.log(" Running Curator...")
        
        curator_script = self.curator_dir / "claude_curator.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(curator_script)],
                cwd=str(self.curator_dir),
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout
            )
            
            if result.returncode == 0:
                self.log(" Curator complete")
                self.last_curation_time = datetime.now()
                return True
            else:
                self.log(f" Curator warning: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(" Curator timeout (took >3 minutes)")
            return False
        except Exception as e:
            self.log(f" Curator error: {e}")
            return False
    
    def should_compress_now(self):
        """Determine if we should run compression now."""
        # First time - always compress
        if self.last_compression_time is None:
            return True
        
        # Check if enough time has passed
        time_since_last = datetime.now() - self.last_compression_time
        if time_since_last.total_seconds() >= self.compression_interval:
            # Only compress if there are unprocessed files
            return len(self.get_unprocessed_logs()) > 0
        
        return False
    
    def get_stats(self):
        """Get current statistics."""
        stats = {
            'raw_logs': len(list(self.raw_logs_dir.glob("*.jsonl"))),
            'compressed': len(list(self.compressed_dir.glob("*.jsonl"))),
            'last_compression': self.last_compression_time.strftime("%H:%M:%S") if self.last_compression_time else "Never",
            'last_curation': self.last_curation_time.strftime("%H:%M:%S") if self.last_curation_time else "Never"
        }
        return stats
    
    def run_cycle(self):
        """Run one cycle of monitoring and processing."""
        # Check if we should compress
        if self.should_compress_now():
            compressed = self.run_compressor()
            
            # If compression succeeded, run curator
            if compressed:
                time.sleep(2)  # Brief pause
                self.run_curator()
        
        # Prevent memory leak: Clear processed files older than 24 hours
        if len(self.processed_files) > 100:
            current_files = {f.name for f in self.raw_logs_dir.glob("*.jsonl")}
            self.processed_files = self.processed_files.intersection(current_files)
    
    def run_forever(self):
        """Main loop - runs forever in background."""
        self.log(" Autonomous AI Librarian Starting...")
        self.log(f"    Project: {self.project_root}")
        self.log(f"   [TIMER]  Compression interval: {self.compression_interval}s")
        self.log(f"    Check interval: {self.check_interval}s")
        self.log("")
        self.log("[INFO] Logger runs independently (claude_storage_parser.py)")
        self.log("[INFO] Orchestrator manages compression & curation only")
        self.log("")
        
        self.log(" Autonomous mode active - running 24/7")
        self.log("   Press Ctrl+C to stop")
        self.log("")
        
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                
                # Run processing cycle
                self.run_cycle()
                
                # Log status every 20 cycles (~10 minutes)
                if cycle_count % 20 == 0:
                    stats = self.get_stats()
                    self.log(f" Status: Raw={stats['raw_logs']}, "
                           f"Compressed={stats['compressed']}, Last compression={stats['last_compression']}")
                
                # Sleep until next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log("\n[STOP]  Stopping Autonomous Librarian...")
            self.log(" Orchestrator stopped")
        except Exception as e:
            self.log(f" Fatal error: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")


def main():
    """Main entry point."""
    librarian = AutonomousLibrarian()
    librarian.run_forever()


if __name__ == "__main__":
    main()
