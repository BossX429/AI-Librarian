#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous AI Librarian - Background Orchestrator
Runs everything automatically in the background with ZERO manual intervention.

What it does:
1. Starts Logger in background
2. Watches for new/updated log files
3. Auto-compresses logs every 5 minutes
4. Auto-runs Curator after compression
5. Runs 24/7 silently in background

Set it and forget it!
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import threading
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class AutonomousLibrarian:
    """
    Orchestrates all AI Librarian agents autonomously.
    Runs forever in background, managing everything automatically.
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.logger_dir = self.project_root / "logger"
        self.compressor_dir = self.project_root / "compressor"
        self.curator_dir = self.project_root / "curator"
        self.raw_logs_dir = self.logger_dir / "raw_logs"
        self.compressed_dir = self.compressor_dir / "compressed"
        
        # Tracking
        self.logger_process = None
        self.last_compression_time = None
        self.last_curation_time = None
        self.processed_files = set()
        
        # Configuration
        self.compression_interval = 300  # 5 minutes
        self.check_interval = 30  # Check every 30 seconds
        self.min_file_age = 60  # Wait 60 seconds before processing new files
        
        # Ensure directories exist
        self.raw_logs_dir.mkdir(exist_ok=True)
        self.compressed_dir.mkdir(exist_ok=True)
        
        # Log file
        self.log_file = self.project_root / "orchestrator" / "orchestrator.log"
        
    def log(self, message: str):
        """Log message to both console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        # Append to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except:
            pass  # Fail silently if can't write to log
    
    def start_logger(self):
        """Start the Logger agent in background."""
        self.log("🔴 Starting Logger Agent...")
        
        logger_script = self.logger_dir / "claude_desktop_logger.py"
        
        if not logger_script.exists():
            self.log(f"❌ Logger script not found: {logger_script}")
            return False
        
        try:
            # Start logger as subprocess (runs in background)
            self.logger_process = subprocess.Popen(
                [sys.executable, str(logger_script)],
                cwd=str(self.logger_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            self.log(f"✅ Logger started (PID: {self.logger_process.pid})")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start Logger: {e}")
            return False
    
    def get_unprocessed_logs(self):
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
    
    def run_compressor(self):
        """Run the Compressor on unprocessed logs."""
        unprocessed = self.get_unprocessed_logs()
        
        if not unprocessed:
            return False
        
        self.log(f"⚡ Compressing {len(unprocessed)} log file(s)...")
        
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
                self.log("✅ Compression complete")
                # Mark files as processed
                for f in unprocessed:
                    self.processed_files.add(f.name)
                self.last_compression_time = datetime.now()
                return True
            else:
                self.log(f"⚠️ Compression warning: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("⚠️ Compression timeout (took >2 minutes)")
            return False
        except Exception as e:
            self.log(f"❌ Compression error: {e}")
            return False
    
    def run_curator(self):
        """Run the Curator to update database."""
        self.log("🧠 Running Curator...")
        
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
                self.log("✅ Curator complete")
                self.last_curation_time = datetime.now()
                return True
            else:
                self.log(f"⚠️ Curator warning: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("⚠️ Curator timeout (took >3 minutes)")
            return False
        except Exception as e:
            self.log(f"❌ Curator error: {e}")
            return False
    
    def check_logger_health(self):
        """Check if Logger is still running, restart if needed."""
        if self.logger_process is None:
            return False
        
        # Check if process is still alive
        poll = self.logger_process.poll()
        
        if poll is None:
            # Still running
            return True
        else:
            # Process died, restart it
            self.log("⚠️ Logger stopped, restarting...")
            return self.start_logger()
    
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
            'logger_running': self.check_logger_health(),
            'raw_logs': len(list(self.raw_logs_dir.glob("*.jsonl"))),
            'compressed': len(list(self.compressed_dir.glob("*.jsonl"))),
            'last_compression': self.last_compression_time.strftime("%H:%M:%S") if self.last_compression_time else "Never",
            'last_curation': self.last_curation_time.strftime("%H:%M:%S") if self.last_curation_time else "Never"
        }
        return stats
    
    def run_cycle(self):
        """Run one cycle of monitoring and processing."""
        # Check Logger health
        self.check_logger_health()
        
        # Check if we should compress
        if self.should_compress_now():
            compressed = self.run_compressor()
            
            # If compression succeeded, run curator
            if compressed:
                time.sleep(2)  # Brief pause
                self.run_curator()
    
    def run_forever(self):
        """Main loop - runs forever in background."""
        self.log("🚀 Autonomous AI Librarian Starting...")
        self.log(f"   📂 Project: {self.project_root}")
        self.log(f"   ⏱️  Compression interval: {self.compression_interval}s")
        self.log(f"   🔄 Check interval: {self.check_interval}s")
        self.log("")
        
        # Start logger
        if not self.start_logger():
            self.log("❌ Failed to start Logger - exiting")
            return
        
        self.log("✅ Autonomous mode active - running 24/7")
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
                    self.log(f"📊 Status: Logger={stats['logger_running']}, Raw={stats['raw_logs']}, "
                           f"Compressed={stats['compressed']}, Last compression={stats['last_compression']}")
                
                # Sleep until next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log("\n⏹️  Stopping Autonomous Librarian...")
            self.stop()
        except Exception as e:
            self.log(f"❌ Fatal error: {e}")
            self.stop()
    
    def stop(self):
        """Clean shutdown."""
        # Stop logger
        if self.logger_process and self.logger_process.poll() is None:
            self.log("⏹️  Stopping Logger...")
            self.logger_process.terminate()
            try:
                self.logger_process.wait(timeout=5)
                self.log("✅ Logger stopped")
            except:
                self.logger_process.kill()
                self.log("⚠️ Logger force killed")
        
        self.log("👋 Autonomous Librarian stopped")


def main():
    """Main entry point."""
    librarian = AutonomousLibrarian()
    librarian.run_forever()


if __name__ == "__main__":
    main()
