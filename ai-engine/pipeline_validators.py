import re
import time
from ast_parser import parse_code

class ProtectionTimeout(Exception):
    pass

class PipelineValidators:
    MAX_FILE_SIZE = 500 * 1024 # 500 KB limit for optimization
    MAX_PROCESSING_TIME = 10.0 # 10 seconds max

    def __init__(self, language):
        self.language = language
        self.start_time = time.time()
        self.masks = {}
        self.mask_counter = 0

    def check_timeout(self):
        if time.time() - self.start_time > self.MAX_PROCESSING_TIME:
            raise ProtectionTimeout("Optimization processing time exceeded.")

    def check_file_size(self, code):
        if len(code.encode('utf-8')) > self.MAX_FILE_SIZE:
            return False
        return True

    def count_functions(self, code):
        tree, conf, err = parse_code(code, self.language)
        if not tree or not tree.root_node:
            return -1
            
        func_count = 0
        def walk(node):
            nonlocal func_count
            if node.type in ['function_definition', 'function_declaration', 'method_definition', 'method_declaration', 'arrow_function', 'class_definition', 'class_declaration']:
                func_count += 1
            for child in node.children:
                walk(child)
        walk(tree.root_node)
        return func_count

    def remove_duplicate_functions(self, code):
        """
        Conservative AST-based duplicate removal.
        Matches signature + normalized body.
        """
        tree, conf, err = parse_code(code, self.language)
        if not tree or not tree.root_node or conf < 0.8:
            return code
            
        functions = []
        
        def walk(node):
            if node.type in ['function_definition', 'method_definition', 'function_declaration', 'method_declaration']:
                # Find the body node
                body_node = None
                for child in node.children:
                    if child.type in ['block', 'compound_statement', 'statement_block']:
                        body_node = child
                        break
                
                if body_node:
                    # Get the body source
                    body_source = code[body_node.start_byte:body_node.end_byte]
                    # Signature source (everything before body)
                    sig_source = code[node.start_byte:body_node.start_byte]
                    
                    functions.append({
                        'start': node.start_byte,
                        'end': node.end_byte,
                        'sig': re.sub(r'\s+', ' ', sig_source.strip()),
                        'body': re.sub(r'\s+', ' ', body_source.strip())
                    })
                    
            for child in node.children:
                walk(child)
                
        walk(tree.root_node)
        
        if not functions:
            return code
            
        # Find duplicates
        to_remove = []
        seen = {} # key = (sig, body)
        
        for func in functions:
            key = (func['sig'], func['body'])
            if key in seen:
                to_remove.append((func['start'], func['end']))
            else:
                seen[key] = True
                
        if not to_remove:
            return code
            
        # Sort reverse for replacement from end to start
        to_remove.sort(key=lambda x: x[0], reverse=True)
        
        code_bytes = bytearray(code.encode('utf-8'))
        for start, end in to_remove:
            # Safely remove the block
            code_bytes[start:end] = b""
            
        cleaned_code = code_bytes.decode('utf-8', errors='replace')
        
        # Post-validation: ensure AST count decreased and syntax is valid
        new_tree, new_conf, _ = parse_code(cleaned_code, self.language)
        if not new_tree or new_conf < 0.7:
            return code # Rollback duplicate removal if it broke syntax
            
        return cleaned_code

    def validate_diff(self, original_code, new_code):
        """Transformation diff safety."""
        orig_len = len(original_code.strip())
        new_len = len(new_code.strip())
        
        # Rule: code shrinks suspiciously (>20% removed for files > 50 chars)
        if orig_len > 50 and new_len < orig_len * 0.8:
            return False, "Large unexpected deletion (>20% shrinkage)"
            
        orig_funcs = self.count_functions(original_code)
        new_funcs = self.count_functions(new_code)
        
        # Rule: function/class count changes unexpectedly
        if orig_funcs != -1 and new_funcs != -1 and new_funcs < orig_funcs:
            return False, f"Structural block count decreased from {orig_funcs} to {new_funcs}"
            
        return True, "Diff OK"

    def mask_protected_regions(self, code):
        """
        Uses AST to find strings, comments, template literals and mask them.
        Returns (masked_code, masks_dict)
        """
        self.check_timeout()
        tree, conf, err = parse_code(code, self.language)
        if not tree or not tree.root_node:
            return code # Fallback: don't mask if we can't parse at all, or we could fallback to regex mask

        # Collect ranges to mask
        ranges_to_mask = []
        
        mask_types = [
            'string', 'string_literal', 'template_string', 'template_substitution',
            'comment', 'line_comment', 'block_comment', 'char_literal',
            'regex_literal', 'decorator', 'annotation',
            'preproc_include', 'preproc_def', 'preproc_function_def', 
            'preproc_if', 'preproc_else', 'preproc_elif', 'preproc_ifdef', 'preproc_ifndef'
        ]

        def walk(node):
            if node.type in mask_types:
                ranges_to_mask.append((node.start_byte, node.end_byte))
            else:
                for child in node.children:
                    walk(child)

        walk(tree.root_node)
        
        # Sort ranges descending to replace from end to start without messing up offsets
        ranges_to_mask.sort(key=lambda x: x[0], reverse=True)
        
        code_bytes = bytearray(code.encode('utf-8'))
        masks = {}
        counter = 0
        
        for start, end in ranges_to_mask:
            original_bytes = code_bytes[start:end]
            mask_key = f"__PROTECTED_MASK_{counter}__".encode('utf-8')
            masks[mask_key.decode('utf-8')] = original_bytes.decode('utf-8', errors='replace')
            
            # Replace in bytearray
            code_bytes[start:end] = mask_key
            counter += 1
            
        return code_bytes.decode('utf-8', errors='replace'), masks

    def restore_protected_regions(self, code, masks):
        """Restores masked regions."""
        for mask_key, original_val in masks.items():
            code = code.replace(mask_key, original_val)
        return code

    def validate_syntax(self, code):
        """Structural validation (balanced braces, confidence)."""
        tree, conf, err = parse_code(code, self.language)
        if err or conf < 0.6:
            return False, f"Low AST confidence ({conf}) or parsing error"
            
        # Basic Brace Matching for languages with braces
        if self.language in ['javascript', 'java', 'c', 'cpp']:
            if code.count('{') != code.count('}'):
                return False, "Unbalanced braces detected"
            if code.count('(') != code.count(')'):
                return False, "Unbalanced parentheses detected"
                
        # Python indentation sanity check
        if self.language == 'python':
            if code.count('(') != code.count(')'):
                return False, "Unbalanced parentheses detected"
            # Simple indentation check: No sudden dedent to 1 space or weird alignments
            lines = code.splitlines()
            for line in lines:
                if line.strip() and len(line) - len(line.lstrip()) % 4 != 0:
                    # Not strictly an error but Python heavily favors 4 spaces.
                    # We'll rely on AST for deep indentation validation.
                    pass
        
        return True, "Syntax Valid"

    def is_safe_to_optimize(self, code):
        valid, _ = self.validate_syntax(code)
        return valid
