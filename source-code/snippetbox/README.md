# SnippetBox - Example Application

This is the complete source code for the SnippetBox application built throughout the "Let's Build with Elixir and Phoenix" guide.

## What is SnippetBox?

SnippetBox is a web application for creating and sharing text snippets (code, notes, etc.) - similar to Pastebin or GitHub Gists.

### Features

- ✅ Create, view, and manage text snippets
- ✅ Set expiration dates for snippets
- ✅ User authentication and authorization
- ✅ Syntax highlighting for code
- ✅ Flash messages for user feedback
- ✅ Responsive design
- ✅ Session management
- ✅ CSRF protection
- ✅ Comprehensive tests
- ⏳ Real-time updates with LiveView (optional)
- ⏳ Full-text search

## Prerequisites

Before running this application, ensure you have:

- Elixir 1.16+ installed
- Erlang/OTP 26+ installed
- PostgreSQL 14+ installed and running
- Node.js 16+ (for asset compilation)

## Setup Instructions

### 1. Clone or Navigate to the Project

```bash
cd /path/to/elixir-phoenix/source-code/snippetbox
```

### 2. Install Dependencies

```bash
# Install Elixir dependencies
mix deps.get

# Install Node.js dependencies for assets
cd assets && npm install && cd ..

# Compile assets
mix assets.build
```

### 3. Configure Database

Update `config/dev.exs` with your PostgreSQL credentials:

```elixir
config :snippetbox, Snippetbox.Repo,
  username: "postgres",      # Your PostgreSQL username
  password: "postgres",      # Your PostgreSQL password
  hostname: "localhost",
  database: "snippetbox_dev",
  stacktrace: true,
  show_sensitive_data_on_connection_error: true,
  pool_size: 10
```

### 4. Create and Migrate Database

```bash
# Create the database
mix ecto.create

# Run migrations
mix ecto.migrate

# (Optional) Seed sample data
mix run priv/repo/seeds.exs
```

### 5. Start the Server

```bash
# Start Phoenix server
mix phx.server

# Or start with interactive shell
iex -S mix phx.server
```

Visit `http://localhost:4000` in your browser.

## Project Structure

```
snippetbox/
├── assets/           # Frontend assets (CSS, JS)
├── config/           # Application configuration
│   ├── config.exs    # Shared configuration
│   ├── dev.exs       # Development config
│   ├── prod.exs      # Production config
│   ├── runtime.exs   # Runtime config
│   └── test.exs      # Test config
├── lib/
│   ├── snippetbox/           # Core application
│   │   ├── snippets/         # Snippets context
│   │   │   ├── snippet.ex    # Snippet schema
│   │   │   └── ...
│   │   ├── accounts/         # User accounts context
│   │   │   ├── user.ex       # User schema
│   │   │   └── ...
│   │   ├── application.ex    # Application supervisor
│   │   └── repo.ex           # Database repository
│   └── snippetbox_web/       # Web interface
│       ├── controllers/      # Request handlers
│       ├── components/       # Reusable components
│       ├── live/            # LiveView modules (optional)
│       ├── endpoint.ex      # HTTP endpoint
│       ├── router.ex        # URL routing
│       └── ...
├── priv/
│   ├── repo/
│   │   ├── migrations/      # Database migrations
│   │   └── seeds.exs        # Seed data
│   └── static/              # Compiled static assets
├── test/                    # Test files
│   ├── snippetbox/          # Core tests
│   ├── snippetbox_web/      # Web tests
│   └── support/             # Test helpers
├── mix.exs                  # Project definition
└── README.md                # This file
```

## Development

### Running Tests

```bash
# Run all tests
mix test

# Run specific test file
mix test test/snippetbox_web/controllers/snippet_controller_test.exs

# Run with coverage
mix test --cover

# Run in watch mode (requires mix test.watch)
mix test.watch
```

### Interactive Console

```bash
# Start IEx with your application
iex -S mix

# Try some commands:
iex> alias Snippetbox.{Repo, Snippets.Snippet}
iex> Repo.all(Snippet)
iex> Snippetbox.Snippets.list_snippets()
```

### Database Operations

```bash
# Create a new migration
mix ecto.gen.migration add_field_to_snippets

# Run migrations
mix ecto.migrate

# Rollback last migration
mix ecto.rollback

# Reset database (drop, create, migrate)
mix ecto.reset

# Check migration status
mix ecto.migrations
```

### Code Quality

```bash
# Format code
mix format

# Check for issues with Credo (if installed)
mix credo

# Run static analysis with Dialyzer (if configured)
mix dialyzer
```

## Features by Chapter

The application is built progressively through the guide. Here's what's covered in each chapter:

**Chapter 2: Foundations**
- Basic Phoenix setup
- Routing and controllers
- Templates and layouts
- Static files

**Chapter 4: Database**
- PostgreSQL setup
- Ecto schemas and migrations
- CRUD operations
- Queries and transactions

**Chapter 5: Templates**
- Dynamic templates
- View helpers
- Template functions

**Chapter 6: Plugs**
- Custom middleware
- Security headers
- Request logging

**Chapter 8: Forms**
- Form helpers
- Validation with changesets
- Error display

**Chapter 9: Sessions**
- Session storage
- Flash messages
- State management

**Chapter 11: Authentication**
- User registration
- Login/logout
- Password hashing
- Authorization

**Chapter 12: LiveView (Optional)**
- Real-time updates
- Interactive components
- Event handling

**Chapter 13: Testing**
- Unit tests
- Integration tests
- Test coverage

## API Endpoints

The application provides these routes:

### Public Routes
```
GET  /                    # Home page (list snippets)
GET  /snippets            # List all snippets
GET  /snippets/:id        # View specific snippet
```

### Authenticated Routes
```
GET  /snippets/new        # New snippet form
POST /snippets            # Create snippet
GET  /snippets/:id/edit   # Edit snippet form
PUT  /snippets/:id        # Update snippet
DELETE /snippets/:id      # Delete snippet
```

### User Routes
```
GET  /users/register      # Registration form
POST /users/register      # Create account
GET  /users/login         # Login form
POST /users/login         # Authenticate
GET  /users/logout        # Logout
GET  /users/settings      # User settings
```

## Environment Variables

Configure these in production:

```bash
# Database
DATABASE_URL=ecto://user:pass@localhost/snippetbox_prod

# Secret key base (generate with: mix phx.gen.secret)
SECRET_KEY_BASE=your_secret_key_here

# Server
PORT=4000
PHX_HOST=example.com

# Optional: Email configuration for notifications
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
```

## Deployment

See Chapter 14 of the guide for detailed deployment instructions.

Quick start for production:

```bash
# Build a release
MIX_ENV=prod mix release

# Run the release
_build/prod/rel/snippetbox/bin/snippetbox start
```

## Troubleshooting

### Database Connection Errors

```bash
# Check PostgreSQL is running
pg_ctl status

# Reset database if needed
mix ecto.reset
```

### Port Already in Use

```bash
# Find process using port 4000
lsof -i :4000

# Kill the process or use different port
PORT=4001 mix phx.server
```

### Asset Compilation Errors

```bash
# Reinstall Node dependencies
cd assets && rm -rf node_modules && npm install && cd ..

# Rebuild assets
mix assets.build
```

### Mix Dependencies Issues

```bash
# Clean and reinstall dependencies
mix deps.clean --all
mix deps.get
mix compile
```

## Contributing

This is an example application for educational purposes. Feel free to:

- Use it as a starting point for your projects
- Modify and extend features
- Report issues or suggest improvements

## License

This example application is provided for educational purposes as part of the "Let's Build with Elixir and Phoenix" guide.

## Further Reading

- [Phoenix Framework Guides](https://hexdocs.pm/phoenix/)
- [Ecto Documentation](https://hexdocs.pm/ecto/)
- [Elixir Documentation](https://elixir-lang.org/docs.html)

## Support

For questions about this application or the guide:

- Check the guide chapters for detailed explanations
- Visit [Elixir Forum](https://elixirforum.com/)
- Check [Phoenix Forum](https://elixirforum.com/c/phoenix-forum)

Happy coding!
