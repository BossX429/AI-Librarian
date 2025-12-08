# Real-Time Performance Dashboard
while ($true) {
    Clear-Host
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "       SYSTEM PERFORMANCE DASHBOARD" -ForegroundColor Cyan
    Write-Host "       $timestamp" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    # CPU
    $cpuLoad = (Get-CimInstance Win32_Processor).LoadPercentage
    $cpuBar = "█" * [math]::Floor($cpuLoad / 5)
    Write-Host "CPU:  [$($cpuBar.PadRight(20))] $cpuLoad%" -ForegroundColor $(if($cpuLoad -gt 80){"Red"}elseif($cpuLoad -gt 50){"Yellow"}else{"Green"})
    
    # RAM
    $os = Get-CimInstance Win32_OperatingSystem
    $ramPercent = [math]::Round((($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize) * 100, 1)
    $ramBar = "█" * [math]::Floor($ramPercent / 5)
    Write-Host "RAM:  [$($ramBar.PadRight(20))] $ramPercent%" -ForegroundColor $(if($ramPercent -gt 80){"Red"}elseif($ramPercent -gt 60){"Yellow"}else{"Green"})
    
    # Critical Processes
    Write-Host "`nCRITICAL PROCESSES:" -ForegroundColor Yellow
    $procs = @('claude', 'ollama', 'pythonw')
    foreach ($p in $procs) {
        $running = Get-Process $p -ErrorAction SilentlyContinue
        if ($running) {
            Write-Host "  ✅ $p" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $p" -ForegroundColor Red
        }
    }
    
    Start-Sleep -Seconds 5
}
