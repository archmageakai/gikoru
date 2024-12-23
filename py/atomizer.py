import os
import xml.etree.ElementTree as ET
from datetime import datetime

def extract_metadata_from_html(file_path):
    """
    Extract metadata (title, published date) from an HTML file.

    Args:
        file_path (str): Path to the HTML file.

    Returns:
        dict: Metadata with 'title', 'published', and 'summary'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # Ensure the file has at least 3 lines to process
        if len(lines) < 3:
            print(f"Warning: {file_path} does not have enough lines and will be skipped.")
            return None

        # Extract metadata
        title = lines[2].strip()  # LINE 3
        published = lines[1].strip()  # LINE 2 (already in RFC3339 format)
        summary = "...." if len(lines) < 4 else lines[3].strip()  # Optional summary (LINE 4 if exists)

        return {
            "title": title,
            "published": published,
            "summary": summary,
        }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

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
    ET.SubElement(feed, "id").text = feed_metadata["id"]
    ET.SubElement(feed, "updated").text = feed_metadata["updated"]

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
                # Add entry metadata to the entries list
                entries.append({
                    "title": metadata["title"],
                    "link": f"/posts/{filename}",
                    "published": metadata["published"],
                    "summary": metadata["summary"],
                })

    # Sort entries by the published date (newest first)
    entries.sort(key=lambda x: datetime.fromisoformat(x["published"]), reverse=True)

    # Add entries to the feed
    for entry in entries:
        entry_elem = ET.SubElement(feed, "entry")
        ET.SubElement(entry_elem, "title").text = entry["title"]
        ET.SubElement(entry_elem, "link", {"href": entry["link"]})
        ET.SubElement(entry_elem, "published").text = entry["published"]
        ET.SubElement(entry_elem, "summary").text = entry["summary"]

    # Write the Atom feed to a file
    tree = ET.ElementTree(feed)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Atom feed generated at: {output_path}")

if __name__ == "__main__":
    # Directory containing the original HTML files
    input_directory = os.path.expanduser("~/gikoru/posts")

    # Path to save the Atom feed
    output_path = os.path.expanduser("~/gikoru/public/index.atom")

    # Define feed metadata
    feed_metadata = {
        "title": "akai.gikopoi.com",
        "subtitle": "generated by gikoru (on github: archmageakai/gikoru.git)",
        "author": "akai",
        "id": "",
        "updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    print("Generating Atom feed from HTML files...")
    generate_atom_feed(input_directory, output_path, feed_metadata)
