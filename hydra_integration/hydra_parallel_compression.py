#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hydra Parallel Compression - TRUE SIMULTANEOUS EXECUTION
Uses ProcessPoolExecutor for actual multi-core parallel processing
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from compressor.delta_compressor import DeltaCompressor


def compress_single_file(task_data: Dict) -> Dict:
    """
    Worker function - runs on separate core.
    This is what gets executed SIMULTANEOUSLY on multiple processors.
    """
    task_id = task_data['task_id']
    input_file = Path(task_data['input_file'])
    output_dir = Path(task_data['output_dir'])
    
    start_time = time.time()
    
    try:
        # Create compressor instance for this worker
        compressor = DeltaCompressor(
            str(input_file.parent),
            str(output_dir)
        )
        
        # Compress the file
        compressed_file = compressor.compress_log_file(input_file)
        
        duration = time.time() - start_time
        
        if compressed_file:
            original_size = input_file.stat().st_size
            compressed_size = compressed_file.stat().st_size
            compression_ratio = 1 - (compressed_size / original_size) if original_size > 0 else 0
            
            return {
                'task_id': task_id,
                'status': 'success',
                'duration': duration,
                'input_file': input_file.name,
                'output_file': compressed_file.name,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'space_saved': original_size - compressed_size
            }
        else:
            return {
                'task_id': task_id,
                'status': 'failed',
                'duration': duration,
                'error': 'Compression returned None'
            }
    
    except Exception as e:
        duration = time.time() - start_time
        return {
            'task_id': task_id,
            'status': 'failed',
            'duration': duration,
            'error': str(e)
        }


class HydraParallelCompressor:
    """
    TRUE parallel compression orchestrator.
    Uses ProcessPoolExecutor for simultaneous multi-core execution.
    """
    
    def __init__(self, raw_logs_dir: str, compressed_dir: str, max_workers: int = None):
        self.raw_logs_dir = Path(raw_logs_dir)
        self.compressed_dir = Path(compressed_dir)
        self.compressed_dir.mkdir(exist_ok=True)
        
        # Determine number of workers (cores to use)
        if max_workers is None:
            import os
            # Use all available cores, cap at 20
            max_workers = min(os.cpu_count() or 4, 20)
        
        self.max_workers = max_workers
    
    def get_uncompressed_files(self) -> List[Path]:
        """Find all raw log files that need compression."""
        if not self.raw_logs_dir.exists():
            return []
        
        uncompressed = []
        for log_file in self.raw_logs_dir.glob("*.jsonl"):
            compressed_name = f"compressed_{log_file.name}"
            if not (self.compressed_dir / compressed_name).exists():
                uncompressed.append(log_file)
        
        return uncompressed
    
    def compress_parallel(self, max_files: int = None) -> Dict:
        """
        Execute TRUE parallel compression.
        
        This uses ProcessPoolExecutor to spawn worker processes,
        each running on a separate CPU core SIMULTANEOUSLY.
        """
        start_time = time.time()
        
        # Get files to compress
        files = self.get_uncompressed_files()
        
        if max_files:
            files = files[:max_files]
        
        if not files:
            print("[INFO] No uncompressed files found")
            return {
                'status': 'no_work',
                'files_processed': 0,
                'duration': 0
            }
        
        print()
        print("=" * 70)
        print("HYDRA PARALLEL COMPRESSION - TRUE SIMULTANEOUS EXECUTION")
        print("=" * 70)
        print(f"[HYDRA] Files to compress: {len(files)}")
        print(f"[HYDRA] Worker cores: {self.max_workers}")
        print(f"[HYDRA] Mode: PARALLEL (all cores running SIMULTANEOUSLY)")
        print("=" * 70)
        print()
        
        # Create task list
        tasks = []
        for idx, file_path in enumerate(files):
            task = {
                'task_id': f"compress_{idx}",
                'input_file': str(file_path),
                'output_dir': str(self.compressed_dir)
            }
            tasks.append(task)
        
        # Execute in parallel using ProcessPoolExecutor
        results = []
        completed = 0
        
        print("[PARALLEL] Spawning worker processes...")
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks at once
            futures = {executor.submit(compress_single_file, task): task for task in tasks}
            
            print(f"[PARALLEL] {len(futures)} tasks submitted to {self.max_workers} cores")
            print()
            
            # Collect results as they complete
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                
                # Progress indicator
                if result['status'] == 'success':
                    ratio = result['compression_ratio'] * 100
                    print(f"  [{completed}/{len(files)}] ✓ {result['input_file']}: {ratio:.1f}% compressed ({result['duration']:.2f}s)")
                else:
                    print(f"  [{completed}/{len(files)}] ✗ {futures[future]['input_file']}: {result['error']}")
        
        total_duration = time.time() - start_time
        
        # Calculate aggregate stats
        successful = [r for r in results if r['status'] == 'success']
        total_original = sum(r['original_size'] for r in successful)
        total_compressed = sum(r['compressed_size'] for r in successful)
        overall_ratio = 1 - (total_compressed / total_original) if total_original > 0 else 0
        
        print()
        print("=" * 70)
        print("[HYDRA] PARALLEL COMPRESSION COMPLETE")
        print("=" * 70)
        print(f"Files processed: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(results) - len(successful)}")
        print(f"Total duration: {total_duration:.2f}s")
        print(f"Avg per file: {total_duration / len(files):.2f}s")
        print()
        print(f"Original size: {total_original / 1024 / 1024:.2f} MB")
        print(f"Compressed size: {total_compressed / 1024 / 1024:.2f} MB")
        print(f"Compression ratio: {overall_ratio * 100:.1f}%")
        print(f"Space saved: {(total_original - total_compressed) / 1024 / 1024:.2f} MB")
        print("=" * 70)
        
        return {
            'status': 'complete',
            'files_processed': len(results),
            'successful': len(successful),
            'failed': len(results) - len(successful),
            'duration': total_duration,
            'workers_used': self.max_workers,
            'compression_stats': {
                'total_original': total_original,
                'total_compressed': total_compressed,
                'compression_ratio': overall_ratio,
                'space_saved': total_original - total_compressed
            },
            'results': results
        }


def main():
    """CLI interface."""
    project_root = Path(__file__).parent.parent
    
    # Parse arguments
    max_files = None
    max_workers = None
    
    if len(sys.argv) > 1:
        try:
            max_files = int(sys.argv[1])
        except ValueError:
            print("Usage: python hydra_parallel_compression.py [max_files] [max_workers]")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        try:
            max_workers = int(sys.argv[2])
        except ValueError:
            print("Usage: python hydra_parallel_compression.py [max_files] [max_workers]")
            sys.exit(1)
    
    # Create parallel compressor
    compressor = HydraParallelCompressor(
        str(project_root / "logger" / "raw_logs"),
        str(project_root / "compressor" / "compressed"),
        max_workers=max_workers
    )
    
    # Run parallel compression
    result = compressor.compress_parallel(max_files)
    
    # Output result as JSON
    print()
    print("[HYDRA] Result JSON:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
