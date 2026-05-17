import re
from typing import List, Dict, Any, Tuple

def analyze_base(code: str, tree=None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    issues = []
    steps = []
    lines = code.splitlines()


    empty_block_pattern = re.compile(r'\{\s*\}')
    for i, line in enumerate(lines, 1):
        if empty_block_pattern.search(line):
            issues.append({
                "severity": "info",
                "title": "Empty Code Block",
                "description": "Empty blocks can be a sign of unfinished logic or redundant syntax.",
                "line": i,
                "category": "readability",
                "rule_id": "GEN_BP_001"
            })


    todo_pattern = re.compile(r'\b(TODO|FIXME|HACK|XXX)\b', re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        match = todo_pattern.search(line)
        if match:
            issues.append({
                "severity": "info",
                "title": f"Marker Detected: {match.group(1)}",
                "description": f"Code contains a '{match.group(1)}' marker. Ensure this is addressed before production.",
                "line": i,
                "category": "best_practices",
                "rule_id": "GEN_BP_002"
            })


    for i, line in enumerate(lines, 1):
        indent = len(line) - len(line.lstrip())

        if indent > 16: # > 4 levels deep
             issues.append({
                "severity": "warning",
                "title": "Deep Code Nesting",
                "description": "Excessive nesting depth makes code hard to read and maintain.",
                "line": i,
                "category": "readability",
                "rule_id": "GEN_BP_003"
            })
             break # One warning per file is enough for nesting


    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            issues.append({
                "severity": "info",
                "title": "Line Too Long",
                "description": f"Line exceeds 120 characters ({len(line)} chars). Consider breaking it up.",
                "line": i,
                "category": "readability",
                "rule_id": "GEN_BP_005"
            })
            break

    return issues, steps
