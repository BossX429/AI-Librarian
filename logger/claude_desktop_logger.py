"""
Claude Desktop Conversation Logger
===================================
Monitors Claude Desktop and captures conversations in real-time using Windows UI Automation.
Saves conversations to JSONL format for the AI Librarian system.

Requirements:
    pip install pywinauto psutil pygetwindow
"""

import os
import json
import time
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import sys

try:
    from pywinauto import Application, Desktop
    from pywinauto.findwindows import ElementNotFoundError
    import pygetwindow as gw
    import psutil
except ImportError as e:
    print(f"Missing required package: {e}")
    print("\nPlease install required packages:")
    print("pip install pywinauto psutil pygetwindow")
    sys.exit(1)

# Configuration
BASE_DIR = Path(r"C:\Projects\AI-Librarian\logger")
RAW_LOGS_DIR = BASE_DIR / "raw_logs"
PROCESSED_DIR = BASE_DIR / "processed"
LOG_FILE = BASE_DIR / "logger.log"

# Ensure directories exist
RAW_LOGS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConversationCapture:
    """Captures and saves Claude Desktop conversations."""
    
    def __init__(self):
        self.current_session_id = self._generate_session_id()
        self.last_captured_text = ""
        self.message_count = 0
        self.session_start = datetime.now()
        logger.info(f"New session started: {self.current_session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"claude_session_{timestamp}"
    
    def _get_text_hash(self, text: str) -> str:
        """Generate hash of text to detect changes."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def find_claude_window(self) -> Optional[object]:
        """Find and return Claude Desktop window."""
        try:
            # Try to find Claude window by title
            windows = gw.getWindowsWithTitle("Claude")
            if windows:
                logger.info(f"Found Claude window: {windows[0].title}")
                return windows[0]
            
            # Alternative: search for process
            for proc in psutil.process_iter(['name']):
                if 'claude' in proc.info['name'].lower():
                    logger.info(f"Found Claude process: {proc.info['name']}")
                    # Try to get window by process
                    try:
                        app = Application(backend="uia").connect(process=proc.pid)
                        return app.top_window()
                    except Exception as e:
                        logger.debug(f"Could not connect to process: {e}")
            
            logger.warning("Claude Desktop window not found")
            return None

        except Exception as e:
            logger.error(f"Error finding Claude window: {e}")
            return None
    
    def extract_conversation_text(self, window) -> Optional[str]:
        """Extract text from Claude Desktop window using UI Automation."""
        try:
            if hasattr(window, 'window_text'):
                # Using pygetwindow
                text = window.window_text()
                return text if text else None
            
            # Using pywinauto - more detailed extraction
            try:
                app = Application(backend="uia").connect(handle=window._hWnd)
                main_window = app.top_window()
                
                # Try to find the conversation container
                # Claude Desktop typically uses web view, so we need to access text elements
                all_text = []
                
                # Get all text controls
                for element in main_window.descendants():
                    try:
                        if hasattr(element, 'window_text'):
                            text = element.window_text()
                            if text and len(text.strip()) > 0:
                                all_text.append(text.strip())
                    except:
                        continue
                
                if all_text:
                    combined = "\n".join(all_text)
                    return combined
                
            except Exception as e:
                logger.debug(f"Detailed extraction failed: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return None

    def parse_and_save_conversation(self, text: str):
        """Parse conversation text and save to JSONL."""
        if not text or text == self.last_captured_text:
            return  # No new content
        
        text_hash = self._get_text_hash(text)
        if text_hash == self._get_text_hash(self.last_captured_text):
            return  # Content hasn't changed
        
        # Save the raw capture
        timestamp = datetime.now().isoformat()
        
        # Create a conversation entry
        entry = {
            "session_id": self.current_session_id,
            "timestamp": timestamp,
            "message_number": self.message_count,
            "raw_text": text,
            "text_hash": text_hash,
            "capture_method": "windows_ui_automation"
        }
        
        # Save to JSONL file
        output_file = RAW_LOGS_DIR / f"{self.current_session_id}.jsonl"
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            self.message_count += 1
            self.last_captured_text = text
            logger.info(f"Captured message #{self.message_count} ({len(text)} chars)")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
    
    def run(self, interval: int = 5):
        """Main loop - monitor and capture conversations."""
        logger.info(f"Starting conversation capture (checking every {interval}s)")
        logger.info("Press Ctrl+C to stop")
        
        retry_count = 0
        max_retries = 3
        
        try:
            while True:
                window = self.find_claude_window()

                
                if window:
                    retry_count = 0  # Reset retry counter
                    text = self.extract_conversation_text(window)
                    
                    if text:
                        self.parse_and_save_conversation(text)
                    else:
                        logger.debug("No text extracted from window")
                else:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.warning(f"Claude window not found after {max_retries} attempts")
                        logger.info("Waiting for Claude Desktop to open...")
                        retry_count = 0  # Reset and keep trying
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\nStopping conversation capture...")
            logger.info(f"Session ended. Captured {self.message_count} messages")
            logger.info(f"Session duration: {datetime.now() - self.session_start}")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)


def main():
    """Entry point for the conversation logger."""
    print("=" * 60)
    print("Claude Desktop Conversation Logger")
    print("=" * 60)
    print(f"Raw logs directory: {RAW_LOGS_DIR}")
    print(f"Log file: {LOG_FILE}")
    print("=" * 60)
    print()
    
    # Start the capture
    capturer = ConversationCapture()
    capturer.run(interval=5)


if __name__ == "__main__":
    main()
