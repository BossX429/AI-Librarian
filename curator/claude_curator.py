#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Desktop Curator
Processes raw logs from the Logger and extracts structured conversations.

The Curator reads JSONL files from the Logger, filters out UI noise,
extracts actual conversation messages, and organizes them into
structured, searchable conversations.
"""

import json
import re
import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class ClaudeCurator:
    """
    Curator Agent for processing Claude Desktop conversation logs.
    
    Responsibilities:
    1. Parse raw JSONL files from Logger
    2. Extract actual conversation content (filter UI noise)
    3. Detect message boundaries and conversation structure
    4. Store in SQLite database for efficient querying
    5. Create searchable index of conversations
    """
    
    def __init__(self, raw_logs_dir: str, output_dir: str):
        self.raw_logs_dir = Path(raw_logs_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Database path
        self.db_path = self.output_dir / "conversations.db"
        
        # Initialize database
        self.init_database()
        
        # Patterns to identify different message types
        self.ui_noise_patterns = [
            r'^(New chat|Chats|Projects|Artifacts|Code|Starred)',
            r'^(Chrome Legacy Window|Minimize|Restore|Close)',
            r'^(Sidebar|Home|Claude)',
            r'^(How can I help you today\?)',
            r'^(Claude can make mistakes)',
            r'(Notifications|Project content)',
        ]
        
    def init_database(self):
        """Initialize SQLite database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                start_time TEXT,
                end_time TEXT,
                message_count INTEGER,
                total_chars INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                message_number INTEGER,
                role TEXT,  -- 'user' or 'assistant'
                content TEXT,
                timestamp TEXT,
                content_hash TEXT,
                tokens_estimate INTEGER,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')
        
        # Create indexes for faster searching
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_content ON messages(content)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation ON messages(conversation_id)')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized at {self.db_path}")
    
    def is_ui_noise(self, text: str) -> bool:
        """Check if text is UI noise that should be filtered out."""
        for pattern in self.ui_noise_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def extract_conversation_content(self, raw_text: str) -> Optional[str]:
        """
        Extract actual conversation content from raw UI capture.
        
        The raw_text contains everything visible in Claude Desktop,
        including UI elements, sidebars, etc. We need to extract
        just the conversation messages.
        """
        lines = raw_text.split('\n')
        
        # Filter out UI noise
        clean_lines = []
        for line in lines:
            line = line.strip()
            if line and not self.is_ui_noise(line):
                clean_lines.append(line)
        
        # Join and return
        content = '\n'.join(clean_lines)
        return content if content else None
    
    def parse_raw_log(self, log_file: Path) -> List[Dict]:
        """Parse a raw JSONL log file."""
        messages = []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            msg = json.loads(line)
                            messages.append(msg)
                        except json.JSONDecodeError as e:
                            print(f"⚠️  Failed to parse line: {e}")
                            continue
        except Exception as e:
            print(f"❌ Error reading {log_file}: {e}")
            return []
        
        return messages
    
    def detect_message_role(self, content: str, prev_content: str = "") -> str:
        """
        Detect if a message is from 'user' or 'assistant'.
        
        Heuristics:
        - Short messages are usually user input
        - Messages with thinking blocks are assistant
        - Messages with tool calls are assistant
        - Messages with code blocks are often assistant
        """
        # Check for assistant indicators
        if "```" in content:  # Code blocks
            return "assistant"
        if "Request {" in content and "Response" in content:  # Tool calls
            return "assistant"
        if len(content) > 500:  # Long responses usually assistant
            return "assistant"
        
        # Check for user indicators
        if len(content) < 200 and not any(indicator in content for indicator in ["✅", "📊", "🎯"]):
            return "user"
        
        # Default to assistant for longer content
        return "assistant" if len(content) > 200 else "user"
    
    def estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count (1 token ≈ 4 chars)."""
        return len(text) // 4
    
    def process_log_file(self, log_file: Path):
        """
        Process a single raw log file and extract conversations.
        """
        print(f"\n📂 Processing: {log_file.name}")
        
        # Parse the raw log
        raw_messages = self.parse_raw_log(log_file)
        
        if not raw_messages:
            print("⚠️  No messages found in log file")
            return
        
        print(f"📥 Found {len(raw_messages)} raw captures")
        
        # Extract session info
        session_id = raw_messages[0].get('session_id', 'unknown')
        
        # Track unique content by hash to avoid duplicates
        seen_hashes = set()
        extracted_messages = []
        
        for raw_msg in raw_messages:
            text_hash = raw_msg.get('text_hash')
            raw_text = raw_msg.get('raw_text', '')
            timestamp = raw_msg.get('timestamp')
            
            # Skip if we've seen this exact content before
            if text_hash in seen_hashes:
                continue
            seen_hashes.add(text_hash)
            
            # Extract actual conversation content
            content = self.extract_conversation_content(raw_text)
            
            if content and len(content) > 50:  # Minimum meaningful content
                extracted_messages.append({
                    'content': content,
                    'timestamp': timestamp,
                    'content_hash': text_hash
                })
        
        print(f"✨ Extracted {len(extracted_messages)} unique messages")
        
        # Store in database
        self.store_conversation(session_id, extracted_messages)
    
    def store_conversation(self, session_id: str, messages: List[Dict]):
        """Store extracted conversation in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if conversation already exists
            cursor.execute('SELECT id FROM conversations WHERE session_id = ?', (session_id,))
            existing = cursor.fetchone()
            
            if existing:
                print(f"⚠️  Conversation {session_id} already exists, skipping")
                return
            
            # Calculate conversation stats
            start_time = messages[0]['timestamp'] if messages else None
            end_time = messages[-1]['timestamp'] if messages else None
            total_chars = sum(len(msg['content']) for msg in messages)
            
            # Insert conversation
            cursor.execute('''
                INSERT INTO conversations (session_id, start_time, end_time, message_count, total_chars)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, start_time, end_time, len(messages), total_chars))
            
            conversation_id = cursor.lastrowid
            
            # Insert messages
            prev_content = ""
            for idx, msg in enumerate(messages):
                role = self.detect_message_role(msg['content'], prev_content)
                tokens = self.estimate_tokens(msg['content'])
                
                cursor.execute('''
                    INSERT INTO messages (conversation_id, message_number, role, content, 
                                        timestamp, content_hash, tokens_estimate)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (conversation_id, idx, role, msg['content'], 
                      msg['timestamp'], msg['content_hash'], tokens))
                
                prev_content = msg['content']
            
            conn.commit()
            print(f"✅ Stored conversation: {session_id} ({len(messages)} messages, {total_chars:,} chars)")
            
        except Exception as e:
            print(f"❌ Error storing conversation: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def export_conversation_to_json(self, session_id: str, output_file: Path):
        """Export a conversation to JSON format."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get conversation
        cursor.execute('SELECT * FROM conversations WHERE session_id = ?', (session_id,))
        conv = cursor.fetchone()
        
        if not conv:
            print(f"❌ Conversation {session_id} not found")
            return
        
        # Get messages
        cursor.execute('''
            SELECT message_number, role, content, timestamp, tokens_estimate
            FROM messages
            WHERE conversation_id = ?
            ORDER BY message_number
        ''', (conv[0],))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'message_number': row[0],
                'role': row[1],
                'content': row[2],
                'timestamp': row[3],
                'tokens_estimate': row[4]
            })
        
        # Create export object
        export_data = {
            'session_id': conv[1],
            'start_time': conv[2],
            'end_time': conv[3],
            'message_count': conv[4],
            'total_chars': conv[5],
            'messages': messages
        }
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported to {output_file}")
        conn.close()
    
    def process_all_logs(self):
        """Process all raw log files in the input directory."""
        log_files = sorted(self.raw_logs_dir.glob("*.jsonl"))
        
        if not log_files:
            print(f"⚠️  No JSONL files found in {self.raw_logs_dir}")
            return
        
        print(f"\n🔍 Found {len(log_files)} log files to process")
        print("=" * 60)
        
        for log_file in log_files:
            self.process_log_file(log_file)
        
        # Show summary
        self.show_summary()
    
    def show_summary(self):
        """Display summary of stored conversations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM conversations')
        conv_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM messages')
        msg_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(total_chars) FROM conversations')
        total_chars = cursor.fetchone()[0] or 0
        
        print("\n" + "=" * 60)
        print("📊 CURATOR SUMMARY")
        print("=" * 60)
        print(f"📚 Conversations: {conv_count}")
        print(f"💬 Messages: {msg_count}")
        print(f"📝 Total Characters: {total_chars:,}")
        print(f"💾 Database: {self.db_path}")
        print("=" * 60)
        
        conn.close()
    
    def search_conversations(self, query: str, limit: int = 10):
        """Search for conversations containing a query string."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.session_id, c.start_time, m.role, m.content, m.timestamp
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE m.content LIKE ?
            ORDER BY m.timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = cursor.fetchall()
        
        if not results:
            print(f"🔍 No results found for '{query}'")
        else:
            print(f"\n🔍 Found {len(results)} results for '{query}'")
            print("=" * 60)
            for session_id, start_time, role, content, timestamp in results:
                print(f"\n📅 {timestamp}")
                print(f"👤 {role.upper()}")
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"💬 {preview}")
                print("-" * 60)
        
        conn.close()


def main():
    """Main execution function."""
    import sys
    
    # Default paths
    raw_logs_dir = Path(__file__).parent.parent / "logger" / "raw_logs"
    output_dir = Path(__file__).parent / "processed"
    
    # Initialize curator
    curator = ClaudeCurator(str(raw_logs_dir), str(output_dir))
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "search" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            curator.search_conversations(query)
        elif command == "export" and len(sys.argv) > 2:
            session_id = sys.argv[2]
            output_file = output_dir / f"{session_id}.json"
            curator.export_conversation_to_json(session_id, output_file)
        else:
            print("Usage:")
            print("  python claude_curator.py              # Process all logs")
            print("  python claude_curator.py search <query>  # Search conversations")
            print("  python claude_curator.py export <session_id>  # Export to JSON")
    else:
        # Default action: process all logs
        curator.process_all_logs()


if __name__ == "__main__":
    main()
    
    def read_compressed_log(self, compressed_file: Path) -> List[str]:
        """
        Read and decompress a compressed log file on-the-fly.
        Returns list of full text content for each capture.
        """
        try:
            with open(compressed_file, 'r', encoding='utf-8') as f:
                compressed_captures = [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error reading compressed file: {e}")
            return []
        
        # Decompress on-the-fly
        decompressed_texts = []
        previous_text = ''
        
        for compressed in compressed_captures:
            diff_data = compressed['diff']
            
            # Reconstruct full text
            if diff_data['type'] == 'full':
                full_text = diff_data['content']
            elif diff_data['type'] == 'identical':
                full_text = previous_text
            elif diff_data['type'] == 'delta':
                # Reconstruct from delta
                lines = previous_text.splitlines(keepends=True)
                
                for change in diff_data['changes']:
                    op = change['op']
                    
                    if op == 'replace':
                        start = change['old_start']
                        end = change['old_end']
                        lines[start:end] = change['new_lines']
                    elif op == 'delete':
                        start = change['old_start']
                        end = change['old_end']
                        del lines[start:end]
                    elif op == 'insert':
                        pos = change['position']
                        lines[pos:pos] = change['new_lines']
                
                full_text = ''.join(lines)
            else:
                full_text = ''
            
            # Build reconstructed message
            decompressed_texts.append({
                'session_id': compressed['session_id'],
                'timestamp': compressed['timestamp'],
                'message_number': compressed['message_number'],
                'text_hash': compressed['text_hash'],
                'raw_text': full_text
            })
            
            previous_text = full_text
        
        return decompressed_texts
    
    def parse_raw_log(self, log_file: Path) -> List[Dict]:
        """Parse a raw JSONL log file (works with both raw and compressed)."""
        
        # Check if it's a compressed file
        if 'compressed_' in log_file.name:
            print(f"   📦 Detected compressed file, decompressing on-the-fly...")
            return self.read_compressed_log(log_file)
        
        # Regular raw file parsing (original code)
        messages = []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            msg = json.loads(line)
                            messages.append(msg)
                        except json.JSONDecodeError as e:
                            print(f"⚠️  Failed to parse line: {e}")
                            continue
        except Exception as e:
            print(f"❌ Error reading {log_file}: {e}")
            return []
        
        return messages
