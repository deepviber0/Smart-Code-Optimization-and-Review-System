import tree_sitter
import tree_sitter_python
import tree_sitter_javascript

def get_node_types(code, lang_mod):
    language = tree_sitter.Language(lang_mod.language())
    parser = tree_sitter.Parser(language)
    tree = parser.parse(bytes(code, 'utf8'))
    
    node_types = set()
    def traverse(node):
        node_types.add(node.type)
        for child in node.children:
            traverse(child)
    traverse(tree.root_node)
    return node_types

python_code = """
def hello():
    if True:
        print("world")
"""

js_code = """
function hello() {
    if (true) {
        console.log("world");
    }
}
"""

print("Python code parsed with Python parser:")
print(get_node_types(python_code, tree_sitter_python))

print("\nJS code parsed with JS parser:")
print(get_node_types(js_code, tree_sitter_javascript))

print("\nPython code parsed with JS parser:")
print(get_node_types(python_code, tree_sitter_javascript))
