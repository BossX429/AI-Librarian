# Weekly System Maintenance Automation
param([switch]$DryRun = $false)

$logFile = "C:\repos\AI-Librarian\automation\logs\maintenance.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log {
    param($Message)
    "$timestamp - $Message" | Out-File -FilePath $logFile -Append
    Write-Host $Message
}

Write-Log "=== WEEKLY MAINTENANCE START ==="

# Clear Windows Temp
$tempSize = (Get-ChildItem $env:TEMP -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
if (-not $DryRun) {
    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Log "✅ Cleared Windows Temp: $([math]::Round($tempSize, 2)) MB"
}

# Clear System Temp
$sysTempSize = (Get-ChildItem C:\Windows\Temp -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
if (-not $DryRun) {
    Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Log "✅ Cleared System Temp: $([math]::Round($sysTempSize, 2)) MB"
}

# Flush DNS
if (-not $DryRun) {
    ipconfig /flushdns | Out-Null
    Write-Log "✅ Flushed DNS cache"
}

Write-Log "=== MAINTENANCE COMPLETE ==="
