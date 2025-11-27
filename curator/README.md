#  Claude Desktop Curator









**The Brain of the AI Librarian System**









The Curator Agent processes raw conversation logs from the Logger and transforms them into organized, searchable knowledge.









##  What It Does









The Curator is responsible for:









1. ** Parsing** - Reads raw JSONL files from the Logger




2. ** Filtering** - Removes UI noise and extracts actual conversation content




3. ** Detection** - Identifies message boundaries and roles (user vs assistant)




4. ** Storage** - Saves conversations in a SQLite database for fast querying




5. ** Indexing** - Creates searchable indexes for finding specific content




6. ** Export** - Converts conversations to JSON format for analysis









##  Architecture









```




Input:  logger/raw_logs/*.jsonl (raw UI captures)




           ↓




Process: Extract + Filter + Organize




           ↓




Output: processed/conversations.db (structured database)




```









### Database Schema









**Conversations Table:**




- `id` - Unique conversation identifier




- `session_id` - Session ID from Logger




- `start_time` - When conversation started




- `end_time` - When conversation ended




- `message_count` - Number of messages




- `total_chars` - Total character count









**Messages Table:**




- `id` - Unique message identifier




- `conversation_id` - Links to conversation




- `message_number` - Sequential number in conversation




- `role` - "user" or "assistant"




- `content` - The actual message text




- `timestamp` - When message was captured




- `content_hash` - Hash for duplicate detection




- `tokens_estimate` - Estimated token count









##  Usage









### Process All Logs









```bash




python claude_curator.py




```









This will:




- Find all `.jsonl` files in `../logger/raw_logs/`




- Extract and organize conversations




- Store in `processed/conversations.db`




- Display a summary









### Search Conversations









```bash




python claude_curator.py search "your query here"




```









Example:




```bash




python claude_curator.py search "AI Librarian"




python claude_curator.py search "Hydra"




python claude_curator.py search "logger"




```









### Export Conversation









```bash




python claude_curator.py export <session_id>




```









Example:




```bash




python claude_curator.py export claude_session_20251115_094309




```









This creates a JSON file in `processed/` with the full conversation.









##  How It Works









### 1. Parsing Raw Logs









The Curator reads JSONL files line by line:









```python




# Each line is a JSON object




{




  "session_id": "claude_session_20251115_094309",




  "timestamp": "2025-11-15T09:43:10.249054",




  "message_number": 0,




  "raw_text": "...",  # Everything visible in Claude Desktop




  "text_hash": "887b...",




  "capture_method": "windows_ui_automation"




}




```









### 2. Filtering UI Noise









The Curator identifies and removes UI elements:




- Sidebar navigation




- Button labels




- System messages




- Window chrome




- Empty captures









**Filters out:**




- "New chat", "Chats", "Projects"




- "Minimize", "Restore", "Close"




- "Claude can make mistakes"




- "How can I help you today?"




- And many more...









### 3. Detecting Message Roles









Smart heuristics determine if a message is from user or assistant:









**Assistant indicators:**




- Contains code blocks (\`\`\`)




- Has tool call output




- Long messages (>500 chars)




- Contains emojis like   









**User indicators:**




- Short messages (<200 chars)




- Simple questions




- Commands/requests









### 4. Storing in Database









SQLite provides:




-  **Fast queries** - Indexed for speed




-  **Full-text search** - Find anything instantly




-  **Analytics** - Count messages, chars, tokens




-  **Relationships** - Link messages to conversations




-  **Portable** - Single file database









### 5. Deduplication









The Curator tracks content hashes to avoid storing duplicate captures:




- Same content hash = already processed, skip it




- New content hash = new message, store it









##  Output Examples









### Summary Output









```




==============================================================




 CURATOR SUMMARY




==============================================================




 Conversations: 1




 Messages: 15




 Total Characters: 287,132




 Database: C:\Projects\AI-Librarian\curator\processed\conversations.db




==============================================================




```









### Search Results









```




 Found 3 results for 'logger'









 2025-11-15T09:43:10.249054




 ASSISTANT




 Perfect! Let's build the Logger Agent - the first part of your AI Librarian system...




------------------------------------------------------------




```









### Exported JSON









```json




{




  "session_id": "claude_session_20251115_094309",




  "start_time": "2025-11-15T09:43:10.249054",




  "end_time": "2025-11-15T09:45:49.170139",




  "message_count": 15,




  "total_chars": 287132,




  "messages": [




    {




      "message_number": 0,




      "role": "user",




      "content": "Let's build the logger!",




      "timestamp": "2025-11-15T09:43:10.249054",




      "tokens_estimate": 6




    },




    {




      "message_number": 1,




      "role": "assistant",




      "content": "Perfect! Let's build the Logger Agent...",




      "timestamp": "2025-11-15T09:43:15.123456",




      "tokens_estimate": 1500




    }




  ]




}




```









##  Future Enhancements









- [ ] Machine learning for better role detection




- [ ] Conversation topic classification




- [ ] Sentiment analysis




- [ ] Automatic summarization




- [ ] Export to Markdown




- [ ] Vector embeddings for semantic search




- [ ] Knowledge graph generation




- [ ] Timeline visualization




- [ ] Statistics dashboard









##  Configuration









All configuration is in the Python script:









```python




# UI noise patterns to filter




ui_noise_patterns = [




    r'^(New chat|Chats|Projects|Artifacts|Code|Starred)',




    r'^(Chrome Legacy Window|Minimize|Restore|Close)',




    # ... add more patterns as needed




]









# Token estimation (adjust as needed)




def estimate_tokens(text):




    return len(text) // 4  # Rough: 1 token ≈ 4 chars




```









##  Notes









- **No external dependencies** - Uses only Python standard library




- **Fast processing** - SQLite handles millions of messages




- **Incremental** - Only processes new log files




- **Safe** - Read-only on Logger files, writes to separate DB




- **Portable** - Database is a single file you can backup/move









##  Integration with Logger









The Curator works seamlessly with the Logger:









1. **Logger** runs continuously, capturing UI → `raw_logs/*.jsonl`




2. **Curator** processes periodically → `processed/conversations.db`




3. You can query/search/export anytime!









Run them together:




- Keep Logger running in one terminal




- Run Curator periodically (manually or via scheduler)




- Search/export as needed









##  Tips









- Run Curator after each conversation session for latest data




- Use search to find specific topics across all conversations




- Export conversations for external analysis or backup




- Check database size periodically (`conversations.db`)









---









**Built with  as part of the AI Librarian Project**




