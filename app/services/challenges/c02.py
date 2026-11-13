"""Course 2 topic-specific programming challenges."""

CHALLENGES = {(1, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(values) >= 1',
                      'difficulty': 'Advance',
                      'explanation': 'Scikit-learn StandardScaler normalization.',
                      'function_name': 'standard_scale_data',
                      'hint': 'Calculate mean and std = sqrt(variance).',
                      'id': 'c2-m1-l1-a',
                      'prompt': 'Write `standard_scale_data(values)` returning `(x - mean) / std` rounded to 2 '
                                'decimals. If std is 0 return [0.0]*len(values).',
                      'solution_code': 'def standard_scale_data(values: list) -> list:\n'
                                       '    n = len(values)\n'
                                       '    m = sum(values) / n\n'
                                       '    var = sum((x - m)**2 for x in values) / n\n'
                                       '    std = var ** 0.5\n'
                                       '    if std == 0: return [0.0] * n\n'
                                       '    return [round((x - m) / std, 2) for x in values]\n',
                      'starter_code': 'def standard_scale_data(values: list) -> list:\n'
                                      '    # Return standardized values\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Standardized 10, 20, 30',
                                      'expected': [-1.22, 0.0, 1.22],
                                      'input': [[10, 20, 30]]}],
                      'title': 'StandardScaler with Zero Variance Protection'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'total_samples >= 2, 0 < test_ratio < 1',
                    'difficulty': 'Basic',
                    'explanation': 'Scikit-learn train_test_split deterministic index allocation.',
                    'function_name': 'train_test_split_indices',
                    'hint': 'test_count = int(total_samples * test_ratio). train_count = total_samples - test_count.',
                    'id': 'c2-m1-l1-b',
                    'prompt': 'Write `train_test_split_indices(total_samples, test_ratio)` returning `{"train": '
                              '[0..train_end-1], "test": [train_end..total_samples-1]}` where test_size = '
                              'int(total_samples * test_ratio).',
                    'solution_code': 'def train_test_split_indices(total_samples: int, test_ratio: float) -> dict:\n'
                                     '    n_test = int(total_samples * test_ratio)\n'
                                     '    n_train = total_samples - n_test\n'
                                     '    return {"train": list(range(n_train)), "test": list(range(n_train, '
                                     'total_samples))}\n',
                    'starter_code': 'def train_test_split_indices(total_samples: int, test_ratio: float) -> dict:\n'
                                    '    # Return split indices dict\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '8 train, 2 test',
                                    'expected': {'test': [8, 9], 'train': [0, 1, 2, 3, 4, 5, 6, 7]},
                                    'input': [10, 0.2]}],
                    'title': 'Train/Test Split Index Partitioning'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(values) >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Scikit-learn MinMaxScaler implementation.',
                           'function_name': 'min_max_scale_data',
                           'hint': 'Find min and max, divide difference by range.',
                           'id': 'c2-m1-l1-i',
                           'prompt': 'Write `min_max_scale_data(values)` scaling numbers to [0, 1]: `(x - min) / (max '
                                     '- min)`. Round to 2 decimals. If max == min return [0.0]*len(values).',
                           'solution_code': 'def min_max_scale_data(values: list) -> list:\n'
                                            '    mn, mx = min(values), max(values)\n'
                                            '    if mn == mx: return [0.0] * len(values)\n'
                                            '    return [round((x - mn) / (mx - mn), 2) for x in values]\n',
                           'starter_code': 'def min_max_scale_data(values: list) -> list:\n'
                                           '    # Return scaled values in [0, 1]\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Linear scale 10-50',
                                           'expected': [0.0, 0.25, 0.5, 0.75, 1.0],
                                           'input': [[10, 20, 30, 40, 50]]}],
                           'title': 'Min-Max Feature Scaler'}},
 (1, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(features) >= 1',
                      'difficulty': 'Advance',
                      'explanation': 'Scikit-learn PolynomialFeatures(degree=2) expansion.',
                      'function_name': 'generate_polynomial_pairs',
                      'hint': 'Originals, then for i in range(n) for j in range(i, n): append(features[i] * '
                              'features[j]).',
                      'id': 'c2-m1-l2-a',
                      'prompt': 'Write `generate_polynomial_pairs(features)` where features is `[x1, x2, ...]`. Return '
                                '`[x1, x2, ..., x1^2, x1*x2, x2^2]` (degree 2 interactions). Round to 2 decimals.',
                      'solution_code': 'def generate_polynomial_pairs(features: list) -> list:\n'
                                       '    n = len(features)\n'
                                       '    res = [float(x) for x in features]\n'
                                       '    for i in range(n):\n'
                                       '        for j in range(i, n):\n'
                                       '            res.append(round(features[i] * features[j], 2))\n'
                                       '    return res\n',
                      'starter_code': 'def generate_polynomial_pairs(features: list) -> list:\n'
                                      '    # Return polynomial interaction terms\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'x1, x2, x1^2, x1*x2, x2^2',
                                      'expected': [2.0, 3.0, 4.0, 6.0, 9.0],
                                      'input': [[2, 3]]}],
                      'title': 'Polynomial Feature Pair Expansion'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'categories is list of strings',
                    'difficulty': 'Basic',
                    'explanation': 'Scikit-learn OneHotEncoder binary matrix creation.',
                    'function_name': 'one_hot_encode_categories',
                    'hint': 'Sorted unique classes = sorted(list(set(categories))).',
                    'id': 'c2-m1-l2-b',
                    'prompt': 'Write `one_hot_encode_categories(categories)` returning `{"classes": sorted_unique, '
                              '"encoded": [[1 if c == cls else 0 for cls in sorted_unique] for c in categories]}`.',
                    'solution_code': 'def one_hot_encode_categories(categories: list) -> dict:\n'
                                     '    classes = sorted(list(set(categories)))\n'
                                     '    encoded = [[1 if c == cls else 0 for cls in classes] for c in categories]\n'
                                     '    return {"classes": classes, "encoded": encoded}\n',
                    'starter_code': 'def one_hot_encode_categories(categories: list) -> dict:\n'
                                    '    # Return classes and one-hot matrix\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Encodes red and blue',
                                    'expected': {'classes': ['blue', 'red'], 'encoded': [[0, 1], [1, 0], [0, 1]]},
                                    'input': [['red', 'blue', 'red']]}],
                    'title': 'One-Hot Categorical Encoder'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'labels is list of strings/ints, 0 < sample_rate <= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Class imbalance prevention in machine learning data pipelines.',
                           'function_name': 'stratified_sample_indices',
                           'hint': 'Group indices by label, take first k indices for each label, merge and sort.',
                           'id': 'c2-m1-l2-i',
                           'prompt': 'Write `stratified_sample_indices(labels, sample_rate)` that picks `max(1, '
                                     'int(count * sample_rate))` samples from each class. Return sorted indices.',
                           'solution_code': 'def stratified_sample_indices(labels: list, sample_rate: float) -> list:\n'
                                            '    by_label = {}\n'
                                            '    for i, lbl in enumerate(labels): by_label.setdefault(lbl, '
                                            '[]).append(i)\n'
                                            '    sampled = []\n'
                                            '    for lbl, idxs in by_label.items():\n'
                                            '        k = max(1, int(len(idxs) * sample_rate))\n'
                                            '        sampled.extend(idxs[:k])\n'
                                            '    return sorted(sampled)\n',
                           'starter_code': 'def stratified_sample_indices(labels: list, sample_rate: float) -> list:\n'
                                           '    # Return stratified sampled indices\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '2 from A (4*0.5), 1 from B (2*0.5)',
                                           'expected': [0, 1, 4],
                                           'input': [['A', 'A', 'A', 'A', 'B', 'B'], 0.5]}],
                           'title': 'Stratified Class Sampler'}},
 (2, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(x) == len(y) >= 2',
                      'difficulty': 'Advance',
                      'explanation': 'Closed-form Normal Equation solution for 1D linear regression.',
                      'function_name': 'ols_linear_regression',
                      'hint': 'Calculate mean_x, mean_y, slope = sum((x_i - mean_x)*(y_i - mean_y)) / sum((x_i - '
                              'mean_x)**2).',
                      'id': 'c2-m2-l1-a',
                      'prompt': 'Write `ols_linear_regression(x, y)` computing slope m and intercept b: `m = cov(x, y) '
                                '/ var(x)`, `b = mean(y) - m * mean(x)`. Return `{"slope": round(m, 2), "intercept": '
                                'round(b, 2)}`.',
                      'solution_code': 'def ols_linear_regression(x: list, y: list) -> dict:\n'
                                       '    n = len(x)\n'
                                       '    mx, my = sum(x) / n, sum(y) / n\n'
                                       '    num = sum((a - mx) * (b - my) for a, b in zip(x, y))\n'
                                       '    den = sum((a - mx)**2 for a in x)\n'
                                       '    m = num / den if den != 0 else 0.0\n'
                                       '    b = my - m * mx\n'
                                       '    return {"slope": round(m, 2), "intercept": round(b, 2)}\n',
                      'starter_code': 'def ols_linear_regression(x: list, y: list) -> dict:\n'
                                      '    # Return slope and intercept\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'y = 2x',
                                      'expected': {'intercept': 0.0, 'slope': 2.0},
                                      'input': [[1, 2, 3], [2, 4, 6]]}],
                      'title': 'Analytical Ordinary Least Squares Fit'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(actual) == len(predicted) >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Fundamental regression objective loss metric.',
                    'function_name': 'calculate_mse',
                    'hint': 'sum((a - p)**2 for a, p in zip(actual, predicted)) / len(actual).',
                    'id': 'c2-m2-l1-b',
                    'prompt': 'Write `calculate_mse(actual, predicted)`: `sum((y - y_hat)**2) / N`. Round to 2 '
                              'decimals.',
                    'solution_code': 'def calculate_mse(actual: list, predicted: list) -> float:\n'
                                     '    return round(sum((a - p)**2 for a, p in zip(actual, predicted)) / '
                                     'len(actual), 2)\n',
                    'starter_code': 'def calculate_mse(actual: list, predicted: list) -> float:\n'
                                    '    # Return MSE\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'MSE 0.38', 'expected': 0.38, 'input': [[3, -0.5, 2, 7], [2.5, 0.0, 2, 8]]},
                                   {'desc': 'Zero error', 'expected': 0.0, 'input': [[1, 2, 3], [1, 2, 3]]}],
                    'title': 'Mean Squared Error (MSE) Calculator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(actual) == len(predicted) >= 2',
                           'difficulty': 'Intermediate',
                           'explanation': 'Proportion of variance explained by regression model.',
                           'function_name': 'compute_r_squared',
                           'hint': 'SS_res = sum((a - p)**2), SS_tot = sum((a - mean_a)**2).',
                           'id': 'c2-m2-l1-i',
                           'prompt': 'Write `compute_r_squared(actual, predicted)`: `1 - (SS_res / SS_tot)`. Round to '
                                     '4 decimals.',
                           'solution_code': 'def compute_r_squared(actual: list, predicted: list) -> float:\n'
                                            '    m = sum(actual) / len(actual)\n'
                                            '    ss_tot = sum((a - m)**2 for a in actual)\n'
                                            '    ss_res = sum((a - p)**2 for a, p in zip(actual, predicted))\n'
                                            '    if ss_tot == 0: return 1.0 if ss_res == 0 else 0.0\n'
                                            '    return round(1.0 - (ss_res / ss_tot), 4)\n',
                           'starter_code': 'def compute_r_squared(actual: list, predicted: list) -> float:\n'
                                           '    # Return R-squared\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Perfect fit', 'expected': 1.0, 'input': [[1, 2, 3], [1, 2, 3]]}],
                           'title': 'R-Squared (Coefficient of Determination)'}},
 (2, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'alpha >= 0, 0 <= l1_ratio <= 1',
                      'difficulty': 'Advance',
                      'explanation': 'ElasticNet hybrid regularization balancing feature selection and ridge grouping.',
                      'function_name': 'elastic_net_loss',
                      'hint': 'Combine L1 and L2 penalties according to l1_ratio balance.',
                      'id': 'c2-m2-l2-a',
                      'prompt': 'Write `elastic_net_loss(mse, weights, alpha, l1_ratio)`: `mse + alpha * (l1_ratio * '
                                'sum(abs(w)) + 0.5 * (1 - l1_ratio) * sum(w**2))`. Round to 2 decimals.',
                      'solution_code': 'def elastic_net_loss(mse: float, weights: list, alpha: float, l1_ratio: float) '
                                       '-> float:\n'
                                       '    l1 = sum(abs(w) for w in weights)\n'
                                       '    l2 = sum(w**2 for w in weights)\n'
                                       '    pen = alpha * (l1_ratio * l1 + 0.5 * (1.0 - l1_ratio) * l2)\n'
                                       '    return round(mse + pen, 2)\n',
                      'starter_code': 'def elastic_net_loss(mse: float, weights: list, alpha: float, l1_ratio: float) '
                                      '-> float:\n'
                                      '    # Return total ElasticNet loss\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '10 + 1.0 * (0.5*4 + 0.5*0.5*8) = 10 + 4 = 14.0',
                                      'expected': 14.0,
                                      'input': [10.0, [2.0, -2.0], 1.0, 0.5]}],
                      'title': 'ElasticNet Combined Regularization Loss'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'alpha >= 0',
                    'difficulty': 'Basic',
                    'explanation': 'Ridge regression shrinkage parameter.',
                    'function_name': 'ridge_l2_penalty',
                    'hint': 'Multiply alpha by the sum of squares of weights.',
                    'id': 'c2-m2-l2-b',
                    'prompt': 'Write `ridge_l2_penalty(weights, alpha)` computing `alpha * sum(w**2)`. Round to 2 '
                              'decimals.',
                    'solution_code': 'def ridge_l2_penalty(weights: list, alpha: float) -> float:\n'
                                     '    return round(alpha * sum(w**2 for w in weights), 2)\n',
                    'starter_code': 'def ridge_l2_penalty(weights: list, alpha: float) -> float:\n'
                                    '    # Return L2 penalty\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '0.1 * (1 + 4 + 9) = 1.4',
                                    'expected': 1.4,
                                    'input': [[1.0, -2.0, 3.0], 0.1]}],
                    'title': 'Ridge L2 Regularization Penalty'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'alpha >= 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'Lasso regression sparsity-inducing L1 norm.',
                           'function_name': 'lasso_l1_penalty',
                           'hint': 'Multiply alpha by the sum of absolute values.',
                           'id': 'c2-m2-l2-i',
                           'prompt': 'Write `lasso_l1_penalty(weights, alpha)` computing `alpha * sum(abs(w))`. Round '
                                     'to 2 decimals.',
                           'solution_code': 'def lasso_l1_penalty(weights: list, alpha: float) -> float:\n'
                                            '    return round(alpha * sum(abs(w) for w in weights), 2)\n',
                           'starter_code': 'def lasso_l1_penalty(weights: list, alpha: float) -> float:\n'
                                           '    # Return L1 penalty\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '0.5 * (3 + 4) = 3.5',
                                           'expected': 3.5,
                                           'input': [[-3.0, 4.0], 0.5]}],
                           'title': 'Lasso L1 Regularization Penalty'}},
 (3, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': '0.0 <= threshold <= 1.0',
                      'difficulty': 'Advance',
                      'explanation': 'Threshold tuning to balance precision and recall.',
                      'function_name': 'predict_classes_with_threshold',
                      'hint': 'List comprehension [1 if p >= threshold else 0 for p in probabilities].',
                      'id': 'c2-m3-l1-a',
                      'prompt': 'Write `predict_classes_with_threshold(probabilities, threshold)` returning list of 1s '
                                '(if p >= threshold) and 0s.',
                      'solution_code': 'def predict_classes_with_threshold(probabilities: list, threshold: float) -> '
                                       'list:\n'
                                       '    return [1 if p >= threshold else 0 for p in probabilities]\n',
                      'starter_code': 'def predict_classes_with_threshold(probabilities: list, threshold: float) -> '
                                      'list:\n'
                                      '    # Return binary predictions\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Threshold 0.5', 'expected': [0, 1, 1], 'input': [[0.2, 0.5, 0.8], 0.5]},
                                     {'desc': 'Threshold 0.7', 'expected': [0, 0, 1], 'input': [[0.2, 0.5, 0.8], 0.7]}],
                      'title': 'Binary Classification Decision Thresholding'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': '-100 <= z <= 100',
                    'difficulty': 'Basic',
                    'explanation': 'Logistic curve mapping real line to probability space.',
                    'function_name': 'sigmoid_activation',
                    'hint': 'Use 2.71828 ** (-z).',
                    'id': 'c2-m3-l1-b',
                    'prompt': 'Write `sigmoid_activation(z)`: `1.0 / (1.0 + e^(-z))`. Round to 4 decimals with e = '
                              '2.71828.',
                    'solution_code': 'def sigmoid_activation(z: float) -> float:\n'
                                     '    e = 2.718281828459045\n'
                                     '    return round(1.0 / (1.0 + (e ** (-z))), 4)\n',
                    'starter_code': 'def sigmoid_activation(z: float) -> float:\n'
                                    '    # Return sigmoid value in (0, 1)\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Sigmoid of 0 is 0.5', 'expected': 0.5, 'input': [0.0]},
                                   {'desc': 'Sigmoid of 2', 'expected': 0.8808, 'input': [2.0]}],
                    'title': 'Sigmoid Activation Function'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'y_true contains 0 or 1, y_pred in (0, 1)',
                           'difficulty': 'Intermediate',
                           'explanation': 'Log-loss objective for binary logistic regression.',
                           'function_name': 'binary_cross_entropy',
                           'hint': 'import math; clip p to max(1e-15, min(1 - 1e-15, p)).',
                           'id': 'c2-m3-l1-i',
                           'prompt': 'Write `binary_cross_entropy(y_true, y_pred)`: `-1/N * sum(y*log(p) + '
                                     '(1-y)*log(1-p))` using math.log with epsilon clip 1e-15. Round to 4 decimals.',
                           'solution_code': 'def binary_cross_entropy(y_true: list, y_pred: list) -> float:\n'
                                            '    import math\n'
                                            '    n = len(y_true)\n'
                                            '    loss = 0.0\n'
                                            '    for y, p in zip(y_true, y_pred):\n'
                                            '        p_clip = max(1e-15, min(1.0 - 1e-15, p))\n'
                                            '        loss += y * math.log(p_clip) + (1 - y) * math.log(1.0 - p_clip)\n'
                                            '    return round(-loss / n, 4)\n',
                           'starter_code': 'def binary_cross_entropy(y_true: list, y_pred: list) -> float:\n'
                                           '    # Return log loss\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Confident accurate predictions',
                                           'expected': 0.1054,
                                           'input': [[1, 0], [0.9, 0.1]]}],
                           'title': 'Binary Cross Entropy Loss'}},
 (3, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'y_true in {-1, 1}',
                      'difficulty': 'Advance',
                      'explanation': 'Maximum margin optimization loss function.',
                      'function_name': 'svm_hinge_loss',
                      'hint': 'sum(max(0, 1 - y * s) for y, s in zip(y_true, scores)) / len(y_true).',
                      'id': 'c2-m3-l2-a',
                      'prompt': 'Write `svm_hinge_loss(y_true, scores)`: `1/N * sum(max(0, 1 - y * s))` where y_true '
                                'is -1 or 1 and scores are real numbers. Round to 4 decimals.',
                      'solution_code': 'def svm_hinge_loss(y_true: list, scores: list) -> float:\n'
                                       '    tot = sum(max(0.0, 1.0 - y * s) for y, s in zip(y_true, scores))\n'
                                       '    return round(tot / len(y_true), 4)\n',
                      'starter_code': 'def svm_hinge_loss(y_true: list, scores: list) -> float:\n'
                                      '    # Return hinge loss\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'First correct with margin (loss 0), second margin violation (loss 0.5)',
                                      'expected': 0.25,
                                      'input': [[1, -1], [1.5, -0.5]]}],
                      'title': 'Hinge Loss for Support Vector Machines'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'X is list of lists of same length',
                    'difficulty': 'Basic',
                    'explanation': 'Support Vector Machine linear kernel Gram matrix computation.',
                    'function_name': 'linear_kernel_matrix',
                    'hint': 'K[i][j] = sum(X[i][k] * X[j][k] for k).',
                    'id': 'c2-m3-l2-b',
                    'prompt': 'Write `linear_kernel_matrix(X)` computing dot product matrix `X @ X.T` for list of '
                              'vector points.',
                    'solution_code': 'def linear_kernel_matrix(X: list) -> list:\n'
                                     '    n = len(X)\n'
                                     '    return [[sum(a * b for a, b in zip(X[i], X[j])) for j in range(n)] for i in '
                                     'range(n)]\n',
                    'starter_code': 'def linear_kernel_matrix(X: list) -> list:\n    # Return Gram matrix\n    pass\n',
                    'test_cases': [{'desc': 'Dot product matrix',
                                    'expected': [[5, 11], [11, 25]],
                                    'input': [[[1, 2], [3, 4]]]}],
                    'title': 'Linear Kernel Gram Matrix'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'gamma > 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'Non-linear SVM projection into infinite-dimensional Hilbert space.',
                           'function_name': 'rbf_kernel_distance',
                           'hint': 'import math; sq_dist = sum((a - b)**2 for a, b in zip(x1, x2)); '
                                   'round(math.exp(-gamma * sq_dist), 4).',
                           'id': 'c2-m3-l2-i',
                           'prompt': 'Write `rbf_kernel_distance(x1, x2, gamma)`: `exp(-gamma * ||x1 - x2||^2)`. Round '
                                     'to 4 decimals.',
                           'solution_code': 'def rbf_kernel_distance(x1: list, x2: list, gamma: float) -> float:\n'
                                            '    import math\n'
                                            '    sq_dist = sum((a - b)**2 for a, b in zip(x1, x2))\n'
                                            '    return round(math.exp(-gamma * sq_dist), 4)\n',
                           'starter_code': 'def rbf_kernel_distance(x1: list, x2: list, gamma: float) -> float:\n'
                                           '    # Return RBF similarity\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Identical points = 1.0',
                                           'expected': 1.0,
                                           'input': [[1, 2], [1, 2], 0.1]},
                                          {'desc': 'Distance sq = 2, exp(-1) = 0.3679',
                                           'expected': 0.3679,
                                           'input': [[0, 0], [1, 1], 0.5]}],
                           'title': 'Radial Basis Function (RBF) Kernel Distance'}},
 (4, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'parent_labels == left + right',
                      'difficulty': 'Advance',
                      'explanation': 'Decision tree optimal feature threshold selection.',
                      'function_name': 'information_gain_split',
                      'hint': 'Compute entropy of parent and weighted sum of left and right entropies.',
                      'id': 'c2-m4-l1-a',
                      'prompt': 'Write `information_gain_split(parent_labels, left_labels, right_labels)`: `H(parent) '
                                '- (|left|/N * H(left) + |right|/N * H(right))` where H is entropy. Round to 4 '
                                'decimals.',
                      'solution_code': 'def information_gain_split(parent_labels: list, left_labels: list, '
                                       'right_labels: list) -> float:\n'
                                       '    import math\n'
                                       '    def h(labels):\n'
                                       '        if not labels: return 0.0\n'
                                       '        n = len(labels)\n'
                                       '        counts = {}\n'
                                       '        for l in labels: counts[l] = counts.get(l, 0) + 1\n'
                                       '        return -sum((c/n) * math.log2(c/n) for c in counts.values() if c > 0)\n'
                                       '    n = len(parent_labels)\n'
                                       '    ig = h(parent_labels) - (len(left_labels)/n * h(left_labels) + '
                                       'len(right_labels)/n * h(right_labels))\n'
                                       '    return round(ig, 4)\n',
                      'starter_code': 'def information_gain_split(parent_labels: list, left_labels: list, '
                                      'right_labels: list) -> float:\n'
                                      '    # Return information gain\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Perfect split gives 1.0 bit gain',
                                      'expected': 1.0,
                                      'input': [['A', 'A', 'B', 'B'], ['A', 'A'], ['B', 'B']]}],
                      'title': 'Information Gain from Threshold Split'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'labels is non-empty list',
                    'difficulty': 'Basic',
                    'explanation': 'CART decision tree node split evaluation.',
                    'function_name': 'calculate_gini_impurity',
                    'hint': 'Count occurrences of each class, divide by total, square and subtract from 1.',
                    'id': 'c2-m4-l1-b',
                    'prompt': 'Write `calculate_gini_impurity(labels)`: `1 - sum(p_i**2)` where p_i is class fraction. '
                              'Round to 4 decimals.',
                    'solution_code': 'def calculate_gini_impurity(labels: list) -> float:\n'
                                     '    n = len(labels)\n'
                                     '    counts = {}\n'
                                     '    for l in labels: counts[l] = counts.get(l, 0) + 1\n'
                                     '    return round(1.0 - sum((c / n)**2 for c in counts.values()), 4)\n',
                    'starter_code': 'def calculate_gini_impurity(labels: list) -> float:\n'
                                    '    # Return Gini impurity\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Pure leaf = 0.0', 'expected': 0.0, 'input': [['A', 'A', 'A']]},
                                   {'desc': '50/50 split = 0.5', 'expected': 0.5, 'input': [['A', 'B']]}],
                    'title': 'Gini Impurity Calculator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'labels is non-empty list',
                           'difficulty': 'Intermediate',
                           'explanation': 'Information theory metric used in ID3 and C4.5 decision trees.',
                           'function_name': 'calculate_entropy',
                           'hint': 'import math; -sum(p * math.log2(p)).',
                           'id': 'c2-m4-l1-i',
                           'prompt': 'Write `calculate_entropy(labels)`: `-sum(p * log2(p))` for each unique class '
                                     'with p > 0. Round to 4 decimals.',
                           'solution_code': 'def calculate_entropy(labels: list) -> float:\n'
                                            '    import math\n'
                                            '    n = len(labels)\n'
                                            '    counts = {}\n'
                                            '    for l in labels: counts[l] = counts.get(l, 0) + 1\n'
                                            '    ent = -sum((c/n) * math.log2(c/n) for c in counts.values() if c > 0)\n'
                                            '    return round(ent, 4)\n',
                           'starter_code': 'def calculate_entropy(labels: list) -> float:\n'
                                           '    # Return Shannon entropy\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Pure set = 0 bits', 'expected': 0.0, 'input': [['A', 'A']]},
                                          {'desc': 'Equal binary = 1.0 bit', 'expected': 1.0, 'input': [['A', 'B']]}],
                           'title': 'Shannon Entropy Calculator'}},
 (4, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all lists have equal length',
                      'difficulty': 'Advance',
                      'explanation': 'Sequential error minimization in XGBoost / LightGBM gradient boosted trees.',
                      'function_name': 'gradient_boost_step',
                      'hint': 'new = curr + lr * res for each element.',
                      'id': 'c2-m4-l2-a',
                      'prompt': 'Write `gradient_boost_step(y_true, current_predictions, learning_rate, '
                                'tree_residuals)`: `new_pred = curr + learning_rate * tree_res`. Return new '
                                'predictions rounded to 2 decimals.',
                      'solution_code': 'def gradient_boost_step(y_true: list, current_predictions: list, '
                                       'learning_rate: float, tree_residuals: list) -> list:\n'
                                       '    return [round(c + learning_rate * r, 2) for c, r in '
                                       'zip(current_predictions, tree_residuals)]\n',
                      'starter_code': 'def gradient_boost_step(y_true: list, current_predictions: list, learning_rate: '
                                      'float, tree_residuals: list) -> list:\n'
                                      '    # Return updated predictions\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Adds 0.1 * residual',
                                      'expected': [8.2, 15.5],
                                      'input': [[10, 20], [8.0, 15.0], 0.1, [2.0, 5.0]]}],
                      'title': 'Gradient Boosting Residual Update Step'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'tree_predictions is non-empty list',
                    'difficulty': 'Basic',
                    'explanation': 'Random forest consensus prediction aggregation.',
                    'function_name': 'majority_vote_classifier',
                    'hint': 'Count occurrences and return max by count.',
                    'id': 'c2-m4-l2-b',
                    'prompt': 'Write `majority_vote_classifier(tree_predictions)` where tree_predictions is a list of '
                              'predicted labels for a sample. Return the most common label.',
                    'solution_code': 'def majority_vote_classifier(tree_predictions: list):\n'
                                     '    counts = {}\n'
                                     '    for p in tree_predictions: counts[p] = counts.get(p, 0) + 1\n'
                                     '    return max(counts, key=counts.get)\n',
                    'starter_code': 'def majority_vote_classifier(tree_predictions: list):\n'
                                    '    # Return consensus class\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '3 dogs vs 2 cats',
                                    'expected': 'dog',
                                    'input': [['cat', 'dog', 'dog', 'cat', 'dog']]}],
                    'title': 'Majority Voting Ensemble Classifier'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'n_samples >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Bagging (Bootstrap Aggregation) data resampler.',
                           'function_name': 'bootstrap_sample_indices',
                           'hint': 'Generate [(i * seed_multiplier) % n_samples for i in range(n_samples)].',
                           'id': 'c2-m4-l2-i',
                           'prompt': 'Write `bootstrap_sample_indices(n_samples, seed_multiplier)` generating '
                                     '`n_samples` indices using `(i * seed_multiplier) % n_samples`. Return list of '
                                     'sampled indices.',
                           'solution_code': 'def bootstrap_sample_indices(n_samples: int, seed_multiplier: int) -> '
                                            'list:\n'
                                            '    return [(i * seed_multiplier) % n_samples for i in '
                                            'range(n_samples)]\n',
                           'starter_code': 'def bootstrap_sample_indices(n_samples: int, seed_multiplier: int) -> '
                                           'list:\n'
                                           '    # Return bootstrap indices\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Generates 5 indices with replacement simulator',
                                           'expected': [0, 3, 1, 4, 2],
                                           'input': [5, 3]}],
                           'title': 'Deterministic Bootstrap Sample Generator'}},
 (5, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all points have same dimensionality',
                      'difficulty': 'Advance',
                      'explanation': 'Objective criterion for the Elbow Method in clustering.',
                      'function_name': 'calculate_inertia',
                      'hint': 'Iterate centroid and points, compute distance squared and accumulate.',
                      'id': 'c2-m5-l1-a',
                      'prompt': 'Write `calculate_inertia(clusters)` where clusters is dict `{centroid_tuple: '
                                '[points]}`. Compute sum of squared Euclidean distances of each point to its assigned '
                                'centroid. Round to 2 decimals.',
                      'solution_code': 'def calculate_inertia(clusters: list) -> float:\n'
                                       '    tot = 0.0\n'
                                       '    for c, pts in clusters.items():\n'
                                       '        for p in pts:\n'
                                       '            tot += sum((a - b)**2 for a, b in zip(p, c))\n'
                                       '    return round(tot, 2)\n',
                      'starter_code': 'def calculate_inertia(clusters: list) -> float:\n'
                                      '    # Return total inertia\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '1 + 1 = 2.0', 'expected': 2.0, 'input': [[{'centroid': [0, 0], 'points': [[1, 0], [0, 1]]}]]}],
                      'title': 'K-Means Inertia (Sum of Squared Errors)'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'centroids is non-empty list of points',
                    'difficulty': 'Basic',
                    'explanation': 'K-Means Expectation step: Voronoi partition assignment.',
                    'function_name': 'assign_nearest_cluster',
                    'hint': 'Calculate sum((a - b)**2) for each centroid and find min index.',
                    'id': 'c2-m5-l1-b',
                    'prompt': 'Write `assign_nearest_cluster(point, centroids)` returning index of closest centroid by '
                              'Euclidean distance.',
                    'solution_code': 'def assign_nearest_cluster(point: list, centroids: list) -> int:\n'
                                     '    dists = [sum((a - b)**2 for a, b in zip(point, c)) for c in centroids]\n'
                                     '    return dists.index(min(dists))\n',
                    'starter_code': 'def assign_nearest_cluster(point: list, centroids: list) -> int:\n'
                                    '    # Return nearest centroid index\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Closest to [0,0] (index 0)',
                                    'expected': 0,
                                    'input': [[2, 2], [[0, 0], [10, 10]]]}],
                    'title': 'Assign Nearest Cluster Centroid'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'assigned_points is non-empty list of points',
                           'difficulty': 'Intermediate',
                           'explanation': 'K-Means Maximization step: centroid relocation to mean.',
                           'function_name': 'compute_cluster_centroid',
                           'hint': 'For each dimension, sum coordinates and divide by number of points.',
                           'id': 'c2-m5-l1-i',
                           'prompt': 'Write `compute_cluster_centroid(assigned_points)` computing mean of each '
                                     'dimension. Round to 2 decimals.',
                           'solution_code': 'def compute_cluster_centroid(assigned_points: list) -> list:\n'
                                            '    n, dims = len(assigned_points), len(assigned_points[0])\n'
                                            '    return [round(sum(p[d] for p in assigned_points) / n, 2) for d in '
                                            'range(dims)]\n',
                           'starter_code': 'def compute_cluster_centroid(assigned_points: list) -> list:\n'
                                           '    # Return center point\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Mean of 3 points is [2.0, 2.0]',
                                           'expected': [2.0, 2.0],
                                           'input': [[[0, 0], [2, 4], [4, 2]]]}],
                           'title': 'K-Means Centroid Recalculation'}},
 (5, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(row) == len(component_vector)',
                      'difficulty': 'Advance',
                      'explanation': 'Dimensionality reduction projection step: Z = X @ V.',
                      'function_name': 'project_to_1d_component',
                      'hint': 'Dot product of each row with the principal vector.',
                      'id': 'c2-m5-l2-a',
                      'prompt': 'Write `project_to_1d_component(X, component_vector)` computing dot product of each '
                                'row in X with component_vector. Round to 2 decimals.',
                      'solution_code': 'def project_to_1d_component(X: list, component_vector: list) -> list:\n'
                                       '    return [round(sum(a * b for a, b in zip(row, component_vector)), 2) for '
                                       'row in X]\n',
                      'starter_code': 'def project_to_1d_component(X: list, component_vector: list) -> list:\n'
                                      '    # Return 1D projections\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Extracts first dimension',
                                      'expected': [2.0, 4.0],
                                      'input': [[[2, 3], [4, 5]], [1, 0]]}],
                      'title': 'Principal Component 1D Projection'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'X is non-empty 2D list of numbers',
                    'difficulty': 'Basic',
                    'explanation': 'Mandatory first step of Principal Component Analysis (PCA).',
                    'function_name': 'center_data_matrix',
                    'hint': 'Find column means, subtract from each row element.',
                    'id': 'c2-m5-l2-b',
                    'prompt': 'Write `center_data_matrix(X)` subtracting column means from each row. Round to 2 '
                              'decimals.',
                    'solution_code': 'def center_data_matrix(X: list) -> list:\n'
                                     '    n_rows, n_cols = len(X), len(X[0])\n'
                                     '    means = [sum(X[r][c] for r in range(n_rows)) / n_rows for c in '
                                     'range(n_cols)]\n'
                                     '    return [[round(X[r][c] - means[c], 2) for c in range(n_cols)] for r in '
                                     'range(n_rows)]\n',
                    'starter_code': 'def center_data_matrix(X: list) -> list:\n'
                                    '    # Return mean-centered matrix\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Subtracts means 3 and 20',
                                    'expected': [[-2.0, -10.0], [0.0, 0.0], [2.0, 10.0]],
                                    'input': [[[1, 10], [3, 20], [5, 30]]]}],
                    'title': 'Center Data Matrix (Zero Mean)'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'eigenvalues is list of positive numbers',
                           'difficulty': 'Intermediate',
                           'explanation': 'PCA scree plot variance retention metric.',
                           'function_name': 'explained_variance_ratio',
                           'hint': 'Divide each eigenvalue by the total sum of eigenvalues.',
                           'id': 'c2-m5-l2-i',
                           'prompt': 'Write `explained_variance_ratio(eigenvalues)` computing `lambda_i / '
                                     'sum(eigenvalues)` for each eigenvalue. Round to 4 decimals.',
                           'solution_code': 'def explained_variance_ratio(eigenvalues: list) -> list:\n'
                                            '    tot = sum(eigenvalues)\n'
                                            '    return [round(e / tot, 4) for e in eigenvalues]\n',
                           'starter_code': 'def explained_variance_ratio(eigenvalues: list) -> list:\n'
                                           '    # Return proportion of variance\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '4/5 = 0.8, 1/5 = 0.2',
                                           'expected': [0.8, 0.2],
                                           'input': [[4.0, 1.0]]}],
                           'title': 'Explained Variance Ratio Calculator'}},
 (6, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'fpr sorted ascending from 0.0 to 1.0',
                      'difficulty': 'Advance',
                      'explanation': 'Scikit-learn roc_auc_score numerical integration.',
                      'function_name': 'trapezoidal_auc_score',
                      'hint': 'Iterate i from 1 to len(fpr) and sum trapezoid areas.',
                      'id': 'c2-m6-l1-a',
                      'prompt': 'Write `trapezoidal_auc_score(fpr_points, tpr_points)` computing area under curve '
                                'using trapezoid rule: `sum((fpr[i] - fpr[i-1]) * (tpr[i] + tpr[i-1]) / 2)`. Round to '
                                '4 decimals.',
                      'solution_code': 'def trapezoidal_auc_score(fpr_points: list, tpr_points: list) -> float:\n'
                                       '    auc = 0.0\n'
                                       '    for i in range(1, len(fpr_points)):\n'
                                       '        dx = fpr_points[i] - fpr_points[i - 1]\n'
                                       '        h = (tpr_points[i] + tpr_points[i - 1]) / 2.0\n'
                                       '        auc += dx * h\n'
                                       '    return round(auc, 4)\n',
                      'starter_code': 'def trapezoidal_auc_score(fpr_points: list, tpr_points: list) -> float:\n'
                                      '    # Return AUC score in [0, 1]\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Perfect classifier ROC AUC = 1.0',
                                      'expected': 1.0,
                                      'input': [[0.0, 0.0, 1.0], [0.0, 1.0, 1.0]]},
                                     {'desc': 'Random classifier AUC = 0.5',
                                      'expected': 0.5,
                                      'input': [[0.0, 1.0], [0.0, 1.0]]}],
                      'title': 'Trapezoidal ROC-AUC Approximation'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'lists contain 0 or 1',
                    'difficulty': 'Basic',
                    'explanation': 'Foundation of all classification diagnostic metrics.',
                    'function_name': 'compute_confusion_matrix',
                    'hint': 'Compare each pair: 1,1=TP, 0,1=FP, 0,0=TN, 1,0=FN.',
                    'id': 'c2-m6-l1-b',
                    'prompt': 'Write `compute_confusion_matrix(y_true, y_pred)` returning `{"TP": tp, "FP": fp, "TN": '
                              'tn, "FN": fn}` where positive class is 1 and negative is 0.',
                    'solution_code': 'def compute_confusion_matrix(y_true: list, y_pred: list) -> dict:\n'
                                     '    tp, fp, tn, fn = 0, 0, 0, 0\n'
                                     '    for yt, yp in zip(y_true, y_pred):\n'
                                     '        if yt == 1 and yp == 1: tp += 1\n'
                                     '        elif yt == 0 and yp == 1: fp += 1\n'
                                     '        elif yt == 0 and yp == 0: tn += 1\n'
                                     '        elif yt == 1 and yp == 0: fn += 1\n'
                                     '    return {"TP": tp, "FP": fp, "TN": tn, "FN": fn}\n',
                    'starter_code': 'def compute_confusion_matrix(y_true: list, y_pred: list) -> dict:\n'
                                    '    # Return TP, FP, TN, FN\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2 TP, 0 FP, 1 TN, 1 FN',
                                    'expected': {'FN': 1, 'FP': 0, 'TN': 1, 'TP': 2},
                                    'input': [[1, 0, 1, 1], [1, 0, 0, 1]]}],
                    'title': 'Binary Confusion Matrix Counter'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'tp, fp, fn are non-negative ints',
                           'difficulty': 'Intermediate',
                           'explanation': 'Harmonic mean of precision and recall for imbalanced datasets.',
                           'function_name': 'calculate_f1_score',
                           'hint': 'Calculate precision and recall, handle zero divisions.',
                           'id': 'c2-m6-l1-i',
                           'prompt': 'Write `calculate_f1_score(tp, fp, fn)`: Precision = TP/(TP+FP), Recall = '
                                     'TP/(TP+FN), F1 = 2*P*R/(P+R). Round to 4 decimals.',
                           'solution_code': 'def calculate_f1_score(tp: int, fp: int, fn: int) -> dict:\n'
                                            '    p = tp / (tp + fp) if (tp + fp) > 0 else 0.0\n'
                                            '    r = tp / (tp + fn) if (tp + fn) > 0 else 0.0\n'
                                            '    f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0\n'
                                            '    return {"precision": round(p, 4), "recall": round(r, 4), "f1": '
                                            'round(f1, 4)}\n',
                           'starter_code': 'def calculate_f1_score(tp: int, fp: int, fn: int) -> dict:\n'
                                           '    # Return precision, recall, f1\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Symmetric 0.8',
                                           'expected': {'f1': 0.8, 'precision': 0.8, 'recall': 0.8},
                                           'input': [80, 20, 20]}],
                           'title': 'Precision, Recall and F1-Score'}},
 (6, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'patience >= 1, min_delta >= 0',
                      'difficulty': 'Advance',
                      'explanation': 'Early stopping callback mechanism preventing overfitting.',
                      'function_name': 'early_stopping_monitor',
                      'hint': 'Track best_loss and bad_epochs counter.',
                      'id': 'c2-m6-l2-a',
                      'prompt': 'Write `early_stopping_monitor(val_losses, patience, min_delta)` returning the '
                                '0-indexed epoch where training should stop (no improvement by >= min_delta for '
                                'patience consecutive epochs). If training never stopped return len(val_losses) - 1.',
                      'solution_code': 'def early_stopping_monitor(val_losses: list, patience: int, min_delta: float) '
                                       '-> int:\n'
                                       '    best = val_losses[0]\n'
                                       '    bad = 0\n'
                                       '    for ep, l in enumerate(val_losses[1:], start=1):\n'
                                       '        if best - l >= min_delta:\n'
                                       '            best = l\n'
                                       '            bad = 0\n'
                                       '        else:\n'
                                       '            bad += 1\n'
                                       '            if bad >= patience:\n'
                                       '                return ep\n'
                                       '    return len(val_losses) - 1\n',
                      'starter_code': 'def early_stopping_monitor(val_losses: list, patience: int, min_delta: float) '
                                      '-> int:\n'
                                      '    # Return stopping epoch index\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Best 0.8 at epoch 1. Epochs 2 and 3 did not improve by 0.05 -> stops at '
                                              '3',
                                      'expected': 3,
                                      'input': [[1.0, 0.8, 0.79, 0.81, 0.82], 2, 0.05]}],
                      'title': 'Early Stopping Epoch Monitor'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'param_grid has 1 or 2 keys',
                    'difficulty': 'Basic',
                    'explanation': 'Scikit-learn GridSearchCV hyperparameter cartesian product.',
                    'function_name': 'generate_grid_combinations',
                    'hint': 'Use itertools.product or nested loops over items.',
                    'id': 'c2-m6-l2-b',
                    'prompt': 'Write `generate_grid_combinations(param_grid)` where param_grid is `{param: [values]}`. '
                              'Return list of all combination dicts.',
                    'solution_code': 'def generate_grid_combinations(param_grid: dict) -> list:\n'
                                     '    keys = list(param_grid.keys())\n'
                                     '    if not keys: return []\n'
                                     '    import itertools\n'
                                     '    values = [param_grid[k] for k in keys]\n'
                                     '    return [dict(zip(keys, prod)) for prod in itertools.product(*values)]\n',
                    'starter_code': 'def generate_grid_combinations(param_grid: dict) -> list:\n'
                                    '    # Return list of config dicts\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2x2 grid = 4 configs',
                                    'expected': [{'C': 0.1, 'kernel': 'linear'},
                                                 {'C': 0.1, 'kernel': 'rbf'},
                                                 {'C': 1.0, 'kernel': 'linear'},
                                                 {'C': 1.0, 'kernel': 'rbf'}],
                                    'input': [{'C': [0.1, 1.0], 'kernel': ['linear', 'rbf']}]}],
                    'title': 'Grid Search Parameter Combinations'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'total_samples >= k >= 2',
                           'difficulty': 'Intermediate',
                           'explanation': 'Standard KFold cross-validation protocol.',
                           'function_name': 'k_fold_split_indices',
                           'hint': 'chunk_size = total_samples // k. val is slice, train is the rest.',
                           'id': 'c2-m6-l2-i',
                           'prompt': 'Write `k_fold_split_indices(total_samples, k)` partitioning 0..total_samples-1 '
                                     'into k contiguous chunks. Return list of k dicts `{"train": [...], "val": '
                                     '[...]}`.',
                           'solution_code': 'def k_fold_split_indices(total_samples: int, k: int) -> list:\n'
                                            '    chunk = total_samples // k\n'
                                            '    all_idx = list(range(total_samples))\n'
                                            '    res = []\n'
                                            '    for i in range(k):\n'
                                            '        start = i * chunk\n'
                                            '        end = (i + 1) * chunk if i < k - 1 else total_samples\n'
                                            '        val = all_idx[start:end]\n'
                                            '        train = all_idx[:start] + all_idx[end:]\n'
                                            '        res.append({"train": train, "val": val})\n'
                                            '    return res\n',
                           'starter_code': 'def k_fold_split_indices(total_samples: int, k: int) -> list:\n'
                                           '    # Return K fold splits\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '3 folds of size 2',
                                           'expected': [{'train': [2, 3, 4, 5], 'val': [0, 1]},
                                                        {'train': [0, 1, 4, 5], 'val': [2, 3]},
                                                        {'train': [0, 1, 2, 3], 'val': [4, 5]}],
                                           'input': [6, 3]}],
                           'title': 'K-Fold Cross-Validation Split Indices'}}}
