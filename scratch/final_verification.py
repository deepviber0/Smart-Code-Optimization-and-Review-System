import requests
import json
import time

def test_analyze(code, language, name):
    url = "http://localhost:5001/analyze"
    payload = {
        "code": code,
        "language": language
    }
    print(f"\n[TESTING: {name}]")
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"Language Used: {result.get('language')}")
        print(f"Issues Found: {len(result.get('issues', []))}")
        for issue in result.get('issues', []):
            print(f" - [{issue.get('severity')}] {issue.get('title')}")
        
        # print("Optimized Code Snippet:")
        # print("\n".join(result.get('optimizedCode', '').split('\n')[:10]))
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test Cases
python_test = """
def process_data(items=[]):
    if items == None:
        return
    for i in range(len(items)):
        print(items[i])
    try:
        eval("1+1")
    except:
        pass
"""

js_test = """
var x = 0;
for(i=0; i<10; i++) {
    console.log(i);
}
if (x == null) {
    document.getElementById("foo").innerHTML = "<b>Hello</b>";
}
"""

java_test = """
public class Test {
    public void run() {
        String s = "hello";
        if (s == "world") {
            System.out.println(s);
        }
        try {
            FileInputStream fis = new FileInputStream("file.txt");
        } catch (Exception e) {}
    }
}
"""

cpp_test = """
#include <stdio.h>
#include <string.h>
int main() {
    char buf[10];
    gets(buf);
    strcpy(buf, "hello world");
    int *p = (int*)malloc(10);
    printf(buf);
    return 0;
}
"""

if __name__ == "__main__":
    print("Starting Final System Verification...")
    test_analyze(python_test, "python", "Python Rule Engine")
    test_analyze(js_test, "javascript", "JS Rule Engine")
    test_analyze(java_test, "java", "Java Rule Engine")
    test_analyze(cpp_test, "cpp", "C++ Rule Engine")
