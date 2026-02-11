# AGENTS.md - Agentic Coding Guidelines

## Build/Lint/Test Commands

```bash
# Setup (run these first)
source venv/bin/activate                    # Activate virtual environment
pip install -r requirements.txt             # Install dependencies

# Running the application
python api/index.py                         # Start dev server on port 5001

# Testing (pytest - not yet configured)
pip install pytest pytest-flask             # Install test dependencies first
pytest                                      # Run all tests
pytest tests/test_file.py                   # Run single test file
pytest -k test_function_name                # Run single test by name
pytest -v                                   # Run with verbose output

# Linting and Formatting (not yet configured)
pip install ruff black mypy                 # Install linting tools
ruff check .                                # Run linter
ruff check --fix .                          # Fix linting issues
black .                                     # Format code
mypy api/                                   # Type checking

# Deployment
vercel                                      # Deploy to Vercel
vercel --prod                               # Deploy to production
```

## Code Style Guidelines

### Python Conventions
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
- **Type hints**: Use type annotations for all function parameters and return values
- **Docstrings**: Google-style docstrings with Args/Returns sections for all public functions

### Import Order
1. Standard library imports (`os`, `json`)
2. Third-party imports (`flask`, `supabase`)
3. Local module imports (`.database`, `.utils`)
4. Separate each group with a blank line

### Error Handling
- Wrap all route handlers in try-except blocks
- Return JSON error responses: `{"success": false, "error": "message"}`
- Use appropriate HTTP status codes (400, 404, 500)

### API Response Format
Always return JSON with consistent structure:
```python
# Success response
{"success": True, "data": result, "message": "..."}  # 200 or 201

# Error response
{"success": False, "error": "error message"}         # 400, 404, or 500
```

### Flask Patterns
- Use decorators for routes: `@app.route('/api/<table_name>', methods=['GET'])`
- Use `request.get_json()` for JSON body parsing
- Use `request.args.to_dict()` for query parameters
- Register error handlers: `@app.errorhandler(404)`

### Supabase Patterns
- Use `get_supabase_client()` singleton function for client access
- Chain query methods: `client.table(name).select("*").eq(column, value)`
- Handle empty results gracefully

### Environment Variables
- Store in `.env` file (never commit to git)
- Load with `python-dotenv` in database module
- Access via `os.getenv()` with defaults where appropriate

### File Organization
```
api/
  index.py          # Flask app and routes
  database.py       # Supabase client and queries
  utils.py          # Helper functions (create as needed)
tests/              # Test files (create as needed)
  test_api.py
  test_database.py
```

## Security Guidelines
- Never commit `.env` or secrets
- Use Supabase anon key (not service role key) in client code
- Validate all request data before processing
- Consider adding rate limiting for production

## Notes for Agents
- No existing test suite - add pytest if writing tests
- No linting configured - can add ruff/black on request
- Project deploys to Vercel serverless
- Uses Supabase as database backend
