# Miscellaneous Utility Scripts

Collection of Python and Bash scripts for household automation tasks.

## Scripts

### Python Scripts (requires: `pip install exifread requests beautifulsoup4`)

- **Picture_Foldering.py** - Organize photos by year using EXIF metadata (⚠️ moves files)
- **Picture_Foldering2.py** - Enhanced photo organizer
- **reddit_scrape.py** - Download images from Reddit user submissions
- **reddit_scrape2.py** - Enhanced Reddit scraper with pagination

### Bash Scripts

- **verify_backup.sh** - Verify backup integrity with SHA-1 hash comparison (⚠️ very slow)

## Quick Start

```bash
# Install Python dependencies
pip install exifread requests beautifulsoup4

# Organize photos by year
python Picture_Foldering.py  # Edit script first: set root_path

# Scrape Reddit user images
python reddit_scrape.py      # Edit script first: set username

# Verify backup
./verify_backup.sh           # Edit script first: set source/dest paths
```

⚠️ **Warning:** Scripts have hardcoded paths - customize before running. Some operations are destructive.

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed usage instructions, configuration, workflows, and safety warnings.
