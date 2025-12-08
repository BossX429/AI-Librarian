# Daily Incremental Backup - C:\repos
# Backs up to D:\Backups (create if needed)

$ErrorActionPreference = 'Continue'

$source = "C:\repos"
$destination = "D:\Backups\repos_" + (Get-Date -Format "yyyy-MM-dd")
$logFile = "C:\repos\AI-Librarian\logs\backup.log"

# Create backup directory if needed
if (-not (Test-Path "D:\Backups")) {
    New-Item -ItemType Directory -Path "D:\Backups" -Force
}

# Create log directory if needed
if (-not (Test-Path "C:\repos\AI-Librarian\logs")) {
    New-Item -ItemType Directory -Path "C:\repos\AI-Librarian\logs" -Force
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    # Use robocopy for incremental backup
    $result = robocopy $source $destination /MIR /XD node_modules __pycache__ .git .venv /R:3 /W:5 /MT:8 /LOG+:$logFile /NP
    
    $size = (Get-ChildItem $destination -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1GB
    $sizeGB = [math]::Round($size, 2)
    
    Add-Content $logFile "$timestamp - Backup complete: $sizeGB GB"
    Write-Host "✅ Backup complete: $sizeGB GB to $destination"
    
} catch {
    Add-Content $logFile "$timestamp - ERROR: $_"
    Write-Host "❌ Backup failed: $_"
}
