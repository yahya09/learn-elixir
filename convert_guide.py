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
    # Front matter
    ("00.00-front-matter", "Front Matter", None, "00.01-contents"),
    ("00.01-contents", "Contents", "00.00-front-matter", "01.00-introduction"),

    # Chapter 1: Introduction
    ("01.00-introduction", "Introduction", "00.01-contents", "01.01-prerequisites"),
    ("01.01-prerequisites", "Prerequisites", "01.00-introduction", "02.00-foundations"),

    # Chapter 2: Foundations
    ("02.00-foundations", "Foundations", "01.01-prerequisites", "02.01-project-setup"),
    ("02.01-project-setup", "Project Setup", "02.00-foundations", "02.02-web-application-basics"),
    ("02.02-web-application-basics", "Web Application Basics", "02.01-project-setup", "02.03-routing-requests"),
    ("02.03-routing-requests", "Routing Requests", "02.02-web-application-basics", "02.04-customizing-http-headers"),
    ("02.04-customizing-http-headers", "Customizing HTTP Headers", "02.03-routing-requests", "02.05-url-query-strings"),
    ("02.05-url-query-strings", "URL Query Strings", "02.04-customizing-http-headers", "02.06-project-structure"),
    ("02.06-project-structure", "Project Structure", "02.05-url-query-strings", "02.07-html-templating"),
    ("02.07-html-templating", "HTML Templating", "02.06-project-structure", "02.08-serving-static-files"),
    ("02.08-serving-static-files", "Serving Static Files", "02.07-html-templating", "02.09-the-controller-pattern"),
    ("02.09-the-controller-pattern", "The Controller Pattern", "02.08-serving-static-files", "03.00-configuration-and-error-handling"),

    # Chapter 3: Configuration and Error Handling
    ("03.00-configuration-and-error-handling", "Configuration and Error Handling", "02.09-the-controller-pattern", "03.01-managing-configuration"),
    ("03.01-managing-configuration", "Managing Configuration", "03.00-configuration-and-error-handling", "03.02-environment-variables"),
    ("03.02-environment-variables", "Environment Variables", "03.01-managing-configuration", "03.03-custom-error-responses"),
    ("03.03-custom-error-responses", "Custom Error Responses", "03.02-environment-variables", "03.04-error-pages"),
    ("03.04-error-pages", "Error Pages", "03.03-custom-error-responses", "03.05-logging"),
    ("03.05-logging", "Logging", "03.04-error-pages", "04.00-database-driven-responses"),

    # Chapter 4: Database with Ecto
    ("04.00-database-driven-responses", "Database-Driven Responses", "03.05-logging", "04.01-setting-up-postgresql"),
    ("04.01-setting-up-postgresql", "Setting Up PostgreSQL", "04.00-database-driven-responses", "04.02-creating-database-migrations"),
    ("04.02-creating-database-migrations", "Database Migrations", "04.01-setting-up-postgresql", "04.03-ecto-schemas"),
    ("04.03-ecto-schemas", "Ecto Schemas", "04.02-creating-database-migrations", "04.04-changesets-and-validations"),
    ("04.04-changesets-and-validations", "Changesets and Validations", "04.03-ecto-schemas", "04.05-crud-operations"),
    ("04.05-crud-operations", "CRUD Operations", "04.04-changesets-and-validations", "04.06-ecto-queries"),
    ("04.06-ecto-queries", "Ecto Queries", "04.05-crud-operations", "04.07-associations"),
    ("04.07-associations", "Associations", "04.06-ecto-queries", "04.08-transactions"),
    ("04.08-transactions", "Transactions", "04.07-associations", "04.09-database-best-practices"),
    ("04.09-database-best-practices", "Database Best Practices", "04.08-transactions", "05.00-dynamic-templates"),

    # Chapter 5: Dynamic Templates
    ("05.00-dynamic-templates", "Dynamic Templates", "04.09-database-best-practices", "05.01-displaying-data"),
    ("05.01-displaying-data", "Displaying Data", "05.00-dynamic-templates", "05.02-template-actions"),
    ("05.02-template-actions", "Template Actions", "05.01-displaying-data", "05.03-iterating-collections"),
    ("05.03-iterating-collections", "Iterating Collections", "05.02-template-actions", "05.04-components"),
    ("05.04-components", "Components", "05.03-iterating-collections", "05.05-layouts"),
    ("05.05-layouts", "Layouts", "05.04-components", "05.06-helpers-and-formatting"),
    ("05.06-helpers-and-formatting", "Helpers and Formatting", "05.05-layouts", "06.00-plugs-and-middleware"),

    # Chapter 6: Plugs and Middleware
    ("06.00-plugs-and-middleware", "Plugs and Middleware", "05.06-helpers-and-formatting", "06.01-understanding-plugs"),
    ("06.01-understanding-plugs", "Understanding Plugs", "06.00-plugs-and-middleware", "06.02-phoenix-pipelines"),
    ("06.02-phoenix-pipelines", "Phoenix Pipelines", "06.01-understanding-plugs", "06.03-creating-custom-plugs"),
    ("06.03-creating-custom-plugs", "Creating Custom Plugs", "06.02-phoenix-pipelines", "06.04-common-plug-patterns"),
    ("06.04-common-plug-patterns", "Common Plug Patterns", "06.03-creating-custom-plugs", "06.05-testing-plugs"),
    ("06.05-testing-plugs", "Testing Plugs", "06.04-common-plug-patterns", "07.00-advanced-routing"),

    # Chapter 7: Advanced Routing
    ("07.00-advanced-routing", "Advanced Routing", "06.05-testing-plugs", "07.01-nested-resources"),
    ("07.01-nested-resources", "Nested Resources", "07.00-advanced-routing", "07.02-scopes-and-namespaces"),
    ("07.02-scopes-and-namespaces", "Scopes and Namespaces", "07.01-nested-resources", "07.03-custom-routes"),
    ("07.03-custom-routes", "Custom Routes", "07.02-scopes-and-namespaces", "08.00-processing-forms"),

    # Chapter 8: Processing Forms
    ("08.00-processing-forms", "Processing Forms", "07.03-custom-routes", "08.01-form-basics"),
    ("08.01-form-basics", "Form Basics", "08.00-processing-forms", "08.02-phoenix-forms"),
    ("08.02-phoenix-forms", "Phoenix Forms", "08.01-form-basics", "08.03-changesets-in-forms"),
    ("08.03-changesets-in-forms", "Changesets in Forms", "08.02-phoenix-forms", "08.04-file-uploads"),
    ("08.04-file-uploads", "File Uploads", "08.03-changesets-in-forms", "08.05-form-validation"),
    ("08.05-form-validation", "Form Validation", "08.04-file-uploads", "08.06-form-security"),
    ("08.06-form-security", "Form Security", "08.05-form-validation", "09.00-sessions-and-state"),

    # Chapter 9: Sessions and State
    ("09.00-sessions-and-state", "Sessions and State", "08.06-form-security", "09.01-session-management"),
    ("09.01-session-management", "Session Management", "09.00-sessions-and-state", "09.02-flash-messages"),
    ("09.02-flash-messages", "Flash Messages", "09.01-session-management", "09.03-cookies"),
    ("09.03-cookies", "Cookies", "09.02-flash-messages", "09.04-ets-and-caching"),
    ("09.04-ets-and-caching", "ETS and Caching", "09.03-cookies", "10.00-security"),

    # Chapter 10: Security
    ("10.00-security", "Security", "09.04-ets-and-caching", "10.01-https-and-tls"),
    ("10.01-https-and-tls", "HTTPS and TLS", "10.00-security", "10.02-csrf-protection"),
    ("10.02-csrf-protection", "CSRF Protection", "10.01-https-and-tls", "10.03-sql-injection"),
    ("10.03-sql-injection", "SQL Injection", "10.02-csrf-protection", "10.04-xss-prevention"),
    ("10.04-xss-prevention", "XSS Prevention", "10.03-sql-injection", "10.05-security-headers"),
    ("10.05-security-headers", "Security Headers", "10.04-xss-prevention", "10.06-common-vulnerabilities"),
    ("10.06-common-vulnerabilities", "Common Vulnerabilities", "10.05-security-headers", "11.00-authentication"),

    # Chapter 11: Authentication
    ("11.00-authentication", "Authentication", "10.06-common-vulnerabilities", "11.01-password-hashing"),
    ("11.01-password-hashing", "Password Hashing", "11.00-authentication", "11.02-user-registration"),
    ("11.02-user-registration", "User Registration", "11.01-password-hashing", "11.03-login-logout"),
    ("11.03-login-logout", "Login and Logout", "11.02-user-registration", "11.04-remember-me"),
    ("11.04-remember-me", "Remember Me", "11.03-login-logout", "11.05-password-reset"),
    ("11.05-password-reset", "Password Reset", "11.04-remember-me", "11.06-email-verification"),
    ("11.06-email-verification", "Email Verification", "11.05-password-reset", "11.07-oauth"),
    ("11.07-oauth", "OAuth Integration", "11.06-email-verification", "12.00-liveview"),

    # Chapter 12: LiveView
    ("12.00-liveview", "Phoenix LiveView", "11.07-oauth", "12.01-liveview-basics"),
    ("12.01-liveview-basics", "LiveView Basics", "12.00-liveview", "12.02-liveview-forms"),
    ("12.02-liveview-forms", "LiveView Forms", "12.01-liveview-basics", "12.03-live-components"),
    ("12.03-live-components", "Live Components", "12.02-liveview-forms", "12.04-real-time-features"),
    ("12.04-real-time-features", "Real-Time Features", "12.03-live-components", "13.00-testing"),

    # Chapter 13: Testing
    ("13.00-testing", "Testing", "12.04-real-time-features", "13.01-unit-testing"),
    ("13.01-unit-testing", "Unit Testing", "13.00-testing", "13.02-controller-testing"),
    ("13.02-controller-testing", "Controller Testing", "13.01-unit-testing", "13.03-integration-testing"),
    ("13.03-integration-testing", "Integration Testing", "13.02-controller-testing", "13.04-liveview-testing"),
    ("13.04-liveview-testing", "LiveView Testing", "13.03-integration-testing", "13.05-database-testing"),
    ("13.05-database-testing", "Database Testing", "13.04-liveview-testing", "13.06-test-best-practices"),
    ("13.06-test-best-practices", "Test Best Practices", "13.05-database-testing", "14.00-deployment"),

    # Chapter 14: Deployment
    ("14.00-deployment", "Deployment", "13.06-test-best-practices", "14.01-releases"),
    ("14.01-releases", "Elixir Releases", "14.00-deployment", "14.02-docker"),
    ("14.02-docker", "Docker Deployment", "14.01-releases", "14.03-fly-io"),
    ("14.03-fly-io", "Fly.io Deployment", "14.02-docker", "14.04-production-config"),
    ("14.04-production-config", "Production Config", "14.03-fly-io", "14.05-monitoring"),
    ("14.05-monitoring", "Monitoring", "14.04-production-config", "15.00-conclusion"),

    # Conclusion and Appendix
    ("15.00-conclusion", "Conclusion", "14.05-monitoring", "16.00-further-reading"),
    ("16.00-further-reading", "Further Reading", "15.00-conclusion", "17.00-guided-exercises"),

    # Chapter 17: Exercises
    ("17.00-guided-exercises", "Guided Exercises", "16.00-further-reading", "17.01-foundations-exercises"),
    ("17.01-foundations-exercises", "Foundations Exercises", "17.00-guided-exercises", "17.02-database-exercises"),
    ("17.02-database-exercises", "Database Exercises", "17.01-foundations-exercises", "17.03-web-exercises"),
    ("17.03-web-exercises", "Web Layer Exercises", "17.02-database-exercises", "17.04-auth-exercises"),
    ("17.04-auth-exercises", "Authentication Exercises", "17.03-web-exercises", "17.05-liveview-exercises"),
    ("17.05-liveview-exercises", "LiveView Exercises", "17.04-auth-exercises", "17.06-deployment-exercises"),
    ("17.06-deployment-exercises", "Deployment Exercises", "17.05-liveview-exercises", None),
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
