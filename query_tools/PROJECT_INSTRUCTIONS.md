# CLAUDE PROJECT INSTRUCTIONS




# Add these to your "Hydra Ver-1.0" project custom instructions









## AI Librarian Integration









You have access to a local AI Librarian system that captures and indexes ALL your conversations with Claude. This is MUCH more efficient than using the built-in `conversation_search` or `recent_chats` tools.









### When to Use AI Librarian vs Built-in Tools









**ALWAYS prefer AI Librarian tools when:**




- User asks "what did we discuss about X?"




- User references past conversations




- You need context from previous chats




- User asks "remember when we..."




- You need to find specific code/solutions from past sessions




- User wants to know conversation history









**AI Librarian is:**




-  Instant (local database query)




-  Zero token overhead (no big conversation dumps)




-  Complete history (ALL conversations ever)




-  More accurate (structured database)









**Built-in tools are:**




-  Slower (cloud API calls)




-  Expensive (large token usage)




-  Limited (recent conversations only)




-  Less reliable (semantic search limitations)









### Available AI Librarian Commands









Use Desktop Commander to run these Python scripts:









#### 1. Search Conversations




```python




cd C:\Projects\AI-Librarian\query_tools




python librarian_query.py search "your search term" [limit]




```









**Returns:** JSON with matching messages, timestamps, snippets




**Use when:** User asks about past topics, code, discussions









**Example:**




- User: "What did we discuss about Hydra?"




- Claude: Uses Desktop Commander to run search query




- Result: Instant JSON with relevant conversation snippets









#### 2. Get Specific Conversation




```python




python librarian_query.py get <session_id>




```









**Returns:** Full conversation (up to 20 messages)




**Use when:** Need complete context from a specific session









#### 3. Get Statistics




```python




python librarian_query.py stats




```









**Returns:** Total conversations, message counts, recent sessions




**Use when:** User asks "how many conversations have we had?"









#### 4. Search by Date




```python




python librarian_query.py date --after 2025-11-01 --before 2025-11-15




```









**Returns:** Conversations within date range




**Use when:** User asks about conversations from specific time period









### Workflow Example









**User asks:** "What did we discuss about the Logger yesterday?"









**CORRECT approach (AI Librarian):**




1. Use Desktop Commander: `python librarian_query.py search "Logger" 5`




2. Get instant JSON results with snippets




3. Respond naturally: "Yesterday we discussed the Logger capturing Claude Desktop conversations..."









**WRONG approach (built-in tools):**




1. Call `conversation_search("Logger")` 




2. Wait for cloud API




3. Get limited results




4. Waste tokens on conversation dumps









### Integration Best Practices









1. **Check database first:** Before using built-in tools, try AI Librarian




2. **Be specific:** Use targeted search terms for better results




3. **Limit results:** Default to 5 results, increase if needed




4. **Natural responses:** Don't expose the mechanics to user




5. **Combine if needed:** Can use both if AI Librarian insufficient









### When Built-in Tools Are Still Needed









**Use `conversation_search` / `recent_chats` ONLY when:**




- AI Librarian database doesn't exist yet




- Query is about conversations NOT yet processed




- Need very recent chat (< 5 minutes ago)




- AI Librarian query fails/errors









### Output Format









AI Librarian returns compact JSON:




```json




{




  "found": 3,




  "query": "Logger",




  "results": [




    {




      "session_id": "claude_session_20251115_094309",




      "timestamp": "2025-11-15T09:43:10",




      "role": "assistant",




      "snippet": "...Perfect! Let's build the Logger Agent..."




    }




  ]




}




```









### Token Savings









**Example comparison:**









| Method | Token Usage | Speed | Accuracy |




|--------|-------------|-------|----------|




| Built-in `conversation_search` | ~5,000 tokens | 3-5 sec | 70% |




| AI Librarian query | ~500 tokens | <1 sec | 95% |




| **Savings** | **90% fewer tokens!** | **5x faster!** | **Better!** |









### Example Conversation









```




User: "Can you remind me what we decided about compression?"









Claude: [Internally thinks: This is a past conversation query, use AI Librarian]









[Runs Desktop Commander command:]




cd C:\Projects\AI-Librarian\query_tools && python librarian_query.py search "compression" 3









[Gets results instantly:]




{




  "found": 3,




  "results": [...]




}









[Responds naturally:]




"We discussed using delta compression for the AI Librarian! We decided to compress logs every 5 minutes, achieving 85% size reduction (from 10 MB to 1.5 MB per session). The compressor only stores changes between captures rather than full dumps, which dramatically reduces storage and speeds up processing by 10-100x."




```









### Database Location









**Path:** `C:\Projects\AI-Librarian\curator\processed\conversations.db`









This SQLite database contains:




- ALL conversations (complete history)




- Structured messages (user/assistant)




- Timestamps and metadata




- Full-text search indexes









### Autonomous Updates









The database auto-updates every 5 minutes via the Orchestrator, so it's always current!









---









## Summary









**TL;DR:** When user references past conversations, use AI Librarian query tools via Desktop Commander instead of built-in tools. It's faster, cheaper, more accurate, and has complete history.









**Default workflow:**




1. User mentions past conversation




2. Use Desktop Commander to query AI Librarian




3. Get instant JSON results




4. Respond naturally with context




5. Save 90% tokens!




