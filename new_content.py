import os
from datetime import datetime, timezone, timedelta

# Get the current time with timezone info (UTC-5 for example)
# You can change the offset to match your local timezone
local_timezone = timezone(timedelta(hours=-5))  # UTC-5 timezone offset (for example)
current_time = datetime.now(local_timezone).replace(microsecond=0).isoformat()

# Prompt for filename
filename = input("Enter the filename (without .html): ")

# Define the output directory
output_dir = os.path.expanduser('~/gikoru/drafts/')
os.makedirs(output_dir, exist_ok=True)

# Define the full path for the new file
file_path = os.path.join(output_dir, f"{filename}.html")

# Create the content of the HTML file
html_content = f"""DRAFT
+++++
{current_time}
[Please write title here for this line]
[Please write section for this line]
+++++

<p>Post body goes here, use HTML noob</p>

***When you are ready for this to post, make sure line 1 says POST instead of DRAFT
"""

# Write the content to the file
with open(file_path, 'w') as file:
    file.write(html_content)

# Print confirmation message
print(f":: stored in {file_path}")
