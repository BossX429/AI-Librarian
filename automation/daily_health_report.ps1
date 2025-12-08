# Daily Health Report
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$reportFile = "C:\repos\AI-Librarian\automation\logs\health_report_$(Get-Date -Format 'yyyy-MM-dd').txt"

"=== SYSTEM HEALTH REPORT ===" | Out-File $reportFile
"Generated: $date`n" | Out-File $reportFile -Append

# Hardware
$cpu = Get-CimInstance Win32_Processor
$os = Get-CimInstance Win32_OperatingSystem
$ramUsedGB = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 2)
$ramTotalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$ramPercent = [math]::Round(($ramUsedGB / $ramTotalGB) * 100, 1)

"[HARDWARE]" | Out-File $reportFile -Append
"CPU: $($cpu.Name)" | Out-File $reportFile -Append
"RAM: $ramUsedGB GB / $ramTotalGB GB ($ramPercent%)`n" | Out-File $reportFile -Append

# Critical Processes
"[CRITICAL PROCESSES]" | Out-File $reportFile -Append
$criticalProcs = @('claude', 'ollama', 'pythonw')
foreach ($proc in $criticalProcs) {
    $running = Get-Process $proc -ErrorAction SilentlyContinue
    if ($running) {
        "✅ $proc running ($(($running | Measure-Object).Count) instances)" | Out-File $reportFile -Append
    } else {
        "❌ $proc NOT RUNNING" | Out-File $reportFile -Append
    }
}
"`n[COMPLETE]" | Out-File $reportFile -Append

Write-Host "Health report saved: $reportFile"
