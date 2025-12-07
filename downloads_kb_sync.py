#!/usr/bin/env python3
"""Downloads → Knowledge-Base Auto-Sync"""
import os
from pathlib import Path
from datetime import datetime

DOWNLOADS = Path(r"C:\Users\kyleh\Downloads")
KNOWLEDGE_BASE = Path(r"C:\repos\AI-Librarian\Knowledge-Base")
SYNC_FILE = KNOWLEDGE_BASE / "downloads_inventory.md"

def get_category(file_path):
    ext = file_path.suffix.lower()
    cats = {
        'Installers': ['.exe', '.msi'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.cpp', '.c', '.h', '.java'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.md'],
        'Data': ['.json', '.xml', '.csv', '.yaml', '.yml']
    }
    for category, extensions in cats.items():
        if ext in extensions:
            return category
    return 'Other'

print("Syncing Downloads to Knowledge-Base...")

# Scan Downloads
total_files = 0
total_size = 0
all_files = []
categories = {}

for item in DOWNLOADS.rglob("*"):
    if item.is_file() and item.name != 'desktop.ini':
        try:
            size_mb = item.stat().st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(item.stat().st_mtime)
            
            file_info = {
                'name': item.name,
                'path': str(item.relative_to(DOWNLOADS)),
                'size_mb': round(size_mb, 2),
                'modified': modified.isoformat(),
                'category': get_category(item)
            }
            
            all_files.append(file_info)
            total_size += size_mb
            total_files += 1
            
            cat = file_info['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(file_info)
        except:
            pass

# Recent files
now = datetime.now()
recent = []
for f in all_files:
    file_time = datetime.fromisoformat(f['modified'])
    hours_old = (now - file_time).total_seconds() / 3600
    if hours_old < 24:
        recent.append({**f, 'hours_ago': round(hours_old, 1)})

# Generate markdown
md = f"""# Downloads Folder Inventory

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Auto-synced from:** `C:\\Users\\kyleh\\Downloads`

## Overview

- **Total Files:** {total_files}
- **Total Size:** {round(total_size, 2)} MB

## Recent Additions (Last 24 Hours)

"""

if recent:
    for item in sorted(recent, key=lambda x: x['hours_ago'])[:10]:
        md += f"- **{item['name']}** ({item['size_mb']:.2f} MB) - {item['hours_ago']:.1f}h ago\n"
else:
    md += "*No recent additions*\n"

md += "\n## Files by Category\n\n"

for category in sorted(categories.keys()):
    files = categories[category]
    cat_size = sum(f['size_mb'] for f in files)
    md += f"### {category} ({len(files)} files, {cat_size:.2f} MB)\n\n"
    
    for file_info in sorted(files, key=lambda x: x['modified'], reverse=True)[:15]:
        md += f"- **{file_info['name']}** ({file_info['size_mb']:.2f} MB)\n"

# Write to Knowledge-Base
KNOWLEDGE_BASE.mkdir(exist_ok=True)
with open(SYNC_FILE, 'w', encoding='utf-8') as f:
    f.write(md)

print(f"✓ Synced {total_files} files to Knowledge-Base")
