import os

def merge_html_files(input_files, output_file):
    """
    Merge multiple HTML files into a single file.

    Args:
        input_files (list): List of file paths to merge.
        output_file (str): Path to the output file.
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_path in input_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')  # Add a newline for separation
                else:
                    print(f"Warning: File {file_path} does not exist and will be skipped.")

        print(f"HTML files merged successfully into {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_pg_html_files(directory):
    """
    Get all HTML files starting with 'pg' (e.g., pg1.html, pg2.html) in the given directory.

    Args:
        directory (str): Path to the directory to scan.

    Returns:
        list: List of HTML file paths (pg*.html).
    """
    pg_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and file.endswith('.html') and file.startswith('pg'):
            pg_files.append(file_path)
    return pg_files

if __name__ == "__main__":
    # Paths to the input files for the common merge (head, header, footer)
    head_file = os.path.expanduser("~/site/pg/head.html")
    header_file = os.path.expanduser("~/site/pg/header.html")
    footer_file = os.path.expanduser("~/site/pg/footer.html")

    # Path to the output directory
    output_dir = os.path.expanduser("~/site/public/sections/")

    # Get all pg*.html files in the sections directory
    sections_directory = os.path.expanduser("~/site/pg/sections/")
    pg_html_files = get_pg_html_files(sections_directory)

    # Merge index.html separately first
    index_file = os.path.expanduser("~/site/pg/sections/index.html")
    output_file_for_index = os.path.join(output_dir, "index.html")

    # Merge head.html, header.html, and index.html
    print(f"Merging index.html with head.html and header.html into {output_file_for_index}...")
    merge_html_files([head_file, header_file, index_file], output_file_for_index)

    # Now, merge each pg*.html file with head.html and header.html
    for pg_file in pg_html_files:
        output_file_for_pg = os.path.join(output_dir, os.path.basename(pg_file))

        # Merge head.html, header.html, current pg*.html file (without footer yet)
        print(f"Merging {pg_file} with head.html, header.html into {output_file_for_pg}...")
        merge_html_files([head_file, header_file, pg_file], output_file_for_pg)

    # Now, add the footer to each merged file (only once)
    for pg_file in pg_html_files:
        output_file_for_pg = os.path.join(output_dir, os.path.basename(pg_file))

        # Append the footer to the merged file
        with open(output_file_for_pg, 'a', encoding='utf-8') as outfile:
            if os.path.exists(footer_file):
                with open(footer_file, 'r', encoding='utf-8') as footer:
                    outfile.write(footer.read())
                    outfile.write('\n')  # Add a newline after footer
            else:
                print(f"Warning: Footer file {footer_file} does not exist.")
        
        print(f"Added footer to {output_file_for_pg}")

    # Finally, add the footer to the index.html
    with open(output_file_for_index, 'a', encoding='utf-8') as outfile:
        if os.path.exists(footer_file):
            with open(footer_file, 'r', encoding='utf-8') as footer:
                outfile.write(footer.read())
                outfile.write('\n')  # Add a newline after footer
        else:
            print(f"Warning: Footer file {footer_file} does not exist.")
    
    print(f"Added footer to {output_file_for_index}")
