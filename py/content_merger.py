import os

def merge_individual_file(input_file, output_file, head_file, header_file, footer_file):
    """
    Merge an individual HTML file with head, header, and footer files.

    Args:
        input_file (str): Path to the individual HTML file.
        output_file (str): Path to the output file.
        head_file (str): Path to the head HTML file.
        header_file (str): Path to the header HTML file.
        footer_file (str): Path to the footer HTML file.
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write head file
            if os.path.exists(head_file):
                with open(head_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')

            # Write header file
            if os.path.exists(header_file):
                with open(header_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')

            # Write the individual file
            if os.path.exists(input_file):
                with open(input_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')

            # Write footer file
            if os.path.exists(footer_file):
                with open(footer_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')

        print(f"Merged {input_file} into {output_file}")
    except Exception as e:
        print(f"An error occurred while merging {input_file}: {e}")

def merge_all_files(input_directory, output_directory, head_file, header_file, footer_file):
    """
    Merge all HTML files in the input directory with head, header, and footer files.

    Args:
        input_directory (str): Directory containing individual HTML files.
        output_directory (str): Directory to save the merged files.
        head_file (str): Path to the head HTML file.
        header_file (str): Path to the header HTML file.
        footer_file (str): Path to the footer HTML file.
    """
    try:
        # Ensure the output directory exists and clear it
        if os.path.exists(output_directory):
            for file_name in os.listdir(output_directory):
                file_path = os.path.join(output_directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(output_directory)

        # Merge each file in the input directory
        for filename in sorted(os.listdir(input_directory)):
            input_file = os.path.join(input_directory, filename)
            if os.path.isfile(input_file) and filename.endswith(".html"):
                output_file = os.path.join(output_directory, filename)
                merge_individual_file(input_file, output_file, head_file, header_file, footer_file)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Input directory containing individual HTML files
    posts_directory = os.path.expanduser("~/site/pg/posts/")

    # Output directory for merged files
    output_directory = os.path.expanduser("~/site/public/posts/")

    # Paths to the head, header, and footer HTML files
    head_file = os.path.expanduser("~/site/pg/head.html")
    header_file = os.path.expanduser("~/site/pg/header.html")
    footer_file = os.path.expanduser("~/site/pg/footer.html")

    print("Merging individual files with head, header, and footer...")
    merge_all_files(posts_directory, output_directory, head_file, header_file, footer_file)
