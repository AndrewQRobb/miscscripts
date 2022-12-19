import os
import exifread
import shutil

# Set the path to the root folder containing the images
root_path = '/path/to/image/folder'

# Iterate through all the files in the root folder and its subdirectories
for root, dirs, files in os.walk(root_path):
  for file in files:
    # Check if the file is an image file
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif') or file.endswith('.jpeg') or file.endswith('.raw') or file.endswith('.cr2') or file.endswith('.tiff') or file.endswith('.crw') or file.endswith('.nef'):
      # Open the image file
      with open(os.path.join(root, file), 'rb') as f:
        # Extract the EXIF metadata
        tags = exifread.process_file(f)
        # Check if the "DateTimeOriginal" tag is present in the metadata
        if 'EXIF DateTimeOriginal' in tags:
          # Get the value of the "DateTimeOriginal" tag and extract the year
          year = tags['EXIF DateTimeOriginal'].values[:4]
          # Create a new folder for the year, if it doesn't already exist
          year_folder = os.path.join(root, year)
          if not os.path.exists(year_folder):
            os.makedirs(year_folder)
          # Move the image file to the year folder
          shutil.move(os.path.join(root, file), os.path.join(year_folder, file))

#This script uses the exifread library to extract EXIF metadata from the image files, and the shutil library to move the files into the appropriate year folders.
#To use this script, simply replace '/path/to/image/folder' with the actual path to the root folder containing the images, and run the script. 
#It will search the root folder and all its subdirectories for image files, extract the EXIF metadata from the images, and move the images into folders labeled by the year the photo was taken.
