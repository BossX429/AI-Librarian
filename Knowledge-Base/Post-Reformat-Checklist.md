# Post-Reformat Rebuild Checklist







**Reformat Date:** 2025-11-25  



**Created:** Today at 4:40 AM







## Phase 1: Core System Setup







### Essential Software



- [ ] Python 3.12 (C:\Program Files\Python312)



- [ ] Git



- [ ] Visual Studio Code



- [ ] AMD Adrenalin drivers (latest)



- [ ] Chrome/Edge browser







### Development Tools



- [ ] Node.js (if needed)



- [ ] Docker Desktop (if needed)



- [ ] Windows Terminal (enhanced)







## Phase 2: Python Environment







### Base Packages



```bash



pip install --upgrade pip



pip install pandas numpy matplotlib seaborn



pip install requests aiohttp



pip install torch torchvision  # AMD ROCm version



```







### AI/ML Tools



```bash



# Ollama for local models



# Download from https://ollama.ai







# Additional ML packages



pip install transformers



pip install accelerate



```







## Phase 3: Project Restoration







### AI-Librarian



- [ ] Create database structure



- [ ] Restore conversations (if backup exists)



- [ ] Install dependencies



- [ ] Configure automation/service



- [ ] Test search functionality







### Agent-Farm



- [ ] Restore code (if backup exists)



- [ ] Rebuild from documentation



- [ ] Test agent framework



- [ ] Implement evolution mechanics







### Hydra



- [ ] Determine latest version status



- [ ] Restore configuration



- [ ] Set up local model routing



- [ ] Configure API endpoints







## Phase 4: System Configuration







### PowerShell



```powershell



# Set execution policy



Set-ExecutionPolicy RemoteSigned -Scope CurrentUser







# Install useful modules



Install-Module -Name PSReadLine



Install-Module -Name posh-git



```







### Windows Services



- [ ] Review startup programs



- [ ] Configure necessary services



- [ ] Set up automated tasks







### File Associations



- [ ] .py files -> VS Code



- [ ] .md files -> VS Code



- [ ] Configure default apps







## Phase 5: Backup Strategy







### Critical Data



- [ ] Set up OneDrive/cloud backup



- [ ] Configure local backup solution



- [ ] Document backup locations



- [ ] Test restore procedures







### Backup Schedule



- **Daily:** Active project files



- **Weekly:** Full system state



- **Monthly:** Complete backup with verification







## Phase 6: System Optimization







### Performance Tuning



- [ ] Disable unnecessary startup programs



- [ ] Configure power plan (High Performance)



- [ ] Optimize virtual memory



- [ ] Configure AMD GPU settings







### Monitoring



- [ ] Set up resource monitoring



- [ ] Configure alerting (if needed)



- [ ] Document baseline performance







## Investigation Required







### Unicode Corruption



- Determine root cause



- Implement permanent fix



- Document prevention strategy







### Previous Reformat Cause



What triggered the need for this reformat?



Document to prevent future occurrences.







## Notes



Keep this checklist updated as you rebuild. Check off items as completed.



Add new sections as needed for your specific workflow.



