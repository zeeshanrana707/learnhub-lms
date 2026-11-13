"""
Safe Subprocess Code Evaluator & Unit Test Runner
Executes student solutions in an isolated Python process with strict resource limits,
full stdout/stderr capturing, syntax/runtime error formatting, and custom input testing.
"""

import sys
import os
import json
import subprocess
from typing import Dict, Any, Optional
from app.services.programming_challenges import get_programming_quiz

WORKER_SCRIPT = os.path.join(os.path.dirname(__file__), 'sandbox_runner.py')

def evaluate_solution(lesson, difficulty: str, user_code: str, custom_input: Optional[str] = None) -> Dict[str, Any]:
    """
    Evaluate user code against lesson test cases and optional custom input.
    difficulty: 'basic', 'intermediate', or 'advance'
    """
    quiz_data = get_programming_quiz(lesson)
    diff_key = (difficulty or 'basic').lower().strip()
    if diff_key not in quiz_data['challenges']:
        diff_key = 'basic'

    challenge = quiz_data['challenges'][diff_key]
    func_name = challenge.get('function_name', '')
    test_cases = challenge.get('test_cases', [])
    approach = challenge.get('approach', 'function')
    target_var = challenge.get('target_variable', 'result')
    class_name = challenge.get('class_name', '')

    payload = {
        'code': user_code or '',
        'function_name': func_name,
        'approach': approach,
        'target_variable': target_var,
        'class_name': class_name,
        'test_cases': test_cases,
        'custom_input': custom_input
    }

    try:
        proc = subprocess.run(
            [sys.executable, WORKER_SCRIPT],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=3.5
        )
        if proc.stdout:
            try:
                res_data = json.loads(proc.stdout)
            except Exception:
                res_data = {
                    'passed': False,
                    'message': 'Failed to parse evaluation output.',
                    'error': proc.stdout + '\n' + proc.stderr,
                    'stdout': '',
                    'test_results': [],
                    'custom_result': None,
                    'passed_count': 0,
                    'total_count': len(test_cases)
                }
        else:
            res_data = {
                'passed': False,
                'message': 'Runtime crash in code runner.',
                'error': proc.stderr or 'Process exited with non-zero status.',
                'stdout': '',
                'test_results': [],
                'custom_result': None,
                'passed_count': 0,
                'total_count': len(test_cases)
            }
    except subprocess.TimeoutExpired:
        res_data = {
            'passed': False,
            'message': 'Time Limit Exceeded (3.5s): Process timed out. Check for infinite loops or deep recursion.',
            'error': 'TimeoutError: Execution exceeded the 3.5-second time limit.\nCommon causes:\n  1. Infinite while loops (missing loop condition update)\n  2. Unbounded recursion (missing base case)\n  3. Extremely large iterations',
            'stdout': '',
            'test_results': [],
            'custom_result': {
                'input': custom_input,
                'output': None,
                'stdout': '',
                'error': 'TimeoutError: Execution exceeded 3.5 seconds.',
                'success': False
            } if custom_input is not None else None,
            'passed_count': 0,
            'total_count': len(test_cases)
        }
    except Exception as e:
        res_data = {
            'passed': False,
            'message': f'Evaluation error: {type(e).__name__}: {str(e)}',
            'error': str(e),
            'stdout': '',
            'test_results': [],
            'custom_result': None,
            'passed_count': 0,
            'total_count': len(test_cases)
        }

    # Attach challenge metadata
    res_data['difficulty'] = diff_key.capitalize()
    res_data['challenge_title'] = challenge.get('title')
    res_data['hint'] = challenge.get('hint', '')
    res_data['explanation'] = challenge.get('explanation', '')
    if res_data.get('passed'):
        res_data['solution_code'] = challenge.get('solution_code', '')

    return res_data
