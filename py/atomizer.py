import os
import xml.etree.ElementTree as ET
from datetime import datetime

def extract_metadata_from_html(file_path):
    """
    Extract metadata (title, published date, and content from LINE 6 onward) from an HTML file.

    Args:
        file_path (str): Path to the HTML file.

    Returns:
        dict: Metadata with 'title', 'published', and 'content'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # Ensure the file has at least 6 lines to process
        if len(lines) < 6:
            print(f"Warning: {file_path} does not have enough lines and will be skipped.")
            return None

        # Extract metadata
        title = lines[2].strip()  # LINE 3
        published = lines[1].strip()  # LINE 2 (already in RFC3339 format)

        # Extract content from LINE 6 onward
        content = "".join(lines[5:]).strip()  # Start from index 5 (LINE 6)

        return {
            "title": title,
            "published": published,
            "content": content,
        }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def indent(elem, level=0):
    """
    Indents the XML element to make it more readable, ensuring each tag gets its own line.

    Args:
        elem (Element): The XML element to indent.
        level (int): The current level of indentation.
    """
    indent_space = "  "
    
    # Ensure every tag gets its own line
    if len(elem):
        if elem.text and not elem.text.strip():
            elem.text = None  # Remove unnecessary whitespace
        for child in elem:
            indent(child, level + 1)
        if not elem.tag in ["entry", "feed"]:
            elem.tail = (elem.tail or "").strip()
        if level:
            elem.tail = f"\n{indent_space * level}" + (elem.tail or "").strip()

    # Ensure that the tag itself is on a new line
    if level == 0:  # Only add newline after root element
        elem.tail = "\n" + (elem.tail or "").strip()

def generate_atom_feed(input_directory, output_path, feed_metadata):
    """
    Generates an Atom feed XML file based on HTML files in the input directory.

    Args:
        input_directory (str): Directory containing HTML files.
        output_path (str): Path to save the generated Atom feed.
        feed_metadata (dict): Metadata for the feed (title, subtitle, author, updated).
    """
    # Define the Atom namespace
    ATOM_NS = "http://www.w3.org/2005/Atom"
    ET.register_namespace("", ATOM_NS)

    # Create the root element
    feed = ET.Element(ET.QName(ATOM_NS, "feed"))

    # Add feed metadata
    ET.SubElement(feed, "title").text = feed_metadata["title"]
    ET.SubElement(feed, "subtitle").text = feed_metadata["subtitle"]
    ET.SubElement(feed, "updated").text = feed_metadata["updated"]
    ET.SubElement(feed, "id").text = feed_metadata["id"]  # Correctly add the feed-level <id> tag

    # Add author information
    author = ET.SubElement(feed, "author")
    ET.SubElement(author, "name").text = feed_metadata["author"]

    # List to hold all the entries
    entries = []

    # Process each HTML file in the input directory
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".html"):
            metadata = extract_metadata_from_html(file_path)
            if metadata:
                # Generate a unique ID for the entry
                entry_id = f"https://akai.gikopoi.com/posts/{filename}"

                # Add entry metadata to the entries list
                entries.append({
                    "title": metadata["title"],
                    "link": f"/posts/{filename}",
                    "published": metadata["published"],
                    "content": metadata["content"],
                    "id": entry_id,
                    "updated": feed_metadata["updated"],  # Same updated time as feed
                })

    # Sort entries by the published date (newest first)
    entries.sort(key=lambda x: datetime.fromisoformat(x["published"]), reverse=True)

    # Add entries to the feed
    for entry in entries:
        entry_elem = ET.SubElement(feed, "entry")
        ET.SubElement(entry_elem, "id").text = entry["id"]  # Add <id> first
        ET.SubElement(entry_elem, "title").text = entry["title"]
        ET.SubElement(entry_elem, "link", {"href": entry["link"]})  # Add <link> after <id>
        ET.SubElement(entry_elem, "published").text = entry["published"]
        
        # Add <updated> tag with the same time as feed metadata
        ET.SubElement(entry_elem, "updated").text = entry["updated"]

        # Add <content> with type="html"
        content_elem = ET.SubElement(entry_elem, "content", {"type": "html"})
        content_elem.text = entry["content"]

    # Indent the XML to make it more readable
    indent(feed)

    # Write the Atom feed to a file
    tree = ET.ElementTree(feed)
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    
    print(f"Atom feed generated at: {output_path}")

if __name__ == "__main__":
    # Directory containing the original HTML files
    input_directory = os.path.expanduser("~/gikoru/posts")

    # Path to save the Atom feed
    output_path = os.path.expanduser("~/gikoru/public/index.atom")

    # Get current time in the local timezone
    updated_time = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")  # RFC 3339 with timezone

    # Define feed metadata
    feed_metadata = {
        "title": "akai.gikopoi.com",
        "subtitle": "generated by gikoru (on github: archmageakai/gikoru.git)",
        "author": "akai",
        "id": "akai.gikopoi.com",  # Base URL for the feed
        "updated": updated_time,  # Updated time in RFC 3339 format with timezone
    }

    print("Generating Atom feed from HTML files...")
    generate_atom_feed(input_directory, output_path, feed_metadata)
