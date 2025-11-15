#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Librarian Query Tools
Fast, token-efficient tools for Claude to search conversation history.

These tools allow Claude to query the local database directly instead of
using expensive cloud-based memory/search tools.
"""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class LibrarianQuery:
    """Query the AI Librarian database efficiently."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.db_path = self.project_root / "curator" / "processed" / "conversations.db"
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
    
    def search(self, query: str, limit: int = 5, context_chars: int = 300):
        """
        Search conversations for a query string.
        Returns compact results optimized for token efficiency.
        
        Args:
            query: Search term
            limit: Max results (default: 5)
            context_chars: Characters of context around match (default: 300)
        """
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
        conn.close()
        
        if not results:
            return {
                'found': 0,
                'query': query,
                'results': []
            }
        
        # Format results compactly
        formatted_results = []
        for session_id, start_time, role, content, timestamp in results:
            # Find query position for context
            query_pos = content.lower().find(query.lower())
            if query_pos != -1:
                # Extract context around the match
                start = max(0, query_pos - context_chars // 2)
                end = min(len(content), query_pos + len(query) + context_chars // 2)
                snippet = content[start:end]
                
                # Add ellipsis if truncated
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
            else:
                # Fallback to start of content
                snippet = content[:context_chars] + "..."
            
            formatted_results.append({
                'session_id': session_id,
                'timestamp': timestamp,
                'role': role,
                'snippet': snippet
            })
        
        return {
            'found': len(results),
            'query': query,
            'results': formatted_results
        }
    
    def get_conversation(self, session_id: str, max_messages: int = 20):
        """
        Retrieve a specific conversation by session ID.
        Returns compact message list.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get conversation info
        cursor.execute('SELECT * FROM conversations WHERE session_id = ?', (session_id,))
        conv = cursor.fetchone()
        
        if not conv:
            conn.close()
            return {
                'found': False,
                'session_id': session_id
            }
        
        # Get messages (limited)
        cursor.execute('''
            SELECT message_number, role, content, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY message_number
            LIMIT ?
        ''', (conv[0], max_messages))
        
        messages = []
        for msg_num, role, content, timestamp in cursor.fetchall():
            # Truncate very long messages
            if len(content) > 500:
                content = content[:500] + f"... [{len(content)-500} more chars]"
            
            messages.append({
                'num': msg_num,
                'role': role,
                'content': content,
                'time': timestamp
            })
        
        conn.close()
        
        return {
            'found': True,
            'session_id': conv[1],
            'start_time': conv[2],
            'end_time': conv[3],
            'total_messages': conv[4],
            'messages_shown': len(messages),
            'messages': messages
        }
    
    def get_stats(self):
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_convs = cursor.fetchone()[0]
        
        # Total messages
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_msgs = cursor.fetchone()[0]
        
        # Messages by role
        cursor.execute('SELECT role, COUNT(*) FROM messages GROUP BY role')
        by_role = dict(cursor.fetchall())
        
        # Recent conversations (last 10)
        cursor.execute('''
            SELECT session_id, start_time, message_count
            FROM conversations
            ORDER BY start_time DESC
            LIMIT 10
        ''')
        recent = [
            {'session': row[0], 'time': row[1], 'messages': row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'total_conversations': total_convs,
            'total_messages': total_msgs,
            'by_role': by_role,
            'recent_conversations': recent
        }
    
    def search_by_date(self, after_date: str = None, before_date: str = None, limit: int = 10):
        """
        Search conversations by date range.
        
        Args:
            after_date: ISO format datetime (e.g., "2025-11-01")
            before_date: ISO format datetime
            limit: Max conversations to return
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT session_id, start_time, end_time, message_count FROM conversations WHERE 1=1'
        params = []
        
        if after_date:
            query += ' AND start_time >= ?'
            params.append(after_date)
        
        if before_date:
            query += ' AND start_time <= ?'
            params.append(before_date)
        
        query += ' ORDER BY start_time DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        results = [
            {
                'session_id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'message_count': row[3]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'found': len(results),
            'after_date': after_date,
            'before_date': before_date,
            'conversations': results
        }


def main():
    """CLI interface for query tools."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python query_tools.py search <query> [limit]")
        print("  python query_tools.py get <session_id>")
        print("  python query_tools.py stats")
        print("  python query_tools.py date [--after YYYY-MM-DD] [--before YYYY-MM-DD]")
        return
    
    try:
        librarian = LibrarianQuery()
        command = sys.argv[1]
        
        if command == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            result = librarian.search(query, limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == "get":
            session_id = sys.argv[2] if len(sys.argv) > 2 else ""
            result = librarian.get_conversation(session_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == "stats":
            result = librarian.get_stats()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == "date":
            after = None
            before = None
            limit = 10
            
            for i, arg in enumerate(sys.argv[2:], 2):
                if arg == "--after" and i + 1 < len(sys.argv):
                    after = sys.argv[i + 1]
                elif arg == "--before" and i + 1 < len(sys.argv):
                    before = sys.argv[i + 1]
                elif arg == "--limit" and i + 1 < len(sys.argv):
                    limit = int(sys.argv[i + 1])
            
            result = librarian.search_by_date(after, before, limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            print(f"Unknown command: {command}")
    
    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
