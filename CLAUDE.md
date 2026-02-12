# Miscellaneous Utility Scripts

Collection of Python and Bash scripts for household automation tasks.

## Prerequisites

**Python Scripts:**
```bash
pip install exifread requests beautifulsoup4
```

**Python version:** 3.6+ (tested on 3.x)

## Scripts

### Picture_Foldering.py
Organize photos into year-based folders using EXIF metadata

```bash
python Picture_Foldering.py
```

**What it does:**
- Scans directory for images (jpg, png, gif, raw, cr2, tiff, nef, etc.)
- Extracts EXIF "DateTimeOriginal" metadata
- Creates year folders (e.g., "2023/", "2024/")
- **Moves** images into corresponding year folders

**Configuration:** Edit line 6 - `root_path = '/path/to/image/folder'`

**⚠️ Warning:** Moves files permanently - test on copies first or use version 2

### Picture_Foldering2.py
Enhanced version with additional features (compare to version 1 for differences)

### reddit_scrape.py
Download all images posted by a Reddit user

```bash
python reddit_scrape.py
```

**What it does:**
- Fetches user's submitted posts via Reddit JSON API
- Downloads linked images to `reddit_images/` folder
- Handles pagination for users with many posts

**Configuration:**
- Line 7: `user = "RailScales"` (change to target username)
- Line 8: `folder = "reddit_images"` (destination folder)

**Dependencies:** requests, beautifulsoup4

### reddit_scrape2.py
Enhanced version with better pagination and error handling

### verify_backup.sh
Verify backup integrity by comparing SHA-1 hashes

```bash
./verify_backup.sh
```

**What it does:**
- Compares every file between source and destination
- Uses SHA-1 hashing for file comparison
- Reports mismatches (corrupted/missing files)
- Shows progress percentage

**Configuration:**
- Line 3: `SOURCE_DIR="/Volumes/Backblaze_MacEx4TB32540642"`
- Line 4: `DEST_DIR="/Volumes/My Passport Mac 4TB"`

**⚠️ Warning:** Very slow for large backups (SHA-1 hashing every file)

**When to use:** Verify backup drives after large copy operations

## Usage Patterns

### Photo Organization Workflow
```bash
# 1. Backup photos first!
cp -r /path/to/photos /path/to/backup

# 2. Edit Picture_Foldering.py - set root_path
# 3. Run organizer
python Picture_Foldering.py

# 4. Verify results before deleting backup
```

### Reddit Scraping Workflow
```bash
# 1. Install dependencies
pip install requests beautifulsoup4

# 2. Edit reddit_scrape.py - set username
# 3. Run scraper
python reddit_scrape.py

# Images saved to ./reddit_images/
```

### Backup Verification Workflow
```bash
# 1. Edit verify_backup.sh - set SOURCE_DIR and DEST_DIR
# 2. Make executable
chmod +x verify_backup.sh

# 3. Run verification (takes hours for TB of data)
./verify_backup.sh

# 4. Check output for mismatches
```

## Gotchas

- **Picture_Foldering:** Moves files, doesn't copy - destructive operation
- **Reddit scrapers:** Respect Reddit API rate limits (add delays for large scrapes)
- **verify_backup.sh:** Extremely slow - SHA-1 hash every file (can take hours/days)
- **Python paths:** All scripts have hardcoded paths - customize before running
- **EXIF data:** Picture_Foldering skips files without EXIF DateTimeOriginal tag
