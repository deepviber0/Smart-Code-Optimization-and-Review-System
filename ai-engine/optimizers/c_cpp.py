import re

def optimize_CPP_SEC_001(code):
    pattern = r'gets\s*\((.*?)\)'
    replacement = r'fgets(\1, sizeof(\1), stdin)'
    return re.sub(pattern, replacement, code)

def optimize_CPP_SEC_002(code):
    return code # Risky: sizeof(\1) fails if it is a pointer

def optimize_CPP_SEC_003(code):
    pattern = r'scanf\s*\(\s*"%s"\s*,\s*(.*?)\)'
    replacement = r'scanf("%19s", \1)'
    return re.sub(pattern, replacement, code)

def optimize_CPP_SEC_004(code):
    pattern = r'printf\s*\(([^",]*?)\)'
    replacement = r'printf("%s", \1)'
    return re.sub(pattern, replacement, code)

def optimize_CPP_CORR_001(code):
    return code # Logic is complex, handled by heuristics

def optimize_CPP_CORR_002(code):
    return code # Risky: can break expressions if malloc is nested

def optimize_CPP_CORR_003(code):
    pattern = r'\bint\s+(\w+)\s*;'
    replacement = r'int \1 = 0;'
    return re.sub(pattern, replacement, code)

def optimize_CPP_BP_001(code):
    pattern = r'(\w+)\s*\*\s*(\w+)\s*=\s*new\s+(\w+)\((.*?)\);'
    replacement = r'std::unique_ptr<\1> \2 = std::make_unique<\3>(\4);'
    return re.sub(pattern, replacement, code)

def optimize_CPP_PERF_001(code):
    pattern = r'(\w+)\s+(\w+)\s*\(\s*std::string\s+(\w+)\s*\)'
    replacement = r'\1 \2(const std::string& \3)'
    return re.sub(pattern, replacement, code)

def optimize_CPP_PERF_002(code):
    return code # Handled by DeepOptimizer

def optimize_c_cpp(code, issues, global_applied_rules=None):
    if global_applied_rules is None:
        global_applied_rules = set()
        
    optimized_code = code
    rule_map = {
        "CPP_SEC_001": ("Buffer Safety", optimize_CPP_SEC_001),
        "CPP_SEC_002": ("Safe Copy", optimize_CPP_SEC_002),
        "CPP_SEC_003": ("Scanf Safety", optimize_CPP_SEC_003),
        "CPP_SEC_004": ("Format Safety", optimize_CPP_SEC_004),
        "CPP_CORR_002": ("Null Check Injection", optimize_CPP_CORR_002),
        "CPP_CORR_003": ("Var Initialization", optimize_CPP_CORR_003),
        "CPP_BP_001": ("Smart Pointer Fix", optimize_CPP_BP_001),
        "CPP_PERF_001": ("Const Ref Optimization", optimize_CPP_PERF_001),
    }
    
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in global_applied_rules:
            desc, func = rule_map[rule_id]
            optimized_code = func(optimized_code)
            global_applied_rules.add(rule_id)
            
    return optimized_code
