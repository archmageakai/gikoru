import os
from datetime import datetime

def generate_paginated_url_list(workfiles_dir, output_dir, posts_per_page=10):
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
                            url_list.append((date, f'<div class="blog_item">- <a href="{url}">{link_text}</a></div>\n'))
                        except ValueError:
                            print(f"Warning: {filename} has an invalid date format in line 2 and will be skipped.")
                    else:
                        print(f"Warning: {filename} does not have enough lines and will be skipped.")

        # Sort the list by date (newest first)
        url_list.sort(key=lambda x: x[0], reverse=True)

        # Generate paginated HTML files
        total_urls = len(url_list)
        total_pages = (total_urls + posts_per_page - 1) // posts_per_page

        for page in range(1, total_pages + 1):
            page_file = os.path.join(output_dir, "index.html" if page == 1 else f"pg{page}.html")
            with open(page_file, 'w', encoding='utf-8') as outfile:
                # Open the main tag and wrap content inside <div class="blog-list">
                outfile.write('<main>\n')
                outfile.write('<div class="blog-list">\n')  # Add <div class="blog-list">
                
                start_index = (page - 1) * posts_per_page
                end_index = start_index + posts_per_page
                page_links = [url for _, url in url_list[start_index:end_index]]

                # Ensure exactly 5 lines per page
                while len(page_links) < posts_per_page:
                    page_links.append('<br>\n')

                for link in page_links:
                    outfile.write(link)

                # Close the blog-list div
                outfile.write('</div>\n')  # Close <div class="blog-list">

                # Pagination section
                if total_pages > 1:
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

                # If there is only one page (no pagination), add an extra <br>
                if total_pages == 1:
                    outfile.write('<br>\n')

                outfile.write('</main>\n')

        print(f"Paginated URL list generated successfully in {output_dir}.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    workfiles_directory = os.path.expanduser("~/gikoru/posts/")
    output_directory = os.path.expanduser("~/gikoru/pg/index")
    generate_paginated_url_list(workfiles_directory, output_directory)