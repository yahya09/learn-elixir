# Git Workflow Guide

This document explains how to use git to track changes to the Elixir/Phoenix guide.

## Repository Information

**Repository Location**: `/Users/yahya/Development/learn/elixir-phoenix`

**Initial Commit**: 80afe83 - Complete guide structure with 12 chapters

## Current Status

```bash
# View repository status
git status

# View commit history
git log

# View changes
git diff
```

## Basic Git Commands

### Checking Status

```bash
# See what files have changed
git status

# See what's changed in detail
git diff

# See staged changes
git diff --staged
```

### Making Changes

When you edit files in the guide:

```bash
# 1. Check what changed
git status

# 2. Review your changes
git diff

# 3. Stage files for commit
git add guide/02.04-customizing-http-headers.md
# Or add all changed files
git add .

# 4. Commit with a message
git commit -m "Add Chapter 2.4: Customizing HTTP Headers"
```

### Viewing History

```bash
# View commit history
git log

# View compact history
git log --oneline

# View last 5 commits
git log --oneline -5

# View changes in a commit
git show <commit-hash>

# View file history
git log -- guide/01.00-introduction.md
```

## Recommended Workflow

### 1. When Starting Work

```bash
# Check current status
git status

# Make sure you're on main branch
git branch
```

### 2. Making Changes

Edit your files as needed (guide chapters, HTML, etc.)

### 3. Committing Changes

```bash
# See what you changed
git status
git diff

# Add files to stage
git add guide/new-chapter.md
# or
git add .

# Commit with descriptive message
git commit -m "Add Chapter X: Topic name

- Added section on X
- Included Y examples
- Updated table of contents"
```

### 4. When Regenerating HTML

```bash
# After editing markdown and running convert_guide.py
git add guide/
git add html/
git commit -m "Update Chapter X and regenerate HTML

- Updated markdown content
- Regenerated HTML files
- Fixed typos in code examples"
```

## Commit Message Guidelines

### Good Commit Messages

```bash
# Format: Short summary (50 chars or less)

git commit -m "Add Chapter 3.1: Managing Configuration"

# With details:
git commit -m "Add Chapter 8: Processing Forms

- Cover form helpers
- Explain changeset validation
- Add form examples with error handling
- Update table of contents"

# For fixes:
git commit -m "Fix code example in Chapter 2.2

- Correct Elixir syntax in router example
- Update HTML formatting"

# For updates:
git commit -m "Update prerequisites with Elixir 1.17

- Bump Elixir version requirement
- Update installation instructions
- Add note about OTP 27"
```

### Commit Message Structure

```
Short summary (imperative mood)

- Bullet point describing change
- Another change detail
- Reference to related chapters

Optional: More context or reasoning
```

## Common Scenarios

### Scenario 1: Adding a New Chapter

```bash
# Create the markdown file
vim guide/03.01-managing-configuration.md

# Generate HTML
python3 convert_guide.py

# Update table of contents if needed
vim guide/00.01-contents.md
python3 convert_guide.py

# Commit everything
git add guide/03.01-managing-configuration.md
git add html/03.01-managing-configuration.html
git add guide/00.01-contents.md
git add html/00.01-contents.html
git commit -m "Add Chapter 3.1: Managing Configuration Settings

- Explain Phoenix config system
- Cover environment-specific configuration
- Add examples for dev, test, prod
- Update table of contents"
```

### Scenario 2: Fixing a Typo

```bash
# Edit the file
vim guide/01.00-introduction.md

# Regenerate HTML
python3 convert_guide.py

# Commit
git add guide/01.00-introduction.md html/01.00-introduction.html
git commit -m "Fix typo in Chapter 1 introduction"
```

### Scenario 3: Major Update to Multiple Chapters

```bash
# Edit multiple files
vim guide/02.01-project-setup.md
vim guide/02.02-web-application-basics.md

# Regenerate HTML
python3 convert_guide.py

# Review changes
git status
git diff guide/

# Add all changes
git add .

# Commit with detailed message
git commit -m "Update Chapter 2 with Phoenix 1.7 changes

- Update project setup for Phoenix 1.7
- Add verified routes examples
- Update code examples to use new syntax
- Regenerate all HTML files
- Add note about breaking changes from 1.6"
```

### Scenario 4: Viewing What Changed

```bash
# See what files changed
git status

# See what changed in a file
git diff guide/01.00-introduction.md

# See last commit
git show

# Compare with 3 commits ago
git diff HEAD~3
```

## Branch Strategy (Optional)

For larger changes, you might want to use branches:

```bash
# Create a new branch for a feature
git checkout -b add-authentication-chapter

# Make your changes
vim guide/11.00-user-authentication.md
python3 convert_guide.py

# Commit on branch
git add .
git commit -m "Add Chapter 11: User Authentication"

# Switch back to main
git checkout main

# Merge the branch
git merge add-authentication-chapter

# Delete the branch
git branch -d add-authentication-chapter
```

## Undoing Changes

### Undo Unstaged Changes

```bash
# Discard changes to a file
git checkout -- guide/01.00-introduction.md

# Discard all unstaged changes
git checkout -- .
```

### Undo Staged Changes

```bash
# Unstage a file
git reset HEAD guide/01.00-introduction.md

# Unstage all files
git reset HEAD
```

### Undo Last Commit

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1
```

### Amend Last Commit

```bash
# Fix last commit message
git commit --amend -m "New commit message"

# Add forgotten files to last commit
git add forgotten-file.md
git commit --amend --no-edit
```

## Checking History

### View File Changes Over Time

```bash
# See when file was changed
git log --follow guide/01.00-introduction.md

# See actual changes
git log -p guide/01.00-introduction.md

# See who changed what (if multiple authors)
git blame guide/01.00-introduction.md
```

### Search Commits

```bash
# Find commits with specific text
git log --grep="authentication"

# Find commits that changed specific text
git log -S "pattern matching"
```

## Best Practices

### ✅ Do

- Commit often with clear messages
- Review changes before committing (`git diff`)
- Use descriptive commit messages
- Commit logical chunks of work
- Regenerate HTML after markdown changes
- Keep commits focused on one topic

### ❌ Don't

- Commit broken code or half-finished chapters
- Use vague commit messages ("fix stuff", "updates")
- Commit generated files without source changes
- Make massive commits with unrelated changes
- Forget to regenerate HTML after markdown edits

## Quick Reference

```bash
# Daily workflow
git status                          # Check status
git diff                            # Review changes
git add .                           # Stage all changes
git commit -m "Message"             # Commit changes
git log --oneline                   # View history

# When editing guide
1. Edit markdown files
2. Run: python3 convert_guide.py
3. Run: git add .
4. Run: git commit -m "Descriptive message"

# View information
git status                          # Current state
git log                             # Commit history
git diff                            # Unstaged changes
git diff --staged                   # Staged changes
git show                            # Last commit

# Undo operations
git checkout -- file                # Discard changes
git reset HEAD file                 # Unstage file
git reset --soft HEAD~1             # Undo last commit
```

## Backup Strategy

Your repository is currently local. To back up to GitHub:

```bash
# Create a GitHub repository, then:
git remote add origin https://github.com/yourusername/elixir-phoenix-guide.git
git branch -M main
git push -u origin main
```

## Repository Structure

```
.git/                           # Git repository data
├── HEAD                        # Current branch
├── config                      # Repository config
├── objects/                    # All file versions
└── refs/                       # Branch pointers

Working Directory:
├── guide/                      # Source markdown files
├── html/                       # Generated HTML files
├── .gitignore                  # Ignored files
└── [other project files]
```

## Getting Help

```bash
# Git help
git help
git help commit
git help log

# Quick command help
git status --help
git commit --help
```

## Summary

**Basic Daily Workflow:**

1. `git status` - See what changed
2. `git diff` - Review changes
3. `git add .` - Stage changes
4. `git commit -m "Message"` - Save changes
5. `git log` - View history

**Remember**: Commit early, commit often, use clear messages!

---

Happy tracking! 🎯
