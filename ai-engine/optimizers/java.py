import re

def optimize_JAVA_CORR_001(code):
    return code

def optimize_JAVA_CORR_002(code):
    pattern = r'(\w+)\s*==\s*"(.*?)"'
    replacement = r'"\2".equals(\1)'
    return re.sub(pattern, replacement, code)

def optimize_JAVA_CORR_004(code):
    return code

def optimize_JAVA_PERF_001(code):
    return code

def optimize_JAVA_BP_001(code):
    return code

def optimize_JAVA_BP_002(code):
    return re.sub(r'catch\s*\(Exception\s+e\)', r'catch (IOException e)', code)

def optimize_JAVA_BP_003(code):
    pattern = r'(String\s+\w*(?:password|passwd|secret)\w*\s*=\s*)(["\'].*?["\'])'
    replacement = r'\1System.getenv("DB_PASSWORD")'
    return re.sub(pattern, replacement, code, flags=re.IGNORECASE)

def optimize_java(code, issues, global_applied_rules=None):
    if global_applied_rules is None:
        global_applied_rules = set()
        
    optimized_code = code
    rule_map = {
        "JAVA_CORR_001": ("Empty Catch Fix", optimize_JAVA_CORR_001),
        "JAVA_CORR_002": ("String Comparison Fix", optimize_JAVA_CORR_002),
        "JAVA_CORR_004": ("Try-With-Resources", optimize_JAVA_CORR_004),
        "JAVA_BP_001": ("Logger Integration", optimize_JAVA_BP_001),
        "JAVA_BP_002": ("Specific Exceptions", optimize_JAVA_BP_002),
        "JAVA_BP_003": ("Secret Management", optimize_JAVA_BP_003),
    }
    
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in global_applied_rules:
            desc, func = rule_map[rule_id]
            optimized_code = func(optimized_code)
            global_applied_rules.add(rule_id)
            
    return optimized_code
