from ast_parser import parse_code

# Language-specific AST node types that strongly indicate a particular language.
# Only nodes that are UNIQUE to a grammar are listed to avoid cross-language false matches.
LANGUAGE_FINGERPRINTS = {
    'javascript': {
        'program',                # JS root node (not 'translation_unit' like C/C++)
        'variable_declaration',   # var/let/const (JS-specific node)
        'call_expression',        # function calls (vs method_invocation in Java)
        'member_expression',      # obj.prop (vs field_expression in C)
        'property_identifier',    # property names (vs field_identifier in C)
        'number',                 # numeric literals (vs number_literal in C, decimal_integer_literal in Java)
    },
    'python': {
        'module',                 # Python root node
        'function_definition',    # def ...
        'import_statement',       # import ...
        'import_from_statement',  # from ... import ...
        'integer',                # numeric literals (Python-specific)
        'list_comprehension',     # [x for x in ...]
    },
    'java': {
        'method_invocation',           # obj.method() (vs call_expression in JS)
        'decimal_integer_literal',     # numeric literals (Java-specific)
        'local_variable_declaration',  # type var = val (Java-specific)
        'class_declaration',           # class Foo {}
        'method_declaration',          # void foo() {}
    },
    'c': {
        'translation_unit',       # C root node (not 'program' like JS)
        'preproc_include',        # #include (C-specific)
        'number_literal',         # numeric literals (C-specific)
        'compound_statement',     # { } blocks (C-specific name)
    },
    'cpp': {
        'translation_unit',       # C++ root node
        'preproc_include',        # #include (C++-specific)
        'number_literal',         # numeric literals (C++-specific)
        'namespace_identifier',   # std:: (C++-specific)
        'template_type',          # vector<int> (C++-specific)
    }
}


def collect_node_types(tree):
    """Walks the AST and returns the set of all node types."""
    node_types = set()
    def walk(node):
        node_types.add(node.type)
        for child in node.children:
            walk(child)
    walk(tree.root_node)
    return node_types


def compute_fingerprint_score(node_types, language):
    """
    Computes a fingerprint match score: the fraction of the language's
    fingerprint node types that appear in the parsed AST.
    """
    fingerprints = LANGUAGE_FINGERPRINTS.get(language, set())
    if not fingerprints:
        return 0.0
    matches = node_types & fingerprints
    return len(matches) / len(fingerprints)


def detect_language_ast(code):
    """
    Returns the most likely language and a combined score using
    AST parsing confidence + node type fingerprinting.
    """
    best_lang = None
    best_score = -1.0
    
    for lang in ['javascript', 'python', 'java', 'c', 'cpp']:
        tree, conf, err = parse_code(code, lang)
        if err is not None or tree is None:
            continue
            
        node_types = collect_node_types(tree)
        fp_score = compute_fingerprint_score(node_types, lang)
        
        # Combined score: 40% parse confidence + 60% fingerprint match
        combined = 0.4 * conf + 0.6 * fp_score
        
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
        fp_score = compute_fingerprint_score(node_types, selected_language)
        sel_score = 0.4 * sel_conf + 0.6 * fp_score
    
    # If the selected language is the best match, no issue
    if best_lang == selected_language:
        return None, selected_language
    
    # If the best detected language scores meaningfully higher
    if best_score > sel_score + 0.05:
        # C and C++ overlap heavily, give them leniency
        if selected_language in ['c', 'cpp'] and best_lang in ['c', 'cpp']:
            return None, selected_language
            
        issue = {
            "severity": "critical",
            "title": "Language Mismatch Detected",
            "description": f"Selected language is {selected_language.capitalize()}, but AST analysis identified the code as {best_lang.capitalize()}.",
            "step": {
                "what": "Correct the selected language",
                "why": "The syntax analyzer and optimization engines are strictly language-specific. The engine has auto-corrected the language for proper analysis.",
                "how": f"The engine has internally corrected the language from {selected_language.capitalize()} to {best_lang.capitalize()} for this request."
            }
        }
        return issue, best_lang
        
    return None, selected_language

