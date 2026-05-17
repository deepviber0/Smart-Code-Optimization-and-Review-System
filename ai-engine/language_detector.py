from ast_parser import parse_code


LANGUAGE_FINGERPRINTS = {
    'javascript': {
        'program':                     1.0,  # JS/TS root node
        'statement_block':             0.7,  # { ... } in JS
        'expression_statement':        0.5,
        'sequence_expression':         0.7,  # a, b, c
        # Declarations
        'variable_declaration':        0.8,  # var
        'lexical_declaration':         1.0,  # let / const
        'function_declaration':        0.6,
        'generator_function':          1.0,  # function*
        'class_declaration':           0.5,
        'class_body':                  0.5,

        'arrow_function':              1.0,  # () => {}
        'function':                    0.7,
        'method_definition':           0.8,
        'call_expression':             0.5,

        'template_string':             1.0,  # `template ${literal}`
        'template_substitution':       1.0,
        'tagged_template_expression':  1.0,
        'spread_element':              0.9,  # ...arr
        'rest_pattern':                0.9,
        'optional_chain':              1.0,  # obj?.prop
        'await_expression':            0.9,
        'yield_expression':            0.9,

        'object_pattern':              0.9,  # {a, b} = obj
        'array_pattern':               0.9,  # [a, b] = arr
        'shorthand_property_identifier_pattern': 1.0,

        'export_statement':            1.0,
        'import_statement':            0.8,
        'import_specifier':            1.0,
        'export_specifier':            1.0,
        'namespace_import':            1.0,  # import * as

        'async':                       0.8,

        'jsx_element':                 1.0,
        'jsx_self_closing_element':    1.0,
        'jsx_expression':              1.0,

        'typeof':                      0.9,  # typeof x
        'void_operator':               0.9,  # void 0
        'delete_statement':            0.8,
        'in_operator':                 0.7,  # key in obj
        'instanceof_expression':       0.7,
        'ternary_expression':          0.5,
        'new_expression':              0.5,
        'null':                        0.6,  # null literal node
        'undefined':                   0.9,
        'console':                     0.9,

        'let':                         1.0,
        'const':                       1.0,
        'async':                       0.9,
        'await':                       0.9,
    },

    'python': {
        'module':                      1.0,  # Python root node
        'block':                       1.0,  # indentation block
        'pass_statement':              1.0,  # pass

        'function_definition':         1.0,  # def
        'class_definition':            0.9,
        'decorated_definition':        1.0,  # @decorator
        'lambda':                      1.0,

        'import_statement':            0.7,
        'import_from_statement':       1.0,  # from x import y
        'aliased_import':              0.9,
        'wildcard_import':             1.0,  # from x import *

        'list_comprehension':          1.0,
        'dictionary_comprehension':    1.0,
        'set_comprehension':           1.0,
        'generator_expression':        1.0,

        'for_statement':               0.6,
        'while_statement':             0.5,
        'if_statement':                0.5,
        'elif_clause':                 1.0,  # elif is Python-only
        'else_clause':                 0.6,
        'with_statement':              1.0,  # with open(...) as f:
        'match_statement':             1.0,  # Python 3.10+ match
        'case_clause':                 1.0,

        'try_statement':               0.6,
        'except_clause':               1.0,  # except (not catch)
        'except_group_clause':         1.0,
        'raise_statement':             1.0,
        'finally_clause':              0.7,

        'yield':                       0.9,
        'yield_expression':            0.9,
        'await':                       0.8,
        'not_operator':                1.0,  # 'not' keyword
        'boolean_operator':            0.8,  # and / or
        'comparison_operator':         0.7,
        'augmented_assignment':        0.7,
        'walrus_operator':             1.0,  # :=

        'list':                        0.5,
        'dictionary':                  0.7,
        'set':                         0.7,
        'tuple':                       0.8,
        'pair':                        0.7,  # dict key:value

        'keyword_argument':            1.0,  # func(a=1)
        'default_parameter':           1.0,
        'typed_parameter':             1.0,  # def f(x: int)
        'type_alias_statement':        1.0,
        'type':                        0.6,
        'none':                        1.0,  # None literal
        'true':                        0.8,  # True
        'false':                       0.8,  # False

        'string':                      0.4,
        'concatenated_string':         0.8,
        'interpolation':               0.9,  # f-string {}

        'global_statement':            1.0,
        'nonlocal_statement':          1.0,
        'delete_statement':            0.8,  # del x
        'assert_statement':            0.9,
        'print_statement':             0.8,  # Python 2 / identifier
        'ellipsis':                    1.0,  # ...
        'star_expression':             0.9,  # *args
        'double_star_expression':      1.0,  # **kwargs
    },

    'java': {
        # Root / structural
        'program':                     0.4,  # shared with JS but context differs
        'class_declaration':           0.8,
        'class_body':                  0.7,
        'interface_declaration':       1.0,
        'enum_declaration':            1.0,
        'annotation_type_declaration': 1.0,
        'record_declaration':          1.0,  # Java 16+
        # Package / imports
        'package_declaration':         1.0,
        'import_declaration':          1.0,  # Java-specific node name
        # Members
        'method_declaration':          1.0,
        'constructor_declaration':     1.0,
        'field_declaration':           1.0,
        'static_initializer':          1.0,
        'instance_initializer':        1.0,
        # Modifiers
        'modifiers':                   1.0,
        'public':                      0.7,
        'private':                     0.7,
        'protected':                   0.7,
        'static':                      0.7,
        'final':                       0.8,
        'abstract':                    0.9,
        'synchronized':                1.0,
        'volatile':                    0.9,
        'transient':                   1.0,
        # Types
        'type_identifier':             0.8,
        'void_type':                   1.0,
        'generic_type':                0.9,
        'wildcard':                    1.0,  # <? extends T>
        'type_parameters':             0.9,
        'type_arguments':              0.8,
        'array_type':                  0.8,
        'integral_type':               1.0,  # int/long/byte/short/char
        'floating_point_type':         1.0,  # float/double
        'boolean_type':                1.0,
        # Statements
        'local_variable_declaration':  1.0,
        'enhanced_for_statement':      1.0,  # for (Type x : collection)
        'try_with_resources_statement':1.0,
        'resource':                    0.9,
        'switch_expression':           0.9,
        'switch_block':                0.8,
        'throw_statement':             0.9,
        'assert_statement':            0.8,
        'labeled_statement':           0.8,
        # Expressions
        'method_invocation':           1.0,
        'object_creation_expression':  1.0,  # new Foo()
        'array_creation_expression':   1.0,
        'cast_expression':             0.9,
        'instanceof_expression':       0.8,
        'lambda_expression':           0.9,
        'method_reference':            1.0,  # Foo::bar
        'ternary_expression':          0.6,
        # Literals
        'decimal_integer_literal':     1.0,  # Java-specific naming
        'hex_integer_literal':         0.9,
        'octal_integer_literal':       0.9,
        'binary_integer_literal':      1.0,
        'decimal_floating_point_literal': 1.0,
        'character_literal':           0.9,
        'null_literal':                0.9,
        # Annotations
        'annotation':                  1.0,  # @Override
        'marker_annotation':           1.0,
        'element_value_array_initializer': 1.0,
        # Misc
        'dimensions':                  0.9,
        'requires_directive':          1.0,  # Java modules
        'exports_directive':           1.0,
        'opens_directive':             1.0,
    },

    'c': {
        # Root
        'translation_unit':            1.0,  # C/C++ root
        # Preprocessor
        'preproc_include':             1.0,
        'preproc_def':                 1.0,
        'preproc_ifdef':               1.0,
        'preproc_ifndef':              1.0,
        'preproc_if':                  0.9,
        'preproc_elif':                0.9,
        'preproc_else':                0.8,
        'preproc_undef':               1.0,
        'preproc_pragma':              1.0,
        'preproc_function_def':        1.0,  # #define macro(x)
        'preproc_params':              1.0,
        'system_lib_string':           1.0,  # <stdio.h>
        # Declarations
        'declaration':                 0.7,
        'function_definition':         0.7,
        'type_definition':             1.0,  # typedef
        'struct_specifier':            1.0,
        'union_specifier':             1.0,
        'enum_specifier':              1.0,
        'enumerator_list':             0.9,
        'enumerator':                  0.9,
        # Types / qualifiers
        'primitive_type':              0.9,  # int/char/void/etc
        'type_qualifier':              0.9,  # const/volatile/restrict
        'storage_class_specifier':     1.0,  # static/extern/register/auto
        'sized_type_specifier':        1.0,  # unsigned long int
        # Pointers
        'pointer_declarator':          1.0,
        'pointer_expression':          0.9,
        'abstract_pointer_declarator': 1.0,
        'pointer_type':                0.9,
        # Parameters
        'parameter_declaration':       0.8,
        'parameter_list':              0.7,
        'variadic_parameter':          1.0,  # ...
        # Statements
        'goto_statement':              1.0,  # goto (C-era)
        'labeled_statement':           0.8,
        'compound_statement':          0.7,
        'expression_statement':        0.5,
        # Expressions
        'cast_expression':             0.8,
        'sizeof_expression':           1.0,
        'alignof_expression':          1.0,
        'subscript_expression':        0.7,
        'field_expression':            0.8,
        'comma_expression':            0.7,
        'assignment_expression':       0.5,
        'conditional_expression':      0.6,  # ternary
        # Literals
        'number_literal':              0.6,
        'char_literal':                0.9,
        'string_literal':              0.5,
        'concatenated_string':         0.7,
        'null':                        0.6,
        # Init
        'initializer_list':            0.9,  # {1, 2, 3}
        'designated_initializer':      1.0,  # .field = val  (C99)
        # Misc
        'linkage_specification':       0.7,  # extern "C" {}
        '_Static_assert':              1.0,
        # C-specific primitive types (node types)
        'primitive_type':              1.0,
        'type_qualifier':              0.9,
        'storage_class_specifier':     1.0,
    },

    'cpp': {
        # Root
        'translation_unit':            1.0,
        # C++ exclusive
        'namespace_definition':        1.0,
        'namespace_alias_definition':  1.0,
        'using_declaration':           1.0,
        'using_directive':             1.0,  # using namespace std;
        'template_declaration':        1.0,
        'template_instantiation':      1.0,
        'explicit_template_instantiation': 1.0,
        'template_parameter_list':     1.0,
        'type_parameter_declaration':  1.0,  # typename T
        'variadic_type_parameter_declaration': 1.0,
        # Classes
        'class_specifier':             1.0,  # class Foo {};
        'base_class_clause':           1.0,  # : public Bar
        'visibility_label':            1.0,  # public:, private:
        'access_specifier':            1.0,
        'virtual_specifier':           1.0,
        'override':                    1.0,
        'final':                       1.0,
        # Functions / operators
        'function_definition':         0.6,
        'operator_cast':               1.0,
        'operator_cast_definition':    1.0,
        'operator_name':               1.0,  # operator+
        'destructor_name':             1.0,  # ~Foo
        'qualified_identifier':        1.0,  # Foo::bar
        'scope_resolution':            1.0,  # ::
        # Lambda / closures
        'lambda_expression':           1.0,  # [cap](){}
        'lambda_capture_specifier':    1.0,
        'variadic_parameter_declaration': 1.0,
        # New / Delete
        'new_expression':              1.0,
        'delete_expression':           1.0,
        # Casts
        'static_cast':                 1.0,
        'dynamic_cast':                1.0,
        'reinterpret_cast':            1.0,
        'const_cast':                  1.0,
        # STL / modern C++
        'decltype':                    1.0,
        'auto':                        0.9,
        'nullptr':                     1.0,
        'constexpr':                   1.0,
        'consteval':                   1.0,
        'constinit':                   1.0,
        'co_await_expression':         1.0,
        'co_yield_expression':         1.0,
        'co_return_statement':         1.0,
        'concept_definition':          1.0,  # C++20 concepts
        'requires_clause':             1.0,
        'fold_expression':             1.0,  # parameter pack fold
        'parameter_pack_expansion':    1.0,
        # Exception
        'throw_statement':             0.9,
        'try_statement':               0.6,
        'catch_clause':                1.0,
        'noexcept':                    1.0,
        # Struct / enum
        'struct_specifier':            0.6,
        'enum_specifier':              0.6,
        'scoped_type_identifier':      1.0,
        # Preprocessor (shared with C but still useful)
        'preproc_include':             0.5,
        'preproc_def':                 0.5,
    },
}



KEYWORD_FINGERPRINTS = {
    'javascript': [
        # High-confidence exclusives
        ('=>',                    1.0),  # arrow function
        ('`',                     0.9),  # template literal
        ('?.', 0.95),                   # optional chaining
        ('??',                    0.9),  # nullish coalescing
        ('console.log',           1.0),
        ('console.error',         1.0),
        ('console.warn',          1.0),
        ('typeof ',               0.9),
        ('instanceof ',           0.8),
        ('undefined',             0.9),
        ('NaN',                   0.9),
        ('Promise.',              1.0),
        ('async function',        1.0),
        ('await ',                0.9),
        ('function*',             1.0),
        ('yield ',                0.8),
        ('.then(',                1.0),
        ('.catch(',               0.9),
        ('.finally(',             0.9),
        ('require(',              1.0),
        ('module.exports',        1.0),
        ('export default',        1.0),
        ('export const',          1.0),
        ('import {',              0.9),
        ('from \'',               0.8),
        ('from "',                0.8),
        ('const ',                0.7),
        ('let ',                  0.7),
        ('var ',                  0.7),
        ('===',                   0.8),  # strict equality
        ('!==',                   0.8),
        ('document.',             1.0),
        ('window.',               1.0),
        ('addEventListener(',     1.0),
        ('.querySelector(',       1.0),
        ('JSON.parse(',           1.0),
        ('JSON.stringify(',       1.0),
        ('Array.from(',           1.0),
        ('Object.keys(',         1.0),
        ('Object.values(',       1.0),
        ('Object.entries(',      1.0),
        ('Map(',                  0.7),
        ('Set(',                  0.7),
        ('Symbol(',               1.0),
        ('.map(',                 0.6),
        ('.filter(',              0.6),
        ('.reduce(',              0.8),
        ('.forEach(',             0.8),
        ('...', 0.6),                   # spread
        ('jsx',                   0.8),
        ('React.',                1.0),
        ('useState(',             1.0),
        ('useEffect(',            1.0),
        ('let ',                  1.0),
        ('const ',                1.0),
        ('===',                   1.0),
        ('!==',                   1.0),
        ('=>',                    1.0),
    ],

    'python': [
        ('def ',                  1.0),
        ('elif ',                 1.0),
        ('lambda ',               1.0),
        ('yield ',                0.9),
        ('yield from ',           1.0),
        ('if __name__ ==',        1.0),
        ('__init__',              1.0),
        ('self.',                 1.0),
        ('cls.',                  1.0),
        ('super()',               0.9),
        ('@property',             1.0),
        ('@staticmethod',         1.0),
        ('@classmethod',          1.0),
        ('from import',           0.8),
        ('import ',               0.5),
        ('print(',                0.8),
        ('len(',                  0.7),
        ('range(',                0.9),
        ('enumerate(',            1.0),
        ('zip(',                  0.7),
        ('isinstance(',           1.0),
        ('issubclass(',           1.0),
        ('hasattr(',              1.0),
        ('getattr(',              1.0),
        ('setattr(',              1.0),
        ('type(',                 0.6),
        (':=',                    1.0),  # walrus operator
        ('f"',                    1.0),  # f-string
        ("f'",                    1.0),
        ('None',                  0.9),
        ('True',                  0.8),
        ('False',                 0.8),
        ('not ',                  0.9),
        (' and ',                 0.8),
        (' or ',                  0.8),
        (' in ',                  0.7),
        (' is ',                  0.8),
        (' is not ',              1.0),
        (' not in ',              1.0),
        ('pass',                  1.0),
        ('raise ',                0.9),
        ('except ',               0.9),
        ('finally:',              0.8),
        ('with ',                 0.7),
        ('as ',                   0.6),
        ('[x for',                1.0),  # list comp hint
        ('{k:',                   0.8),  # dict comp hint
        ('**kwargs',              1.0),
        ('*args',                 1.0),
        ('-> ',                   0.9),  # return type hint
        (': int',                 0.8),
        (': str',                 0.8),
        (': bool',                0.8),
        (': list',                0.8),
        (': dict',                0.8),
        ('dataclass',             1.0),
        ('__str__',               1.0),
        ('__repr__',              1.0),
        ('__len__',               1.0),
        ('__iter__',              1.0),
        ('async def ',            1.0),
        ('await ',                0.8),
        ('match ',                0.8),  # Python 3.10
        ('case ',                 0.7),
    ],

    'java': [
        ('public class ',         1.0),
        ('private class ',        1.0),
        ('public interface ',     1.0),
        ('public enum ',          1.0),
        ('public record ',        1.0),
        ('package ',              1.0),
        ('import java.',          1.0),
        ('import org.',           0.9),
        ('import com.',           0.9),
        ('System.out.println',    1.0),
        ('System.err.println',    1.0),
        ('System.in',             1.0),
        ('public static void main', 1.0),
        ('throws ',               1.0),
        ('extends ',              0.9),
        ('implements ',           1.0),
        ('instanceof ',           0.8),
        ('new ',                  0.7),
        ('final ',                0.8),
        ('static ',               0.7),
        ('abstract ',             1.0),
        ('synchronized ',         1.0),
        ('volatile ',             0.9),
        ('transient ',            1.0),
        ('@Override',             1.0),
        ('@Deprecated',           1.0),
        ('@SuppressWarnings',     1.0),
        ('@FunctionalInterface',  1.0),
        ('@Annotation',           0.9),
        ('ArrayList<',           1.0),
        ('HashMap<',             1.0),
        ('List<',                0.9),
        ('Map<',                 0.9),
        ('Set<',                 0.8),
        ('Optional<',           1.0),
        ('Stream<',             1.0),
        ('.stream()',            1.0),
        ('.collect(',           1.0),
        ('Collectors.',         1.0),
        ('Iterator<',           1.0),
        ('try {',               0.6),
        ('catch (',             0.9),
        ('finally {',           0.8),
        ('throw new ',          1.0),
        ('String ',             0.8),
        ('int ',                0.7),
        ('void ',               0.8),
        ('boolean ',            0.9),
        ('this.',               0.8),
        ('super(',              0.9),
        ('::',                  0.9),   # method reference
        ('->',                  0.7),   # lambda
        ('var ',                0.7),   # Java 10+
        ('record ',             1.0),
        ('sealed ',             1.0),
        ('permits ',            1.0),
        ('yield ',              0.8),   # switch expression
        ('instanceof pattern',  1.0),
    ],

    'c': [
        ('#include',              1.0),
        ('#define',               1.0),
        ('#ifdef',                1.0),
        ('#ifndef',               1.0),
        ('#pragma',               1.0),
        ('#undef',                1.0),
        ('#error',                1.0),
        ('#warning',              1.0),
        ('<stdio.h>',             1.0),
        ('<stdlib.h>',            1.0),
        ('<string.h>',            1.0),
        ('<math.h>',              1.0),
        ('<stdint.h>',            1.0),
        ('<stdbool.h>',           1.0),
        ('printf(',               1.0),
        ('scanf(',                1.0),
        ('fprintf(',              1.0),
        ('sprintf(',              1.0),
        ('sscanf(',               1.0),
        ('malloc(',               1.0),
        ('calloc(',               1.0),
        ('realloc(',              1.0),
        ('free(',                 1.0),
        ('sizeof(',               1.0),
        ('typedef ',              1.0),
        ('struct ',               0.9),
        ('union ',                1.0),
        ('enum ',                 0.8),
        ('void *',               1.0),
        ('int *',                0.9),
        ('char *',               0.9),
        ('NULL',                  0.9),
        ('goto ',                 1.0),
        ('extern ',               0.9),
        ('register ',             1.0),
        ('volatile ',             0.8),
        ('static ',               0.6),
        ('const ',                0.5),
        ('unsigned ',             0.9),
        ('signed ',               0.9),
        ('->',                    0.8),  # struct pointer member
        ('fopen(',                1.0),
        ('fclose(',               1.0),
        ('fread(',                1.0),
        ('fwrite(',               1.0),
        ('memcpy(',               1.0),
        ('memset(',               1.0),
        ('strlen(',               1.0),
        ('strcpy(',               1.0),
        ('strcmp(',               1.0),
        ('atoi(',                 1.0),
        ('exit(',                 0.8),
        ('int ',                  0.8),
        ('void ',                 0.8),
        ('char ',                 0.8),
        ('double ',               0.8),
        ('NULL',                  1.0),
        ('->',                    1.0),
    ],

    'cpp': [
        ('#include',              0.6),   # shared with C
        ('using namespace ',      1.0),
        ('using namespace std',   1.0),
        ('std::',                 1.0),
        ('cout <<',              1.0),
        ('cin >>',               1.0),
        ('cerr <<',              1.0),
        ('endl',                  1.0),
        ('vector<',              1.0),
        ('string ',               0.7),
        ('std::string',           1.0),
        ('std::vector',           1.0),
        ('std::map',              1.0),
        ('std::unordered_map',    1.0),
        ('std::set',              1.0),
        ('std::pair',             1.0),
        ('std::tuple',            1.0),
        ('std::optional',         1.0),
        ('std::variant',          1.0),
        ('std::shared_ptr',       1.0),
        ('std::unique_ptr',       1.0),
        ('std::make_shared',      1.0),
        ('std::make_unique',      1.0),
        ('nullptr',               1.0),
        ('auto ',                 0.9),
        ('decltype(',             1.0),
        ('constexpr ',            1.0),
        ('consteval ',            1.0),
        ('constinit ',            1.0),
        ('template<',            1.0),
        ('template <',           1.0),
        ('typename ',             1.0),
        ('class ',                0.6),   # shared with Java-ish
        ('virtual ',              1.0),
        ('override',              1.0),
        ('final ',                0.8),
        ('explicit ',             1.0),
        ('operator ',             1.0),
        ('~',                     0.8),   # destructor hint
        ('::',                    0.9),
        ('new ',                  0.7),
        ('delete ',               1.0),
        ('delete[] ',             1.0),
        ('::', 0.9),
        ('throw ',                0.8),
        ('noexcept',              1.0),
        ('try {',                0.6),
        ('catch (',              0.8),
        ('static_cast<',        1.0),
        ('dynamic_cast<',       1.0),
        ('reinterpret_cast<',   1.0),
        ('const_cast<',         1.0),
        ('[&]',                  1.0),  # lambda capture
        ('[=]',                  1.0),
        ('co_await ',            1.0),
        ('co_yield ',            1.0),
        ('co_return ',           1.0),
        ('concept ',             1.0),
        ('requires ',            1.0),
    ],
}


NEGATIVE_EVIDENCE = {
    'python':     ['};', '->', '::', 'public class', 'void ', '#include', 'cout', 'endl', '===', '!--', 'function ', 'console.log', 'let ', 'const ', '=>', 'System.out'],
    'javascript': ['#include', 'System.out', 'public class', 'using namespace', 'cout <<', 'scanf(', 'def ', 'elif ', 'NULL', 'public void', 'std::', 'printf(', 'String[] args'],
    'java':       ['#include', 'cout', 'using namespace', 'printf(', 'malloc(', 'free(', 'def ', 'elif ', 'function ', 'console.log', '===', '!==', 'let ', 'const ', '=>', 'document.', 'window.', 'pass'],
    'c':          ['using namespace', 'cout <<', 'System.out', 'public class', 'def ', 'elif ', '=>', '`', 'let ', 'const ', '===', '!==', 'console.log', 'function ', 'public void', 'String[] args'],
    'cpp':        ['System.out', 'public class', 'def ', 'elif ', 'console.log', 'require(', 'function ', '===', '!==', 'let ', '=>', 'public void', 'String[] args', 'stdio.h', 'printf('],
}


def collect_node_types(tree):
    node_types = set()
    if not tree or not tree.root_node:
        return node_types

    def walk(node):
        node_types.add(node.type)
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return node_types


def compute_fingerprint_score(node_types, language, tree=None):
    fp = LANGUAGE_FINGERPRINTS.get(language, {})
    if not fp:
        return 0.0

    total_weight   = sum(fp.values())
    matched_weight = sum(w for node, w in fp.items() if node in node_types)
    score = matched_weight / total_weight if total_weight else 0.0


    if tree and fp:
        expected_root = next(iter(fp))  # first key = root node
        if tree.root_node.type == expected_root:
            score = min(1.0, score + 0.15)

    return min(1.0, score)


def compute_keyword_score(code_text, language):
    kw_list   = KEYWORD_FINGERPRINTS.get(language, [])
    neg_list  = NEGATIVE_EVIDENCE.get(language, [])

    if not kw_list:
        return 0.0, 0.0

    total_possible = sum(w for _, w in kw_list)
    hit_weight     = sum(w for pattern, w in kw_list if pattern in code_text)

    raw_score = min(1.0, hit_weight / (total_possible * 0.25))

    neg_hits    = sum(1 for pattern in neg_list if pattern in code_text)
    neg_penalty = min(0.40, neg_hits * 0.06)

    return raw_score, neg_penalty


def detect_language_ast(code):
    best_lang  = None
    best_score = -1.0
    code_text  = code.strip()

    for lang in ['javascript', 'python', 'java', 'c', 'cpp']:
        kw_score, neg_penalty = compute_keyword_score(code_text, lang)

        tree, conf, err = parse_code(code, lang)

        if tree is not None and err is None:
            node_types = collect_node_types(tree)
            fp_score   = compute_fingerprint_score(node_types, lang, tree)
            combined = 0.35 * kw_score + 0.10 * conf + 0.55 * fp_score
        else:

            combined = 0.55 * kw_score


        combined = max(0.0, combined - neg_penalty)

        if combined > best_score:
            best_score = combined
            best_lang  = lang

    return best_lang, best_score


def validate_language(code, selected_language):
    best_lang, best_score = detect_language_ast(code)

    if not best_lang:
        return {
            "issue": None,
            "selected": selected_language,
            "detected": "unknown",
            "confidence": 0.0,
            "score": 0.0
        }


    code_text             = code.strip()
    kw_score, neg_penalty = compute_keyword_score(code_text, selected_language)
    tree, sel_conf, err   = parse_code(code, selected_language)

    if tree is not None and err is None:
        node_types = collect_node_types(tree)
        fp_score   = compute_fingerprint_score(node_types, selected_language, tree)
        sel_score  = 0.35 * kw_score + 0.10 * sel_conf + 0.55 * fp_score
    else:
        sel_score  = 0.55 * kw_score

    sel_score = max(0.0, sel_score - neg_penalty)

    metadata = {
        "selected": selected_language,
        "detected": best_lang,
        "confidence": best_score,
        "score": sel_score,
        "issue": None
    }


    if selected_language == best_lang or sel_score > 0.50:
        return metadata


    if selected_language in ('c', 'cpp') and best_lang in ('c', 'cpp') and abs(best_score - sel_score) < 0.15:
        return metadata


    if best_score > sel_score + 0.15 or sel_score < 0.20:
        issue = {
            "severity": "critical",
            "title": "Language Mismatch Detected",
            "description": (
                f"Selected language is {selected_language.capitalize()}, "
                f"but deep syntactic analysis identified the code as {best_lang.capitalize()} "
                f"({int(best_score*100)}% confidence)."
            ),
            "step": {
                "what": "Correct the selected language",
                "why": "Optimising code with the wrong language engine produces invalid results.",
                "how": f"The engine has internally switched to {best_lang.capitalize()} mode for safety."
            },
        }
        metadata["issue"] = issue
        metadata["corrected_language"] = best_lang
        return metadata

    return metadata
