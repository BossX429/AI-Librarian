import sqlite3
from datetime import datetime, timedelta
import os

# Database path - use environment variable or default
AI_LIBRARIAN_HOME = Path(os.getenv('AI_LIBRARIAN_HOME', r'C:\repos\AI-Librarian'))
db_path = AI_LIBRARIAN_HOME / "curator" / "processed" / "conversations.db"

# Sample data
def generate_sample_data():
    conversations = [
        {
            "session_id": "session_1",
            "start_time": (datetime.now() - timedelta(days=2)).isoformat(),
            "end_time": (datetime.now() - timedelta(days=2, hours=-1)).isoformat(),
            "message_count": 3,
            "messages": [
                {"message_number": 1, "role": "user", "content": "Hello, Claude!", "timestamp": (datetime.now() - timedelta(days=2, hours=1)).isoformat()},
                {"message_number": 2, "role": "assistant", "content": "Hi! How can I assist you today?", "timestamp": (datetime.now() - timedelta(days=2, hours=1, minutes=1)).isoformat()},
                {"message_number": 3, "role": "user", "content": "Can you summarize yesterday's meeting?", "timestamp": (datetime.now() - timedelta(days=2, hours=1, minutes=2)).isoformat()}
            ]
        },
        {
            "session_id": "session_2",
            "start_time": (datetime.now() - timedelta(days=1)).isoformat(),
            "end_time": (datetime.now() - timedelta(days=1, hours=-1)).isoformat(),
            "message_count": 2,
            "messages": [
                {"message_number": 1, "role": "user", "content": "What is the weather today?", "timestamp": (datetime.now() - timedelta(days=1, hours=1)).isoformat()},
                {"message_number": 2, "role": "assistant", "content": "The weather is sunny with a high of 25degC.", "timestamp": (datetime.now() - timedelta(days=1, hours=1, minutes=1)).isoformat()}
            ]
        }
    ]
    return conversations

# Populate database
def populate_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            start_time TEXT,
            end_time TEXT,
            message_count INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            message_number INTEGER,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')

    # Insert sample data
    conversations = generate_sample_data()
    for conv in conversations:
        cursor.execute(
            'INSERT OR IGNORE INTO conversations (session_id, start_time, end_time, message_count) VALUES (?, ?, ?, ?)',
            (conv["session_id"], conv["start_time"], conv["end_time"], conv["message_count"])
        )
        conversation_id = cursor.lastrowid

        for msg in conv["messages"]:
            cursor.execute(
                'INSERT INTO messages (conversation_id, message_number, role, content, timestamp) VALUES (?, ?, ?, ?, ?)',
                (conversation_id, msg["message_number"], msg["role"], msg["content"], msg["timestamp"])
            )

    conn.commit()
    conn.close()
    print("Sample data populated successfully.")

if __name__ == "__main__":
    populate_database()