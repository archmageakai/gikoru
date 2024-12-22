import os
import shutil

def clear_directory(directory_path):
    """
    Remove all files and subdirectories in the specified directory.

    Args:
        directory_path (str): Path to the directory to clear.
    """
    try:
        # Expand the user path and check if the directory exists
        directory_path = os.path.expanduser(directory_path)
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist. Nothing to clear.")
            return

        # Remove all contents in the directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")

        print(f"All contents in {directory_path} have been removed.")
    except Exception as e:
        print(f"An error occurred while clearing the directory: {e}")

if __name__ == "__main__":
    # Directory to clear
    target_directory = "~/site/public/"

    print(f"Clearing contents of {target_directory}...")
    clear_directory(target_directory)
