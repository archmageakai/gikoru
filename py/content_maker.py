import os
import shutil

def clear_output_directory(output_directory):
    """
    Clears all files in the specified output directory.

    Args:
        output_directory (str): Path to the directory to be cleared.
    """
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

def modify_html_files(input_directory, output_directory):
    """
    Modify HTML files as per the requirements:
    - Delete LINE 1, LINE 3, LINE 4, and LINE 5.
    - Wrap LINE 3 in <h1> tags and place it in LINE 1.
    - Wrap LINE 2 in <time> tags and place it in LINE 2.
    - Append a modified <div> block to the end of the file based on LINE 4 with formatted URL.
    - Wrap the entire content in <main> tags.
    - Convert uppercase characters in LINE 4 to lowercase for the URL.

    Args:
        input_directory (str): Path to the directory containing original HTML files.
        output_directory (str): Path to the directory to save modified HTML files.
    """
    # Character map for URL replacements
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

    # Clear the output directory
    clear_output_directory(output_directory)

    try:
        # Loop through each HTML file in the input directory
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()

                # Ensure the file has at least 5 lines to process
                if len(lines) < 5:
                    print(f"Warning: {filename} does not have enough lines and will be skipped.")
                    continue

                # Extract the necessary lines
                line_3 = lines[2].strip()  # Original LINE 3
                line_2 = lines[1].strip()  # Original LINE 2
                line_4 = lines[3].strip()  # Original LINE 4

                # Wrap LINE 3 in <h1> tags and place it in LINE 1
                new_line_1 = f"<h1>{line_3}</h1>\n"

                # Wrap LINE 2 in <time> tags and place it in LINE 2
                new_line_2 = f"<time>{line_2}</time>\n"

                # Modify LINE 4 for the URL: Replace special characters and convert to lowercase
                modified_line_4 = "".join(char_map.get(char, char) for char in line_4).lower()

                # Create the new <div> block based on LINE 4
                new_div_block = f"""
<div>
    <div>:</div>
    <ul>
        <li><a href="/sections/{modified_line_4}/">{line_4}</a></li> 
    </ul>
</div>
"""

                # Combine the modified content:
                # 1. Add new Line 1 and Line 2.
                # 2. Include remaining lines except original Lines 3, 4, and 5.
                # 3. Append the new <div> block.
                modified_content = [new_line_1, new_line_2] + lines[5:] + [new_div_block]

                # Wrap the entire content in <main> tags
                wrapped_content = ["<main>\n"] + modified_content + ["</main>\n"]

                # Save the modified file to the output directory
                output_file = os.path.join(output_directory, filename)
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(wrapped_content)

                print(f"Processed and saved: {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Directory containing the original HTML files
    input_directory = os.path.expanduser("~/site/posts")

    # Directory to save the modified HTML files
    output_directory = os.path.expanduser("~/site/pg/posts")

    print("Clearing output directory and modifying HTML files...")
    modify_html_files(input_directory, output_directory)
