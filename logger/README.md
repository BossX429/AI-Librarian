# Claude Desktop Conversation Logger

Automatically captures conversations from Claude Desktop in real-time using Windows UI Automation.

## 📁 Project Structure

```
C:\Projects\AI-Librarian\
└── logger\
    ├── claude_desktop_logger.py    # Main logger script
    ├── requirements.txt             # Python dependencies
    ├── setup.bat                    # Setup installer
    ├── start_logger.bat             # Quick start script
    ├── logger.log                   # Application logs
    ├── raw_logs\                    # Captured conversations (JSONL)
    │   └── claude_session_YYYYMMDD_HHMMSS.jsonl
    └── processed\                   # For future processing pipeline
```

## 🚀 Quick Start

### 1. Install Dependencies

Run the setup script:
```bash
setup.bat
```

This will install:
- `pywinauto` - Windows UI Automation
- `psutil` - Process management
- `pygetwindow` - Window detection
- `pywin32` - Windows API access

### 2. Start Logging

```bash
start_logger.bat
```

Or directly:
```bash
python claude_desktop_logger.py
```

### 3. Use Claude Desktop Normally

The logger will automatically:
- Detect when Claude Desktop is open
- Capture conversation text every 5 seconds
- Save to JSONL format with timestamps
- Handle window state changes gracefully

## 📊 Output Format

Conversations are saved as JSONL (JSON Lines) in `raw_logs/`:

```json
{
  "session_id": "claude_session_20251115_093000",
  "timestamp": "2025-11-15T09:30:05.123456",
  "message_number": 0,
  "raw_text": "User: Hello!\nClaude: Hi there! How can I help?",
  "text_hash": "abc123...",
  "capture_method": "windows_ui_automation"
}
```

## ✨ Features

- **Automatic Window Detection**: Finds Claude Desktop even if renamed
- **Change Detection**: Only saves when conversation changes (MD5 hashing)
- **Session Management**: Each run creates a new session file
- **Robust Error Handling**: Continues running even if window closes
- **Detailed Logging**: Full activity log in `logger.log`
- **Low Resource Usage**: Checks every 5 seconds (configurable)

## 🔧 Configuration

Edit `claude_desktop_logger.py` to customize:

```python
# Check interval (seconds)
capturer.run(interval=5)  # Default: 5 seconds

# Base directory
BASE_DIR = Path(r"C:\Projects\AI-Librarian\logger")
```

## 🐛 Troubleshooting

### "Claude Desktop window not found"
- Ensure Claude Desktop is running
- Try restarting both Claude and the logger
- Check that Windows UI Automation is enabled

### "Missing required package"
- Run `setup.bat` again
- Or manually: `pip install -r requirements.txt`

### Text not capturing
- Claude Desktop uses web view technology, which can be tricky
- Try clicking inside the Claude window to give it focus
- Check `logger.log` for detailed error messages

## 🔮 Future Enhancements

- [ ] Parse individual messages (User vs Assistant)
- [ ] Extract code blocks separately
- [ ] Detect conversation boundaries
- [ ] Export to markdown format
- [ ] Integration with vector databases
- [ ] Background Windows service mode
- [ ] Real-time indexing for search

## 📝 Notes

- Conversations are stored locally only
- No data is sent anywhere except Anthropic's official Claude service
- JSONL format allows easy streaming and processing
- Each line is a complete JSON object (easy to parse)
