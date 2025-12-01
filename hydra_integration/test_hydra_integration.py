#!/usr/bin/env python3
"""
Hydra Integration Test
Tests the Hydra compression orchestrator
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from hydra_compression import HydraCompressionOrchestrator


def test():
    """Test Hydra integration."""
    print("=" * 70)
    print("HYDRA INTEGRATION TEST")
    print("=" * 70)
    
    project_root = Path(r"C:\repos\AI-Librarian")
    
    if not project_root.exists():
        print("[ERROR] AI-Librarian not found")
        return False
    
    print("[OK] AI-Librarian found")
    
    raw_logs = project_root / "logger" / "raw_logs"
    compressed = project_root / "compressor" / "compressed"
    
    orch = HydraCompressionOrchestrator(str(raw_logs), str(compressed))
    files = orch.get_uncompressed_files()
    
    print(f"[OK] Found {len(files)} uncompressed files")
    print("[SUCCESS] Integration test passed")
    
    return True


if __name__ == "__main__":
    success = test()
    sys.exit(0 if success else 1)
