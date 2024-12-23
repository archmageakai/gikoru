import os
from datetime import datetime

def ensure_five_lines(url_list, posts_per_page=5):
    """
    Ensure that there are exactly 5 lines on the page by adding empty lines (breaks) if necessary.

    Args:
        url_list (list): List of URL links to be written on the page.
        posts_per_page (int): Number of posts per page (default is 5).
    
    Returns:
        list: The list of URL links padded to ensure 5 lines with breaks.
    """
    while len(url_list) < posts_per_page:
        url_list.append('<br>\n')  # Add an empty line (break) to ensure 5 lines
    return url_list

def generate_paginated_url_list(workfiles_dir, output_dir, posts_per_page=5):
    """
    Generate paginated HTML pages with sorted URL links based on the contents of files in a directory.

    Args:
        workfiles_dir (str): Path to the directory containing the work files.
        output_dir (str): Path to the output directory for the HTML pages.
        posts_per_page (int): Number of posts per page.
    """
    url_list = []

    try:
        # Ensure the directory exists
        if not os.path.exists(workfiles_dir):
            print(f"Error: Directory {workfiles_dir} does not exist.")
            return

        # Clear the output directory
        if os.path.exists(output_dir):
            for file_name in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(output_dir)

        # Read all files in the directory
        for filename in os.listdir(workfiles_dir):
            file_path = os.path.join(workfiles_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                    # Ensure the file has enough lines
                    if len(lines) >= 3:
                        try:
                            # Line 2 contains the date in RFC3339 format (e.g., '2024-11-25T01:26:49-05:00')
                            date_str = lines[1].strip()  # Date in line 2
                            date = datetime.fromisoformat(date_str)  # Parse the RFC3339 date

                            # Line 3 contains the link text (Title)
                            link_text = lines[2].strip()  # Title in line 3
                            url = f"/posts/{filename}"

                            # Append the tuple (date, link) for sorting later
                            url_list.append((date, f'- <a href="{url}">{link_text}</a><br>\n'))  # Add <br> after each URL
                        except ValueError:
                            print(f"Warning: {filename} has an invalid date format in line 2 and will be skipped.")
                    else:
                        print(f"Warning: {filename} does not have enough lines and will be skipped.")

        # Sort the list by date (newest first)
        url_list.sort(key=lambda x: x[0], reverse=True)

        # If there are 5 or fewer URLs, don't create pagination
        total_urls = len(url_list)
        if total_urls <= posts_per_page:
            page_file = os.path.join(output_dir, "index.html")
            with open(page_file, 'w', encoding='utf-8') as outfile:
                outfile.write('<main>\n')  # Start the <main> tag
                page_links = [url for _, url in url_list]
                page_links = ensure_five_lines(page_links, posts_per_page)
                for link in page_links:
                    outfile.write(link)
                outfile.write('</main>\n')  # Close the <main> tag
            print(f"Generated {page_file} successfully with {total_urls} URL(s).")
        else:
            total_pages = (total_urls + posts_per_page - 1) // posts_per_page
            for page in range(1, total_pages + 1):
                page_file = os.path.join(output_dir, "index.html" if page == 1 else f"pg{page}.html")
                with open(page_file, 'w', encoding='utf-8') as outfile:
                    outfile.write('<main>\n')  # Start the <main> tag
                    start_index = (page - 1) * posts_per_page
                    end_index = start_index + posts_per_page
                    page_links = [url for _, url in url_list[start_index:end_index]]
                    page_links = ensure_five_lines(page_links, posts_per_page)
                    for link in page_links:
                        outfile.write(link)
                    outfile.write('<div class="pagination">\n')
                    for p in range(1, total_pages + 1):
                        if p == page:
                            outfile.write(f'[{p}] ')
                        else:
                            link = "index.html" if p == 1 else f"pg{p}.html"
                            outfile.write(f'<a href="{link}">[{p}]</a> ')
                    outfile.write('\n</div>\n')
                    outfile.write('</main>\n')  # Close the <main> tag
            print(f"Paginated URL list generated successfully in {output_dir}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    workfiles_directory = os.path.expanduser("~/gikoru/posts/")
    output_directory = os.path.expanduser("~/gikoru/pg/index")
    generate_paginated_url_list(workfiles_directory, output_directory)
