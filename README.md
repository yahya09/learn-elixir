# Let's Build with Elixir and Phoenix

A comprehensive guide to building professional web applications with Elixir and Phoenix Framework.

## About This Guide

This guide teaches you how to build a complete web application using Elixir and Phoenix Framework from scratch. We'll build **SnippetBox** - a pastebin-style application where users can create, view, and share text snippets.

## Who Is This For?

This guide is designed for **senior software engineers** who:
- Have experience with languages like Python, PHP, C#, or JavaScript
- Are new to functional programming or have minimal FP experience
- Want to learn practical web development with Elixir and Phoenix
- Prefer hands-on, code-driven learning

## What You'll Learn

Throughout this guide, you'll learn:

- **Elixir Fundamentals**: Pattern matching, immutability, pipe operator, and functional programming concepts
- **Phoenix Framework**: Controllers, views, templates, contexts, and the Phoenix request lifecycle
- **Ecto**: Database migrations, schemas, queries, and changesets
- **Plugs**: Middleware pattern for composable request processing
- **LiveView**: Real-time, interactive web interfaces without JavaScript
- **Authentication**: User registration, login, sessions, and authorization
- **Testing**: Unit tests, integration tests, and test-driven development with ExUnit
- **Deployment**: Creating releases and deploying to production

## Project Structure

```
elixir-phoenix/
├── README.md                  # This file
├── guide/                     # Tutorial chapters (markdown)
│   ├── 00.00-front-matter.md
│   ├── 00.01-contents.md
│   ├── 01.00-introduction.md
│   └── ...
└── source-code/              # Example application code
    └── snippetbox/           # Complete SnippetBox application
```

## Prerequisites

Before starting this guide, you should have:

- Elixir 1.16+ installed
- Erlang/OTP 26+ installed
- PostgreSQL 14+ installed
- Basic command line familiarity
- A code editor (VS Code, IntelliJ, etc.)

## Getting Started

Start by reading the guide chapters in order:

1. [Introduction](guide/01.00-introduction.md)
2. [Prerequisites](guide/01.01-prerequisites.md)
3. [Foundations](guide/02.00-foundations.md)

Each chapter builds on the previous one, gradually adding features to the SnippetBox application.

## Conventions

- **Code blocks** show complete, runnable code with file paths
- **Terminal commands** are prefixed with `$`
- **FP Concepts** sections introduce functional programming ideas with references
- **Additional Information** sections provide deeper technical details

## Learning Approach

This guide emphasizes:

1. **Practical Application**: Write real code that works
2. **Progressive Complexity**: Start simple, add features incrementally
3. **Best Practices**: Learn idiomatic Elixir and Phoenix patterns
4. **Functional Thinking**: Understand FP concepts in context
5. **Professional Quality**: Write production-ready code

## Related Resources

- [Official Elixir Documentation](https://hexdocs.pm/elixir/)
- [Phoenix Framework Guides](https://hexdocs.pm/phoenix/)
- [Ecto Documentation](https://hexdocs.pm/ecto/)
- [Elixir Forum](https://elixirforum.com/)
- [Elixir School](https://elixirschool.com/)

## About Functional Programming

If you're coming from object-oriented languages, Elixir will introduce you to functional programming concepts:

- **Immutability**: Data never changes; transformations create new data
- **Pure Functions**: Functions with no side effects
- **Pattern Matching**: Destructuring and matching data structures
- **Pipelines**: Chaining function calls for readable data transformations
- **Recursion**: Looping through recursive function calls

Don't worry - we'll introduce these concepts gradually as we build the application.

## License

This guide is provided for educational purposes.

## Feedback

Found an issue or have suggestions? Please open an issue or submit a pull request.

---

Let's begin your journey into Elixir and Phoenix web development!
