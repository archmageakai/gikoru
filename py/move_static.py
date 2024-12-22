import os
import shutil

def copy_static_to_public(static_dir, public_dir):
    """
    Copy all files and folders from the static directory to the public directory.

    Args:
        static_dir (str): Path to the static directory (source).
        public_dir (str): Path to the public directory (destination).
    """
    try:
        # Expand user paths
        static_dir = os.path.expanduser(static_dir)
        public_dir = os.path.expanduser(public_dir)

        # Ensure the source directory exists
        if not os.path.exists(static_dir):
            print(f"Source directory {static_dir} does not exist.")
            return

        # Ensure the destination directory exists
        os.makedirs(public_dir, exist_ok=True)

        # Copy files and directories
        for item in os.listdir(static_dir):
            source_path = os.path.join(static_dir, item)
            destination_path = os.path.join(public_dir, item)

            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                print(f"Copied directory: {source_path} -> {destination_path}")
            elif os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)
                print(f"Copied file: {source_path} -> {destination_path}")

        print(f"All contents from {static_dir} have been copied to {public_dir}.")
    except Exception as e:
        print(f"An error occurred while copying files: {e}")

if __name__ == "__main__":
    # Source and destination directories
    static_directory = "~/site/static/"
    public_directory = "~/site/public/"

    print(f"Copying contents from {static_directory} to {public_directory}...")
    copy_static_to_public(static_directory, public_directory)
