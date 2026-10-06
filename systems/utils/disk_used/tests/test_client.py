"""
Client script to test and demonstrate du.py
"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

from du import DiskUsage


def main():
    # 1. Create a clean temporary workspace
    with TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)

        print("--- Setting Up Test Files ---")
        
        # Create a 100-byte file
        file1 = tmp_dir / "file1.txt"
        file1.write_bytes(b"A" * 100)
        print("Created: file1.txt (100 bytes)")

        # Create two hard links pointing to file1 (shares the same inode)
        link1 = tmp_dir / "link1.txt"
        os.link(file1, link1)
        print("Created: link1.txt (hard link -> file1.txt)")

        # Create a nested subfolder with a 200-byte file
        subfolder = tmp_dir / "subfolder"
        subfolder.mkdir()
        file2 = subfolder / "file2.txt"
        file2.write_bytes(b"B" * 200)
        print("Created: subfolder/file2.txt (200 bytes)\n")

        print("--- Testing DiskUsage ---")

        # Test 1: Full Scan
        # Total file entries on disk = 3 (file1, link1, file2)
        # Expected unique files = 2 (file1 and file2)
        # Expected total size = 300 bytes
        du_full = DiskUsage(tmp_dir)
        files, size = du_full.scan_for_sizes()
        print(f"Full Scan       -> Unique Files: {files} | Total Size: {size} bytes")

        # Test 2: Max Depth = 0 (top folder only, ignores 'subfolder')
        du_depth0 = DiskUsage(tmp_dir, max_depth=0)
        files_d0, size_d0 = du_depth0.scan_for_sizes()
        print(f"Max Depth = 0   -> Unique Files: {files_d0} | Total Size: {size_d0} bytes")


if __name__ == "__main__":
    main()