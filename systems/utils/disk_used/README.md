# System Utilities

A collection of lightweight, low-level Python scripts that re-implement and extend standard Unix/Linux command-line utilities.

---

## 1. Disk Usage Tool (`du.py`)

`du.py` traverses directory structures to compute true disk space usage. Unlike naive file traversals, it tracks unique inode numbers (`st_dev`, `st_ino`) to ensure duplicate hard links pointing to the same disk blocks are counted only once. It also supports search depth limiting to restrict recursion.

### Standard Form / Usage

```bash
python du.py [-d MAX_DEPTH] <target_path>
```

#### Command Arguments
* `target_path` *(Required)*: Path to the directory you want to inspect.
* `-d, --max-depth` *(Optional)*: Integer specifying the maximum folder recursion depth (`0` searches top-level files only).

---

### Example Commands & Output

#### 1. Standard Execution
Calculate usage across an entire target directory:

```bash
python du.py /var/log
```

**Output:**
```text
Files: 142 | Total Size: 18492012 bytes
```

#### 2. Max Depth Restriction
Limit recursion to 1 directory level deep:

```bash
python du.py -d 1 /var/log
```

**Output:**
```text
Files: 38 | Total Size: 4194304 bytes
```

---

## 2. Running Tests

The test suite validates hard-link deduplication and depth pruning using temporary isolated directories.

Execute the test client from the root of the `system_utilities/` directory:

```bash
python -m tests.test_client
```

**Example Test Output:**
```text
--- Setting Up Test Files ---
Created: file1.txt (100 bytes)
Created: link1.txt (hard link -> file1.txt)
Created: subfolder/file2.txt (200 bytes)

--- Testing DiskUsage ---
Full Scan       -> Unique Files: 2 | Total Size: 300 bytes
Max Depth = 0   -> Unique Files: 1 | Total Size: 100 bytes
```