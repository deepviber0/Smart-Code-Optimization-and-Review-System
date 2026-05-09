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
    
    # 1. Language Detection & Validation
    lang_metadata = validate_language(code, selected_language)
    lang_validation_issue = lang_metadata.get("issue")
    detected_lang = lang_metadata.get("detected", "unknown")
    detection_confidence = lang_metadata.get("confidence", 0.0)
    
    is_critical_mismatch = False
    if lang_validation_issue:
        is_critical_mismatch = True
        selected_language = lang_metadata.get("corrected_language", selected_language)
        issues.append({
            "severity": lang_validation_issue["severity"],
            "title": lang_validation_issue["title"],
            "description": lang_validation_issue["description"],
            "line": 1,
            "category": "correctness",
            "rule_id": "LANG_MISMATCH"
        })
        steps.append({
            "number": 1,
            "what": lang_validation_issue["step"]["what"],
            "why": lang_validation_issue["step"]["why"],
            "how": lang_validation_issue["step"]["how"]
        })
        
    # 2. AST Parsing
    tree, confidence, error = parse_code(code, selected_language)
    if error:
        print(f"AST Parse Error: {error}")
        
    # 3. ML Prediction & Structural Analysis
    ml_results = {
        "structural_quality_score": 80,
        "cyclomatic_complexity": 1,
        "danger_level": "None",
        "maintainability": "Good",
        "ai_generated_probability": 0.1,
        "is_anomalous": False
    }
    
    if tree:
        analysis = ml_analyzer.analyze(tree, selected_language)
        if analysis:
            ml_results.update(analysis)
            
        if ml_results.get("is_anomalous"):
            issues.append({
                "severity": "warning",
                "title": "Anomalous Code Structure",
                "description": "Detected unusual syntactic patterns that may indicate complex logic or potential bugs.",
                "category": "performance",
                "rule_id": "ML_ANOMALY"
            })
            
    # 4. Deep Heuristic Analysis (Performance & Logic)
    # Base heuristics
    base_issues, base_steps = analyze_base(code, tree)
    issues.extend(base_issues)
    
    # Language-specific heuristics (Updated with performance focus)
    lang_analyzer = get_heuristics(selected_language)
    lang_issues, lang_steps = lang_analyzer(code, tree)
    issues.extend(lang_issues)

    # 5. Optimization & AI Generation
    # We now pass issues to the optimizer which will synthesize findings
    optimization_result = optimize_code(code, selected_language, issues)
    
    optimized_code = optimization_result.get("code", code)
    explanation = optimization_result.get("explanation", "Code optimized for performance and readability.")
    metadata = optimization_result.get("metadata", {
        "performance_impact": "Medium",
        "readability_improvement": "High",
        "maintainability_improvement": "High",
        "complexity_reduction": "N/A",
        "confidence_score": 0.85
    })
    
    # NEW: Add findings from DeepOptimizer back to issues so they appear in the UI
    for pattern in optimization_result.get("patterns_found", []):
        issues.append({
            "severity": pattern.get("impact", "info").lower() if pattern.get("impact") != "High" else "warning",
            "title": pattern["title"],
            "description": pattern["reasoning"],
            "category": "performance",
            "rule_id": pattern["id"]
        })

    # 6. Scoring & Synthesis
    ml_struct_score = ml_results.get("structural_quality_score", 80) if ml_results else 80
    
    penalty = len([i for i in issues if i['severity'] == 'critical']) * 20
    penalty += len([i for i in issues if i['severity'] == 'warning']) * 10
    penalty += len([i for i in issues if i['severity'] == 'info']) * 5
    
    base_score = max(5, 100 - penalty)
    overall_score = int(0.6 * base_score + 0.4 * ml_struct_score)

    # NEW: Severe penalty for language mismatch or syntax failure
    if is_critical_mismatch:
        overall_score = min(overall_score, 15)
        base_score = 10
    elif confidence < 0.5:
        overall_score = min(overall_score, 30)
        issues.append({
            "severity": "critical",
            "title": "Poor Syntax Quality",
            "description": f"Code parsing confidence is low ({int(confidence*100)}%). Ensure the code is complete and syntactically correct.",
            "category": "correctness",
            "rule_id": "LOW_CONFIDENCE"
        })
    
    # 7. NEW: Deep Intelligence Verdict Generation
    verdict = "Overall, your code follows a standard structure."
    if lang_validation_issue:
        verdict = "Selected language does not match detected code language."
    elif overall_score < 40:
        verdict = "Critical structural and logic issues were detected. Refactoring is strongly recommended to ensure stability."
    elif overall_score < 65:
        verdict = "Your code is functional but contains several anti-patterns. Improving resource management and logic efficiency will help."
    elif overall_score < 85:
        verdict = "Good quality code. Some minor optimizations could further enhance performance and readability."
    else:
        verdict = "Excellent! Your code demonstrates professional-grade structure and efficiency."

    # Code DNA Profile (Synthesis)
    dna = {
        "complexity_profile": "Linear" if ml_results.get("cyclomatic_complexity", 0) < 5 else "Moderate" if ml_results.get("cyclomatic_complexity", 0) < 15 else "High-Complexity",
        "primary_risk": ml_results.get("danger_level", "None").capitalize(),
        "style_verdict": ml_results.get("maintainability", "Good").capitalize(),
        "ai_score": f"{int(ml_results.get('ai_generated_probability', 0) * 100)}%"
    }

    result = {
        "score": {
            "overall": overall_score,
            "correctness": min(100, base_score + 10) if not is_critical_mismatch else 10,
            "performance": min(100, base_score - 5) if not is_critical_mismatch else 5,
            "readability": min(100, base_score + 5) if not is_critical_mismatch else 5,
            "bestPractices": min(100, ml_struct_score) if not is_critical_mismatch else 5
        },
        "verdict": verdict,
        "dna": dna,
        "issues": issues,
        "steps": steps,
        "optimizedCode": optimized_code,
        "explanation": explanation,
        "fullAnalysis": optimization_result.get("raw_output", ""),
        "metadata": {
            **metadata,
            "detected_language": detected_lang,
            "detection_confidence": f"{int(detection_confidence * 100)}%",
            "original_selection": lang_metadata.get("selected")
        },
        "mlStats": ml_results,
        "language": selected_language
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
