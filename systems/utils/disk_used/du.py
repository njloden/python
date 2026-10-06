"""
Author:         Nick Loden

Last Update:    10/06/2026

Description:    This script will get the true disk usage for a target directory down to the specified depth/level. Duplicate inodes
                pointing to the same disk blocks will not be counted.

Input:          None

Standard Form:  python system_health_check.py <target path> <optional: max depth: num>
"""

import os
import argparse
from pathlib import Path


class DiskUsage:
    def __init__(self, root_dir: Path, max_depth: int | None = None):
        self.root_dir = root_dir.resolve()
        self.max_depth = max_depth
        self.seen_files = set() # keep track of unique files, hash table implementation with O(1) key lookup complexity
        self.unique_file_count = 0
        self.total_size = 0

    
    def scan_for_sizes(self) -> tuple[int, int]:
        """traverse directory and return tuple of (unique file count, total size in bytes)."""
        base_depth = len(self.root_dir.parts) 

        for root, dirs, files in os.walk(self.root_dir):
            root_path = Path(root)
            current_depth = len(root_path.parts) - base_depth

            # Once max_depth is reached, clear 'dirs' in-place so os.walk stops descending
            #   while allowing the current loop iteration to process files at this level.
            if self.max_depth is not None and current_depth >= self.max_depth:
                dirs.clear()

            for file in files:
                file_path = root_path / file

                if file_path.is_symlink(): # skips symlinks
                    continue

                file_stat = file_path.stat()
                file_key = (file_stat.st_dev, file_stat.st_ino) # ensure unique key across multiple devices/filesystems

                if file_key not in self.seen_files: 
                    self.seen_files.add(file_key)
                    self.unique_file_count += 1
                    self.total_size += file_stat.st_size
                    continue

        return (self.unique_file_count, self.total_size)
    

def main():
    parser = argparse.ArgumentParser(
        prog="du.py",
        description="Calculate true disk usage accounting for duplicate hard links.",
        usage="python %(prog)s [-d MAX_DEPTH] target_path")
    
    parser.add_argument("target_path", type=Path, help="Target directory path")
    parser.add_argument("-d", "--max-depth", type=int, default=None, help="Maximum search depth")
    args = parser.parse_args()

    du = DiskUsage(args.target_path, max_depth=args.max_depth)
    count, size = du.scan_for_sizes()
    print(f"Files: {count} | Total Size: {size} bytes")


if __name__ == "__main__":
    main()

    


