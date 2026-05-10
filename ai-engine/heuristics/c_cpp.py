import re
from typing import List, Dict, Any, Tuple
from ast_parser import parse_code

class CppTreeAnalyzer:
    def __init__(self, code: str, root_node, language: str):
        self.code = code
        self.root = root_node
        self.language = language
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
        if node.type == "ERROR" or node.is_missing:
            self.add_issue("critical", "Syntax Error", "Detected mandatory syntax error (possibly missing semicolon or brace).", node, "correctness", "CPP_CORR_000")
            
        is_loop = node.type in ["for_statement", "while_statement", "do_statement", "for_range_loop"]
        if is_loop: self.loop_stack.append(node)

        # Rule Checks
        
        # CPP_SEC_001: gets() usage
        if node.type == "call_expression":
            fn_node = node.child_by_field_name("function")
            if fn_node:
                fn_name = self.get_text(fn_node)
                
                # Tracking allocations for leak detection
                if fn_name == "malloc":
                    self.has_allocation = True
                if fn_name == "free":
                    self.has_deallocation = True

                if fn_name == "gets":
                    self.add_issue("critical", "Dangerous Function gets() Used", "gets() has no bounds checking and is removed from modern C standards.", node, "best_practices", "CPP_SEC_001")
                
                # CPP_SEC_002: strcpy()
                if fn_name == "strcpy":
                    self.add_issue("critical", "strcpy Without Bounds Check", "Use strncpy() or strlcpy() to prevent buffer overflows.", node, "best_practices", "CPP_SEC_002")

                # CPP_SEC_005: strcat()
                if fn_name == "strcat":
                    self.add_issue("critical", "strcat Without Bounds Check", "Use strncat() to prevent buffer overflows.", node, "best_practices", "CPP_SEC_005")

                # CPP_SEC_006: rand() usage
                if fn_name == "rand":
                    self.add_issue("warning", "Use of rand()", "rand() is not cryptographically secure. Use arc4random() or modern C++ <random>.", node, "best_practices", "CPP_SEC_006")

                # CPP_SEC_004: printf format string vulnerability
                if fn_name in ["printf", "sprintf", "fprintf"]:
                    args = node.child_by_field_name("arguments")
                    if args and len(args.children) > 1:
                         first_arg = next((c for c in args.children if c.type not in ["(", ")", ","]), None)
                         if first_arg and first_arg.type != "string_literal":
                             self.add_issue("critical", "Format String Vulnerability", "Passing a non-literal string as format is dangerous.", first_arg, "best_practices", "CPP_SEC_004")

                # CPP_PERF_002: Allocation in loop
                if self.loop_stack and fn_name in ["malloc", "calloc", "realloc"]:
                     self.add_issue("warning", "Memory Allocation in Loop", "Frequent allocations in loops cause performance bottlenecks.", node, "performance", "CPP_PERF_002")

        # CPP_PERF_003: Nested Loop Detection
        if is_loop and len(self.loop_stack) > 1:
            self.add_issue("critical", "Nested Loop Performance Warning", "Detected nested loop structure. This typically results in O(n^2) complexity.", node, "performance", "CPP_PERF_003")

        # CPP_BP_002: using namespace std (C++)
        if self.language in ["cpp", "c++"] and node.type == "using_directive":
             if "std" in self.get_text(node):
                 self.add_issue("warning", "Global 'using namespace std'", "Pollutes the global namespace. Consider using 'std::' explicitly.", node, "best_practices", "CPP_BP_002", "medium")

        # CPP_BP_001: Raw pointers vs smart pointers (C++ only)
        if self.language in ["cpp", "c++"]:
            if node.type == "new_expression":
                self.add_issue("warning", "Raw 'new' Used", "Consider using std::make_unique or std::make_shared instead of raw 'new'.", node, "best_practices", "CPP_BP_001", "medium")

        # CPP_PERF_001: Large objects by value (C++ only)
        if self.language in ["cpp", "c++"] and node.type == "parameter_declaration":
             type_node = node.child_by_field_name("type")
             if type_node and type_node.type in ["type_identifier", "qualified_identifier"]:
                 is_ref = any(c.type == "&" for c in node.children)
                 is_ptr = any(c.type == "*" for c in node.children)
                 if not is_ref and not is_ptr:
                     self.add_issue("info", "Object Passed by Value", "Consider passing by const reference to avoid unnecessary copies.", node, "performance", "CPP_PERF_001", "low")

        for child in node.children:
            self.traverse(child)

        if is_loop:
            self.loop_stack.pop()

def analyze_c_cpp(code: str, tree=None, language: str = "c") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if tree is None:
        tree, confidence, error = parse_code(code, language)
        if not tree:
            return [{"severity": "critical", "title": "Parsing Error", "description": error, "line": 1, "category": "correctness", "rule_id": "CPP_CORR_000"}], []

    analyzer = CppTreeAnalyzer(code, tree.root_node, language)
    analyzer.has_allocation = False
    analyzer.has_deallocation = False
    
    analyzer.traverse(tree.root_node)
    
    # CPP_CORR_003: Memory Leak Detection
    if analyzer.has_allocation and not analyzer.has_deallocation:
        analyzer.issues.append({
            "severity": "critical", "title": "Potential Memory Leak", "description": "Detected memory allocation (malloc) without any visible deallocation (free).",
            "line": 1, "category": "correctness", "rule_id": "CPP_CORR_003", "confidence": "medium"
        })
    
    # Regex fallback
    # CPP_SEC_003: scanf without width
    if "%s" in code and "scanf" in code:
        for i, line in enumerate(code.splitlines(), 1):
            if re.search(r'scanf\s*\(\s*"[^"]*%s', line):
                 analyzer.issues.append({
                    "severity": "critical", "title": "scanf %s Without Width", "description": "Always specify buffer size in scanf, e.g., %10s.",
                    "line": i, "category": "best_practices", "rule_id": "CPP_SEC_003", "confidence": "high"
                })

    return analyzer.issues, []
