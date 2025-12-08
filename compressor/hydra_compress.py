import sys
#!/usr/bin/env python3
"""
Hydra Compression CLI - Parallel compression with 20-core power
Drop-in replacement for delta_compressor.py with PARALLEL execution
"""

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Main CLI interface - matches delta_compressor.py interface"""
    
    # Default paths
    raw_logs_dir = Path(__file__).parent.parent / "logger" / "raw_logs"
    compressed_dir = Path(__file__).parent / "compressed"
    
    # Initialize parallel compressor
    compressor = HydraParallelCompressor(str(raw_logs_dir), str(compressed_dir))
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "compress":
            # PARALLEL compress all logs
            compressor.compress_parallel()
        elif command == "decompress" and len(sys.argv) > 2:
            # Decompress not supported in parallel mode - use original
            print("ERROR: Decompress not supported in Hydra mode")
            print("Use: python delta_compressor.py decompress <file>")
            sys.exit(1)
        else:
            print("Usage:")
            print("  python hydra_compress.py compress    # PARALLEL compress all logs")
    else:
        # Default action: parallel compress all logs
        compressor.compress_parallel()

if __name__ == "__main__":
    main()
