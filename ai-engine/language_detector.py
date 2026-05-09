from ast_parser import parse_code

LANGUAGE_FINGERPRINTS = {
    'javascript': [
        'program',                # JS root node
        'variable_declaration',   # var/let/const
        'lexical_declaration',    # let/const specific
        'arrow_function',         # () => {}
        'template_string',        # `string`
        'export_statement',       # export ...
        'object_pattern',         # {a, b} = obj
        'array_pattern',          # [a, b] = arr
        'statement_block',        # { ... } in JS
    ],
    'python': [
        'module',                 # Python root node
        'function_definition',    # def ...
        'import_from_statement',  # from x import y
        'list_comprehension',     # [x for x in ...]
        'dictionary_comprehension',# {k:v for k,v in ...}
        'set_comprehension',      # {x for x in ...}
        'decorated_definition',   # @decorator
        'with_statement',         # with open(...)
        'keyword_argument',       # func(a=1)
        'block',                  # Python specific block node name
    ],
    'java': [
        'method_invocation',           # obj.method()
        'decimal_integer_literal',     # Java specific naming
        'local_variable_declaration',  # type var = val
        'class_declaration',           # class Foo {}
        'method_declaration',          # void foo() {}
        'package_declaration',         # package ...
        'import_declaration',          # import ... (Java specific node name)
        'constructor_declaration',     # public Foo() {}
        'try_with_resources_statement' # try (Resource r = ...) {}
    ],
    'c': [
        'translation_unit',       # C/C++ root node
        'preproc_include',        # #include
        'preproc_def',            # #define
        'pointer_declarator',     # int *p
        'parameter_declaration',  # (int a, char b)
        'struct_specifier',       # struct Foo {}
    ],
    'cpp': [
        'translation_unit',       # C/C++ root node
        'namespace_definition',   # namespace foo {}
        'template_declaration',   # template <typename T>
        'class_specifier',        # class Foo {}; (C++ style)
        'visibility_label',       # public:, private:
        'lambda_expression',      # [](){}
    ]
}


def collect_node_types(tree):
    """Walks the AST and returns the set of all node types."""
    node_types = set()
    if not tree or not tree.root_node:
        return node_types
        
    def walk(node):
        node_types.add(node.type)
        for child in node.children:
            walk(child)
    walk(tree.root_node)
    return node_types


def compute_fingerprint_score(node_types, language, tree=None):
    """
    Computes a fingerprint match score: the fraction of the language's
    fingerprint node types that appear in the parsed AST.
    """
    fps = LANGUAGE_FINGERPRINTS.get(language, [])
    if not fps:
        return 0.0
    
    fingerprints_set = set(fps)
    matches = node_types & fingerprints_set
    
    score = len(matches) / len(fingerprints_set)
    
    # Root node boost: if the root node type matches the expected root for the language
    if tree and tree.root_node.type == fps[0]: # Root is always first in our list
        score += 0.2
        
    return min(1.0, score)


def detect_language_ast(code):
    """
    Returns the most likely language and a combined score using
    AST parsing confidence + node type fingerprinting.
    """
    best_lang = None
    best_score = -1.0
    
    # Check for obvious markers first (Shebang or specific keywords at start)
    code_start = code.strip()[:100]
    if code_start.startswith(('#include', 'import std', 'using namespace')):
        return 'cpp', 1.0
    if code_start.startswith(('package ', 'import java.')):
        return 'java', 1.0
    if code_start.startswith(('import ', 'from ', 'def ')):
        # Common in Python, but check AST to be sure
        pass

    for lang in ['javascript', 'python', 'java', 'c', 'cpp']:
        tree, conf, err = parse_code(code, lang)
        if err is not None or tree is None:
            continue
            
        node_types = collect_node_types(tree)
        fp_score = compute_fingerprint_score(node_types, lang, tree)
        
        # Combined score: 20% parse confidence + 80% fingerprint match
        # Fingerprints are stronger indicators of identity than just parsing "without errors"
        combined = 0.2 * conf + 0.8 * fp_score
        
        if combined > best_score:
            best_score = combined
            best_lang = lang
            
    return best_lang, best_score


def validate_language(code, selected_language):
    """
    Validates if the code matches the selected language based on AST parsing
    and node type fingerprinting.
    Returns (issue_dict, corrected_language).
    """
    best_lang, best_score = detect_language_ast(code)
    
    if not best_lang:
        return None, selected_language
    
    # Compute the selected language's score
    tree, sel_conf, err = parse_code(code, selected_language)
    if err or tree is None:
        sel_score = 0.0
    else:
        node_types = collect_node_types(tree)
        fp_score = compute_fingerprint_score(node_types, selected_language, tree)
        sel_score = 0.2 * sel_conf + 0.8 * fp_score
    
    # PRIORITY LOGIC:
    # 1. If selected language has very high score (> 0.7), trust it.
    if selected_language == best_lang or sel_score > 0.7:
        return None, selected_language
        
    # 2. C and C++ overlap heavily, trust the user's choice between them if both parse reasonably well.
    if selected_language in ['c', 'cpp'] and best_lang in ['c', 'cpp'] and sel_score > 0.3:
        return None, selected_language
    
    # 3. Only override if the best detected language is SIGNIFICANTLY better (delta > 0.15)
    # or the selected language is clearly wrong (sel_score < 0.25)
    if best_score > sel_score + 0.15 or sel_score < 0.25:
        issue = {
            "severity": "critical",
            "title": "Language Mismatch Detected",
            "description": f"Selected language is {selected_language.capitalize()}, but AST analysis identified the code as {best_lang.capitalize()}.",
            "step": {
                "what": "Correct the selected language",
                "why": "The syntax analyzer and optimization engines are strictly language-specific. Analysis for the wrong language will produce invalid results.",
                "how": f"The engine has internally corrected the language from {selected_language.capitalize()} to {best_lang.capitalize()} for this request."
            }
        }
        return issue, best_lang
        
    return None, selected_language

