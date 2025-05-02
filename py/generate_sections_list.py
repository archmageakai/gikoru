import os
import re
from datetime import datetime

def sanitize_filename(title):
    """
    Convert a title string into a valid folder name by replacing invalid characters with numbers.
    Dashes are preserved and apostrophes remain unchanged.
    """
    # Dictionary of specific characters to replace
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
    
    # Replace characters defined in the char_map
    sanitized = ''.join(char_map.get(char, char) for char in title)
    
    # Replace all remaining invalid characters except apostrophe with their ASCII value
    sanitized = re.sub(r"[^\w\d\-_']", lambda match: str(ord(match.group(0))), sanitized)
    
    # Return the sanitized folder name in lowercase
    return sanitized.lower()

def parse_date(date_str):
    """
    Parse a date string in RFC3339 format into a datetime object.
    """
    try:
        return datetime.fromisoformat(date_str.strip())
    except ValueError:
        return None  # Return None if the date format is invalid

def generate_links_and_sort(input_dir, sections_dir, posts_per_page=10):
    """
    Generate sorted links based on LINE 2 (date) and match LINE 4 with section directories.
    Auto-creates section folders if missing.
    """
    try:
        if not os.path.exists(input_dir):
            print("Error: Posts directory does not exist.")
            return

        os.makedirs(sections_dir, exist_ok=True)
        all_links = []

        # Read and collect all valid links with their dates
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()

                    if len(lines) >= 4:
                        section_title = lines[3].strip()  # Line 4 (Section Title)
                        link_text = lines[2].strip()      # Line 3 (Link Text)
                        date_str = lines[1].strip()       # Line 2 (Date)

                        date = parse_date(date_str)
                        if date:
                            sanitized_section = sanitize_filename(section_title)
                            section_path = os.path.join(sections_dir, sanitized_section)

                            # Create the section directory if it doesn't exist
                            os.makedirs(section_path, exist_ok=True)

                            link = {
                                'date': date,
                                'link': f'<div class="blog_item">- <a href="/posts/{filename}">{link_text}</a></div>\n',
                                'title': section_title
                            }
                            all_links.append((date, link))
                        else:
                            print(f"Warning: Invalid date format in {filename}, skipping.")
                    else:
                        print(f"Warning: {filename} does not have at least 4 lines and will be skipped.")

        # Sort links by date (newest first)
        all_links.sort(key=lambda x: x[0], reverse=True)

        # Create paginated index.html files for each section
        for section_folder in os.listdir(sections_dir):
            section_path = os.path.join(sections_dir, section_folder)
            if os.path.isdir(section_path):
                section_links = [
                    link[1]['link']
                    for link in all_links
                    if sanitize_filename(link[1]['title']) == section_folder
                ]

                if section_links:
                    total_pages = (len(section_links) + posts_per_page - 1) // posts_per_page

                    for page in range(1, total_pages + 1):
                        page_file = "index.html" if page == 1 else f"pg{page}.html"
                        page_file_path = os.path.join(section_path, page_file)

                        with open(page_file_path, 'w', encoding='utf-8') as page_file:
                            page_file.write('<main>\n')
                            page_file.write(f"♡ <br>\n<strong>{section_folder.replace('_', ' ').title().replace('S ', 's ')}</strong>\n ✧*｡٩(－ω－*)و✧*｡<br><img src=\"/image/wiz.png\"</img><br>")
                            page_file.write('<div class="blog-list">\n')

                            start = (page - 1) * posts_per_page
                            end = start + posts_per_page
                            page_links = section_links[start:end]

                            while len(page_links) < posts_per_page:
                                page_links.append('<br>\n')

                            page_file.writelines(page_links)
                            page_file.write('</div>\n')

                            # Pagination
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
                                    page_file.write('') #[&laquo;] [&lsaquo;]  blank now

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
                                    page_file.write('') #[&rsaquo;] [&raquo;] --> blank

                                page_file.write('</div>\n')
                            else:
                                page_file.write('<br>')

                            page_file.write('</main>\n')

                        print(f"Generated page {page_file_path} for section: {section_folder}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    posts_directory = os.path.expanduser("~/gikoru/posts/")
    sections_directory = os.path.expanduser("~/gikoru/pg/sections/")

    print("Starting the script...")
    generate_links_and_sort(posts_directory, sections_directory)
