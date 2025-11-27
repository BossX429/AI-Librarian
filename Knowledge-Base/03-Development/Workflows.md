# Development Workflows

## Python Development

### Environment Setup
```powershell
# Python installation path (to be added)
$PYTHON_PATH = "C:\Program Files\Python312"
$PIP_PATH = "C:\Program Files\Python312\Scripts\pip.exe"

# Common virtual environment creation
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Common Packages
- pandas, numpy - Data analysis
- torch, tensorflow - ML frameworks (ROCm for AMD GPU)
- requests, aiohttp - HTTP clients
- fastapi, flask - Web frameworks
- ollama - Local model interface

## PowerShell Automation

### Execution Policy
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for development
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Common Commands
```powershell
# System info
systeminfo
Get-ComputerInfo

# Process management
Get-Process
Stop-Process -Name "processname"

# Service management
Get-Service
Start-Service -Name "servicename"
```
