#  AI Librarian - Installation Guide









##  Autonomous Mode (Recommended - 30 Seconds Setup!)









**This is the "set it and forget it" mode. Do this once and never think about it again.**









### Step 1: Install (ONE TIME ONLY)









1. Open Windows Explorer




2. Navigate to: `C:\Projects\AI-Librarian\orchestrator\`




3. **Right-click** `install_autonomous.bat`




4. Select **"Run as Administrator"**




5. Wait 10 seconds




6. Done!









### What Just Happened?









The installer just:




-  Created a Windows Task Scheduler task




-  Set it to auto-start on every Windows login




-  Started the AI Librarian in background RIGHT NOW




-  Configured 24/7 autonomous operation









### What Happens Now? (Forever!)









**Automatically, with ZERO work from you:**









1. **Every second:** Captures Claude conversations




2. **Every 5 minutes:** Compresses logs (85% smaller!)




3. **After compression:** Updates searchable database




4. **On crashes:** Restarts itself automatically




5. **On Windows login:** Starts automatically




6. **Forever:** Runs silently in background









### Verify It's Working









**Check Task Manager:**




- Press `Ctrl+Shift+Esc`




- Look for process: `pythonw.exe`




- Command line contains: `autonomous_librarian.py`









**Check the Log:**




```




C:\Projects\AI-Librarian\orchestrator\orchestrator.log




```









Should show:




```




[2025-11-15 10:07:11]  Autonomous AI Librarian Starting...




[2025-11-15 10:07:11]  Starting Logger Agent...




[2025-11-15 10:07:11]  Logger started (PID: 19756)




[2025-11-15 10:07:11]  Autonomous mode active - running 24/7




```









---









##  Using Your AI Librarian









### Search Anytime









```bash




cd C:\Projects\AI-Librarian\curator




python claude_curator.py search "your topic"




```









### Export Conversation









```bash




python claude_curator.py export <session_id>




```









### View Statistics









```bash




python claude_curator.py




```









---









##  Management









### Stop (Temporarily)









Double-click: `orchestrator\stop_autonomous.bat`









**Note:** Will restart on next Windows login unless you uninstall.









### Uninstall Auto-Start









**Right-click** `orchestrator\uninstall_autonomous.bat` → **Run as Administrator**









**Note:** Your data remains safe! This only stops the automation.









### Manual Mode (For Debugging)









Double-click: `orchestrator\start_manual.bat`









Shows console output so you can see what's happening.









---









##  What You Get









### After 1 Day of Use:




-  10-20 conversations captured




-  ~30 MB raw logs → ~5 MB compressed (85% savings!)




-  Fully searchable database




-  Zero manual work









### After 1 Month of Use:




-  300-600 conversations captured




-  ~1 GB raw logs → ~150 MB compressed




-  Complete conversation history




-  Still zero manual work!









### After 1 Year of Use:




-  3,000+ conversations captured




-  ~12 GB raw logs → ~2 GB compressed




-  Entire year of knowledge preserved




-  **You did absolutely nothing!**









---









##  Troubleshooting









### "I installed it, is it working?"









**Yes if:**




-  `pythonw.exe` in Task Manager




-  `orchestrator.log` has recent entries




-  New files appear in `logger\raw_logs\`




-  Database updates in `curator\processed\conversations.db`









### "Nothing seems to be happening"









**Try this:**




1. Double-click `orchestrator\start_manual.bat`




2. Watch console output for errors




3. Check if Claude Desktop is running




4. Verify Windows UI Automation is enabled









### "Want to see it working"









**Real-time monitoring:**




1. Open `orchestrator\orchestrator.log` in Notepad




2. Keep refreshing to see new entries




3. Watch `logger\raw_logs\` folder for new files




4. Check Task Manager → pythonw.exe → CPU usage (should be low)









### "How do I know it's capturing?"









**Open Claude Desktop and have a conversation, then:**




1. Wait 1 minute




2. Check `logger\raw_logs\` for new `.jsonl` file




3. File size should be growing




4. `orchestrator.log` will show compression activity after 5 minutes









---









##  Pro Tips









### Tip 1: First Time Setup




Run `start_manual.bat` first time to watch it work, then install autonomous mode.









### Tip 2: Monitor Performance




Check `orchestrator.log` once a week to see stats:




```




[2025-11-15 14:30:00]  Status: Logger=True, Raw=1, Compressed=3, Last compression=14:25:00




```









### Tip 3: Save Space




After autonomous mode runs for a week, raw logs in `logger\raw_logs\` can be deleted (they're already compressed in `compressor\compressed\`). Saves 85% disk space!









### Tip 4: Backup Your Database




Periodically copy:




```




curator\processed\conversations.db




```




to a backup location. This is your entire conversation history!









### Tip 5: Search Often




Get in the habit of searching your past conversations:




```bash




python curator\claude_curator.py search "that thing we discussed"




```









You'll be amazed how often you need to reference past conversations!









---









##  Privacy & Security









**Everything stays LOCAL:**




-  Nothing sent to cloud




-  No external connections (except Claude Desktop itself)




-  No telemetry or tracking




-  All data on YOUR machine only




-  You control everything









**Data Location:**




- Raw logs: `C:\Projects\AI-Librarian\logger\raw_logs\`




- Compressed: `C:\Projects\AI-Librarian\compressor\compressed\`




- Database: `C:\Projects\AI-Librarian\curator\processed\conversations.db`









**To completely remove all data:**




Delete the `C:\Projects\AI-Librarian` folder.









---









##  Summary









**What you just installed:**




-  Autonomous orchestrator (manages everything)




-  Logger agent (captures conversations)




-  Compressor agent (reduces file sizes 85%)




-  Curator agent (organizes into database)









**What happens automatically:**




- ⏰ Starts with Windows




-  Runs forever in background




-  Captures all conversations




-  Compresses every 5 minutes




-  Updates database automatically




-  Restarts if crashes




-  Logs all activity









**What you need to do:**




- **Nothing!**




- (Optional) Search your conversations anytime









---









**You're all set! The AI Librarian is now working 24/7 in the background.** 









**Never lose a conversation again!** 




