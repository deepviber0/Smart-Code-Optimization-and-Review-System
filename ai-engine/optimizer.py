from optimizers.javascript import optimize_javascript as js_optimize
from optimizers.python import optimize_python as py_optimize
from optimizers.java import optimize_java as java_optimize
from optimizers.c_cpp import optimize_c_cpp as cpp_optimize
from ai_optimizer import DeepOptimizer
from pipeline_validators import PipelineValidators, ProtectionTimeout
from language_detector import detect_language_ast

class SafePipeline:
    def __init__(self, language):
        self.language = language
        self.validators = PipelineValidators(language)
        self.metadata = {
            "applied_rules": [],
            "skipped_rules": [],
            "failed_rules": [],
            "rollback_reasons": [],
            "snapshots": {}
        }
        self.findings = []
        self.legacy_rules_applied = set()
        
    def normalize_code(self, code):
        code = code.replace('\r\n', '\n')
        code = code.replace('\t', '    ')
        # Trailing whitespace removal
        code = '\n'.join([line.rstrip() for line in code.splitlines()])
        return code + '\n'

    def run(self, code, selected_language, issues):
        try:

            if not self.validators.check_file_size(code):
                return self._fail_safe(code, "File exceeds max optimization size limit.", issues)


            detected_lang, score = detect_language_ast(code)
            if detected_lang and detected_lang != selected_language and score > 0.6:
                self.language = detected_lang
                self.validators.language = detected_lang


            code = self.normalize_code(code)
            self.metadata["snapshots"]["original"] = code


            valid, msg = self.validators.validate_syntax(code)
            if not valid:
                return self._fail_safe(code, f"Structural check failed before optimization: {msg}", issues)

            # Duplicate removal and mask protected regions
            code = self.validators.remove_duplicate_functions(code)
            masked_code, masks = self.validators.mask_protected_regions(code)


            optimized_code = self._run_optimizations(masked_code, issues)

            restored_code = self.validators.restore_protected_regions(optimized_code, masks)
            

            restored_code = self._cleanup_code(restored_code)
            
            self.metadata["snapshots"]["optimized"] = restored_code

            # Final validation
            diff_valid, diff_msg = self.validators.validate_diff(code, restored_code)
            if not diff_valid:
                return self._fail_safe(code, f"Transformation diff failed: {diff_msg}", issues)

            syntax_valid, syntax_msg = self.validators.validate_syntax(restored_code)
            if not syntax_valid:
                return self._fail_safe(code, f"Final syntax check failed: {syntax_msg}", issues)



            return {
                "code": restored_code,
                "explanation": "Optimized using Safe Pipeline (Correctness priority).",
                "metadata": self.metadata,
                "patterns_found": self.findings
            }

        except ProtectionTimeout as e:
            return self._fail_safe(code, f"Optimization timeout: {str(e)}", issues)
        except Exception as e:
            return self._fail_safe(code, f"Unexpected error: {str(e)}", issues)

    def _fail_safe(self, code, reason, issues):
        self.metadata["rollback_reasons"].append(reason)
        return {
            "code": code,
            "explanation": f"Optimization skipped for safety. Reason: {reason}",
            "metadata": self.metadata,
            "patterns_found": issues
        }

    def _cleanup_code(self, code):
        lines = [line.rstrip() for line in code.splitlines()]
        cleaned_lines = []
        for i, line in enumerate(lines):
            if i > 0 and not line.strip() and not lines[i-1].strip():
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines) + "\n"

    def _safe_apply(self, rule_name, func, code, *args):
        self.validators.check_timeout()
        try:
            new_code = func(code, *args)
            if new_code == code:
                self.metadata["skipped_rules"].append(rule_name)
                return code


            valid, msg = self.validators.validate_syntax(new_code)
            diff_ok, _ = self.validators.validate_diff(code, new_code)
            
            if valid and diff_ok:
                self.metadata["applied_rules"].append({"rule": rule_name, "confidence": 0.95, "risk": "low"})
                return new_code
            else:
                self.metadata["failed_rules"].append(rule_name)
                self.metadata["rollback_reasons"].append(f"Rule {rule_name} broke syntax/diff.")
                return code
        except Exception as e:
            self.metadata["failed_rules"].append(rule_name)
            self.metadata["rollback_reasons"].append(f"Rule {rule_name} raised error: {str(e)}")
            return code

    def _run_optimizations(self, code, issues):
        MAX_OPTIMIZATION_PASSES = 3
        previous_code = ""
        passes = 0
        
        while code != previous_code and passes < MAX_OPTIMIZATION_PASSES:
            previous_code = code
            passes += 1
            

            if self.language == 'javascript':
                code = self._safe_apply("Legacy_JS", js_optimize, code, issues, self.legacy_rules_applied)
            elif self.language == 'python':
                code = self._safe_apply("Legacy_PY", py_optimize, code, issues, self.legacy_rules_applied)
            elif self.language == 'java':
                code = self._safe_apply("Legacy_JAVA", java_optimize, code, issues, self.legacy_rules_applied)
            elif self.language in ['c', 'cpp']:
                code = self._safe_apply("Legacy_CPP", cpp_optimize, code, issues, self.legacy_rules_applied)

            # Deep Optimizer pass
            deep_optimizer = DeepOptimizer(self.language)

            new_patterns = deep_optimizer._detect_patterns(code) + deep_optimizer._detect_logical_issues(code)
            for p in new_patterns:
                if p not in self.findings:
                    self.findings.append(p)
                    
            code = self._safe_apply("Deep_AI_Optimization", deep_optimizer.apply_safe_rules, code, issues)
            
        self.metadata["optimization_passes_run"] = passes
        return code

def optimize_code(code, language, issues):
    pipeline = SafePipeline(language)
    return pipeline.run(code, language, issues)
