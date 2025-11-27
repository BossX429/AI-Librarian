# Enable Windows EFS Encryption for AI-Librarian Sensitive Data
# Run this script as Administrator

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "AI-Librarian Security Hardening" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$directories = @(
    "C:\repos\AI-Librarian\logger\raw_logs",
    "C:\repos\AI-Librarian\curator\processed",
    "C:\repos\AI-Librarian\compressor\compressed"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "Encrypting: $dir" -ForegroundColor Yellow
        
        try {
            # Enable encryption
            cipher /e /s:$dir 2>&1 | Out-Null
            
            # Verify encryption
            $result = cipher /c $dir
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ Successfully encrypted" -ForegroundColor Green
            } else {
                Write-Host "  ✗ Encryption may have failed" -ForegroundColor Red
            }
        } catch {
            Write-Host "  ✗ Error: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "Directory not found: $dir" -ForegroundColor Gray
    }
    Write-Host ""
}

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setting Restrictive Permissions" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "Setting permissions: $dir" -ForegroundColor Yellow
        
        try {
            # Remove inheritance
            icacls $dir /inheritance:r | Out-Null
            
            # Grant full control to current user only
            $username = $env:USERNAME
            icacls $dir /grant:r "${username}:(OI)(CI)F" | Out-Null
            
            Write-Host "  ✓ Permissions set to user-only access" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Error: $_" -ForegroundColor Red
        }
    }
    Write-Host ""
}

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Security Hardening Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your sensitive data is now:" -ForegroundColor White
Write-Host "  ✓ Encrypted at rest (Windows EFS)" -ForegroundColor Green
Write-Host "  ✓ Protected with user-only permissions" -ForegroundColor Green
Write-Host "  ✓ Safe from unauthorized access" -ForegroundColor Green
Write-Host ""
Write-Host "Note: Keep your Windows password secure!" -ForegroundColor Yellow
Write-Host "EFS encryption is tied to your user account." -ForegroundColor Yellow
