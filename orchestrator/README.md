#  Autonomous AI Librarian









**Fully Automatic, Zero-Maintenance Conversation Capture**









The Orchestrator runs everything automatically in the background. Once installed, it requires ZERO manual intervention - ever.









##  What It Does









The Autonomous Librarian:




1. **Auto-starts** with Windows (on login)




2. **Runs 24/7** silently in background




3. **Captures** all Claude conversations automatically




4. **Compresses** logs every 5 minutes (85% size reduction)




5. **Updates** database automatically




6. **Monitors** and restarts itself if needed









**You literally never have to think about it.**









##  Quick Setup









### Install (One Time Only)









**Right-click** `install_autonomous.bat` → **Run as Administrator**









That's it! The AI Librarian is now:




-  Running in background




-  Set to auto-start on every Windows login




-  Capturing all conversations




-  Compressing and organizing automatically









##  Management









### Stop (Temporary)




```




stop_autonomous.bat




```




Stops the background process. Will restart on next login.









### Uninstall (Remove Auto-Start)




```




uninstall_autonomous.bat (Run as Administrator)




```




Removes auto-start. Your data is safe, just stops the automation.









### Manual Start (For Monitoring)




```




start_manual.bat




```




Starts with visible console so you can see what's happening.









##  How It Works









```









         Autonomous Orchestrator                      




                                                       




                




    Logger  → Compressor→  Curator  → Database




    24/7      Every 5min  Auto-run    Updated 




                




                                                       




  • Monitors all agents                               




  • Restarts if crashed                               




  • Processes new data automatically                  




  • Logs everything to orchestrator.log               









```









### The Cycle (Runs Forever)









**Every 30 seconds:**




1. Check if Logger is still running (restart if needed)




2. Check for new log files




3. Every 5 minutes: Compress any new logs




4. After compression: Update database




5. Log status every 10 minutes









##  Files Created









| File | Purpose |




|------|---------|




| `autonomous_librarian.py` | Main orchestrator |




| `orchestrator.log` | Activity log |




| `install_autonomous.bat` | One-time setup |




| `start_background.bat` | Silent start |




| `start_manual.bat` | Visible start |




| `stop_autonomous.bat` | Stop process |




| `uninstall_autonomous.bat` | Remove auto-start |









##  Auto-Start Mechanism









The installer creates:









1. **Windows Task Scheduler Task**




   - Name: `AI_Librarian_Autonomous`




   - Trigger: On user login




   - Runs with highest privileges




   - Hidden window









2. **Startup Folder Shortcut**




   - Location: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`




   - Backup method if Task Scheduler fails









**Result:** Starts automatically on every Windows login, runs forever.









##  Monitoring









### Check If Running









**Task Manager:**




- Look for `pythonw.exe` process




- Command line contains `autonomous_librarian.py`









**Log File:**




```




C:\Projects\AI-Librarian\orchestrator\orchestrator.log




```




Shows all activity with timestamps.









### Status Updates









The orchestrator logs status every ~10 minutes:




```




[2025-11-15 14:30:00]  Status: Logger=True, Raw=1, Compressed=3, Last compression=14:25:00




```









##  Configuration









Edit `autonomous_librarian.py` to customize:









```python




# How often to check for new data




self.check_interval = 30  # seconds









# How often to compress logs




self.compression_interval = 300  # 5 minutes









# How old files must be before processing




self.min_file_age = 60  # 1 minute




```









##  Searching









Even while running autonomously, you can search anytime:









```bash




cd C:\Projects\AI-Librarian\curator




python claude_curator.py search "your query"




```









The database is always up-to-date!









##  Safety & Reliability









### Health Monitoring




- Checks Logger every 30 seconds




- Auto-restarts if crashed




- Logs all errors









### Crash Recovery




- If orchestrator crashes, it restarts on next login




- All data is safe (already on disk)




- Database commits are atomic









### Resource Usage




- **CPU:** <1% (mostly idle)




- **RAM:** ~50 MB




- **Disk:** Minimal writes (only on changes)









##  Troubleshooting









### "Nothing happening after install"




- Check Task Manager for `pythonw.exe`




- Check `orchestrator.log` for errors




- Try `start_manual.bat` to see console output









### "Logger not capturing"




- Ensure Claude Desktop is running




- Check Logger works manually first




- Verify Windows UI Automation is enabled









### "Auto-start not working"




- Run `install_autonomous.bat` as Administrator




- Check Task Scheduler has the task




- Try logging out and back in









### "Want to see what it's doing"




- Run `start_manual.bat` for visible console




- Watch `orchestrator.log` file




- Check Curator database for updates









##  Pro Tips









1. **First Run:** Use `start_manual.bat` first to verify everything works




2. **Monitoring:** Keep `orchestrator.log` open in a text editor to watch activity




3. **Space Saving:** Old raw logs can be deleted after compression (auto-compression keeps them)




4. **Testing:** Stop autonomous mode, make changes, test, then restart




5. **Backup:** Periodically backup `curator/processed/conversations.db`









##  Future Enhancements









Planned features:




- [ ] System tray icon with status




- [ ] Web dashboard for monitoring




- [ ] Email/notifications on errors




- [ ] Cloud backup integration




- [ ] Resource usage optimization




- [ ] Smart compression timing




- [ ] Multiple user support









##  Technical Details









### Process Architecture









```




pythonw.exe (orchestrator)




    ↓




    → python.exe (logger subprocess)




```









The orchestrator runs as `pythonw.exe` (no console window).




It spawns the Logger as a subprocess and monitors it.









### Startup Flow









1. Windows login triggers Task Scheduler




2. Task runs `start_background.bat`




3. Batch file starts `autonomous_librarian.py` with `pythonw.exe`




4. Orchestrator starts Logger subprocess




5. Main loop begins (runs forever)









### Graceful Shutdown









On system shutdown:




1. Windows sends termination signal




2. Orchestrator catches signal




3. Stops Logger subprocess cleanly




4. Saves state and exits









On next boot: Everything restarts automatically!









---









**Status:** Fully autonomous, zero maintenance required! 









**Set it and forget it!**




