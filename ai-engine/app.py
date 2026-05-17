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

def calculate_detailed_score(issues, ml_struct_score, confidence, is_mismatch, language):
    breakdown = {
        "syntax_safety": 25,
        "readability": 20,
        "performance": 20,
        "best_practices": 20,
        "structure": 15
    }
    deductions = []
    

    syntax_deduction = 0
    if is_mismatch:
        syntax_deduction = 20
        deductions.append("Language mismatch: -20")
    elif confidence < 0.5:
        syntax_deduction = 15
        deductions.append("Syntax ambiguity: -15")
    

    read_ded = 0
    perf_ded = 0
    bp_ded = 0
    corr_ded = 0
    
    for i in issues:
        if language == 'javascript' and i.get('rule_id') == 'JS_BP_004':
            continue
        
        sev = i.get('severity', 'info')
        cat = i.get('category', 'best_practices')
        title = i.get('title', 'Issue')
        penalty = 15 if sev == 'critical' else 7 if sev == 'warning' else 2
        if cat == 'correctness': 
            corr_ded += penalty * 1.5 # 22.5 for critical correctness
        elif cat == 'performance': perf_ded += penalty
        elif cat == 'readability': read_ded += penalty
        else: bp_ded += penalty
        
        if len(deductions) < 8:
            deductions.append(f"{title}: -{penalty}")

    breakdown["syntax_safety"] = max(0, breakdown["syntax_safety"] - (syntax_deduction + corr_ded))
    breakdown["readability"] = max(0, breakdown["readability"] - read_ded)
    breakdown["performance"] = max(0, breakdown["performance"] - perf_ded)
    breakdown["best_practices"] = max(0, breakdown["best_practices"] - bp_ded)
    breakdown["structure"] = int((ml_struct_score / 100) * 15)
    
    final_score = sum(breakdown.values())
    
    # Boost score for clean code
    is_very_clean = not any(i['severity'] in ['critical', 'warning'] for i in issues)
    if is_very_clean and confidence > 0.9:
        final_score = max(final_score, 92) # Guaranteed Excellent
    elif is_very_clean and confidence > 0.7:
        final_score = max(final_score, 85) # Guaranteed Good/Great
    
    return int(final_score), breakdown, deductions

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data.get('code', '')
    selected_language = data.get('language', 'javascript').lower()
    
    issues = []
    steps = []
    
    # Language Detection
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
        
    # AST Parsing
    tree, confidence, error = parse_code(code, selected_language)
    if error:
        print(f"AST Parse Error: {error}")
        
    # ML Prediction
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
            
    # Heuristic Analysis
    base_issues, base_steps = analyze_base(code, tree)
    issues.extend(base_issues)
    

    lang_analyzer = get_heuristics(selected_language)
    lang_issues, lang_steps = lang_analyzer(code, tree)
    issues.extend(lang_issues)

    # Optimization
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
    
    # Feed optimizer findings back into issues
    for pattern in optimization_result.get("patterns_found", []):
        issues.append({
            "severity": pattern.get("impact", "info").lower() if pattern.get("impact") != "High" else "warning",
            "title": pattern.get("title", "Optimization Hint"),
            "description": pattern.get("reasoning", pattern.get("description", "Structural improvement suggested.")),
            "category": "performance",
            "rule_id": pattern.get("id", pattern.get("rule_id", "DEEP_OPT"))
        })

    # Scoring
    ml_struct_score = ml_results.get("structural_quality_score", 80) if ml_results else 80
    overall_score, score_breakdown, score_deductions = calculate_detailed_score(
        issues, ml_struct_score, confidence, is_critical_mismatch, selected_language
    )

    if confidence < 0.5 and not is_critical_mismatch:
        issues.append({
            "severity": "critical",
            "title": "Poor Syntax Quality",
            "description": f"Code parsing confidence is low ({int(confidence*100)}%). Ensure the code is complete and syntactically correct.",
            "category": "correctness",
            "rule_id": "LOW_CONFIDENCE"
        })
    
    # Verdict Generation
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


    dna = {
        "complexity_profile": "Linear" if ml_results.get("cyclomatic_complexity", 0) < 5 else "Moderate" if ml_results.get("cyclomatic_complexity", 0) < 15 else "High-Complexity",
        "primary_risk": ml_results.get("danger_level", "None").capitalize(),
        "style_verdict": ml_results.get("maintainability", "Good").capitalize(),
        "ai_score": f"{int(ml_results.get('ai_generated_probability', 0) * 100)}%"
    }

    result = {
        "score": {
            "overall": overall_score,
            "breakdown": score_breakdown,
            "deductions": score_deductions
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
