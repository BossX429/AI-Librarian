# Uninstall Git Auto-Sync Scheduled Task

$TaskName = "AI_Librarian_Git_AutoSync"

Write-Host "Uninstalling Git Auto-Sync Scheduled Task..." -ForegroundColor Yellow

$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "✓ Git Auto-Sync task removed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Task '$TaskName' not found." -ForegroundColor Red
}
