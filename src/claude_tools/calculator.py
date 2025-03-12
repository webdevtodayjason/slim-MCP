import math

def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression.
    Args:
        expression: A mathematical expression as a string (e.g. "2 + 2", "sin(30)")
    """
    try:
        # Replace common math functions with their python equivalents
        expression = expression.replace("^", "**")
        
        # Create a safe namespace with only math functions
        safe_dict = {
            'abs': abs, 'round': round,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
            'pi': math.pi, 'e': math.e
        }
        
        # Evaluate the expression in the safe namespace
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def register_calculator_tools(mcp):
    """Register all calculator tools with the MCP server."""
    mcp.tool()(calculate)
