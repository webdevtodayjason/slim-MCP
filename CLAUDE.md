# Claude Tools Project Guide

## Environment Setup & Run Commands
```bash
# Create conda environment with Python 3.11
conda create -n mcp-tools python=3.11

# Activate environment
conda activate mcp-tools

# Install with uv (preferred)
uv pip install -e .

# Alternative: Install with pip
pip install -e .

# Run the application
python -m claude_tools.main
```

## Configuration
### Claude Config
```json
{
    "mcpServers": {
        "claude-tools": {
            "command": "/Users/jasonbrashear/miniconda3/envs/claude-tools/bin/python",
            "args": ["-m", "claude_tools.main"]
        }
    }
}
```

### Cursor Config
```
NAME: claude-tools
TYPE: command
COMMAND: /Users/jasonbrashear/miniconda3/envs/claude-tools/bin/python -m claude_tools.main
```

## Code Style Guidelines
- Follow PEP 8 conventions
- Use Google-style docstrings for functions and classes
- Type annotations required for all function parameters and return values
- Constants defined at module level in UPPER_CASE
- Imports ordered: standard library, third-party, local
- Error handling: use try/except blocks with specific exceptions
- Function names use snake_case
- Class names use PascalCase
- Prefer async/await for I/O operations
- Each tool function should have a clear single responsibility
- Use meaningful variable names that describe purpose