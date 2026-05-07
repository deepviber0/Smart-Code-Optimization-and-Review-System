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
        good_code = ["function_declaration identifier formal_parameters block let_declaration"] * 20
        bad_code = ["function_declaration identifier formal_parameters block var_declaration while_statement empty_statement"] * 5
        ai_code = ["function_declaration identifier formal_parameters block try_statement catch_clause return_statement"] * 10

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
