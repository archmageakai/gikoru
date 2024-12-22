import os

def merge_html_files(input_files, output_file, news_file):
    """
    Merge multiple HTML files into a single file and insert the content of news.html after the <main> tag.

    Args:
        input_files (list): List of file paths to merge.
        output_file (str): Path to the output file.
        news_file (str): Path to the news.html file to insert after the <main> tag.
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_path in input_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()

                        # Check if the current file is the one to insert news.html after
                        if "<main>" in content and os.path.exists(news_file):
                            # Insert news.html content right after the <main> tag
                            parts = content.split("<main>", 1)
                            with open(news_file, 'r', encoding='utf-8') as news_infile:
                                news_content = news_infile.read()
                            content = f"{parts[0]}<main>\n{news_content}\n{parts[1]}"

                        outfile.write(content)
                        outfile.write('\n')  # Add a newline for separation
                else:
                    print(f"Warning: File {file_path} does not exist and will be skipped.")

        print(f"HTML files merged successfully into {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def merge_individual_files(input_directory, output_directory, news_file):
    """
    Merge individual HTML files from the specified directory with the common files
    and insert news.html after the <main> tag.

    Args:
        input_directory (str): Path to the directory containing individual HTML files.
        output_directory (str): Path to the output directory for merged files.
        news_file (str): Path to the news.html file.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Paths to the common HTML files
        common_files = [
            os.path.expanduser("~/site/pg/head.html"),
            os.path.expanduser("~/site/pg/header.html")
        ]
        footer_file = os.path.expanduser("~/site/pg/footer.html")

        # Loop through each individual HTML file in the input directory
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)
            if os.path.isfile(file_path) and filename.endswith(".html") and filename != "individualfile.html":
                output_file = os.path.join(output_directory, filename)

                # Combine the common files with the individual HTML file, placing footer last
                input_files = common_files + [file_path] + [footer_file]
                merge_html_files(input_files, output_file, news_file)

                print(f"Merged {filename} into {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Directory containing the individual HTML files
    input_directory = os.path.expanduser("~/site/pg/index")

    # Output directory for merged files
    output_directory = os.path.expanduser("~/site/public")

    # Path to the news.html file
    news_file = os.path.expanduser("~/site/pg/news.html")

    print("Merging individual HTML files with news.html insertion...")
    merge_individual_files(input_directory, output_directory, news_file)
