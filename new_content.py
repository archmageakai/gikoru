import os
from datetime import datetime

# get timezone - updated
current_time = datetime.now().astimezone().isoformat(timespec="seconds")

filename = input("Enter the filename (without .html): ")

output_dir = os.path.expanduser('~/gikoru/drafts/')
os.makedirs(output_dir, exist_ok=True)

file_path = os.path.join(output_dir, f"{filename}.html")

# Use raw f-string (fr"""...""") and double curly braces in JS code
html_content = fr"""DRAFT
<head><meta charset="UTF-8">Meta-data loaded for live-server
+++++
{current_time}
[Please write title here for this line]
[Please write section for this line]
----Style: "black & red"----
<link rel="stylesheet" type="text/css" href="css/style.css">
+++++

<p>Body</p>

</head>
"""

with open(file_path, 'w') as file:
    file.write(html_content)

print(f":: stored in {file_path}")
