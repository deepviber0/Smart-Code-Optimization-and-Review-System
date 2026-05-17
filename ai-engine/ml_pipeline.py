import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from collections import Counter
import math


# Training corpora for AST sequence analysis

_GOOD_HUMAN_CODE = [
    # Python: typical utility functions
    "module import_statement function_definition parameters block assignment_statement if_statement comparison return_statement",
    "module function_definition parameters typed_parameter block for_statement block expression_statement call identifier",
    "module class_definition block function_definition parameters block assignment_statement return_statement binary_expression",
    "module decorated_definition function_definition parameters block with_statement block expression_statement return_statement",
    "module import_from_statement function_definition parameters block list_comprehension call identifier return_statement",
    "module function_definition parameters block try_statement block expression_statement except_clause block raise_statement",
    "module function_definition parameters block while_statement block assignment_statement augmented_assignment if_statement break_statement",
    "module class_definition block function_definition parameters block dictionary comprehension return_statement",
    # JavaScript: idiomatic modern JS
    "program lexical_declaration identifier arrow_function block return_statement ternary_expression identifier",
    "program function_declaration identifier parameters block lexical_declaration call_expression member_expression",
    "program export_statement function_declaration identifier parameters block for_statement block expression_statement",
    "program lexical_declaration identifier object call_expression identifier template_string",
    "program class_declaration identifier class_body method_definition block return_statement member_expression",
    "program import_statement import_clause identifier string function_declaration identifier parameters block",
    # Java: standard patterns
    "class_declaration modifiers identifier class_body method_declaration modifiers void_type identifier block",
    "class_declaration identifier class_body constructor_declaration identifier parameters block assignment_expression",
    "class_declaration identifier class_body method_declaration modifiers type_identifier identifier parameters block for_statement",
    "class_declaration identifier interface_declaration class_body method_declaration modifiers generic_type",
    # C: procedural patterns
    "translation_unit preproc_include function_definition type_specifier identifier parameter_list compound_statement declaration",
    "translation_unit function_definition compound_statement for_statement compound_statement assignment_expression call_expression",
    "translation_unit preproc_def function_definition pointer_declarator compound_statement if_statement return_statement",
    # C++: OOP patterns
    "translation_unit namespace_definition class_specifier visibility_label method_definition compound_statement return_statement",
    "translation_unit template_declaration class_specifier identifier visibility_label method_definition lambda_expression",
]

_BAD_CODE = [
    # Dangerous / suspicious patterns
    "module function_definition parameters block call identifier eval argument_list string",
    "module function_definition block call identifier exec string assignment_statement",
    "program function_declaration block call_expression identifier string eval",
    "translation_unit function_definition compound_statement call_expression gets string",
    "translation_unit preproc_include function_definition compound_statement call_expression strcpy pointer_declarator",
    "module function_definition block while_statement true block assignment_statement call identifier append",
    "program lexical_declaration while_statement binary_expression assignment_expression augmented_assignment",
    "module import_statement function_definition block call subprocess shell true string",
    "class_declaration method_declaration block call_expression method_invocation reflect invoke",
    "translation_unit function_definition compound_statement pointer_expression assignment_expression integer_literal",
    # AI hallucination-like: overly uniform, repetitive
    "module function_definition block try_statement except_clause return_statement function_definition block try_statement except_clause return_statement",
    "program arrow_function block try_statement catch_clause return_statement arrow_function block try_statement catch_clause return_statement",
    "class_declaration class_body method_declaration block try_statement catch_clause method_declaration block try_statement catch_clause",
    "module function_definition parameters block if_statement block return_statement else_clause block return_statement function_definition parameters block if_statement block return_statement else_clause block return_statement",
]

_AI_GENERATED_CODE = [
    # Over-structured, deeply nested try/catch everywhere
    "module function_definition parameters block try_statement block expression_statement except_clause block return_statement",
    "program arrow_function block try_statement block expression_statement catch_clause block return_statement",
    "class_declaration class_body method_declaration block try_statement block method_invocation catch_clause block return_statement",
    # Redundant type annotations and docstrings in every function
    "module function_definition parameters typed_parameter typed_parameter typed_parameter block expression_statement string return_statement",
    "module function_definition parameters block expression_statement string if_statement block return_statement else_clause block return_statement",
    "module class_definition block function_definition parameters block expression_statement string for_statement block if_statement block continue_statement expression_statement return_statement",
    # Boilerplate-heavy Java
    "class_declaration modifiers identifier class_body method_declaration modifiers type_identifier identifier parameters block try_statement catch_clause finally_clause",
    "class_declaration modifiers identifier class_body constructor_declaration parameters block try_statement catch_clause return_statement method_declaration",
    # Overly symmetric C++
    "translation_unit namespace_definition class_specifier visibility_label method_definition compound_statement try_statement catch_clause",
    "translation_unit template_declaration class_specifier visibility_label method_definition compound_statement try_statement catch_clause method_definition compound_statement try_statement",
    # Verbose JS with consistent promise chaining
    "program function_declaration identifier parameters block return_statement call_expression member_expression then_clause catch_clause finally_clause",
    "program lexical_declaration arrow_function block try_statement block await_expression catch_clause block return_statement finally_clause",
]




DANGEROUS_NODES = frozenset({
    'eval', 'exec', 'gets', 'system', 'popen', 'strcpy', 'strcat',
    'sprintf', 'vsprintf', 'scanf',
    'shell', 'subprocess', 'pickle', 'marshal',
    'reflect', 'invoke', 'classloader',
    'innerHTML', 'outerHTML', 'document_write',
    'eval_expression', 'dynamic_import',
})


COMPLEXITY_NODES = frozenset({
    'if_statement', 'elif_clause', 'else_clause',
    'for_statement', 'while_statement', 'do_statement',
    'switch_statement', 'case_clause',
    'try_statement', 'except_clause', 'catch_clause', 'finally_clause',
    'conditional_expression', 'ternary_expression',
    'and_operator', 'or_operator', 'boolean_operator',
    'lambda', 'arrow_function', 'generator_expression',
    'match_statement', 'case_clause',
    'break_statement', 'continue_statement', 'goto_statement',
})


QUALITY_NODES = frozenset({
    'function_definition', 'function_declaration', 'method_declaration',
    'method_definition', 'class_definition', 'class_declaration',
    'class_specifier', 'interface_declaration', 'constructor_declaration',
    'import_statement', 'import_from_statement', 'import_declaration',
    'decorated_definition', 'annotation',
    'try_statement', 'except_clause', 'catch_clause',  # error handling = quality
    'with_statement',
    'type_definition', 'typedef', 'type_alias_statement',
    'typed_parameter', 'keyword_argument',
    'return_statement', 'yield', 'yield_expression',
    'assert_statement',
    'namespace_definition', 'template_declaration',
    'enum_declaration', 'enum_specifier',
})


AI_SIGNAL_NODES = frozenset({
    'try_statement', 'catch_clause', 'except_clause', 'finally_clause',
    'return_statement', 'string',
    'expression_statement',
})


class ASTFeatureVector:
    __slots__ = (
        'sequence', 'node_counts', 'max_depth', 'total_nodes',
        'cyclomatic_complexity', 'dangerous_node_count',
        'quality_node_ratio', 'ai_signal_ratio',
        'depth_breadth_ratio', 'unique_node_ratio',
        'avg_fanout', 'leaf_ratio',
        'top_node_concentration',
        'bigram_sequence',
    )

    def __init__(self):
        for s in self.__slots__:
            setattr(self, s, None)


class MLAnalyzer:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            token_pattern=r'(?u)\b\w+\b',
            max_features=200,
            sublinear_tf=True,
            ngram_range=(1, 1),
        )
        self.bigram_vectorizer = TfidfVectorizer(
            token_pattern=r'(?u)\b\w+\b',
            max_features=300,
            sublinear_tf=True,
            ngram_range=(1, 3),
        )
        self.anomaly_detector = IsolationForest(
            n_estimators=200,
            contamination=0.12,
            max_samples='auto',
            random_state=42,
        )

        _base_ai = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42,
        )
        self.ai_detector = CalibratedClassifierCV(_base_ai, cv=3, method='isotonic')

        self.quality_scaler = StandardScaler()

        self.is_trained = False



    def extract_features(self, tree) -> ASTFeatureVector:
        fv = ASTFeatureVector()

        sequence        = []
        bigram_seq      = []
        node_counts     = Counter()
        depth_sum       = 0
        node_depths     = []
        children_counts = []
        leaf_count      = 0
        max_depth       = 0

        def traverse(node, depth):
            nonlocal max_depth, leaf_count
            if depth > max_depth:
                max_depth = depth

            node_type = node.type
            is_named  = node.is_named

            if is_named:
                sequence.append(node_type)
                node_counts[node_type] += 1
                node_depths.append(depth)
                depth_sum_ref[0] += depth
                children_counts.append(len(node.children))
                if not node.children:
                    leaf_count += 1

            for i, child in enumerate(node.children):
                if is_named and i > 0:
                    prev = node.children[i - 1]
                    if prev.is_named:
                        bigram_seq.append(f"{prev.type}__{child.type}")
                traverse(child, depth + 1)

        depth_sum_ref = [0]
        traverse(tree.root_node, 0)

        total = len(sequence)
        fv.sequence       = " ".join(sequence)
        fv.bigram_sequence= " ".join(bigram_seq)
        fv.node_counts    = node_counts
        fv.total_nodes    = total
        fv.max_depth      = max_depth

        fv.cyclomatic_complexity = sum(
            node_counts[n] for n in COMPLEXITY_NODES if n in node_counts
        )

        fv.dangerous_node_count = sum(
            node_counts[n] for n in DANGEROUS_NODES if n in node_counts
        )

        quality_hits = sum(node_counts[n] for n in QUALITY_NODES if n in node_counts)
        fv.quality_node_ratio = quality_hits / max(total, 1)

        ai_hits = sum(node_counts[n] for n in AI_SIGNAL_NODES if n in node_counts)
        fv.ai_signal_ratio = ai_hits / max(total, 1)

        fv.depth_breadth_ratio = (
            max_depth / math.log2(max(total, 2))
        ) if total > 1 else 0.0

        fv.unique_node_ratio = len(node_counts) / max(total, 1)

        fv.avg_fanout = (
            sum(children_counts) / len(children_counts)
        ) if children_counts else 0.0

        fv.leaf_ratio = leaf_count / max(total, 1)

        if total > 0:
            top_count = node_counts.most_common(1)[0][1]
            fv.top_node_concentration = top_count / total
        else:
            fv.top_node_concentration = 0.0

        return fv

    def _build_quality_feature_vector(self, fv: ASTFeatureVector):
        return np.array([
            fv.total_nodes,
            fv.max_depth,
            fv.cyclomatic_complexity,
            fv.dangerous_node_count,
            fv.quality_node_ratio,
            fv.ai_signal_ratio,
            fv.depth_breadth_ratio,
            fv.unique_node_ratio,
            fv.avg_fanout,
            fv.leaf_ratio,
            fv.top_node_concentration,
            fv.cyclomatic_complexity / max(fv.quality_node_ratio * fv.total_nodes, 1),
            (fv.node_counts.get('try_statement', 0) + fv.node_counts.get('with_statement', 0))
            / max(fv.node_counts.get('function_definition', 0)
                  + fv.node_counts.get('function_declaration', 0)
                  + fv.node_counts.get('method_declaration', 0), 1),
        ], dtype=np.float64)



    def train_dummy_models(self):
        all_sequences = _GOOD_HUMAN_CODE + _BAD_CODE + _AI_GENERATED_CODE
        all_sequences_aug = all_sequences * 3

        X_uni   = self.vectorizer.fit_transform(all_sequences_aug)
        X_bi    = self.bigram_vectorizer.fit_transform(all_sequences_aug)


        n_good  = len(_GOOD_HUMAN_CODE) * 3
        self.anomaly_detector.fit(X_uni[:n_good])


        labels = (
            [0] * (len(_GOOD_HUMAN_CODE) * 3)
            + [0] * (len(_BAD_CODE) * 3)
            + [1] * (len(_AI_GENERATED_CODE) * 3)
        )
        self.ai_detector.fit(X_bi, labels)

        dummy_features = np.random.default_rng(42).random((60, 13))
        self.quality_scaler.fit(dummy_features)

        self.is_trained = True



    def _compute_structural_score(self, fv: ASTFeatureVector, anomaly_raw: float) -> int:
        base = min(100, max(0, int((anomaly_raw + 0.25) * 200)))

        if fv.max_depth > 8:
            base -= (fv.max_depth - 8) * 3

        if fv.cyclomatic_complexity > 15:
            base -= (fv.cyclomatic_complexity - 15) * 2

        base -= fv.dangerous_node_count * 10

        base += int(fv.quality_node_ratio * 20)

        base += int(fv.unique_node_ratio * 15)

        if fv.top_node_concentration > 0.35:
            base -= int((fv.top_node_concentration - 0.35) * 40)

        return min(100, max(0, base))

    def _compute_ai_probability(self, fv: ASTFeatureVector, model_prob: float) -> float:
        heuristic = 0.0


        eh_count   = fv.node_counts.get('try_statement', 0) + \
                     fv.node_counts.get('except_clause', 0) + \
                     fv.node_counts.get('catch_clause', 0)
        func_count = (fv.node_counts.get('function_definition', 0)
                      + fv.node_counts.get('function_declaration', 0)
                      + fv.node_counts.get('method_declaration', 0))
        if func_count > 0 and (eh_count / func_count) > 1.5:
            heuristic += 0.15


        if fv.unique_node_ratio < 0.15:
            heuristic += 0.12


        if fv.ai_signal_ratio > 0.30:
            heuristic += 0.10


        if fv.top_node_concentration > 0.40:
            heuristic += 0.10

        blended = 0.65 * model_prob + 0.35 * min(1.0, heuristic)
        return round(min(1.0, max(0.0, blended)), 4)

    def _compute_danger_level(self, fv: ASTFeatureVector) -> str:
        d = fv.dangerous_node_count
        if d == 0:
            return "none"
        elif d == 1:
            return "low"
        elif d <= 3:
            return "medium"
        elif d <= 6:
            return "high"
        else:
            return "critical"

    def _compute_maintainability(self, fv: ASTFeatureVector) -> str:
        score = 0
        if fv.max_depth <= 5:          score += 2
        elif fv.max_depth <= 8:        score += 1
        if fv.cyclomatic_complexity <= 10: score += 2
        elif fv.cyclomatic_complexity <= 20: score += 1
        if fv.unique_node_ratio >= 0.25:  score += 1
        if fv.quality_node_ratio >= 0.20: score += 1
        if fv.avg_fanout <= 4.0:          score += 1

        if score >= 6:  return "excellent"
        if score >= 4:  return "good"
        if score >= 2:  return "fair"
        return "poor"



    def analyze(self, tree, language: str) -> dict:
        if not self.is_trained:
            self.train_dummy_models()

        fv = self.extract_features(tree)

        if not fv.sequence:
            fv.sequence        = "empty"
            fv.bigram_sequence = "empty"


        X_uni             = self.vectorizer.transform([fv.sequence])
        anomaly_score_raw = self.anomaly_detector.decision_function(X_uni)[0]
        is_anomalous      = bool(self.anomaly_detector.predict(X_uni)[0] == -1)
        structural_score  = self._compute_structural_score(fv, anomaly_score_raw)


        X_bi       = self.bigram_vectorizer.transform([fv.bigram_sequence])
        model_prob = self.ai_detector.predict_proba(X_bi)[0][1]
        ai_prob    = self._compute_ai_probability(fv, model_prob)


        danger_level    = self._compute_danger_level(fv)
        maintainability = self._compute_maintainability(fv)


        top_nodes = [
            {"node": n, "count": c}
            for n, c in fv.node_counts.most_common(10)
        ]


        dangerous_found = [
            n for n in DANGEROUS_NODES if fv.node_counts.get(n, 0) > 0
        ]

        return {
            "structural_quality_score":  structural_score,
            "ai_generated_probability":  ai_prob,
            "danger_level":              danger_level,
            "maintainability":           maintainability,
            "ast_node_count":            fv.total_nodes,
            "ast_max_depth":             fv.max_depth,
            "ast_unique_node_types":     len(fv.node_counts),
            "ast_avg_fanout":            round(fv.avg_fanout, 3),
            "ast_leaf_ratio":            round(fv.leaf_ratio, 3),

            "cyclomatic_complexity":     fv.cyclomatic_complexity,
            "top_node_concentration":    round(fv.top_node_concentration, 3),
            "unique_node_ratio":         round(fv.unique_node_ratio, 3),
            "quality_node_ratio":        round(fv.quality_node_ratio, 3),

            "dangerous_node_count":      fv.dangerous_node_count,
            "dangerous_nodes_found":     dangerous_found,

            "is_anomalous":              is_anomalous,
            "anomaly_decision_score":    round(float(anomaly_score_raw), 4),

            "top_10_node_types":         top_nodes,
            "language":                  language,
        }

    def analyze_batch(self, trees_and_langs: list[tuple]) -> list[dict]:
        if not self.is_trained:
            self.train_dummy_models()
        return [self.analyze(tree, lang) for tree, lang in trees_and_langs]



ml_analyzer = MLAnalyzer()
