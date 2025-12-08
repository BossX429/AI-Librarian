# Remove Claude Desktop Admin Auto-Launch
# Run this script as Admin to revert to normal non-admin Claude

$taskName = "Claude_Desktop_Admin"

$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "✅ Removed admin auto-launch task" -ForegroundColor Green
    Write-Host "Claude Desktop will now run normally without admin privileges." -ForegroundColor White
} else {
    Write-Host "⚠️ Task '$taskName' not found - nothing to remove" -ForegroundColor Yellow
}
