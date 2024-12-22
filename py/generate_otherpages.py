import os

def merge_pages_with_template(pages_dir, output_dir, head_file, header_file, footer_file):
    """
    Merges each HTML file in the pages directory with the template files (head, header, footer).

    Args:
        pages_dir (str): Path to the directory containing the HTML pages.
        output_dir (str): Path to the output directory for merged files.
        head_file (str): Path to the head.html file.
        header_file (str): Path to the header.html file.
        footer_file (str): Path to the footer.html file.
    """
    try:
        # Ensure the output directory exists (but don't delete any files)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Check if template files exist
        for template_file in [head_file, header_file, footer_file]:
            if not os.path.exists(template_file):
                print(f"Error: Template file {template_file} does not exist.")
                return

        # Process each HTML file in the $$$pages directory
        for filename in os.listdir(pages_dir):
            file_path = os.path.join(pages_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                output_file = os.path.join(output_dir, filename)

                # Merge the template files with the current HTML file
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    # Write head.html
                    with open(head_file, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')

                    # Write header.html
                    with open(header_file, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')

                    # Write the current HTML file
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')

                    # Write footer.html
                    with open(footer_file, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')

                print(f"Merged {filename} into {output_file}")

        print("All files merged successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define paths
    pages_directory = os.path.expanduser("~/gikoru/pg/$$$pages/")  # Update this if needed
    output_directory = os.path.expanduser("~/gikoru/public/")  # Update this if needed
    head_file_path = os.path.expanduser("~/gikoru/pg/head.html")
    header_file_path = os.path.expanduser("~/gikoru/pg/header.html")
    footer_file_path = os.path.expanduser("~/gikoru/pg/footer.html")

    # Merge the pages with the template
    merge_pages_with_template(pages_directory, output_directory, head_file_path, header_file_path, footer_file_path)
