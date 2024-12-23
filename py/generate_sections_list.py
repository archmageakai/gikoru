import os
import re
from datetime import datetime

def sanitize_filename(title):
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

def parse_date(date_str):
    """
    Parse a date string in RFC3339 format into a datetime object.

    Args:
        date_str (str): The date string to parse.

    Returns:
        datetime: The parsed datetime object.
    """
    try:
        return datetime.fromisoformat(date_str.strip())
    except ValueError:
        return None  # Return None if the date format is invalid

def generate_links_and_sort(input_dir, sections_dir, posts_per_page=5):
    """
    Generate sorted links based on LINE 2 (date) and match LINE 4 with section directories.

    Args:
        input_dir (str): Path to the directory containing the input HTML files.
        sections_dir (str): Path to the directory containing section folders.
        posts_per_page (int): Number of posts per page (default is 5).
    """
    try:
        if not os.path.exists(input_dir) or not os.path.exists(sections_dir):
            print("Error: One or more required directories do not exist.")
            return

        all_links = []

        # Read and collect all valid links with their dates
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()

                    if len(lines) >= 4:
                        # Extract relevant lines
                        section_title = lines[3].strip()  # Line 4 (Section Title)
                        link_text = lines[2].strip()  # Line 3 (Link Text)
                        date_str = lines[1].strip()  # Line 2 (Date)

                        # Parse the date
                        date = parse_date(date_str)
                        if date:
                            sanitized_section = sanitize_filename(section_title)
                            section_path = os.path.join(sections_dir, sanitized_section)

                            # Check if section directory exists
                            if os.path.exists(section_path):
                                # Prepare the link with date for sorting
                                link = {
                                    'date': date,
                                    'link': f'- <a href="/posts/{filename}">{link_text}</a><br>\n',
                                    'title': section_title
                                }
                                all_links.append((date, link))  # Store the link with its date
                            else:
                                print(f"Warning: Section directory '{sanitized_section}' does not exist.")
                        else:
                            print(f"Warning: Invalid date format in {filename}, skipping.")
                    else:
                        print(f"Warning: {filename} does not have at least 4 lines and will be skipped.")

        # Sort all links by date (newest first)
        all_links.sort(key=lambda x: x[0], reverse=True)

        # Create index.html files for each section with the sorted links
        for section_folder in os.listdir(sections_dir):
            section_path = os.path.join(sections_dir, section_folder)
            if os.path.isdir(section_path):
                # Filter links that match the current section folder
                section_links = [link[1]['link'] for link in all_links if sanitize_filename(link[1]['title']) == section_folder]

                if section_links:
                    # Calculate the total number of pages
                    total_pages = (len(section_links) + posts_per_page - 1) // posts_per_page

                    for page in range(1, total_pages + 1):
                        # Determine the file name for the current page
                        if page == 1:
                            page_file_path = os.path.join(section_path, "index.html")
                        else:
                            page_file_path = os.path.join(section_path, f"pg{page}.html")

                        # Read the original HTML file content (preserving the first line)
                        with open(os.path.join(section_path, "index.html"), 'r', encoding='utf-8') as original_file:
                            lines = original_file.readlines()

                        # Extract LINE 2 from index.html (for the paginated pages)
                        line_2 = lines[1].strip() if len(lines) > 1 else ""

                        # Write the page content
                        with open(page_file_path, 'w', encoding='utf-8') as page_file:
                            page_file.write('<main>\n')  # Start the <main> tag

                            # Write the first line (wrapped in <h1> tags)
                            page_file.write(f"<h1>{lines[0].strip()}</h1>\n")

                            # Write LINE 2 extracted from index.html
                            page_file.write(f"<h2>{line_2}</h2>\n")

                            # Ensure there are always 5 lines (including blank lines)
                            start_index = (page - 1) * posts_per_page
                            end_index = start_index + posts_per_page
                            page_links = section_links[start_index:end_index]

                            # If fewer than 5 links, add blank lines
                            while len(page_links) < 5:
                                page_links.append('<br>\n')

                            # Write the links for the current page
                            page_file.writelines(page_links)

                            # Add pagination navigation
                            page_file.write('<div class="pagination">\n')
                            for p in range(1, total_pages + 1):
                                if total_pages == 1:
                                    # No pagination needed if there is only one page
                                    continue
                                elif p == 1 and page != 1:
                                    # For the first page, link to index.html
                                    page_file.write(f'<a href="index.html">[{p}]</a> ')
                                elif p == page:
                                    # For the current page, just display the page number (no link)
                                    page_file.write(f'[{p}] ')
                                else:
                                    # For other pages, link to pg{p}.html
                                    page_file.write(f'<a href="pg{p}.html">[{p}]</a> ')
                            page_file.write('\n</div>\n')

                            page_file.write('</main>\n')  # Close the <main> tag

                        print(f"Generated page {page_file_path} for section: {section_folder}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Input directory containing the original HTML files
    posts_directory = os.path.expanduser("~/gikoru/posts/")  # Adjust as needed
    # Directory containing the section folders
    sections_directory = os.path.expanduser("~/gikoru/pg/sections/")  # Adjust as needed

    print("Starting the script...")
    # Generate links and sort them with pagination
    generate_links_and_sort(posts_directory, sections_directory)
