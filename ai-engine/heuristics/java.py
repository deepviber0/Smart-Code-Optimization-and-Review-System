import re
from typing import List, Dict, Any, Tuple
from ast_parser import parse_code

class JavaTreeAnalyzer:
    def __init__(self, code: str, root_node):
        self.code = code
        self.root = root_node
        self.issues = []
        self.loop_stack = []

    def add_issue(self, severity, title, description, node, category, rule_id, confidence="high"):
        line = node.start_point[0] + 1 if node else None
        self.issues.append({
            "severity": severity, "title": title, "description": description,
            "line": line, "category": category, "rule_id": rule_id, "confidence": confidence
        })

    def get_text(self, node): return self.code[node.start_byte:node.end_byte]

    def traverse(self, node):
        is_loop = node.type in ["for_statement", "while_statement", "enhanced_for_statement", "do_statement"]
        if is_loop: self.loop_stack.append(node)

        # Rule Checks
        
        # JAVA_CORR_001: Empty catch block
        if node.type == "catch_clause":
            body = node.child_by_field_name("body")
            if body and body.type == "block" and len(body.children) <= 2: # { } usually has 2 tokens
                # Check if it's really empty (ignoring comments)
                if len([c for c in body.children if not c.type.startswith("comment") and c.type not in ["{", "}"]]) == 0:
                    self.add_issue("critical", "Empty Catch Block", "Exceptions should never be swallowed silently.", node, "correctness", "JAVA_CORR_001")

        # JAVA_BP_002: Catching generic Exception
        if node.type == "catch_formal_parameter":
            type_node = node.child_by_field_name("type")
            if type_node and self.get_text(type_node) == "Exception":
                self.add_issue("warning", "Catching Generic Exception", "Catch specific exceptions instead of 'Exception'.", node, "best_practices", "JAVA_BP_002")

        # JAVA_CORR_002: String comparison with ==
        if node.type == "binary_expression":
            operator = self.get_text(node.child_by_field_name("operator") or node.children[1])
            if operator == "==":
                left = node.child_by_field_name("left") or node.children[0]
                right = node.child_by_field_name("right") or node.children[2]
                if left.type == "string_literal" or right.type == "string_literal":
                    self.add_issue("warning", "String Comparison with ==", "Use .equals() for string value comparison.", node, "correctness", "JAVA_CORR_002")

        # JAVA_PERF_001: String concatenation in loop
        if self.loop_stack and node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            operator = self.get_text(node.children[1])
            if operator == "+=":
                # This is a heuristic, we assume it might be a string if it's +=
                self.add_issue("warning", "String Concatenation in Loop", "Use StringBuilder for efficient string building in loops.", node, "performance", "JAVA_PERF_001", "medium")

        # JAVA_PERF_002: Object creation in loop
        if self.loop_stack and node.type == "object_creation_expression":
             self.add_issue("info", "Object Creation in Loop", "Consider moving object creation outside the loop if possible.", node, "performance", "JAVA_PERF_002", "low")

        # JAVA_BP_001: System.out.println
        if node.type == "method_invocation":
            obj = node.child_by_field_name("object")
            if obj and "System.out" in self.get_text(obj):
                name = node.child_by_field_name("name")
                if name and self.get_text(name) == "println":
                    self.add_issue("info", "System.out.println Detected", "Use a logger (like SLF4J or Log4j) for better log management.", node, "best_practices", "JAVA_BP_001")

            # JAVA_BP_005: Vector/Hashtable usage
            if obj and self.get_text(obj) in ["Vector", "Hashtable"]:
                 self.add_issue("warning", f"Use of {self.get_text(obj)}", 
                                f"{self.get_text(obj)} is legacy and synchronized. Use ArrayList or HashMap.", 
                                node, "best_practices", "JAVA_BP_005")

        # JAVA_BP_004: Missing try-with-resources
        if node.type == "variable_declarator":
             val = node.child_by_field_name("value")
             if val and val.type == "object_creation_expression":
                 type_name = self.get_text(val.child_by_field_name("type"))
                 if type_name in ["FileInputStream", "FileOutputStream", "BufferedReader", "Scanner", "Connection"]:
                     # Check if parent is a try-with-resources (resource_specification)
                     is_twr = False
                     p = node.parent
                     while p:
                         if p.type == "resource_specification":
                             is_twr = True; break
                         p = p.parent
                     if not is_twr:
                         self.add_issue("warning", "Resource Not in Try-With-Resources", f"{type_name} should be opened in a try-with-resources block.", node, "best_practices", "JAVA_BP_004")
                 
                 # JAVA_BP_006: Legacy Collection Types in declaration
                 if type_name in ["Vector", "Hashtable", "Stack"]:
                     self.add_issue("warning", f"Use of Legacy Collection {type_name}", 
                                    f"{type_name} is legacy. Use modern collections (ArrayList, HashMap, Deque).", 
                                    node, "best_practices", "JAVA_BP_006")

        for child in node.children:
            self.traverse(child)

        if is_loop:
            self.loop_stack.pop()

def analyze_java(code: str, tree=None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if tree is None:
        tree, confidence, error = parse_code(code, "java")
        if not tree:
            return [{"severity": "critical", "title": "Parsing Error", "description": error, "line": 1, "category": "correctness", "rule_id": "JAVA_CORR_000"}], []

    analyzer = JavaTreeAnalyzer(code, tree.root_node)
    analyzer.traverse(tree.root_node)
    
    # Regex fallbacks
    # JAVA_BP_003: Hardcoded credentials
    secret_pattern = re.compile(r'(password|passwd|secret|api_key|token|apikey)\s*=\s*"[^"]+"', re.IGNORECASE)
    for i, line in enumerate(code.splitlines(), 1):
        if secret_pattern.search(line):
            analyzer.issues.append({
                "severity": "critical", "title": "Hardcoded Credential", "description": "Sensitive data found in hardcoded string.",
                "line": i, "category": "best_practices", "rule_id": "JAVA_BP_003", "confidence": "high"
            })

    return analyzer.issues, []
