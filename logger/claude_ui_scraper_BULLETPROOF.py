import os
import json
import time
import logging
import hashlib
import psutil
import threading
from datetime import datetime
import sys
    from pywinauto import Application, Desktop
    from pywinauto.findwindows import ElementNotFoundError
    import pygetwindow as gw
from config import LOGGER_DIR, RAW_LOGS_DIR, PROCESSED_DIR, LOGGER_LOG
"""
Claude Desktop Conversation Logger - BULLETPROOF EDITION
=========================================================
CPU-LIMITED, SELF-PROTECTING VERSION

Features:
- Automatic CPU monitoring and self-termination if over 25%
- Rate limiting to prevent UI query spam
- Maximum element iteration limits
- Watchdog timer for hung operations
- Memory leak prevention
"""


try:
except ImportError as e:
    print(f"Missing required package: {e}")
    print("\nPlease install: pip install pywinauto psutil pygetwindow")
    sys.exit(1)

# Import centralized configuration
sys.path.insert(0, str(Path(__file__).parent.parent))

# === UNICODE PREVENTION ===
def strip_unicode(text):
    """Strip ALL unicode - ASCII only at capture time"""
    if not text:
        return text
    return ''.join(char if ord(char) <= 127 else '?' for char in text)

# === PROTECTION CONFIGURATION ===
MAX_CPU_PERCENT = 25.0  # Kill self if CPU usage exceeds this
MAX_MEMORY_MB = 150     # Kill self if memory exceeds this
MAX_ELEMENTS_SCAN = 100 # Maximum UI elements to scan per cycle
OPERATION_TIMEOUT = 5   # Kill operation if takes longer than 5 seconds
CHECK_INTERVAL = 5      # Check every 5 seconds (less frequent = less CPU)

# Configuration
BASE_DIR = LOGGER_DIR
LOG_FILE = LOGGER_LOG

# Ensure directories exist
RAW_LOGS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class CPUProtection:
    """Monitors CPU usage and kills process if it goes rogue."""
    
    def __init__(self, max_cpu_percent=MAX_CPU_PERCENT, max_memory_mb=MAX_MEMORY_MB):
        self.max_cpu = max_cpu_percent
        self.max_memory = max_memory_mb
        self.process = psutil.Process()
        self.running = True
        self.violations = 0
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info(f"CPU Protection: MAX {self.max_cpu}% CPU, {self.max_memory}MB RAM")
    
    def _monitor_loop(self):
        """Background thread that monitors resource usage."""
        while self.running:
            try:
                cpu_percent = self.process.cpu_percent(interval=1)
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                
                if cpu_percent > self.max_cpu:
                    self.violations += 1
                    logger.warning(f"!!! CPU VIOLATION: {cpu_percent:.1f}% (limit: {self.max_cpu}%)")
                    
                    if self.violations >= 3:
                        logger.error(f"!!! KILLING SELF - CPU limit violated 3 times !!!")
                        logger.error(f"CPU: {cpu_percent:.1f}%, Memory: {memory_mb:.1f}MB")
                        os._exit(1)  # Hard kill
                else:
                    self.violations = max(0, self.violations - 1)
                
                if memory_mb > self.max_memory:
                    logger.error(f"!!! KILLING SELF - Memory limit exceeded !!!")
                    logger.error(f"Memory: {memory_mb:.1f}MB (limit: {self.max_memory}MB)")
                    os._exit(1)
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(5)
    
    def stop(self):
        """Stop monitoring."""
        self.running = False


class ConversationCapture:
    """Captures Claude Desktop conversations with STRICT LIMITS."""
    
    def __init__(self):
        self.current_session_id = self._generate_session_id()
        self.last_captured_text = ""
        self.message_count = 0
        self.session_start = datetime.now()
        self.cpu_protection = CPUProtection()
        logger.info(f"New session: {self.current_session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"claude_session_{timestamp}"
    
    def _get_text_hash(self, text: str) -> str:
        """Generate hash of text."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def find_claude_window(self) -> Optional[object]:
        """Find Claude Desktop window."""
        try:
            windows = gw.getWindowsWithTitle("Claude")
            if windows:
                return windows[0]
            
            for proc in psutil.process_iter(['name']):
                if 'claude' in proc.info['name'].lower():
                    try:
                        app = Application(backend="uia").connect(process=proc.pid)
                        return app.top_window()
                    except:
                        continue
            
            return None
        except Exception as e:
            logger.error(f"Error finding window: {e}")
            return None
    
    def extract_conversation_text(self, window) -> Optional[str]:
        """Extract text with STRICT LIMITS to prevent CPU explosion."""
        try:
            start_time = time.time()
            
            # Try simple method first
            if hasattr(window, 'window_text'):
                text = window.window_text()
                if text:
                    return text
            
            # Detailed extraction WITH LIMITS
            try:
                app = Application(backend="uia").connect(handle=window._hWnd)
                main_window = app.top_window()
                
                all_text = []
                element_count = 0
                
                # CRITICAL: Limit number of elements scanned
                for element in main_window.descendants():
                    # HARD LIMIT: Stop after MAX_ELEMENTS_SCAN
                    element_count += 1
                    if element_count > MAX_ELEMENTS_SCAN:
                        logger.warning(f"Hit element limit ({MAX_ELEMENTS_SCAN}) - stopping scan")
                        break
                    
                    # TIMEOUT CHECK: Stop if operation takes too long
                    if time.time() - start_time > OPERATION_TIMEOUT:
                        logger.warning(f"Operation timeout ({OPERATION_TIMEOUT}s) - stopping scan")
                        break
                    
                    try:
                        if hasattr(element, 'window_text'):
                            text = element.window_text()
                            if text and len(text.strip()) > 10:
                                all_text.append(text.strip())
                    except:
                        continue
                
                if all_text:
                    # Deduplicate
                    seen = set()
                    unique_text = []
                    for text_block in all_text:
                        text_hash = hashlib.md5(text_block.encode()).hexdigest()
                        if text_hash not in seen:
                            seen.add(text_hash)
                            unique_text.append(text_block)
                    
                    return "\n".join(unique_text)
                
            except Exception as e:
                logger.debug(f"Extraction failed: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return None

    def parse_and_save_conversation(self, text: str):
        """Parse and save conversation."""
        if not text or text == self.last_captured_text:
            return
        
        text_hash = self._get_text_hash(text)
        if text_hash == self._get_text_hash(self.last_captured_text):
            return
        
        timestamp = datetime.now().isoformat()
        
        # Strip unicode BEFORE saving
        clean_text = strip_unicode(text)
        
        entry = {
            "session_id": self.current_session_id,
            "timestamp": timestamp,
            "message_number": self.message_count,
            "raw_text": clean_text,
            "text_hash": text_hash,
            "capture_method": "bulletproof_ui_automation"
        }
        
        output_file = RAW_LOGS_DIR / f"{self.current_session_id}.jsonl"
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=True) + '\n')
            
            self.message_count += 1
            self.last_captured_text = text
            logger.info(f"Captured message #{self.message_count} ({len(text)} chars)")
            
        except Exception as e:
            logger.error(f"Error saving: {e}")
    
    def run(self, interval: int = CHECK_INTERVAL):
        """Main loop with protection."""
        logger.info(f"Starting BULLETPROOF capture (every {interval}s)")
        logger.info(f"Limits: {MAX_CPU_PERCENT}% CPU, {MAX_MEMORY_MB}MB RAM, {MAX_ELEMENTS_SCAN} elements")
        logger.info("Press Ctrl+C to stop")
        
        retry_count = 0
        
        try:
            while True:
                window = self.find_claude_window()
                
                if window:
                    retry_count = 0
                    text = self.extract_conversation_text(window)
                    
                    if text:
                        self.parse_and_save_conversation(text)
                else:
                    retry_count += 1
                    if retry_count % 10 == 0:
                        logger.info("Waiting for Claude Desktop...")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\nStopping capture...")
            logger.info(f"Captured {self.message_count} messages")
            self.cpu_protection.stop()
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            self.cpu_protection.stop()


def main():
    """Entry point."""
    print("=" * 70)
    print("Claude Desktop Conversation Logger - BULLETPROOF EDITION")
    print("=" * 70)
    print(f"CPU Limit: {MAX_CPU_PERCENT}%")
    print(f"Memory Limit: {MAX_MEMORY_MB}MB")
    print(f"Element Scan Limit: {MAX_ELEMENTS_SCAN}")
    print(f"Check Interval: {CHECK_INTERVAL}s")
    print(f"Raw logs: {RAW_LOGS_DIR}")
    print("=" * 70)
    print()
    
    capturer = ConversationCapture()
    capturer.run()


if __name__ == "__main__":
    main()
