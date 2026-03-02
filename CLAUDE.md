# Miscellaneous Utility Scripts

Collection of Python and Bash scripts for household automation tasks.

## Prerequisites

**Python Scripts:**
```bash
pip install exifread requests
```

**Python version:** 3.6+

## Scripts

### photo_organizer.py
Organize photos into year/month/day folders using EXIF metadata

```bash
cd /path/to/photos
python photo_organizer.py
```

**What it does:**
- Scans directory for images (jpg, jpeg, png, gif, bmp, raw, cr2, tiff, nef, etc.)
- Extracts EXIF "DateTimeOriginal" metadata
- Creates year/month/day folders (e.g., "2023/06/15/")
- **Moves** images into corresponding date folders

**Configuration:** Uses current working directory by default (`os.getcwd()`)

**Warning:** Moves files permanently - test on copies first

### reddit_scraper.py
Download all images posted by a Reddit user

```bash
python reddit_scraper.py
```

**What it does:**
- Fetches user's submitted posts via Reddit JSON API
- Downloads linked images to `reddit_images/` folder
- Handles pagination for users with many posts

**Configuration:**
- Edit `user` variable (change to target username)
- Edit `folder` variable (destination folder)

**Dependencies:** requests

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
- `SOURCE_DIR` - path to source drive
- `DEST_DIR` - path to destination drive

**Warning:** Very slow for large backups (SHA-1 hashing every file)

## Usage Patterns

### Photo Organization Workflow
```bash
# 1. Backup photos first!
cp -r /path/to/photos /path/to/backup

# 2. Navigate to photo directory
cd /path/to/photos

# 3. Run organizer
python photo_organizer.py

# 4. Verify results before deleting backup
```

### Reddit Scraping Workflow
```bash
# 1. Install dependencies
pip install requests

# 2. Edit reddit_scraper.py - set username
# 3. Run scraper
python reddit_scraper.py

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

- **photo_organizer:** Moves files, doesn't copy - destructive operation
- **Reddit scraper:** Respect Reddit API rate limits (add delays for large scrapes)
- **verify_backup.sh:** Extremely slow - SHA-1 hash every file (can take hours/days)
- **EXIF data:** photo_organizer skips files without EXIF DateTimeOriginal tag
