import os
import shutil

# Define source and destination directories
source_dir = os.path.expanduser('~/gikoru/public/')
destination_dir = os.path.expanduser('~/www/')

# Function to clear all files and directories in the destination directory
# but skip hidden directories like .git
def clear_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Skip hidden directories and files (those starting with a dot)
        if item.startswith('.'):
            print(f"Skipped hidden item: {item_path}")
            continue

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove directory and all its contents
            print(f"Removed directory: {item_path}")
        elif os.path.isfile(item_path):
            os.remove(item_path)  # Remove file
            print(f"Removed file: {item_path}")

# Check if the source directory exists
if not os.path.exists(source_dir):
    print(f"Source directory {source_dir} does not exist.")
else:
    # Clear the destination directory before copying new files, but skip .git
    if os.path.exists(destination_dir):
        clear_directory(destination_dir)
    else:
        os.makedirs(destination_dir)

    # Loop through all files and folders in the source directory
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        destination_item = os.path.join(destination_dir, item)

        # If it's a directory, copy the entire directory and its contents (overwrite)
        if os.path.isdir(source_item):
            # Use dirs_exist_ok=True to allow overwriting of existing directories
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
            print(f"Copied directory: {source_item} to {destination_item}")
        # If it's a file, copy the file (overwrite)
        elif os.path.isfile(source_item):
            shutil.copy2(source_item, destination_item)  # copy2 preserves metadata like timestamps
            print(f"Copied file: {source_item} to {destination_item}")
        else:
            print(f"Skipped: {source_item} (not a file or directory)")

    print("File and folder transfer complete.")
