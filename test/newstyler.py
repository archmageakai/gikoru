import os

def insert_style_line(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    insert_lines = [
        '----Style: "black & red"----\n',
        '<link rel="stylesheet" type="text/css" href="css/style.css">\n'
    ]

    for filename in os.listdir(input_dir):
        if filename.endswith(".html"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            # Check that line 5 exists
            if len(lines) >= 5:
                modified_lines = lines[:4] + insert_lines + lines[4:]
            else:
                print(f"kipping {filename}: less than 5 lines")
                continue

            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.writelines(modified_lines)

            print(f"Processed: {filename}")

if __name__ == "__main__":
    input_directory = os.path.expanduser("~/gikoru/posts")  # CHANGE THIS
    output_directory = os.path.expanduser("~/gikoru/test")  # CHANGE THIS

    insert_style_line(input_directory, output_directory)
