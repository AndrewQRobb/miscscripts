import os
import shutil
import exifread

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
  year, month, day = date_taken.values.split(':')[:3]
  # create destination folder path
  folder_path = f"{year}/{month}/{day}"
  # create destination folder if it does not exist
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  # move image to destination folder
  shutil.move(image_path, folder_path)

# search for image files in given folder
for root, dirs, files in os.walk(folder_path):
  for file in files:
    # check if file is an image
    if file.endswith(('.jpg', '.png', '.gif', '.bmp')):
      # move image to date folder
      move_to_date_folder(os.path.join(root, file))

print("Script complete.")
