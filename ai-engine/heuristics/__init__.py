from .base import analyze_base
from .javascript import analyze_javascript
from .python import analyze_python
from .java import analyze_java
from .c_cpp import analyze_c_cpp

def get_heuristics(language):
    if language == 'javascript':
        return analyze_javascript
    elif language == 'python':
        return analyze_python
    elif language == 'java':
        return analyze_java
    elif language in ['c', 'cpp']:
        return lambda code, tree: analyze_c_cpp(code, tree, language)
    return lambda code, tree: ([], [])