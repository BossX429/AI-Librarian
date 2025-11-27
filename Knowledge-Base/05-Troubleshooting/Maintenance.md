# System Maintenance

## Regular Tasks

### Daily
- [ ] Check system resources (CPU, RAM, disk)
- [ ] Monitor running processes
- [ ] Check for service failures

### Weekly
- [ ] Windows Update check
- [ ] AMD driver check
- [ ] Disk cleanup
- [ ] Backup verification

### Monthly
- [ ] Full system backup
- [ ] Disk defragmentation (if HDD)
- [ ] Driver updates review
- [ ] Performance benchmarking

## Automated Checks

### PowerShell Health Check Script
```powershell
# System health check
Write-Host "=== System Health Check ===" -ForegroundColor Cyan

# CPU usage
$cpu = Get-Counter '\Processor(_Total)\% Processor Time' | 
       Select-Object -ExpandProperty CounterSamples | 
       Select-Object -ExpandProperty CookedValue
Write-Host "CPU Usage: $([math]::Round($cpu, 2))%"

# Memory usage
$mem = Get-CimInstance Win32_OperatingSystem
$usedMem = $mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory
$memPercent = ($usedMem / $mem.TotalVisibleMemorySize) * 100
Write-Host "Memory Usage: $([math]::Round($memPercent, 2))%"
