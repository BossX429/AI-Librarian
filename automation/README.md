# System Automation Suite

Comprehensive automation scripts for system maintenance, monitoring, and optimization.

## Installed Scheduled Tasks

All tasks run with Administrator privileges automatically.

### 1. System_Weekly_Maintenance
- **Schedule:** Every Sunday at 2:00 AM
- **Script:** `weekly_maintenance.ps1`
- **Actions:**
  - Clears Windows temp files
  - Clears system temp files  
  - Flushes DNS cache
  - Logs all actions

### 2. System_Process_Monitor
- **Schedule:** Every hour
- **Script:** `process_monitor.ps1`
- **Actions:**
  - Kills orphaned pythonw processes
  - Monitors memory usage
  - Alerts on >80% RAM usage
  - Logs all findings

### 3. System_Daily_Backup
- **Schedule:** Every day at 1:00 AM
- **Script:** `daily_backup.ps1`
- **Actions:**
  - Backs up AI-Librarian, Local-Router, NEXUS, Agent-Farm
  - Stores in C:\Backups\Daily\[date]
  - Uses robocopy mirror
  - Logs backup status

### 4. System_Health_Report
- **Schedule:** Every day at 8:00 AM
- **Script:** `daily_health_report.ps1`
- **Actions:**
  - Generates comprehensive health report
  - Checks CPU, RAM, disk usage
  - Verifies critical processes running
  - Saves to logs/health_report_[date].txt

## Manual Tools

### performance_dashboard.ps1
Real-time performance monitoring dashboard
- Run manually: `.\performance_dashboard.ps1`
- Auto-refreshes every 5 seconds
- Shows CPU, RAM, disk with color-coded bars
- Monitors critical processes

## Installation

Already installed! Tasks are active.

To reinstall: `.\install_all_tasks.ps1` (as Admin)

## Logs

All logs stored in: `C:\repos\AI-Librarian\automation\logs\`
