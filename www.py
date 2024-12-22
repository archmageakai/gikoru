import os
import shutil

# Define source and destination directories
source_dir = os.path.expanduser('~/gikoru/public/')
destination_dir = os.path.expanduser('~/www/')

# Check if the source directory exists
if not os.path.exists(source_dir):
    print(f"Source directory {source_dir} does not exist.")
else:
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Loop through all files and folders in the source directory
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        destination_item = os.path.join(destination_dir, item)

        # If it's a directory, copy the entire directory and its contents
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
            print(f"Copied directory: {source_item} to {destination_item}")
        # If it's a file, copy the file
        elif os.path.isfile(source_item):
            shutil.copy2(source_item, destination_item)  # copy2 preserves metadata like timestamps
            print(f"Copied file: {source_item} to {destination_item}")
        else:
            print(f"Skipped: {source_item} (not a file or directory)")

    print("File and folder transfer complete.")
