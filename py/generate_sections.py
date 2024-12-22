import os
import re
import shutil

def sanitize_filename(title):
    """
    Convert a title string into a valid folder name by replacing invalid characters with numbers.

    Args:
        title (str): The title to sanitize.

    Returns:
        str: A sanitized folder name.
    """
    char_map = {
        '?': '1',
        '>': '2',
        '<': '3',
        ':': '4',
        '"': '5',
        '/': '6',
        '\\': '7',
        '|': '8',
        '*': '9',
        ' ': '_'
    }
    sanitized = ''.join(char_map.get(char, char) for char in title)
    sanitized = re.sub(r'[^\w\d_]', lambda match: str(ord(match.group(0))), sanitized)
    return sanitized.lower()

def clear_and_create_directory(directory):
    """
    Clear the contents of a directory and recreate it.

    Args:
        directory (str): The directory to clear and recreate.
    """
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                os.remove(os.path.join(root, file))  # Remove all files
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))  # Remove all subdirectories
    else:
        os.makedirs(directory)  # Create the directory if it doesn't exist

def generate_section_files(input_dir, output_dir):
    """
    Process HTML files in the input directory to generate new folders and index.html files in the output directory.

    Args:
        input_dir (str): Path to the directory containing the input HTML files.
        output_dir (str): Path to the directory for the output folders and files.
    """
    try:
        if not os.path.exists(input_dir):
            print(f"Error: Directory {input_dir} does not exist.")
            return

        # Clear and recreate the output directory
        clear_and_create_directory(output_dir)

        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()

                    if len(lines) >= 4:
                        original_title = lines[3].strip()  # Line 4 as title
                        sanitized_folder_name = sanitize_filename(original_title)
                        folder_path = os.path.join(output_dir, sanitized_folder_name)

                        # Create the folder
                        os.makedirs(folder_path, exist_ok=True)

                        # Write the index.html file with the title
                        index_file_path = os.path.join(folder_path, "index.html")
                        with open(index_file_path, 'w', encoding='utf-8') as outfile:
                            outfile.write(f"{original_title}\n")  # Title in line 1

                        print(f"Generated folder and file: {index_file_path}")
                    else:
                        print(f"Warning: {filename} does not have at least 4 lines and will be skipped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Input directory containing the original HTML files
    posts_directory = os.path.expanduser("~/gikoru/posts/")
    # Output directory for the new section folders and files
    sections_directory = os.path.expanduser("~/gikoru/pg/sections/")

    # Generate the section folders and files
    generate_section_files(posts_directory, sections_directory)
