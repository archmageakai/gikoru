import os
import zipfile
import shutil
import subprocess

def zip_directory(source_dir, zip_filename):
    """
    Zip the contents of a directory, but not the directory itself.

    Args:
        source_dir (str): The directory to zip.
        zip_filename (str): The name of the zip file to create.
    """
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    # Get the relative path of the file, excluding the source_dir
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)  # Remove the source_dir from the file path
                    zipf.write(file_path, arcname)
        print(f"Contents of {source_dir} have been zipped into {zip_filename}.")
    except Exception as e:
        print(f"Error while zipping: {e}")

def move_zip_file(zip_filename, destination_dir):
    """
    Move the zip file to a specified directory.

    Args:
        zip_filename (str): The zip file to move.
        destination_dir (str): The destination directory.
    """
    try:
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        shutil.move(zip_filename, os.path.join(destination_dir, os.path.basename(zip_filename)))
        print(f"Moved {zip_filename} to {destination_dir}.")
    except Exception as e:
        print(f"Error while moving the zip file: {e}")

def run_scp(zip_filename, remote_path):
    """
    Run the SCP command to transfer the zip file to a remote server.

    Args:
        zip_filename (str): The zip file to transfer.
        remote_path (str): The remote path for the SCP command.
    """
    try:
        scp_command = ["scp", "-i", os.path.expanduser("~/.ssh/id_rsa"), zip_filename, remote_path]
        subprocess.run(scp_command, check=True)
        print(f"Successfully transferred {zip_filename} to {remote_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error while transferring the file: {e}")

def deploy():
    """
    Main function to zip, move, and transfer the zip file.
    """
    source_dir = os.path.expanduser("~/site/public/")  # Directory to zip
    zip_filename = os.path.expanduser("~/deploy/deploy.zip")  # Name of the zip file
    destination_dir = os.path.expanduser("~/deploy/")  # Directory to move the zip file to
    remote_path = "akai@gikopoi.com:~/www/"  # Remote server path

    # Zip the directory
    zip_directory(source_dir, zip_filename)

    # Move the zip file to the ~/deploy/ directory
    move_zip_file(zip_filename, destination_dir)

    # Run the SCP command to transfer the zip file to the remote server
    run_scp(os.path.join(destination_dir, "deploy.zip"), remote_path)

if __name__ == "__main__":
    deploy()
