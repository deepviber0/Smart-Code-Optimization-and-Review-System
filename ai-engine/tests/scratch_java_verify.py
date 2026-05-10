from ast_parser import parse_code

code = """import java.util.ArrayList;
import java.util.List;
import java.util.List;

public class TestClass {
    public void processData() {
        List<String> items = new ArrayList<>();
        for (int i = 0; i < items.size(); i++) {
            double constantVal = Math.PI * 100;
            System.out.println(items.get(i) + constantVal);
        }
    }
}"""

tree, confidence, error = parse_code(code, "java")
print(f"Confidence: {confidence}")
print(f"Error: {error}")

def print_errors(node):
    if node.type == "ERROR" or node.is_missing:
        print(f"Found Error Node: {node.type} at {node.start_point}")
    for child in node.children:
        print_errors(child)

if tree:
    print_errors(tree.root_node)
