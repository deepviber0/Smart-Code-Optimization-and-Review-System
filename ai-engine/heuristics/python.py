import ast
import re
from typing import List, Dict, Any, Tuple

class PythonHeuristicAnalyzer(ast.NodeVisitor):
    def __init__(self, code: str):
        self.code = code
        self.lines = code.splitlines()
        self.issues = []
        self.steps = []
        self.current_function = None
        self.loop_stack = []

    def add_issue(self, severity, title, description, node, category, rule_id, confidence="high", step=None):
        line = node.lineno if hasattr(node, 'lineno') else None
        issue = {
            "severity": severity,
            "title": title,
            "description": description,
            "line": line,
            "category": category,
            "rule_id": rule_id,
            "confidence": confidence
        }
        self.issues.append(issue)
        if step:
            self.steps.append(step)

    def visit_Call(self, node):
        # PY_BP_001: eval() / exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec"]:
                self.add_issue("critical", f"Use of {node.func.id}()", 
                               f"{node.func.id}() is dangerous as it executes arbitrary code.", 
                               node, "best_practices", "PY_BP_001",
                               step={
                                   "what": f"Replace {node.func.id}()",
                                   "why": "It allows execution of arbitrary strings which is a massive security risk.",
                                   "how": "Use json.loads() for data or a dictionary of allowed functions."
                               })
            
            # PY_PERF_002: range(len())
            if node.func.id == "range" and len(node.args) == 1:
                arg = node.args[0]
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == "len":
                    self.add_issue("warning", "range(len()) Anti-pattern", 
                                   "Use 'for item in iterable' or 'enumerate()' instead of range(len()).", 
                                   node, "performance", "PY_PERF_002",
                                   step={
                                       "what": "Use direct iteration",
                                       "why": "It is more readable and efficient than indexing.",
                                       "how": "Change 'for i in range(len(items)):' to 'for item in items:'."
                                   })

    def visit_FunctionDef(self, node):
        # PY_CORR_001: Mutable default argument
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.add_issue("critical", "Mutable Default Argument", 
                               f"Function '{node.name}' uses a mutable default argument which is shared across calls.", 
                               node, "correctness", "PY_CORR_001",
                               step={
                                   "what": "Fix mutable default",
                                   "why": "Mutable defaults are only evaluated once, leading to shared state bugs.",
                                   "how": "Use 'arg=None' and then 'if arg is None: arg = []' inside the function."
                               })

        # PY_READ_001: Function too long
        func_lines = node.end_lineno - node.lineno
        if func_lines > 50:
            self.add_issue("info", "Function Too Long", 
                           f"Function '{node.name}' is {func_lines} lines. Consider refactoring.", 
                           node, "readability", "PY_READ_001", "medium")

        self.current_function = node
        self.generic_visit(node)
        self.current_function = None

    def visit_For(self, node):
        self.loop_stack.append(node)
        # PY_PERF_003: List comprehension vs loop (.append in loop)
        if len(node.body) == 1:
            stmt = node.body[0]
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute) and stmt.value.func.attr == "append":
                    self.add_issue("info", "Loop can be List Comprehension", 
                                   "This for loop building a list can be rewritten as a list comprehension for better performance.", 
                                   node, "performance", "PY_PERF_003", "medium")
        
        # PY_CORR_003: Modifying list while iterating
        if isinstance(node.iter, ast.Name):
            iter_name = node.iter.id
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Attribute) and sub_node.func.attr in ["remove", "pop", "append", "extend"]:
                    if isinstance(sub_node.func.value, ast.Name) and sub_node.func.value.id == iter_name:
                        self.add_issue("critical", "Modifying List During Iteration", 
                                       f"Modifying list '{iter_name}' while iterating over it can cause skipped elements or errors.", 
                                       sub_node, "correctness", "PY_CORR_003")

        # PY_PERF_004: Nested Loops (O(n^2))
        if len(self.loop_stack) > 1:
            self.add_issue("critical", "Nested Loop Performance Warning", 
                           "Nested loops detected. This may lead to O(n^2) time complexity. Consider using a dictionary for O(1) lookups.", 
                           node, "performance", "PY_PERF_004")

        # PY_PERF_005: Repeated function call in loop (e.g. range(len()))
        # (Existing PY_PERF_002 covers range(len))

        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_Compare(self, node):
        # PY_BP_002: == None
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(comparator, ast.Constant) and comparator.value is None:
                self.add_issue("warning", "Comparison with None", 
                               "Use 'is None' or 'is not None' for identity comparison with None.", 
                               node, "best_practices", "PY_BP_002")
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        # PY_BP_003: Bare except
        if node.type is None:
            self.add_issue("warning", "Bare except Clause", 
                           "Bare 'except:' catches all exceptions. Use 'except Exception:' or specific types.", 
                           node, "best_practices", "PY_BP_003")
        self.generic_visit(node)

    def visit_Constant(self, node):
        # PY_READ_003: Magic numbers
        if isinstance(node.value, (int, float)) and node.value not in [0, 1, -1, 2, 10, 100]:
            self.add_issue("info", "Magic Number Detected", 
                           f"The number '{node.value}' is used without a named constant.", 
                           node, "readability", "PY_READ_003", "low")

def analyze_python(code: str, tree=None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    try:
        ast_tree = ast.parse(code)
    except SyntaxError as e:
        return [{
            "severity": "critical",
            "title": "Syntax Error",
            "description": str(e),
            "line": e.lineno,
            "category": "correctness",
            "rule_id": "PY_CORR_000"
        }], []

    analyzer = PythonHeuristicAnalyzer(code)
    analyzer.visit(ast_tree)
    
    # Regex fallbacks
    secret_pattern = re.compile(r'(password|passwd|secret|api_key|token|access_key)\s*=\s*["\'].+["\']', re.IGNORECASE)
    for i, line in enumerate(code.splitlines(), 1):
        if secret_pattern.search(line):
            analyzer.issues.append({
                "severity": "critical",
                "title": "Hardcoded Credential",
                "description": "Possible hardcoded credential detected in string literal.",
                "line": i,
                "category": "best_practices",
                "rule_id": "PY_BP_004",
                "confidence": "high"
            })
            
    return analyzer.issues, analyzer.steps
