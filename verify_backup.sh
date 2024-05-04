#!/bin/bash

SOURCE_DIR="/Volumes/Backblaze_MacEx4TB32540642"
DEST_DIR="/Volumes/My Passport Mac 4TB"

# Count total files for progress calculation, excluding certain system directories
total_files=$(find "$SOURCE_DIR" -type f -not -path '*/.Spotlight-V100/*' -not -path '*/.fseventsd/*' -not -path '*/.Trashes/*' | wc -l)
current_file=0

# Function to display progress
display_progress() {
    percent=$(awk "BEGIN {printf \"%.2f\", ($current_file/$total_files)*100}")
    echo -ne "Progress: $current_file/$total_files ($percent%)\r"
}

# Find all files in the source directory, excluding certain system directories, calculate their SHA-1 hash, and compare it with the destination file's hash.
find "$SOURCE_DIR" -type f -not -path '*/.Spotlight-V100/*' -not -path '*/.fseventsd/*' -not -path '*/.Trashes/*' -print0 | while IFS= read -r -d '' file; do
    current_file=$((current_file+1))
    display_progress

    # Get relative path
    relative_path="${file#$SOURCE_DIR}"

    # Compute hashes
    src_hash=$(shasum "$file" | awk '{print $1}')
    dest_hash=$(shasum "$DEST_DIR$relative_path" 2>/dev/null | awk '{print $1}')

    # Compare hashes
    if [ "$src_hash" != "$dest_hash" ]; then
        echo "Mismatch found: $relative_path"
    fi
done

echo "Verification Complete."
