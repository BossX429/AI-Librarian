# Zombie Process Hunter - Runs every hour
# Kills orphaned pythonw processes and other zombies

$ErrorActionPreference = 'SilentlyContinue'

$killed = @()

# Find orphaned pythonw processes
$pythonProcs = Get-Process pythonw -ErrorAction SilentlyContinue
foreach ($proc in $pythonProcs) {
    try {
        $wmiProc = Get-WmiObject Win32_Process -Filter "ProcessId=$($proc.Id)"
        $parent = Get-Process -Id $wmiProc.ParentProcessId -ErrorAction SilentlyContinue
        
        # If parent is dead and process is old (>24 hours)
        if (-not $parent -and ((Get-Date) - $proc.StartTime).TotalHours -gt 24) {
            Stop-Process -Id $proc.Id -Force
            $killed += "pythonw PID $($proc.Id)"
        }
    } catch {}
}

# Find processes using >50% CPU for >30 minutes
$highCPU = Get-Process | Where-Object {
    $_.CPU -gt 1800 -and 
    $_.Name -notin @('claude', 'ollama', 'python', 'pythonw', 'System', 'Idle', 'MsMpEng')
}

foreach ($proc in $highCPU) {
    try {
        Stop-Process -Id $proc.Id -Force
        $killed += "$($proc.Name) PID $($proc.Id) (high CPU)"
    } catch {}
}

# Log results
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
if ($killed.Count -gt 0) {
    Add-Content "C:\repos\AI-Librarian\logs\zombie_hunter.log" "$timestamp - Killed: $($killed -join ', ')"
} else {
    Add-Content "C:\repos\AI-Librarian\logs\zombie_hunter.log" "$timestamp - No zombies found"
}

Write-Host "✅ Zombie hunter complete - killed $($killed.Count) processes"
