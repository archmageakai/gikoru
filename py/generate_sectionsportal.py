import os
import re

def sanitize_directory_name(title):
    """
    Convert a title string into a valid folder name by replacing invalid characters with numbers.
    """
    char_map = {
        '?': '1', '>': '2', '<': '3', ':': '4', '"': '5',
        '/': '6', '\\': '7', '|': '8', '*': '9', ' ': '_'
    }
    sanitized = ''.join(char_map.get(char, char) for char in title)
    sanitized = re.sub(r"[^\w\d\-_']", lambda match: str(ord(match.group(0))), sanitized)
    return sanitized.lower()

def extract_text_from_line(line):
    """
    Remove HTML tags from a line of text.
    """
    return re.sub(r'<[^>]*>', '', line).strip()

def generate_sections_portal(sections_dir, output_file, posts_per_page=10):
    """
    Generate a portal index.html file that links to each section directory and handles pagination.
    """
    try:
        if not os.path.exists(sections_dir):
            print(f"Error: Directory {sections_dir} does not exist.")
            return

        links = []

        # Loop through each section folder
        for section_folder in os.listdir(sections_dir):
            section_path = os.path.join(sections_dir, section_folder)
            index_file_path = os.path.join(section_path, "index.html")

            if os.path.isdir(section_path) and os.path.exists(index_file_path):
                # Read the second line from the index.html file
                with open(index_file_path, 'r', encoding='utf-8') as index_file:
                    lines = index_file.readlines()

                if len(lines) >= 2:
                    line_2 = lines[2].strip()
                    text_content = extract_text_from_line(line_2)

                    # Generate a sanitized folder name for the link
                    sanitized_name = sanitize_directory_name(section_folder)

                    # Generate a link for the section
                    link = f'<div class="blog_item">- <a href="/sections/{sanitized_name}/">{text_content}</a></div>'
                    links.append(link)

        # Alphabetize the links list
        links.sort()

        # If there are more than the post limit, paginate
        total_links = len(links)
        total_pages = (total_links + posts_per_page - 1) // posts_per_page

        for page in range(1, total_pages + 1):
            # Determine the file name for the current page
            page_file_path = output_file if page == 1 else os.path.join(sections_dir, f"pg{page}.html")

            # Calculate the start and end index for the current page
            start_index = (page - 1) * posts_per_page
            end_index = start_index + posts_per_page
            page_links = links[start_index:end_index]

            # Ensure there are exactly `posts_per_page` lines
            while len(page_links) < posts_per_page:
                page_links.append('<br>\n')

            # Write the page content
            with open(page_file_path, 'w', encoding='utf-8') as page_file:
                page_file.write('<main>\n')

                page_file.write('♡ <br>\n<strong>Sections</strong>\n ✧*｡٩(－ω－*)و✧*｡<br><img src=\"/image/wiz.png\"</img><br>\n\n')

                page_file.write('<div class="blog-list">\n')

                # Write the links for the current page
                for link in page_links:
                    page_file.write(f'{link}\n')

                # Add pagination navigation with sliding window
                if total_pages > 1:
                    page_file.write('<div class="pagination">\n')

                    # Navigation arrows - L
                    if page > 1:
                        prev_page = "index.html" if page - 1 == 1 else f"pg{page - 1}.html"

                        if page > 2:
                            page_file.write(f'<a href="index.html">[&laquo;]</a> ')
                        
                        page_file.write(f'<a href="{prev_page}">[&lsaquo;]</a> ')
                    else:
                        page_file.write('') #[&laquo;] [&lsaquo;] ---> blank

                    # Sliding window logic for page numbers
                    if total_pages <= 5:
                        block_start = 1
                        block_end = total_pages
                    else:
                        if page <= 3:
                            block_start = 1
                            block_end = 5
                        elif page >= total_pages - 2:
                            block_start = total_pages - 4
                            block_end = total_pages
                        else:
                            block_start = page - 2
                            block_end = page + 2

                    # Render the page number links
                    for p in range(block_start, block_end + 1):
                        if p == page:
                            page_file.write(f'[{p:02d}] ')
                        else:
                            page_url = "index.html" if p == 1 else f"pg{p}.html"
                            page_file.write(f'<a href="{page_url}">[{p:02d}]</a> ')

                    """
                    #Experimental
                    # blanks
                    if total_pages < 5:
                        for _ in range(5 - total_pages):
                            page_file.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                    """

                    # Navigation arrows - R
                    if page < total_pages:
                        next_page = f"pg{page + 1}.html"
                        page_file.write(f'<a href="{next_page}">[&rsaquo;]</a> ')

                        if page + 1 < total_pages:
                            last_page = f"pg{total_pages}.html"
                            page_file.write(f'<a href="{last_page}">[&raquo;]</a>')
                    else:
                        page_file.write('[&rsaquo;] [&raquo;]')

                    page_file.write('</div>\n')
                else:
                    page_file.write('<br>')

                page_file.write('</main>\n')

            print(f"Generated page {page_file_path} with {len(page_links)} links")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Directory containing the section folders
    sections_directory = os.path.expanduser("~/gikoru/pg/sections/")
    # Path to the output index.html file
    output_path = os.path.join(sections_directory, "index.html")

    print("Generating sections portal...")
    generate_sections_portal(sections_directory, output_path)