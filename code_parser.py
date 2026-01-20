import ast


def parse_code(code: str):
    """
    Parses Python code and returns basic structure information.
    This function NEVER crashes the app.
    """

    result = {
        "is_valid": True,
        "error": None,
        "functions": [],
        "classes": [],
        "imports": []
    }

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result["functions"].append(node.name)

            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    result["imports"].append(alias.name)

    except SyntaxError as e:
        result["is_valid"] = False
        result["error"] = f"Syntax Error: {e.msg}"

    return result
