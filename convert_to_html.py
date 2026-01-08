#!/usr/bin/env python3
"""
Convert markdown guide files to HTML with navigation
"""

import os
import re
from pathlib import Path
import markdown
from markdown.extensions import fenced_code, tables, codehilite

# Chapter navigation map
CHAPTERS = [
    ("00.00-front-matter", "Front Matter", None, "00.01-contents"),
    ("00.01-contents", "Contents", "00.00-front-matter", "01.00-introduction"),
    ("01.00-introduction", "Introduction", "00.01-contents", "01.01-prerequisites"),
    ("01.01-prerequisites", "Prerequisites", "01.00-introduction", "02.00-foundations"),
    ("02.00-foundations", "Foundations", "01.01-prerequisites", "02.01-project-setup"),
    ("02.01-project-setup", "Project Setup", "02.00-foundations", "02.02-web-application-basics"),
    ("02.02-web-application-basics", "Web Application Basics", "02.01-project-setup", "02.03-routing-requests"),
    ("02.03-routing-requests", "Routing Requests", "02.02-web-application-basics", "04.00-database-driven-responses"),
    ("04.00-database-driven-responses", "Database-Driven Responses", "02.03-routing-requests", "15.00-conclusion"),
    ("15.00-conclusion", "Conclusion", "04.00-database-driven-responses", "16.00-further-reading"),
    ("16.00-further-reading", "Further Reading", "15.00-conclusion", "17.00-guided-exercises"),
    ("17.00-guided-exercises", "Guided Exercises", "16.00-further-reading", None),
]

def create_html_template(title, content, prev_link=None, next_link=None, chapter_num=None):
    """Create HTML page with navigation"""

    prev_html = ""
    if prev_link:
        prev_title = next((c[1] for c in CHAPTERS if c[0] == prev_link), "Previous")
        prev_html = f'<a href="{prev_link}.html">Previous</a>'

    next_html = ""
    if next_link:
        next_title = next((c[1] for c in CHAPTERS if c[0] == next_link), "Next")
        next_html = f'<a href="{next_link}.html">Next</a> &rsaquo;'

    chapter_html = ""
    if chapter_num:
        chapter_html = f'<div class="chapter">{chapter_num}</div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{title} &mdash; Let's Build with Elixir and Phoenix</title>
    <link rel="stylesheet" type="text/css" href="assets/css/main.css">
</head>
<body>
    <header>
        <div class="wrapper">
            <div>
                <a href="index.html">Let's Build with Elixir and Phoenix</a>
                <span class="crumbs">&rsaquo; {title}</span>
            </div>
            <div>
                {prev_html and f"&lsaquo; {prev_html} &middot;" or ""}
                <a href="00.01-contents.html">Contents</a>
                {next_html and f"&middot; {next_html}" or ""}
            </div>
        </div>
    </header>
    <main class="wrapper text">
        {chapter_html}
        {content}
    </main>
    <footer>
        <div class="wrapper">
            <div>
                {prev_html and f"&lsaquo; {prev_html}" or ""}
            </div>
            <div>
                <a href="00.01-contents.html">Contents</a>
            </div>
            <div>
                {next_html or ""}
            </div>
        </div>
    </footer>
</body>
</html>
"""

def convert_markdown_to_html(md_content):
    """Convert markdown to HTML with extensions"""

    # Process code blocks with file paths
    md_content = re.sub(
        r'```(\w+)\n# File: ([^\n]+)\n',
        r'<figure class="code"><figcaption>File: \2</figcaption><pre><code class="\1">',
        md_content
    )

    # Close code blocks
    md_content = re.sub(r'```\n', '</code></pre></figure>\n', md_content)
    md_content = re.sub(r'```', '</code></pre></figure>', md_content)

    # Convert blockquotes with special formatting for FP concepts
    md_content = re.sub(
        r'> \*\*FP Concept: ([^\*]+)\*\*',
        r'<blockquote class="fp-concept"><strong>FP Concept: \1</strong>',
        md_content
    )

    # Convert notes/hints/important blocks
    md_content = re.sub(r'> \*\*Note\*\*:', r'<div class="note"><strong>Note:</strong>', md_content)
    md_content = re.sub(r'> \*\*Hint\*\*:', r'<div class="hint"><strong>Hint:</strong>', md_content)
    md_content = re.sub(r'> \*\*Important\*\*:', r'<div class="important"><strong>Important:</strong>', md_content)

    # Convert remaining markdown
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'codehilite', 'nl2br'])
    html = md.convert(md_content)

    return html

def process_chapter(md_file, output_dir):
    """Process a single chapter file"""

    filename = md_file.stem

    # Find chapter info
    chapter_info = next((c for c in CHAPTERS if c[0] == filename), None)
    if not chapter_info:
        print(f"Skipping {filename} - not in navigation map")
        return

    filename_base, title, prev_link, next_link = chapter_info

    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract chapter number if present
    chapter_match = re.search(r'^# Chapter (\d+[.\d]*):?(.+)$', md_content, re.MULTILINE)
    chapter_num = None
    if chapter_match:
        chapter_num = f"Chapter {chapter_match.group(1)}"
        # Remove the chapter line from content as we'll add it separately
        md_content = re.sub(r'^# Chapter \d+[.\d]*:?[^\n]*\n', '', md_content, count=1, flags=re.MULTILINE)

    # Convert markdown to HTML
    html_content = convert_markdown_to_html(md_content)

    # Create full HTML page
    html_page = create_html_template(title, html_content, prev_link, next_link, chapter_num)

    # Write HTML file
    output_file = output_dir / f"{filename}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_page)

    print(f"Created {output_file.name}")

def main():
    """Main conversion function"""

    base_dir = Path(__file__).parent
    guide_dir = base_dir / "guide"
    output_dir = base_dir / "html"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Process all markdown files
    md_files = sorted(guide_dir.glob("*.md"))

    for md_file in md_files:
        try:
            process_chapter(md_file, output_dir)
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    print(f"\nConversion complete! Open html/index.html in your browser.")

if __name__ == "__main__":
    main()
