# Network TCP Optimization
# Run this as admin to optimize network settings

Write-Host "Optimizing TCP settings..."

netsh int tcp set global autotuninglevel=normal
netsh int tcp set global chimney=enabled
netsh int tcp set global dca=enabled
netsh int tcp set global netdma=enabled

Set-NetTCPSetting -SettingName InternetCustom -AutoTuningLevelLocal Normal
Set-NetAdapterAdvancedProperty -Name "Ethernet" -DisplayName "Interrupt Moderation" -DisplayValue "Enabled" -ErrorAction SilentlyContinue
Set-NetAdapterAdvancedProperty -Name "Ethernet" -DisplayName "Large Send Offload V2 (IPv4)" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

Write-Host "✅ Network TCP optimization complete - restart may be required"
