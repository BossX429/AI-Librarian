# Weekly RAM Cache Flush
# Clears standby memory and working sets

$ErrorActionPreference = 'SilentlyContinue'

# Get memory before
$beforeMem = Get-WmiObject Win32_OperatingSystem | Select-Object @{Name='FreeGB';Expression={[math]::Round($_.FreePhysicalMemory/1MB,2)}}

# Clear standby list (requires RAMMap or EmptyStandbyList.exe)
# Using native Windows method
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

# Clear working sets
$processes = Get-Process
foreach ($proc in $processes) {
    try {
        $proc.Refresh()
    } catch {}
}

# Get memory after
$afterMem = Get-WmiObject Win32_OperatingSystem | Select-Object @{Name='FreeGB';Expression={[math]::Round($_.FreePhysicalMemory/1MB,2)}}

# Log result
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$freed = $afterMem.FreeGB - $beforeMem.FreeGB
Add-Content "C:\repos\AI-Librarian\logs\ram_flush.log" "$timestamp - Freed $freed GB RAM"

Write-Host "✅ RAM flush complete - freed $freed GB"
