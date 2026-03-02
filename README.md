# Miscellaneous Utility Scripts

Collection of Python and Bash scripts for household automation tasks.

## Scripts

### Python Scripts (requires: `pip install exifread requests`)

- **photo_organizer.py** - Organize photos by year/month/day using EXIF metadata (moves files)
- **reddit_scraper.py** - Download images from Reddit user submissions with pagination

### Bash Scripts

- **verify_backup.sh** - Verify backup integrity with SHA-1 hash comparison (very slow)

## Quick Start

```bash
# Install Python dependencies
pip install exifread requests

# Organize photos by date
cd /path/to/photos
python photo_organizer.py  # Uses current directory by default

# Scrape Reddit user images
python reddit_scraper.py   # Edit script first: set username

# Verify backup
./verify_backup.sh         # Edit script first: set source/dest paths
```

**Warning:** Scripts may have hardcoded paths - customize before running. Some operations are destructive (file moves).

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed usage instructions, configuration, workflows, and safety warnings.
