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
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Check if the first line is "POST"
        if lines and lines[0].strip() == "POST":
            # Remove the first line (which is "POST")
            lines.pop(0)
            
            # Define the new file path in the posts directory
            new_file_path = os.path.join(posts_dir, filename)
            
            # Write the modified content to the new file in the posts directory
            with open(new_file_path, 'w') as file:
                file.writelines(lines)
            
            # Remove the original file from the drafts directory
            os.remove(file_path)
            
            # Print confirmation message
            print(f"Moved and modified: {filename} -> {new_file_path}")