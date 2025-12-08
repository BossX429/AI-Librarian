# Process Monitor - Auto-kill zombies and resource hogs
param([switch]$DryRun = $false)

$logFile = "C:\repos\AI-Librarian\automation\logs\process_monitor.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log {
    param($Message)
    "$timestamp - $Message" | Out-File -FilePath $logFile -Append
    Write-Host $Message
}

Write-Log "=== PROCESS MONITOR START ==="

# Find orphaned pythonw processes
$pythonwProcs = Get-Process pythonw -ErrorAction SilentlyContinue
foreach ($proc in $pythonwProcs) {
    $wmiProc = Get-WmiObject Win32_Process -Filter "ProcessId=$($proc.Id)"
    $parentExists = Get-Process -Id $wmiProc.ParentProcessId -ErrorAction SilentlyContinue
    
    if (-not $parentExists) {
        if (-not $DryRun) {
            Stop-Process -Id $proc.Id -Force
            Write-Log "✅ Killed orphaned pythonw PID $($proc.Id)"
        }
    }
}

# Check memory usage
$memPercent = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize
if ($memPercent -lt 0.2) {
    Write-Log "⚠️ WARNING: Memory usage >80%"
}

Write-Log "=== MONITOR COMPLETE ==="
