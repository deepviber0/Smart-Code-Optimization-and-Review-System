from optimizers.javascript import optimize_javascript as js_optimize
from optimizers.python import optimize_python as py_optimize
from optimizers.java import optimize_java as java_optimize
from optimizers.c_cpp import optimize_c_cpp as cpp_optimize

def optimize_code(code, language, issues):
    """
    Routes the code to the appropriate language-specific optimizer.
    """
    if language == 'javascript':
        return js_optimize(code, issues)
    elif language == 'python':
        return py_optimize(code, issues)
    elif language == 'java':
        return java_optimize(code, issues)
    elif language in ['c', 'cpp']:
        return cpp_optimize(code, issues)
    return code
