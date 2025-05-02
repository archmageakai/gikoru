import os
from datetime import datetime
from collections import defaultdict

def generate_paginated_url_list(workfiles_dir, output_dir, posts_per_page=10):
    """
    Generate paginated HTML pages with sorted URL links based on the contents of files in a directory.
    Also generates a full archive grouped by year and month.
    """
    url_list = []
    archive_dict = defaultdict(lambda: defaultdict(list))  # year -> month -> list of links

    try:
        if not os.path.exists(workfiles_dir):
            print(f"Error: Directory {workfiles_dir} does not exist.")
            return

        if os.path.exists(output_dir):
            for file_name in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(output_dir)

        for filename in os.listdir(workfiles_dir):
            file_path = os.path.join(workfiles_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if len(lines) >= 3:
                        try:
                            date_str = lines[1].strip()
                            date = datetime.fromisoformat(date_str)
                            link_text = lines[2].strip()
                            url = f"/posts/{filename}"
                            html_link = f'<div class="blog_item">- <a href="{url}">{link_text}</a></div>\n'
                            url_list.append((date, html_link))

                            # For archive
                            year = str(date.year)
                            month = date.strftime('%B')
                            archive_dict[year][month].append((date, html_link))
                        except ValueError:
                            print(f"Warning: {filename} has an invalid date format in line 2 and will be skipped.")
                    else:
                        print(f"Warning: {filename} does not have enough lines and will be skipped.")

        # Sort for pagination
        url_list.sort(key=lambda x: x[0], reverse=True)

        total_urls = len(url_list)
        total_pages = (total_urls + posts_per_page - 1) // posts_per_page

        for page in range(1, total_pages + 1):
            page_file = os.path.join(output_dir, "index.html" if page == 1 else f"pg{page}.html")
            with open(page_file, 'w', encoding='utf-8') as outfile:
                outfile.write('<main>\n<div class="blog-list">\n')
                start_index = (page - 1) * posts_per_page
                end_index = start_index + posts_per_page
                page_links = [url for _, url in url_list[start_index:end_index]]

                while len(page_links) < posts_per_page:
                    page_links.append('<br>\n')

                for link in page_links:
                    outfile.write(link)
                outfile.write('</div>\n')

                if total_pages > 1:
                    outfile.write('<div class="pagination">\n')

                # Navigation arrows - L
                if page > 1:
                    prev_page = "index.html" if page - 1 == 1 else f"pg{page - 1}.html"

                    if page > 2:
                        outfile.write(f'<a href="index.html">[&laquo;]</a> ')
                        
                    outfile.write(f'<a href="{prev_page}">[&lsaquo;]</a> ')
                else:
                    outfile.write('') #[&laquo;] [&lsaquo;]  now blank

                # Page number group (5-page block)
                # Sliding window logic for page numbers
                if total_pages <= 5:
                    block_start = 1
                    block_end = total_pages
                else:
                    if page <= 3:
                        block_start = 1
                        block_end = 5
                    elif page >= total_pages - 2:
                        block_start = total_pages - 4
                        block_end = total_pages
                    else:
                        block_start = page - 2
                        block_end = page + 2

                # Render the page number links
                for p in range(block_start, block_end + 1):
                    if p == page:
                        outfile.write(f'[{p:02d}] ')
                    else:
                        page_url = "index.html" if p == 1 else f"pg{p}.html"
                        outfile.write(f'<a href="{page_url}">[{p:02d}]</a> ')
                """
                #Experimental
                if (block_end - block_start + 1) < 5:
                    for _ in range(5 - (block_end - block_start + 1)):
                        outfile.write('&nbsp;&nbsp;&nbsp;&nbsp;')
                """
                
                # Navigation arrows - R
                if page < total_pages:
                    next_page = f"pg{page + 1}.html"
                    outfile.write(f'<a href="{next_page}">[&rsaquo;]</a> ')

                    if page + 1 < total_pages:
                        last_page = f"pg{total_pages}.html"
                        outfile.write(f'<a href="{last_page}">[&raquo;]</a>')
                else:
                    outfile.write('') #[&rsaquo;] [&raquo;]  now blank

                outfile.write('\n</div>\n')


                if total_pages == 1:
                    outfile.write('<br>\n')

                outfile.write('</main>\n')

        print(f"Paginated URL list generated successfully in {output_dir}.")

        # --- ARCHIVE GENERATION ---
        archive_dir = os.path.expanduser("~/gikoru/pg/archive")
        os.makedirs(archive_dir, exist_ok=True)
        archive_path = os.path.join(archive_dir, "index.html")

        # Group posts by year and month
        grouped_posts = defaultdict(lambda: defaultdict(list))  # {year: {month: [HTML_LINKS]}}

        for date, html_link in url_list:
            year = date.year
            month_name = date.strftime("%B")
            grouped_posts[year][month_name].append((date, html_link))

        with open(archive_path, 'w', encoding='utf-8') as archive_file:
            archive_file.write('<main>\n')
            archive_file.write('♡ <br>\n<strong>wizard\'s archive</strong>\n')
            archive_file.write('✧*｡٩(－ω－*)و✧*｡<br>\n')
            archive_file.write('<img src="/image/wiz.png" alt="Wizard Image"/><br>\n')
            archive_file.write('<div class="blog-list">\n')

            for year in sorted(grouped_posts.keys(), reverse=True):
                archive_file.write(f"<u>{year}</u><br>\n")
                for month in sorted(grouped_posts[year].keys(), key=lambda m: datetime.strptime(m, "%B"), reverse=True):
                    archive_file.write(f"<small>♡ {month} ♡</small><br>\n")
                    
                    # Sort posts within each month by date from 1st to 31st (ascending order)
                    for post_date, post_link in sorted(grouped_posts[year][month], key=lambda x: x[0], reverse=True):
                        archive_file.write(post_link)
                    
                    archive_file.write('<br>\n')  # break at the end of the month

                archive_file.write("\n") # end month

            archive_file.write('(´｡• ᵕ •｡`) ♡\n')
            archive_file.write('</div>\n</main>\n')

        print(f"Full archive generated at {archive_path}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    workfiles_directory = os.path.expanduser("~/gikoru/posts/")
    output_directory = os.path.expanduser("~/gikoru/pg/index")
    generate_paginated_url_list(workfiles_directory, output_directory)
