# Quick System Status Check
# Fast one-liner health check

$cpu = (Get-CimInstance Win32_Processor).LoadPercentage
$os = Get-CimInstance Win32_OperatingSystem
$ramPercent = [math]::Round((($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize) * 100, 1)
$disk = Get-PSDrive C
$diskPercent = [math]::Round(($disk.Used / ($disk.Used + $disk.Free)) * 100, 1)

$status = if ($cpu -lt 50 -and $ramPercent -lt 70 -and $diskPercent -lt 80) { "✅ HEALTHY" } 
          elseif ($cpu -lt 80 -and $ramPercent -lt 85 -and $diskPercent -lt 90) { "⚠️ WARNING" }
          else { "❌ CRITICAL" }

Write-Host "`n$status - CPU: $cpu% | RAM: $ramPercent% | DISK: $diskPercent%`n" -ForegroundColor $(
    if ($status -like "*HEALTHY*") { "Green" }
    elseif ($status -like "*WARNING*") { "Yellow" }
    else { "Red" }
)

# Check critical processes
$critical = @('claude', 'ollama', 'pythonw')
foreach ($proc in $critical) {
    $running = Get-Process $proc -ErrorAction SilentlyContinue
    if ($running) {
        Write-Host "  ✅ $proc" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $proc NOT RUNNING" -ForegroundColor Red
    }
}

Write-Host ""
