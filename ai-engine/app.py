import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_pipeline import ml_analyzer
from language_detector import validate_language
from ast_parser import parse_code
from heuristics import get_heuristics, analyze_base
from optimizer import optimize_code

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data.get('code', '')
    selected_language = data.get('language', 'javascript').lower()
    
    issues = []
    steps = []
    
    # 1. Language Validation Pipeline
    lang_validation_issue, corrected_language = validate_language(code, selected_language)
    if lang_validation_issue:
        selected_language = corrected_language
        issues.append({
            "severity": lang_validation_issue["severity"],
            "title": lang_validation_issue["title"],
            "description": lang_validation_issue["description"],
            "line": 1
        })
        steps.append({
            "number": 1,
            "what": lang_validation_issue["step"]["what"],
            "why": lang_validation_issue["step"]["why"],
            "how": lang_validation_issue["step"]["how"]
        })
        
    # 2. AST Parsing Pipeline
    tree, confidence, error = parse_code(code, selected_language)
    if error:
        print(f"AST Parse Error: {error}")
        
    # 3. ML Feature Extraction & Prediction Pipeline
    ml_results = None
    if tree:
        ml_results = ml_analyzer.analyze(tree, selected_language)
        
        # Integrate ML findings
        if ml_results.get("is_anomalous"):
            issues.append({
                "severity": "warning",
                "title": "Anomalous Code Structure Detected",
                "description": "ML model detected unusual AST structural patterns that deviate from best practices."
            })
            steps.append({
                "number": len(steps) + 1,
                "what": "Review code structure",
                "why": "The underlying structure of the code is highly unusual compared to standard projects.",
                "how": "Refactor deeply nested logic or unusual syntactic combinations."
            })
            
        if ml_results.get("ai_generated_probability", 0) > 0.8:
            issues.append({
                "severity": "info",
                "title": "High AI-Generation Probability",
                "description": f"Model indicates {int(ml_results['ai_generated_probability']*100)}% likelihood this code is AI generated."
            })
            
    # 4. Heuristics Analysis Pipeline
    # Base heuristics (all languages)
    base_issues, base_steps = analyze_base(code, tree)
    issues.extend(base_issues)
    for step in base_steps:
        step["number"] = len(steps) + 1
        steps.append(step)
        
    # Language-specific heuristics
    lang_analyzer = get_heuristics(selected_language)
    lang_issues, lang_steps = lang_analyzer(code, tree)
    issues.extend(lang_issues)
    for step in lang_steps:
        step["number"] = len(steps) + 1
        steps.append(step)

    # Missing docs check
    if not any("doc" in i['title'].lower() for i in issues) and len(code.split('\n')) > 5:
        if not re.search(r'(//|/\*|#|""")', code):
            issues.append({
                "severity": "info",
                "title": "Missing documentation",
                "description": "Code lacks comments or docstrings."
            })
            steps.append({
                "number": len(steps) + 1,
                "what": "Add comments",
                "why": "Improves readability and maintainability.",
                "how": "Add comments explaining complex logic or function definitions."
            })

    # 5. Final Scoring Pipeline
    ml_struct_score = ml_results.get("structural_quality_score", 80) if ml_results else 80
    
    penalty = len([i for i in issues if i['severity'] == 'critical']) * 20
    penalty += len([i for i in issues if i['severity'] == 'warning']) * 10
    penalty += len([i for i in issues if i['severity'] == 'info']) * 5
    
    if lang_validation_issue:
        penalty += 30 # Heavy penalty for language mismatch
        
    base_score = max(20, 100 - penalty)
    
    # Weight ML Score (30%) with Heuristic Score (70%)
    overall_score = int(0.7 * base_score + 0.3 * ml_struct_score)
    
    # 6. Optimization Generation
    optimized_code = optimize_code(code, selected_language, issues)
    
    # Post-optimization validation
    _, opt_conf, opt_err = parse_code(optimized_code, selected_language)
    
    comment_style = "#" if selected_language == 'python' else "//"
    
    if opt_err is not None or opt_conf < (confidence - 0.2):
        print(f"Optimization introduced syntax errors for {selected_language}. Reverting.")
        optimized_code = f"{comment_style} Optimization failed. Returning original {selected_language.capitalize()} code.\n" + code
    else:
        # Avoid double header if the optimizer already added one
        if not optimized_code.strip().startswith(comment_style):
            optimized_code = f"{comment_style} Optimized Version for {selected_language.capitalize()}\n" + optimized_code
    
    result = {
        "score": {
            "overall": overall_score,
            "correctness": min(100, base_score + 10),
            "performance": min(100, base_score - 5),
            "readability": min(100, base_score + 5),
            "bestPractices": min(100, ml_struct_score) 
        },
        "issues": issues,
        "steps": steps,
        "optimizedCode": optimized_code,
        "mlStats": ml_results,
        "language": selected_language
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
