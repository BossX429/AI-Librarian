# Code Snippets

## GPU Monitoring

### Check AMD GPU Status
```powershell
# Using AMD System Monitor
Get-Process | Where-Object {$_.ProcessName -like "*amd*"}

# GPU memory info would need AMD tools
```

### Python GPU Check
```python
import torch

# Check if ROCm is available
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("No GPU available")
```

## File Operations

### Batch File Processing
```python
import os
from pathlib import Path

def process_files(directory, extension):
    """Process all files with given extension in directory"""
    path = Path(directory)
    for file in path.rglob(f"*.{extension}"):
        # Your processing logic here
        print(f"Processing: {file}")
```

## System Automation

### Windows Service Template
```python
import win32serviceutil
import win32service
import win32event
import servicemanager

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyServiceName"
    _svc_display_name_ = "My Service Display Name"
