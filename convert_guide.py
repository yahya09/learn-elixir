#!/usr/bin/env python3
"""
Convert markdown guide files to HTML with proper navigation and formatting
"""

import os
import re
from pathlib import Path

# Try to import markdown, if not available use basic conversion
try:
    import markdown
    from markdown.extensions import fenced_code, tables
    USE_MARKDOWN = True
except ImportError:
    USE_MARKDOWN = False
    print("Note: markdown library not found, using basic conversion")
    print("For better formatting: pip3 install markdown")

# Chapter navigation mapping
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

def basic_markdown_to_html(text):
    """Basic markdown to HTML conversion without external libraries"""

    # Code blocks with file paths
    text = re.sub(r'```(\w+)\s*\n#\s*File:\s*([^\n]+)\n(.*?)```',
                  r'<figure class="code"><figcaption>File: \2</figcaption><pre><code class="language-\1">\3</code></pre></figure>',
                  text, flags=re.DOTALL)

    # Code blocks without file paths
    text = re.sub(r'```(\w+)?\s*\n(.*?)```',
                  r'<figure class="code"><pre><code>\2</code></pre></figure>',
                  text, flags=re.DOTALL)

    # Headers
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Blockquotes (FP Concept boxes)
    lines = text.split('\n')
    result = []
    in_blockquote = False
    blockquote_lines = []

    for line in lines:
        if line.startswith('> '):
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            blockquote_lines.append(line[2:])
        else:
            if in_blockquote:
                blockquote_content = '\n'.join(blockquote_lines)
                # Check if it's an FP concept
                if '**FP Concept:' in blockquote_content:
                    result.append('<blockquote class="fp-concept">')
                elif '**Note' in blockquote_content:
                    result.append('<div class="note">')
                elif '**Important' in blockquote_content:
                    result.append('<div class="important">')
                elif '**Hint' in blockquote_content:
                    result.append('<div class="hint">')
                else:
                    result.append('<blockquote>')

                result.append(blockquote_content)

                if '**Note' in blockquote_content or '**Important' in blockquote_content or '**Hint' in blockquote_content:
                    result.append('</div>')
                else:
                    result.append('</blockquote>')
                in_blockquote = False
            result.append(line)

    text = '\n'.join(result)

    # Bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)

    # Lists
    lines = text.split('\n')
    result = []
    in_ul = False
    in_ol = False

    for line in lines:
        if re.match(r'^[-*]\s+', line):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            line = re.sub(r'^[-*]\s+', '', line)
            result.append(f'<li>{line}</li>')
        elif re.match(r'^\d+\.\s+', line):
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            line = re.sub(r'^\d+\.\s+', '', line)
            result.append(f'<li>{line}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False

            # Paragraphs
            if line.strip() and not line.startswith('<'):
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)

    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')

    text = '\n'.join(result)

    # Clean up empty paragraphs
    text = re.sub(r'<p>\s*</p>', '', text)

    return text

def advanced_markdown_to_html(text):
    """Convert markdown to HTML using the markdown library"""
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'nl2br'])

    # Pre-process code blocks with file paths
    text = re.sub(r'```(\w+)\s*\n#\s*File:\s*([^\n]+)\n(.*?)```',
                  r'<figure class="code"><figcaption>File: \2</figcaption><pre><code class="language-\1">\3</code></pre></figure>',
                  text, flags=re.DOTALL)

    html = md.convert(text)
    return html

def create_html_template(title, content, prev_link=None, next_link=None, chapter_num=None):
    """Create complete HTML page with navigation"""

    prev_html = ""
    if prev_link:
        prev_html = f'&lsaquo; <a href="{prev_link}.html">Previous</a>'

    next_html = ""
    if next_link:
        next_html = f'<a href="{next_link}.html">Next</a> &rsaquo;'

    chapter_html = ""
    if chapter_num:
        chapter_html = f'<div class="chapter">{chapter_num}</div>'

    nav_prev = f"{prev_html} &middot;" if prev_html else ""
    nav_next = f"&middot; {next_html}" if next_html else ""

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
                {nav_prev}
                <a href="00.01-contents.html">Contents</a>
                {nav_next}
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
                {prev_html}
            </div>
            <div>
                <a href="00.01-contents.html">Contents</a>
            </div>
            <div>
                {next_html}
            </div>
        </div>
    </footer>
</body>
</html>
"""

def process_chapter(md_file, output_dir):
    """Process a single markdown chapter"""

    filename = md_file.stem

    # Find chapter info
    chapter_info = next((c for c in CHAPTERS if c[0] == filename), None)
    if not chapter_info:
        print(f"⊗ Skipping {filename} - not in navigation map")
        return

    filename_base, title, prev_link, next_link = chapter_info

    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract chapter number if present
    chapter_match = re.search(r'^# Chapter (\d+(?:\.\d+)?):?\s*(.*)$', md_content, re.MULTILINE)
    chapter_num = None
    if chapter_match:
        chapter_num = f"Chapter {chapter_match.group(1)}"

    # Convert markdown to HTML
    if USE_MARKDOWN:
        html_content = advanced_markdown_to_html(md_content)
    else:
        html_content = basic_markdown_to_html(md_content)

    # Create full HTML page
    html_page = create_html_template(title, html_content, prev_link, next_link, chapter_num)

    # Write HTML file
    output_file = output_dir / f"{filename}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_page)

    print(f"✓ Created {output_file.name}")

def main():
    """Main conversion function"""

    base_dir = Path(__file__).parent
    guide_dir = base_dir / "guide"
    output_dir = base_dir / "html"

    print("=" * 60)
    print("Converting Markdown Guide to HTML")
    print("=" * 60)
    print()

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Process all markdown files that exist
    converted_count = 0
    for chapter_info in CHAPTERS:
        filename = chapter_info[0]
        md_file = guide_dir / f"{filename}.md"

        if md_file.exists():
            try:
                process_chapter(md_file, output_dir)
                converted_count += 1
            except Exception as e:
                print(f"✗ Error processing {filename}: {e}")
        else:
            print(f"⊗ Skipping {filename} (file not found)")

    print()
    print("=" * 60)
    print(f"Conversion complete! Converted {converted_count} files.")
    print(f"Open html/index.html in your browser to view the guide.")
    print("=" * 60)

if __name__ == "__main__":
    main()
