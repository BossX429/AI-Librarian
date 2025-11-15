# 🚀 AI Librarian - Quick Reference

## 📋 Quick Commands

### Start Logger
```bash
cd C:\Projects\AI-Librarian\logger
start_logger.bat
```
*Leave running while using Claude Desktop*

### Process Everything
```bash
cd C:\Projects\AI-Librarian
process_all.bat
```
*Compresses logs + updates database*

### Search Conversations
```bash
cd C:\Projects\AI-Librarian\curator
python claude_curator.py search "your query here"
```

### Export Conversation
```bash
python claude_curator.py export <session_id>
```

## 📊 File Locations

| What | Where |
|------|-------|
| Raw logs | `logger/raw_logs/*.jsonl` (10 MB) |
| Compressed | `compressor/compressed/*.jsonl` (1.5 MB) |
| Database | `curator/processed/conversations.db` ⭐ |
| Exports | `curator/processed/*.json` |

## ⚡ Performance

- **Compression:** 85% smaller (10 MB → 1.5 MB)
- **Processing:** 10x faster with compressed logs
- **Search:** Instant with database indexes
- **Storage:** ~1.5 MB per conversation session

## 🔄 Workflow

```
1. Logger captures ──→ raw_logs/ (10 MB)
2. Compressor shrinks ──→ compressed/ (1.5 MB)
3. Curator organizes ──→ database.db (searchable!)
4. You search/export ──→ Instant results!
```

## 💡 Pro Tips

- Run `process_all.bat` after each Claude session
- Delete raw logs after compression (save 85% space!)
- Search before asking Claude - you might have already discussed it!
- Export important conversations as backup

## 🎯 Most Common Tasks

**Task:** Find when I discussed X  
**Command:** `python claude_curator.py search "X"`

**Task:** Get full conversation  
**Command:** `python claude_curator.py export session_id`

**Task:** See all conversations  
**Command:** `python claude_curator.py` (shows summary)

**Task:** Free up space  
**Command:** Run `process_all.bat` then delete `logger/raw_logs/*.jsonl`

---

**Remember:** Logger must be running to capture conversations!
