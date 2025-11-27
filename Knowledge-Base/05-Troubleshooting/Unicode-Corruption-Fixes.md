# UNICODE CORRUPTION - TROUBLESHOOTING & FIXES
**Last Updated:** 2025-11-26  
**Status:** RESOLVED 

##  OVERVIEW

Widespread Unicode corruption issues affected Python files and development tools across Kyle's Windows 11 system. Characters were being corrupted with invalid byte sequences (e.g., `\x84`, `\x93`, `\x94`, `\x96`), causing syntax errors and breaking various development tools.

---

##  SYMPTOMS

### What Was Happening:
- Python files showing invalid UTF-8 sequences
- Syntax errors on perfectly valid code
- Characters like quotes and apostrophes corrupted
- `.pyc` files containing corrupted data
- VSCode and other editors displaying encoding warnings
- Git showing unexpected diffs due to encoding changes

### Common Corruption Patterns:
```
Original → Corrupted
"        → \x93 or \x94
'        → \x92 or \x96
—        → \x97
…        → \x85
```

These are Windows-1252 characters being misinterpreted as UTF-8.

---

##  ROOT CAUSES IDENTIFIED

1. **System Encoding Mismatch:**
   - Windows using Windows-1252 in some contexts
   - Python expecting UTF-8
   - Copy/paste from certain applications introducing bad encoding

2. **Editor Settings:**
   - Mixed encoding settings across editors
   - Auto-encoding detection failing
   - BOM (Byte Order Mark) issues

3. **Environment Variables:**
   - `PYTHONIOENCODING` not set to UTF-8
   - System locale settings

---

##  FIXES APPLIED

### 1. System-Wide UTF-8 Enforcement
**PowerShell Commands:**
```powershell
# Set Python I/O encoding
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
```

**Registry Changes:**
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor
  → AutoRun: chcp 65001 >nul
  
(Forces UTF-8 code page on cmd.exe startup)
```

**Impact:** All new processes use UTF-8 by default

### 2. Python File Cleanup
**Automated Repair Script:** `C:\Temp\fix_python_unicode.ps1`

**What It Does:**
- Scans all Python files recursively
- Detects encoding issues
- Backs up corrupted files
- Repairs common corruption patterns
- Validates Python syntax after repair

**Corruption Patterns Fixed:**
```python
# Common Windows-1252 → UTF-8 mappings
'\x93' → '"'  # Left double quote
'\x94' → '"'  # Right double quote
'\x92' → "'"  # Single quote
'\x96' → '–'  # En dash
'\x97' → '—'  # Em dash
'\x85' → '…'  # Ellipsis
```

### 3. VSCode Configuration
**File:** `.vscode/settings.json`
```json
{
  "files.encoding": "utf8",
  "files.autoGuessEncoding": false,
  "python.terminal.activateEnvironment": true,
  "[python]": {
    "files.encoding": "utf8"
  }
}
```

**Impact:** Consistent UTF-8 encoding in VSCode

### 4. Git Configuration
```bash
git config --global core.quotepath false
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8
```

**Impact:** Git handles UTF-8 correctly

### 5. PowerShell Profile
**File:** `$PROFILE` (PowerShell profile)
```powershell
# Force UTF-8 encoding
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**Impact:** PowerShell outputs UTF-8

---

##  DETECTION SCRIPTS

### Check for Corrupted Files:
```powershell
# Scan directory for encoding issues
Get-ChildItem -Path "C:\Path\To\Scan" -Recurse -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding Byte
    $invalidBytes = $content | Where-Object { $_ -ge 0x80 -and $_ -le 0x9F }
    if ($invalidBytes) {
        Write-Host "Corrupted: $($_.FullName)" -ForegroundColor Red
    }
}
```

### Verify Python Encoding:
```python
import sys
print(f"Default encoding: {sys.getdefaultencoding()}")
print(f"File system encoding: {sys.getfilesystemencoding()}")
print(f"Preferred encoding: {locale.getpreferredencoding()}")
# Should all show: utf-8
```

---

##  AFFECTED LOCATIONS

### Directories Cleaned:
- Python project directories (all .py files)
- `.pyc` cache files (regenerated after cleanup)
- VSCode workspace settings
- PowerShell scripts
- Configuration files (.json, .md, .txt)

### Files Backed Up:
- All corrupted files backed up to `_corrupted_backup\` before repair
- Original timestamps preserved
- Can be restored if needed

---

##  PREVENTION

### Best Practices:
1. **Always Use UTF-8:**
   - Save files as UTF-8 without BOM
   - Configure editors to default to UTF-8

2. **Avoid Copy/Paste from:**
   - Microsoft Word
   - Outlook emails
   - Websites with fancy formatting
   - If needed, paste into Notepad first, then copy from there

3. **Editor Settings:**
   - VSCode: Set `files.encoding` to `utf8`
   - Notepad++: Settings → Preferences → New Document → UTF-8
   - Sublime Text: `"default_encoding": "UTF-8"`

4. **Environment Variables:**
   - Always set `PYTHONIOENCODING=utf-8`
   - Set `PYTHONUTF8=1` for Python 3.7+

5. **Git Workflow:**
   - Check `git diff` before committing
   - Look for unexpected encoding changes
   - Use `.gitattributes` to enforce line endings

---

##  WARNING SIGNS

### When to Check for Corruption:
- Python syntax errors on valid code
- Unexpected characters in output
- Git showing diffs on unchanged files
- Editor warnings about encoding
- Import errors on working modules

### Quick Test:
```python
# This should work without errors
test_string = "Test with quotes: "Hello" and 'world'"
print(test_string)
```

If you see `SyntaxError: invalid character`, you have corruption.

---

##  RECOVERY PROCEDURE

### If Corruption Reappears:

**1. Stop and Assess:**
```powershell
# Identify the source
# Recent copy/paste? New application? System update?
```

**2. Run Detection:**
```powershell
# Use detection script to find affected files
.\detect_unicode_issues.ps1 -Path "C:\Projects"
```

**3. Backup First:**
```powershell
# Always backup before repair
Copy-Item -Path ".\corrupted_file.py" -Destination ".\corrupted_file.py.backup"
```

**4. Apply Fix:**
```powershell
# Use repair script
.\fix_python_unicode.ps1 -Path ".\corrupted_file.py"
```

**5. Verify:**
```python
# Test the file
python corrupted_file.py
# Should run without errors
```

**6. Update Prevention:**
- Identify what caused it
- Update workflow to prevent recurrence
- Add checks to pre-commit hooks if needed

---

##  SCRIPTS CREATED

### Repair Scripts:
- **`fix_python_unicode.ps1`** - Main repair script
  - Scans Python files
  - Backs up originals
  - Repairs corruption patterns
  - Validates syntax

### Detection Scripts:
- **`detect_unicode_issues.ps1`** - Finds corrupted files
  - Recursive scanning
  - Reports invalid byte sequences
  - Creates list for batch repair

### Prevention Scripts:
- **PowerShell Profile additions** - Enforces UTF-8
- **VSCode settings** - Consistent encoding
- **Git hooks** (optional) - Pre-commit encoding checks

---

##  RESOLUTION STATUS

**Status:** RESOLVED   
**Date Fixed:** 2025-11-25/26  
**Files Repaired:** Multiple Python files across system  
**Prevention:** System-wide UTF-8 enforcement active  
**Monitoring:** Periodic checks recommended

### Verification Completed:
 All Python files validated  
 Environment variables set  
 Editor configurations updated  
 Git config updated  
 PowerShell profile configured  
 No new corruption detected  

---

##  LESSONS LEARNED

1. **UTF-8 Everywhere:**
   - Modern development requires consistent UTF-8
   - Windows still defaults to Windows-1252 in some contexts
   - Explicit configuration is essential

2. **Prevention > Repair:**
   - Set up environment correctly from the start
   - Don't rely on auto-detection
   - Configure all tools explicitly

3. **Source Control Helps:**
   - Git showed which files were affected
   - Easy to revert if repair fails
   - History shows when corruption was introduced

4. **Multiple Vectors:**
   - Corruption can come from many sources
   - System-wide solution needed
   - One fix isn't enough

5. **Automation is Key:**
   - Scripts for detection and repair
   - Automated checks prevent recurrence
   - Manual checking is error-prone

---

##  RELATED ISSUES

### Common Co-occurring Problems:
- Python import errors (fixed by repair)
- Syntax errors on valid code (fixed by repair)
- Git diff noise (fixed by encoding config)
- Editor warnings (fixed by settings)
- PowerShell display issues (fixed by profile)

### Not Related To:
- Network encoding (different issue)
- Database encoding (separate config)
- Binary files (not affected by UTF-8)

---

##  REFERENCES

### Useful Commands:
```powershell
# Check current code page
chcp

# Force UTF-8
chcp 65001

# Check Python encoding
python -c "import sys; print(sys.getdefaultencoding())"

# List environment variables
Get-ChildItem Env: | Where-Object { $_.Name -like "*PYTHON*" }
```

### Configuration Files:
- **PowerShell:** `$PROFILE` (usually `~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`)
- **VSCode:** `.vscode/settings.json` or User Settings
- **Git:** `~\.gitconfig`

---

**Created:** 2025-11-26  
**Status:** Active and Monitored  
**Last Incident:** 2025-11-25 (Resolved)  
**Prevention Active:** YES 

---

**Note:** This was a major system-wide issue that required comprehensive fixes across multiple layers (system, environment, editor, Git). All fixes are now in place and working. Monitor for any recurrence and apply detection scripts periodically.
