#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hydra Integration for AI-Librarian
Parallel delta compression orchestration
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from compressor.delta_compressor import DeltaCompressor


class HydraCompressionOrchestrator:
    """Orchestrates parallel delta compression using Hydra."""
    
    def __init__(self, raw_logs_dir, compressed_dir):
        self.raw_logs_dir = Path(raw_logs_dir)
        self.compressed_dir = Path(compressed_dir)
        self.compressed_dir.mkdir(exist_ok=True)
    
    def get_uncompressed_files(self):
        """Find all raw log files that need compression."""
        if not self.raw_logs_dir.exists():
            return []
        
        uncompressed = []
        for log_file in self.raw_logs_dir.glob("*.jsonl"):
            compressed_name = f"compressed_{log_file.name}"
            if not (self.compressed_dir / compressed_name).exists():
                uncompressed.append(log_file)
        
        return uncompressed
    
    def compress_parallel(self):
        """Execute parallel compression."""
        files = self.get_uncompressed_files()
        
        if not files:
            print("[INFO] No uncompressed files found")
            return
        
        print(f"[HYDRA] Found {len(files)} files to compress")
        
        # Create compressor
        compressor = DeltaCompressor(
            str(self.raw_logs_dir),
            str(self.compressed_dir)
        )
        
        # Compress each file
        for f in files:
            print(f"  Compressing {f.name}...")
            compressor.compress_log_file(f)
        
        print("[OK] Compression complete")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    
    orchestrator = HydraCompressionOrchestrator(
        str(project_root / "logger" / "raw_logs"),
        str(project_root / "compressor" / "compressed")
    )
    
    orchestrator.compress_parallel()
