import re

def optimize_JAVA_CORR_001(code):
    pattern = r'catch\s*\((.*?)\)\s*\{\s*\}'
    replacement = r'catch (\1) {\n            logger.error("Exception occurred: ", \1.getMessage());\n        }'
    return re.sub(pattern, replacement, code)

def optimize_JAVA_CORR_002(code):
    pattern = r'(\w+)\s*==\s*"(.*?)"'
    replacement = r'"\2".equals(\1)'
    return re.sub(pattern, replacement, code)

def optimize_JAVA_CORR_004(code):
    pattern = r'(\w+Stream|Scanner)\s+(\w+)\s*=\s*new\s+(.*?)\((.*?)\);'
    replacement = r'try (\1 \2 = new \3(\4)) {'
    if re.search(pattern, code):
        code = re.sub(pattern, replacement, code)
        code += "\n} catch (Exception e) { e.printStackTrace(); }"
    return code

def optimize_JAVA_PERF_001(code):
    return code # Handled by DeepOptimizer

def optimize_JAVA_BP_001(code):
    return re.sub(r'System\.out\.println\((.*?)\);', r'logger.info(\1);', code)

def optimize_JAVA_BP_002(code):
    return re.sub(r'catch\s*\(Exception\s+e\)', r'catch (IOException e)', code)

def optimize_JAVA_BP_003(code):
    pattern = r'(String\s+\w*(?:password|passwd|secret)\w*\s*=\s*)(["\'].*?["\'])'
    replacement = r'\1System.getenv("DB_PASSWORD")'
    return re.sub(pattern, replacement, code, flags=re.IGNORECASE)

def optimize_java(code, issues):
    optimized_code = code
    rule_map = {
        "JAVA_CORR_001": ("Empty Catch Fix", optimize_JAVA_CORR_001),
        "JAVA_CORR_002": ("String Comparison Fix", optimize_JAVA_CORR_002),
        "JAVA_CORR_004": ("Try-With-Resources", optimize_JAVA_CORR_004),
        "JAVA_BP_001": ("Logger Integration", optimize_JAVA_BP_001),
        "JAVA_BP_002": ("Specific Exceptions", optimize_JAVA_BP_002),
        "JAVA_BP_003": ("Secret Management", optimize_JAVA_BP_003),
    }
    
    applied_descriptions = []
    applied_rules = set()
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in applied_rules:
            desc, func = rule_map[rule_id]
            optimized_code = func(optimized_code)
            applied_descriptions.append(desc)
            applied_rules.add(rule_id)
            
    if applied_descriptions:
        header = f"// Optimized: {', '.join(applied_descriptions)}\n"
        return header + optimized_code
        
    return optimized_code
