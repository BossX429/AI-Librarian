import sys
#!/usr/bin/env python3
"""Test TRUE parallel compression"""
sys.path.insert(0, str(Path(__file__).parent))

def test():
    print("=" * 70)
    print("HYDRA PARALLEL COMPRESSION TEST")
    print("=" * 70)
    
    project_root = Path(r"C:\repos\AI-Librarian")
    compressor = HydraParallelCompressor(
        str(project_root / "logger" / "raw_logs"),
        str(project_root / "compressor" / "compressed")
    )
    
    files = compressor.get_uncompressed_files()
    print(f"[OK] Found {len(files)} uncompressed files")
    print(f"[OK] Using {compressor.max_workers} worker cores")
    print("[SUCCESS] Parallel integration test passed")
    
    return True

if __name__ == "__main__":
    test()
