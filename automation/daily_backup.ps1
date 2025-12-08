# Automated Backup System
param([switch]$DryRun = $false)

$logFile = "C:\repos\AI-Librarian\automation\logs\backup.log"
$backupRoot = "C:\Backups"
$date = Get-Date -Format "yyyy-MM-dd"

function Write-Log {
    param($Message)
    "$date $(Get-Date -Format 'HH:mm:ss') - $Message" | Out-File -FilePath $logFile -Append
    Write-Host $Message
}

Write-Log "=== BACKUP START ==="

$dailyBackup = "$backupRoot\Daily\$date"
if (-not (Test-Path $dailyBackup) -and -not $DryRun) {
    New-Item -Path $dailyBackup -ItemType Directory -Force | Out-Null
}

$repos = @(
    "C:\repos\AI-Librarian",
    "C:\repos\Local-Router",
    "C:\repos\NEXUS",
    "C:\repos\Agent-Farm"
)

foreach ($repo in $repos) {
    $repoName = Split-Path $repo -Leaf
    $destination = "$dailyBackup\$repoName"
    
    if (-not $DryRun) {
        robocopy $repo $destination /MIR /R:3 /W:5 /NFL /NDL /NJH /NJS | Out-Null
        Write-Log "✅ Backed up $repoName"
    }
}

Write-Log "=== BACKUP COMPLETE ==="
