import os
import shutil

# Define the directories
drafts_dir = os.path.expanduser('~/gikoru/drafts/')
posts_dir = os.path.expanduser('~/gikoru/posts/')

# Ensure the posts directory exists
os.makedirs(posts_dir, exist_ok=True)

# Iterate through all files in the drafts directory
for filename in os.listdir(drafts_dir):
    file_path = os.path.join(drafts_dir, filename)
    
    # Check if it's a file (skip directories)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if the first line is "POST"
        if content.startswith("POST"):
            # Remove lines based on lin_del
            lin_del = 2
            content = content.split('\n', lin_del)[lin_del]

            end = "</head>"
            end_index = content.find(end)
            if end_index != -1:
                content = content[:end_index].rstrip() + "\n"
            
            """
            # Remove everything after the AUTO-REMOVED marker
            marker = "<!-- *** AUTO-REMOVED  *** -->"
            marker_index = content.find(marker)
            if marker_index != -1:
                content = content[:marker_index].rstrip() + "\n"
            """
            
            # Define the new file path in the posts directory
            new_file_path = os.path.join(posts_dir, filename)

            # Write the modified content to the new file in the posts directory
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            # Remove the original file from the drafts directory
            os.remove(file_path)

            # Print confirmation message
            print(f"Moved and cleaned: {filename} -> {new_file_path}")
