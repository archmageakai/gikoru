import os
from datetime import datetime

# get timezone - updated
current_time = datetime.now().astimezone().isoformat(timespec="seconds")

filename = input("Enter the filename (without .html): ")

output_dir = os.path.expanduser('~/gikoru/drafts/')
os.makedirs(output_dir, exist_ok=True)

file_path = os.path.join(output_dir, f"{filename}.html")

# post body 
html_content = f"""DRAFT
+++++
{current_time}
[Please write title here for this line]
[Please write section for this line]
----Style: "black & red"----
<link rel="stylesheet" type="text/css" href="css/style.css">
+++++

<p>POST BODY GOES HERE</p>
"""

with open(file_path, 'w') as file:
    file.write(html_content)

print(f":: stored in {file_path}")
