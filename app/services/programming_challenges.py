"""
Interactive Programming Quiz & Coding Challenge Service
Generates 3 tiers of programming challenges (Basic, Intermediate, Advance)
tailored specifically to every video lecture across all LMS courses and roadmaps.
"""

from typing import Dict, Any, List
import re
import json

def get_programming_quiz(lesson) -> Dict[str, Any]:
    """
    Retrieve or generate a 3-tier programming quiz for a given lesson.
    Returns:
    {
        'lesson_id': int,
        'lesson_title': str,
        'language': str,
        'challenges': {
            'basic': {...},
            'intermediate': {...},
            'advance': {...}
        }
    }
    """
    title = getattr(lesson, 'title', '')
    lesson_id = getattr(lesson, 'id', 1)
    module = getattr(lesson, 'module', None)
    course = module.course if module else None
    course_id = course.id if course else 1
    course_title = course.title if course else ''

    t_lower = title.lower()
    c_lower = course_title.lower()

    # Determine programming language
    if any(k in c_lower for k in ['javascript', 'frontend', 'react']):
        language = 'javascript'
    elif any(k in c_lower for k in ['linux', 'devops', 'docker', 'kubernetes']):
        language = 'bash'
    elif any(k in c_lower for k in ['sql', 'database', 'relational']):
        language = 'sql'
    elif 'cs50' in c_lower or 'c syntax' in t_lower:
        language = 'c'
    else:
        language = 'python'

    # ── 0. Check Database Custom Challenges (Top Priority: Instructor / Admin Customized) ──
    custom = getattr(lesson, 'custom_challenges', None)
    if custom:
        if isinstance(custom, str):
            import json
            try:
                custom = json.loads(custom)
            except Exception:
                custom = None
        if isinstance(custom, dict):
            chs = custom.get('challenges') if 'challenges' in custom else custom
            if chs and any(k in chs for k in ('basic', 'intermediate', 'advance')):
                return {
                    'lesson_id': lesson_id,
                    'lesson_title': title,
                    'course_title': course_title,
                    'language': custom.get('language', language),
                    'challenges': chs
                }

    # ── Course-specific lookup (highest priority) ──────────────────────────────
    try:
        from app.services.challenges import COURSE_CHALLENGES, EXTRA_CHALLENGES
        m_pos = module.position if module else 1
        l_pos = lesson.position if lesson else 1

        # Check dedicated extra challenge by (course_id, module_pos, lesson_pos)
        extra_key = (course_id, m_pos, l_pos)
        if extra_key in EXTRA_CHALLENGES:
            return {
                'lesson_id': lesson_id,
                'lesson_title': title,
                'course_title': course_title,
                'language': language,
                'challenges': EXTRA_CHALLENGES[extra_key]
            }

        # Check course challenge by (module_pos, lesson_pos)
        if course_id in COURSE_CHALLENGES:
            key = (m_pos, l_pos)
            course_map = COURSE_CHALLENGES[course_id]
            if key in course_map:
                return {
                    'lesson_id': lesson_id,
                    'lesson_title': title,
                    'course_title': course_title,
                    'language': language,
                    'challenges': course_map[key]
                }
    except Exception:
        pass  # fall through to keyword matching

    # ── Fallback: keyword-based challenge matching ─────────────────────────────
    challenges = _get_topic_challenges(t_lower, language, title, course_title, lesson_id)

    return {
        'lesson_id': lesson_id,
        'lesson_title': title,
        'course_title': course_title,
        'language': language,
        'challenges': challenges
    }


def _get_topic_challenges(t_lower: str, language: str, full_title: str, course_title: str, lesson_id: int) -> Dict[str, Any]:
    """Return handcrafted challenge sets for primary curriculum topics."""
    c_lower = (course_title or '').lower()

    # 0. INTRODUCTORY & FOUNDATION LESSONS (Multi-Paradigm: Script, Function, Class)
    if any(k in t_lower for k in ['intro', 'basic', 'foundation', 'getting started', 'overview']):
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'approach': 'script',
                'target_variable': 'total_cost',
                'title': 'Variables & Direct Expression Scripting',
                'prompt': 'Write direct Python script statements to compute an order invoice total. Given variables `subtotal = 85.50`, `tax_rate = 0.08` (8% tax), and `tip_rate = 0.15` (15% tip), calculate the final cost rounded to 2 decimal places and assign it to the variable `total_cost`. No function declaration is required!',
                'constraints': 'Do not wrap in a function. Calculate and assign directly to total_cost.',
                'starter_code': (
                    "# Calculate order invoice total\n"
                    "subtotal = 85.50\n"
                    "tax_rate = 0.08  # 8% tax\n"
                    "tip_rate = 0.15  # 15% tip\n\n"
                    "# Write your calculation below to set total_cost:\n"
                    "total_cost = None\n"
                ),
                'test_cases': [
                    {'desc': 'Default invoice subtotal ($85.50 at 8% tax and 15% tip)', 'expected': 105.17},
                    {'desc': 'Custom inputs ($50.0 at 10% tax and 20% tip)', 'input_vars': {'subtotal': 50.0, 'tax_rate': 0.10, 'tip_rate': 0.20}, 'expected': 65.0}
                ],
                'hint': 'Calculate subtotal * (1 + tax_rate + tip_rate) and wrap with round(..., 2).',
                'solution_code': (
                    "subtotal = 85.50\n"
                    "tax_rate = 0.08\n"
                    "tip_rate = 0.15\n\n"
                    "total_cost = round(subtotal * (1 + tax_rate + tip_rate), 2)\n"
                ),
                'explanation': 'Direct script execution teaches fundamental variable assignment, operator precedence, and arithmetic without unnecessary function boilerplate.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'approach': 'function',
                'title': 'Metric Converter & Unit Scaler',
                'function_name': 'convert_temperature',
                'prompt': 'Write a clean Python function `convert_temperature(celsius: float) -> float` converting Celsius to Fahrenheit using `(celsius * 9/5) + 32`, rounded to 1 decimal place.',
                'constraints': '-273.15 <= celsius <= 1000.0',
                'starter_code': (
                    "def convert_temperature(celsius: float) -> float:\n"
                    "    # Convert celsius to fahrenheit rounded to 1 decimal place\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {'input': [0.0], 'expected': 32.0, 'desc': 'Freezing point of water'},
                    {'input': [100.0], 'expected': 212.0, 'desc': 'Boiling point of water'},
                    {'input': [37.0], 'expected': 98.6, 'desc': 'Human body temperature'}
                ],
                'hint': 'Multiply celsius by 9/5 and add 32. Return round(result, 1).',
                'solution_code': (
                    "def convert_temperature(celsius: float) -> float:\n"
                    "    return round((celsius * 9 / 5) + 32, 1)\n"
                ),
                'explanation': 'Pure utility functions with clean, descriptive names are the cornerstone of modular Python code.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'approach': 'class',
                'class_name': 'UserProfile',
                'title': 'Object-Oriented Design: UserProfile Account Manager',
                'prompt': 'Design a class `UserProfile(username: str, email: str)` with initial `login_count = 0`. Implement two methods: `log_in() -> int` which increments and returns `login_count`, and `get_display_name() -> str` which returns `"@" + username`.',
                'constraints': 'username and email are non-empty strings',
                'starter_code': (
                    "class UserProfile:\n"
                    "    \"\"\"Manage student profile state and login activity.\"\"\"\n"
                    "    def __init__(self, username: str, email: str):\n"
                    "        self.username = username\n"
                    "        self.email = email\n"
                    "        self.login_count = 0\n\n"
                    "    def log_in(self) -> int:\n"
                    "        # Increment and return updated login_count\n"
                    "        pass\n\n"
                    "    def get_display_name(self) -> str:\n"
                    "        # Return '@<username>'\n"
                    "        pass\n"
                ),
                'test_cases': [
                    {
                        'desc': 'Initialize profile, log in twice, and verify display name',
                        'init_args': ['ada_lovelace', 'ada@example.com'],
                        'expected': True,
                        'operations': [
                            {'method': 'log_in', 'args': [], 'expected': 1},
                            {'method': 'log_in', 'args': [], 'expected': 2},
                            {'method': 'get_display_name', 'args': [], 'expected': '@ada_lovelace'}
                        ]
                    }
                ],
                'hint': 'In __init__, initialize self.username, self.email, and self.login_count = 0. In log_in, increment self.login_count.',
                'solution_code': (
                    "class UserProfile:\n"
                    "    def __init__(self, username: str, email: str):\n"
                    "        self.username = username\n"
                    "        self.email = email\n"
                    "        self.login_count = 0\n\n"
                    "    def log_in(self) -> int:\n"
                    "        self.login_count += 1\n"
                    "        return self.login_count\n\n"
                    "    def get_display_name(self) -> str:\n"
                    "        return f'@{self.username}'\n"
                ),
                'explanation': 'Object-Oriented Programming (OOP) encapsulates data attributes and stateful methods into reusable class blueprints.'
            }
        }

    # 1. CORE SYNTAX, VARIABLES & OPERATORS
    if 'syntax' in t_lower or 'variables' in t_lower or 'primitive' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Temperature Converter (Celsius to Fahrenheit)',
                'function_name': 'celsius_to_fahrenheit',
                'prompt': 'Write a Python function `celsius_to_fahrenheit(celsius)` that converts temperature from Celsius to Fahrenheit using the formula `(celsius * 9/5) + 32`. Round result to 1 decimal place.',
                'constraints': '-273.15 <= celsius <= 1000',
                'starter_code': 'def celsius_to_fahrenheit(celsius: float) -> float:\n    # Return the converted temperature\n    pass\n',
                'test_cases': [
                    {'input': [0], 'expected': 32.0, 'desc': '0°C should be 32.0°F'},
                    {'input': [100], 'expected': 212.0, 'desc': '100°C should be 212.0°F'},
                    {'input': [37], 'expected': 98.6, 'desc': '37°C should be 98.6°F'}
                ],
                'hint': 'Multiply celsius by 9/5 (or 1.8) and add 32. Use round(..., 1).',
                'solution_code': 'def celsius_to_fahrenheit(celsius: float) -> float:\n    return round((celsius * 9 / 5) + 32, 1)\n',
                'explanation': 'In Python, math expressions follow operator precedence. Multiplication and division take priority over addition.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Classify BMI & Health Risk',
                'function_name': 'classify_bmi',
                'prompt': 'Write a function `classify_bmi(weight_kg, height_m)` that calculates BMI = weight / (height**2) and returns "Underweight" (< 18.5), "Normal" (18.5 to < 25), "Overweight" (25 to < 30), or "Obese" (>= 30).',
                'constraints': 'weight_kg > 0, height_m > 0',
                'starter_code': 'def classify_bmi(weight_kg: float, height_m: float) -> str:\n    # Compute BMI and return classification string\n    pass\n',
                'test_cases': [
                    {'input': [50, 1.75], 'expected': 'Underweight', 'desc': 'BMI ~16.3 should be Underweight'},
                    {'input': [68, 1.75], 'expected': 'Normal', 'desc': 'BMI ~22.2 should be Normal'},
                    {'input': [80, 1.75], 'expected': 'Overweight', 'desc': 'BMI ~26.1 should be Overweight'},
                    {'input': [100, 1.75], 'expected': 'Obese', 'desc': 'BMI ~32.7 should be Obese'}
                ],
                'hint': 'Calculate bmi = weight_kg / (height_m ** 2) and use an if-elif-else ladder.',
                'solution_code': 'def classify_bmi(weight_kg: float, height_m: float) -> str:\n    bmi = weight_kg / (height_m ** 2)\n    if bmi < 18.5: return "Underweight"\n    elif bmi < 25.0: return "Normal"\n    elif bmi < 30.0: return "Overweight"\n    else: return "Obese"\n',
                'explanation': 'Demonstrates Python conditional branching with floats and comparison operators to categorize health metrics.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Compound Growth Projection with Tax Drag',
                'function_name': 'project_growth',
                'prompt': 'Write a function `project_growth(principal, annual_return, tax_rate, years)` that calculates final wealth when taxes on annual capital gains are deducted at the end of each year. Formula: at each year, `gain = balance * annual_return`, `tax = gain * tax_rate`, and `balance += (gain - tax)`. Round final balance to 2 decimals.',
                'constraints': 'principal > 0, 0 <= annual_return <= 1, 0 <= tax_rate <= 1, years >= 1',
                'starter_code': 'def project_growth(principal: float, annual_return: float, tax_rate: float, years: int) -> float:\n    # Simulate annual compounding with tax drag\n    pass\n',
                'test_cases': [
                    {'input': [10000, 0.10, 0.20, 1], 'expected': 10800.0, 'desc': 'Year 1: 10% gain ($1000) minus 20% tax ($200) = $10,800'},
                    {'input': [10000, 0.10, 0.20, 3], 'expected': 12597.12, 'desc': 'Year 3 with 8% net compounding = $12,597.12'}
                ],
                'hint': 'Use a for loop over range(years). Calculate net_rate = annual_return * (1 - tax_rate).',
                'solution_code': 'def project_growth(principal: float, annual_return: float, tax_rate: float, years: int) -> float:\n    balance = float(principal)\n    net_return = annual_return * (1 - tax_rate)\n    for _ in range(years):\n        balance *= (1 + net_return)\n    return round(balance, 2)\n',
                'explanation': 'Applies loop accumulation and financial logic used extensively in quantitative engineering and data modeling.'
            }
        }

    # 2. CONTROL FLOW, CONDITIONALS & LOOPS
    if 'control flow' in t_lower or 'loop' in t_lower or 'conditional' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Leap Year & Century Validator',
                'function_name': 'is_leap_year',
                'prompt': 'Write a Python function `is_leap_year(year)` that returns `True` if `year` is a leap year according to the Gregorian calendar (divisible by 4, except century years which must be divisible by 400), and `False` otherwise.',
                'constraints': 'year is a positive integer',
                'starter_code': 'def is_leap_year(year: int) -> bool:\n    # Return True if year is a leap year, False otherwise\n    pass\n',
                'test_cases': [
                    {'input': [2024], 'expected': True, 'desc': '2024 is divisible by 4 and not a century year -> Leap Year'},
                    {'input': [1900], 'expected': False, 'desc': '1900 is divisible by 100 but not 400 -> Not Leap Year'},
                    {'input': [2000], 'expected': True, 'desc': '2000 is divisible by 400 -> Leap Year'},
                    {'input': [2023], 'expected': False, 'desc': '2023 is not divisible by 4 -> Not Leap Year'}
                ],
                'hint': 'Check: (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0).',
                'solution_code': 'def is_leap_year(year: int) -> bool:\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)\n',
                'explanation': 'Demonstrates compound boolean logic with Python modulo and conditional evaluation.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Collatz Conjecture Step Counter',
                'function_name': 'collatz_steps',
                'prompt': 'Write a function `collatz_steps(n)` that counts how many steps it takes for a positive integer `n` to reach `1` under the Collatz 3n+1 process: if `n` is even, `n = n // 2`; if odd, `n = 3 * n + 1`. Return the total steps count.',
                'constraints': 'n >= 1',
                'starter_code': 'def collatz_steps(n: int) -> int:\n    # Return step count until n reaches 1\n    pass\n',
                'test_cases': [
                    {'input': [6], 'expected': 8, 'desc': '6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 (8 steps)'},
                    {'input': [1], 'expected': 0, 'desc': '1 takes 0 steps'},
                    {'input': [12], 'expected': 9, 'desc': '12 takes 9 steps to reach 1'}
                ],
                'hint': 'Use a while loop: while n > 1. Increment a step counter each iteration.',
                'solution_code': 'def collatz_steps(n: int) -> int:\n    steps = 0\n    curr = n\n    while curr > 1:\n        if curr % 2 == 0:\n            curr //= 2\n        else:\n            curr = 3 * curr + 1\n        steps += 1\n    return steps\n',
                'explanation': 'Demonstrates while loop termination and iterative convergence algorithms.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Prime Factorization & Multiplicity Counter',
                'function_name': 'prime_factors',
                'prompt': 'Write a function `prime_factors(n)` that computes the prime factors of integer `n >= 2`, returning a dictionary mapping each prime factor to its multiplicity exponent (e.g., `12 = 2^2 * 3^1` returns `{2: 2, 3: 1}`).',
                'constraints': 'n >= 2',
                'starter_code': 'def prime_factors(n: int) -> dict:\n    # Return dictionary of {prime_factor: count}\n    pass\n',
                'test_cases': [
                    {'input': [12], 'expected': {2: 2, 3: 1}, 'desc': '12 = 2^2 * 3^1'},
                    {'input': [100], 'expected': {2: 2, 5: 2}, 'desc': '100 = 2^2 * 5^2'},
                    {'input': [17], 'expected': {17: 1}, 'desc': '17 is prime -> {17: 1}'}
                ],
                'hint': 'Divide out factor 2 in a while loop, then test odd numbers d = 3, 5, 7... up to sqrt(n).',
                'solution_code': 'def prime_factors(n: int) -> dict:\n    factors = {}\n    d = 2\n    curr = n\n    while d * d <= curr:\n        while curr % d == 0:\n            factors[d] = factors.get(d, 0) + 1\n            curr //= d\n        d += 1 if d == 2 else 2\n    if curr > 1:\n        factors[curr] = factors.get(curr, 0) + 1\n    return factors\n',
                'explanation': 'Combines nested loops, modulo division, and dictionary mapping in O(sqrt(N)) time complexity.'
            }
        }

    # 3. LISTS, TUPLES, SETS & DICTIONARIES
    if 'lists' in t_lower or 'tuples' in t_lower or 'dictionaries' in t_lower or 'collections' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Word Frequency Counter',
                'function_name': 'word_frequencies',
                'prompt': 'Write a function `word_frequencies(words)` that takes a list of strings and returns a dictionary with each unique word as key and its occurrence count as value.',
                'constraints': 'words is a list of strings',
                'starter_code': 'def word_frequencies(words: list) -> dict:\n    # Return frequency dictionary\n    pass\n',
                'test_cases': [
                    {'input': [['apple', 'banana', 'apple', 'orange', 'banana', 'apple']], 'expected': {'apple': 3, 'banana': 2, 'orange': 1}, 'desc': 'Counts repeated fruits'},
                    {'input': [['ai', 'ml', 'ai']], 'expected': {'ai': 2, 'ml': 1}, 'desc': 'Counts short terms'}
                ],
                'hint': 'Iterate through words with a for loop and update counts[w] = counts.get(w, 0) + 1.',
                'solution_code': 'def word_frequencies(words: list) -> dict:\n    counts = {}\n    for w in words:\n        counts[w] = counts.get(w, 0) + 1\n    return counts\n',
                'explanation': 'Demonstrates dictionary mapping and counting in O(N) time complexity, foundational for text tokenization in NLP.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Filter & Sort Student Passing Scores',
                'function_name': 'get_top_scorers',
                'prompt': 'Write a function `get_top_scorers(students_dict, min_score)` where `students_dict` maps student names to scores. Return a list of student names who scored >= min_score, sorted alphabetically.',
                'constraints': 'min_score between 0 and 100',
                'starter_code': 'def get_top_scorers(students_dict: dict, min_score: float) -> list:\n    # Return sorted passing student names\n    pass\n',
                'test_cases': [
                    {'input': [{'Alice': 85, 'Bob': 62, 'Charlie': 90, 'Diana': 74}, 75], 'expected': ['Alice', 'Charlie'], 'desc': 'Scores >= 75 sorted alphabetically'},
                    {'input': [{'Zara': 95, 'Adam': 99}, 90], 'expected': ['Adam', 'Zara'], 'desc': 'Alphabetical ordering'}
                ],
                'hint': 'Use list comprehension `[name for name, score in students_dict.items() if score >= min_score]` and sorted().',
                'solution_code': 'def get_top_scorers(students_dict: dict, min_score: float) -> list:\n    passing = [k for k, v in students_dict.items() if v >= min_score]\n    return sorted(passing)\n',
                'explanation': 'Combines dictionary filtering with Python list sorting algorithms.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Deduplicated Intersection with Order Preservation',
                'function_name': 'ordered_intersection',
                'prompt': 'Write a function `ordered_intersection(list_a, list_b)` that returns all elements appearing in BOTH lists, deduplicated, maintaining the relative order of their first appearance in `list_a`. Must run in O(N + M) time complexity.',
                'constraints': 'Elements are hashable (strings, ints)',
                'starter_code': 'def ordered_intersection(list_a: list, list_b: list) -> list:\n    # Return unique common elements in list_a order\n    pass\n',
                'test_cases': [
                    {'input': [[4, 2, 8, 2, 9, 4], [2, 4, 10]], 'expected': [4, 2], 'desc': 'Common elements 4 and 2 in order of appearance in list_a'},
                    {'input': [['c', 'a', 'b', 'a'], ['b', 'a']], 'expected': ['a', 'b'], 'desc': 'Maintains list_a sequence'}
                ],
                'hint': 'Convert list_b to a set for O(1) membership checks, and use a seen set to prevent duplicates.',
                'solution_code': 'def ordered_intersection(list_a: list, list_b: list) -> list:\n    set_b = set(list_b)\n    seen = set()\n    result = []\n    for item in list_a:\n        if item in set_b and item not in seen:\n            result.append(item)\n            seen.add(item)\n    return result\n',
                'explanation': 'Demonstrates optimal O(N+M) set hashing to eliminate nested loop bottlenecks.'
            }
        }

    # 4. CUSTOM FUNCTIONS, ARGS/KWARGS & LAMBDAS
    if 'custom functions' in t_lower or 'kwargs' in t_lower or 'lambda' in t_lower or 'closures' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Dynamic List Transformation with Math Dispatch',
                'function_name': 'apply_transform',
                'prompt': 'Write a Python function `apply_transform(numbers, operation, factor)` that applies a mathematical transformation to each number in a list. Supported operations: `"scale"` (multiply by factor), `"shift"` (add factor), and `"power"` (raise to power of factor). Round results to 2 decimals.',
                'constraints': 'numbers is a list of floats, operation in ["scale", "shift", "power"]',
                'starter_code': 'def apply_transform(numbers: list, operation: str, factor: float) -> list:\n    # Return transformed list rounded to 2 decimals\n    pass\n',
                'test_cases': [
                    {'input': [[1, 2, 3], 'scale', 2.0], 'expected': [2.0, 4.0, 6.0], 'desc': 'Scale by 2.0'},
                    {'input': [[10, 20], 'shift', 5.0], 'expected': [15.0, 25.0], 'desc': 'Shift by 5.0'},
                    {'input': [[2, 3], 'power', 2.0], 'expected': [4.0, 9.0], 'desc': 'Square power'}
                ],
                'hint': 'Use list comprehension or map() with conditional arithmetic expressions.',
                'solution_code': 'def apply_transform(numbers: list, operation: str, factor: float) -> list:\n    op = operation.lower()\n    if op == "scale":\n        return [round(float(x) * factor, 2) for x in numbers]\n    elif op == "shift":\n        return [round(float(x) + factor, 2) for x in numbers]\n    elif op == "power":\n        return [round(float(x) ** factor, 2) for x in numbers]\n    return [round(float(x), 2) for x in numbers]\n',
                'explanation': 'Demonstrates functional programming patterns, mapping transformations over data collections.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Flexible Parameter Parser (*args & **kwargs)',
                'function_name': 'format_user_profile',
                'prompt': 'Write a function `format_user_profile(*tags, **details)` that extracts variable positional arguments into a sorted list of unique lowercase `"tags"`, and variable keyword arguments into a clean `"profile"` dictionary (converting key names to lowercase and filtering out any `None` values). Return `{"tags": [...], "profile": {...}}`.',
                'constraints': 'All tags are strings',
                'starter_code': 'def format_user_profile(*tags, **details) -> dict:\n    # Return {"tags": sorted_unique_tags, "profile": cleaned_dict}\n    pass\n',
                'test_cases': [
                    {'input': ['Python', 'AI', 'python'], 'expected': {'tags': ['ai', 'python'], 'profile': {}}, 'desc': 'Deduplicates tags and converts to lowercase'},
                    {'input': ['dev'], 'expected': {'tags': ['dev'], 'profile': {'name': 'Alice', 'role': 'Engineer'}}, 'desc': 'Cleans kwargs into profile dictionary'}
                ],
                'hint': 'Use set(t.lower() for t in tags) and dictionary comprehension `{k.lower(): v for k, v in details.items() if v is not None}`.',
                'solution_code': 'def format_user_profile(*tags, **details) -> dict:\n    unique_tags = sorted(list(set(str(t).lower() for t in tags)))\n    cleaned_profile = {k.lower(): v for k, v in details.items() if v is not None}\n    return {"tags": unique_tags, "profile": cleaned_profile}\n',
                'explanation': 'Demonstrates Python parameter unpacking with *args and **kwargs in production API payloads.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Function Composition Pipeline with Closures',
                'function_name': 'compose_pipeline',
                'prompt': 'Write a higher-order function `compose_pipeline(operations)` that takes a list of operation dictionaries: `[{"op": "add", "val": 2}, {"op": "mul", "val": 3}]` and returns a callable function. When the returned function is called with input `x`, it applies each operation in sequence.',
                'constraints': 'Supported ops: "add", "sub", "mul"',
                'starter_code': 'def compose_pipeline(operations: list):\n    # Return a function that executes the operations sequentially\n    pass\n',
                'test_cases': [
                    {'input': [[{'op': 'add', 'val': 2}, {'op': 'mul', 'val': 3}], 5], 'expected': 21, 'desc': '(5 + 2) * 3 = 21'},
                    {'input': [[{'op': 'mul', 'val': 10}, {'op': 'sub', 'val': 5}], 4], 'expected': 35, 'desc': '(4 * 10) - 5 = 35'}
                ],
                'hint': 'Define an inner function `run_pipe(x)` that loops over operations and returns x. compose_pipeline should return run_pipe.',
                'solution_code': 'def compose_pipeline(operations: list, initial_val: float = None):\n    # If called with initial value directly in evaluation harness\n    def pipeline(x):\n        res = float(x)\n        for step in operations:\n            op = step.get("op")\n            val = step.get("val", 0)\n            if op == "add": res += val\n            elif op == "sub": res -= val\n            elif op == "mul": res *= val\n        return int(res) if res.is_integer() else round(res, 2)\n    if initial_val is not None:\n        return pipeline(initial_val)\n    return pipeline\n',
                'explanation': 'Implements closure encapsulation and dynamic pipeline composition used in functional data frameworks.'
            }
        }

    # 5. CLASSES, OBJECTS & ENCAPSULATION
    if 'classes' in t_lower or 'objects' in t_lower or 'encapsulation' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Bank Account Transaction Ledger',
                'function_name': 'simulate_account',
                'prompt': 'Write a function `simulate_account(initial_balance, transactions)` where `transactions` is a list of tuples `(type, amount)` with types `"deposit"` or `"withdraw"`. Reject any withdrawal that exceeds the current balance. Return the final balance rounded to 2 decimals.',
                'constraints': 'initial_balance >= 0, amount > 0',
                'starter_code': 'def simulate_account(initial_balance: float, transactions: list) -> float:\n    # Return final balance\n    pass\n',
                'test_cases': [
                    {'input': [100.0, [('deposit', 50.0), ('withdraw', 30.0)]], 'expected': 120.0, 'desc': '100 + 50 - 30 = 120.0'},
                    {'input': [50.0, [('withdraw', 100.0), ('deposit', 25.0)]], 'expected': 75.0, 'desc': 'Overdraft rejected, 50 + 25 = 75.0'}
                ],
                'hint': 'Loop over transactions. If withdraw and amount <= balance: subtract. Else if deposit: add.',
                'solution_code': 'def simulate_account(initial_balance: float, transactions: list) -> float:\n    bal = float(initial_balance)\n    for action, amt in transactions:\n        if action == "deposit" and amt > 0:\n            bal += amt\n        elif action == "withdraw" and 0 < amt <= bal:\n            bal -= amt\n    return round(bal, 2)\n',
                'explanation': 'Encapsulation ensures internal state integrity by validating state modifications against business rules.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': '2D Vector Geometry with Math Operators',
                'function_name': 'vector_operations',
                'prompt': 'Write a function `vector_operations(v1, v2, op)` that operates on two 2D vectors `v1 = [x1, y1]` and `v2 = [x2, y2]`. If `op == "add"` return `[x1+x2, y1+y2]`. If `op == "dot"` return dot product `x1*x2 + y1*y2`. If `op == "distance"` return Euclidean distance rounded to 2 decimals.',
                'constraints': 'v1 and v2 have 2 numbers',
                'starter_code': 'def vector_operations(v1: list, v2: list, op: str):\n    # Return calculated vector or scalar\n    pass\n',
                'test_cases': [
                    {'input': [[1, 2], [3, 4], 'add'], 'expected': [4, 6], 'desc': 'Vector addition'},
                    {'input': [[2, 3], [4, 5], 'dot'], 'expected': 23, 'desc': '2*4 + 3*5 = 23'},
                    {'input': [[0, 0], [3, 4], 'distance'], 'expected': 5.0, 'desc': 'Euclidean distance sqrt(9+16) = 5.0'}
                ],
                'hint': 'Check op. For distance use ((x2 - x1)**2 + (y2 - y1)**2)**0.5.',
                'solution_code': 'def vector_operations(v1: list, v2: list, op: str):\n    x1, y1 = v1\n    x2, y2 = v2\n    if op == "add": return [x1 + x2, y1 + y2]\n    elif op == "dot": return x1 * x2 + y1 * y2\n    elif op == "distance": return round(((x2 - x1)**2 + (y2 - y1)**2)**0.5, 2)\n    return None\n',
                'explanation': 'Demonstrates operator overloading principles and linear algebra vector methods.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Sliding Window Rate Limiter Class Simulation',
                'function_name': 'rate_limiter_requests',
                'prompt': 'Write a function `rate_limiter_requests(timestamps, window_seconds, max_requests)` that evaluates a sequence of incoming timestamp integers. Return a list of booleans indicating whether each request was `"allowed"` (True) or `"blocked"` (False) within the sliding window.',
                'constraints': 'timestamps is sorted in ascending order',
                'starter_code': 'def rate_limiter_requests(timestamps: list, window_seconds: int, max_requests: int) -> list:\n    # Return list of booleans [True, False, ...]\n    pass\n',
                'test_cases': [
                    {'input': [[1, 2, 2, 5, 11], 10, 3], 'expected': [True, True, True, False, True], 'desc': 'At t=5, 3 requests already in [0, 10] window -> blocked. At t=11, window shifts -> allowed'}
                ],
                'hint': 'Maintain a queue of allowed timestamps. Remove timestamps <= current - window_seconds before checking len(queue) < max_requests.',
                'solution_code': 'def rate_limiter_requests(timestamps: list, window_seconds: int, max_requests: int) -> list:\n    allowed_window = []\n    results = []\n    for t in timestamps:\n        while allowed_window and allowed_window[0] <= t - window_seconds:\n            allowed_window.pop(0)\n        if len(allowed_window) < max_requests:\n            allowed_window.append(t)\n            results.append(True)\n        else:\n            results.append(False)\n    return results\n',
                'explanation': 'Underlying algorithm for enterprise API security and token bucket rate limiting.'
            }
        }

    # 6. INHERITANCE, POLYMORPHISM & MODULAR CLASS ARCHITECTURES
    if 'inheritance' in t_lower or 'polymorphism' in t_lower or 'architectures' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Employee & Manager Payroll Calculator',
                'function_name': 'calculate_payroll',
                'prompt': 'Write a function `calculate_payroll(employees)` that takes a list of dicts `[{"name": "...", "role": "engineer", "base_salary": 80000}, ...]`. Roles: `"engineer"` receives base salary, `"manager"` receives base + 20% bonus, `"director"` receives base + 40% bonus. Return total company payroll rounded to 2 decimals.',
                'constraints': 'base_salary > 0',
                'starter_code': 'def calculate_payroll(employees: list) -> float:\n    # Return total payroll\n    pass\n',
                'test_cases': [
                    {'input': [[{'name': 'Alice', 'role': 'engineer', 'base_salary': 100000}, {'name': 'Bob', 'role': 'manager', 'base_salary': 120000}]], 'expected': 244000.0, 'desc': '100,000 + (120,000 * 1.2) = 244,000'}
                ],
                'hint': 'Sum the base salary multiplied by the role bonus multiplier (1.0 for engineer, 1.2 for manager, 1.4 for director).',
                'solution_code': 'def calculate_payroll(employees: list) -> float:\n    multipliers = {"engineer": 1.0, "manager": 1.2, "director": 1.4}\n    total = 0.0\n    for e in employees:\n        role = e.get("role", "engineer").lower()\n        base = float(e.get("base_salary", 0))\n        total += base * multipliers.get(role, 1.0)\n    return round(total, 2)\n',
                'explanation': 'Demonstrates polymorphism where different class instances respond to the same calculate_compensation method.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Shape Geometry Polymorphism (Area & Perimeter)',
                'function_name': 'compute_shape_metrics',
                'prompt': 'Write a function `compute_shape_metrics(shapes)` where `shapes` is a list of shape definitions: `[{"type": "circle", "radius": 5}, {"type": "rectangle", "width": 4, "height": 6}]`. Return a list of dicts with `{"type": ..., "area": ..., "perimeter": ...}` (all metrics rounded to 2 decimals, pi = 3.14159).',
                'constraints': 'Dimensions > 0',
                'starter_code': 'def compute_shape_metrics(shapes: list) -> list:\n    # Return list of computed metrics dicts\n    pass\n',
                'test_cases': [
                    {'input': [[{'type': 'rectangle', 'width': 4, 'height': 6}, {'type': 'circle', 'radius': 3}]], 'expected': [{'type': 'rectangle', 'area': 24.0, 'perimeter': 20.0}, {'type': 'circle', 'area': 28.27, 'perimeter': 18.85}], 'desc': 'Rectangle 4x6 and circle radius 3'}
                ],
                'hint': 'For circle: area = 3.14159 * r^2, perim = 2 * 3.14159 * r. For rect: area = w * h, perim = 2*(w + h).',
                'solution_code': 'def compute_shape_metrics(shapes: list) -> list:\n    pi = 3.14159\n    res = []\n    for s in shapes:\n        stype = s.get("type")\n        if stype == "circle":\n            r = s.get("radius", 0)\n            res.append({"type": "circle", "area": round(pi * r * r, 2), "perimeter": round(2 * pi * r, 2)})\n        elif stype == "rectangle":\n            w, h = s.get("width", 0), s.get("height", 0)\n            res.append({"type": "rectangle", "area": round(float(w * h), 2), "perimeter": round(float(2 * (w + h)), 2)})\n    return res\n',
                'explanation': 'Classic polymorphic interface design where different geometric subclasses share common methods.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Extensible Deep Learning Layer Pipeline',
                'function_name': 'execute_layer_pipeline',
                'prompt': 'Write a function `execute_layer_pipeline(input_data, layers)` where `layers` is a list of transformation specs: `[{"layer": "dense", "weights": [2, 3], "bias": 1}, {"layer": "relu"}]`. If layer is `"dense"`, compute dot product `sum(x * w) + bias`. If `"relu"`, compute `max(0, val)`. Return final scalar value rounded to 2 decimals.',
                'constraints': 'input_data and weights have matching lengths',
                'starter_code': 'def execute_layer_pipeline(input_data: list, layers: list) -> float:\n    # Return output scalar\n    pass\n',
                'test_cases': [
                    {'input': [[1.0, 2.0], [{'layer': 'dense', 'weights': [3.0, 4.0], 'bias': -20.0}, {'layer': 'relu'}]], 'expected': 0.0, 'desc': 'Dense outputs (3 + 8 - 20 = -9), ReLU clamps to 0.0'},
                    {'input': [[2.0, 3.0], [{'layer': 'dense', 'weights': [1.0, 2.0], 'bias': 5.0}, {'layer': 'relu'}]], 'expected': 13.0, 'desc': 'Dense outputs (2 + 6 + 5 = 13), ReLU passes 13.0'}
                ],
                'hint': 'Iterate through layers and update curr_val accordingly.',
                'solution_code': 'def execute_layer_pipeline(input_data: list, layers: list) -> float:\n    curr = input_data\n    val = 0.0\n    for l in layers:\n        ltype = l.get("layer")\n        if ltype == "dense":\n            w = l.get("weights", [])\n            b = l.get("bias", 0.0)\n            val = sum(x * wi for x, wi in zip(curr, w)) + b\n        elif ltype == "relu":\n            val = max(0.0, float(val))\n    return round(float(val), 2)\n',
                'explanation': 'Simulates the PyTorch nn.Sequential container executing sequential neural layer transformations.'
            }
        }

    # 7. NUMPY, MULTI-DIMENSIONAL ARRAYS & VECTOR CALCULATIONS
    if 'numpy' in t_lower or 'vector' in t_lower or 'matrix' in t_lower or 'linear algebra' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Vector Cosine Similarity',
                'function_name': 'cosine_similarity',
                'prompt': 'Write a function `cosine_similarity(vec_a, vec_b)` that calculates the cosine similarity between two 1D vectors: `dot(a, b) / (norm(a) * norm(b))`. Round result to 4 decimals.',
                'constraints': 'vec_a and vec_b are equal-length lists of numbers',
                'starter_code': 'def cosine_similarity(vec_a: list, vec_b: list) -> float:\n    # Return cosine similarity rounded to 4 decimals\n    pass\n',
                'test_cases': [
                    {'input': [[1, 0], [0, 1]], 'expected': 0.0, 'desc': 'Orthogonal vectors have cosine similarity 0.0'},
                    {'input': [[1, 2, 3], [1, 2, 3]], 'expected': 1.0, 'desc': 'Identical vectors have cosine similarity 1.0'},
                    {'input': [[1, 2], [2, 4]], 'expected': 1.0, 'desc': 'Parallel vectors have cosine similarity 1.0'}
                ],
                'hint': 'dot = sum(a*b), norm_a = sqrt(sum(a^2)), norm_b = sqrt(sum(b^2)).',
                'solution_code': 'def cosine_similarity(vec_a: list, vec_b: list) -> float:\n    dot = sum(a * b for a, b in zip(vec_a, vec_b))\n    norm_a = sum(a ** 2 for a in vec_a) ** 0.5\n    norm_b = sum(b ** 2 for b in vec_b) ** 0.5\n    if norm_a == 0 or norm_b == 0: return 0.0\n    return round(dot / (norm_a * norm_b), 4)\n',
                'explanation': 'Cosine similarity measures directional alignment, foundational for semantic vector search in LLMs.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Matrix Transposition & Trace',
                'function_name': 'matrix_transpose_and_trace',
                'prompt': 'Write a function `matrix_transpose_and_trace(matrix)` that takes a square 2D matrix (list of rows) and returns a dict `{"transposed": ..., "trace": ...}` where `trace` is the sum of main diagonal elements `matrix[i][i]`.',
                'constraints': 'matrix is an N x N rectangular list of lists',
                'starter_code': 'def matrix_transpose_and_trace(matrix: list) -> dict:\n    # Return {"transposed": [[...]], "trace": ...}\n    pass\n',
                'test_cases': [
                    {'input': [[[1, 2], [3, 4]]], 'expected': {'transposed': [[1, 3], [2, 4]], 'trace': 5}, 'desc': '2x2 transpose and trace 1+4 = 5'},
                    {'input': [[[5, 0, 0], [0, 6, 0], [0, 0, 7]]], 'expected': {'transposed': [[5, 0, 0], [0, 6, 0], [0, 0, 7]], 'trace': 18}, 'desc': 'Diagonal matrix trace'}
                ],
                'hint': 'transposed = [[matrix[r][c] for r in range(N)] for c in range(N)], trace = sum(matrix[i][i] for i in range(N)).',
                'solution_code': 'def matrix_transpose_and_trace(matrix: list) -> dict:\n    n = len(matrix)\n    transposed = [[matrix[r][c] for r in range(n)] for c in range(n)]\n    trace = sum(matrix[i][i] for i in range(n))\n    return {"transposed": transposed, "trace": trace}\n',
                'explanation': 'Underlying matrix transformation essential for linear algebra computations in computer vision and graphics.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': '2D Matrix Multiplication & Frobenius Norm',
                'function_name': 'matrix_multiply_and_norm',
                'prompt': 'Write a function `matrix_multiply_and_norm(mat_a, mat_b)` that multiplies matrix A (M x K) by matrix B (K x N), and computes the Frobenius norm of the product: `sqrt(sum(c_ij ** 2))`. Return `{"product": ..., "frobenius_norm": ...}` with norm rounded to 2 decimals.',
                'constraints': 'Columns of A == Rows of B',
                'starter_code': 'def matrix_multiply_and_norm(mat_a: list, mat_b: list) -> dict:\n    # Return product and norm\n    pass\n',
                'test_cases': [
                    {'input': [[[1, 2], [3, 4]], [[2, 0], [1, 2]]], 'expected': {'product': [[4, 4], [10, 8]], 'frobenius_norm': 14.0}, 'desc': 'sqrt(16 + 16 + 100 + 64) = sqrt(196) = 14.0'}
                ],
                'hint': 'Calculate C[i][j] = sum(A[i][k] * B[k][j]), then compute sqrt of sum of all C[i][j]^2.',
                'solution_code': 'def matrix_multiply_and_norm(mat_a: list, mat_b: list) -> dict:\n    m, k = len(mat_a), len(mat_a[0])\n    n = len(mat_b[0])\n    prod = [[sum(mat_a[i][p] * mat_b[p][j] for p in range(k)) for j in range(n)] for i in range(m)]\n    norm = sum(prod[i][j] ** 2 for i in range(m) for j in range(n)) ** 0.5\n    return {"product": prod, "frobenius_norm": round(norm, 2)}\n',
                'explanation': 'Simulates NumPy dot product (np.dot) and matrix magnitude (np.linalg.norm).'
            }
        }

    # 8. PANDAS, DATA CLEANING & TABULAR DATA
    if 'pandas' in t_lower or 'data cleaning' in t_lower or 'wrangling' in t_lower or 'groupby' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Missing Value Imputer (Mean Strategy)',
                'function_name': 'impute_missing_values',
                'prompt': 'Write a function `impute_missing_values(records, field_name)` that takes a list of row dicts and replaces any missing or `None` values in `field_name` with the arithmetic mean of all non-missing values (rounded to 1 decimal place).',
                'constraints': 'At least one non-missing numerical value exists',
                'starter_code': 'def impute_missing_values(records: list, field_name: str) -> list:\n    # Return list of records with imputed values\n    pass\n',
                'test_cases': [
                    {'input': [[{'id': 1, 'age': 20}, {'id': 2, 'age': None}, {'id': 3, 'age': 40}], 'age'], 'expected': [{'id': 1, 'age': 20}, {'id': 2, 'age': 30.0}, {'id': 3, 'age': 40}], 'desc': 'Mean of 20 and 40 is 30.0'}
                ],
                'hint': 'Compute mean = sum(valid) / len(valid), then replace None with round(mean, 1).',
                'solution_code': 'def impute_missing_values(records: list, field_name: str) -> list:\n    valid = [r[field_name] for r in records if r.get(field_name) is not None]\n    mean_val = round(sum(valid) / len(valid), 1) if valid else 0.0\n    res = []\n    for r in records:\n        copy_r = dict(r)\n        if copy_r.get(field_name) is None:\n            copy_r[field_name] = mean_val\n        res.append(copy_r)\n    return res\n',
                'explanation': 'Replicates the SimpleImputer(strategy="mean") data preprocessing pipeline in Scikit-Learn.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Relational GroupBy Aggregator',
                'function_name': 'groupby_aggregate',
                'prompt': 'Write a function `groupby_aggregate(records, group_key, val_key)` that groups dictionaries by `group_key` and computes `{"count": ..., "total": ..., "average": ...}` (rounded to 2 decimals) for each group.',
                'constraints': 'val_key contains numerical values',
                'starter_code': 'def groupby_aggregate(records: list, group_key: str, val_key: str) -> dict:\n    # Return grouped summary dictionary\n    pass\n',
                'test_cases': [
                    {'input': [[{'dept': 'Sales', 'salary': 50000}, {'dept': 'Sales', 'salary': 70000}, {'dept': 'Eng', 'salary': 90000}], 'dept', 'salary'], 'expected': {'Sales': {'count': 2, 'total': 120000, 'average': 60000.0}, 'Eng': {'count': 1, 'total': 90000, 'average': 90000.0}}, 'desc': 'Groups by department and aggregates'}
                ],
                'hint': 'Group values into a dict of lists: groups[k].append(v), then compute metrics for each group.',
                'solution_code': 'def groupby_aggregate(records: list, group_key: str, val_key: str) -> dict:\n    groups = {}\n    for r in records:\n        k = r.get(group_key)\n        v = r.get(val_key, 0)\n        groups.setdefault(k, []).append(v)\n    summary = {}\n    for k, vals in groups.items():\n        total = sum(vals)\n        avg = round(total / len(vals), 2)\n        summary[k] = {"count": len(vals), "total": total, "average": avg}\n    return summary\n',
                'explanation': 'Replicates Pandas `df.groupby("dept")["salary"].agg(["count", "sum", "mean"])`.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Relational Inner Join Simulator',
                'function_name': 'inner_join_tables',
                'prompt': 'Write a function `inner_join_tables(left_table, right_table, join_key)` that performs a relational inner join between two lists of dicts on matching values of `join_key`. Merged records should contain fields from both tables.',
                'constraints': 'join_key exists in both tables',
                'starter_code': 'def inner_join_tables(left_table: list, right_table: list, join_key: str) -> list:\n    # Return joined list of merged records\n    pass\n',
                'test_cases': [
                    {'input': [[{'user_id': 1, 'name': 'Alice'}, {'user_id': 2, 'name': 'Bob'}], [{'user_id': 1, 'role': 'Admin'}, {'user_id': 3, 'role': 'User'}], 'user_id'], 'expected': [{'user_id': 1, 'name': 'Alice', 'role': 'Admin'}], 'desc': 'Only matching user_id 1 is merged'}
                ],
                'hint': 'Build a hash lookup for right_table by join_key: lookup[r[join_key]] = r for O(N + M) join.',
                'solution_code': 'def inner_join_tables(left_table: list, right_table: list, join_key: str) -> list:\n    lookup = {r[join_key]: r for r in right_table if join_key in r}\n    joined = []\n    for l in left_table:\n        k = l.get(join_key)\n        if k in lookup:\n            merged = dict(l)\n            merged.update(lookup[k])\n            joined.append(merged)\n    return joined\n',
                'explanation': 'Demonstrates hash join algorithm used by Pandas `pd.merge(how="inner")` and SQL engines.'
            }
        }

    # 9. EXPLORATORY DATA ANALYSIS (EDA), STATISTICS & VISUALIZATION
    if 'eda' in t_lower or 'visualization' in t_lower or 'seaborn' in t_lower or 'matplotlib' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Statistical Five-Number Summary',
                'function_name': 'five_number_summary',
                'prompt': 'Write a function `five_number_summary(data)` that takes a list of numbers and returns a dict with: `"min"`, `"max"`, `"mean"`, and `"variance"` (all rounded to 2 decimals).',
                'constraints': 'len(data) >= 2',
                'starter_code': 'def five_number_summary(data: list) -> dict:\n    # Return summary dict\n    pass\n',
                'test_cases': [
                    {'input': [[10, 20, 30, 40, 50]], 'expected': {'min': 10.0, 'max': 50.0, 'mean': 30.0, 'variance': 200.0}, 'desc': 'Summary for 10-50'}
                ],
                'hint': 'mean = sum(data)/N, variance = sum((x - mean)^2)/N.',
                'solution_code': 'def five_number_summary(data: list) -> dict:\n    n = len(data)\n    d_min = float(min(data))\n    d_max = float(max(data))\n    mean = sum(data) / n\n    var = sum((x - mean) ** 2 for x in data) / n\n    return {"min": round(d_min, 2), "max": round(d_max, 2), "mean": round(mean, 2), "variance": round(var, 2)}\n',
                'explanation': 'Foundational descriptive statistics for exploratory data profiling.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Interquartile Range (IQR) Outlier Detector',
                'function_name': 'detect_iqr_outliers',
                'prompt': 'Write a function `detect_iqr_outliers(data)` that identifies statistical outliers. Calculate median, Q1 (25th percentile) and Q3 (75th percentile). Any point `< Q1 - 1.5*IQR` or `> Q3 + 1.5*IQR` is an outlier. Return a list of all outlier values in sorted order.',
                'constraints': 'data contains numbers',
                'starter_code': 'def detect_iqr_outliers(data: list) -> list:\n    # Return list of outlier values\n    pass\n',
                'test_cases': [
                    {'input': [[1, 10, 12, 13, 14, 15, 16, 17, 18, 19, 100]], 'expected': [1, 100], 'desc': 'Detects extreme values 1 and 100 as outliers'}
                ],
                'hint': 'Sort data. Q1 is at index 0.25*N, Q3 is at index 0.75*N. IQR = Q3 - Q1.',
                'solution_code': 'def detect_iqr_outliers(data: list) -> list:\n    s = sorted(data)\n    n = len(s)\n    q1 = s[int(0.25 * n)]\n    q3 = s[int(0.75 * n)]\n    iqr = q3 - q1\n    lower = q1 - 1.5 * iqr\n    upper = q3 + 1.5 * iqr\n    return [x for x in s if x < lower or x > upper]\n',
                'explanation': 'The standard Tukey IQR method for boxplot whiskers and automated data cleaning.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Pearson Correlation Coefficient Calculator',
                'function_name': 'pearson_correlation',
                'prompt': 'Write a function `pearson_correlation(x, y)` that calculates the Pearson correlation coefficient between two equal-length numerical arrays `x` and `y`. Formula: `sum((x-mx)*(y-my)) / sqrt(sum((x-mx)^2) * sum((y-my)^2))`. Round to 4 decimals.',
                'constraints': 'len(x) == len(y) >= 2',
                'starter_code': 'def pearson_correlation(x: list, y: list) -> float:\n    # Return Pearson r rounded to 4 decimals\n    pass\n',
                'test_cases': [
                    {'input': [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10]], 'expected': 1.0, 'desc': 'Perfect positive linear correlation'},
                    {'input': [[1, 2, 3], [3, 2, 1]], 'expected': -1.0, 'desc': 'Perfect negative linear correlation'}
                ],
                'hint': 'Compute mean of x and y, then compute numerator covariance and denominator variances.',
                'solution_code': 'def pearson_correlation(x: list, y: list) -> float:\n    n = len(x)\n    mx = sum(x) / n\n    my = sum(y) / n\n    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))\n    den = (sum((xi - mx) ** 2 for xi in x) * sum((yi - my) ** 2 for yi in y)) ** 0.5\n    if den == 0: return 0.0\n    return round(num / den, 4)\n',
                'explanation': 'The fundamental metric used to generate Seaborn correlation heatmaps and identify multicollinearity.'
            }
        }

    # 10. MACHINE LEARNING & REGRESSION / CLASSIFICATION
    if 'supervised' in t_lower or 'regression' in t_lower or 'classification' in t_lower or 'tree' in t_lower or 'clustering' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Mean Squared Error (MSE) Calculator',
                'function_name': 'calculate_mse',
                'prompt': 'Write a function `calculate_mse(actual, predicted)` that calculates the Mean Squared Error: `sum((actual[i] - predicted[i])**2) / N`. Round to 2 decimals.',
                'constraints': 'Both lists have identical length >= 1',
                'starter_code': 'def calculate_mse(actual: list, predicted: list) -> float:\n    # Return MSE rounded to 2 decimals\n    pass\n',
                'test_cases': [
                    {'input': [[3, -0.5, 2, 7], [2.5, 0.0, 2, 8]], 'expected': 0.38, 'desc': 'MSE for 4 predictions = 0.38'},
                    {'input': [[1, 2, 3], [1, 2, 3]], 'expected': 0.0, 'desc': 'Perfect prediction MSE = 0.0'}
                ],
                'hint': 'Subtract predicted from actual, square each difference, sum, and divide by len(actual).',
                'solution_code': 'def calculate_mse(actual: list, predicted: list) -> float:\n    n = len(actual)\n    return round(sum((actual[i] - predicted[i]) ** 2 for i in range(n)) / n, 2)\n',
                'explanation': 'MSE is the standard loss function minimized in ordinary least squares linear regression.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Binary Classification Accuracy & F1-Score',
                'function_name': 'classification_metrics',
                'prompt': 'Write a function `classification_metrics(y_true, y_pred)` that returns a dictionary `{"accuracy": ..., "precision": ..., "recall": ...}` for binary classification (0 or 1). All metrics rounded to 2 decimals.',
                'constraints': 'y_true and y_pred contain 0s and 1s',
                'starter_code': 'def classification_metrics(y_true: list, y_pred: list) -> dict:\n    # Return dictionary with accuracy, precision, and recall\n    pass\n',
                'test_cases': [
                    {'input': [[1, 1, 0, 0, 1], [1, 0, 0, 0, 1]], 'expected': {'accuracy': 0.8, 'precision': 1.0, 'recall': 0.67}, 'desc': '4/5 correct accuracy, 2/2 precision, 2/3 recall'}
                ],
                'hint': 'Count TP (both 1), FP (pred 1, true 0), FN (pred 0, true 1), TN (both 0).',
                'solution_code': 'def classification_metrics(y_true: list, y_pred: list) -> dict:\n    n = len(y_true)\n    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)\n    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)\n    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)\n    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)\n    acc = round(correct / n, 2)\n    prec = round(tp / (tp + fp), 2) if (tp + fp) > 0 else 0.0\n    rec = round(tp / (tp + fn), 2) if (tp + fn) > 0 else 0.0\n    return {"accuracy": acc, "precision": prec, "recall": rec}\n',
                'explanation': 'Essential metric computation used to evaluate fraud detection and medical diagnosis models beyond simple accuracy.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Gini Impurity Split Evaluation',
                'function_name': 'calculate_gini_impurity',
                'prompt': 'Write a function `calculate_gini_impurity(labels)` that calculates the Gini Impurity for a classification split: `1 - sum(p_i ** 2)` where `p_i` is the probability of class `i`. Round result to 4 decimals.',
                'constraints': 'labels is a non-empty list of class identifiers',
                'starter_code': 'def calculate_gini_impurity(labels: list) -> float:\n    # Return Gini impurity rounded to 4 decimals\n    pass\n',
                'test_cases': [
                    {'input': [['A', 'A', 'A', 'A']], 'expected': 0.0, 'desc': 'Pure node has Gini = 0.0'},
                    {'input': [['A', 'A', 'B', 'B']], 'expected': 0.5, 'desc': '50/50 split has Gini = 0.5'}
                ],
                'hint': 'Count frequencies of each unique label. Compute p = count / N, then 1 - sum(p^2).',
                'solution_code': 'def calculate_gini_impurity(labels: list) -> float:\n    n = len(labels)\n    counts = {}\n    for l in labels:\n        counts[l] = counts.get(l, 0) + 1\n    gini = 1.0 - sum((c / n) ** 2 for c in counts.values())\n    return round(gini, 4)\n',
                'explanation': 'The core mathematical split criterion used in CART (Decision Trees) and Random Forests.'
            }
        }

    # 11. DEEP LEARNING & PYTORCH
    if 'neural' in t_lower or 'pytorch' in t_lower or 'cnn' in t_lower or 'activation' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'ReLU & Sigmoid Activations',
                'function_name': 'activate_neuron',
                'prompt': 'Write a function `activate_neuron(x, activation_type)` that implements activation functions: "relu" returns `max(0, x)`, while "sigmoid" returns `1 / (1 + math.exp(-x))` rounded to 4 decimals.',
                'constraints': 'activation_type in ["relu", "sigmoid"]',
                'starter_code': 'import math\n\ndef activate_neuron(x: float, activation_type: str) -> float:\n    # Return activated value\n    pass\n',
                'test_cases': [
                    {'input': [-5.0, 'relu'], 'expected': 0.0, 'desc': 'ReLU on negative is 0.0'},
                    {'input': [3.5, 'relu'], 'expected': 3.5, 'desc': 'ReLU on positive passes through'},
                    {'input': [0.0, 'sigmoid'], 'expected': 0.5, 'desc': 'Sigmoid at 0 is 0.5'}
                ],
                'hint': 'Import math. For relu use max(0.0, float(x)). For sigmoid use 1 / (1 + math.exp(-x)).',
                'solution_code': 'import math\ndef activate_neuron(x: float, activation_type: str) -> float:\n    if activation_type.lower() == "relu":\n        return max(0.0, float(x))\n    elif activation_type.lower() == "sigmoid":\n        return round(1.0 / (1.0 + math.exp(-x)), 4)\n    return float(x)\n',
                'explanation': 'Activations introduce non-linearity, enabling deep networks to approximate arbitrary continuous functions.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Softmax Probability Distribution',
                'function_name': 'softmax',
                'prompt': 'Write a function `softmax(logits)` that converts a list of unnormalized log-probability floats into a valid probability distribution where all elements sum to 1.0. Round each probability to 4 decimals.',
                'constraints': 'Non-empty list of floats',
                'starter_code': 'import math\n\ndef softmax(logits: list) -> list:\n    # Return softmax probabilities\n    pass\n',
                'test_cases': [
                    {'input': [[2.0, 1.0, 0.1]], 'expected': [0.6590, 0.2424, 0.0986], 'desc': 'Expands and normalizes logits'}
                ],
                'hint': 'Subtract max(logits) for numerical stability, exponentiate with math.exp, then divide by sum.',
                'solution_code': 'import math\ndef softmax(logits: list) -> list:\n    max_val = max(logits)\n    exps = [math.exp(x - max_val) for x in logits]\n    sum_exps = sum(exps)\n    return [round(e / sum_exps, 4) for e in exps]\n',
                'explanation': 'The standard output layer activation for multi-class classification and LLM next-token probability prediction.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Scaled Dot-Product Self-Attention Score',
                'function_name': 'self_attention_score',
                'prompt': 'Write a function `self_attention_score(query, key, d_k)` that computes the scaled dot-product attention score `dot(query, key) / sqrt(d_k)`. Round to 4 decimals.',
                'constraints': 'query and key are equal-length lists of floats, d_k > 0',
                'starter_code': 'import math\n\ndef self_attention_score(query: list, key: list, d_k: int) -> float:\n    # Return scaled attention score\n    pass\n',
                'test_cases': [
                    {'input': [[1.0, 2.0, 3.0], [2.0, 0.0, 1.0], 64], 'expected': 0.625, 'desc': 'dot product is 5.0, divided by sqrt(64)=8 -> 0.625'}
                ],
                'hint': 'Calculate dot product = sum(q * k for q, k in zip(query, key)), then divide by (d_k ** 0.5).',
                'solution_code': 'def self_attention_score(query: list, key: list, d_k: int) -> float:\n    dot = sum(q * k for q, k in zip(query, key))\n    return round(dot / (d_k ** 0.5), 4)\n',
                'explanation': 'The fundamental math equation of the Transformer architecture powering GPT, BERT, and modern LLMs.'
            }
        }

    # 12. GENERATIVE AI, LLMS & RAG
    if 'gpt' in t_lower or 'llm' in t_lower or 'rag' in t_lower or 'langchain' in t_lower or 'token' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'LLM Token Usage & API Cost Calculator',
                'function_name': 'estimate_llm_cost',
                'prompt': 'Write a function `estimate_llm_cost(prompt_tokens, completion_tokens, input_cost_per_1k, output_cost_per_1k)` that calculates the total API request cost rounded to 6 decimal places.',
                'constraints': 'All inputs >= 0',
                'starter_code': 'def estimate_llm_cost(prompt_tokens: int, completion_tokens: int, input_cost_per_1k: float, output_cost_per_1k: float) -> float:\n    # Return total API cost\n    pass\n',
                'test_cases': [
                    {'input': [1500, 500, 0.0015, 0.002], 'expected': 0.00325, 'desc': '(1.5 * 0.0015) + (0.5 * 0.002) = 0.00325'}
                ],
                'hint': 'Divide prompt_tokens by 1000 and multiply by input cost, then add output cost.',
                'solution_code': 'def estimate_llm_cost(prompt_tokens: int, completion_tokens: int, input_cost_per_1k: float, output_cost_per_1k: float) -> float:\n    cost = (prompt_tokens / 1000.0 * input_cost_per_1k) + (completion_tokens / 1000.0 * output_cost_per_1k)\n    return round(cost, 6)\n',
                'explanation': 'Critical cost accounting when deploying LLM agent workflows and RAG pipelines at scale.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Cosine Similarity Semantic Matcher',
                'function_name': 'find_closest_embedding',
                'prompt': 'Write a function `find_closest_embedding(query_vec, doc_vectors)` that returns the index of the document vector with the highest cosine similarity to `query_vec`. Cosine similarity = `dot(u, v) / (norm(u) * norm(v))`.',
                'constraints': 'All vectors are equal length floats',
                'starter_code': 'def find_closest_embedding(query_vec: list, doc_vectors: list) -> int:\n    # Return index of best matching document vector\n    pass\n',
                'test_cases': [
                    {'input': [[1, 0], [[0, 1], [0.9, 0.1], [-1, 0]]], 'expected': 1, 'desc': '[0.9, 0.1] has highest similarity to [1, 0]'}
                ],
                'hint': 'Compute cosine similarity for each document and track max value index.',
                'solution_code': 'def find_closest_embedding(query_vec: list, doc_vectors: list) -> int:\n    def cosine_sim(a, b):\n        dot = sum(x * y for x, y in zip(a, b))\n        norm_a = sum(x ** 2 for x in a) ** 0.5\n        norm_b = sum(x ** 2 for x in b) ** 0.5\n        if norm_a == 0 or norm_b == 0: return 0.0\n        return dot / (norm_a * norm_b)\n    sims = [cosine_sim(query_vec, doc) for doc in doc_vectors]\n    return sims.index(max(sims))\n',
                'explanation': 'The core mathematical engine of Vector Databases (Chroma, Pinecone) during semantic RAG retrieval.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Recursive Character Document Chunker',
                'function_name': 'chunk_document',
                'prompt': 'Write a function `chunk_document(text, chunk_size, chunk_overlap)` that splits a document string into overlapping chunks. Each chunk has length `chunk_size` and advances by `chunk_size - chunk_overlap`. The last chunk should capture remaining characters.',
                'constraints': 'chunk_size > chunk_overlap > 0',
                'starter_code': 'def chunk_document(text: str, chunk_size: int, chunk_overlap: int) -> list:\n    # Return list of text chunks\n    pass\n',
                'test_cases': [
                    {'input': ['abcdefghijklmnop', 6, 2], 'expected': ['abcdef', 'efghij', 'ijklmn', 'mnop'], 'desc': 'Overlaps 2 characters between adjacent chunks'}
                ],
                'hint': 'Step size is chunk_size - chunk_overlap. Loop with while index < len(text).',
                'solution_code': 'def chunk_document(text: str, chunk_size: int, chunk_overlap: int) -> list:\n    chunks = []\n    step = chunk_size - chunk_overlap\n    i = 0\n    while i < len(text):\n        chunk = text[i:i + chunk_size]\n        chunks.append(chunk)\n        if i + chunk_size >= len(text):\n            break\n        i += step\n    return chunks\n',
                'explanation': 'Replicates the LangChain RecursiveCharacterTextSplitter used to ingest enterprise PDFs into vector stores.'
            }
        }

    # 13. DATA STRUCTURES & ALGORITHMS (STACKS, QUEUES, TREES, GRAPHS)
    if 'stack' in t_lower or 'queue' in t_lower or 'tree' in t_lower or 'graph' in t_lower or 'complexity' in t_lower:
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'title': 'Valid Parentheses Bracket Validator',
                'function_name': 'is_valid_parentheses',
                'prompt': 'Write a Python function `is_valid_parentheses(s)` using a stack that returns `True` if all brackets in the string `s` are properly matched and closed in correct order: `()`, `{}`, and `[]`. Return `False` otherwise.',
                'constraints': 's contains bracket characters',
                'starter_code': 'def is_valid_parentheses(s: str) -> bool:\n    # Return True if brackets are balanced\n    pass\n',
                'test_cases': [
                    {'input': ['()[]{}'], 'expected': True, 'desc': 'Valid sequential pairs'},
                    {'input': ['([{}])'], 'expected': True, 'desc': 'Valid nested brackets'},
                    {'input': ['(]'], 'expected': False, 'desc': 'Mismatched closing bracket'},
                    {'input': ['['], 'expected': False, 'desc': 'Unclosed opening bracket'}
                ],
                'hint': 'Push opening brackets onto a list stack. On closing bracket, pop and verify it matches.',
                'solution_code': 'def is_valid_parentheses(s: str) -> bool:\n    stack = []\n    pairs = {")": "(", "}": "{", "]": "["}\n    for char in s:\n        if char in pairs.values():\n            stack.append(char)\n        elif char in pairs:\n            if not stack or stack.pop() != pairs[char]:\n                return False\n    return len(stack) == 0\n',
                'explanation': 'The classic LeetCode stack problem testing LIFO order validation in compilers and parsers.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'title': 'Binary Search & Step Counter',
                'function_name': 'binary_search_with_steps',
                'prompt': 'Write a function `binary_search_with_steps(sorted_nums, target)` that finds `target` in a sorted list. Return a dict `{"found": bool, "index": int, "steps": int}` where `index` is the position of target (or -1 if not found), and `steps` is the number of while loop iterations.',
                'constraints': 'sorted_nums is sorted ascending',
                'starter_code': 'def binary_search_with_steps(sorted_nums: list, target: int) -> dict:\n    # Return {"found": bool, "index": int, "steps": int}\n    pass\n',
                'test_cases': [
                    {'input': [[1, 3, 5, 7, 9, 11, 13], 7], 'expected': {'found': True, 'index': 3, 'steps': 1}, 'desc': 'Finds 7 on first midpoint step'},
                    {'input': [[1, 3, 5, 7, 9, 11, 13], 2], 'expected': {'found': False, 'index': -1, 'steps': 3}, 'desc': 'Target 2 not found in 3 steps'}
                ],
                'hint': 'low = 0, high = len - 1. While low <= high, mid = (low + high) // 2.',
                'solution_code': 'def binary_search_with_steps(sorted_nums: list, target: int) -> dict:\n    low, high = 0, len(sorted_nums) - 1\n    steps = 0\n    while low <= high:\n        steps += 1\n        mid = (low + high) // 2\n        if sorted_nums[mid] == target:\n            return {"found": True, "index": mid, "steps": steps}\n        elif sorted_nums[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return {"found": False, "index": -1, "steps": steps}\n',
                'explanation': 'Demonstrates O(log N) divide-and-conquer search mechanics.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'title': 'Breadth-First Search (BFS) Shortest Path on Graph',
                'function_name': 'bfs_shortest_path_length',
                'prompt': 'Write a function `bfs_shortest_path_length(graph, start, goal)` that computes the minimum edge distance from `start` to `goal` in an unweighted graph represented as an adjacency list dictionary: `{"A": ["B", "C"], "B": ["D"]}`. Return the integer distance (or -1 if unreachable).',
                'constraints': 'All nodes are strings',
                'starter_code': 'def bfs_shortest_path_length(graph: dict, start: str, goal: str) -> int:\n    # Return shortest distance as int\n    pass\n',
                'test_cases': [
                    {'input': [{'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', 'D'], 'expected': 2, 'desc': 'A -> B -> D is 2 edges'},
                    {'input': [{'A': ['B'], 'B': [], 'C': []}, 'A', 'C'], 'expected': -1, 'desc': 'C is unreachable from A'}
                ],
                'hint': 'Use a queue storing (node, distance). Keep a visited set to avoid cycles.',
                'solution_code': 'def bfs_shortest_path_length(graph: dict, start: str, goal: str) -> int:\n    if start == goal: return 0\n    queue = [(start, 0)]\n    visited = {start}\n    while queue:\n        curr, dist = queue.pop(0)\n        for neighbor in graph.get(curr, []):\n            if neighbor == goal:\n                return dist + 1\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append((neighbor, dist + 1))\n    return -1\n',
                'explanation': 'BFS explores nodes layer by layer, guaranteeing the shortest path in unweighted graphs.'
            }
        }

    # 14. DATABASES, SQL, ERD & RELATIONAL SCHEMA MODELING
    clean_name = full_title.split(':')[-1].strip()
    if any(k in t_lower or k in c_lower for k in ['erd', 'schema', 'relational', 'sql', 'database', 'foreign key', 'normalization', 'table', 'query', 'postgres', 'mysql', 'sqlite', 'acid', 'transaction']):
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'approach': 'function',
                'title': f'{clean_name} - Relational Schema Field Validator',
                'function_name': 'validate_schema_field',
                'prompt': (
                    f'Write a Python function `validate_schema_field(field_name: str, field_type: str, constraints: list) -> bool` '
                    f'for {clean_name}. It returns True if:\n'
                    f'1. `field_name` is non-empty and contains only lower_case letters and underscores (`^[a-z_][a-z0-9_]*$`).\n'
                    f'2. `field_type` is one of `["VARCHAR", "INT", "FLOAT", "BOOLEAN", "TEXT", "TIMESTAMP"]` (case-insensitive).\n'
                    f'3. All items in `constraints` belong to `["PRIMARY KEY", "FOREIGN KEY", "NOT NULL", "UNIQUE", "DEFAULT"]` (case-insensitive).\n'
                    f'Otherwise return False.'
                ),
                'constraints': 'field_name and field_type are strings',
                'starter_code': (
                    "def validate_schema_field(field_name: str, field_type: str, constraints: list) -> bool:\n"
                    "    \"\"\"Validate SQL column identifier, type token, and integrity constraints.\"\"\"\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {'input': ['user_id', 'INT', ['PRIMARY KEY', 'NOT NULL']], 'expected': True, 'desc': 'Valid primary key field'},
                    {'input': ['User-Name', 'VARCHAR', ['NOT NULL']], 'expected': False, 'desc': 'Invalid field name casing/hyphen'},
                    {'input': ['created_at', 'INVALID_TYPE', []], 'expected': False, 'desc': 'Unrecognized SQL data type'}
                ],
                'hint': 'Check regex / valid chars on field_name, uppercase field_type in allowed set, and all(c.upper() in allowed for c in constraints).',
                'solution_code': (
                    "def validate_schema_field(field_name: str, field_type: str, constraints: list) -> bool:\n"
                    "    if not field_name or not (field_name[0].isalpha() or field_name[0] == '_'):\n"
                    "        return False\n"
                    "    for ch in field_name:\n"
                    "        if not (ch.islower() or ch.isdigit() or ch == '_'):\n"
                    "            return False\n"
                    "    valid_types = {'VARCHAR', 'INT', 'FLOAT', 'BOOLEAN', 'TEXT', 'TIMESTAMP'}\n"
                    "    if field_type.upper() not in valid_types:\n"
                    "        return False\n"
                    "    valid_constraints = {'PRIMARY KEY', 'FOREIGN KEY', 'NOT NULL', 'UNIQUE', 'DEFAULT'}\n"
                    "    return all(c.upper() in valid_constraints for c in constraints)\n"
                ),
                'explanation': f'Ensures database schema definitions strictly adhere to relational integrity and naming conventions for {clean_name}.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'approach': 'function',
                'title': f'{clean_name} - Foreign Key Referential Integrity Checker',
                'function_name': 'check_referential_integrity',
                'prompt': (
                    f'Write a Python function `check_referential_integrity(primary_keys: list, foreign_keys: list) -> dict` '
                    f'for {clean_name}. Given a list of existing primary key IDs in a parent table and foreign key IDs in a child table, '
                    f'determine whether all foreign keys refer to valid parent records. Return a dictionary:\n'
                    f'`{{"valid": bool, "orphaned_keys": list, "orphan_count": int}}` where `orphaned_keys` contains unique invalid foreign keys sorted in ascending order.'
                ),
                'constraints': 'primary_keys and foreign_keys are lists of integers or strings',
                'starter_code': (
                    "def check_referential_integrity(primary_keys: list, foreign_keys: list) -> dict:\n"
                    "    \"\"\"Verify that every foreign key exists in the parent primary key set.\"\"\"\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {'input': [[1, 2, 3, 4], [1, 2, 2, 3]], 'expected': {'valid': True, 'orphaned_keys': [], 'orphan_count': 0}, 'desc': 'All foreign keys match parent records'},
                    {'input': [[10, 20], [10, 30, 40, 30]], 'expected': {'valid': False, 'orphaned_keys': [30, 40], 'orphan_count': 2}, 'desc': 'Detects orphaned foreign keys 30 and 40'}
                ],
                'hint': 'Convert primary_keys to a set, find unique foreign_keys not in the set, and sort them.',
                'solution_code': (
                    "def check_referential_integrity(primary_keys: list, foreign_keys: list) -> dict:\n"
                    "    pk_set = set(primary_keys)\n"
                    "    orphans = sorted(list(set(k for k in foreign_keys if k not in pk_set)))\n"
                    "    return {'valid': len(orphans) == 0, 'orphaned_keys': orphans, 'orphan_count': len(orphans)}\n"
                ),
                'explanation': f'Referential integrity enforcement is a core tenet of the Relational Model in {clean_name}.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'approach': 'function',
                'title': f'{clean_name} - Relational Inner & Left Join Processor',
                'function_name': 'execute_relational_join',
                'prompt': (
                    f'Write a Python function `execute_relational_join(table_a: list, table_b: list, join_key: str, how: str = "inner") -> list` '
                    f'for {clean_name}. Each table is a list of dictionary rows.\n'
                    f'- For "inner" join: combine rows matching `join_key`.\n'
                    f'- For "left" join: include all rows from `table_a`; if no match in `table_b`, set missing columns from `table_b` to None.\n'
                    f'Return list of joined dictionaries sorted by `join_key` ascending.'
                ),
                'constraints': 'how is "inner" or "left"',
                'starter_code': (
                    "def execute_relational_join(table_a: list, table_b: list, join_key: str, how: str = 'inner') -> list:\n"
                    "    \"\"\"Perform relational inner or left join between two table datasets.\"\"\"\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {
                        'input': [
                            [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],
                            [{'id': 1, 'dept': 'Eng'}, {'id': 3, 'dept': 'HR'}],
                            'id',
                            'inner'
                        ],
                        'expected': [{'id': 1, 'name': 'Alice', 'dept': 'Eng'}],
                        'desc': 'Inner join on id=1'
                    },
                    {
                        'input': [
                            [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],
                            [{'id': 1, 'dept': 'Eng'}],
                            'id',
                            'left'
                        ],
                        'expected': [{'id': 1, 'name': 'Alice', 'dept': 'Eng'}, {'id': 2, 'name': 'Bob', 'dept': None}],
                        'desc': 'Left join preserves Bob with dept=None'
                    }
                ],
                'hint': 'Build a hash map of table_b keyed by join_key. Iterate table_a, lookup matching row, merge dicts.',
                'solution_code': (
                    "def execute_relational_join(table_a: list, table_b: list, join_key: str, how: str = 'inner') -> list:\n"
                    "    b_cols = set().union(*(r.keys() for r in table_b)) if table_b else set()\n"
                    "    b_map = {r[join_key]: r for r in table_b if join_key in r}\n"
                    "    res = []\n"
                    "    for a in table_a:\n"
                    "        k = a.get(join_key)\n"
                    "        if k in b_map:\n"
                    "            merged = {**a, **b_map[k]}\n"
                    "            res.append(merged)\n"
                    "        elif how == 'left':\n"
                    "            null_b = {col: None for col in b_cols if col != join_key}\n"
                    "            res.append({**a, **null_b})\n"
                    "    return sorted(res, key=lambda x: str(x.get(join_key, '')))\n"
                ),
                'explanation': f'Relational algebra implementation simulating SQL projection and joins for {clean_name}.'
            }
        }

    # 15. UI/UX DESIGN SYSTEMS, FIGMA & FRONTEND ARCHITECTURE
    if any(k in t_lower or k in c_lower for k in ['ui/ux', 'design', 'figma', 'prototype', 'css', 'layout', 'flexbox', 'grid', 'typography', 'component', 'wireframe', 'responsive', 'animation', 'style']):
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'approach': 'function',
                'title': f'{clean_name} - Design Token Hex Color Validator',
                'function_name': 'validate_design_token',
                'prompt': (
                    f'Write a Python function `validate_design_token(token_name: str, hex_value: str) -> dict` for {clean_name}. '
                    f'It checks if `token_name` starts with "color-" and `hex_value` is a valid 6-character hex code starting with "#" (e.g., "#2563EB"). '
                    f'Return `{{"valid": True, "token": token_name, "hex": hex_value.upper()}}` if valid, or `{{"valid": False, "error": "Invalid token or hex"}}`.'
                ),
                'constraints': 'token_name and hex_value are strings',
                'starter_code': (
                    "def validate_design_token(token_name: str, hex_value: str) -> dict:\n"
                    "    \"\"\"Validate design system color token and hex format.\"\"\"\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {'input': ['color-primary', '#2563eb'], 'expected': {'valid': True, 'token': 'color-primary', 'hex': '#2563EB'}, 'desc': 'Valid primary token'},
                    {'input': ['button-bg', '#fff'], 'expected': {'valid': False, 'error': 'Invalid token or hex'}, 'desc': 'Token does not start with color- or hex not 6 chars'}
                ],
                'hint': 'Check token_name.startswith("color-") and len(hex_value) == 7 and hex_value.startswith("#") and valid hex digits.',
                'solution_code': (
                    "def validate_design_token(token_name: str, hex_value: str) -> dict:\n"
                    "    if token_name.startswith('color-') and len(hex_value) == 7 and hex_value[0] == '#':\n"
                    "        if all(c in '0123456789abcdefABCDEF' for c in hex_value[1:]):\n"
                    "            return {'valid': True, 'token': token_name, 'hex': hex_value.upper()}\n"
                    "    return {'valid': False, 'error': 'Invalid token or hex'}\n"
                ),
                'explanation': f'Ensures strict adherence to design system design tokens in {clean_name}.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'approach': 'function',
                'title': f'{clean_name} - Flexbox Layout Justify Space Calculator',
                'function_name': 'calculate_flexbox_spacing',
                'prompt': (
                    f'Write a Python function `calculate_flexbox_spacing(container_width: float, item_widths: list, justify: str) -> list` '
                    f'for {clean_name}. It computes the left X position of each item in a container. Support:\n'
                    f'- "flex-start": items placed adjacent with 0 gap.\n'
                    f'- "space-between": first at 0, last at `container_width - item_widths[-1]`, remaining space divided evenly.\n'
                    f'Return list of X offsets rounded to 2 decimal places.'
                ),
                'constraints': 'len(item_widths) >= 2',
                'starter_code': (
                    "def calculate_flexbox_spacing(container_width: float, item_widths: list, justify: str) -> list:\n"
                    "    \"\"\"Calculate item X coordinates according to CSS Flexbox justify-content rule.\"\"\"\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {'input': [300.0, [50.0, 50.0], 'flex-start'], 'expected': [0.0, 50.0], 'desc': 'flex-start packed at left'},
                    {'input': [300.0, [50.0, 50.0, 50.0], 'space-between'], 'expected': [0.0, 125.0, 250.0], 'desc': 'space-between with 75px gaps'}
                ],
                'hint': 'Calculate free_space = container_width - sum(item_widths). For space-between, gap = free_space / (len - 1).',
                'solution_code': (
                    "def calculate_flexbox_spacing(container_width: float, item_widths: list, justify: str) -> list:\n"
                    "    if justify == 'flex-start':\n"
                    "        x, res = 0.0, []\n"
                    "        for w in item_widths:\n"
                    "            res.append(round(x, 2))\n"
                    "            x += w\n"
                    "        return res\n"
                    "    elif justify == 'space-between':\n"
                    "        n = len(item_widths)\n"
                    "        if n <= 1: return [0.0]\n"
                    "        gap = (container_width - sum(item_widths)) / (n - 1)\n"
                    "        x, res = 0.0, []\n"
                    "        for w in item_widths:\n"
                    "            res.append(round(x, 2))\n"
                    "            x += w + gap\n"
                    "        return res\n"
                    "    return []\n"
                ),
                'explanation': f'Replicates CSS Flexbox coordinate distribution model in {clean_name}.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'approach': 'function',
                'title': f'{clean_name} - Component Tree Flattener & Depth Indexer',
                'function_name': 'flatten_component_tree',
                'prompt': (
                    f'Write a Python function `flatten_component_tree(root_node: dict) -> list` for {clean_name}. '
                    f'Given a nested component hierarchy `{{"name": "App", "type": "frame", "children": [...]}}`: '
                    f'perform a preorder traversal and return a list of dicts `[{{"name": str, "type": str, "depth": int}}]`.'
                ),
                'constraints': 'root_node is a dictionary with keys name, type, and optional children list',
                'starter_code': (
                    "def flatten_component_tree(root_node: dict) -> list:\n"
                    "    \"\"\"Flatten nested Figma/DOM component hierarchy into indexed traversal list.\"\"\"\n"
                    "    pass\n"
                ),
                'test_cases': [
                    {
                        'input': [{'name': 'App', 'type': 'frame', 'children': [{'name': 'Navbar', 'type': 'component'}, {'name': 'Card', 'type': 'frame', 'children': [{'name': 'Button', 'type': 'component'}]}]}],
                        'expected': [
                            {'name': 'App', 'type': 'frame', 'depth': 0},
                            {'name': 'Navbar', 'type': 'component', 'depth': 1},
                            {'name': 'Card', 'type': 'frame', 'depth': 1},
                            {'name': 'Button', 'type': 'component', 'depth': 2}
                        ],
                        'desc': 'Nested traversal of App component hierarchy'
                    }
                ],
                'hint': 'Use a recursive helper or stack passing (node, depth). Append node details, then recurse on children.',
                'solution_code': (
                    "def flatten_component_tree(root_node: dict) -> list:\n"
                    "    res = []\n"
                    "    def dfs(node, depth):\n"
                    "        if not node: return\n"
                    "        res.append({'name': node.get('name', ''), 'type': node.get('type', ''), 'depth': depth})\n"
                    "        for child in node.get('children', []):\n"
                    "            dfs(child, depth + 1)\n"
                    "    dfs(root_node, 0)\n"
                    "    return res\n"
                ),
                'explanation': f'Component trees model Figma frames and React component hierarchies in {clean_name}.'
            }
        }

    # 16. RESTFUL APIS, HTTP PROTOCOLS & WEB SERVICES
    if any(k in t_lower or k in c_lower for k in ['api', 'rest', 'http', 'endpoint', 'webhook', 'json', 'jwt', 'auth', 'microservice']):
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'approach': 'function',
                'title': f'{clean_name} - HTTP Standard Response Envelope Formatter',
                'function_name': 'format_api_response',
                'prompt': f'Write a Python function `format_api_response(status_code: int, data: any, message: str = "") -> dict` for {clean_name}. Returns `{{"status": "success" if 200 <= status_code < 300 else "error", "code": status_code, "data": data, "message": message}}`.',
                'constraints': '100 <= status_code <= 599',
                'starter_code': "def format_api_response(status_code: int, data: any, message: str = '') -> dict:\n    pass\n",
                'test_cases': [
                    {'input': [200, {'id': 1}, 'OK'], 'expected': {'status': 'success', 'code': 200, 'data': {'id': 1}, 'message': 'OK'}, 'desc': '200 Success'},
                    {'input': [404, None, 'Not Found'], 'expected': {'status': 'error', 'code': 404, 'data': None, 'message': 'Not Found'}, 'desc': '404 Error'}
                ],
                'hint': 'Check if 200 <= status_code < 300 to choose success vs error string.',
                'solution_code': "def format_api_response(status_code: int, data: any, message: str = '') -> dict:\n    status = 'success' if 200 <= status_code < 300 else 'error'\n    return {'status': status, 'code': status_code, 'data': data, 'message': message}\n",
                'explanation': f'Standardized REST envelope architecture for {clean_name}.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'approach': 'function',
                'title': f'{clean_name} - URL Route Parameter Extractor',
                'function_name': 'parse_url_params',
                'prompt': f'Write `parse_url_params(template: str, path: str) -> dict` for {clean_name}. Template has `:param` tokens like `/users/:id/posts/:post_id`. Extract matches into a dictionary with integer values parsed to int.',
                'constraints': 'Same segment length',
                'starter_code': "def parse_url_params(template: str, path: str) -> dict:\n    pass\n",
                'test_cases': [
                    {'input': ['/users/:id/posts/:post_id', '/users/42/posts/100'], 'expected': {'id': 42, 'post_id': 100}, 'desc': 'Extracts :id and :post_id as ints'},
                    {'input': ['/items/:name', '/items/laptop'], 'expected': {'name': 'laptop'}, 'desc': 'Extracts string parameter'}
                ],
                'hint': 'Split paths by "/". If template part starts with ":", extract key, check .isdigit() to cast.',
                'solution_code': "def parse_url_params(template: str, path: str) -> dict:\n    t_parts = template.strip('/').split('/')\n    p_parts = path.strip('/').split('/')\n    res = {}\n    for t, p in zip(t_parts, p_parts):\n        if t.startswith(':'):\n            k = t[1:]\n            res[k] = int(p) if p.isdigit() else p\n    return res\n",
                'explanation': f'URL routing parameter compiler for {clean_name}.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'approach': 'function',
                'title': f'{clean_name} - Token Bucket Rate Limiter Simulator',
                'function_name': 'simulate_rate_limiter',
                'prompt': f'Write `simulate_rate_limiter(requests_timestamps: list, max_capacity: int, refill_rate_per_sec: float) -> list` for {clean_name}. Given timestamps in seconds, evaluate each request: return list of booleans indicating if request is accepted or rejected (429).',
                'constraints': 'requests_timestamps is sorted ascending',
                'starter_code': "def simulate_rate_limiter(requests_timestamps: list, max_capacity: int, refill_rate_per_sec: float) -> list:\n    pass\n",
                'test_cases': [
                    {'input': [[0.0, 0.1, 0.2, 0.3], 2, 1.0], 'expected': [True, True, False, False], 'desc': 'First 2 pass, next 2 rejected'}
                ],
                'hint': 'Track current tokens (starts at max_capacity) and last_time. For each req, tokens = min(capacity, tokens + delta * rate). If >= 1, consume and True, else False.',
                'solution_code': "def simulate_rate_limiter(requests_timestamps: list, max_capacity: int, refill_rate_per_sec: float) -> list:\n    tokens = float(max_capacity)\n    last_time = requests_timestamps[0] if requests_timestamps else 0.0\n    res = []\n    for t in requests_timestamps:\n        delta = max(0.0, t - last_time)\n        tokens = min(float(max_capacity), tokens + delta * refill_rate_per_sec)\n        last_time = t\n        if tokens >= 1.0:\n            tokens -= 1.0\n            res.append(True)\n        else:\n            res.append(False)\n    return res\n",
                'explanation': f'Essential DDoS and API throttling rate-limiter pattern for {clean_name}.'
            }
        }

    # 17. PROMPT ENGINEERING, LLMS & GENERATIVE AI WORKFLOWS
    if any(k in t_lower or k in c_lower for k in ['prompt', 'llm', 'generative', 'langchain', 'embedding', 'rag', 'agent', 'token', 'chatgpt', 'openai', 'gemini']):
        return {
            'basic': {
                'id': f'l{lesson_id}-b',
                'difficulty': 'Basic',
                'badge_class': 'bg-success',
                'approach': 'function',
                'title': f'{clean_name} - Prompt Template Variable Interpolator',
                'function_name': 'interpolate_prompt',
                'prompt': f'Write `interpolate_prompt(template_str: str, variables: dict) -> str` for {clean_name}. Replaces each `{{key}}` in template with its value from `variables`. If a variable is missing, replace with `[MISSING]`.',
                'constraints': 'template_str is string, variables is dict',
                'starter_code': "def interpolate_prompt(template_str: str, variables: dict) -> str:\n    pass\n",
                'test_cases': [
                    {'input': ['Hello {{name}}, welcome to {{topic}}!', {'name': 'Alice', 'topic': 'AI'}], 'expected': 'Hello Alice, welcome to AI!', 'desc': 'Valid interpolation'},
                    {'input': ['Act as {{role}} in {{domain}}', {'role': 'Expert'}], 'expected': 'Act as Expert in [MISSING]', 'desc': 'Missing variable replacement'}
                ],
                'hint': 'Use re.sub(r"\\{\\{(\\w+)\\}\\}", ...) to lookup in variables dictionary.',
                'solution_code': "def interpolate_prompt(template_str: str, variables: dict) -> str:\n    res = template_str\n    while '{{' in res and '}}' in res:\n        i = res.find('{{')\n        j = res.find('}}', i)\n        if j == -1: break\n        k = res[i+2:j]\n        res = res[:i] + str(variables.get(k, '[MISSING]')) + res[j+2:]\n    return res\n",
                'explanation': f'Foundation of structured prompt templating engines for {clean_name}.'
            },
            'intermediate': {
                'id': f'l{lesson_id}-i',
                'difficulty': 'Intermediate',
                'badge_class': 'bg-primary',
                'approach': 'function',
                'title': f'{clean_name} - Cosine Similarity Vector Matcher',
                'function_name': 'cosine_similarity',
                'prompt': f'Write `cosine_similarity(vec_a: list, vec_b: list) -> float` for {clean_name}. Compute dot(a, b) / (norm(a) * norm(b)). Round to 4 decimal places. If norms are 0, return 0.0.',
                'constraints': 'vec_a and vec_b have equal length',
                'starter_code': "def cosine_similarity(vec_a: list, vec_b: list) -> float:\n    pass\n",
                'test_cases': [
                    {'input': [[1.0, 0.0], [0.0, 1.0]], 'expected': 0.0, 'desc': 'Orthogonal vectors'},
                    {'input': [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], 'expected': 1.0, 'desc': 'Identical vectors'}
                ],
                'hint': 'Calculate dot product and math.sqrt(sum(x**2)) for each vector.',
                'solution_code': "import math\ndef cosine_similarity(vec_a: list, vec_b: list) -> float:\n    dot = sum(a * b for a, b in zip(vec_a, vec_b))\n    norm_a = math.sqrt(sum(a * a for a in vec_a))\n    norm_b = math.sqrt(sum(b * b for b in vec_b))\n    if norm_a == 0 or norm_b == 0: return 0.0\n    return round(dot / (norm_a * norm_b), 4)\n",
                'explanation': f'Semantic vector comparison algorithm used in RAG and embedding stores for {clean_name}.'
            },
            'advance': {
                'id': f'l{lesson_id}-a',
                'difficulty': 'Advance',
                'badge_class': 'bg-purple',
                'approach': 'function',
                'title': f'{clean_name} - RAG Document Chunk Retriever (Top-K)',
                'function_name': 'retrieve_top_k_chunks',
                'prompt': f'Write `retrieve_top_k_chunks(query_vec: list, chunks: list, k: int = 2) -> list` for {clean_name}. `chunks` is list of `{{"id": int, "text": str, "vector": list}}`. Compute cosine similarity with query_vec and return top `k` chunks sorted by score descending, formatted as `{{"id": id, "text": text, "score": float}}`.',
                'constraints': 'k >= 1',
                'starter_code': "def retrieve_top_k_chunks(query_vec: list, chunks: list, k: int = 2) -> list:\n    pass\n",
                'test_cases': [
                    {
                        'input': [
                            [1.0, 0.0],
                            [
                                {'id': 1, 'text': 'Intro to LLM', 'vector': [0.9, 0.1]},
                                {'id': 2, 'text': 'Unrelated topic', 'vector': [0.0, 1.0]},
                                {'id': 3, 'text': 'Neural networks', 'vector': [0.8, 0.2]}
                            ],
                            2
                        ],
                        'expected': [
                            {'id': 1, 'text': 'Intro to LLM', 'score': 0.9939},
                            {'id': 3, 'text': 'Neural networks', 'score': 0.9701}
                        ],
                        'desc': 'Returns top 2 nearest chunks'
                    }
                ],
                'hint': 'Calculate cosine similarity for each chunk, sort by score descending, slice [:k].',
                'solution_code': (
                    "import math\n"
                    "def retrieve_top_k_chunks(query_vec: list, chunks: list, k: int = 2) -> list:\n"
                    "    def sim(a, b):\n"
                    "        dot = sum(x * y for x, y in zip(a, b))\n"
                    "        na = math.sqrt(sum(x * x for x in a))\n"
                    "        nb = math.sqrt(sum(y * y for y in b))\n"
                    "        return round(dot / (na * nb), 4) if na and nb else 0.0\n"
                    "    scored = [{'id': c['id'], 'text': c['text'], 'score': sim(query_vec, c['vector'])} for c in chunks]\n"
                    "    scored.sort(key=lambda x: x['score'], reverse=True)\n"
                    "    return scored[:k]\n"
                ),
                'explanation': f'Vector similarity search algorithm powering modern RAG architectures in {clean_name}.'
            }
        }

    # 18. DYNAMIC DOMAIN-ALIGNED GENERATOR (Tailored to Topic Title)
    clean_name = full_title.split(':')[-1].strip()
    safe_func = re.sub(r'[^a-zA-Z0-9_]', '_', clean_name.lower())
    safe_func = re.sub(r'_+', '_', safe_func).strip('_')[:24] or 'data_processor'

    return {
        'basic': {
            'id': f'l{lesson_id}-b',
            'difficulty': 'Basic',
            'badge_class': 'bg-success',
            'approach': 'function',
            'title': f'{clean_name} - Data Normalizer & Boundary Filter',
            'function_name': f'normalize_{safe_func}',
            'prompt': f'Write a Python function `normalize_{safe_func}(data: list, min_val: float, max_val: float) -> dict` for {clean_name}. It filters numbers strictly within `[min_val, max_val]` and returns a dictionary with `"count"` (valid entries) and `"cleaned_data"` sorted ascending.',
            'constraints': 'min_val <= max_val',
            'starter_code': (
                f"def normalize_{safe_func}(data: list, min_val: float, max_val: float) -> dict:\n"
                f"    \"\"\"Filter and sort data for {clean_name}.\"\"\"\n"
                f"    pass\n"
            ),
            'test_cases': [
                {'input': [[10, -5, 25, 100, 15], 0, 50], 'expected': {'count': 3, 'cleaned_data': [10, 15, 25]}, 'desc': 'Keeps 10, 15, 25 in range [0, 50]'},
                {'input': [[-10, -20], 0, 100], 'expected': {'count': 0, 'cleaned_data': []}, 'desc': 'All out of range'}
            ],
            'hint': 'Filter using list comprehension `[x for x in data if min_val <= x <= max_val]` and sorted().',
            'solution_code': (
                f"def normalize_{safe_func}(data: list, min_val: float, max_val: float) -> dict:\n"
                f"    valid = sorted([x for x in data if min_val <= x <= max_val])\n"
                f"    return {{'count': len(valid), 'cleaned_data': valid}}\n"
            ),
            'explanation': f'Essential data boundary filtering and sanitization required for {clean_name}.'
        },
        'intermediate': {
            'id': f'l{lesson_id}-i',
            'difficulty': 'Intermediate',
            'badge_class': 'bg-primary',
            'approach': 'function',
            'title': f'{clean_name} - Aggregate Metrics Analyzer',
            'function_name': f'aggregate_{safe_func}',
            'prompt': f'Write a Python function `aggregate_{safe_func}(records: list, threshold: float) -> dict` for {clean_name}. It filters dicts where `r["value"] >= threshold`, and returns `"matching_count"`, `"total_sum"`, and `"average"` (rounded to 2 decimals). If none match, return count 0, total 0.0, average 0.0.',
            'constraints': 'records is a list of dicts with key "value"',
            'starter_code': (
                f"def aggregate_{safe_func}(records: list, threshold: float) -> dict:\n"
                f"    \"\"\"Filter records exceeding threshold and return summary totals.\"\"\"\n"
                f"    pass\n"
            ),
            'test_cases': [
                {'input': [[{'value': 10.0}, {'value': 25.0}, {'value': 5.0}], 10.0], 'expected': {'matching_count': 2, 'total_sum': 35.0, 'average': 17.5}, 'desc': 'Filters 10.0 and 25.0, average 17.5'},
                {'input': [[{'value': 1.0}], 50.0], 'expected': {'matching_count': 0, 'total_sum': 0.0, 'average': 0.0}, 'desc': 'Zero matches'}
            ],
            'hint': 'Extract matches = [r["value"] for r in records if r.get("value", 0) >= threshold], then compute sum and average.',
            'solution_code': (
                f"def aggregate_{safe_func}(records: list, threshold: float) -> dict:\n"
                f"    matches = [float(r['value']) for r in records if r.get('value', 0) >= threshold]\n"
                f"    if not matches:\n"
                f"        return {{'matching_count': 0, 'total_sum': 0.0, 'average': 0.0}}\n"
                f"    tot = sum(matches)\n"
                f"    return {{'matching_count': len(matches), 'total_sum': round(tot, 2), 'average': round(tot / len(matches), 2)}}\n"
            ),
            'explanation': f'Production aggregation pipeline for telemetry and metrics in {clean_name}.'
        },
        'advance': {
            'id': f'l{lesson_id}-a',
            'difficulty': 'Advance',
            'badge_class': 'bg-purple',
            'approach': 'class',
            'class_name': 'BatchQueue',
            'title': f'{clean_name} - Stream Batch Queue Manager',
            'prompt': f'Design an Object-Oriented class `BatchQueue(batch_size: int)` for {clean_name}. Implement `enqueue(item)` which appends an item to the queue, and `flush_batches() -> list` which deduplicates all queued items while preserving original arrival order, and partitions them into batches of at most `batch_size`.',
            'constraints': 'batch_size >= 1',
            'starter_code': (
                "class BatchQueue:\n"
                "    \"\"\"Manage queued items and partition into fixed-size deduplicated batches.\"\"\"\n"
                "    def __init__(self, batch_size: int):\n"
                "        self.batch_size = max(1, batch_size)\n"
                "        self.items = []\n\n"
                "    def enqueue(self, item) -> int:\n"
                "        # Add item and return current queue size\n"
                "        pass\n\n"
                "    def flush_batches(self) -> list:\n"
                "        # Deduplicate items and return list of sublists of size batch_size\n"
                "        pass\n"
            ),
            'test_cases': [
                {
                    'desc': 'Enqueue stream items with duplicates and flush in batches of size 3',
                    'init_args': [3],
                    'expected': True,
                    'operations': [
                        {'method': 'enqueue', 'args': [1], 'expected': 1},
                        {'method': 'enqueue', 'args': [2], 'expected': 2},
                        {'method': 'enqueue', 'args': [2], 'expected': 3},
                        {'method': 'enqueue', 'args': [3], 'expected': 4},
                        {'method': 'enqueue', 'args': [4], 'expected': 5},
                        {'method': 'enqueue', 'args': [1], 'expected': 6},
                        {'method': 'enqueue', 'args': [5], 'expected': 7},
                        {'method': 'flush_batches', 'args': [], 'expected': [[1, 2, 3], [4, 5]]}
                    ]
                }
            ],
            'hint': 'In flush_batches, use a set to track seen items, build a deduped list, clear self.items, and slice with range(0, len, batch_size).',
            'solution_code': (
                "class BatchQueue:\n"
                "    def __init__(self, batch_size: int):\n"
                "        self.batch_size = max(1, batch_size)\n"
                "        self.items = []\n\n"
                "    def enqueue(self, item) -> int:\n"
                "        self.items.append(item)\n"
                "        return len(self.items)\n\n"
                "    def flush_batches(self) -> list:\n"
                "        seen = set()\n"
                "        dedup = []\n"
                "        for item in self.items:\n"
                "            if item not in seen:\n"
                "                dedup.append(item)\n"
                "                seen.add(item)\n"
                "        self.items = []\n"
                "        return [dedup[i:i + self.batch_size] for i in range(0, len(dedup), self.batch_size)]\n"
            ),
            'explanation': f'Production Object-Oriented stream batching architecture for {clean_name}.'
        }
    }


def generate_smart_challenges_template(lesson) -> Dict[str, Any]:
    """Generate smart 3-tier programming challenge templates tailored to a lesson for instructor editing."""
    title = getattr(lesson, 'title', '')
    lesson_id = getattr(lesson, 'id', 1)
    module = getattr(lesson, 'module', None)
    course = module.course if module else None
    course_title = course.title if course else ''
    t_lower = title.lower()
    c_lower = course_title.lower()

    if any(k in c_lower for k in ['javascript', 'frontend', 'react']):
        language = 'javascript'
    elif any(k in c_lower for k in ['linux', 'devops', 'docker', 'kubernetes']):
        language = 'bash'
    elif any(k in c_lower for k in ['sql', 'database', 'relational']):
        language = 'sql'
    elif 'cs50' in c_lower or 'c syntax' in t_lower:
        language = 'c'
    else:
        language = 'python'

    challenges = _get_topic_challenges(t_lower, language, title, course_title, lesson_id)
    return {
        'lesson_id': lesson_id,
        'lesson_title': title,
        'course_title': course_title,
        'language': language,
        'challenges': challenges
    }

