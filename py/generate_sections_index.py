import os

def combine_html_files(base_files, page_file, output_file):
    """
    Combine base HTML files with a page-specific HTML file.

    Args:
        base_files (list): List of base HTML files to combine (e.g., head, header, footer).
        page_file (str): Path of the page-specific HTML file.
        output_file (str): Path of the final combined HTML file.
    """
    try:
        # Ensure the directory for the output file exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write the head and header files first
            for base_file in base_files[:-1]:  # Exclude the footer for now
                if os.path.exists(base_file):
                    with open(base_file, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')
                else:
                    print(f"Warning: {base_file} does not exist and will be skipped.")

            # Write the page-specific content
            if os.path.exists(page_file):
                with open(page_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')
            else:
                print(f"Warning: {page_file} does not exist and will be skipped.")

        print(f"Page {output_file} combined successfully.")
    except Exception as e:
        print(f"An error occurred while combining files: {e}")

def merge_html_files(sections_dir, base_files, output_dir):
    """
    Merge HTML files from sections directory with base files and output them to the respective directories.

    Args:
        sections_dir (str): Path to the directory containing section folders.
        base_files (list): List of base HTML files to combine with each page.
        output_dir (str): Path to the final output directory.
    """
    try:
        # Check if sections directory exists
        if not os.path.exists(sections_dir):
            print(f"Error: Directory {sections_dir} does not exist.")
            return

        # Loop through each section in the sections directory
        for section_folder in os.listdir(sections_dir):
            section_path = os.path.join(sections_dir, section_folder)

            if os.path.isdir(section_path):
                # Loop through each HTML file in the section folder
                for filename in os.listdir(section_path):
                    file_path = os.path.join(section_path, filename)

                    if os.path.isfile(file_path) and filename.endswith(".html"):
                        # Construct the output path
                        output_section_dir = os.path.join(output_dir, 'sections', section_folder)
                        os.makedirs(output_section_dir, exist_ok=True)

                        # Construct the output file path
                        output_file = os.path.join(output_section_dir, filename)

                        # Combine base files with the current page file and save it to the output directory
                        combine_html_files(base_files, file_path, output_file)

        # Append the footer to all files in the output directory
        footer_file = base_files[-1]  # The last file in base_files is the footer
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".html"):
                    output_file_path = os.path.join(root, file)
                    with open(output_file_path, 'a', encoding='utf-8') as outfile:
                        if os.path.exists(footer_file):
                            with open(footer_file, 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read())
                                outfile.write('\n')
                        else:
                            print(f"Warning: Footer file {footer_file} does not exist and will not be added.")

        print(f"All HTML files merged successfully in {output_dir}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Base HTML files to combine with each page
    base_html_files = [
        os.path.expanduser("~/gikoru/pg/head.html"),
        os.path.expanduser("~/gikoru/pg/header.html"),
        os.path.expanduser("~/gikoru/pg/footer.html")
    ]
    # Directory containing the section folders
    sections_directory = os.path.expanduser("~/gikoru/pg/sections/")
    # Output directory where merged HTML files will be saved
    output_directory = os.path.expanduser("~/gikoru/public/")

    print("Starting the script...")
    # Merge HTML files from the sections directory and save to the output directory
    merge_html_files(sections_directory, base_html_files, output_directory)
