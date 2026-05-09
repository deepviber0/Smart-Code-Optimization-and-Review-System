from optimizers.javascript import optimize_javascript as js_optimize
from optimizers.python import optimize_python as py_optimize
from optimizers.java import optimize_java as java_optimize
from optimizers.c_cpp import optimize_c_cpp as cpp_optimize
from ai_optimizer import DeepOptimizer

def optimize_code(code, language, issues):
    """
    Orchestrates the optimization process using heuristics and AI analysis.
    """
    # 1. Gather language-specific rule fixes (Legacy/Fallback)
    rule_optimized = code
    if language == 'javascript':
        rule_optimized = js_optimize(code, issues)
    elif language == 'python':
        rule_optimized = py_optimize(code, issues)
    elif language == 'java':
        rule_optimized = java_optimize(code, issues)
    elif language in ['c', 'cpp']:
        rule_optimized = cpp_optimize(code, issues)
        
    # 2. Run Deep AI-Powered Optimization
    deep_optimizer = DeepOptimizer(language)
    result = deep_optimizer.analyze_and_optimize(code, issues, rule_optimized)
    
    return result
