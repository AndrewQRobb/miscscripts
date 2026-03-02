import os
import shutil
import exifread

# Set the root path to scan for images (defaults to current working directory)
root_path = os.getcwd()

def move_to_date_folder(image_path):
  # open image file and read exif data
  with open(image_path, 'rb') as f:
    exif_data = exifread.process_file(f)
  # extract date taken from exif data
  date_taken = exif_data.get('EXIF DateTimeOriginal', None)
  # if exif data does not contain date taken, return
  if date_taken is None:
    return
  # extract year, month, and day from date taken
  # EXIF format is "YYYY:MM:DD HH:MM:SS" — split on space first, then colon
  date_str = str(date_taken.values).split(' ')[0]
  year, month, day = date_str.split(':')
  # create destination folder path
  folder_path = os.path.join(root_path, year, month, day)
  # create destination folder if it does not exist
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  # move image to destination folder
  shutil.move(image_path, folder_path)

# search for image files in root path
for root, dirs, files in os.walk(root_path):
  for file in files:
    # check if file is an image
    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.raw', '.cr2', '.tiff', '.crw', '.nef')):
      # move image to date folder
      move_to_date_folder(os.path.join(root, file))

print("Script complete.")
