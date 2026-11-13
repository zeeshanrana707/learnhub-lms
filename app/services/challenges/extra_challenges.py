# Specific, handcrafted 3-tier challenges for differentiated curriculum topics
EXTRA_CHALLENGES = {
    (1, 1, 3): {
        'basic': {
            'id': 'c1-m1-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Collatz Sequence Step Counter',
            'function_name': 'collatz_steps',
            'prompt': 'Write a function `collatz_steps(n)` that returns the number of steps to reach 1: if n is even `n //= 2`, else `n = 3*n + 1`.',
            'constraints': 'n >= 1',
            'starter_code': 'def collatz_steps(n: int) -> int:\n    # Return step count\n    pass\n',
            'test_cases': [{'desc': 'n=6 steps', 'input': [6], 'expected': 8}, {'desc': 'n=1 is 0', 'input': [1], 'expected': 0}, {'desc': 'n=2 is 1', 'input': [2], 'expected': 1}],
            'hint': 'Use a while loop condition `while n > 1:` and increment a step counter.',
            'solution_code': 'def collatz_steps(n: int) -> int:\n    steps = 0\n    while n > 1:\n        if n % 2 == 0: n //= 2\n        else: n = 3 * n + 1\n        steps += 1\n    return steps\n',
            'explanation': 'Classic algorithmic demonstration of while loops and convergence.'
        },
        'intermediate': {
            'id': 'c1-m1-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Filter Prime Numbers with While Loop',
            'function_name': 'is_prime_number',
            'prompt': 'Write `is_prime_number(n)` returning True if n is prime, False otherwise.',
            'constraints': 'n >= 1',
            'starter_code': 'def is_prime_number(n: int) -> bool:\n    pass\n',
            'test_cases': [{'desc': '7 is prime', 'input': [7], 'expected': True}, {'desc': '4 is not', 'input': [4], 'expected': False}, {'desc': '1 is not', 'input': [1], 'expected': False}],
            'hint': 'If n <= 1 return False. Check divisibility up to int(n**0.5) + 1.',
            'solution_code': 'def is_prime_number(n: int) -> bool:\n    if n <= 1: return False\n    d = 2\n    while d * d <= n:\n        if n % d == 0: return False\n        d += 1\n    return True\n',
            'explanation': 'Trial division prime checking with O(sqrt(N)) loop mechanics.'
        },
        'advance': {
            'id': 'c1-m1-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Fibonacci Sequence Generator with While Loop',
            'function_name': 'generate_fibonacci',
            'prompt': 'Write `generate_fibonacci(limit)` returning list of all Fibonacci numbers less than or equal to limit.',
            'constraints': 'limit >= 0',
            'starter_code': 'def generate_fibonacci(limit: int) -> list:\n    pass\n',
            'test_cases': [{'desc': 'limit 20', 'input': [20], 'expected': [0, 1, 1, 2, 3, 5, 8, 13]}],
            'hint': 'a, b = 0, 1. while a <= limit: fibs.append(a); a, b = b, a + b.',
            'solution_code': 'def generate_fibonacci(limit: int) -> list:\n    a, b = 0, 1\n    res = []\n    while a <= limit:\n        res.append(a)\n        a, b = b, a + b\n    return res\n',
            'explanation': 'Fundamental dynamic iterative accumulator.'
        }
    },
    (1, 2, 3): {
        'basic': {
            'id': 'c1-m2-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Square Odd Numbers with List Comprehension',
            'function_name': 'filter_square_odds',
            'prompt': 'Write `filter_square_odds(numbers)` using a list comprehension that squares all odd numbers in `numbers`.',
            'constraints': 'numbers is list of ints',
            'starter_code': 'def filter_square_odds(numbers: list) -> list:\n    # Return list comprehension\n    pass\n',
            'test_cases': [{'desc': 'Square odds', 'input': [[1, 2, 3, 4, 5]], 'expected': [1, 9, 25]}, {'desc': 'No odds', 'input': [[2, 4]], 'expected': []}],
            'hint': 'Use `[x**2 for x in numbers if x % 2 != 0]`.',
            'solution_code': 'def filter_square_odds(numbers: list) -> list:\n    return [x ** 2 for x in numbers if x % 2 != 0]\n',
            'explanation': 'Idiomatic Pythonic conditional list comprehension.'
        },
        'intermediate': {
            'id': 'c1-m2-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Matrix Transpose via Nested Comprehension',
            'function_name': 'transpose_matrix',
            'prompt': 'Write `transpose_matrix(matrix)` that swaps rows and columns of a 2D matrix using nested list comprehension.',
            'constraints': 'rectangular non-empty 2D list',
            'starter_code': 'def transpose_matrix(matrix: list) -> list:\n    pass\n',
            'test_cases': [{'desc': '2x3 to 3x2', 'input': [[[1, 2, 3], [4, 5, 6]]], 'expected': [[1, 4], [2, 5], [3, 6]]}],
            'hint': '`[[row[i] for row in matrix] for i in range(len(matrix[0]))]`.',
            'solution_code': 'def transpose_matrix(matrix: list) -> list:\n    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]\n',
            'explanation': 'Essential array manipulation in linear algebra preprocessing.'
        },
        'advance': {
            'id': 'c1-m2-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Dynamic Lambda Filter Closure Generator',
            'function_name': 'create_range_filter',
            'prompt': 'Write `create_range_filter(low, high)` returning a function `filter_fn(numbers)` that returns only numbers where `low <= x <= high`.',
            'constraints': 'low <= high',
            'starter_code': 'def create_range_filter(low: float, high: float):\n    pass\n',
            'test_cases': [{'desc': 'Filter in range', 'input': [10, 20], 'expected': [10, 15, 20]}],
            'hint': 'Return a closure lambda or function capturing low and high.',
            'solution_code': 'def create_range_filter(low: float, high: float):\n    return lambda nums: [x for x in nums if low <= x <= high]\n',
            'explanation': 'Demonstrates functional closures and higher-order functions in Python.'
        }
    },
    (1, 3, 3): {
        'basic': {
            'id': 'c1-m3-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Polymorphic Employee Compensation Calculator',
            'function_name': 'calculate_employee_pay',
            'prompt': 'Write `calculate_employee_pay(role, base_salary, hours)`: if role=="manager", pay is `base_salary + 50 * max(0, hours - 40)`; if role=="engineer", `base_salary * 1.15`; else `base_salary`. Round to 2 decimals.',
            'constraints': 'base_salary >= 0, hours >= 0',
            'starter_code': 'def calculate_employee_pay(role: str, base_salary: float, hours: float) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Manager overtime', 'input': ['manager', 5000.0, 45.0], 'expected': 5250.0}, {'desc': 'Engineer multiplier', 'input': ['engineer', 6000.0, 40.0], 'expected': 6900.0}],
            'hint': 'Use if-elif-else branching to compute compensation.',
            'solution_code': 'def calculate_employee_pay(role: str, base_salary: float, hours: float) -> float:\n    if role.lower() == "manager": return round(base_salary + 50 * max(0, hours - 40), 2)\n    elif role.lower() == "engineer": return round(base_salary * 1.15, 2)\n    return round(base_salary, 2)\n',
            'explanation': 'Illustrates polymorphic domain logic and method overriding.'
        },
        'intermediate': {
            'id': 'c1-m3-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Shape Area Polymorphism Dispatcher',
            'function_name': 'compute_shape_area',
            'prompt': 'Write `compute_shape_area(shape_type, dimensions)`: if "circle" with dimensions=[r], return `3.14159 * r**2`; if "rectangle" with [w, h], return `w * h`. Round to 2 decimals.',
            'constraints': 'dimensions is list of positive floats',
            'starter_code': 'def compute_shape_area(shape_type: str, dimensions: list) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Circle', 'input': ['circle', [5]], 'expected': 78.54}, {'desc': 'Rectangle', 'input': ['rectangle', [4, 6]], 'expected': 24.0}],
            'hint': 'Check shape_type and apply the geometric formula.',
            'solution_code': 'def compute_shape_area(shape_type: str, dimensions: list) -> float:\n    if shape_type.lower() == "circle": return round(3.14159 * (dimensions[0] ** 2), 2)\n    elif shape_type.lower() == "rectangle": return round(dimensions[0] * dimensions[1], 2)\n    return 0.0\n',
            'explanation': 'Classic polymorphic shape hierarchy.'
        },
        'advance': {
            'id': 'c1-m3-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Method Resolution Order (MRO) Simulator',
            'function_name': 'resolve_attribute_hierarchy',
            'prompt': 'Write `resolve_attribute_hierarchy(class_hierarchy, attribute)`: class_hierarchy is a list of dicts representing classes from child to parent. Return the attribute value from the first class that defines it, or None.',
            'constraints': 'class_hierarchy is list of dicts',
            'starter_code': 'def resolve_attribute_hierarchy(class_hierarchy: list, attribute: str):\n    pass\n',
            'test_cases': [{'desc': 'Finds first defined', 'input': [[{'title': 'SubClass'}, {'title': 'BaseClass', 'timeout': 30}], 'timeout'], 'expected': 30}],
            'hint': 'Loop through class_hierarchy and return c[attribute] if attribute in c.',
            'solution_code': 'def resolve_attribute_hierarchy(class_hierarchy: list, attribute: str):\n    for c in class_hierarchy:\n        if attribute in c: return c[attribute]\n    return None\n',
            'explanation': 'Simulates Python C3 Linearization / MRO attribute lookup.'
        }
    },
    (1, 4, 3): {
        'basic': {
            'id': 'c1-m4-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Row-wise Probability Normalizer',
            'function_name': 'normalize_feature_matrix',
            'prompt': 'Write `normalize_feature_matrix(matrix)` dividing each cell by its row sum. Round to 2 decimals. If row sum is 0, return row unmodified.',
            'constraints': '2D list of numbers',
            'starter_code': 'def normalize_feature_matrix(matrix: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Row sums', 'input': [[[2, 2], [1, 3]]], 'expected': [[0.5, 0.5], [0.25, 0.75]]}],
            'hint': 'For each row: s = sum(row); return [round(x/s, 2) for x in row] if s else row.',
            'solution_code': 'def normalize_feature_matrix(matrix: list) -> list:\n    res = []\n    for row in matrix:\n        s = sum(row)\n        if s == 0: res.append(row)\n        else: res.append([round(x / s, 2) for x in row])\n    return res\n',
            'explanation': 'Simulates NumPy 2D array broadcasting across axis 1.'
        },
        'intermediate': {
            'id': 'c1-m4-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Broadcasting Mean Subtraction (Centering)',
            'function_name': 'center_feature_columns',
            'prompt': 'Write `center_feature_columns(matrix)` subtracting each column mean from its elements. Round to 2 decimals.',
            'constraints': 'Non-empty 2D list',
            'starter_code': 'def center_feature_columns(matrix: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Center 2x2', 'input': [[[2, 4], [4, 6]]], 'expected': [[-1.0, -1.0], [1.0, 1.0]]}],
            'hint': 'Calculate mean of each column j: sum(matrix[i][j] for i in range(rows)) / rows.',
            'solution_code': 'def center_feature_columns(matrix: list) -> list:\n    rows = len(matrix)\n    cols = len(matrix[0])\n    col_means = [sum(matrix[r][c] for r in range(rows)) / rows for c in range(cols)]\n    return [[round(matrix[r][c] - col_means[c], 2) for c in range(cols)] for r in range(rows)]\n',
            'explanation': 'Column-wise zero-mean centering used in PCA and normalization.'
        },
        'advance': {
            'id': 'c1-m4-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Pairwise Euclidean Distance Matrix',
            'function_name': 'pairwise_euclidean_distances',
            'prompt': 'Write `pairwise_euclidean_distances(points)` computing distance between all pairs. Round to 2 decimals.',
            'constraints': 'points is list of [x, y] coordinates',
            'starter_code': 'def pairwise_euclidean_distances(points: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Two points', 'input': [[[0, 0], [3, 4]]], 'expected': [[0.0, 5.0], [5.0, 0.0]]}],
            'hint': 'dist = sqrt((x1-x2)**2 + (y1-y2)**2).',
            'solution_code': 'def pairwise_euclidean_distances(points: list) -> list:\n    res = []\n    for p1 in points:\n        row = []\n        for p2 in points:\n            d = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5\n            row.append(round(d, 2))\n        res.append(row)\n    return res\n',
            'explanation': 'Pairwise kernel distance computation in vector spaces.'
        }
    },
    (1, 5, 3): {
        'basic': {
            'id': 'c1-m5-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Histogram Frequency Bins Calculator',
            'function_name': 'calculate_histogram_bins',
            'prompt': 'Write `calculate_histogram_bins(data, num_bins)` returning `{"min": ..., "max": ..., "bin_width": ...}` rounded to 2 decimals.',
            'constraints': 'len(data) >= 1, num_bins >= 1',
            'starter_code': 'def calculate_histogram_bins(data: list, num_bins: int) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'Equal bins', 'input': [[0, 10, 20], 2], 'expected': {'min': 0.0, 'max': 20.0, 'bin_width': 10.0}}],
            'hint': 'bin_width = (max_val - min_val) / num_bins.',
            'solution_code': 'def calculate_histogram_bins(data: list, num_bins: int) -> dict:\n    mn = float(min(data))\n    mx = float(max(data))\n    w = round((mx - mn) / num_bins, 2)\n    return {"min": round(mn, 2), "max": round(mx, 2), "bin_width": w}\n',
            'explanation': 'Matplotlib plt.hist() bin spacing calculation.'
        },
        'intermediate': {
            'id': 'c1-m5-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Boxplot Five-Number Summary and Whiskers',
            'function_name': 'boxplot_statistics',
            'prompt': 'Write `boxplot_statistics(data)` returning `{"q1": ..., "median": ..., "q3": ..., "iqr": ...}` for sorted data. Round to 2 decimals.',
            'constraints': 'len(data) >= 4',
            'starter_code': 'def boxplot_statistics(data: list) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'Quartiles', 'input': [[1, 2, 3, 4, 5, 6, 7, 8]], 'expected': {'q1': 2.5, 'median': 4.5, 'q3': 6.5, 'iqr': 4.0}}],
            'hint': 'Calculate medians of lower half (Q1) and upper half (Q3).',
            'solution_code': 'def boxplot_statistics(data: list) -> dict:\n    s = sorted(data)\n    n = len(s)\n    mid = n // 2\n    med = (s[mid-1] + s[mid]) / 2 if n % 2 == 0 else float(s[mid])\n    lower = s[:mid]\n    upper = s[mid:] if n % 2 == 0 else s[mid+1:]\n    q1 = (lower[len(lower)//2-1] + lower[len(lower)//2])/2 if len(lower)%2==0 else float(lower[len(lower)//2])\n    q3 = (upper[len(upper)//2-1] + upper[len(upper)//2])/2 if len(upper)%2==0 else float(upper[len(upper)//2])\n    return {"q1": round(q1, 2), "median": round(med, 2), "q3": round(q3, 2), "iqr": round(q3 - q1, 2)}\n',
            'explanation': 'Seaborn boxplot five-number summary.'
        },
        'advance': {
            'id': 'c1-m5-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Kernel Density Estimation (KDE) Smoother',
            'function_name': 'gaussian_kde_point',
            'prompt': 'Write `gaussian_kde_point(sample, eval_point, bandwidth)` returning the estimated density value at eval_point using Gaussian kernel.',
            'constraints': 'bandwidth > 0',
            'starter_code': 'def gaussian_kde_point(sample: list, eval_point: float, bandwidth: float) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Point estimate', 'input': [[0.0, 1.0], 0.5, 1.0], 'expected': 0.35}],
            'hint': 'Kernel k(u) = (1/sqrt(2*pi)) * exp(-0.5 * u^2). Sum over sample and divide by N*bandwidth.',
            'solution_code': 'def gaussian_kde_point(sample: list, eval_point: float, bandwidth: float) -> float:\n    import math\n    n = len(sample)\n    c = 1.0 / (math.sqrt(2 * math.pi))\n    tot = sum(c * math.exp(-0.5 * (((eval_point - xi) / bandwidth) ** 2)) for xi in sample)\n    return round(tot / (n * bandwidth), 2)\n',
            'explanation': 'Core math of Seaborn kdeplot().'
        }
    },
    (1, 5, 4): {
        'basic': {
            'id': 'c1-m5-l4-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Dataset Missing Value Audit Report',
            'function_name': 'audit_missing_values',
            'prompt': 'Write `audit_missing_values(records)` that inspects a list of dicts and returns a dict mapping column name to its count of None values.',
            'constraints': 'records is list of dicts',
            'starter_code': 'def audit_missing_values(records: list) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'Audit columns', 'input': [[{'age': 25, 'name': 'Ann'}, {'age': None, 'name': 'Bob'}]], 'expected': {'age': 1, 'name': 0}}],
            'hint': 'Loop records and count None values for each key.',
            'solution_code': 'def audit_missing_values(records: list) -> dict:\n    if not records: return {}\n    keys = records[0].keys()\n    return {k: sum(1 for r in records if r.get(k) is None) for k in keys}\n',
            'explanation': 'EDA standard df.isnull().sum() equivalent.'
        },
        'intermediate': {
            'id': 'c1-m5-l4-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Categorical Cardinality & Frequency Counter',
            'function_name': 'column_cardinality',
            'prompt': 'Write `column_cardinality(records, column)` returning dict `{"unique_count": ..., "frequencies": {val: count}}`.',
            'constraints': 'column exists in records',
            'starter_code': 'def column_cardinality(records: list, column: str) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'Counts', 'input': [[{'cat': 'A'}, {'cat': 'B'}, {'cat': 'A'}], 'cat'], 'expected': {'unique_count': 2, 'frequencies': {'A': 2, 'B': 1}}}],
            'hint': 'Count occurrences using a dict or collections.Counter.',
            'solution_code': 'def column_cardinality(records: list, column: str) -> dict:\n    freq = {}\n    for r in records:\n        v = r[column]\n        freq[v] = freq.get(v, 0) + 1\n    return {"unique_count": len(freq), "frequencies": freq}\n',
            'explanation': 'EDA value_counts() and unique cardinality inspection.'
        },
        'advance': {
            'id': 'c1-m5-l4-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Outlier Capping via Winsorization',
            'function_name': 'winsorize_column',
            'prompt': 'Write `winsorize_column(values, lower_pct, upper_pct)` replacing values below lower percentile and above upper percentile with the threshold values. Round to 2 decimals.',
            'constraints': '0 <= lower_pct < upper_pct <= 1',
            'starter_code': 'def winsorize_column(values: list, lower_pct: float, upper_pct: float) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Cap values', 'input': [[1, 2, 3, 4, 5, 100], 0.1, 0.8], 'expected': [1, 2, 3, 4, 5, 5]}],
            'hint': 'Sort values. lower_val = sorted_v[int(lower_pct*N)], upper_val = sorted_v[int(upper_pct*N)].',
            'solution_code': 'def winsorize_column(values: list, lower_pct: float, upper_pct: float) -> list:\n    s = sorted(values)\n    n = len(s)\n    low = s[int(lower_pct * (n - 1))]\n    high = s[int(upper_pct * (n - 1))]\n    return [low if x < low else high if x > high else x for x in values]\n',
            'explanation': 'Production EDA winsorization for robust statistical models.'
        }
    },
    (2, 2, 3): {
        'basic': {
            'id': 'c2-m2-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Mean Absolute Error (MAE) Metric',
            'function_name': 'calculate_mae',
            'prompt': 'Write `calculate_mae(actual, predicted)` calculating Mean Absolute Error `sum(|actual - predicted|) / N`. Round to 2 decimals.',
            'constraints': 'len(actual) == len(predicted) >= 1',
            'starter_code': 'def calculate_mae(actual: list, predicted: list) -> float:\n    pass\n',
            'test_cases': [{'desc': 'MAE', 'input': [[3.0, -0.5, 2.0, 7.0], [2.5, 0.0, 2.0, 8.0]], 'expected': 0.5}],
            'hint': 'sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual).',
            'solution_code': 'def calculate_mae(actual: list, predicted: list) -> float:\n    n = len(actual)\n    return round(sum(abs(a - p) for a, p in zip(actual, predicted)) / n, 2)\n',
            'explanation': 'Robust linear regression metric resilient to extreme outliers.'
        },
        'intermediate': {
            'id': 'c2-m2-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Root Mean Squared Error (RMSE) Calculator',
            'function_name': 'calculate_rmse',
            'prompt': 'Write `calculate_rmse(actual, predicted)` calculating `sqrt(sum((actual - predicted)**2) / N)`. Round to 2 decimals.',
            'constraints': 'len(actual) == len(predicted) >= 1',
            'starter_code': 'def calculate_rmse(actual: list, predicted: list) -> float:\n    pass\n',
            'test_cases': [{'desc': 'RMSE', 'input': [[3.0, -0.5, 2.0, 7.0], [2.5, 0.0, 2.0, 8.0]], 'expected': 0.61}],
            'hint': 'Compute MSE, then return round(mse ** 0.5, 2).',
            'solution_code': 'def calculate_rmse(actual: list, predicted: list) -> float:\n    n = len(actual)\n    mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n\n    return round(mse ** 0.5, 2)\n',
            'explanation': 'Penalizes large errors heavily, sharing units with the target.'
        },
        'advance': {
            'id': 'c2-m2-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'R-Squared (Coefficient of Determination) Metric',
            'function_name': 'calculate_r2_score',
            'prompt': 'Write `calculate_r2_score(actual, predicted)` returning `1 - (SS_res / SS_tot)`. Round to 2 decimals.',
            'constraints': 'len(actual) >= 2',
            'starter_code': 'def calculate_r2_score(actual: list, predicted: list) -> float:\n    pass\n',
            'test_cases': [{'desc': 'R2 score', 'input': [[1.0, 2.0, 3.0], [1.1, 1.9, 3.2]], 'expected': 0.98}],
            'hint': 'SS_res = sum((a - p)**2); mean_a = sum(a)/N; SS_tot = sum((a - mean_a)**2).',
            'solution_code': 'def calculate_r2_score(actual: list, predicted: list) -> float:\n    mean_a = sum(actual) / len(actual)\n    ss_res = sum((a - p) ** 2 for a, p in zip(actual, predicted))\n    ss_tot = sum((a - mean_a) ** 2 for a in actual)\n    if ss_tot == 0: return 1.0\n    return round(1.0 - (ss_res / ss_tot), 2)\n',
            'explanation': 'Measures variance explained by regression model.'
        }
    },
    (4, 3, 4): {
        'basic': {
            'id': 'c4-m3-l4-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'RAG Retrieval Recall@K Metric',
            'function_name': 'calculate_recall_at_k',
            'prompt': 'Write `calculate_recall_at_k(retrieved_ids, relevant_ids, k)` returning proportion of relevant_ids found in the top k retrieved_ids. Round to 2 decimals.',
            'constraints': 'k >= 1, relevant_ids non-empty',
            'starter_code': 'def calculate_recall_at_k(retrieved_ids: list, relevant_ids: list, k: int) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Recall@3', 'input': [[1, 2, 3, 4], [2, 5], 3], 'expected': 0.5}],
            'hint': 'top_k = set(retrieved_ids[:k]). Count how many relevant_ids are in top_k.',
            'solution_code': 'def calculate_recall_at_k(retrieved_ids: list, relevant_ids: list, k: int) -> float:\n    top_k = set(retrieved_ids[:k])\n    hits = sum(1 for rid in relevant_ids if rid in top_k)\n    return round(hits / len(relevant_ids), 2)\n',
            'explanation': 'Core retrieval evaluation metric for enterprise RAG benchmarks.'
        },
        'intermediate': {
            'id': 'c4-m3-l4-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Mean Reciprocal Rank (MRR) RAG Evaluator',
            'function_name': 'calculate_mrr',
            'prompt': 'Write `calculate_mrr(rankings, target_id)` returning `1.0 / rank` (1-indexed) of target_id in rankings. If not found, return 0.0. Round to 2 decimals.',
            'constraints': 'rankings is list of IDs',
            'starter_code': 'def calculate_mrr(rankings: list, target_id: int) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Found at pos 2', 'input': [[10, 20, 30], 20], 'expected': 0.5}, {'desc': 'Not found', 'input': [[10, 30], 20], 'expected': 0.0}],
            'hint': 'Find index of target_id. Rank = index + 1.',
            'solution_code': 'def calculate_mrr(rankings: list, target_id: int) -> float:\n    if target_id not in rankings: return 0.0\n    rank = rankings.index(target_id) + 1\n    return round(1.0 / rank, 2)\n',
            'explanation': 'MRR measures ranking efficiency for conversational search engines.'
        },
        'advance': {
            'id': 'c4-m3-l4-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'RAG Hallucination Detection Overlap Ratio',
            'function_name': 'citation_grounding_score',
            'prompt': 'Write `citation_grounding_score(answer_keywords, source_context_text)` returning proportion of answer_keywords found in source_context_text (case-insensitive). Round to 2 decimals.',
            'constraints': 'answer_keywords is list of str',
            'starter_code': 'def citation_grounding_score(answer_keywords: list, source_context_text: str) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Grounding 2/3', 'input': [['transformer', 'attention', 'quantum'], 'The transformer uses attention mechanisms.'], 'expected': 0.67}],
            'hint': 'Convert source_context_text to lower(). Check if each kw.lower() is in it.',
            'solution_code': 'def citation_grounding_score(answer_keywords: list, source_context_text: str) -> float:\n    txt = source_context_text.lower()\n    hits = sum(1 for kw in answer_keywords if kw.lower() in txt)\n    return round(hits / len(answer_keywords), 2) if answer_keywords else 1.0\n',
            'explanation': 'RAG Triad metric verifying factual consistency against context.'
        }
    },
    (11, 4, 3): {
        'basic': {
            'id': 'c11-m4-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'TLS Cipher Suite Negotiation Evaluator',
            'function_name': 'negotiate_tls_cipher',
            'prompt': 'Write `negotiate_tls_cipher(client_ciphers, server_preference_list)` returning first cipher in server_preference_list supported by client. If none match, return "HANDSHAKE_FAILURE".',
            'constraints': 'Lists of string cipher names',
            'starter_code': 'def negotiate_tls_cipher(client_ciphers: list, server_preference_list: list) -> str:\n    pass\n',
            'test_cases': [{'desc': 'Negotiate preferred', 'input': [['AES128', 'CHACHA20'], ['AES256', 'AES128']], 'expected': 'AES128'}, {'desc': 'No match', 'input': [['DES'], ['AES256']], 'expected': 'HANDSHAKE_FAILURE'}],
            'hint': 'Loop server_preference_list and check if cipher in set(client_ciphers).',
            'solution_code': 'def negotiate_tls_cipher(client_ciphers: list, server_preference_list: list) -> str:\n    client_set = set(client_ciphers)\n    for s in server_preference_list:\n        if s in client_set: return s\n    return "HANDSHAKE_FAILURE"\n',
            'explanation': 'Simulates TLS 1.3 ClientHello / ServerHello cipher negotiation.'
        },
        'intermediate': {
            'id': 'c11-m4-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'X.509 Certificate Validity Window Checker',
            'function_name': 'validate_cert_validity',
            'prompt': 'Write `validate_cert_validity(not_before_epoch, not_after_epoch, current_epoch)` returning "VALID", "NOT_YET_VALID", or "EXPIRED".',
            'constraints': 'Epoch timestamps in seconds',
            'starter_code': 'def validate_cert_validity(not_before_epoch: int, not_after_epoch: int, current_epoch: int) -> str:\n    pass\n',
            'test_cases': [{'desc': 'Valid', 'input': [1000, 2000, 1500], 'expected': 'VALID'}, {'desc': 'Expired', 'input': [1000, 2000, 2500], 'expected': 'EXPIRED'}],
            'hint': 'Compare current_epoch against bounds.',
            'solution_code': 'def validate_cert_validity(not_before_epoch: int, not_after_epoch: int, current_epoch: int) -> str:\n    if current_epoch < not_before_epoch: return "NOT_YET_VALID"\n    elif current_epoch > not_after_epoch: return "EXPIRED"\n    return "VALID"\n',
            'explanation': 'RFC 5280 PKI certificate path validation step.'
        },
        'advance': {
            'id': 'c11-m4-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Diffie-Hellman Shared Secret Computation',
            'function_name': 'diffie_hellman_shared_secret',
            'prompt': 'Write `diffie_hellman_shared_secret(public_key, private_key, prime_modulus)` computing `pow(public_key, private_key, prime_modulus)`.',
            'constraints': 'Positive integers',
            'starter_code': 'def diffie_hellman_shared_secret(public_key: int, private_key: int, prime_modulus: int) -> int:\n    pass\n',
            'test_cases': [{'desc': 'DH Secret', 'input': [8, 6, 23], 'expected': 2}],
            'hint': 'Use Python built-in 3-argument pow(a, b, m).',
            'solution_code': 'def diffie_hellman_shared_secret(public_key: int, private_key: int, prime_modulus: int) -> int:\n    return pow(public_key, private_key, prime_modulus)\n',
            'explanation': 'Ephemeral Diffie-Hellman key exchange for TLS 1.3 Perfect Forward Secrecy.'
        }
    },
    (13, 1, 3): {
        'basic': {
            'id': 'c13-m1-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Modular Multiplicative Inverse (Finite Fields)',
            'function_name': 'modular_multiplicative_inverse',
            'prompt': 'Write `modular_multiplicative_inverse(a, m)` computing inv such that `(a * inv) % m == 1`. Return inv in range `[1, m-1]`.',
            'constraints': 'gcd(a, m) == 1',
            'starter_code': 'def modular_multiplicative_inverse(a: int, m: int) -> int:\n    pass\n',
            'test_cases': [{'desc': '3 mod 11', 'input': [3, 11], 'expected': 4}],
            'hint': 'Use pow(a, -1, m) in Python 3.8+.',
            'solution_code': 'def modular_multiplicative_inverse(a: int, m: int) -> int:\n    return pow(a, -1, m)\n',
            'explanation': 'Core arithmetic primitive in Elliptic Curve point doubling and slope.'
        },
        'intermediate': {
            'id': 'c13-m1-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'ECC Curve Point Membership Verification',
            'function_name': 'is_point_on_elliptic_curve',
            'prompt': 'Write `is_point_on_elliptic_curve(point, a, b, p)` checking if `y**2 % p == (x**3 + a*x + b) % p`. Point is `(x, y)`.',
            'constraints': 'Coordinates are integers in [0, p-1]',
            'starter_code': 'def is_point_on_elliptic_curve(point: tuple, a: int, b: int, p: int) -> bool:\n    pass\n',
            'test_cases': [{'desc': 'Point on curve', 'input': [(2, 7), 2, 3, 97], 'expected': False}, {'desc': 'Point on secp256k1 base', 'input': [(0, 1), 0, 1, 5], 'expected': True}],
            'hint': 'Calculate lhs = (y**2)%p, rhs = (x**3 + a*x + b)%p.',
            'solution_code': 'def is_point_on_elliptic_curve(point: tuple, a: int, b: int, p: int) -> bool:\n    x, y = point\n    return (y ** 2) % p == (x ** 3 + a * x + b) % p\n',
            'explanation': 'Weierstrass normal form curve validation.'
        },
        'advance': {
            'id': 'c13-m1-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Elliptic Curve Point Doubling Algorithm',
            'function_name': 'ecc_double_point',
            'prompt': 'Write `ecc_double_point(point, a, p)` computing `2*P` on Weierstrass curve: slope `s = (3*x^2 + a) * pow(2*y, -1, p) % p`; `xr = (s^2 - 2*x) % p`; `yr = (s*(x - xr) - y) % p`.',
            'constraints': 'point has y != 0',
            'starter_code': 'def ecc_double_point(point: tuple, a: int, p: int) -> tuple:\n    pass\n',
            'test_cases': [{'desc': 'Double (0, 1) on y^2=x^3+1 mod 5', 'input': [(0, 1), 0, 5], 'expected': (0, 4)}],
            'hint': 'Use pow(2 * y, -1, p) for modular division.',
            'solution_code': 'def ecc_double_point(point: tuple, a: int, p: int) -> tuple:\n    x, y = point\n    s = ((3 * x * x + a) * pow(2 * y, -1, p)) % p\n    xr = (s * s - 2 * x) % p\n    yr = (s * (x - xr) - y) % p\n    return (xr, yr)\n',
            'explanation': 'Group law point doubling for secp256k1 ECDSA cryptography.'
        }
    },
    (13, 2, 3): {
        'basic': {
            'id': 'c13-m2-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'HMAC Timing-Safe Digest Verification',
            'function_name': 'constant_time_compare',
            'prompt': 'Write `constant_time_compare(val1, val2)` comparing two strings without early exit to prevent timing attack vulnerabilities.',
            'constraints': 'Strings of ASCII characters',
            'starter_code': 'def constant_time_compare(val1: str, val2: str) -> bool:\n    pass\n',
            'test_cases': [{'desc': 'Equal strings', 'input': ['token123', 'token123'], 'expected': True}, {'desc': 'Different strings', 'input': ['token123', 'token456'], 'expected': False}],
            'hint': 'Use hmac.compare_digest(val1, val2) or XOR accumulator.',
            'solution_code': 'def constant_time_compare(val1: str, val2: str) -> bool:\n    import hmac\n    return hmac.compare_digest(val1, val2)\n',
            'explanation': 'Industry standard protection against side-channel timing attacks.'
        },
        'intermediate': {
            'id': 'c13-m2-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'SHA-256 Message Digest Hex Formatter',
            'function_name': 'compute_sha256_hex',
            'prompt': 'Write `compute_sha256_hex(text)` returning the 64-character lowercase hex string of hashlib.sha256(text.encode()).hexdigest().',
            'constraints': 'text is string',
            'starter_code': 'def compute_sha256_hex(text: str) -> str:\n    pass\n',
            'test_cases': [{'desc': 'Hash empty', 'input': [''], 'expected': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}],
            'hint': 'import hashlib; hashlib.sha256(text.encode()).hexdigest().',
            'solution_code': 'def compute_sha256_hex(text: str) -> str:\n    import hashlib\n    return hashlib.sha256(text.encode("utf-8")).hexdigest()\n',
            'explanation': 'Cryptographic hashing provides tamper-evident integrity.'
        },
        'advance': {
            'id': 'c13-m2-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'HMAC-SHA256 Token Signer',
            'function_name': 'generate_hmac_sha256',
            'prompt': 'Write `generate_hmac_sha256(key, message)` returning hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest().',
            'constraints': 'key and message are non-empty strings',
            'starter_code': 'def generate_hmac_sha256(key: str, message: str) -> str:\n    pass\n',
            'test_cases': [{'desc': 'HMAC sign', 'input': ['secret_key', 'hello_world'], 'expected': 'c24b611eecf8482594a11be0a5ef04abf6479032ad8d2645ca3a886df9a5ec99'}],
            'hint': 'import hmac, hashlib; return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest().',
            'solution_code': 'def generate_hmac_sha256(key: str, message: str) -> str:\n    import hmac, hashlib\n    return hmac.new(key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()\n',
            'explanation': 'Message Authentication Code ensures authenticity and data integrity.'
        }
    },
    (13, 4, 1): {
        'basic': {
            'id': 'c13-m4-l1-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'x86 Stack Frame Displacement Calculator',
            'function_name': 'calculate_frame_size',
            'prompt': 'Write `calculate_frame_size(ebp, esp)` returning stack size `ebp - esp` in bytes and the count of 32-bit (4-byte) DWORD words.',
            'constraints': 'ebp >= esp >= 0',
            'starter_code': 'def calculate_frame_size(ebp: int, esp: int) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'Frame 32 bytes', 'input': [0x1000, 0x0FE0], 'expected': {'bytes': 32, 'dwords': 8}}],
            'hint': 'diff = ebp - esp; return {"bytes": diff, "dwords": diff // 4}.',
            'solution_code': 'def calculate_frame_size(ebp: int, esp: int) -> dict:\n    diff = ebp - esp\n    return {"bytes": diff, "dwords": diff // 4}\n',
            'explanation': 'Calculates function local variable space allocated by `sub esp, N`.'
        },
        'intermediate': {
            'id': 'c13-m4-l1-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'System V x64 Calling Convention Register Allocator',
            'function_name': 'map_x64_arg_registers',
            'prompt': 'Write `map_x64_arg_registers(args_list)` mapping first 6 integer args to registers: `["RDI", "RSI", "RDX", "RCX", "R8", "R9"]`. Remaining args mapped to `"STACK"`.',
            'constraints': 'args_list of any length',
            'starter_code': 'def map_x64_arg_registers(args_list: list) -> list:\n    pass\n',
            'test_cases': [{'desc': '3 args in regs', 'input': [[10, 20, 30]], 'expected': [('RDI', 10), ('RSI', 20), ('RDX', 30)]}],
            'hint': 'Loop up to 6 in order, after that use "STACK".',
            'solution_code': 'def map_x64_arg_registers(args_list: list) -> list:\n    regs = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]\n    res = []\n    for i, arg in enumerate(args_list):\n        r = regs[i] if i < len(regs) else "STACK"\n        res.append((r, arg))\n    return res\n',
            'explanation': 'System V AMD64 ABI specification for Linux/macOS calling conventions.'
        },
        'advance': {
            'id': 'c13-m4-l1-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'x86 Endianness Byte Swap Simulator',
            'function_name': 'endianness_swap_32',
            'prompt': 'Write `endianness_swap_32(val)` converting 32-bit unsigned int between Little-Endian and Big-Endian.',
            'constraints': '0 <= val <= 0xFFFFFFFF',
            'starter_code': 'def endianness_swap_32(val: int) -> int:\n    pass\n',
            'test_cases': [{'desc': '0x12345678 to 0x78563412', 'input': [0x12345678], 'expected': 0x78563412}],
            'hint': 'Extract 4 bytes using shifts and bitwise OR.',
            'solution_code': 'def endianness_swap_32(val: int) -> int:\n    b0 = (val & 0xFF) << 24\n    b1 = ((val >> 8) & 0xFF) << 16\n    b2 = ((val >> 16) & 0xFF) << 8\n    b3 = (val >> 24) & 0xFF\n    return b0 | b1 | b2 | b3\n',
            'explanation': 'Emulates x86 BSWAP instruction for network-to-host conversion.'
        }
    },
    (13, 4, 2): {
        'basic': {
            'id': 'c13-m4-l2-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Stack Canary Smashing Detector',
            'function_name': 'detect_canary_corruption',
            'prompt': 'Write `detect_canary_corruption(buffer_bytes, canary_token)` where the last 4 bytes are expected to equal canary_token. Return True if corrupted, False if intact.',
            'constraints': 'len(buffer_bytes) >= 4',
            'starter_code': 'def detect_canary_corruption(buffer_bytes: list, canary_token: int) -> bool:\n    pass\n',
            'test_cases': [{'desc': 'Intact canary', 'input': [[0x41, 0x41, 0x00, 0x13, 0x37], 0x1337], 'expected': False}, {'desc': 'Corrupted canary', 'input': [[0x41, 0x41, 0x90, 0x90, 0x90], 0x1337], 'expected': True}],
            'hint': 'Check if buffer_bytes[-1] == canary_token & 0xFF and buffer_bytes[-2] == (canary_token>>8)&0xFF.',
            'solution_code': 'def detect_canary_corruption(buffer_bytes: list, canary_token: int) -> bool:\n    found = (buffer_bytes[-2] << 8) | buffer_bytes[-1]\n    return found != canary_token\n',
            'explanation': 'GCC SSP (-fstack-protector) canary integrity check.'
        },
        'intermediate': {
            'id': 'c13-m4-l2-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'NOP Sled Shellcode Padding Generator',
            'function_name': 'craft_nop_sled_payload',
            'prompt': 'Write `craft_nop_sled_payload(target_length, shellcode_bytes)` returning a list of bytes padded with NOP (0x90) sled at front.',
            'constraints': 'target_length >= len(shellcode_bytes)',
            'starter_code': 'def craft_nop_sled_payload(target_length: int, shellcode_bytes: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Pad with 0x90', 'input': [5, [0xCC]], 'expected': [0x90, 0x90, 0x90, 0x90, 0xCC]}],
            'hint': 'Prepend [0x90] * (target_length - len(shellcode_bytes)).',
            'solution_code': 'def craft_nop_sled_payload(target_length: int, shellcode_bytes: list) -> list:\n    sled_len = max(0, target_length - len(shellcode_bytes))\n    return ([0x90] * sled_len) + list(shellcode_bytes)\n',
            'explanation': 'NOP sleds absorb execution jitter during stack redirection.'
        },
        'advance': {
            'id': 'c13-m4-l2-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Return-Oriented Programming (ROP) Gadget Chain Validator',
            'function_name': 'validate_rop_chain',
            'prompt': 'Write `validate_rop_chain(gadget_addresses, null_byte_forbidden=True)` checking if any 32-bit address contains a terminating 0x00 byte.',
            'constraints': 'List of integer addresses',
            'starter_code': 'def validate_rop_chain(gadget_addresses: list, null_byte_forbidden: bool = True) -> bool:\n    pass\n',
            'test_cases': [{'desc': 'Clean gadgets', 'input': [[0x08048123, 0x08048245]], 'expected': True}],
            'hint': 'Check if any byte in (addr >> (8*i)) & 0xFF == 0.',
            'solution_code': 'def validate_rop_chain(gadget_addresses: list, null_byte_forbidden: bool = True) -> bool:\n    if not null_byte_forbidden: return True\n    for addr in gadget_addresses:\n        for i in range(4):\n            if ((addr >> (8 * i)) & 0xFF) == 0:\n                return False\n    return True\n',
            'explanation': 'ROP chains avoid DEP/NX protections by reusing existing code snippets.'
        }
    },
    (15, 3, 2): {
        'basic': {
            'id': 'c15-m3-l2-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Token Bucket Rate Limiter Request Processor',
            'function_name': 'rate_limit_token_bucket',
            'prompt': 'Write `rate_limit_token_bucket(tokens, capacity, refill_rate, elapsed_sec)`: new_tokens = min(capacity, tokens + refill_rate*elapsed_sec). If >= 1.0, consume 1 and return `(True, round(new_tokens - 1.0, 2))`. Else return `(False, round(new_tokens, 2))`.',
            'constraints': 'All numeric >= 0',
            'starter_code': 'def rate_limit_token_bucket(tokens: float, capacity: float, refill_rate: float, elapsed_sec: float) -> tuple:\n    pass\n',
            'test_cases': [{'desc': 'Allow request', 'input': [0.5, 10.0, 1.0, 1.0], 'expected': (True, 0.5)}, {'desc': 'Deny request', 'input': [0.0, 10.0, 0.5, 1.0], 'expected': (False, 0.5)}],
            'hint': 'Compute refilled = min(capacity, tokens + refill_rate * elapsed_sec). Check >= 1.0.',
            'solution_code': 'def rate_limit_token_bucket(tokens: float, capacity: float, refill_rate: float, elapsed_sec: float) -> tuple:\n    refilled = min(capacity, tokens + refill_rate * elapsed_sec)\n    if refilled >= 1.0:\n        return (True, round(refilled - 1.0, 2))\n    return (False, round(refilled, 2))\n',
            'explanation': 'Standard token bucket rate limiting algorithm used by Stripe and Cloudflare.'
        },
        'intermediate': {
            'id': 'c15-m3-l2-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Sliding Window Log Rate Limiter',
            'function_name': 'sliding_window_allow',
            'prompt': 'Write `sliding_window_allow(request_timestamps, window_seconds, max_allowed, current_time)` keeping only timestamps in `[current_time - window_seconds, current_time]`. Return True if count < max_allowed.',
            'constraints': 'request_timestamps is list of floats',
            'starter_code': 'def sliding_window_allow(request_timestamps: list, window_seconds: float, max_allowed: int, current_time: float) -> bool:\n    pass\n',
            'test_cases': [{'desc': 'Within limit', 'input': [[95.0, 98.0], 10.0, 3, 100.0], 'expected': True}],
            'hint': 'Filter timestamps >= current_time - window_seconds. Return len(valid) < max_allowed.',
            'solution_code': 'def sliding_window_allow(request_timestamps: list, window_seconds: float, max_allowed: int, current_time: float) -> bool:\n    cutoff = current_time - window_seconds\n    valid = [t for t in request_timestamps if t >= cutoff]\n    return len(valid) < max_allowed\n',
            'explanation': 'Prevents boundary burst attacks present in fixed window algorithms.'
        },
        'advance': {
            'id': 'c15-m3-l2-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'HTTP 429 Retry-After Header Generator',
            'function_name': 'generate_retry_after',
            'prompt': 'Write `generate_retry_after(current_tokens, refill_rate)` calculating seconds until 1 full token is available: `ceil((1.0 - current_tokens) / refill_rate)`. Return int.',
            'constraints': 'current_tokens < 1.0, refill_rate > 0',
            'starter_code': 'def generate_retry_after(current_tokens: float, refill_rate: float) -> int:\n    pass\n',
            'test_cases': [{'desc': 'Needs 2 seconds', 'input': [0.5, 0.3], 'expected': 2}],
            'hint': 'import math; return math.ceil((1.0 - current_tokens) / refill_rate).',
            'solution_code': 'def generate_retry_after(current_tokens: float, refill_rate: float) -> int:\n    import math\n    return math.ceil((1.0 - current_tokens) / refill_rate)\n',
            'explanation': 'RFC 6585 standard for HTTP 429 Too Many Requests response.'
        }
    },
    (17, 6, 2): {
        'basic': {
            'id': 'c17-m6-l2-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Merge Two Sorted Subarrays (Merge Step)',
            'function_name': 'merge_sorted_arrays',
            'prompt': 'Write `merge_sorted_arrays(arr1, arr2)` that merges two sorted lists into one sorted list in O(N+M) time without calling sort().',
            'constraints': 'arr1 and arr2 are pre-sorted lists',
            'starter_code': 'def merge_sorted_arrays(arr1: list, arr2: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Interleaved', 'input': [[1, 3, 5], [2, 4, 6]], 'expected': [1, 2, 3, 4, 5, 6]}],
            'hint': 'Use two pointers i=0, j=0; compare elements and append smaller one.',
            'solution_code': 'def merge_sorted_arrays(arr1: list, arr2: list) -> list:\n    i = j = 0\n    res = []\n    while i < len(arr1) and j < len(arr2):\n        if arr1[i] <= arr2[j]:\n            res.append(arr1[i])\n            i += 1\n        else:\n            res.append(arr2[j])\n            j += 1\n    res.extend(arr1[i:])\n    res.extend(arr2[j:])\n    return res\n',
            'explanation': 'The fundamental combine phase of Divide-and-Conquer Merge Sort.'
        },
        'intermediate': {
            'id': 'c17-m6-l2-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Recursive Merge Sort Implementation',
            'function_name': 'merge_sort_recursive',
            'prompt': 'Write `merge_sort_recursive(items)` recursively dividing items in half and merging them.',
            'constraints': 'items is list of integers',
            'starter_code': 'def merge_sort_recursive(items: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Sort unsorted', 'input': [[5, 2, 9, 1, 7]], 'expected': [1, 2, 5, 7, 9]}],
            'hint': 'Base case: len(items) <= 1. mid = len(items)//2. Recursively sort left and right, then merge.',
            'solution_code': 'def merge_sort_recursive(items: list) -> list:\n    if len(items) <= 1: return items\n    mid = len(items) // 2\n    left = merge_sort_recursive(items[:mid])\n    right = merge_sort_recursive(items[mid:])\n    i = j = 0\n    res = []\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]: res.append(left[i]); i += 1\n        else: res.append(right[j]); j += 1\n    res.extend(left[i:]); res.extend(right[j:])\n    return res\n',
            'explanation': 'Guaranteed O(N log N) comparison sort.'
        },
        'advance': {
            'id': 'c17-m6-l2-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Count Inversions in Array via Merge Sort',
            'function_name': 'count_inversions',
            'prompt': 'Write `count_inversions(arr)` returning total number of pairs `(i, j)` where `i < j` and `arr[i] > arr[j]`.',
            'constraints': 'arr of distinct integers',
            'starter_code': 'def count_inversions(arr: list) -> int:\n    pass\n',
            'test_cases': [{'desc': 'Count inversions', 'input': [[2, 4, 1, 3, 5]], 'expected': 3}],
            'hint': 'During merge, when element from right is chosen before left, add remaining elements in left.',
            'solution_code': 'def count_inversions(arr: list) -> int:\n    count = 0\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] > arr[j]: count += 1\n    return count\n',
            'explanation': 'Measures sortedness of an array in algorithmic complexity.'
        }
    },
    (18, 1, 1): {
        'basic': {
            'id': 'c18-m1-l1-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Find Min & Max with 3N/2 Comparisons',
            'function_name': 'find_min_and_max',
            'prompt': 'Write `find_min_and_max(nums)` finding both minimum and maximum of a list in a single pass. Return `{"min": ..., "max": ...}`.',
            'constraints': 'nums is non-empty list of numbers',
            'starter_code': 'def find_min_and_max(nums: list) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'Find bounds', 'input': [[3, 1, 9, 4, 7]], 'expected': {'min': 1, 'max': 9}}],
            'hint': 'Initialize min_v = max_v = nums[0]. Compare elements.',
            'solution_code': 'def find_min_and_max(nums: list) -> dict:\n    return {"min": min(nums), "max": max(nums)}\n',
            'explanation': 'Demonstrates O(N) lower bound for simultaneous extremum search.'
        },
        'intermediate': {
            'id': 'c18-m1-l1-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Big-O Growth Rate Comparator',
            'function_name': 'compare_growth_rates',
            'prompt': 'Write `compare_growth_rates(n)` returning dict `{"O(1)": 1, "O(logN)": round(log2(n), 2), "O(N)": n, "O(NlogN)": round(n*log2(n), 2), "O(N^2)": n**2}`.',
            'constraints': 'n >= 1',
            'starter_code': 'def compare_growth_rates(n: int) -> dict:\n    pass\n',
            'test_cases': [{'desc': 'n=8 bounds', 'input': [8], 'expected': {'O(1)': 1, 'O(logN)': 3.0, 'O(N)': 8, 'O(NlogN)': 24.0, 'O(N^2)': 64}}],
            'hint': 'import math; log2_n = math.log2(n).',
            'solution_code': 'def compare_growth_rates(n: int) -> dict:\n    import math\n    l2 = round(math.log2(n), 2)\n    return {"O(1)": 1, "O(logN)": l2, "O(N)": n, "O(NlogN)": round(n * l2, 2), "O(N^2)": n ** 2}\n',
            'explanation': 'Visualizes asymptotic complexity scales.'
        },
        'advance': {
            'id': 'c18-m1-l1-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Master Theorem Recurrence Solver',
            'function_name': 'solve_master_theorem',
            'prompt': 'Write `solve_master_theorem(a, b, d)` for `T(n) = a*T(n/b) + O(n^d)`: compare `d` and `log_b(a)`. Return "Case 1", "Case 2", or "Case 3".',
            'constraints': 'a >= 1, b > 1, d >= 0',
            'starter_code': 'def solve_master_theorem(a: int, b: int, d: float) -> str:\n    pass\n',
            'test_cases': [{'desc': 'Merge sort case (a=2, b=2, d=1)', 'input': [2, 2, 1.0], 'expected': 'Case 2'}],
            'hint': 'import math; crit = math.log(a, b). If d < crit return "Case 1"; if d == crit return "Case 2"; else "Case 3".',
            'solution_code': 'def solve_master_theorem(a: int, b: int, d: float) -> str:\n    import math\n    crit = math.log(a, b)\n    if round(d, 4) < round(crit, 4): return "Case 1"\n    elif round(d, 4) == round(crit, 4): return "Case 2"\n    return "Case 3"\n',
            'explanation': 'The Master Theorem solves divide-and-conquer recurrences.'
        }
    },
    (18, 2, 1): {
        'basic': {
            'id': 'c18-m2-l1-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Balanced Parentheses Stack Validator',
            'function_name': 'validate_parentheses_stack',
            'prompt': 'Write `validate_parentheses_stack(s)` checking if brackets "()", "[]", "{}" are matched and closed in correct order.',
            'constraints': 's contains bracket characters',
            'starter_code': 'def validate_parentheses_stack(s: str) -> bool:\n    pass\n',
            'test_cases': [{'desc': 'Valid', 'input': ['{[()]}'], 'expected': True}, {'desc': 'Invalid', 'input': ['{[(])}'], 'expected': False}],
            'hint': 'Use stack. Push open brackets, pop and compare for closing brackets.',
            'solution_code': 'def validate_parentheses_stack(s: str) -> bool:\n    pairs = {")": "(", "]": "[", "}": "{"}\n    stack = []\n    for ch in s:\n        if ch in pairs.values(): stack.append(ch)\n        elif ch in pairs:\n            if not stack or stack.pop() != pairs[ch]: return False\n    return len(stack) == 0\n',
            'explanation': 'Classic LIFO stack application.'
        },
        'intermediate': {
            'id': 'c18-m2-l1-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Evaluate Reverse Polish Notation (Postfix) with Stack',
            'function_name': 'eval_rpn_stack',
            'prompt': 'Write `eval_rpn_stack(tokens)` evaluating arithmetic postfix expression tokens (strings of numbers or "+", "-", "*").',
            'constraints': 'Valid RPN sequence',
            'starter_code': 'def eval_rpn_stack(tokens: list) -> int:\n    pass\n',
            'test_cases': [{'desc': '2 1 + 3 * = 9', 'input': [['2', '1', '+', '3', '*']], 'expected': 9}],
            'hint': 'Push numbers to stack. On operator, pop b then a, push result.',
            'solution_code': 'def eval_rpn_stack(tokens: list) -> int:\n    stack = []\n    for t in tokens:\n        if t == "+": stack.append(stack.pop() + stack.pop())\n        elif t == "*": stack.append(stack.pop() * stack.pop())\n        elif t == "-": b = stack.pop(); a = stack.pop(); stack.append(a - b)\n        else: stack.append(int(t))\n    return stack[0]\n',
            'explanation': 'Compiler expression evaluation mechanics.'
        },
        'advance': {
            'id': 'c18-m2-l1-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'MinStack O(1) Constant Time Retrieval',
            'function_name': 'simulate_min_stack',
            'prompt': 'Write `simulate_min_stack(operations)` maintaining a stack with O(1) get_min(). Operations are `("PUSH", val)`, `("POP", None)`, `("GET_MIN", None)`. Return list of GET_MIN results.',
            'constraints': 'operations is list of tuples',
            'starter_code': 'def simulate_min_stack(operations: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Min retrieval', 'input': [[('PUSH', 3), ('PUSH', 1), ('GET_MIN', None), ('POP', None), ('GET_MIN', None)]], 'expected': [1, 3]}],
            'hint': 'Maintain a parallel min_stack tracking current minimum.',
            'solution_code': 'def simulate_min_stack(operations: list) -> list:\n    stack = []\n    min_stack = []\n    res = []\n    for op, val in operations:\n        if op == "PUSH":\n            stack.append(val)\n            min_stack.append(val if not min_stack or val < min_stack[-1] else min_stack[-1])\n        elif op == "POP":\n            if stack:\n                stack.pop()\n                min_stack.pop()\n        elif op == "GET_MIN":\n            if min_stack: res.append(min_stack[-1])\n    return res\n',
            'explanation': 'Design a Data Structure with amortized O(1) constraints.'
        }
    },
    (18, 2, 2): {
        'basic': {
            'id': 'c18-m2-l2-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Circular Queue FIFO Simulator',
            'function_name': 'simulate_circular_queue',
            'prompt': 'Write `simulate_circular_queue(capacity, operations)`: operations is list of `("ENQUEUE", val)` and `("DEQUEUE", None)`. Return list of dequeued values.',
            'constraints': 'capacity >= 1',
            'starter_code': 'def simulate_circular_queue(capacity: int, operations: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'FIFO order', 'input': [2, [('ENQUEUE', 10), ('ENQUEUE', 20), ('DEQUEUE', None), ('ENQUEUE', 30), ('DEQUEUE', None)]], 'expected': [10, 20]}],
            'hint': 'Maintain queue. Only enqueue if len < capacity.',
            'solution_code': 'def simulate_circular_queue(capacity: int, operations: list) -> list:\n    q = []\n    dequeued = []\n    for op, val in operations:\n        if op == "ENQUEUE":\n            if len(q) < capacity: q.append(val)\n        elif op == "DEQUEUE":\n            if q: dequeued.append(q.pop(0))\n    return dequeued\n',
            'explanation': 'FIFO queue structure with bounded buffer capacity.'
        },
        'intermediate': {
            'id': 'c18-m2-l2-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Implement Queue using Two Stacks',
            'function_name': 'queue_via_two_stacks',
            'prompt': 'Write `queue_via_two_stacks(operations)` implementing FIFO using in_stack and out_stack. Return dequeued elements.',
            'constraints': 'Valid operations',
            'starter_code': 'def queue_via_two_stacks(operations: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Two stacks', 'input': [[('PUSH', 1), ('PUSH', 2), ('POP', None)]], 'expected': [1]}],
            'hint': 'When popping from out_stack, if empty, transfer all elements from in_stack.',
            'solution_code': 'def queue_via_two_stacks(operations: list) -> list:\n    s_in = []\n    s_out = []\n    res = []\n    for op, val in operations:\n        if op == "PUSH": s_in.append(val)\n        elif op == "POP":\n            if not s_out:\n                while s_in: s_out.append(s_in.pop())\n            if s_out: res.append(s_out.pop())\n    return res\n',
            'explanation': 'Amortized O(1) queue using two LIFO stacks.'
        },
        'advance': {
            'id': 'c18-m2-l2-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Sliding Window Maximum using Deque',
            'function_name': 'sliding_window_maximum',
            'prompt': 'Write `sliding_window_maximum(nums, k)` returning list of maximum values in each sliding window of size k.',
            'constraints': '1 <= k <= len(nums)',
            'starter_code': 'def sliding_window_maximum(nums: list, k: int) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Window 3', 'input': [[1, 3, -1, -3, 5, 3, 6, 7], 3], 'expected': [3, 3, 5, 5, 6, 7]}],
            'hint': 'Maintain a monotonic decreasing deque of indices.',
            'solution_code': 'def sliding_window_maximum(nums: list, k: int) -> list:\n    return [max(nums[i:i+k]) for i in range(len(nums) - k + 1)]\n',
            'explanation': 'Double-ended queue (deque) sliding window pattern.'
        }
    },
    (18, 2, 3): {
        'basic': {
            'id': 'c18-m2-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Next Greater Element via Monotonic Stack',
            'function_name': 'find_next_greater',
            'prompt': 'Write `find_next_greater(nums)`: for each element, find the next strictly greater element to its right. If none, -1.',
            'constraints': 'nums is list of integers',
            'starter_code': 'def find_next_greater(nums: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Next greater', 'input': [[4, 5, 2, 25]], 'expected': [5, 25, 25, -1]}],
            'hint': 'Iterate from right to left using a monotonic decreasing stack.',
            'solution_code': 'def find_next_greater(nums: list) -> list:\n    res = [-1] * len(nums)\n    stack = []\n    for i in range(len(nums) - 1, -1, -1):\n        while stack and stack[-1] <= nums[i]: stack.pop()\n        if stack: res[i] = stack[-1]\n        stack.append(nums[i])\n    return res\n',
            'explanation': 'O(N) monotonic stack pattern.'
        },
        'intermediate': {
            'id': 'c18-m2-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Daily Temperatures Wait Days Calculator',
            'function_name': 'daily_temperatures_wait',
            'prompt': 'Write `daily_temperatures_wait(temperatures)` returning list where `res[i]` is days until a warmer temperature. If none, 0.',
            'constraints': 'List of positive integers',
            'starter_code': 'def daily_temperatures_wait(temperatures: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Wait days', 'input': [[73, 74, 75, 71, 69, 72, 76, 73]], 'expected': [1, 1, 4, 2, 1, 1, 0, 0]}],
            'hint': 'Stack stores indices of temperatures.',
            'solution_code': 'def daily_temperatures_wait(temperatures: list) -> list:\n    n = len(temperatures)\n    res = [0] * n\n    stack = []\n    for i, t in enumerate(temperatures):\n        while stack and temperatures[stack[-1]] < t:\n            prev = stack.pop()\n            res[prev] = i - prev\n        stack.append(i)\n    return res\n',
            'explanation': 'Monotonic stack for index distance tracking.'
        },
        'advance': {
            'id': 'c18-m2-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Largest Rectangle in Histogram',
            'function_name': 'largest_rectangle_area',
            'prompt': 'Write `largest_rectangle_area(heights)` returning area of largest rectangle in histogram.',
            'constraints': 'heights is list of non-negative integers',
            'starter_code': 'def largest_rectangle_area(heights: list) -> int:\n    pass\n',
            'test_cases': [{'desc': 'Largest area', 'input': [[2, 1, 5, 6, 2, 3]], 'expected': 10}],
            'hint': 'Use a stack of (index, height). Pop when height decreases and calculate area.',
            'solution_code': 'def largest_rectangle_area(heights: list) -> int:\n    stack = []\n    max_area = 0\n    h_list = heights + [0]\n    for i, h in enumerate(h_list):\n        start = i\n        while stack and stack[-1][1] > h:\n            idx, height = stack.pop()\n            max_area = max(max_area, height * (i - idx))\n            start = idx\n        stack.append((start, h))\n    return max_area\n',
            'explanation': 'Classic hard LeetCode monotonic stack problem.'
        }
    },
    (18, 4, 2): {
        'basic': {
            'id': 'c18-m4-l2-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Binary Tree In-Order Traversal (LVR)',
            'function_name': 'inorder_tree_traversal',
            'prompt': 'Write `inorder_tree_traversal(tree, root)`: tree is dict `{"val": [left, right]}`. Return list of nodes in Left-Visit-Right order.',
            'constraints': 'root exists in tree',
            'starter_code': 'def inorder_tree_traversal(tree: dict, root: str) -> list:\n    pass\n',
            'test_cases': [{'desc': 'In-order', 'input': [{'A': ['B', 'C'], 'B': [None, None], 'C': [None, None]}, 'A'], 'expected': ['B', 'A', 'C']}],
            'hint': 'Recursive helper: dfs(node): if not node: return; dfs(left); visit; dfs(right).',
            'solution_code': 'def inorder_tree_traversal(tree: dict, root: str) -> list:\n    res = []\n    def dfs(node):\n        if not node: return\n        left, right = tree.get(node, [None, None])\n        dfs(left)\n        res.append(node)\n        dfs(right)\n    dfs(root)\n    return res\n',
            'explanation': 'In-order traversal on a BST yields sorted order.'
        },
        'intermediate': {
            'id': 'c18-m4-l2-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Binary Tree Level-Order Traversal (BFS)',
            'function_name': 'level_order_traversal',
            'prompt': 'Write `level_order_traversal(tree, root)` visiting nodes layer by layer from top to bottom using a queue.',
            'constraints': 'root in tree',
            'starter_code': 'def level_order_traversal(tree: dict, root: str) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Level order', 'input': [{'A': ['B', 'C'], 'B': ['D', 'E'], 'C': [None, None], 'D': [None, None], 'E': [None, None]}, 'A'], 'expected': ['A', 'B', 'C', 'D', 'E']}],
            'hint': 'Queue = [root]. While queue: pop(0), append children.',
            'solution_code': 'def level_order_traversal(tree: dict, root: str) -> list:\n    if not root: return []\n    q = [root]\n    res = []\n    while q:\n        curr = q.pop(0)\n        res.append(curr)\n        for child in tree.get(curr, [None, None]):\n            if child: q.append(child)\n    return res\n',
            'explanation': 'Breadth-First Search level traversal on trees.'
        },
        'advance': {
            'id': 'c18-m4-l2-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Binary Tree Maximum Depth (Height)',
            'function_name': 'max_depth_tree',
            'prompt': 'Write `max_depth_tree(tree, root)` returning maximum edge or node depth from root to deepest leaf.',
            'constraints': 'tree represented as dict',
            'starter_code': 'def max_depth_tree(tree: dict, root: str) -> int:\n    pass\n',
            'test_cases': [{'desc': 'Depth 3', 'input': [{'A': ['B', None], 'B': ['C', None], 'C': [None, None]}, 'A'], 'expected': 3}],
            'hint': 'Depth = 1 + max(dfs(left), dfs(right)). Base case 0 if node is None.',
            'solution_code': 'def max_depth_tree(tree: dict, root: str) -> int:\n    if not root: return 0\n    left, right = tree.get(root, [None, None])\n    return 1 + max(max_depth_tree(tree, left), max_depth_tree(tree, right))\n',
            'explanation': 'Classic divide-and-conquer tree height algorithm.'
        }
    },
    (18, 4, 3): {
        'basic': {
            'id': 'c18-m4-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Min-Heap Sift-Up Insertion Primitive',
            'function_name': 'min_heap_insert',
            'prompt': 'Write `min_heap_insert(heap, val)` appending val and sifting up so parent is always <= child: `parent_idx = (idx - 1) // 2`. Return heap.',
            'constraints': 'heap is list of ints',
            'starter_code': 'def min_heap_insert(heap: list, val: int) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Insert 1', 'input': [[2, 5, 10], 1], 'expected': [1, 2, 10, 5]}],
            'hint': 'Append val. idx = len - 1. While idx > 0 and heap[parent] > heap[idx]: swap and update idx.',
            'solution_code': 'def min_heap_insert(heap: list, val: int) -> list:\n    h = list(heap)\n    h.append(val)\n    idx = len(h) - 1\n    while idx > 0:\n        p = (idx - 1) // 2\n        if h[p] > h[idx]:\n            h[p], h[idx] = h[idx], h[p]\n            idx = p\n        else: break\n    return h\n',
            'explanation': 'Maintains the min-heap invariant in O(log N) time.'
        },
        'intermediate': {
            'id': 'c18-m4-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Find Kth Largest Element via Min-Heap',
            'function_name': 'find_kth_largest',
            'prompt': 'Write `find_kth_largest(nums, k)` returning the kth largest element in nums.',
            'constraints': '1 <= k <= len(nums)',
            'starter_code': 'def find_kth_largest(nums: list, k: int) -> int:\n    pass\n',
            'test_cases': [{'desc': '2nd largest', 'input': [[3, 2, 1, 5, 6, 4], 2], 'expected': 5}],
            'hint': 'Sort descending and return index k-1, or use heapq.',
            'solution_code': 'def find_kth_largest(nums: list, k: int) -> int:\n    import heapq\n    return heapq.nlargest(k, nums)[-1]\n',
            'explanation': 'Standard O(N log K) top-K streaming algorithm.'
        },
        'advance': {
            'id': 'c18-m4-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Merge K Sorted Linked Lists using Min-Heap',
            'function_name': 'merge_k_sorted_arrays',
            'prompt': 'Write `merge_k_sorted_arrays(arrays)` merging a list of sorted integer arrays into one combined sorted list.',
            'constraints': 'List of sorted lists',
            'starter_code': 'def merge_k_sorted_arrays(arrays: list) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Merge 3 lists', 'input': [[[1, 4, 5], [1, 3, 4], [2, 6]]], 'expected': [1, 1, 2, 3, 4, 4, 5, 6]}],
            'hint': 'import heapq; return list(heapq.merge(*arrays)).',
            'solution_code': 'def merge_k_sorted_arrays(arrays: list) -> list:\n    import heapq\n    return list(heapq.merge(*arrays))\n',
            'explanation': 'Hard LeetCode classic solved via Min-Heap in O(N log K).'
        }
    },
    (19, 2, 3): {
        'basic': {
            'id': 'c19-m2-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'WCAG 2.1 Color Contrast Ratio Calculator',
            'function_name': 'calculate_contrast_ratio',
            'prompt': 'Write `calculate_contrast_ratio(lum1, lum2)`: `(L1 + 0.05) / (L2 + 0.05)` where L1 = max(lum1, lum2) and L2 = min(lum1, lum2). Round to 2 decimals.',
            'constraints': '0 <= lum1, lum2 <= 1',
            'starter_code': 'def calculate_contrast_ratio(lum1: float, lum2: float) -> float:\n    pass\n',
            'test_cases': [{'desc': 'Black vs White', 'input': [1.0, 0.0], 'expected': 21.0}],
            'hint': 'l1 = max(lum1, lum2); l2 = min(lum1, lum2); round((l1 + 0.05) / (l2 + 0.05), 2).',
            'solution_code': 'def calculate_contrast_ratio(lum1: float, lum2: float) -> float:\n    l1 = max(lum1, lum2)\n    l2 = min(lum1, lum2)\n    return round((l1 + 0.05) / (l2 + 0.05), 2)\n',
            'explanation': 'WCAG accessibility formula determining AA (4.5:1) and AAA (7:1) compliance.'
        },
        'intermediate': {
            'id': 'c19-m2-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'HEX to Relative Luminance Converter',
            'function_name': 'hex_to_rgb_tuple',
            'prompt': 'Write `hex_to_rgb_tuple(hex_str)` converting "#RRGGBB" to `(r, g, b)` integer tuple in `[0, 255]`.',
            'constraints': '7-char hex string starting with #',
            'starter_code': 'def hex_to_rgb_tuple(hex_str: str) -> tuple:\n    pass\n',
            'test_cases': [{'desc': '#0066FF to RGB', 'input': ['#0066FF'], 'expected': (0, 102, 255)}],
            'hint': 'int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16).',
            'solution_code': 'def hex_to_rgb_tuple(hex_str: str) -> tuple:\n    h = hex_str.lstrip("#")\n    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))\n',
            'explanation': 'Transforms CSS Hex tokens to sRGB color space components.'
        },
        'advance': {
            'id': 'c19-m2-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'WCAG Level AA / AAA Compliance Evaluator',
            'function_name': 'evaluate_wcag_compliance',
            'prompt': 'Write `evaluate_wcag_compliance(ratio, is_large_text=False)`: if large text, AA requires >= 3.0, AAA >= 4.5. Normal text requires AA >= 4.5, AAA >= 7.0. Return "AAA", "AA", or "FAIL".',
            'constraints': 'ratio >= 1.0',
            'starter_code': 'def evaluate_wcag_compliance(ratio: float, is_large_text: bool = False) -> str:\n    pass\n',
            'test_cases': [{'desc': 'Normal text 5.0 is AA', 'input': [5.0, False], 'expected': 'AA'}, {'desc': 'Ratio 8.0 is AAA', 'input': [8.0, False], 'expected': 'AAA'}],
            'hint': 'Check AAA first, then AA, else FAIL.',
            'solution_code': 'def evaluate_wcag_compliance(ratio: float, is_large_text: bool = False) -> str:\n    aaa = 4.5 if is_large_text else 7.0\n    aa = 3.0 if is_large_text else 4.5\n    if ratio >= aaa: return "AAA"\n    elif ratio >= aa: return "AA"\n    return "FAIL"\n',
            'explanation': 'Design system accessibility linter rule.'
        }
    },
    (19, 3, 3): {
        'basic': {
            'id': 'c19-m3-l3-b', 'difficulty': 'Basic', 'badge_class': 'bg-success',
            'title': 'Design Token Reference Alias Resolver',
            'function_name': 'resolve_token_alias',
            'prompt': 'Write `resolve_token_alias(token_map, query_key)` resolving alias strings like `"{colors.brand}"` pointing to `colors.brand` in token_map. Follow up to 5 hops.',
            'constraints': 'token_map maps strings to strings',
            'starter_code': 'def resolve_token_alias(token_map: dict, query_key: str) -> str:\n    pass\n',
            'test_cases': [{'desc': 'Resolve alias', 'input': [{'colors.brand': '#0066FF', 'button.bg': '{colors.brand}'}, 'button.bg'], 'expected': '#0066FF'}],
            'hint': 'While val.startswith("{") and val.endswith("}"): extract ref = val[1:-1] and val = token_map.get(ref).',
            'solution_code': 'def resolve_token_alias(token_map: dict, query_key: str) -> str:\n    val = token_map.get(query_key, "")\n    hops = 0\n    while isinstance(val, str) and val.startswith("{") and val.endswith("}") and hops < 10:\n        ref = val[1:-1]\n        val = token_map.get(ref, val)\n        hops += 1\n    return val\n',
            'explanation': 'Design Tokens Community Group (DTCG) W3C spec alias resolution.'
        },
        'intermediate': {
            'id': 'c19-m3-l3-i', 'difficulty': 'Intermediate', 'badge_class': 'bg-primary',
            'title': 'Figma Component Variant Matrix Combinator',
            'function_name': 'generate_component_variants',
            'prompt': 'Write `generate_component_variants(property_dict)` generating all combinations of property variants as list of dicts.',
            'constraints': 'property_dict maps str to list of str',
            'starter_code': 'def generate_component_variants(property_dict: dict) -> list:\n    pass\n',
            'test_cases': [{'desc': 'Variants', 'input': [{'size': ['sm', 'lg'], 'state': ['default', 'hover']}], 'expected': [{'size': 'sm', 'state': 'default'}, {'size': 'sm', 'state': 'hover'}, {'size': 'lg', 'state': 'default'}, {'size': 'lg', 'state': 'hover'}]}],
            'hint': 'Use itertools.product.',
            'solution_code': 'def generate_component_variants(property_dict: dict) -> list:\n    import itertools\n    keys = list(property_dict.keys())\n    vals = [property_dict[k] for k in keys]\n    res = []\n    for comb in itertools.product(*vals):\n        res.append(dict(zip(keys, comb)))\n    return res\n',
            'explanation': 'Auto-generates component set permutations in Figma design systems.'
        },
        'advance': {
            'id': 'c19-m3-l3-a', 'difficulty': 'Advance', 'badge_class': 'bg-purple',
            'title': 'Design Token DTCG JSON to CSS Variables Exporter',
            'function_name': 'export_tokens_to_css',
            'prompt': 'Write `export_tokens_to_css(tokens)` converting `{"colors.primary": "#123"}` into `:root { --colors-primary: #123; }`.',
            'constraints': 'tokens dict of strings',
            'starter_code': 'def export_tokens_to_css(tokens: dict) -> str:\n    pass\n',
            'test_cases': [{'desc': 'CSS vars', 'input': [{'colors.primary': '#123'}], 'expected': ':root {\n  --colors-primary: #123;\n}'}],
            'hint': 'Replace "." with "-". Format lines indented by 2 spaces.',
            'solution_code': 'def export_tokens_to_css(tokens: dict) -> str:\n    lines = [":root {"]\n    for k, v in sorted(tokens.items()):\n        css_name = "--" + k.replace(".", "-")\n        lines.append(f"  {css_name}: {v};")\n    lines.append("}")\n    return "\n".join(lines)\n',
            'explanation': 'Design Systems build pipeline (Style Dictionary) to production CSS.'
        }
    }
}
