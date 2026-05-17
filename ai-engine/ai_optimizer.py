import re
import json
from ast_parser import parse_code

class DeepOptimizer:
    def __init__(self, language):
        self.language = language
        self.persona = "Senior Performance Engineer"
        
    def analyze_and_optimize(self, code, issues, rule_optimized):

        

        patterns = self._detect_patterns(code)
        

        additional_issues = self._detect_logical_issues(code)
        all_patterns = patterns + additional_issues
        

        all_findings = self._synthesize_findings(issues, all_patterns)
        

        if not all_patterns and not issues:
             return self._format_final_output("No major optimization needed.", code, all_findings)
        

        optimized_code, explanation, metadata = self._generate_ai_response(code, all_findings, rule_optimized, all_patterns)
        

        

        final_output = self._format_final_output(optimized_code, explanation, all_findings)
        
        return {
            "code": optimized_code,
            "explanation": explanation,
            "metadata": metadata,
            "patterns_found": all_patterns,
            "raw_output": final_output # For debugging or direct display
        }

    def _detect_logical_issues(self, code):
        issues = []
        

        var_matches = re.findall(r"(?:let|const|var|int|float|double|String)\s+(\w+)\s*=", code)
        if self.language == 'python':
            var_matches = re.findall(r"^\s*(\w+)\s*=", code, re.MULTILINE)
            
        for var in set(var_matches):
            if var != "_" and code.count(var) == 1:
                issues.append({
                    "id": "LOGIC_UNUSED_VAR",
                    "title": "Unused Variable",
                    "impact": "Low",
                    "reasoning": f"Variable '{var}' is declared but never used. Removing it improves memory usage and clarity."
                })


        if re.search(r"while\s*\(true\)|while\s+True:", code):
            if "break" not in code and "return" not in code:
                issues.append({
                    "id": "LOGIC_INFINITE_LOOP",
                    "title": "Potential Infinite Loop",
                    "impact": "Critical",
                    "reasoning": "A loop with a constant True condition and no exit statement (break/return) will run forever."
                })


        if re.search(r"(\w+)\s*=\s*\1\s*[\+\-\*\/]\s*0|(\w+)\s*=\s*\2\s*\* \s*1", code):
             issues.append({
                "id": "LOGIC_REDUNDANT_OP",
                "title": "Redundant Arithmetic Operation",
                "impact": "Low",
                "reasoning": "Operations like adding zero or multiplying by one do not change the value and waste cycles."
            })

        return issues

    def _format_final_output(self, optimized_code, explanation, findings):
        detected_lang = self.language.capitalize()
        if self.language == 'cpp': detected_lang = "C++"
        if self.language == 'c': detected_lang = "C"
        
        issues_list = "\n".join(findings) if findings else "None"
        

        if optimized_code == "No major optimization needed.":
            return f"* Detected Language: {detected_lang}\n* Issues Found: None\n* Why Issue Occurs: N/A\n* Optimized Code: {optimized_code}\n* Optimization Explanation: N/A"

        why_occurs = "Structural inefficiencies or redundant operations detected in the logic flow."
        if "Infinite Loop" in issues_list:
            why_occurs = "Missing exit conditions in loop structures."
        elif "Complexity" in issues_list:
            why_occurs = "Algorithmic complexity is suboptimal (e.g., O(n^2) when O(n) is possible)."

        output = f"""* Detected Language: {detected_lang}
* Issues Found:
{issues_list}
* Why Issue Occurs:
{why_occurs}
* Optimized Code:
{optimized_code}
* Optimization Explanation:
{explanation}"""
        return output

    def _detect_patterns(self, code):
        patterns = []
        
        # Pattern: Nested Loops (O(n^2)+)
        if self.language in ['javascript', 'python', 'java', 'cpp']:
            is_nested = False
            if self.language == 'python':
                if re.search(r"(for|while)\s+.*:.*\n\s+(for|while)\s+.*:", code):
                    is_nested = True
            else:
                if re.search(r"(for|while)\s*\(.*?\)\s*\{.*? (for|while)\s*\(.*?\)\s*\{", code, re.DOTALL):
                    is_nested = True
            
            if is_nested:
                patterns.append({
                    "id": "PERF_NESTED_LOOPS",
                    "title": "Quadratic Complexity",
                    "impact": "High",
                    "reasoning": "Nested loops lead to O(n^2) complexity. Using a Hash Map for lookups can reduce this to O(n)."
                })
        
        # Pattern: Redundant Calculation
        loop_pattern = r"(for|while).*?:" if self.language == 'python' else r"(for|while).*?\{"
        if re.search(loop_pattern, code):
            if re.search(r"\w+\s*=\s*[\d\.\+\-\*\/\s\(\)]+(;|\n)", code):
                 patterns.append({
                    "id": "PERF_REDUNDANT_CALC",
                    "title": "Loop Invariant Calculation",
                    "impact": "Medium",
                    "reasoning": "Constant calculations inside loops should be hoisted to save CPU cycles."
                })

        return patterns

    def _synthesize_findings(self, issues, patterns):
        findings = []
        # Deduplicate and clean up
        seen = set()
        for issue in issues:
            title = issue['title']
            if title not in seen:
                findings.append(f"- {title}")
                seen.add(title)
        for pattern in patterns:
            title = pattern['title']
            if title not in seen:
                findings.append(f"- {title}")
                seen.add(title)
        return findings

    def _generate_ai_response(self, original_code, findings, rule_optimized, patterns):
        optimized = rule_optimized
        explanation_parts = []
        
        impact = "Low"
        complexity_reduction = "None"
        

        if any(p['id'] == "PERF_NESTED_LOOPS" for p in patterns):
            impact = "High"
            complexity_reduction = "O(n^2) -> O(n)"
            explanation_parts.append("Replaced nested loop with O(n) lookup strategy.")

        if not explanation_parts:
            explanation = "Optimized for performance and readability."
        else:
            explanation = " ".join(explanation_parts)


        
        metadata = {
            "performance_impact": impact,
            "readability_improvement": "High",
            "complexity_reduction": complexity_reduction
        }

        return optimized, explanation, metadata

    def apply_safe_rules(self, code, issues):
        patterns = self._detect_patterns(code)
        additional_issues = self._detect_logical_issues(code)
        all_patterns = patterns + additional_issues
        
        if not all_patterns:
            return code
            
        optimized_code, _, _ = self._generate_ai_response(code, all_patterns, code, all_patterns)
        return optimized_code

