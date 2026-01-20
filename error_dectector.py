import ast

class CodeIssueDetector(ast.NodeVisitor):
    def __init__(self):
        self.assigned_vars = set()
        self.used_vars = set()
        self.imports = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.assigned_vars.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)


def detect_code_issues(code):
    issues = {
        "unused_variables": [],
        "unused_imports": [],
        "python_errors": []
    }

    # --- Detect unused variables & imports (only if AST parse works) ---
    try:
        tree = ast.parse(code)
        detector = CodeIssueDetector()
        detector.visit(tree)
        issues["unused_variables"] = list(detector.assigned_vars - detector.used_vars)
        issues["unused_imports"] = list(detector.imports - detector.used_vars)
    except SyntaxError as e:
        issues["unused_imports"] = ["Cannot detect unused imports due to syntax error."]
        issues["unused_variables"] = ["Cannot detect unused variables due to syntax error."]
        issues["python_errors"].append(f"SyntaxError: {e}")
        # continue, we still want to try runtime execution

    # --- Detect runtime errors ---
    try:
        exec(code, {})
    except Exception as e:
        issues["python_errors"].append(f"{type(e).__name__}: {e}")

    return issues
