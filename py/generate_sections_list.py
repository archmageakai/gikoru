import os
import re
from datetime import datetime

def sanitize_filename(title):
    """
    Convert a title string into a valid folder name by replacing invalid characters with numbers.
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
    """
    try:
        return datetime.fromisoformat(date_str.strip())
    except ValueError:
        return None  # Return None if the date format is invalid

def generate_links_and_sort(input_dir, sections_dir, posts_per_page=5):
    """
    Generate sorted links based on LINE 2 (date) and match LINE 4 with section directories.
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

                        # Write the page content
                        with open(page_file_path, 'w', encoding='utf-8') as page_file:
                            page_file.write('<main>\n')  # Start the <main> tag

                            # Write the section title as <h1>
                            page_file.write(f"<h1>{section_folder.replace('_', ' ').title()}</h1>\n")

                            # Write the links for the current page
                            start_index = (page - 1) * posts_per_page
                            end_index = start_index + posts_per_page
                            page_links = section_links[start_index:end_index]

                            # If fewer than 5 links, add blank lines
                            while len(page_links) < posts_per_page:
                                page_links.append('<br>\n')

                            page_file.writelines(page_links)

                            # Add pagination navigation if more than one page
                            if total_pages > 1:
                                page_file.write('<div class="pagination">\n')
                                pagination_lines = [
                                    ' '.join(
                                        f'[{p:02d}]' if p == page else f'<a href="{"index.html" if p == 1 else f"pg{p}.html"}">[{p:02d}]</a>'
                                        for p in range(i, min(i + 5, total_pages + 1))
                                    )
                                    for i in range(1, total_pages + 1, 5)
                                ]
                                page_file.write('<br>\n'.join(pagination_lines))
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
