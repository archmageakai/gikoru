import os
import xml.etree.ElementTree as ET
from datetime import datetime

def extract_metadata_from_html(file_path):
    """
    Extract metadata (title, published date, and content from LINE 6 onward) from an HTML file.
    Removes lines containing just '+++++' or the stylesheet link.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        if len(lines) < 6:
            print(f"Warning: {file_path} does not have enough lines and will be skipped.")
            return None

        title = lines[2].strip()       # LINE 3
        published = lines[1].strip()   # LINE 2 (must already be RFC-3339)

        raw_content_lines = lines[5:]  # From LINE 6 onward

        # Filter out lines that are just '+++++' or contain the stylesheet link
        filtered_lines = []
        for line in raw_content_lines:
            stripped = line.strip()
            if stripped == "+++++":
                continue
            if '<link rel="stylesheet" type="text/css" href="css/style.css">' in stripped:
                continue
            filtered_lines.append(line)

        content = "".join(filtered_lines).strip()

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
    Indents the XML element to make it more readable.
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    elif not level:
        elem.tail = "\n"

def generate_atom_feed(input_directory, output_path, feed_metadata):
    """
    Generates an Atom feed XML file based on HTML files in the input directory.
    """
    ATOM_NS = "http://www.w3.org/2005/Atom"
    ET.register_namespace("", ATOM_NS)

    feed = ET.Element(ET.QName(ATOM_NS, "feed"))

    # Mimic cadence.moe style metadata block
    ET.SubElement(feed, "id").text = feed_metadata["id"]
    ET.SubElement(feed, "title").text = feed_metadata["title"]
    ET.SubElement(feed, "updated").text = feed_metadata["updated"]
    ET.SubElement(feed, "generator").text = feed_metadata.get("generator", "akai.gikopoi.com generator")

    author = ET.SubElement(feed, "author")
    ET.SubElement(author, "name").text = feed_metadata["author"]
    ET.SubElement(author, "uri").text = feed_metadata.get("author_uri", feed_metadata["id"])

    ET.SubElement(feed, "link", {
        "rel": "alternate",
        "href": feed_metadata.get("alternate", feed_metadata["id"])
    })
    ET.SubElement(feed, "link", {
        "rel": "self",
        "href": feed_metadata["self"],
        "type": "application/atom+xml"
    })

    entries = []

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".html"):
            metadata = extract_metadata_from_html(file_path)
            if metadata:
                entry_id = f"https://akai.gikopoi.com/posts/{filename}"
                entries.append({
                    "title": metadata["title"],
                    "link": f"https://akai.gikopoi.com/posts/{filename}",
                    "published": metadata["published"],
                    "updated": metadata["published"],
                    "id": entry_id,
                    "content": metadata["content"],
                })

    # Sort entries by published date, newest first
    entries.sort(key=lambda x: datetime.fromisoformat(x["published"]), reverse=True)

    for entry in entries:
        entry_elem = ET.SubElement(feed, "entry")
        ET.SubElement(entry_elem, "id").text = entry["id"]
        ET.SubElement(entry_elem, "title").text = entry["title"]
        ET.SubElement(entry_elem, "link", {"href": entry["link"]})
        ET.SubElement(entry_elem, "published").text = entry["published"]
        ET.SubElement(entry_elem, "updated").text = entry["updated"]

        content_elem = ET.SubElement(entry_elem, "content", {"type": "html"})
        content_elem.text = entry["content"]

    indent(feed)
    tree = ET.ElementTree(feed)
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

    print(f"Atom feed generated at: {output_path}")

if __name__ == "__main__":
    input_directory = os.path.expanduser("~/gikoru/posts")
    output_path = os.path.expanduser("~/gikoru/public/index.atom")

    updated_time = datetime.now().astimezone().isoformat(timespec="seconds")

    feed_metadata = {
        "title": "akai.gikopoi.com",
        "author": "akai",
        "author_uri": "https://akai.gikopoi.com/",
        "id": "https://akai.gikopoi.com/",
        "alternate": "https://akai.gikopoi.com/",
        "self": "https://akai.gikopoi.com/index.atom",
        "updated": updated_time,
        "generator": "https://github.com/archmageakai/gikoru",
    }

    print("Generating Atom feed from HTML files...")
    generate_atom_feed(input_directory, output_path, feed_metadata)
