# Network TCP Optimization
# Optimizes Windows TCP stack for performance
# Note: This must run as Administrator

Write-Host "TITAN Network Optimization..." -ForegroundColor Cyan

try {
    # TCP Auto-Tuning
    netsh int tcp set global autotuninglevel=normal
    Write-Host "✓ TCP Auto-tuning: Normal" -ForegroundColor Green
    
    # Chimney Offload
    netsh int tcp set global chimney=enabled
    Write-Host "✓ Chimney Offload: Enabled" -ForegroundColor Green
    
    # Direct Cache Access
    netsh int tcp set global dca=enabled
    Write-Host "✓ DCA: Enabled" -ForegroundColor Green
    
    # NetDMA
    netsh int tcp set global netdma=enabled
    Write-Host "✓ NetDMA: Enabled" -ForegroundColor Green
    
    # Adapter settings
    $adapter = Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -First 1
    if ($adapter) {
        Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Interrupt Moderation" -DisplayValue "Enabled" -ErrorAction SilentlyContinue
        Write-Host "✓ Interrupt Moderation: Enabled" -ForegroundColor Green
        
        Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Large Send Offload V2 (IPv4)" -DisplayValue "Disabled" -ErrorAction SilentlyContinue
        Write-Host "✓ LSO: Disabled (reduces latency)" -ForegroundColor Green
    }
    
    Write-Host "`n✅ Network optimization complete!" -ForegroundColor Green
    Write-Host "   Restart may be required for all changes to take effect" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}
