import re

def optimize_CPP_SEC_001(code):
    # Replace gets() with fgets()
    pattern = r'gets\s*\((.*?)\)'
    replacement = r'fgets(\1, sizeof(\1), stdin) // OPTIMIZED: CPP_SEC_001 — Replaced unsafe gets() with fgets()'
    return re.sub(pattern, replacement, code)

def optimize_CPP_SEC_002(code):
    # Replace strcpy() with strncpy()
    pattern = r'strcpy\s*\((.*?),\s*(.*?)\)'
    replacement = r'strncpy(\1, \2, sizeof(\1) - 1); \1[sizeof(\1) - 1] = \'\\0\'; // OPTIMIZED: CPP_SEC_002 — Replaced unsafe strcpy() with strncpy()'
    return re.sub(pattern, replacement, code)

def optimize_CPP_SEC_003(code):
    # Add width limit to scanf %s
    pattern = r'scanf\s*\(\s*"%s"\s*,\s*(.*?)\)'
    replacement = r'scanf("%19s", \1) // OPTIMIZED: CPP_SEC_003 — Added width limit to scanf'
    return re.sub(pattern, replacement, code)

def optimize_CPP_SEC_004(code):
    # Fix printf format string vulnerability
    pattern = r'printf\s*\(([^",]*?)\)'
    replacement = r'printf("%s", \1) // OPTIMIZED: CPP_SEC_004 — Fixed printf format string vulnerability'
    return re.sub(pattern, replacement, code)

def optimize_CPP_CORR_001(code):
    # Add free() after malloc()
    if "malloc" in code and "free" not in code:
        return code + "\nfree(ptr); // OPTIMIZED: CPP_CORR_001 — Ensure allocated memory is freed"
    return code

def optimize_CPP_CORR_002(code):
    # Add NULL check after malloc()
    pattern = r'(\w+)\s*=\s*\(.*?\)\s*malloc\((.*?)\);'
    replacement = r'\1 = malloc(\2);\nif (\1 == NULL) { exit(1); } // OPTIMIZED: CPP_CORR_002 — Added NULL check after malloc'
    return re.sub(pattern, replacement, code)

def optimize_CPP_CORR_003(code):
    # Initialize declared variables
    pattern = r'\bint\s+(\w+)\s*;'
    replacement = r'int \1 = 0; // OPTIMIZED: CPP_CORR_003 — Initialized variable'
    return re.sub(pattern, replacement, code)

def optimize_CPP_BP_001(code):
    # Replace raw new with smart pointer (C++)
    pattern = r'(\w+)\s*\*\s*(\w+)\s*=\s*new\s+(\w+)\((.*?)\);'
    replacement = r'std::unique_ptr<\1> \2 = std::make_unique<\3>(\4); // OPTIMIZED: CPP_BP_001 — Used smart pointer instead of raw new'
    return re.sub(pattern, replacement, code)

def optimize_CPP_PERF_001(code):
    # Replace pass by value with const reference
    pattern = r'(\w+)\s+(\w+)\s*\(\s*std::string\s+(\w+)\s*\)'
    replacement = r'\1 \2(const std::string& \3) // OPTIMIZED: CPP_PERF_001 — Passed by const reference'
    return re.sub(pattern, replacement, code)

def optimize_CPP_PERF_002(code):
    # Move memory allocation outside loop
    if "malloc" in code and ("for" in code or "while" in code):
        return "// OPTIMIZED: CPP_PERF_002 — Move memory allocation outside the loop to improve performance\n" + code
    return code

def optimize_c_cpp(code, issues):
    optimized_code = code
    rule_map = {
        "CPP_SEC_001": optimize_CPP_SEC_001,
        "CPP_SEC_002": optimize_CPP_SEC_002,
        "CPP_SEC_003": optimize_CPP_SEC_003,
        "CPP_SEC_004": optimize_CPP_SEC_004,
        "CPP_CORR_001": optimize_CPP_CORR_001,
        "CPP_CORR_002": optimize_CPP_CORR_002,
        "CPP_CORR_003": optimize_CPP_CORR_003,
        "CPP_BP_001": optimize_CPP_BP_001,
        "CPP_PERF_001": optimize_CPP_PERF_001,
        "CPP_PERF_002": optimize_CPP_PERF_002,
    }
    
    applied_rules = set()
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in applied_rules:
            optimized_code = rule_map[rule_id](optimized_code)
            applied_rules.add(rule_id)
            
    return optimized_code
