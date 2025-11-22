# CLAUDE.md - AI Assistant Guide for AI Librarian

**Version:** 1.0
**Last Updated:** 2025-11-22
**Target Audience:** AI assistants (Claude, etc.) working on this codebase

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Design](#architecture--design)
3. [Codebase Structure](#codebase-structure)
4. [Development Conventions](#development-conventions)
5. [Key Technologies & Patterns](#key-technologies--patterns)
6. [Development Workflow](#development-workflow)
7. [Data Flow & File Formats](#data-flow--file-formats)
8. [Testing & Debugging](#testing--debugging)
9. [Platform-Specific Considerations](#platform-specific-considerations)
10. [Common Tasks & Patterns](#common-tasks--patterns)
11. [Important Gotchas & Known Issues](#important-gotchas--known-issues)
12. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## 📖 Project Overview

**AI Librarian** is an autonomous conversation capture and search system for Claude Desktop on Windows 11. It captures, compresses, and indexes all Claude conversations into a searchable SQLite database.

### Core Features
- **Fully Autonomous:** Set-and-forget 24/7 operation
- **Real-time Capture:** Windows UI Automation captures conversations
- **85% Compression:** Delta compression reduces 10MB → 1.5MB
- **Searchable Database:** SQLite with full-text search
- **Token-Efficient:** 90% token savings vs built-in Claude tools
- **100% Local:** No cloud dependencies, all data stays local

### Design Philosophy
- **Zero Dependencies (mostly):** Uses Python stdlib where possible
- **Autonomous Operation:** No manual intervention after setup
- **Windows-First:** Built specifically for Windows 11 + Claude Desktop
- **Simple & Robust:** Prefer simple, tested solutions over complex ones
- **Privacy-Focused:** Everything stays local on user's machine

---

## 🏗️ Architecture & Design

### Four-Agent System

The AI Librarian consists of 4 autonomous agents orchestrated together:

```
┌─────────────────────────────────────────────────┐
│     Orchestrator (autonomous_librarian.py)      │
│              ↓ manages ↓                        │
├─────────────┬───────────────┬──────────────────┤
│   Logger    │  Compressor   │    Curator       │
│  (24/7)     │  (every 5min) │  (after compress)│
│             │               │                  │
│ Captures → RAW → Compress → DELTA → Parse → DB │
└─────────────┴───────────────┴──────────────────┘
```

#### 1. **Logger** (`logger/claude_desktop_logger.py`)
- **Purpose:** Captures Claude Desktop conversations in real-time
- **Technology:** Windows UI Automation (pywinauto, pygetwindow, psutil)
- **Output:** JSONL files in `logger/raw_logs/`
- **Runs:** 24/7 as background subprocess
- **Capture Interval:** 5 seconds

#### 2. **Compressor** (`compressor/delta_compressor.py`)
- **Purpose:** Delta compression to reduce file sizes 85%
- **Algorithm:** Line-based diff using `difflib.SequenceMatcher`
- **Output:** Compressed JSONL files in `compressor/compressed/`
- **Runs:** Every 5 minutes (triggered by Orchestrator)
- **Processing:** Only compresses files older than 60 seconds

#### 3. **Curator** (`curator/claude_curator.py`)
- **Purpose:** Parses logs and organizes into searchable database
- **Technology:** SQLite3 with FTS (full-text search)
- **Output:** `curator/processed/conversations.db`
- **Runs:** After each compression (triggered by Orchestrator)
- **Features:** Message role detection, UI noise filtering, deduplication

#### 4. **Orchestrator** (`orchestrator/autonomous_librarian.py`)
- **Purpose:** Manages all agents autonomously
- **Responsibilities:**
  - Start/restart Logger subprocess
  - Monitor for new/updated log files
  - Trigger compression every 5 minutes
  - Trigger curation after compression
  - Health checks and auto-recovery
- **Runs:** 24/7 via Windows Task Scheduler
- **Logging:** `orchestrator/orchestrator.log`

### Additional Components

#### Query Tools (`query_tools/librarian_query.py`)
- **Purpose:** Token-efficient search interface for Claude integration
- **Technology:** Direct SQLite queries
- **Commands:** search, get, stats, date
- **Output:** Compact JSON (optimized for minimal tokens)
- **Use Case:** Allows Claude to query past conversations locally vs expensive cloud tools

---

## 📂 Codebase Structure

```
AI-Librarian/
│
├── orchestrator/               # Autonomous management
│   ├── autonomous_librarian.py # Main orchestrator (runs 24/7)
│   ├── install_autonomous.bat  # Setup Windows Task Scheduler
│   ├── start_manual.bat        # Manual testing mode
│   ├── stop_autonomous.bat     # Stop background process
│   └── uninstall_autonomous.bat# Remove from Task Scheduler
│
├── logger/                     # Conversation capture
│   ├── claude_desktop_logger.py# Main logger agent
│   ├── raw_logs/              # Raw JSONL captures (gitignored)
│   ├── processed/             # (unused, legacy)
│   ├── start_logger.bat       # Start logger manually
│   ├── setup.bat              # Install Python dependencies
│   ├── requirements.txt       # pywinauto, psutil, pygetwindow
│   └── README.md
│
├── compressor/                 # Delta compression
│   ├── delta_compressor.py    # Main compressor
│   ├── compressed/            # Compressed JSONL (gitignored)
│   └── README.md
│
├── curator/                    # Database & organization
│   ├── claude_curator.py      # Main curator agent
│   ├── processed/             # Output directory
│   │   └── conversations.db   # SQLite database (gitignored)
│   ├── run_curator.bat        # Run curator manually
│   ├── requirements.txt       # (empty - uses stdlib)
│   └── README.md
│
├── query_tools/                # Claude integration tools
│   ├── librarian_query.py     # Query interface
│   ├── PROJECT_INSTRUCTIONS.md# How to integrate with Claude
│   ├── COPY_TO_PROJECT.txt    # Quick setup instructions
│   └── README.md
│
├── process_all.bat             # Manual: compress + curate all logs
├── push_to_github.bat          # Git workflow helper
├── .gitignore                  # Ignores data files, keeps structure
│
└── Documentation/
    ├── README.md               # Main user-facing README
    ├── INSTALLATION.md         # Installation guide
    ├── QUICK_START.md          # Quick start guide
    ├── CONTRIBUTING.md         # Contribution guidelines
    ├── GITHUB_SETUP.md         # GitHub repository setup
    ├── READY_FOR_GITHUB.md     # Pre-publish checklist
    ├── COMPLETE.md             # Project completion notes
    └── CLAUDE.md              # This file
```

### File Naming Conventions

- **Python Scripts:** `snake_case.py`
- **Batch Files:** `snake_case.bat`
- **Documentation:** `UPPERCASE.md`
- **Session IDs:** `claude_session_YYYYMMDD_HHMMSS`
- **Raw Logs:** `claude_session_YYYYMMDD_HHMMSS.jsonl`
- **Compressed Logs:** `compressed_claude_session_YYYYMMDD_HHMMSS.jsonl`

---

## 💻 Development Conventions

### Code Style

#### Python
- **Style Guide:** PEP 8 compliant
- **Indentation:** 4 spaces (no tabs)
- **Line Length:** ~100 chars (flexible)
- **Encoding:** UTF-8 with BOM handling for Windows
- **Docstrings:** Triple-quoted strings for modules, classes, and functions

**Standard Header:**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Name - Brief Description
Longer description of what this module does.
"""
```

**Windows Console Encoding Fix (ALWAYS include in CLI scripts):**
```python
# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
```

#### Naming Conventions
- **Classes:** `PascalCase` (e.g., `ConversationCapture`, `DeltaCompressor`)
- **Functions/Methods:** `snake_case` (e.g., `find_claude_window()`, `compress_log_file()`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `RAW_LOGS_DIR`, `LOG_FILE`)
- **Private Methods:** `_leading_underscore()` (e.g., `_generate_session_id()`)

#### Error Handling
- **Defensive Programming:** Expect failures, handle gracefully
- **Fail Silently in Loops:** Log errors but continue processing
- **Loud Failures for Setup:** Raise exceptions during initialization
- **Always Log Errors:** Use `logger.error()` or `print()` to stderr

**Pattern:**
```python
try:
    # Attempt operation
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return default_value  # or continue, depending on context
```

#### Logging Standards
- **Use Emojis for Visual Scanning:** `🚀 ✅ ❌ ⚠️ 📊 🔴 ⚡ 🧠 🔍`
- **Timestamps:** ISO format or `%Y-%m-%d %H:%M:%S`
- **Log Levels:** INFO for normal operations, WARNING for recoverable issues, ERROR for failures

**Pattern:**
```python
self.log("🚀 Starting operation...")
self.log("✅ Operation complete")
self.log("⚠️ Warning: retrying...")
self.log("❌ Operation failed")
```

### Import Organization

**Standard order:**
```python
# 1. Standard library imports
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 2. Third-party imports
try:
    from pywinauto import Application
    import psutil
except ImportError as e:
    print(f"Missing package: {e}")
    sys.exit(1)

# 3. Local imports (if any)
from .utils import helper_function
```

### Path Handling

**ALWAYS use `pathlib.Path` for cross-platform compatibility:**
```python
# Good
self.project_root = Path(__file__).parent.parent
self.db_path = self.output_dir / "conversations.db"

# Avoid
import os.path
db_path = os.path.join(output_dir, "conversations.db")
```

### Database Conventions

#### Schema Design
- **Auto-increment IDs:** All tables have `id INTEGER PRIMARY KEY AUTOINCREMENT`
- **Timestamps:** Store as TEXT in ISO 8601 format
- **Foreign Keys:** Use explicit `FOREIGN KEY` constraints
- **Indexes:** Create indexes on frequently queried columns

#### Query Patterns
- **Always use parameterized queries:** Prevent SQL injection
- **Close connections:** Use try/finally or context managers
- **Commit explicitly:** Don't rely on autocommit

**Pattern:**
```python
conn = sqlite3.connect(self.db_path)
cursor = conn.cursor()
try:
    cursor.execute('SELECT * FROM table WHERE id = ?', (value,))
    result = cursor.fetchone()
    conn.commit()
finally:
    conn.close()
```

---

## 🔧 Key Technologies & Patterns

### Core Technologies

#### 1. **Python Standard Library (Preferred)**
- `json` - JSONL file handling
- `sqlite3` - Database operations
- `pathlib` - File path operations
- `subprocess` - Process management
- `datetime` - Timestamp handling
- `hashlib` - Content hashing (MD5)
- `difflib` - Delta compression algorithm
- `re` - Regular expressions for filtering

#### 2. **Windows-Specific (Logger only)**
- `pywinauto` - UI Automation framework
- `psutil` - Process monitoring
- `pygetwindow` - Window management

#### 3. **Data Formats**
- **JSONL (JSON Lines):** One JSON object per line
- **SQLite3:** Embedded database
- **UTF-8 Encoding:** All text files

### Key Algorithms

#### Delta Compression (`difflib.SequenceMatcher`)
```python
# Line-based diff algorithm
old_lines = old_text.splitlines(keepends=True)
new_lines = new_text.splitlines(keepends=True)
differ = difflib.SequenceMatcher(None, old_lines, new_lines)
opcodes = differ.get_opcodes()

# Opcodes: 'equal', 'replace', 'delete', 'insert'
for tag, i1, i2, j1, j2 in opcodes:
    if tag == 'replace':
        # Store replacement
    elif tag == 'insert':
        # Store insertion
    # etc.
```

**Compression Types:**
- `full` - First capture, stores complete content
- `identical` - No changes, stores nothing
- `delta` - Stores only changes (most common)

#### UI Noise Filtering
```python
# Patterns to ignore from Claude Desktop UI
ui_noise_patterns = [
    r'^(New chat|Chats|Projects|Artifacts)',
    r'^(Chrome Legacy Window|Minimize|Restore)',
    # etc.
]
```

### Design Patterns

#### 1. **Subprocess Management Pattern**
```python
# Start background process
self.process = subprocess.Popen(
    [sys.executable, script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
)

# Health check
poll = self.process.poll()
if poll is None:
    # Still running
else:
    # Died, restart
```

#### 2. **Batch Processing Pattern**
```python
# Process all files in directory
for file_path in directory.glob("*.jsonl"):
    # Check if already processed
    if should_skip(file_path):
        continue

    # Process file
    process_file(file_path)

    # Track as processed
    mark_processed(file_path)
```

#### 3. **Deduplication Pattern**
```python
# Track seen content by hash
seen_hashes = set()

for item in items:
    item_hash = item.get('hash')

    if item_hash in seen_hashes:
        continue  # Skip duplicate

    seen_hashes.add(item_hash)
    process(item)
```

---

## 🔄 Development Workflow

### Setting Up Development Environment

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/AI-Librarian.git
cd AI-Librarian

# 2. Install logger dependencies (only component with deps)
cd logger
pip install -r requirements.txt

# 3. No other setup needed - uses Python stdlib
```

### Testing Individual Components

#### Test Logger (Manually)
```bash
cd logger
python claude_desktop_logger.py
# Should start capturing, creates files in raw_logs/
# Ctrl+C to stop
```

#### Test Compressor
```bash
cd compressor
python delta_compressor.py compress
# Should compress all files in ../logger/raw_logs/
# Output to compressed/
```

#### Test Curator
```bash
cd curator
python claude_curator.py
# Should process all logs and create conversations.db
```

#### Test Query Tools
```bash
cd query_tools
python librarian_query.py search "test" 5
# Should query database and return JSON results
```

### Making Changes

#### Adding Features
1. **Identify the component** - Logger, Compressor, Curator, or Orchestrator
2. **Read the component's README** - Understand current implementation
3. **Test standalone** - Run component manually first
4. **Test with Orchestrator** - Ensure integration works
5. **Update documentation** - Update relevant README files

#### Modifying Database Schema
1. **Update `init_database()` in curator** - Add/modify tables
2. **Consider migrations** - Existing databases won't auto-update
3. **Update query tools** - Ensure queries work with new schema
4. **Test with fresh database** - Delete old DB and regenerate

#### Performance Considerations
- **Compressor:** Optimize for large files (>10MB)
- **Curator:** Batch database inserts for speed
- **Logger:** Keep capture interval ≥5 seconds to avoid overload
- **Orchestrator:** Don't block on long operations, use timeouts

### Git Workflow

```bash
# Current branch convention
git checkout -b claude/feature-name-session-id

# Making changes
git add .
git commit -m "Brief description of changes"

# Push to remote
git push -u origin claude/feature-name-session-id
```

**Commit Message Style:**
- Imperative mood: "Add feature" not "Added feature"
- Be specific: "Fix compressor timeout on large files" not "Fix bug"
- Reference issues if applicable: "Fix #123: Logger crash on..."

---

## 📊 Data Flow & File Formats

### Complete Data Pipeline

```
1. Claude Desktop (User interaction)
   ↓
2. Logger captures screen every 5s
   ↓ writes to
3. raw_logs/claude_session_YYYYMMDD_HHMMSS.jsonl
   ↓ compressed by
4. Compressor (every 5 minutes)
   ↓ writes to
5. compressed/compressed_claude_session_YYYYMMDD_HHMMSS.jsonl
   ↓ parsed by
6. Curator
   ↓ stores in
7. processed/conversations.db (SQLite)
   ↓ queried by
8. Query Tools → JSON output → Claude integration
```

### File Formats

#### Raw Log Format (JSONL)
```json
{
  "session_id": "claude_session_20251115_094309",
  "timestamp": "2025-11-15T09:43:10.123456",
  "message_number": 0,
  "raw_text": "Full UI capture including conversation...",
  "text_hash": "md5hash",
  "capture_method": "windows_ui_automation"
}
```

#### Compressed Log Format (JSONL)
```json
{
  "session_id": "claude_session_20251115_094309",
  "timestamp": "2025-11-15T09:43:10.123456",
  "message_number": 0,
  "text_hash": "md5hash",
  "capture_method": "windows_ui_automation",
  "diff": {
    "type": "delta",
    "changes": [
      {
        "op": "insert",
        "position": 10,
        "new_lines": ["New text here\n"]
      }
    ],
    "size": 150,
    "original_size": 1500,
    "compression_ratio": 0.9
  }
}
```

#### Database Schema

**conversations table:**
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE,
    start_time TEXT,
    end_time TEXT,
    message_count INTEGER,
    total_chars INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**messages table:**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    message_number INTEGER,
    role TEXT,  -- 'user' or 'assistant'
    content TEXT,
    timestamp TEXT,
    content_hash TEXT,
    tokens_estimate INTEGER,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

**Indexes:**
```sql
CREATE INDEX idx_content ON messages(content);
CREATE INDEX idx_timestamp ON messages(timestamp);
CREATE INDEX idx_conversation ON messages(conversation_id);
```

#### Query Tool Output Format (JSON)
```json
{
  "found": 3,
  "query": "compression",
  "results": [
    {
      "session_id": "claude_session_20251115_094309",
      "timestamp": "2025-11-15T09:43:10",
      "role": "assistant",
      "snippet": "...we decided to use delta compression..."
    }
  ]
}
```

---

## 🧪 Testing & Debugging

### Manual Testing

#### End-to-End Test
```bash
# 1. Start orchestrator manually (with console output)
cd orchestrator
start_manual.bat

# 2. Open Claude Desktop and have a conversation

# 3. Wait 1 minute, verify raw log created
dir ..\logger\raw_logs\

# 4. Wait 5 minutes, verify compression
dir ..\compressor\compressed\

# 5. Verify database updated
cd ..\curator
python claude_curator.py stats

# 6. Test search
cd ..\query_tools
python librarian_query.py search "test" 5
```

#### Component Testing

**Logger Health Check:**
```bash
# Check if logger is capturing
cd logger
dir raw_logs\

# Check latest file is growing
type raw_logs\claude_session_*.jsonl
```

**Compressor Verification:**
```bash
# Manually trigger compression
cd compressor
python delta_compressor.py compress

# Check compression ratio in output
# Should show ~85% compression
```

**Curator Verification:**
```bash
# Check database contents
cd curator
python claude_curator.py stats

# Search for known content
python claude_curator.py search "known phrase"
```

### Debugging Tips

#### Logger Not Capturing
- **Check:** Is Claude Desktop running?
- **Check:** Windows UI Automation enabled?
- **Check:** Dependencies installed? (`pip install -r requirements.txt`)
- **Run manually:** See console output for errors

#### Compression Not Working
- **Check:** Are there raw logs in `logger/raw_logs/`?
- **Check:** Files older than 60 seconds?
- **Run manually:** `python delta_compressor.py compress`
- **Check permissions:** Can write to `compressed/` directory?

#### Database Not Updating
- **Check:** Is curator being triggered?
- **Check:** Are there compressed logs?
- **Run manually:** `python claude_curator.py`
- **Check logs:** Look for database errors

#### Orchestrator Issues
- **Check Task Manager:** Is `pythonw.exe` running?
- **Check logs:** `type orchestrator\orchestrator.log`
- **Check permissions:** Run Task Scheduler as Administrator
- **Run manually:** Use `start_manual.bat` to see console output

### Log Analysis

**Orchestrator log patterns:**
```
[2025-11-15 10:07:11] 🚀 Autonomous AI Librarian Starting...
[2025-11-15 10:07:11] 🔴 Starting Logger Agent...
[2025-11-15 10:07:11] ✅ Logger started (PID: 19756)
[2025-11-15 10:12:15] ⚡ Compressing 1 log file(s)...
[2025-11-15 10:12:16] ✅ Compression complete
[2025-11-15 10:12:18] 🧠 Running Curator...
[2025-11-15 10:12:20] ✅ Curator complete
[2025-11-15 10:17:11] 📊 Status: Logger=True, Raw=2, Compressed=3
```

---

## 🖥️ Platform-Specific Considerations

### Windows 11 Specific

#### Task Scheduler Integration
- **Location:** Task Scheduler → Task Scheduler Library → "AI Librarian Autonomous"
- **Trigger:** At log on
- **Action:** `pythonw.exe C:\Projects\AI-Librarian\orchestrator\autonomous_librarian.py`
- **Settings:** Run whether user is logged on or not

#### UI Automation Requirements
- **pywinauto:** Requires Windows UI Automation framework
- **Accessibility:** Windows accessibility features must be enabled
- **Permissions:** No admin required for UI Automation
- **Compatibility:** Windows 11 only (Windows 10 may work but untested)

#### Console Encoding
**Critical for Windows:** Always include encoding fix in CLI scripts
```python
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
```

#### Batch File Conventions
- **Encoding:** UTF-8 without BOM
- **Line Endings:** CRLF (`\r\n`)
- **Paths:** Use absolute paths or `%~dp0` for script directory
- **Echo:** Use `@echo off` at start
- **Pause:** Use `pause` at end for manual runs

### Path Conventions

**Expected installation path:**
```
C:\Projects\AI-Librarian\
```

**If changing paths, update:**
- `logger/claude_desktop_logger.py` - `BASE_DIR` constant
- Batch files - Hardcoded paths
- Documentation - Example paths

---

## 🎯 Common Tasks & Patterns

### Task: Add New Search Capability

**Example: Add regex search to query tools**

1. **Update `LibrarianQuery` class:**
```python
def search_regex(self, pattern: str, limit: int = 5):
    """Search using regex pattern."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()

    # SQLite doesn't have native regex, so fetch all and filter
    cursor.execute('SELECT * FROM messages')
    # ... implement regex filtering
```

2. **Update CLI handler in `main()`:**
```python
elif command == "regex":
    pattern = sys.argv[2]
    result = librarian.search_regex(pattern)
```

3. **Update documentation:**
- `query_tools/README.md`
- `query_tools/PROJECT_INSTRUCTIONS.md`

### Task: Optimize Compression Ratio

**Pattern: Adjust compression algorithm**

1. **Modify `delta_compressor.py`:**
```python
def compute_diff(self, old_text: str, new_text: str) -> Dict:
    # Try different diff algorithms
    # - Character-based vs line-based
    # - Different context window sizes
    # - Custom compression for repeated patterns
```

2. **Add metrics:**
```python
# Track compression ratio per file
stats = {
    'compression_ratio': ...,
    'algorithm': 'line_based',
    'context_window': 3
}
```

3. **Benchmark:**
```bash
# Test on real logs
python delta_compressor.py compress
# Compare file sizes before/after
```

### Task: Add New Database Field

**Example: Add user tags to conversations**

1. **Update schema in `curator/claude_curator.py`:**
```python
def init_database(self):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            ...
            tags TEXT,  -- New field: comma-separated tags
            ...
        )
    ''')
```

2. **Handle migration:**
```python
# Check if column exists, add if missing
cursor.execute("PRAGMA table_info(conversations)")
columns = [col[1] for col in cursor.fetchall()]
if 'tags' not in columns:
    cursor.execute("ALTER TABLE conversations ADD COLUMN tags TEXT")
```

3. **Update query tools:**
```python
def search_by_tag(self, tag: str):
    cursor.execute('''
        SELECT * FROM conversations
        WHERE tags LIKE ?
    ''', (f'%{tag}%',))
```

### Task: Add Error Recovery

**Pattern: Graceful degradation**

```python
class RobustProcessor:
    def process_files(self, files: List[Path]):
        """Process files with error recovery."""
        failed = []

        for file_path in files:
            try:
                self.process_file(file_path)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                failed.append((file_path, str(e)))
                continue  # Don't let one failure stop all processing

        # Report failures at end
        if failed:
            logger.warning(f"Failed to process {len(failed)} files")
            for path, error in failed:
                logger.warning(f"  - {path.name}: {error}")
```

---

## ⚠️ Important Gotchas & Known Issues

### Known Issues

#### 1. **Logger May Miss Content**
- **Issue:** UI Automation captures visible text only
- **Impact:** Hidden/scrolled content not captured
- **Workaround:** Capture interval ensures incremental capture
- **Status:** Acceptable tradeoff for performance

#### 2. **Compression Doesn't Reduce DB Size**
- **Issue:** Curator uses original text, not compressed
- **Reason:** Database needs full text for searching
- **Impact:** Compressed files save disk space, not DB space
- **Future:** Consider storing compressed in DB, decompress on query

#### 3. **Role Detection Heuristic**
- **Issue:** `detect_message_role()` uses heuristics, not perfect
- **Accuracy:** ~80% based on message length/content patterns
- **Impact:** Some messages may be tagged wrong (user vs assistant)
- **Future:** Improve with ML or UI element detection

#### 4. **Windows-Only**
- **Issue:** Heavily dependent on Windows UI Automation
- **Impact:** Not portable to Linux/macOS
- **Future:** Would require complete Logger rewrite for other platforms

### Common Pitfalls

#### Don't: Modify Files While Orchestrator Running
- **Risk:** Race conditions, corrupted files
- **Solution:** Stop orchestrator first (`stop_autonomous.bat`)

#### Don't: Delete Raw Logs Immediately
- **Risk:** Compressor may not have processed them yet
- **Solution:** Check `compressed/` directory first, only delete after compression

#### Don't: Manually Edit Database
- **Risk:** Corrupted indexes, broken foreign keys
- **Solution:** Use curator functions or proper SQL transactions

#### Don't: Change Session ID Format
- **Risk:** Breaks deduplication, file matching
- **Format:** `claude_session_YYYYMMDD_HHMMSS` (exact format required)

#### Don't: Use `print()` for Long-Running Processes
- **Issue:** Output buffers can fill up in background mode
- **Solution:** Always log to file, not just console

---

## 🤖 AI Assistant Guidelines

### When Working on This Codebase

#### 1. **Understand the Agent System**
- This is a 4-agent autonomous system
- Changes to one agent may affect others
- Always consider the full pipeline: Logger → Compressor → Curator → Query

#### 2. **Test Standalone First**
- Before testing with orchestrator, run components manually
- Easier to debug when run directly with console output
- Use provided batch files for manual testing

#### 3. **Preserve Autonomous Operation**
- Core feature: zero manual intervention
- Don't add features requiring user interaction
- Error recovery should be automatic

#### 4. **Maintain Windows Compatibility**
- Always test on Windows 11
- Use Windows-compatible path handling (`Path` not `os.path`)
- Include console encoding fix in all CLI scripts

#### 5. **Keep Dependencies Minimal**
- Prefer stdlib over third-party libraries
- Only Logger needs external dependencies
- Document any new dependencies clearly

#### 6. **Log Everything Important**
- User can't see what's happening in background
- Logs are the only visibility into operation
- Use emojis for quick visual parsing

#### 7. **Be Defensive**
- Expect files to be missing, processes to crash, permissions to fail
- Graceful degradation > crashes
- Log errors and continue when possible

#### 8. **Optimize for Token Efficiency**
- Query tools are designed for minimal token usage
- Keep JSON output compact
- Provide snippets, not full content

### Checklist for Changes

Before committing changes, verify:

- [ ] **Standalone test passed** - Component works in isolation
- [ ] **Integration test passed** - Works with orchestrator
- [ ] **Windows encoding handled** - UTF-8 encoding fix included
- [ ] **Paths use `pathlib`** - No hardcoded `\` or `/`
- [ ] **Errors logged** - All exceptions logged with context
- [ ] **Database changes tested** - Fresh DB works, existing DB migrates
- [ ] **Documentation updated** - Relevant README files updated
- [ ] **No manual intervention required** - Maintains autonomous operation
- [ ] **Backwards compatible** - Existing data still works

### Common Modification Patterns

#### Adding a New Feature
```python
# 1. Add to appropriate agent class
class AgentClass:
    def new_feature(self):
        """Docstring explaining what this does."""
        try:
            # Implementation
            result = self.do_something()
            self.log("✅ Feature completed")
            return result
        except Exception as e:
            self.log(f"❌ Feature failed: {e}")
            return None

# 2. Add CLI interface
def main():
    if command == "new_feature":
        agent.new_feature()

# 3. Document in README
# 4. Test manually
# 5. Test with orchestrator
```

#### Modifying Data Format
```python
# ALWAYS maintain backwards compatibility

def parse_entry(entry: dict) -> dict:
    """Parse entry, supporting old and new formats."""
    # New format
    if 'new_field' in entry:
        return entry['new_field']

    # Old format fallback
    elif 'old_field' in entry:
        return convert_old_to_new(entry['old_field'])

    # Default
    else:
        return default_value
```

### Understanding the User

**Target User:**
- Windows 11 user
- Claude Desktop power user
- Wants "set and forget" solution
- Values privacy (local-only)
- Not necessarily technical

**Design Implications:**
- Simple installation (one batch file)
- Zero configuration needed
- Autonomous operation essential
- Privacy is critical feature
- Errors should self-recover

---

## 📚 Additional Resources

### Key Documentation Files
- `README.md` - User-facing overview
- `INSTALLATION.md` - Installation instructions
- `CONTRIBUTING.md` - How to contribute
- `query_tools/PROJECT_INSTRUCTIONS.md` - Claude integration guide

### Component READMEs
- `orchestrator/README.md` - Orchestrator details
- `logger/README.md` - Logger implementation
- `compressor/README.md` - Compression algorithm
- `curator/README.md` - Database schema
- `query_tools/README.md` - Query interface

### External References
- [pywinauto docs](https://pywinauto.readthedocs.io/) - UI Automation
- [Python difflib](https://docs.python.org/3/library/difflib.html) - Diff algorithm
- [SQLite FTS](https://www.sqlite.org/fts5.html) - Full-text search

---

## 🎓 Quick Reference

### File Paths
```python
project_root = Path(__file__).parent.parent
raw_logs = project_root / "logger" / "raw_logs"
compressed = project_root / "compressor" / "compressed"
database = project_root / "curator" / "processed" / "conversations.db"
```

### Common Commands
```bash
# Start autonomous mode (once)
orchestrator\install_autonomous.bat

# Stop autonomous mode
orchestrator\stop_autonomous.bat

# Manual testing
orchestrator\start_manual.bat

# Search conversations
cd query_tools
python librarian_query.py search "query" 5

# Database stats
cd curator
python claude_curator.py stats
```

### Timeouts & Intervals
- **Logger capture:** 5 seconds
- **Compression trigger:** 5 minutes (300s)
- **Minimum file age:** 60 seconds before processing
- **Compressor timeout:** 2 minutes (120s)
- **Curator timeout:** 3 minutes (180s)
- **Status logging:** Every 10 minutes (20 cycles × 30s)

### Emoji Legend
- 🚀 Starting/Launching
- ✅ Success/Complete
- ❌ Error/Failure
- ⚠️ Warning/Retry
- 📊 Statistics/Summary
- 🔴 Logger-related
- ⚡ Compressor-related
- 🧠 Curator-related
- 🔍 Search/Query-related
- 📂 File operations
- 💾 Database operations

---

**End of CLAUDE.md**

*Last Updated: 2025-11-22*
*For AI Librarian v1.0*
