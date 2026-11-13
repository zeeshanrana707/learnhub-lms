"""
Sandbox Runner - Standalone Worker Process
Executes student code securely with stdout/stderr capture, syntax checking,
runtime exception traceback cleaning, custom input testing, and multi-paradigm
support: Functions, Direct Scripts/Variables, and OOP Classes.
"""

import sys
import json
import ast
import io
import copy
import traceback
from contextlib import redirect_stdout, redirect_stderr

# Safe built-in functions for student programming challenges
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bin': bin,
    'bool': bool,
    'bytearray': bytearray,
    'bytes': bytes,
    'chr': chr,
    'complex': complex,
    'dict': dict,
    'divmod': divmod,
    'enumerate': enumerate,
    'filter': filter,
    'float': float,
    'format': format,
    'frozenset': frozenset,
    'hash': hash,
    'hex': hex,
    'int': int,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'iter': iter,
    'len': len,
    'list': list,
    'map': map,
    'max': max,
    'min': min,
    'next': next,
    'oct': oct,
    'ord': ord,
    'pow': pow,
    'print': print,
    'range': range,
    'repr': repr,
    'reversed': reversed,
    'round': round,
    'set': set,
    'slice': slice,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'type': type,
    'zip': zip,
    'True': True,
    'False': False,
    'None': None,
    # Object-Oriented Programming (OOP) Built-ins
    '__build_class__': __build_class__,
    'property': property,
    'classmethod': classmethod,
    'staticmethod': staticmethod,
    'super': super,
    'getattr': getattr,
    'setattr': setattr,
    'hasattr': hasattr
}

# Pre-imported helper libraries
import math
import random
import collections
import itertools
import string
import datetime
import re
import heapq
import bisect

SAFE_MODULES = {
    'math': math,
    'random': random,
    'collections': collections,
    'itertools': itertools,
    'string': string,
    'datetime': datetime,
    're': re,
    'heapq': heapq,
    'bisect': bisect
}

def format_clean_traceback(exc, user_code: str) -> str:
    """Format traceback focusing only on user's student code lines."""
    lines = []
    tb = exc.__traceback__
    extracted = traceback.extract_tb(tb)
    for frame in extracted:
        if frame.filename == '<student_code>':
            lines.append(f'  Line {frame.lineno}, in {frame.name}')
            if frame.line:
                lines.append(f'    {frame.line}')
    exc_header = f"{type(exc).__name__}: {str(exc)}"
    if lines:
        return "Traceback (most recent call last):\n" + "\n".join(lines) + "\n" + exc_header
    return exc_header

def parse_custom_input(raw_input: str):
    """Safely parse user-supplied custom input string into Python objects."""
    s = raw_input.strip()
    if not s:
        return ()

    # Try literal eval directly
    try:
        val = ast.literal_eval(s)
        return val
    except Exception:
        pass

    # Try wrapping in tuple for multiple comma-separated arguments: e.g. 5, "test"
    try:
        val = ast.literal_eval(f"({s})")
        return val
    except Exception:
        pass

    # Try JSON
    try:
        return json.loads(s)
    except Exception:
        pass

    # Fallback as raw string
    return s

def compare_values(actual, expected):
    """Robust polymorphic equality comparison."""
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return abs(float(actual) - float(expected)) <= 0.02
    elif isinstance(expected, list) and isinstance(actual, (list, tuple)):
        return list(actual) == list(expected)
    elif isinstance(expected, dict) and isinstance(actual, dict):
        return actual == expected
    else:
        return actual == expected

def run():
    try:
        raw_payload = sys.stdin.read()
        payload = json.loads(raw_payload) if raw_payload else {}
    except Exception as e:
        print(json.dumps({
            'passed': False,
            'message': f'Invalid worker payload: {str(e)}',
            'error': str(e),
            'stdout': '',
            'test_results': [],
            'custom_result': None
        }))
        return

    user_code = payload.get('code', '')
    approach = (payload.get('approach') or 'function').lower().strip()
    func_name = payload.get('function_name', '')
    target_var = payload.get('target_variable', 'result')
    class_name = payload.get('class_name', '')
    test_cases = payload.get('test_cases', [])
    custom_input = payload.get('custom_input', None)

    response = {
        'passed': False,
        'message': '',
        'error': None,
        'stdout': '',
        'test_results': [],
        'custom_result': None,
        'passed_count': 0,
        'total_count': len(test_cases)
    }

    if not user_code or not user_code.strip():
        response['message'] = 'No code provided. Please write your Python solution in the editor.'
        response['error'] = 'Empty Code Submission: Editor contains no code to execute.'
        print(json.dumps(response))
        return

    # 1. AST Parsing & Syntax Checking
    try:
        parsed = ast.parse(user_code)
    except SyntaxError as se:
        lines = user_code.splitlines()
        snippet = ""
        if se.lineno and 1 <= se.lineno <= len(lines):
            line_text = lines[se.lineno - 1]
            col = se.offset or 1
            indent = " " * (len(f"Line {se.lineno}: ") + max(col - 1, 0))
            snippet = f"\nLine {se.lineno}: {line_text}\n{indent}^"
        err_msg = f"SyntaxError on line {se.lineno}: {se.msg}{snippet}"
        response['error'] = err_msg
        response['message'] = f"SyntaxError on line {se.lineno}: {se.msg}"
        print(json.dumps(response))
        return

    # 2. Block prohibited operations (exec, eval, open, compile, __import__)
    disallowed = {'exec', 'eval', 'open', '__import__', 'compile'}
    for node in ast.walk(parsed):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in disallowed:
                err = f"Security Restriction: Calling '{node.func.id}()' is prohibited in sandbox."
                response['error'] = err
                response['message'] = err
                print(json.dumps(response))
                return
            elif isinstance(node.func, ast.Attribute) and node.func.attr in disallowed:
                err = f"Security Restriction: Calling '{node.func.attr}()' is prohibited in sandbox."
                response['error'] = err
                response['message'] = err
                print(json.dumps(response))
                return

    # 3. Setup Sandbox Namespace
    sandbox = {
        '__builtins__': SAFE_BUILTINS,
        '__name__': '__main__',
        '__doc__': None
    }
    sandbox.update(SAFE_MODULES)

    top_out = io.StringIO()
    top_err = io.StringIO()

    # 4. Execute Top-Level Code
    try:
        with redirect_stdout(top_out), redirect_stderr(top_err):
            compiled = compile(user_code, '<student_code>', 'exec')
            exec(compiled, sandbox)
    except Exception as e:
        tb_str = format_clean_traceback(e, user_code)
        response['error'] = tb_str
        response['message'] = f"Runtime Error: {type(e).__name__}: {str(e)}"
        response['stdout'] = top_out.getvalue()
        print(json.dumps(response))
        return

    top_stdout = top_out.getvalue()
    response['stdout'] = top_stdout

    # 5. Smart Multi-Paradigm Identification & Setup
    user_func = None
    user_class = None

    if approach == 'script' or approach == 'variable':
        # Script execution: verify target variable exists
        if target_var not in sandbox:
            # Fallback to 'result' or 'output' if student used a standard name
            if 'result' in sandbox:
                target_var = 'result'
            elif 'output' in sandbox:
                target_var = 'output'
            else:
                err = f"Target variable `{target_var}` not found in your script. Please assign the calculated value to `{target_var}`."
                response['error'] = err
                response['message'] = f"Missing Variable: `{target_var}` is not defined."
                print(json.dumps(response))
                return

    elif approach == 'class':
        # Class execution: locate user-defined class
        user_class = sandbox.get(class_name)
        if not isinstance(user_class, type):
            # Fallback: look for any student-defined class
            excluded_names = set(SAFE_BUILTINS.keys()).union(set(SAFE_MODULES.keys()))
            custom_classes = [v for k, v in sandbox.items() if isinstance(v, type) and k not in excluded_names and not k.startswith('_')]
            if custom_classes:
                user_class = custom_classes[-1]
            else:
                err = f"Class `{class_name}` not found in your code. Please declare:\nclass {class_name}: ..."
                response['error'] = err
                response['message'] = f"Missing Class: `{class_name}` is not defined."
                print(json.dumps(response))
                return

    else:
        # Standard function execution
        user_func = sandbox.get(func_name)
        if not callable(user_func):
            # Check for any callable defined by student
            excluded = set(SAFE_BUILTINS.keys()).union(set(SAFE_MODULES.keys())).union({'__builtins__'})
            callables = [v for k, v in sandbox.items() if callable(v) and not k.startswith('_') and k not in excluded and not isinstance(v, type)]
            if callables:
                user_func = callables[-1]
            elif target_var in sandbox:
                # Student wrote direct script instead of function! Switch smoothly to script approach
                approach = 'script'
            else:
                err = f"Function `{func_name}` not found in your code. Please declare:\ndef {func_name}(...):"
                response['error'] = err
                response['message'] = f"Missing Function: `{func_name}` is not defined."
                print(json.dumps(response))
                return

    # 6. Optional Custom Input Execution
    if custom_input is not None and str(custom_input).strip() != "":
        c_in_raw = str(custom_input).strip()
        c_out = io.StringIO()
        c_err = io.StringIO()
        try:
            parsed_args = parse_custom_input(c_in_raw)
            with redirect_stdout(c_out), redirect_stderr(c_err):
                if approach == 'class' and user_class:
                    if isinstance(parsed_args, tuple):
                        inst = user_class(*parsed_args)
                    else:
                        inst = user_class(parsed_args)
                    res = repr(inst)
                elif approach == 'script':
                    res = sandbox.get(target_var)
                elif user_func:
                    if isinstance(parsed_args, tuple):
                        res = user_func(*parsed_args)
                    else:
                        res = user_func(parsed_args)
                else:
                    res = None

            response['custom_result'] = {
                'input': c_in_raw,
                'output': repr(res),
                'stdout': c_out.getvalue(),
                'error': None,
                'success': True
            }
        except Exception as e:
            tb_str = format_clean_traceback(e, user_code)
            response['custom_result'] = {
                'input': c_in_raw,
                'output': None,
                'stdout': c_out.getvalue(),
                'error': tb_str,
                'success': False
            }

    # 7. Evaluate Predefined Test Cases
    results = []
    all_passed = True

    for i, tc in enumerate(test_cases, 1):
        desc = tc.get('desc', f'Test Case {i}')
        expected = tc.get('expected')
        t_out = io.StringIO()
        t_err = io.StringIO()

        try:
            with redirect_stdout(t_out), redirect_stderr(t_err):
                if approach == 'script' or approach == 'variable':
                    # Test script execution
                    input_vars = tc.get('input_vars')
                    if input_vars:
                        # Re-run script with injected input variables, stripping any initial assignments to them
                        class VarStripper(ast.NodeTransformer):
                            def visit_Assign(self, node):
                                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
                                if any(t in input_vars for t in targets):
                                    return None
                                return node
                        try:
                            modified_ast = VarStripper().visit(copy.deepcopy(parsed))
                            ast.fix_missing_locations(modified_ast)
                            compiled_case = compile(modified_ast, '<student_code>', 'exec')
                        except Exception:
                            compiled_case = compiled

                        case_sandbox = {
                            '__builtins__': SAFE_BUILTINS,
                            '__name__': '__main__',
                            '__doc__': None
                        }
                        case_sandbox.update(SAFE_MODULES)
                        case_sandbox.update(input_vars)
                        exec(compiled_case, case_sandbox)
                        actual = case_sandbox.get(tc.get('target_var', target_var))
                        input_repr = repr(input_vars)
                    else:
                        actual = sandbox.get(tc.get('target_var', target_var))
                        input_repr = f"{target_var} from script"

                elif approach == 'class' and user_class:
                    init_args = tc.get('init_args', [])
                    inst = user_class(*init_args)
                    if 'operations' in tc:
                        # Multi-operation state sequence
                        op_results = []
                        ops_passed = True
                        for op in tc['operations']:
                            m_name = op['method']
                            m_args = op.get('args', [])
                            exp_op = op.get('expected')
                            method = getattr(inst, m_name, None)
                            if not callable(method):
                                raise AttributeError(f"Method `{m_name}` not found on `{user_class.__name__}`")
                            act_op = method(*m_args)
                            if not compare_values(act_op, exp_op):
                                ops_passed = False
                            op_results.append(f"{m_name}({', '.join(repr(a) for a in m_args)}) -> {act_op}")
                        actual = "; ".join(op_results)
                        passed_test = ops_passed
                        input_repr = f"Init: {repr(init_args)}"
                    else:
                        m_name = tc.get('method', '')
                        m_args = tc.get('args', [])
                        method = getattr(inst, m_name)
                        actual = method(*m_args)
                        input_repr = f"{user_class.__name__}(*{init_args}).{m_name}(*{m_args})"

                else:
                    # Function execution
                    args = copy.deepcopy(tc.get('input', []))
                    actual = user_func(*args)
                    input_repr = repr(args) if len(args) > 1 else repr(args[0]) if args else '()'

            # Compare actual vs expected
            if approach == 'class' and 'operations' in tc:
                pass  # already calculated
            else:
                passed_test = compare_values(actual, expected)

            if not passed_test:
                all_passed = False

            results.append({
                'test_num': i,
                'desc': desc,
                'input': input_repr,
                'expected': repr(expected),
                'actual': repr(actual),
                'stdout': t_out.getvalue(),
                'passed': passed_test,
                'error': None
            })
        except Exception as e:
            all_passed = False
            tb_str = format_clean_traceback(e, user_code)
            results.append({
                'test_num': i,
                'desc': desc,
                'input': repr(tc.get('input', tc.get('input_vars', ''))),
                'expected': repr(expected),
                'actual': f"Error: {type(e).__name__}: {str(e)}",
                'stdout': t_out.getvalue(),
                'passed': False,
                'error': tb_str
            })

    passed_count = sum(1 for r in results if r['passed'])
    total_count = len(results)

    response['passed'] = all_passed
    response['test_results'] = results
    response['passed_count'] = passed_count
    response['total_count'] = total_count

    if all_passed and total_count > 0:
        response['message'] = f"🎉 Excellent! All {total_count} test cases passed successfully."
    elif total_count > 0:
        response['message'] = f"⚠️ {passed_count} of {total_count} test cases passed. Review details and console output below."
    else:
        response['message'] = "Code executed successfully."

    print(json.dumps(response))

if __name__ == '__main__':
    run()
