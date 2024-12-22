import os

def create_html_from_post():
    """
    Reads content from ~/site/post.txt, creates an HTML document, and saves it in ~/site/.
    """
    try:
        # Define paths
        post_txt_path = os.path.expanduser("~/site/post.txt")
        site_directory = os.path.expanduser("~/site/")

        # Check if post.txt exists
        if not os.path.exists(post_txt_path):
            print("Error: ~/site/post.txt does not exist.")
            return

        # Read content from post.txt
        with open(post_txt_path, 'r', encoding='utf-8') as file:
            post_content = file.read()

        # Ask for the name of the new HTML file
        html_filename = input("Enter the name for the HTML file (without extension): ").strip()
        if not html_filename:
            print("Error: File name cannot be empty.")
            return
        if not html_filename.endswith(".html"):
            html_filename += ".html"

        # Define the output file path
        output_file_path = os.path.join(site_directory, html_filename)

        # Write content to the new HTML file
        with open(output_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(post_content)

        print(f"HTML file created: {output_file_path}")
        print("Please move the file into ~/site/posts/ when the draft is ready to be posted, then run gikoru.py (´｡• ω •｡`)")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_html_from_post()
