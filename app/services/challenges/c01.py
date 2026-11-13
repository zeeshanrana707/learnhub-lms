"""Auto-generated topic-specific challenges."""

CHALLENGES = {(1, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'principal > 0, 0 <= annual_return <= 1, years >= 1',
                      'difficulty': 'Advance',
                      'explanation': 'Models quantitative capital accumulation with friction.',
                      'function_name': 'project_growth',
                      'hint': 'Loop for years and multiply by net factor.',
                      'id': 'c1-m1-l1-a',
                      'prompt': 'Write `project_growth(principal, annual_return, tax_rate, years)`. Each year: '
                                '`balance *= 1 + (annual_return * (1 - tax_rate))`. Return balance rounded to 2 '
                                'decimals.',
                      'solution_code': 'def project_growth(principal: float, annual_return: float, tax_rate: float, '
                                       'years: int) -> float:\n'
                                       '    b = float(principal)\n'
                                       '    factor = 1.0 + (annual_return * (1.0 - tax_rate))\n'
                                       '    for _ in range(years): b *= factor\n'
                                       '    return round(b, 2)\n',
                      'starter_code': 'def project_growth(principal: float, annual_return: float, tax_rate: float, '
                                      'years: int) -> float:\n'
                                      '    # Return final balance\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Year 1', 'expected': 10800.0, 'input': [10000.0, 0.1, 0.2, 1]},
                                     {'desc': 'Year 2', 'expected': 11664.0, 'input': [10000.0, 0.1, 0.2, 2]}],
                      'title': 'Compound Growth with Annual Tax Drag'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': '-273.15 <= celsius <= 1000',
                    'difficulty': 'Basic',
                    'explanation': 'Demonstrates Python floating point operators and precedence.',
                    'function_name': 'celsius_to_fahrenheit',
                    'hint': 'Multiply by 9/5 and add 32. Use round(..., 1).',
                    'id': 'c1-m1-l1-b',
                    'prompt': 'Write `celsius_to_fahrenheit(celsius)` converting °C to °F: `(celsius * 9/5) + 32`. '
                              'Round to 1 decimal.',
                    'solution_code': 'def celsius_to_fahrenheit(celsius: float) -> float:\n'
                                     '    return round((celsius * 9 / 5) + 32, 1)\n',
                    'starter_code': 'def celsius_to_fahrenheit(celsius: float) -> float:\n'
                                    '    # Return converted temperature\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Freezing point', 'expected': 32.0, 'input': [0.0]},
                                   {'desc': 'Boiling point', 'expected': 212.0, 'input': [100.0]}],
                    'title': 'Celsius to Fahrenheit Converter'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'weight_kg > 0, height_m > 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'Applies multi-conditional evaluation.',
                           'function_name': 'classify_bmi',
                           'hint': 'Calculate bmi and compare with if-elif-else ladder.',
                           'id': 'c1-m1-l1-i',
                           'prompt': 'Write `classify_bmi(weight_kg, height_m)` computing `weight / (height**2)` '
                                     'returning "Underweight" (< 18.5), "Normal" (< 25), "Overweight" (< 30), or '
                                     '"Obese".',
                           'solution_code': 'def classify_bmi(weight_kg: float, height_m: float) -> str:\n'
                                            '    bmi = weight_kg / (height_m ** 2)\n'
                                            '    if bmi < 18.5: return "Underweight"\n'
                                            '    elif bmi < 25.0: return "Normal"\n'
                                            '    elif bmi < 30.0: return "Overweight"\n'
                                            '    return "Obese"\n',
                           'starter_code': 'def classify_bmi(weight_kg: float, height_m: float) -> str:\n'
                                           '    # Return category string\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '< 18.5', 'expected': 'Underweight', 'input': [50.0, 1.75]},
                                          {'desc': '18.5-25', 'expected': 'Normal', 'input': [70.0, 1.75]}],
                           'title': 'BMI Health Category Classifier'}},
 (1, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'n >= 2',
                      'difficulty': 'Advance',
                      'explanation': 'Trial division prime factoring in O(sqrt(N)) time.',
                      'function_name': 'prime_factors',
                      'hint': 'Divide out 2, then test odd numbers d = 3, 5, 7...',
                      'id': 'c1-m1-l2-a',
                      'prompt': 'Write `prime_factors(n)` returning `{prime: count}` dictionary for `n >= 2`.',
                      'solution_code': 'def prime_factors(n: int) -> dict:\n'
                                       '    f, d, c = {}, 2, n\n'
                                       '    while d * d <= c:\n'
                                       '        while c % d == 0: f[d] = f.get(d, 0) + 1; c //= d\n'
                                       '        d += 1 if d == 2 else 2\n'
                                       '    if c > 1: f[c] = f.get(c, 0) + 1\n'
                                       '    return f\n',
                      'starter_code': 'def prime_factors(n: int) -> dict:\n    # Return {factor: count}\n    pass\n',
                      'test_cases': [{'desc': '12 = 2^2 * 3^1', 'expected': {2: 2, 3: 1}, 'input': [12]},
                                     {'desc': '17 is prime', 'expected': {17: 1}, 'input': [17]}],
                      'title': 'Prime Factorization Counter'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'year >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Compound modulo conditional logic.',
                    'function_name': 'is_leap_year',
                    'hint': '(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)',
                    'id': 'c1-m1-l2-b',
                    'prompt': 'Write `is_leap_year(year)`: True if divisible by 4, except century years must be '
                              'divisible by 400.',
                    'solution_code': 'def is_leap_year(year: int) -> bool:\n'
                                     '    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)\n',
                    'starter_code': 'def is_leap_year(year: int) -> bool:\n    # Return True if leap year\n    pass\n',
                    'test_cases': [{'desc': 'Leap year', 'expected': True, 'input': [2024]},
                                   {'desc': 'Century non-leap', 'expected': False, 'input': [1900]}],
                    'title': 'Leap Year Validator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'n >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'While loop iteration and termination guarantees.',
                           'function_name': 'collatz_steps',
                           'hint': 'Use while curr > 1 and increment a counter.',
                           'id': 'c1-m1-l2-i',
                           'prompt': 'Write `collatz_steps(n)`: if even `n = n//2`, if odd `n = 3*n + 1`. Return total '
                                     'step count to reach 1.',
                           'solution_code': 'def collatz_steps(n: int) -> int:\n'
                                            '    c, steps = n, 0\n'
                                            '    while c > 1:\n'
                                            '        c = c // 2 if c % 2 == 0 else 3 * c + 1\n'
                                            '        steps += 1\n'
                                            '    return steps\n',
                           'starter_code': 'def collatz_steps(n: int) -> int:\n    # Return steps to 1\n    pass\n',
                           'test_cases': [{'desc': '6 takes 8 steps', 'expected': 8, 'input': [6]},
                                          {'desc': '1 takes 0 steps', 'expected': 0, 'input': [1]}],
                           'title': 'Collatz Conjecture Step Counter'}},
 (2, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'nested contains ints and nested lists',
                      'difficulty': 'Advance',
                      'explanation': 'Recursive tree flattening.',
                      'function_name': 'flatten_nested_list',
                      'hint': 'Use recursion: if isinstance(item, list) recurse, else append.',
                      'id': 'c1-m2-l1-a',
                      'prompt': 'Write `flatten_nested_list(nested)` returning a 1D list from arbitrarily nested '
                                'lists.',
                      'solution_code': 'def flatten_nested_list(nested: list) -> list:\n'
                                       '    res = []\n'
                                       '    for item in nested:\n'
                                       '        if isinstance(item, list): res.extend(flatten_nested_list(item))\n'
                                       '        else: res.append(item)\n'
                                       '    return res\n',
                      'starter_code': 'def flatten_nested_list(nested: list) -> list:\n'
                                      '    # Return flat 1D list\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Flattens deep nest',
                                      'expected': [1, 2, 3, 4, 5, 6],
                                      'input': [[1, [2, [3, 4], 5], 6]]}],
                      'title': 'Flatten Arbitrarily Nested List'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'words is a list of strings',
                    'difficulty': 'Basic',
                    'explanation': 'Fundamental dictionary hashing in Python.',
                    'function_name': 'word_frequencies',
                    'hint': 'Iterate through words and update dict[w] = dict.get(w, 0) + 1.',
                    'id': 'c1-m2-l1-b',
                    'prompt': 'Write `word_frequencies(words)` returning dict mapping each unique word to its count.',
                    'solution_code': 'def word_frequencies(words: list) -> dict:\n'
                                     '    res = {}\n'
                                     '    for w in words: res[w] = res.get(w, 0) + 1\n'
                                     '    return res\n',
                    'starter_code': 'def word_frequencies(words: list) -> dict:\n'
                                    '    # Return frequency dict\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Counts duplicates',
                                    'expected': {'cat': 2, 'dog': 1},
                                    'input': [['cat', 'dog', 'cat']]}],
                    'title': 'Word Frequency Counter'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'd is a dict of {key: value}',
                           'difficulty': 'Intermediate',
                           'explanation': 'Demonstrates multi-key dictionary grouping.',
                           'function_name': 'invert_dict',
                           'hint': 'Group keys by value and sort the resulting lists.',
                           'id': 'c1-m2-l1-i',
                           'prompt': 'Write `invert_dict(d)` mapping each value to a sorted list of its original keys.',
                           'solution_code': 'def invert_dict(d: dict) -> dict:\n'
                                            '    inv = {}\n'
                                            '    for k, v in d.items(): inv.setdefault(v, []).append(k)\n'
                                            '    for v in inv: inv[v].sort()\n'
                                            '    return inv\n',
                           'starter_code': 'def invert_dict(d: dict) -> dict:\n    # Return inverted dict\n    pass\n',
                           'test_cases': [{'desc': 'Inverts with duplicate values',
                                           'expected': {1: ['a', 'c'], 2: ['b']},
                                           'input': [{'a': 1, 'b': 2, 'c': 1}]}],
                           'title': 'Invert Dictionary Mapping'}},
 (2, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'operations is a list of [str, float]',
                      'difficulty': 'Advance',
                      'explanation': 'Sequential data pipeline accumulator.',
                      'function_name': 'compose_pipeline',
                      'hint': 'Iterate through operations and update running float accumulator.',
                      'id': 'c1-m2-l2-a',
                      'prompt': 'Write `compose_pipeline(x, operations)` where each operation is `[op_name, factor]` '
                                '("add" or "mul"). Return final x rounded to 2 decimals.',
                      'solution_code': 'def compose_pipeline(x: float, operations: list) -> float:\n'
                                       '    curr = float(x)\n'
                                       '    for op, val in operations:\n'
                                       '        if op == "add": curr += val\n'
                                       '        elif op == "mul": curr *= val\n'
                                       '    return round(curr, 2)\n',
                      'starter_code': 'def compose_pipeline(x: float, operations: list) -> float:\n'
                                      '    # Execute operations in order\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '(5+5)*2 = 20',
                                      'expected': 20.0,
                                      'input': [5.0, [['add', 5], ['mul', 2]]]}],
                      'title': 'Pipeline Operations Executor'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'operation in ["add", "multiply", "power"]',
                    'difficulty': 'Basic',
                    'explanation': 'Applies functional mapping with parameters.',
                    'function_name': 'apply_transform',
                    'hint': 'Use list comprehension with an operation condition.',
                    'id': 'c1-m2-l2-b',
                    'prompt': 'Write `apply_transform(numbers, operation, factor)` for operations "add", "multiply", '
                              '"power". Return list rounded to 2 decimals.',
                    'solution_code': 'def apply_transform(numbers: list, operation: str, factor: float) -> list:\n'
                                     '    if operation == "add": return [round(float(x + factor), 2) for x in '
                                     'numbers]\n'
                                     '    if operation == "multiply": return [round(float(x * factor), 2) for x in '
                                     'numbers]\n'
                                     '    if operation == "power": return [round(float(x ** factor), 2) for x in '
                                     'numbers]\n'
                                     '    return []\n',
                    'starter_code': 'def apply_transform(numbers: list, operation: str, factor: float) -> list:\n'
                                    '    # Return transformed list\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Adds 10',
                                    'expected': [11.0, 12.0, 13.0],
                                    'input': [[1, 2, 3], 'add', 10]}],
                    'title': 'Dynamic List Transformation Dispatcher'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'tags are strings',
                           'difficulty': 'Intermediate',
                           'explanation': 'Demonstrates variable arguments syntax in Python.',
                           'function_name': 'format_user_profile',
                           'hint': 'Convert tags to sorted list of uppercase strings.',
                           'id': 'c1-m2-l2-i',
                           'prompt': 'Write `format_user_profile(*tags, **details)` returning `{"tags": '
                                     'sorted([uppercase strings]), "details": dict(kwargs)}`.',
                           'solution_code': 'def format_user_profile(*tags, **details) -> dict:\n'
                                            '    return {"tags": sorted([str(t).upper() for t in tags]), "details": '
                                            'dict(details)}\n',
                           'starter_code': 'def format_user_profile(*tags, **details) -> dict:\n'
                                           '    # Return profile dict\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Tags only',
                                           'expected': {'details': {}, 'tags': ['AI', 'DEVELOPER']},
                                           'input': ['ai', 'developer']}],
                           'title': 'Flexible Parameter Parser (*args & **kwargs)'}},
 (3, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'timestamps are positive ints in ascending order',
                      'difficulty': 'Advance',
                      'explanation': 'Sliding window stateful rate limiting class algorithm.',
                      'function_name': 'rate_limiter_requests',
                      'hint': 'Maintain a deque or list of allowed timestamps, evict timestamps <= t - window_seconds.',
                      'id': 'c1-m3-l1-a',
                      'prompt': 'Write `rate_limiter_requests(timestamps, window_seconds, max_requests)` that '
                                'evaluates a sorted list of request timestamps. Return a list of booleans indicating '
                                'if each request is ALLOWED (at most max_requests in previous window_seconds).',
                      'solution_code': 'def rate_limiter_requests(timestamps: list, window_seconds: int, max_requests: '
                                       'int) -> list:\n'
                                       '    allowed, history = [], []\n'
                                       '    for t in timestamps:\n'
                                       '        history = [x for x in history if t - x < window_seconds]\n'
                                       '        if len(history) < max_requests:\n'
                                       '            history.append(t)\n'
                                       '            allowed.append(True)\n'
                                       '        else: allowed.append(False)\n'
                                       '    return allowed\n',
                      'starter_code': 'def rate_limiter_requests(timestamps: list, window_seconds: int, max_requests: '
                                      'int) -> list:\n'
                                      '    # Return list of bools\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'At time 2 third request blocked',
                                      'expected': [True, True, False, False, True],
                                      'input': [[1, 2, 2, 3, 10], 2, 2]}],
                      'title': 'Sliding Window Rate Limiter Class Simulation'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'initial_balance >= 0',
                    'difficulty': 'Basic',
                    'explanation': 'Encapsulation and boundary state management.',
                    'function_name': 'simulate_bank_account',
                    'hint': 'Iterate transactions, if t < 0 only subtract if balance + t >= 0.',
                    'id': 'c1-m3-l1-b',
                    'prompt': 'Write `simulate_bank_account(initial_balance, transactions)`. Positive transactions '
                              'deposit, negative withdraw if sufficient balance exists. Return final balance.',
                    'solution_code': 'def simulate_bank_account(initial_balance: float, transactions: list) -> float:\n'
                                     '    bal = float(initial_balance)\n'
                                     '    for t in transactions:\n'
                                     '        if t >= 0: bal += t\n'
                                     '        elif bal + t >= 0: bal += t\n'
                                     '    return round(bal, 2)\n',
                    'starter_code': 'def simulate_bank_account(initial_balance: float, transactions: list) -> float:\n'
                                    '    # Return final balance\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Disallows overdraft -200',
                                    'expected': 140.0,
                                    'input': [100.0, [50, -30, -200, 20]]}],
                    'title': 'Bank Account Transaction Ledger'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'v1 and v2 are len 2 lists of numbers',
                           'difficulty': 'Intermediate',
                           'explanation': 'Dunder arithmetic operator simulation for vector classes.',
                           'function_name': 'vector_2d_operations',
                           'hint': 'Distance is round(((x1-x2)**2 + (y1-y2)**2)**0.5, 2).',
                           'id': 'c1-m3-l1-i',
                           'prompt': 'Write `vector_2d_operations(v1, v2, op)`. `v1` and `v2` are `[x, y]`. '
                                     'Operations: "add" (`[x1+x2, y1+y2]`), "dot" (`x1*x2 + y1*y2`), "distance" '
                                     '(Euclidean dist rounded to 2 decimals).',
                           'solution_code': 'def vector_2d_operations(v1: list, v2: list, op: str):\n'
                                            '    if op == "add": return [v1[0] + v2[0], v1[1] + v2[1]]\n'
                                            '    if op == "dot": return (v1[0] * v2[0]) + (v1[1] * v2[1])\n'
                                            '    if op == "distance": return round(((v1[0]-v2[0])**2 + '
                                            '(v1[1]-v2[1])**2)**0.5, 2)\n'
                                            '    return None\n',
                           'starter_code': 'def vector_2d_operations(v1: list, v2: list, op: str):\n'
                                           '    # Return result according to op\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Vector addition',
                                           'expected': [4, 6],
                                           'input': [[1, 2], [3, 4], 'add']},
                                          {'desc': '1*3 + 2*4 = 11', 'expected': 11, 'input': [[1, 2], [3, 4], 'dot']}],
                           'title': '2D Vector Math Calculator'}},
 (3, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'layers is a list of layer dicts',
                      'difficulty': 'Advance',
                      'explanation': 'Modular forward pass architecture mirroring PyTorch nn.Sequential.',
                      'function_name': 'execute_layer_pipeline',
                      'hint': 'Iterate layers and update x sequentially.',
                      'id': 'c1-m3-l2-a',
                      'prompt': 'Write `execute_layer_pipeline(x, layers)` where x is float and layers is list of '
                                'dicts: `{"type": "dense", "w": float, "b": float}` -> `x*w + b`, or `{"type": '
                                '"relu"}` -> `max(0.0, x)`. Return final float rounded to 2 decimals.',
                      'solution_code': 'def execute_layer_pipeline(x: float, layers: list) -> float:\n'
                                       '    curr = float(x)\n'
                                       '    for l in layers:\n'
                                       '        if l["type"] == "dense": curr = (curr * l["w"]) + l["b"]\n'
                                       '        elif l["type"] == "relu": curr = max(0.0, curr)\n'
                                       '    return round(curr, 2)\n',
                      'starter_code': 'def execute_layer_pipeline(x: float, layers: list) -> float:\n'
                                      '    # Execute layers sequentially\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '2*(-1.5)+1 = -2 -> relu(-2) = 0.0',
                                      'expected': 0.0,
                                      'input': [2.0, [{'b': 1.0, 'type': 'dense', 'w': -1.5}, {'type': 'relu'}]]}],
                      'title': 'Neural Network Layer Execution Pipeline'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'hours >= 0, rate >= 0',
                    'difficulty': 'Basic',
                    'explanation': 'Polymorphic behavior simulation across organizational roles.',
                    'function_name': 'calculate_payroll',
                    'hint': 'Calculate each pay and sum them up.',
                    'id': 'c1-m3-l2-b',
                    'prompt': 'Write `calculate_payroll(employees)` where each employee is `{"role": str, "hours": '
                              'float, "rate": float}`. If role is "manager", bonus 20% is added to their pay (`hours * '
                              'rate * 1.2`). Return total payroll rounded to 2 decimals.',
                    'solution_code': 'def calculate_payroll(employees: list) -> float:\n'
                                     '    tot = 0.0\n'
                                     '    for e in employees:\n'
                                     '        pay = e["hours"] * e["rate"]\n'
                                     '        if e.get("role") == "manager": pay *= 1.2\n'
                                     '        tot += pay\n'
                                     '    return round(tot, 2)\n',
                    'starter_code': 'def calculate_payroll(employees: list) -> float:\n'
                                    '    # Return total payroll\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2000 + 2400 = 4400',
                                    'expected': 4400.0,
                                    'input': [[{'hours': 40, 'rate': 50, 'role': 'dev'},
                                               {'hours': 40, 'rate': 50, 'role': 'manager'}]]}],
                    'title': 'Polymorphic Payroll Calculator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'dimensions > 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'Polymorphic interface implementation for geometric structures.',
                           'function_name': 'compute_shape_metrics',
                           'hint': 'Circle area = 3.14159 * r**2, perimeter = 2 * 3.14159 * r.',
                           'id': 'c1-m3-l2-i',
                           'prompt': 'Write `compute_shape_metrics(shapes)` where shape is `{"type": "circle", '
                                     '"radius": r}` or `{"type": "rect", "w": w, "h": h}`. Return list of dicts '
                                     '`{"type": type, "area": round(area, 2), "perimeter": round(perim, 2)}` with pi = '
                                     '3.14159.',
                           'solution_code': 'def compute_shape_metrics(shapes: list) -> list:\n'
                                            '    res = []\n'
                                            '    pi = 3.14159\n'
                                            '    for s in shapes:\n'
                                            '        if s["type"] == "rect":\n'
                                            '            a = round(s["w"] * s["h"], 2)\n'
                                            '            p = round(2 * (s["w"] + s["h"]), 2)\n'
                                            '            res.append({"type": "rect", "area": a, "perimeter": p})\n'
                                            '        elif s["type"] == "circle":\n'
                                            '            r = s["radius"]\n'
                                            '            res.append({"type": "circle", "area": round(pi * r * r, 2), '
                                            '"perimeter": round(2 * pi * r, 2)})\n'
                                            '    return res\n',
                           'starter_code': 'def compute_shape_metrics(shapes: list) -> list:\n'
                                           '    # Return list of metric dicts\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Computes rectangle and circle',
                                           'expected': [{'area': 20.0, 'perimeter': 18.0, 'type': 'rect'},
                                                        {'area': 12.57, 'perimeter': 12.57, 'type': 'circle'}],
                                           'input': [[{'h': 5, 'type': 'rect', 'w': 4},
                                                      {'radius': 2, 'type': 'circle'}]]}],
                           'title': 'Geometric Shape Metrics (Area & Perimeter)'}},
 (4, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'matrix is non-empty list of lists',
                      'difficulty': 'Advance',
                      'explanation': 'NumPy matrix regularization calculation.',
                      'function_name': 'frobenius_norm_normalize',
                      'hint': 'Norm is sqrt of sum of squares of all elements.',
                      'id': 'c1-m4-l1-a',
                      'prompt': 'Write `frobenius_norm_normalize(matrix)` returning `{"norm": round(norm, 2), '
                                '"normalized": matrix / norm}`. Round each element in normalized to 2 decimals.',
                      'solution_code': 'def frobenius_norm_normalize(matrix: list) -> dict:\n'
                                       '    tot_sq = sum(x**2 for row in matrix for x in row)\n'
                                       '    norm = round(tot_sq ** 0.5, 2)\n'
                                       '    normed = [[round(x / norm, 2) for x in row] for row in matrix]\n'
                                       '    return {"norm": norm, "normalized": normed}\n',
                      'starter_code': 'def frobenius_norm_normalize(matrix: list) -> dict:\n'
                                      '    # Return norm and normalized matrix\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'sqrt(9+16)=5',
                                      'expected': {'norm': 5.0, 'normalized': [[0.6, 0.0], [0.0, 0.8]]},
                                      'input': [[[3, 0], [0, 4]]]}],
                      'title': 'Frobenius Matrix Norm & Normalization'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'matrix is non-empty square matrix of numbers',
                    'difficulty': 'Basic',
                    'explanation': 'Linear algebra core matrix properties.',
                    'function_name': 'matrix_transpose_and_trace',
                    'hint': 'Transpose column c is [row[c] for row in matrix]. Trace is sum(matrix[i][i]).',
                    'id': 'c1-m4-l1-b',
                    'prompt': 'Write `matrix_transpose_and_trace(matrix)` returning dict `{"transpose": list, "trace": '
                              'sum of main diagonal}`.',
                    'solution_code': 'def matrix_transpose_and_trace(matrix: list) -> dict:\n'
                                     '    n = len(matrix)\n'
                                     '    trans = [[matrix[r][c] for r in range(n)] for c in range(n)]\n'
                                     '    tr = sum(matrix[i][i] for i in range(n))\n'
                                     '    return {"transpose": trans, "trace": tr}\n',
                    'starter_code': 'def matrix_transpose_and_trace(matrix: list) -> dict:\n'
                                    '    # Return {"transpose": ..., "trace": ...}\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2x2 matrix trace = 1+4=5',
                                    'expected': {'trace': 5, 'transpose': [[1, 3], [2, 4]]},
                                    'input': [[[1, 2], [3, 4]]]}],
                    'title': 'Matrix Transpose and Trace'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'columns of A == rows of B',
                           'difficulty': 'Intermediate',
                           'explanation': 'Implements textbook matrix multiplication algorithm in O(N^3).',
                           'function_name': 'matrix_multiply',
                           'hint': 'C[i][j] is sum(A[i][k] * B[k][j] for k).',
                           'id': 'c1-m4-l1-i',
                           'prompt': 'Write `matrix_multiply(A, B)` computing the dot product matrix `A @ B`.',
                           'solution_code': 'def matrix_multiply(A: list, B: list) -> list:\n'
                                            '    rA, cA, cB = len(A), len(A[0]), len(B[0])\n'
                                            '    C = [[0] * cB for _ in range(rA)]\n'
                                            '    for i in range(rA):\n'
                                            '        for j in range(cB):\n'
                                            '            C[i][j] = sum(A[i][k] * B[k][j] for k in range(cA))\n'
                                            '    return C\n',
                           'starter_code': 'def matrix_multiply(A: list, B: list) -> list:\n'
                                           '    # Return matrix product\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Standard 2x2 product',
                                           'expected': [[4, 4], [10, 8]],
                                           'input': [[[1, 2], [3, 4]], [[2, 0], [1, 2]]]}],
                           'title': '2D Matrix Multiplication'}},
 (4, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'non-zero vectors of same length',
                      'difficulty': 'Advance',
                      'explanation': 'Fundamental metric for dense vector search and semantic similarity in AI.',
                      'function_name': 'cosine_similarity',
                      'hint': 'Divide dot product by product of L2 norms.',
                      'id': 'c1-m4-l2-a',
                      'prompt': 'Write `cosine_similarity(vec_a, vec_b)`: `dot(a, b) / (norm(a) * norm(b))`. Round to '
                                '4 decimals.',
                      'solution_code': 'def cosine_similarity(vec_a: list, vec_b: list) -> float:\n'
                                       '    dot = sum(a * b for a, b in zip(vec_a, vec_b))\n'
                                       '    norm_a = sum(a * a for a in vec_a) ** 0.5\n'
                                       '    norm_b = sum(b * b for b in vec_b) ** 0.5\n'
                                       '    if norm_a == 0 or norm_b == 0: return 0.0\n'
                                       '    return round(dot / (norm_a * norm_b), 4)\n',
                      'starter_code': 'def cosine_similarity(vec_a: list, vec_b: list) -> float:\n'
                                      '    # Return cosine similarity\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Identical vectors = 1.0', 'expected': 1.0, 'input': [[1, 0], [1, 0]]},
                                     {'desc': 'Orthogonal vectors = 0.0', 'expected': 0.0, 'input': [[1, 0], [0, 1]]}],
                      'title': 'Vector Cosine Similarity'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(vec_a) == len(vec_b) >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Vectorized inner product foundational to neural network layer operations.',
                    'function_name': 'vector_dot_product',
                    'hint': 'sum(a * b for a, b in zip(vec_a, vec_b)).',
                    'id': 'c1-m4-l2-b',
                    'prompt': 'Write `vector_dot_product(vec_a, vec_b)` returning sum of products of corresponding '
                              'components.',
                    'solution_code': 'def vector_dot_product(vec_a: list, vec_b: list) -> float:\n'
                                     '    return float(sum(a * b for a, b in zip(vec_a, vec_b)))\n',
                    'starter_code': 'def vector_dot_product(vec_a: list, vec_b: list) -> float:\n'
                                    '    # Return dot product\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '4 - 6 + 5 = 3.0', 'expected': 3.0, 'input': [[1, 3, -5], [4, -2, -1]]}],
                    'title': 'Vector Dot Product'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(p1) == len(p2)',
                           'difficulty': 'Intermediate',
                           'explanation': 'L2 spatial metric used across clustering and nearest neighbors.',
                           'function_name': 'euclidean_distance',
                           'hint': 'Subtract, square, sum, take square root.',
                           'id': 'c1-m4-l2-i',
                           'prompt': 'Write `euclidean_distance(p1, p2)` computing `sqrt(sum((p1[i] - p2[i])**2))`. '
                                     'Round to 2 decimals.',
                           'solution_code': 'def euclidean_distance(p1: list, p2: list) -> float:\n'
                                            '    return round(sum((a - b)**2 for a, b in zip(p1, p2)) ** 0.5, 2)\n',
                           'starter_code': 'def euclidean_distance(p1: list, p2: list) -> float:\n'
                                           '    # Return euclidean distance\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '3-4-5 triangle', 'expected': 5.0, 'input': [[0, 0], [3, 4]]},
                                          {'desc': '3D distance', 'expected': 7.07, 'input': [[1, 2, 3], [4, 6, 8]]}],
                           'title': 'Euclidean Distance in N-Dimensions'}},
 (5, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'values is list of at least 4 numbers',
                      'difficulty': 'Advance',
                      'explanation': 'Statistical outlier anomaly detection rule used across data science.',
                      'function_name': 'detect_iqr_outliers',
                      'hint': 'Sort values to find Q1 and Q3, compute IQR = Q3 - Q1, bounds are Q1 - 1.5*IQR and Q3 + '
                              '1.5*IQR.',
                      'id': 'c1-m5-l1-a',
                      'prompt': 'Write `detect_iqr_outliers(values)` using 1.5 * IQR rule. Q1 is median of lower half, '
                                'Q3 median of upper half. Return list of outlier values in original order.',
                      'solution_code': 'def detect_iqr_outliers(values: list) -> list:\n'
                                       '    s = sorted(values)\n'
                                       '    n = len(s)\n'
                                       '    q1 = s[n // 4]\n'
                                       '    q3 = s[(3 * n) // 4]\n'
                                       '    iqr = q3 - q1\n'
                                       '    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n'
                                       '    return [x for x in values if x < low or x > high]\n',
                      'starter_code': 'def detect_iqr_outliers(values: list) -> list:\n'
                                      '    # Return outlier values\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '100 is clear outlier',
                                      'expected': [100],
                                      'input': [[10, 12, 11, 13, 12, 100, 11]]}],
                      'title': 'IQR Outlier Detector'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'At least one non-None value in field_name',
                    'difficulty': 'Basic',
                    'explanation': 'Tabular data sanitization and pandas fillna simulation.',
                    'function_name': 'impute_missing_values',
                    'hint': 'Calculate mean of non-None values, then replace None entries.',
                    'id': 'c1-m5-l1-b',
                    'prompt': 'Write `impute_missing_values(records, field_name)` replacing `None` in `field_name` '
                              'with the column average rounded to 2 decimals.',
                    'solution_code': 'def impute_missing_values(records: list, field_name: str) -> list:\n'
                                     '    vals = [r[field_name] for r in records if r.get(field_name) is not None]\n'
                                     '    mean_val = round(sum(vals) / len(vals), 2) if vals else 0.0\n'
                                     '    res = []\n'
                                     '    for r in records:\n'
                                     '        r_copy = dict(r)\n'
                                     '        if r_copy.get(field_name) is None: r_copy[field_name] = mean_val\n'
                                     '        res.append(r_copy)\n'
                                     '    return res\n',
                    'starter_code': 'def impute_missing_values(records: list, field_name: str) -> list:\n'
                                    '    # Return records with imputed values\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Mean of 10 and 20 is 15.0',
                                    'expected': [{'v': 10}, {'v': 15.0}, {'v': 20}],
                                    'input': [[{'v': 10}, {'v': None}, {'v': 20}], 'v']}],
                    'title': 'Missing Value Imputer (Mean Strategy)'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'key exists in each record',
                           'difficulty': 'Intermediate',
                           'explanation': 'Pandas query and sort_values tabular logic.',
                           'function_name': 'filter_and_sort_records',
                           'hint': 'Use list comprehension then sorted with key=lambda x: x[key], reverse=True.',
                           'id': 'c1-m5-l1-i',
                           'prompt': 'Write `filter_and_sort_records(records, key, min_val)` returning records where '
                                     '`r[key] >= min_val`, sorted descending by `key`.',
                           'solution_code': 'def filter_and_sort_records(records: list, key: str, min_val: float) -> '
                                            'list:\n'
                                            '    filtered = [r for r in records if r[key] >= min_val]\n'
                                            '    return sorted(filtered, key=lambda x: x[key], reverse=True)\n',
                           'starter_code': 'def filter_and_sort_records(records: list, key: str, min_val: float) -> '
                                           'list:\n'
                                           '    # Return filtered and sorted records\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Keeps >= 50 and sorts desc',
                                           'expected': [{'id': 3, 'score': 92}, {'id': 1, 'score': 85}],
                                           'input': [[{'id': 1, 'score': 85},
                                                      {'id': 2, 'score': 40},
                                                      {'id': 3, 'score': 92}],
                                                     'score',
                                                     50]}],
                           'title': 'High-Value Record Filter and Sorter'}},
 (5, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all keys present in records',
                      'difficulty': 'Advance',
                      'explanation': 'Pandas pivot_table cross-tabulation architecture.',
                      'function_name': 'create_pivot_summary',
                      'hint': 'Use nested dictionaries: res.setdefault(r, {}).setdefault(c, 0) += val.',
                      'id': 'c1-m5-l2-a',
                      'prompt': 'Write `create_pivot_summary(records, row_key, col_key, val_key)` producing `{row_val: '
                                '{col_val: total_sum}}`.',
                      'solution_code': 'def create_pivot_summary(records: list, row_key: str, col_key: str, val_key: '
                                       'str) -> dict:\n'
                                       '    res = {}\n'
                                       '    for item in records:\n'
                                       '        r, c, v = item[row_key], item[col_key], item[val_key]\n'
                                       '        res.setdefault(r, {})[c] = res.setdefault(r, {}).get(c, 0) + v\n'
                                       '    return res\n',
                      'starter_code': 'def create_pivot_summary(records: list, row_key: str, col_key: str, val_key: '
                                      'str) -> dict:\n'
                                      '    # Return 2D pivot dictionary\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '2D pivot',
                                      'expected': {'North': {'Q1': 100, 'Q2': 150}, 'South': {'Q1': 80}},
                                      'input': [[{'qtr': 'Q1', 'region': 'North', 'sales': 100},
                                                 {'qtr': 'Q2', 'region': 'North', 'sales': 150},
                                                 {'qtr': 'Q1', 'region': 'South', 'sales': 80}],
                                                'region',
                                                'qtr',
                                                'sales']}],
                      'title': 'Pivot Table 2D Summary Matrix'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'group_key and val_key in all records',
                    'difficulty': 'Basic',
                    'explanation': 'Pandas df.groupby(group_key)[val_key].sum() implementation.',
                    'function_name': 'groupby_aggregate',
                    'hint': 'Iterate records and add salary to dict[dept].',
                    'id': 'c1-m5-l2-b',
                    'prompt': 'Write `groupby_aggregate(records, group_key, val_key)` returning `{group: '
                              'sum_of_vals}`.',
                    'solution_code': 'def groupby_aggregate(records: list, group_key: str, val_key: str) -> dict:\n'
                                     '    res = {}\n'
                                     '    for r in records:\n'
                                     '        k, v = r[group_key], r[val_key]\n'
                                     '        res[k] = res.get(k, 0) + v\n'
                                     '    return res\n',
                    'starter_code': 'def groupby_aggregate(records: list, group_key: str, val_key: str) -> dict:\n'
                                    '    # Return grouped sum dict\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Eng: 220, Sales: 80',
                                    'expected': {'Eng': 220, 'Sales': 80},
                                    'input': [[{'dept': 'Eng', 'salary': 100},
                                               {'dept': 'Sales', 'salary': 80},
                                               {'dept': 'Eng', 'salary': 120}],
                                              'dept',
                                              'salary']}],
                    'title': 'Relational GroupBy Aggregator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'join_key in records',
                           'difficulty': 'Intermediate',
                           'explanation': 'Relational database hash-join algorithm.',
                           'function_name': 'inner_join_tables',
                           'hint': 'Index right_table by join_key, then match against left_table.',
                           'id': 'c1-m5-l2-i',
                           'prompt': 'Write `inner_join_tables(left_table, right_table, join_key)` merging records '
                                     'matching on join_key into combined dicts.',
                           'solution_code': 'def inner_join_tables(left_table: list, right_table: list, join_key: str) '
                                            '-> list:\n'
                                            '    r_map = {r[join_key]: r for r in right_table if join_key in r}\n'
                                            '    res = []\n'
                                            '    for l in left_table:\n'
                                            '        k = l.get(join_key)\n'
                                            '        if k in r_map:\n'
                                            '            merged = dict(l)\n'
                                            '            merged.update(r_map[k])\n'
                                            '            res.append(merged)\n'
                                            '    return res\n',
                           'starter_code': 'def inner_join_tables(left_table: list, right_table: list, join_key: str) '
                                           '-> list:\n'
                                           '    # Return merged joined list of dicts\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Joins id 1',
                                           'expected': [{'id': 1, 'name': 'Alice', 'role': 'Admin'}],
                                           'input': [[{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],
                                                     [{'id': 1, 'role': 'Admin'}, {'id': 3, 'role': 'User'}],
                                                     'id']}],
                           'title': 'Relational Inner Join Simulator'}},
 (6, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(x) == len(y) >= 2',
                      'difficulty': 'Advance',
                      'explanation': 'Seaborn heatmap correlation matrix formula.',
                      'function_name': 'pearson_correlation',
                      'hint': 'Compute mean of x and y, sum((x_i - mean_x) * (y_i - mean_y)) / sqrt(sum_dx2 * '
                              'sum_dy2).',
                      'id': 'c1-m6-l1-a',
                      'prompt': 'Write `pearson_correlation(x, y)`: `cov(x, y) / (std(x) * std(y))`. Round to 4 '
                                'decimals.',
                      'solution_code': 'def pearson_correlation(x: list, y: list) -> float:\n'
                                       '    n = len(x)\n'
                                       '    mx, my = sum(x) / n, sum(y) / n\n'
                                       '    dx = [a - mx for a in x]\n'
                                       '    dy = [b - my for b in y]\n'
                                       '    num = sum(a * b for a, b in zip(dx, dy))\n'
                                       '    den = (sum(a*a for a in dx) * sum(b*b for b in dy)) ** 0.5\n'
                                       '    if den == 0: return 0.0\n'
                                       '    return round(num / den, 4)\n',
                      'starter_code': 'def pearson_correlation(x: list, y: list) -> float:\n'
                                      '    # Return Pearson correlation\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Perfect positive correlation',
                                      'expected': 1.0,
                                      'input': [[1, 2, 3], [2, 4, 6]]}],
                      'title': 'Pearson Correlation Coefficient Matrix'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(data) >= 2, num_bins >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Matplotlib plt.hist binning calculations.',
                    'function_name': 'calculate_histogram_bins',
                    'hint': 'step = (max - min) / num_bins. Add i * step.',
                    'id': 'c1-m6-l1-b',
                    'prompt': 'Write `calculate_histogram_bins(data, num_bins)` returning list of `num_bins + 1` '
                              'boundary floats from min to max rounded to 2 decimals.',
                    'solution_code': 'def calculate_histogram_bins(data: list, num_bins: int) -> list:\n'
                                     '    mn, mx = min(data), max(data)\n'
                                     '    step = (mx - mn) / num_bins\n'
                                     '    return [round(mn + i * step, 2) for i in range(num_bins + 1)]\n',
                    'starter_code': 'def calculate_histogram_bins(data: list, num_bins: int) -> list:\n'
                                    '    # Return bin edges\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '4 bins of width 25',
                                    'expected': [0.0, 25.0, 50.0, 75.0, 100.0],
                                    'input': [[0, 100], 4]}],
                    'title': 'Histogram Bin Boundary Calculator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(values) >= 5',
                           'difficulty': 'Intermediate',
                           'explanation': 'Seaborn boxplot statistical basis.',
                           'function_name': 'five_number_summary',
                           'hint': 'Sort values, calculate median and quartile indices.',
                           'id': 'c1-m6-l1-i',
                           'prompt': 'Write `five_number_summary(values)` returning `{"min": float, "q1": float, '
                                     '"median": float, "q3": float, "max": float}`.',
                           'solution_code': 'def five_number_summary(values: list) -> dict:\n'
                                            '    s = sorted(values)\n'
                                            '    n = len(s)\n'
                                            '    return {"min": float(s[0]), "q1": float(s[n//4]), "median": '
                                            'float(s[n//2]), "q3": float(s[(3*n)//4]), "max": float(s[-1])}\n',
                           'starter_code': 'def five_number_summary(values: list) -> dict:\n'
                                           '    # Return 5-number summary dict\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '5 numbers summary',
                                           'expected': {'max': 5.0, 'median': 3.0, 'min': 1.0, 'q1': 2.0, 'q3': 4.0},
                                           'input': [[1, 2, 3, 4, 5]]}],
                           'title': 'Five-Number Summary (Box Plot Statistics)'}},
 (6, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(values) >= 3',
                      'difficulty': 'Advance',
                      'explanation': 'Measures distribution asymmetry during exploratory data analysis.',
                      'function_name': 'calculate_skewness',
                      'hint': 'Compute mean, median of sorted list, and population std.',
                      'id': 'c1-m6-l2-a',
                      'prompt': 'Write `calculate_skewness(values)` computing Pearson skewness: `(mean - median) / '
                                'std`. Round to 2 decimals.',
                      'solution_code': 'def calculate_skewness(values: list) -> float:\n'
                                       '    s = sorted(values)\n'
                                       '    n = len(s)\n'
                                       '    mean = sum(values) / n\n'
                                       '    median = s[n // 2] if n % 2 != 0 else (s[n // 2 - 1] + s[n // 2]) / 2.0\n'
                                       '    std = (sum((x - mean)**2 for x in values) / n) ** 0.5\n'
                                       '    if std == 0: return 0.0\n'
                                       '    return round((mean - median) / std, 2)\n',
                      'starter_code': 'def calculate_skewness(values: list) -> float:\n'
                                      '    # Return skewness measure\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Positive right-tailed skew',
                                      'expected': 0.61,
                                      'input': [[1, 2, 2, 5, 10]]}],
                      'title': 'Feature Skewness Estimator'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'records is list of dicts',
                    'difficulty': 'Basic',
                    'explanation': 'Automated exploratory data analysis dataset overview.',
                    'function_name': 'generate_eda_summary',
                    'hint': 'Find all keys across records, count None occurrences.',
                    'id': 'c1-m6-l2-b',
                    'prompt': 'Write `generate_eda_summary(records)` returning `{"total_records": N, "column_names": '
                              'sorted_cols, "null_count_per_column": {col: count}}`.',
                    'solution_code': 'def generate_eda_summary(records: list) -> dict:\n'
                                     '    if not records: return {"total_records": 0, "column_names": [], '
                                     '"null_count_per_column": {}}\n'
                                     '    cols = sorted(list({k for r in records for k in r.keys()}))\n'
                                     '    nulls = {c: sum(1 for r in records if r.get(c) is None) for c in cols}\n'
                                     '    return {"total_records": len(records), "column_names": cols, '
                                     '"null_count_per_column": nulls}\n',
                    'starter_code': 'def generate_eda_summary(records: list) -> dict:\n'
                                    '    # Return profiling summary\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Profiles 2 records',
                                    'expected': {'column_names': ['a', 'b'],
                                                 'null_count_per_column': {'a': 0, 'b': 1},
                                                 'total_records': 2},
                                    'input': [[{'a': 1, 'b': None}, {'a': 2, 'b': 'x'}]]}],
                    'title': 'EDA Dataset Summary Profiler'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(values) >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Feature engineering standard scaler for machine learning inputs.',
                           'function_name': 'standardize_features',
                           'hint': 'Calculate mean and sample/pop standard deviation.',
                           'id': 'c1-m6-l2-i',
                           'prompt': 'Write `standardize_features(values)` returning `(x - mean) / std` for each value '
                                     'rounded to 2 decimals. If std is 0 return all 0.0.',
                           'solution_code': 'def standardize_features(values: list) -> list:\n'
                                            '    n = len(values)\n'
                                            '    mean = sum(values) / n\n'
                                            '    var = sum((x - mean) ** 2 for x in values) / n\n'
                                            '    std = var ** 0.5\n'
                                            '    if std == 0: return [0.0] * n\n'
                                            '    return [round((x - mean) / std, 2) for x in values]\n',
                           'starter_code': 'def standardize_features(values: list) -> list:\n'
                                           '    # Return standardized z-scores\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Standardizes 10, 20, 30',
                                           'expected': [-1.22, 0.0, 1.22],
                                           'input': [[10, 20, 30]]}],
                           'title': 'Z-Score Feature Standardization'}}}
