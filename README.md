# AI Librarian

**Autonomous conversation capture and search for Claude Desktop**

Never lose a conversation again. The AI Librarian automatically captures, compresses, and indexes all your Claude Desktop conversations into a searchable database - completely autonomously.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2011-blue)](https://www.microsoft.com/windows)

## 🎯 Features

- 🤖 **Fully Autonomous** - Set it and forget it, runs 24/7
- 🔴 **Real-time Capture** - Records every Claude conversation automatically
- ⚡ **85% Compression** - Smart delta compression (10 MB → 1.5 MB)
- 🧠 **Searchable Database** - Instant full-text search across all conversations
- 🔍 **Query Tools** - 90% token savings vs built-in Claude tools
- 🚀 **Fast** - 10-100x faster processing with compression
- 🔐 **Private** - Everything stays local on your machine
- ⏰ **Auto-Start** - Starts with Windows, requires zero maintenance

## 🚀 Quick Start

### Prerequisites

- Windows 11
- Python 3.7+ (included with Windows)
- Claude Desktop

### Installation (30 Seconds)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Librarian.git
   cd AI-Librarian
   ```

2. **Install autonomous mode (Run as Administrator):**
   ```bash
   cd orchestrator
   install_autonomous.bat
   ```

3. **Done!** The AI Librarian now:
   - ✅ Auto-starts with Windows
   - ✅ Captures all conversations
   - ✅ Compresses automatically
   - ✅ Updates database every 5 minutes
   - ✅ Runs forever with zero maintenance

### Search Your Conversations

```bash
cd curator
python claude_curator.py search "your query"
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Compression Ratio** | 85% (10 MB → 1.5 MB) |
| **Processing Speed** | 10-100x faster |
| **Query Speed** | < 1 second |
| **Token Savings** | 90% vs cloud tools |
| **CPU Usage** | < 1% (mostly idle) |
| **RAM Usage** | ~50 MB |

## 🏗️ Architecture

```
┌──────────────────────────────────────────────┐
│      🤖 Orchestrator (Background)            │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Logger  │→│Compressor│→│ Curator  │→ DB│
│  │  24/7    │  │ Every    │  │  Auto    │   │
│  │          │  │ 5 min    │  │  Run     │   │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                               │
│  • Auto-starts with Windows                  │
│  • Monitors & restarts agents                │
│  • Processes data automatically              │
│  • Zero manual intervention                  │
└──────────────────────────────────────────────┘
```

### Components

- **🤖 Orchestrator** - Manages everything autonomously
- **🔴 Logger** - Captures conversations in real-time
- **⚡ Compressor** - Delta compression (85% size reduction)
- **🧠 Curator** - Organizes into searchable SQLite database
- **🔍 Query Tools** - Token-efficient search for Claude integration

## 📂 Project Structure

```
AI-Librarian/
├── orchestrator/          # Autonomous management
│   ├── autonomous_librarian.py
│   ├── install_autonomous.bat
│   └── ...
├── logger/               # Conversation capture
│   ├── claude_desktop_logger.py
│   └── ...
├── compressor/           # Delta compression
│   ├── delta_compressor.py
│   └── ...
├── curator/              # Database & organization
│   ├── claude_curator.py
│   └── processed/
│       └── conversations.db
└── query_tools/          # Claude integration
    ├── librarian_query.py
    └── ...
```

## 🔧 Usage

### Autonomous Mode (Recommended)

Once installed, everything runs automatically. No manual work required!

**Monitor activity:**
```bash
type orchestrator\orchestrator.log
```

### Manual Mode

If you prefer manual control:

```bash
# Start logger
cd logger
start_logger.bat

# Process & compress
cd ..
process_all.bat

# Search
cd curator
python claude_curator.py search "topic"
```

### Search Examples

```bash
# Search conversations
python claude_curator.py search "machine learning" 10

# Get specific conversation
python claude_curator.py export claude_session_20251115_094309

# View statistics
python claude_curator.py stats
```

## 🔍 Claude Integration

The AI Librarian includes query tools that let Claude search your conversation history directly, saving 90% tokens vs built-in tools.

**Add to your Claude Project instructions:**

```
When user references past conversations, use:
cd C:\Projects\AI-Librarian\query_tools && python librarian_query.py search "term" 5

Benefits: 90% fewer tokens, 5x faster, complete history.
```

See `query_tools/COPY_TO_PROJECT.txt` for complete instructions.

## 💾 Storage

| Period | Raw Logs | Compressed | Savings |
|--------|----------|------------|---------|
| 1 Day | ~30 MB | ~5 MB | 85% |
| 1 Week | ~210 MB | ~35 MB | 85% |
| 1 Month | ~900 MB | ~150 MB | 85% |
| 1 Year | ~11 GB | ~2 GB | 85% |

## 🔐 Privacy

- ✅ Everything stays local on your machine
- ✅ No cloud uploads
- ✅ No external connections
- ✅ No telemetry
- ✅ You control all data

## 🛠️ Management

### Stop (Temporary)
```bash
orchestrator\stop_autonomous.bat
```

### Uninstall Auto-Start
```bash
orchestrator\uninstall_autonomous.bat
```
(Run as Administrator - your data stays safe)

### Manual Start (Debugging)
```bash
orchestrator\start_manual.bat
```

## 📖 Documentation

- [Complete Documentation](README.md)
- [Installation Guide](INSTALLATION.md)
- [Quick Start](QUICK_START.md)
- [Query Tools](query_tools/README.md)

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for Claude Desktop users who want to preserve their conversations
- Inspired by the need for better conversation management and search
- Made with ❤️ and too much coffee ☕

## 📊 Stats

- **4 autonomous agents** working together
- **85% compression** achieved through delta encoding
- **90% token savings** for Claude integration
- **Zero maintenance** required after setup
- **100% local** - your data never leaves your machine

## 🐛 Troubleshooting

### Logger not capturing
- Ensure Claude Desktop is running
- Check Windows UI Automation is enabled
- Try manual start: `logger\start_logger.bat`

### Database not updating
- Check orchestrator is running: Task Manager → `pythonw.exe`
- View logs: `orchestrator\orchestrator.log`
- Run curator manually: `curator\run_curator.bat`

### Search not working
- Ensure database exists: `curator\processed\conversations.db`
- Run curator to process logs
- Check database has data: `python curator\claude_curator.py stats`

## 🚀 Roadmap

- [ ] Web dashboard for browsing conversations
- [ ] Semantic search with embeddings
- [ ] Export to multiple formats (MD, PDF, etc.)
- [ ] Multi-user support
- [ ] Cloud sync option (optional)
- [ ] Mobile app for search
- [ ] Analytics and insights

## ⭐ Star This Repo!

If this project helped you, please consider giving it a star! It helps others discover this tool.

---

**Never lose a conversation again!** 🎉
