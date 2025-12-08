# Install All Automation Scheduled Tasks
$tasks = @(
    @{Name = "System_Weekly_Maintenance"; Script = "weekly_maintenance.ps1"; Trigger = "Weekly"; Day = "Sunday"; Time = "02:00"},
    @{Name = "System_Process_Monitor"; Script = "process_monitor.ps1"; Trigger = "Hourly"},
    @{Name = "System_Daily_Backup"; Script = "daily_backup.ps1"; Trigger = "Daily"; Time = "01:00"},
    @{Name = "System_Health_Report"; Script = "daily_health_report.ps1"; Trigger = "Daily"; Time = "08:00"}
)

foreach ($task in $tasks) {
    Unregister-ScheduledTask -TaskName $task.Name -Confirm:$false -ErrorAction SilentlyContinue
    
    $scriptPath = "C:\repos\AI-Librarian\automation\$($task.Script)"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
    
    if ($task.Trigger -eq "Hourly") {
        $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration ([TimeSpan]::MaxValue)
    } elseif ($task.Trigger -eq "Daily") {
        $trigger = New-ScheduledTaskTrigger -Daily -At $task.Time
    } elseif ($task.Trigger -eq "Weekly") {
        $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $task.Day -At $task.Time
    }
    
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0
    
    Register-ScheduledTask -TaskName $task.Name -Action $action -Trigger $trigger -Principal $principal -Settings $settings | Out-Null
    Write-Host "✅ Installed: $($task.Name)"
}

Write-Host "`n✅ All automation tasks installed!"
