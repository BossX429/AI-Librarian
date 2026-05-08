# AI Librarian

**Autonomous conversation capture and search for Claude Desktop**

Never lose a conversation again. The AI Librarian automatically captures, compresses, and
indexes your Claude Desktop conversations into a searchable local database.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2011-blue)](https://www.microsoft.com/windows)

## Features

- Fully autonomous: runs 24/7 with optional manual control.
- Real-time capture: records Claude Desktop conversations.
- Delta compression for storage savings.
- Searchable local SQLite database.

## Quick Start

Prerequisites:
- Windows 11
- Python 3.12+
- Claude Desktop

Installation:

```bash
git clone https://github.com/BossX429/AI-Librarian.git
cd AI-Librarian
```

Autonomous mode (run as Administrator):

```bash
cd orchestrator
install_autonomous.bat
```

Manual mode examples:

```bash
cd logger
start_logger.bat

cd ..
process_all.bat

cd curator
python claude_curator.py search "your query"
```

## Usage

See the Knowledge-Base/README.md for detailed documentation and next steps.

## Development

This project targets Python 3.12. To run tests:

```bash
python -m pip install -r requirements.txt
python -m pip install -r logger/requirements.txt
pytest -q
```
