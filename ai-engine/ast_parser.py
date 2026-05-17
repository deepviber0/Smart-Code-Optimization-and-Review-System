import tree_sitter
import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_c
import tree_sitter_cpp
import tree_sitter_java

LANGUAGE_MAP = {
    'python': tree_sitter.Language(tree_sitter_python.language()),
    'javascript': tree_sitter.Language(tree_sitter_javascript.language()),
    'c': tree_sitter.Language(tree_sitter_c.language()),
    'cpp': tree_sitter.Language(tree_sitter_cpp.language()),
    'java': tree_sitter.Language(tree_sitter_java.language()),
}

def parse_code(code, language):
    if language not in LANGUAGE_MAP:
        return None, 0.0, f"Unsupported language: {language}"
        
    try:
        parser = tree_sitter.Parser(LANGUAGE_MAP[language])
        tree = parser.parse(bytes(code, 'utf8'))
        

        error_nodes = 0
        total_nodes = 0
        
        def traverse(node):
            nonlocal error_nodes, total_nodes
            total_nodes += 1
            if node.type == 'ERROR' or node.is_missing:
                error_nodes += 1
            for child in node.children:
                traverse(child)
                
        if tree.root_node:
            traverse(tree.root_node)
        
        confidence = 1.0
        if total_nodes > 0:
            confidence = 1.0 - (error_nodes / max(1, total_nodes))
        else:
            confidence = 0.0 if not code.strip() else 0.5
            
        return tree, confidence, None
    except Exception as e:
        return None, 0.0, str(e)
