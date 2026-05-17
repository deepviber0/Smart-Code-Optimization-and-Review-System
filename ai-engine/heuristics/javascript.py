import re
from typing import List, Dict, Any, Tuple
from ast_parser import parse_code

class JSTreeAnalyzer:
    def __init__(self, code: str, root_node):
        self.code = code
        self.root = root_node
        self.issues = []
        self.steps = []
        self.loop_nodes = []
        self.function_nesting = 0
        self.variables_in_scope = set()

    def add_issue(self, severity, title, description, node, category, rule_id, confidence="high"):
        line = node.start_point[0] + 1 if node else None
        self.issues.append({
            "severity": severity,
            "title": title,
            "description": description,
            "line": line,
            "category": category,
            "rule_id": rule_id,
            "confidence": confidence
        })

    def get_text(self, node):
        return self.code[node.start_byte:node.end_byte]

    def traverse(self, node):
        # Track loop depth
        is_loop = node.type in ["for_statement", "while_statement", "do_statement", "for_in_statement"]
        if is_loop:
            self.loop_nodes.append(node)


        

        if node.type == "variable_declaration" and self.get_text(node).startswith("var "):
            self.add_issue("warning", "Use of 'var'", 
                           "Use 'let' or 'const' instead of 'var' for better scoping.", 
                           node, "best_practices", "JS_BP_001")


        if node.type == "call_expression":
            func_name = self.get_text(node.child_by_field_name("function") or node.children[0])
            if func_name == "eval":
                self.add_issue("critical", "Use of eval()", 
                               "eval() is a major security risk and performance bottleneck.", 
                               node, "best_practices", "JS_BP_002")
            

            if self.loop_nodes:
                if "console.log" in func_name:
                    self.add_issue("warning", "console.log in Loop", 
                                   "Frequent I/O in loops can significantly slow down execution.", 
                                   node, "performance", "JS_PERF_001")
                
                if any(x in func_name for x in ["getElementById", "getElementsBy", "querySelector"]):
                    self.add_issue("warning", "Expensive DOM Query in Loop", 
                                   "DOM lookups are extremely slow. Cache the element reference outside the loop to avoid redundant layout thrashing.", 
                                   node, "performance", "JS_PERF_002")


            if node.type in ["for_statement", "while_statement"] and len(self.loop_nodes) > 1:
                 self.add_issue("critical", "Nested Loop Performance Warning", 
                                "Detected nested loop structure. This typically results in O(n^2) complexity. Consider using a Map or Set for O(1) lookups.", 
                                node, "performance", "JS_PERF_007")


            if self.loop_nodes and any(x in func_name for x in [".filter", ".find", ".includes"]):
                self.add_issue("warning", "Linear Search in Loop", 
                               "Performing a linear search (filter/find) inside a loop creates O(n^2) complexity. Use a Map or Set for O(1) lookups.", 
                               node, "performance", "JS_PERF_008")


            if "document.write" in func_name:
                self.add_issue("critical", "Use of document.write()", 
                               "document.write() is an anti-pattern that can break page rendering.", 
                               node, "best_practices", "JS_PERF_003")


        if node.type == "binary_expression":
            operator = self.get_text(node.child_by_field_name("operator") or node.children[1])
            if operator == "==":
                right_text = self.get_text(node.child_by_field_name("right") or node.children[2])
                if right_text == "null":

                    self.add_issue("warning", "Loose Null Check", 
                                   "Use === null for explicit checks or just check truthiness.", 
                                   node, "correctness", "JS_CORR_003")
                else:
                    self.add_issue("warning", "Loose Equality Used", 
                                   "Use '===' to avoid unexpected type coercion.", 
                                   node, "correctness", "JS_CORR_002")
            

            if operator in ["==", "===", "!=", "!=="]:
                left = self.get_text(node.children[0])
                right = self.get_text(node.children[2])
                if left == "NaN" or right == "NaN":
                    self.add_issue("critical", "NaN Comparison", 
                                   "NaN is not equal to itself. Use isNaN() or Number.isNaN().", 
                                   node, "correctness", "JS_CORR_005")


        if node.type == "for_statement":
            init = node.child_by_field_name("initializer")
            if init and init.type == "assignment_expression":
                self.add_issue("critical", "Undeclared Loop Variable", 
                               "Loop counter is implicitly global. Declare it with 'let'.", 
                               init, "correctness", "JS_CORR_001")


        is_function = node.type in ["function_declaration", "arrow_function", "function_expression"]
        if is_function:
            self.function_nesting += 1
            if self.function_nesting > 3:
                self.add_issue("warning", "Callback Hell / Deep Nesting", 
                               f"Functions are nested {self.function_nesting} levels deep. Consider refactoring with async/await.", 
                               node, "best_practices", "JS_BP_005")


        if self.loop_nodes and is_function:
             self.add_issue("info", "Function Created in Loop", 
                            "Creating functions inside a loop is inefficient and can cause memory issues.", 
                            node, "performance", "JS_PERF_006", "medium")


        if node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            if left and ".innerHTML" in self.get_text(left):
                self.add_issue("warning", "Use of innerHTML", 
                               "Using innerHTML can lead to XSS vulnerabilities. Use textContent instead.", 
                               node, "best_practices", "JS_BP_003")


        if node.type == "with_statement":
            self.add_issue("critical", "Use of 'with' Statement", 
                           "The 'with' statement is deprecated and makes code unpredictable.", 
                           node, "best_practices", "JS_BP_006")

        for child in node.children:
            self.traverse(child)

        if is_loop:
            self.loop_nodes.pop()
        
        if is_function:
            self.function_nesting -= 1

def analyze_javascript(code: str, tree=None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if tree is None:
        tree, confidence, error = parse_code(code, "javascript")
        if not tree:
            return [{
                "severity": "critical", "title": "Parsing Error", "description": error or "Unknown error",
                "line": 1, "category": "correctness", "rule_id": "JS_CORR_000"
            }], []

    analyzer = JSTreeAnalyzer(code, tree.root_node)
    analyzer.traverse(tree.root_node)
    
    return analyzer.issues, []
