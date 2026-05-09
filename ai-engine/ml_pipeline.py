import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from collections import Counter

class MLAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b', max_features=100)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.ai_detector = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_trained = False

    def extract_ast_features(self, tree):
        """
        Extracts structural features from AST including sequences, frequency, and depth.
        """
        sequence = []
        node_types = Counter()
        max_depth = 0
        
        def traverse(node, current_depth):
            nonlocal max_depth
            if current_depth > max_depth:
                max_depth = current_depth
                
            if node.is_named:
                sequence.append(node.type)
                node_types[node.type] += 1
                
            for child in node.children:
                traverse(child, current_depth + 1)
                
        traverse(tree.root_node, 0)
        return " ".join(sequence), max_depth, len(sequence)

    def train_dummy_models(self):
        """
        Trains models on a small set of dummy AST representations to demonstrate the pipeline.
        In production, this would load pre-trained binary models.
        """
        good_code = [
            "module function_definition block expression_statement call identifier argument_list string",
            "program variable_declaration identifier arrow_function block return_statement binary_expression",
            "class_declaration identifier class_body method_declaration identifier block local_variable_declaration",
            "translation_unit function_definition compound_statement declaration identifier call_expression",
            "module import_statement function_definition parameters block if_statement comparison_operator return"
        ] * 10
        
        bad_code = [
            "module function_definition parameters block call identifier argument_list eval",
            "program variable_declaration identifier binary_expression assignment_expression while_loop",
            "translation_unit function_definition compound_statement call_expression gets",
            "module function_definition block for_statement block assignment_expression call identifier append"
        ] * 10
        
        ai_code = [
            "module function_definition parameters block try_statement catch_clause return_statement",
            "program arrow_function block try_statement catch_clause return_statement",
            "class_declaration class_body method_declaration block try_statement catch_clause"
        ] * 10

        all_ast = good_code + bad_code + ai_code
        X_vectors = self.vectorizer.fit_transform(all_ast)
        
        self.anomaly_detector.fit(X_vectors)
        
        # 0: Human, 1: AI
        y_labels = [0]*len(good_code) + [0]*len(bad_code) + [1]*len(ai_code)
        self.ai_detector.fit(X_vectors, y_labels)
        
        self.is_trained = True

    def analyze(self, tree, language):
        if not self.is_trained:
            self.train_dummy_models()
            
        sequence, depth, count = self.extract_ast_features(tree)
        if not sequence:
            sequence = "empty"
            
        vectorized = self.vectorizer.transform([sequence])
        
        # Isolation Forest logic (-1 for anomaly, 1 for normal)
        anomaly_score_raw = self.anomaly_detector.decision_function(vectorized)[0]
        # Normalize structural score
        structure_score = min(100, max(0, int((anomaly_score_raw + 0.3) * 100)))
        
        # Depth penalty (too deep = complex code)
        if depth > 5:
            structure_score = max(0, structure_score - (depth - 5) * 2)
            
        ai_prob = self.ai_detector.predict_proba(vectorized)[0][1]
        
        return {
            "structural_quality_score": structure_score,
            "ai_generated_probability": float(ai_prob),
            "ast_node_count": count,
            "ast_max_depth": depth,
            "is_anomalous": bool(self.anomaly_detector.predict(vectorized)[0] == -1)
        }

ml_analyzer = MLAnalyzer()
