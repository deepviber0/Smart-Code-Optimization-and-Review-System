import re

def optimize_javascript(code):
    optimized = code
    
    # 1. Fix undeclared loop variables FIRST (before var→let replacement)
    # Matches `for (i =` but NOT `for (let i =`, `for (var i =`, `for (const i =`
    optimized = re.sub(
        r'for\s*\(\s*(?!let |var |const )([a-zA-Z_]\w*)\s*=',
        r'for (let \1 =',
        optimized
    )
    
    # 2. Replace 'var' with 'let' (only at word boundaries)
    optimized = re.sub(r'\bvar\b', 'let', optimized)
    
    # 3. Comment out console.log inside loops
    lines = optimized.split('\n')
    in_loop = False
    loop_brace_count = 0
    
    for i, line in enumerate(lines):
        if re.search(r'\b(for|while)\s*\(', line):
            in_loop = True
            if '{' in line:
                loop_brace_count += line.count('{') - line.count('}')
        elif in_loop:
            loop_brace_count += line.count('{') - line.count('}')
            if 'console.log' in line:
                lines[i] = re.sub(
                    r'(console\.log\s*\(.*\);?)',
                    r'/* \1 (Optimized: removed I/O from loop) */',
                    line
                )
            
            if loop_brace_count <= 0:
                in_loop = False
                loop_brace_count = 0

    optimized = '\n'.join(lines)
    return optimized

def optimize_python(code):
    # Basic optimization placeholder
    return code

def optimize_java(code):
    # Basic optimization placeholder
    return code

def optimize_c_cpp(code):
    # Basic optimization placeholder
    return code

def optimize_code(code, language):
    """
    Routes the code to the appropriate language-specific optimizer.
    Returns only the optimized code body (no header comment).
    The caller is responsible for adding the header after validation.
    """
    if language == 'javascript':
        return optimize_javascript(code)
    elif language == 'python':
        return optimize_python(code)
    elif language == 'java':
        return optimize_java(code)
    elif language in ['c', 'cpp']:
        return optimize_c_cpp(code)
    return code
