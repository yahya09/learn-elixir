# HTML Version of the Guide

This directory contains the HTML version of "Let's Build with Elixir and Phoenix" guide for easy browser navigation.

## Viewing the Guide

**Simply open `index.html` in your web browser:**

```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html

# Or just double-click index.html in your file explorer
```

## Navigation

- **Home**: `index.html` - Main landing page
- **Contents**: `00.01-contents.html` - Full table of contents
- **Start Reading**: `01.00-introduction.html` - Begin the guide

Each page has navigation links:
- **Header**: Shows current location and quick navigation
- **Footer**: Previous/Next chapter buttons
- **Contents link**: Always available to jump to table of contents

## What's Included

All completed guide chapters have been converted from markdown to HTML:

✅ **Chapter 0**: Front matter and contents
✅ **Chapter 1**: Introduction and prerequisites
✅ **Chapter 2**: Foundations (4 sections)
✅ **Chapter 4**: Database overview
✅ **Chapter 15**: Conclusion
✅ **Chapter 16**: Further reading resources
✅ **Chapter 17**: Guided exercises

## Features

- **Clean, readable design** - Optimized for long-form reading
- **Syntax-highlighted code** - All code examples properly formatted
- **Responsive layout** - Works on desktop, tablet, and mobile
- **Keyboard navigation** - Use ← and → arrow keys (if enabled)
- **Print-friendly** - CSS optimized for printing

## Updating the HTML

If markdown files are updated, regenerate HTML files:

```bash
# From the project root directory
python3 convert_guide.py

# Or with better markdown formatting (requires markdown library)
pip3 install markdown
python3 convert_guide.py
```

## File Structure

```
html/
├── index.html                      # Main landing page
├── 00.00-front-matter.html         # Front matter
├── 00.01-contents.html             # Table of contents
├── 01.00-introduction.html         # Chapter 1
├── 01.01-prerequisites.html        # Chapter 1.1
├── ...                             # Other chapters
├── assets/
│   └── css/
│       └── main.css                # Stylesheet
└── README.md                       # This file
```

## Styling

The guide uses a custom stylesheet (`assets/css/main.css`) inspired by professional technical documentation:

- **Colors**: Purple/violet theme for Elixir
- **Typography**: System fonts for readability
- **Code blocks**: Distinct formatting with file paths
- **Special sections**: Styled notes, hints, and FP concept boxes

## Browser Compatibility

Tested and works in:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Opera

## Notes

- The HTML is generated from markdown source files in `/guide`
- Original markdown files are preserved and unmodified
- Both markdown and HTML versions are maintained
- HTML provides better reading experience with navigation
- Markdown is better for editing and version control

## Troubleshooting

**Styles not loading?**
- Ensure `assets/css/main.css` exists
- Check that you're opening from the `html/` directory

**Links not working?**
- All links are relative
- Keep all HTML files in the same directory
- Don't move files without updating links

**Want better formatting?**
```bash
# Install Python markdown library
pip3 install markdown

# Regenerate HTML
python3 convert_guide.py
```

## Feedback

Found an issue? The source files are in `/guide` directory. Report issues or contribute to the markdown source.

---

**Happy reading! 📚**
