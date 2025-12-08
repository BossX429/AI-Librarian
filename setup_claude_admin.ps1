# Setup Claude Desktop to Always Run as Administrator
# Run this script as Admin once, then Claude will always have admin rights

$claudePath = "C:\Users\kyleh\AppData\Local\AnthropicClaude\app-1.0.1768\claude.exe"
$taskName = "Claude_Desktop_Admin"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute $claudePath

# Create the trigger (at logon)
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

# Create the principal (run with highest privileges)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

# Create the settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Launch Claude Desktop with Administrator privileges on logon"

Write-Host "`n✅ SUCCESS!" -ForegroundColor Green
Write-Host "Claude Desktop will now run with admin privileges on every logon." -ForegroundColor Green
Write-Host "`nTo apply immediately:" -ForegroundColor Cyan
Write-Host "1. Close Claude Desktop" -ForegroundColor White
Write-Host "2. Run: Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
Write-Host "`nOr just restart your PC and it will auto-launch with admin." -ForegroundColor White
