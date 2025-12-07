# Install Git Auto-Sync Scheduled Task
# Runs every 30 minutes to automatically commit and push changes

$TaskName = "AI_Librarian_Git_AutoSync"
$ScriptPath = Join-Path $PSScriptRoot "run_git_auto_sync.bat"
$WorkingDir = $PSScriptRoot

Write-Host "Installing Git Auto-Sync Scheduled Task..." -ForegroundColor Cyan

# Remove existing task if present
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "→ Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create scheduled task action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`"" -WorkingDirectory $WorkingDir

# Create trigger - every 30 minutes
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)

# Task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

# Register the task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Automatically commits and pushes AI-Librarian changes every 30 minutes"

Write-Host "✓ Git Auto-Sync scheduled task installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Task Details:" -ForegroundColor Cyan
Write-Host "  Name: $TaskName"
Write-Host "  Frequency: Every 30 minutes"
Write-Host "  Script: $ScriptPath"
Write-Host ""
Write-Host "To manage the task:" -ForegroundColor Yellow
Write-Host "  View: Get-ScheduledTask -TaskName '$TaskName'"
Write-Host "  Start: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "  Stop: Stop-ScheduledTask -TaskName '$TaskName'"
Write-Host "  Uninstall: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
Write-Host ""
Write-Host "Testing now..." -ForegroundColor Cyan
Start-ScheduledTask -TaskName $TaskName
Start-Sleep -Seconds 3

# Check log
$LogPath = Join-Path $PSScriptRoot "git_auto_sync.log"
if (Test-Path $LogPath) {
    Write-Host "Recent log output:" -ForegroundColor Cyan
    Get-Content $LogPath -Tail 10
}
