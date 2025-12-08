# Weekly Temp Cleanup - Auto-scheduled
# Clears Windows temp, system temp, prefetch, and downloads cache

$ErrorActionPreference = 'SilentlyContinue'

$cleaned = 0

# Windows Temp
Get-ChildItem $env:TEMP -Recurse -Force | Remove-Item -Force -Recurse
$cleaned += (Get-ChildItem $env:TEMP -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum

# System Temp
Get-ChildItem C:\Windows\Temp -Recurse -Force | Remove-Item -Force -Recurse
$cleaned += (Get-ChildItem C:\Windows\Temp -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum

# Prefetch
Get-ChildItem C:\Windows\Prefetch -Force | Remove-Item -Force
$cleaned += (Get-ChildItem C:\Windows\Prefetch -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum

# Edge Cache
$edgeCache = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache"
if (Test-Path $edgeCache) {
    Get-ChildItem $edgeCache -Recurse -Force | Remove-Item -Force -Recurse
}

# Log result
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$cleanedMB = [math]::Round($cleaned/1MB, 2)
Add-Content "C:\repos\AI-Librarian\logs\cleanup.log" "$timestamp - Cleaned $cleanedMB MB"

Write-Host "✅ Cleaned $cleanedMB MB"
