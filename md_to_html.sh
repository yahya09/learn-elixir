#!/bin/bash

# Simple Markdown to HTML converter for the guide
# This creates HTML files from markdown with proper navigation

GUIDE_DIR="guide"
HTML_DIR="html"

# Chapter navigation mapping: filename|title|prev|next
declare -a CHAPTERS=(
    "00.00-front-matter|Front Matter||00.01-contents"
    "00.01-contents|Contents|00.00-front-matter|01.00-introduction"
    "01.00-introduction|Introduction|00.01-contents|01.01-prerequisites"
    "01.01-prerequisites|Prerequisites|01.00-introduction|02.00-foundations"
    "02.00-foundations|Foundations|01.01-prerequisites|02.01-project-setup"
    "02.01-project-setup|Project Setup|02.00-foundations|02.02-web-application-basics"
    "02.02-web-application-basics|Web Application Basics|02.01-project-setup|02.03-routing-requests"
    "02.03-routing-requests|Routing Requests|02.02-web-application-basics|04.00-database-driven-responses"
    "04.00-database-driven-responses|Database-Driven Responses|02.03-routing-requests|15.00-conclusion"
    "15.00-conclusion|Conclusion|04.00-database-driven-responses|16.00-further-reading"
    "16.00-further-reading|Further Reading|15.00-conclusion|17.00-guided-exercises"
    "17.00-guided-exercises|Guided Exercises|16.00-further-reading|"
)

# Function to escape HTML entities
escape_html() {
    sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#39;/g'
}

# Function to convert basic markdown to HTML
convert_markdown() {
    local content="$1"

    # Headers
    content=$(echo "$content" | sed -E 's/^# (.+)$/<h1>\1<\/h1>/g')
    content=$(echo "$content" | sed -E 's/^## (.+)$/<h2>\1<\/h2>/g')
    content=$(echo "$content" | sed -E 's/^### (.+)$/<h3>\1<\/h3>/g')
    content=$(echo "$content" | sed -E 's/^#### (.+)$/<h4>\1<\/h4>/g')

    # Bold and italic
    content=$(echo "$content" | sed -E 's/\*\*([^*]+)\*\*/<strong>\1<\/strong>/g')
    content=$(echo "$content" | sed -E 's/\*([^*]+)\*/<em>\1<\/em>/g')

    # Inline code
    content=$(echo "$content" | sed -E 's/`([^`]+)`/<code>\1<\/code>/g')

    # Links
    content=$(echo "$content" | sed -E 's/\[([^\]]+)\]\(([^\)]+)\)/<a href="\2">\1<\/a>/g')

    # Paragraphs (lines that don't start with < are paragraphs)
    content=$(echo "$content" | awk '
        BEGIN { in_para=0; in_list=0; in_code=0; }
        /^```/ {
            if (in_code) { print "</code></pre></figure>"; in_code=0; }
            else { print "<figure class=\"code\"><pre><code>"; in_code=1; }
            next;
        }
        in_code { print; next; }
        /^[-*] / {
            if (!in_list) { print "<ul>"; in_list=1; }
            gsub(/^[-*] /, "");
            print "<li>" $0 "</li>";
            next;
        }
        /^[0-9]+\. / {
            if (!in_list) { print "<ol>"; in_list=1; }
            gsub(/^[0-9]+\. /, "");
            print "<li>" $0 "</li>";
            next;
        }
        /^</ {
            if (in_list) { print "</ul>"; in_list=0; }
            if (in_para) { print "</p>"; in_para=0; }
            print; next;
        }
        /^$/ {
            if (in_list) { print "</ul>"; in_list=0; }
            if (in_para) { print "</p>"; in_para=0; }
            print; next;
        }
        {
            if (in_list) { print "</ul>"; in_list=0; }
            if (!in_para) { print "<p>"; in_para=1; }
            print;
        }
        END {
            if (in_list) print "</ul>";
            if (in_para) print "</p>";
            if (in_code) print "</code></pre></figure>";
        }
    ')

    echo "$content"
}

# Function to create HTML page
create_html_page() {
    local filename="$1"
    local title="$2"
    local prev="$3"
    local next="$4"
    local content="$5"

    # Build navigation
    local prev_nav=""
    local next_nav=""

    if [ -n "$prev" ]; then
        prev_nav="&lsaquo; <a href=\"${prev}.html\">Previous</a> &middot; "
    fi

    if [ -n "$next" ]; then
        next_nav=" &middot; <a href=\"${next}.html\">Next</a> &rsaquo;"
    fi

    # Extract chapter number if present
    local chapter_num=""
    if echo "$content" | grep -q "^# Chapter [0-9]"; then
        chapter_num=$(echo "$content" | grep "^# Chapter" | head -1 | sed -E 's/^# (Chapter [0-9.]+).*/\1/')
        chapter_num="<div class=\"chapter\">$chapter_num</div>"
        # Remove chapter heading from content as we'll add it separately
        content=$(echo "$content" | sed '1d')
    fi

    # Create HTML file
    cat > "${HTML_DIR}/${filename}.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>$title &mdash; Let's Build with Elixir and Phoenix</title>
    <link rel="stylesheet" type="text/css" href="assets/css/main.css">
</head>
<body>
    <header>
        <div class="wrapper">
            <div>
                <a href="index.html">Let's Build with Elixir and Phoenix</a>
                <span class="crumbs">&rsaquo; $title</span>
            </div>
            <div>
                ${prev_nav}<a href="00.01-contents.html">Contents</a>${next_nav}
            </div>
        </div>
    </header>
    <main class="wrapper text">
        $chapter_num
        $(convert_markdown "$content")
    </main>
    <footer>
        <div class="wrapper">
            <div>
                $([ -n "$prev" ] && echo "&lsaquo; <a href=\"${prev}.html\">Previous</a>" || echo "")
            </div>
            <div>
                <a href="00.01-contents.html">Contents</a>
            </div>
            <div>
                $([ -n "$next" ] && echo "<a href=\"${next}.html\">Next</a> &rsaquo;" || echo "")
            </div>
        </div>
    </footer>
</body>
</html>
EOF

    echo "Created ${filename}.html"
}

# Main conversion loop
echo "Converting markdown files to HTML..."

for chapter_info in "${CHAPTERS[@]}"; do
    IFS='|' read -r filename title prev next <<< "$chapter_info"

    md_file="${GUIDE_DIR}/${filename}.md"

    if [ -f "$md_file" ]; then
        echo "Processing $filename..."
        content=$(cat "$md_file")
        create_html_page "$filename" "$title" "$prev" "$next" "$content"
    else
        echo "Skipping $filename (file not found)"
    fi
done

echo ""
echo "Conversion complete! Open html/index.html in your browser."
