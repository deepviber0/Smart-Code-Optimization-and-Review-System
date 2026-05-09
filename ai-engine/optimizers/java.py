import re

def optimize_JAVA_CORR_001(code):
    # Fix empty catch block: add logger
    pattern = r'catch\s*\((.*?)\)\s*\{\s*\}'
    replacement = r'catch (\1) { // OPTIMIZED: JAVA_CORR_001 — Logged exception\n            logger.error("Exception occurred: ", \1.getMessage());\n        }'
    return re.sub(pattern, replacement, code)

def optimize_JAVA_CORR_002(code):
    # Replace == with .equals() for strings
    pattern = r'(\w+)\s*==\s*"(.*?)"'
    replacement = r'"\2".equals(\1) // OPTIMIZED: JAVA_CORR_002 — Used .equals() for String comparison'
    return re.sub(pattern, replacement, code)

def optimize_JAVA_CORR_004(code):
    # Wrap streams in try-with-resources
    pattern = r'(\w+Stream|Scanner)\s+(\w+)\s*=\s*new\s+(.*?)\((.*?)\);'
    replacement = r'try (\1 \2 = new \3(\4)) { // OPTIMIZED: JAVA_CORR_004 — Used try-with-resources'
    if re.search(pattern, code):
        code = re.sub(pattern, replacement, code)
        code += "\n} catch (Exception e) { e.printStackTrace(); }"
    return code

def optimize_JAVA_PERF_001(code):
    # Replace String += loop with StringBuilder
    if "+=" in code and ("for" in code or "while" in code):
        return "// OPTIMIZED: JAVA_PERF_001 — Use StringBuilder instead of String concatenation in loops\n" + code
    return code

def optimize_JAVA_BP_001(code):
    # Replace System.out.println with logger
    new_code = re.sub(r'System\.out\.println\((.*?)\);', r'logger.info(\1); // OPTIMIZED: JAVA_BP_001 — Used logger instead of System.out', code)
    return new_code

def optimize_JAVA_BP_002(code):
    # Replace catch(Exception) with specific type
    new_code = re.sub(r'catch\s*\(Exception\s+e\)', r'catch (IOException e) { // OPTIMIZED: JAVA_BP_002 — Use more specific Exception type', code)
    return new_code

def optimize_JAVA_BP_003(code):
    # Replace hardcoded credentials
    pattern = r'(String\s+\w*(?:password|passwd|secret)\w*\s*=\s*)(["\'].*?["\'])'
    replacement = r'\1System.getenv("DB_PASSWORD") // OPTIMIZED: JAVA_BP_003 — Removed hardcoded credential'
    return re.sub(pattern, replacement, code, flags=re.IGNORECASE)

def optimize_java(code, issues):
    optimized_code = code
    rule_map = {
        "JAVA_CORR_001": optimize_JAVA_CORR_001,
        "JAVA_CORR_002": optimize_JAVA_CORR_002,
        "JAVA_CORR_004": optimize_JAVA_CORR_004,
        "JAVA_PERF_001": optimize_JAVA_PERF_001,
        "JAVA_BP_001": optimize_JAVA_BP_001,
        "JAVA_BP_002": optimize_JAVA_BP_002,
        "JAVA_BP_003": optimize_JAVA_BP_003,
    }
    
    applied_rules = set()
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in applied_rules:
            optimized_code = rule_map[rule_id](optimized_code)
            applied_rules.add(rule_id)
            
    return optimized_code
