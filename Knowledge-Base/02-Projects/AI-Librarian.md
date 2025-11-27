# AI-Librarian Project

## Overview
**Status:** Rebuilding after reformat  
**Purpose:** Conversation capture and knowledge management system  
**Location:** C:\AI-Librarian

## Features
- Conversation history capture from Claude interactions
- Compression and storage (historically achieved 85% compression)
- Search and retrieval functionality
- Session management
- Token usage optimization

## Components
- **librarian_query.py:** Query interface for retrieving conversations
- **Database:** Stores conversation history
- **Knowledge-Base:** Structured documentation (this folder)

## Commands
- `aistats` - View statistics
- `ais 'keyword' [limit]` - Search conversations
- `python C:\AI-Librarian\librarian_query.py get <session_id>` - Get full conversation

## Setup Status
- [ ] Python environment configured
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Service/automation configured
- [ ] Backup system established

## Notes
- Previous system achieved 85% compression ratio
- Significant token savings through context management
- Needs autonomous operation capability
