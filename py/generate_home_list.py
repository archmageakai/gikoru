import os
from datetime import datetime

def ensure_five_lines(url_list, posts_per_page=5):
    """
    Ensure that there are exactly 5 lines on the page by adding empty lines (breaks) if necessary.
    """
    while len(url_list) < posts_per_page:
        url_list.append('<br>\n')  # Add an empty line (break) to ensure 5 lines
    return url_list

def generate_paginated_url_list(workfiles_dir, output_dir, posts_per_page=5):
    """
    Generate paginated HTML pages with sorted URL links based on the contents of files in a directory.
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
                            # Line 2 contains the date in RFC3339 format
                            date_str = lines[1].strip()
                            date = datetime.fromisoformat(date_str)

                            # Line 3 contains the link text
                            link_text = lines[2].strip()
                            url = f"/posts/{filename}"

                            # Append the tuple (date, link) for sorting later
                            url_list.append((date, f'- <a href="{url}">{link_text}</a><br>\n'))
                        except ValueError:
                            print(f"Warning: {filename} has an invalid date format in line 2 and will be skipped.")
                    else:
                        print(f"Warning: {filename} does not have enough lines and will be skipped.")

        # Sort the list by date (newest first)
        url_list.sort(key=lambda x: x[0], reverse=True)

        # Generate paginated HTML files
        total_urls = len(url_list)
        if total_urls <= posts_per_page:
            page_file = os.path.join(output_dir, "index.html")
            with open(page_file, 'w', encoding='utf-8') as outfile:
                outfile.write('<main>\n')
                page_links = [url for _, url in url_list]
                page_links = ensure_five_lines(page_links, posts_per_page)
                for link in page_links:
                    outfile.write(link)
                outfile.write('</main>\n')
            print(f"Generated {page_file} successfully with {total_urls} URL(s).")
        else:
            total_pages = (total_urls + posts_per_page - 1) // posts_per_page
            for page in range(1, total_pages + 1):
                page_file = os.path.join(output_dir, "index.html" if page == 1 else f"pg{page}.html")
                with open(page_file, 'w', encoding='utf-8') as outfile:
                    outfile.write('<main>\n')
                    start_index = (page - 1) * posts_per_page
                    end_index = start_index + posts_per_page
                    page_links = [url for _, url in url_list[start_index:end_index]]
                    page_links = ensure_five_lines(page_links, posts_per_page)
                    for link in page_links:
                        outfile.write(link)
                    
                    # Pagination section
                    outfile.write('<div class="pagination">\n')
                    pagination_lines = [
                        ' '.join(
                            f'[{"%02d" % p}]' if p == page else f'<a href="{"index.html" if p == 1 else f"pg{p}.html"}">[{"%02d" % p}]</a>'
                            for p in range(i, min(i + 5, total_pages + 1))
                        )
                        for i in range(1, total_pages + 1, 5)
                    ]
                    outfile.write('<br>\n'.join(pagination_lines))
                    outfile.write('\n</div>\n')
                    outfile.write('</main>\n')
            print(f"Paginated URL list generated successfully in {output_dir}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    workfiles_directory = os.path.expanduser("~/gikoru/posts/")
    output_directory = os.path.expanduser("~/gikoru/pg/index")
    generate_paginated_url_list(workfiles_directory, output_directory)
