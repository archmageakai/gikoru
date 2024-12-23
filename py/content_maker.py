import os
import shutil
from datetime import datetime, timezone, timedelta

def clear_output_directory(output_directory):
    """
    Clears all files in the specified output directory.

    Args:
        output_directory (str): Path to the directory to be cleared.
    """
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

def parse_rfc3339(date_str):
    """
    Parses a date string in RFC3339 format to a datetime object.

    Args:
        date_str (str): The RFC3339 date string.

    Returns:
        datetime: A datetime object with timezone information.
    """
    try:
        # Handle 'Z' for UTC
        if 'Z' in date_str:
            date_str = date_str.replace('Z', '+00:00')
        # Parse the datetime and offset
        if '+' in date_str or '-' in date_str:
            main_date, offset = date_str[:-6], date_str[-6:]
            dt = datetime.strptime(main_date, "%Y-%m-%dT%H:%M:%S")
            hours_offset = int(offset[1:3])
            minutes_offset = int(offset[4:6])
            delta = timedelta(hours=hours_offset, minutes=minutes_offset)
            if offset[0] == '-':
                delta = -delta
            return dt.replace(tzinfo=timezone(delta))
        else:
            # Default to UTC if no offset is provided
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError as e:
        print(f"Error parsing RFC3339 date: {date_str} - {e}")
        return None

def convert_rfc3339_to_time_tag(date_str):
    """
    Converts a date string in RFC3339 format to a formatted <time> tag.

    Args:
        date_str (str): The RFC3339 date string.

    Returns:
        str: A <time> tag with both datetime and human-readable format.
    """
    date = parse_rfc3339(date_str)
    if not date:
        return "<time>Invalid Date</time>"

    # Extract UTC offset
    offset = date.utcoffset()
    if offset:
        hours_offset = int(offset.total_seconds() // 3600)
        minutes_offset = abs(int((offset.total_seconds() % 3600) // 60))
        utc_offset = f"UTC {hours_offset:+03}:{minutes_offset:02}"
    else:
        utc_offset = "UTC +00:00"

    # Format the datetime attribute and human-readable text
    datetime_attr = date.isoformat()
    human_readable = date.strftime(f"%B %-d, %Y :: %H:%M [{utc_offset}]")
    return f'<time datetime="{datetime_attr}">{human_readable}</time>'

def modify_html_files(input_directory, output_directory):
    """
    Modify HTML files as per the requirements:
    - Delete LINE 1, LINE 3, LINE 4, and LINE 5.
    - Wrap LINE 3 in <h1> tags and place it in LINE 1.
    - Convert RFC3339 date in LINE 2 to a <time> tag and place it in LINE 2.
    - Append a modified <div> block to the end of the file based on LINE 4 with formatted URL.
    - Wrap the entire content in <main> tags.
    - Convert uppercase characters in LINE 4 to lowercase for the URL.

    Args:
        input_directory (str): Path to the directory containing original HTML files.
        output_directory (str): Path to the directory to save modified HTML files.
    """
    # Character map for URL replacements
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

    # Clear the output directory
    clear_output_directory(output_directory)

    try:
        # Loop through each HTML file in the input directory
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()

                # Ensure the file has at least 5 lines to process
                if len(lines) < 5:
                    print(f"Warning: {filename} does not have enough lines and will be skipped.")
                    continue

                # Extract the necessary lines
                line_3 = lines[2].strip()  # Original LINE 3
                line_2 = lines[1].strip()  # Original LINE 2
                line_4 = lines[3].strip()  # Original LINE 4

                # Wrap LINE 3 in <h1> tags and place it in LINE 1
                new_line_1 = f"<h1>{line_3}</h1>\n"

                # Convert RFC3339 LINE 2 to a <time> tag
                time_tag = convert_rfc3339_to_time_tag(line_2)
                new_line_2 = f"{time_tag}\n"

                # Modify LINE 4 for the URL: Replace special characters and convert to lowercase
                modified_line_4 = "".join(char_map.get(char, char) for char in line_4).lower()

                # Create the new <div> block based on LINE 4
                new_div_block = f"""
<div>
    <div>:</div>
    <ul>
        <li><a href="/sections/{modified_line_4}/">{line_4}</a></li> 
    </ul>
</div>
"""

                # Combine the modified content:
                # 1. Add new Line 1 and Line 2.
                # 2. Include remaining lines except original Lines 3, 4, and 5.
                # 3. Append the new <div> block.
                modified_content = [new_line_1, new_line_2] + lines[5:] + [new_div_block]

                # Wrap the entire content in <main> tags
                wrapped_content = ["<main>\n"] + modified_content + ["</main>\n"]

                # Save the modified file to the output directory
                output_file = os.path.join(output_directory, filename)
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(wrapped_content)

                print(f"Processed and saved: {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Directory containing the original HTML files
    input_directory = os.path.expanduser("~/gikoru/posts")

    # Directory to save the modified HTML files
    output_directory = os.path.expanduser("~/gikoru/pg/posts")

    print("Clearing output directory and modifying HTML files...")
    modify_html_files(input_directory, output_directory)
