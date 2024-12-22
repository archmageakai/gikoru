import os
import re

def sanitize_directory_name(title):
    """
    Convert a title string into a valid folder name by replacing invalid characters with numbers.

    Args:
        title (str): The title to sanitize.

    Returns:
        str: A sanitized folder name.
    """
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
    sanitized = ''.join(char_map.get(char, char) for char in title)
    sanitized = re.sub(r'[^\w\d_]', lambda match: str(ord(match.group(0))), sanitized)
    return sanitized.lower()

def extract_text_from_line(line):
    """
    Remove HTML tags from a line of text.

    Args:
        line (str): A line of HTML content.

    Returns:
        str: Text content without HTML tags.
    """
    return re.sub(r'<[^>]*>', '', line).strip()

def ensure_five_lines(links, posts_per_page=5):
    """
    Ensure that there are exactly 5 lines on the page by adding empty lines if necessary.

    Args:
        links (list): List of HTML link strings.
        posts_per_page (int): Number of posts per page (default is 5).
    
    Returns:
        list: The list of links padded to ensure 5 lines.
    """
    while len(links) < posts_per_page:
        links.append('<br>\n')  # Add an empty line (break) to ensure 5 lines
    
    return links

def generate_sections_portal(sections_dir, output_file, posts_per_page=5):
    """
    Generate a portal index.html file that links to each section directory and handles pagination.

    Args:
        sections_dir (str): Path to the directory containing section folders.
        output_file (str): Path to the output index.html file.
        posts_per_page (int): Number of posts per page (default is 5).
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
                    line_2 = lines[1].strip()
                    text_content = extract_text_from_line(line_2)

                    # Generate a sanitized folder name for the link
                    sanitized_name = sanitize_directory_name(section_folder)

                    # Generate a link for the section
                    link = f'- <a href="/sections/{sanitized_name}/">{text_content}</a><br>'
                    links.append(link)

        # Alphabetize the links list
        links.sort()

        # If there are more than 5 links, paginate
        if len(links) > posts_per_page:
            total_pages = (len(links) + posts_per_page - 1) // posts_per_page

            for page in range(1, total_pages + 1):
                # Determine the file name for the current page
                if page == 1:
                    page_file_path = output_file  # The first page is the main index.html
                else:
                    page_file_path = os.path.join(sections_dir, f"pg{page}.html")

                # Calculate the start and end index for the current page
                start_index = (page - 1) * posts_per_page
                end_index = start_index + posts_per_page
                page_links = links[start_index:end_index]

                # Ensure there are 5 lines on the page
                page_links = ensure_five_lines(page_links, posts_per_page)

                # Write the page content
                with open(page_file_path, 'w', encoding='utf-8') as page_file:
                    page_file.write('<main>\n')
                    page_file.write('<h1>Sections</h1>\n\n')

                    # Write the links for the current page
                    for link in page_links:
                        page_file.write(f'{link}\n')

                    # Add pagination navigation
                    page_file.write('<div class="pagination">\n')
                    for p in range(1, total_pages + 1):
                        if p == 1 and page != 1:
                            # For the first page, link to index.html
                            page_file.write(f'<a href="index.html">[{p}]</a> ')
                        elif p == page:
                            # For the current page, just display the page number (no link)
                            page_file.write(f'[{p}] ')
                        else:
                            # For other pages, link to pg{p}.html
                            page_file.write(f'<a href="pg{p}.html">[{p}]</a> ')
                    page_file.write('\n</div>\n')

                    page_file.write('</main>\n')

                print(f"Generated page {page_file_path} with {len(page_links)} links")

        else:
            # If there are 5 or fewer links, just write them to the main index.html
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write('<main>\n')
                outfile.write('<h1>Sections</h1>\n\n')

                # Ensure there are 5 lines on the page
                links = ensure_five_lines(links, posts_per_page)

                for link in links:
                    outfile.write(f'{link}\n')

                outfile.write('</main>\n')

            print(f"Portal file generated successfully at {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Directory containing the section folders
    sections_directory = os.path.expanduser("~/site/pg/sections/")
    # Path to the output index.html file
    output_path = os.path.join(sections_directory, "index.html")

    print("Generating sections portal...")
    generate_sections_portal(sections_directory, output_path)
