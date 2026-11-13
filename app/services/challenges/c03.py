"""Course 3 topic-specific programming challenges."""

CHALLENGES = {(1, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(inputs) == len(weights)',
                      'difficulty': 'Advance',
                      'explanation': 'Fundamental perceptron affine transformation with non-linear activation.',
                      'function_name': 'neuron_forward',
                      'hint': 'Dot product plus bias passed into max(0.0, ...).',
                      'id': 'c3-m1-l1-a',
                      'prompt': 'Write `neuron_forward(inputs, weights, bias)` computing `relu(dot(inputs, weights) + '
                                'bias)`. Round to 2 decimals.',
                      'solution_code': 'def neuron_forward(inputs: list, weights: list, bias: float) -> float:\n'
                                       '    z = sum(x * w for x, w in zip(inputs, weights)) + bias\n'
                                       '    return round(max(0.0, float(z)), 2)\n',
                      'starter_code': 'def neuron_forward(inputs: list, weights: list, bias: float) -> float:\n'
                                      '    # Return activated output\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '1.0 - 3.0 + 1.0 = -1.0 -> 0.0',
                                      'expected': 0.0,
                                      'input': [[2.0, 3.0], [0.5, -1.0], 1.0]},
                                     {'desc': '2.0 + 3.0 - 1.0 = 4.0',
                                      'expected': 4.0,
                                      'input': [[1.0, 2.0], [2.0, 1.5], -1.0]}],
                      'title': 'Single Neuron Forward Feed'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'values is list of numbers',
                    'difficulty': 'Basic',
                    'explanation': 'Non-linear Rectified Linear Unit activation standard across modern deep networks.',
                    'function_name': 'relu_activation',
                    'hint': 'Use max(0.0, float(x)) in list comprehension.',
                    'id': 'c3-m1-l1-b',
                    'prompt': 'Write `relu_activation(values)` returning `[max(0.0, float(x)) for x in values]`.',
                    'solution_code': 'def relu_activation(values: list) -> list:\n'
                                     '    return [max(0.0, float(x)) for x in values]\n',
                    'starter_code': 'def relu_activation(values: list) -> list:\n'
                                    '    # Return ReLU activated values\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Zeros negative inputs',
                                    'expected': [0.0, 0.0, 3.2, 0.0],
                                    'input': [[-5.0, 0.0, 3.2, -1.1]]}],
                    'title': 'ReLU Activation Function'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'logits is non-empty list of numbers',
                           'difficulty': 'Intermediate',
                           'explanation': 'Converts unnormalized raw network logits to a valid categorical probability '
                                          'simplex.',
                           'function_name': 'softmax_probabilities',
                           'hint': 'import math; subtract max for stability before exp.',
                           'id': 'c3-m1-l1-i',
                           'prompt': 'Write `softmax_probabilities(logits)` computing `exp(x - max(logits)) / '
                                     'sum(exp(x - max(logits)))` for numerical stability. Round to 4 decimals.',
                           'solution_code': 'def softmax_probabilities(logits: list) -> list:\n'
                                            '    import math\n'
                                            '    mx = max(logits)\n'
                                            '    exps = [math.exp(x - mx) for x in logits]\n'
                                            '    tot = sum(exps)\n'
                                            '    return [round(e / tot, 4) for e in exps]\n',
                           'starter_code': 'def softmax_probabilities(logits: list) -> list:\n'
                                           '    # Return normalized probability distribution\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Probabilities sum to 1',
                                           'expected': [0.09, 0.2447, 0.6652],
                                           'input': [[1.0, 2.0, 3.0]]}],
                           'title': 'Softmax Multi-Class Probabilities'}},
 (1, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 't >= 1, 0 < beta1 < 1, 0 < beta2 < 1',
                      'difficulty': 'Advance',
                      'explanation': 'Adam optimizer first and second moment bias-correction.',
                      'function_name': 'adam_step_moments',
                      'hint': 'Compute m and v, divide by (1 - beta**t).',
                      'id': 'c3-m1-l2-a',
                      'prompt': 'Write `adam_step_moments(m_prev, v_prev, grad, beta1, beta2, t)` computing first '
                                'moment `m = beta1*m_prev + (1-beta1)*grad`, second moment `v = beta2*v_prev + '
                                '(1-beta2)*grad^2`, and bias-corrected `m_hat = m / (1 - beta1^t)`, `v_hat = v / (1 - '
                                'beta2^t)`. Return `{"m_hat": round(m_hat, 4), "v_hat": round(v_hat, 4)}`.',
                      'solution_code': 'def adam_step_moments(m_prev: float, v_prev: float, grad: float, beta1: float, '
                                       'beta2: float, t: int) -> dict:\n'
                                       '    m = beta1 * m_prev + (1.0 - beta1) * grad\n'
                                       '    v = beta2 * v_prev + (1.0 - beta2) * (grad ** 2)\n'
                                       '    m_hat = m / (1.0 - (beta1 ** t))\n'
                                       '    v_hat = v / (1.0 - (beta2 ** t))\n'
                                       '    return {"m_hat": round(m_hat, 4), "v_hat": round(v_hat, 4)}\n',
                      'starter_code': 'def adam_step_moments(m_prev: float, v_prev: float, grad: float, beta1: float, '
                                      'beta2: float, t: int) -> dict:\n'
                                      '    # Return bias-corrected moments\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'At step t=1 bias correction unbiases zero init',
                                      'expected': {'m_hat': 0.5, 'v_hat': 0.25},
                                      'input': [0.0, 0.0, 0.5, 0.9, 0.999, 1]}],
                      'title': 'Adam Optimizer Bias-Corrected Moments'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'values is list of numbers',
                    'difficulty': 'Basic',
                    'explanation': 'Backpropagation chain rule term through a ReLU non-linearity.',
                    'function_name': 'relu_derivative',
                    'hint': '[1.0 if x > 0 else 0.0 for x in values]',
                    'id': 'c3-m1-l2-b',
                    'prompt': 'Write `relu_derivative(values)` returning 1.0 if x > 0 else 0.0 for each value.',
                    'solution_code': 'def relu_derivative(values: list) -> list:\n'
                                     '    return [1.0 if x > 0 else 0.0 for x in values]\n',
                    'starter_code': 'def relu_derivative(values: list) -> list:\n'
                                    '    # Return gradient vector\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Only positive inputs have gradient 1.0',
                                    'expected': [0.0, 0.0, 1.0],
                                    'input': [[-2.5, 0.0, 3.1]]}],
                    'title': 'ReLU Derivative Gradient'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(weights) == len(gradients)',
                           'difficulty': 'Intermediate',
                           'explanation': 'Stochastic Gradient Descent parameter step equation.',
                           'function_name': 'sgd_weight_update',
                           'hint': 'w - learning_rate * g for each pair.',
                           'id': 'c3-m1-l2-i',
                           'prompt': 'Write `sgd_weight_update(weights, gradients, learning_rate)`: `w_new = w - lr * '
                                     'grad`. Round to 4 decimals.',
                           'solution_code': 'def sgd_weight_update(weights: list, gradients: list, learning_rate: '
                                            'float) -> list:\n'
                                            '    return [round(w - learning_rate * g, 4) for w, g in zip(weights, '
                                            'gradients)]\n',
                           'starter_code': 'def sgd_weight_update(weights: list, gradients: list, learning_rate: '
                                           'float) -> list:\n'
                                           '    # Return updated weights\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Subtracts lr * grad',
                                           'expected': [0.999, -0.498],
                                           'input': [[1.0, -0.5], [0.1, -0.2], 0.01]}],
                           'title': 'SGD Weight Update Step'}},
 (2, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'both lists of identical length',
                      'difficulty': 'Advance',
                      'explanation': 'Gradient accumulation for training massive models on constrained GPU VRAM.',
                      'function_name': 'accumulate_graph_gradients',
                      'hint': 'Add corresponding elements: p + s.',
                      'id': 'c3-m2-l1-a',
                      'prompt': 'Write `accumulate_graph_gradients(param_grads, step_grads)` adding step_grads into '
                                'param_grads element-wise. Round to 4 decimals.',
                      'solution_code': 'def accumulate_graph_gradients(param_grads: list, step_grads: list) -> list:\n'
                                       '    return [round(p + s, 4) for p, s in zip(param_grads, step_grads)]\n',
                      'starter_code': 'def accumulate_graph_gradients(param_grads: list, step_grads: list) -> list:\n'
                                      '    # Return accumulated gradients\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Accumulates gradients across micro-batches',
                                      'expected': [0.3, 0.4],
                                      'input': [[0.1, 0.5], [0.2, -0.1]]}],
                      'title': 'Autograd Computational Graph Accumulation'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'tensor is non-empty 2D list of numbers',
                    'difficulty': 'Basic',
                    'explanation': 'PyTorch tensor.shape and tensor.numel() introspection.',
                    'function_name': 'tensor_shape_and_size',
                    'hint': 'rows = len(tensor), cols = len(tensor[0]).',
                    'id': 'c3-m2-l1-b',
                    'prompt': 'Write `tensor_shape_and_size(tensor)` returning `{"shape": [rows, cols], "numel": rows '
                              '* cols}`.',
                    'solution_code': 'def tensor_shape_and_size(tensor: list) -> dict:\n'
                                     '    r, c = len(tensor), len(tensor[0])\n'
                                     '    return {"shape": [r, c], "numel": r * c}\n',
                    'starter_code': 'def tensor_shape_and_size(tensor: list) -> dict:\n'
                                    '    # Return shape and total elements\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2x3 tensor numel 6',
                                    'expected': {'numel': 6, 'shape': [2, 3]},
                                    'input': [[[1, 2, 3], [4, 5, 6]]]}],
                    'title': '2D Tensor Shape and Element Count'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'max_norm > 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'PyTorch torch.nn.utils.clip_grad_norm_ to stabilize exploding gradients.',
                           'function_name': 'clip_gradient_norm',
                           'hint': 'Calculate L2 norm, scale if > max_norm.',
                           'id': 'c3-m2-l1-i',
                           'prompt': 'Write `clip_gradient_norm(gradients, max_norm)`: total_norm = sqrt(sum(g**2)). '
                                     'If total_norm > max_norm, scale each g by `max_norm / total_norm`. Round to 4 '
                                     'decimals.',
                           'solution_code': 'def clip_gradient_norm(gradients: list, max_norm: float) -> list:\n'
                                            '    total_norm = (sum(g**2 for g in gradients)) ** 0.5\n'
                                            '    if total_norm <= max_norm or total_norm == 0:\n'
                                            '        return [round(float(g), 4) for g in gradients]\n'
                                            '    scale = max_norm / total_norm\n'
                                            '    return [round(g * scale, 4) for g in gradients]\n',
                           'starter_code': 'def clip_gradient_norm(gradients: list, max_norm: float) -> list:\n'
                                           '    # Return clipped gradients\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Norm 5.0 clipped to 2.5 (half)',
                                           'expected': [1.5, 2.0],
                                           'input': [[3.0, 4.0], 2.5]},
                                          {'desc': 'Norm < max_norm untouched',
                                           'expected': [1.0, 1.0],
                                           'input': [[1.0, 1.0], 5.0]}],
                           'title': 'Gradient Norm Clipping'}},
 (2, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'batch_sizes are positive ints',
                      'difficulty': 'Advance',
                      'explanation': 'Standard metric computation in PyTorch custom training loops.',
                      'function_name': 'epoch_loss_accumulator',
                      'hint': 'Multiply each batch loss by its sample count and divide by total samples.',
                      'id': 'c3-m2-l2-a',
                      'prompt': 'Write `epoch_loss_accumulator(batch_losses, batch_sizes)` computing weighted average '
                                'epoch loss: `sum(loss * size) / sum(size)`. Round to 4 decimals.',
                      'solution_code': 'def epoch_loss_accumulator(batch_losses: list, batch_sizes: list) -> float:\n'
                                       '    tot_loss = sum(l * s for l, s in zip(batch_losses, batch_sizes))\n'
                                       '    tot_samples = sum(batch_sizes)\n'
                                       '    return round(tot_loss / tot_samples, 4) if tot_samples > 0 else 0.0\n',
                      'starter_code': 'def epoch_loss_accumulator(batch_losses: list, batch_sizes: list) -> float:\n'
                                      '    # Return weighted epoch loss\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '(32*1.0 + 64*0.5)/96 = 64/96 = 0.6667',
                                      'expected': 0.6667,
                                      'input': [[1.0, 0.5], [32, 64]]}],
                      'title': 'Training Epoch Batch Loss Accumulator'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(x) == len(weights_matrix)',
                    'difficulty': 'Basic',
                    'explanation': 'PyTorch nn.Linear forward pass.',
                    'function_name': 'linear_layer_forward',
                    'hint': 'For each output j: sum(x[i] * weights_matrix[i][j]) + bias_vector[j].',
                    'id': 'c3-m2-l2-b',
                    'prompt': 'Write `linear_layer_forward(x, weights_matrix, bias_vector)`: `y_j = sum(x_i * W_ij) + '
                              'b_j`. Round to 2 decimals.',
                    'solution_code': 'def linear_layer_forward(x: list, weights_matrix: list, bias_vector: list) -> '
                                     'list:\n'
                                     '    n_in = len(x)\n'
                                     '    n_out = len(bias_vector)\n'
                                     '    res = []\n'
                                     '    for j in range(n_out):\n'
                                     '        val = sum(x[i] * weights_matrix[i][j] for i in range(n_in)) + '
                                     'bias_vector[j]\n'
                                     '        res.append(round(val, 2))\n'
                                     '    return res\n',
                    'starter_code': 'def linear_layer_forward(x: list, weights_matrix: list, bias_vector: list) -> '
                                    'list:\n'
                                    '    # Return layer output vector\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '1*0.5 + 2*(-1) + 0.1 = -1.4, 1*1 + 2*0.5 + 0.2 = 2.2',
                                    'expected': [-1.4, 2.2],
                                    'input': [[1.0, 2.0], [[0.5, 1.0], [-1.0, 0.5]], [0.1, 0.2]]}],
                    'title': 'Linear Layer Affine Forward'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'mask contains 0 or 1, drop_prob < 1.0',
                           'difficulty': 'Intermediate',
                           'explanation': 'PyTorch nn.Dropout inverted scaling to maintain constant expected '
                                          'activation norm.',
                           'function_name': 'dropout_layer_forward',
                           'hint': 'Multiply by mask and divide by (1.0 - drop_prob).',
                           'id': 'c3-m2-l2-i',
                           'prompt': 'Write `dropout_layer_forward(activations, mask, drop_prob)`: if training '
                                     '(drop_prob > 0), `x_i * mask_i / (1 - drop_prob)`. Round to 2 decimals.',
                           'solution_code': 'def dropout_layer_forward(activations: list, mask: list, drop_prob: '
                                            'float) -> list:\n'
                                            '    scale = 1.0 / (1.0 - drop_prob) if drop_prob < 1.0 else 0.0\n'
                                            '    return [round(a * m * scale, 2) for a, m in zip(activations, mask)]\n',
                           'starter_code': 'def dropout_layer_forward(activations: list, mask: list, drop_prob: float) '
                                           '-> list:\n'
                                           '    # Return scaled activations\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Scaled by 1/(1-0.5) = 2.0',
                                           'expected': [20.0, 0.0, 60.0],
                                           'input': [[10.0, 20.0, 30.0], [1, 0, 1], 0.5]}],
                           'title': 'Inverted Dropout Layer Forward'}},
 (3, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'stride >= 1, padding >= 0',
                      'difficulty': 'Advance',
                      'explanation': 'PyTorch convolutional arithmetic formula for layer design.',
                      'function_name': 'conv_output_dimension',
                      'hint': '(input_size - kernel_size + 2 * padding) // stride + 1.',
                      'id': 'c3-m3-l1-a',
                      'prompt': 'Write `conv_output_dimension(input_size, kernel_size, stride, padding)`: '
                                '`floor((input_size - kernel_size + 2*padding) / stride) + 1`.',
                      'solution_code': 'def conv_output_dimension(input_size: int, kernel_size: int, stride: int, '
                                       'padding: int) -> int:\n'
                                       '    return ((input_size - kernel_size + 2 * padding) // stride) + 1\n',
                      'starter_code': 'def conv_output_dimension(input_size: int, kernel_size: int, stride: int, '
                                      'padding: int) -> int:\n'
                                      '    # Return output spatial dimension\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Same padding retains 32x32', 'expected': 32, 'input': [32, 5, 1, 2]},
                                     {'desc': 'Stride 2 halves dimension', 'expected': 16, 'input': [32, 3, 2, 1]}],
                      'title': 'Feature Map Output Dimension Formula'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(matrix) % pool_size == 0',
                    'difficulty': 'Basic',
                    'explanation': 'PyTorch nn.MaxPool2d translation-invariant spatial downsampling.',
                    'function_name': 'max_pool_2d',
                    'hint': 'Iterate r and c by step pool_size, take max of submatrix.',
                    'id': 'c3-m3-l1-b',
                    'prompt': 'Write `max_pool_2d(matrix, pool_size)` on square matrix of size divisible by pool_size, '
                              'computing max within each non-overlapping pool window.',
                    'solution_code': 'def max_pool_2d(matrix: list, pool_size: int) -> list:\n'
                                     '    n = len(matrix)\n'
                                     '    out_n = n // pool_size\n'
                                     '    out = []\n'
                                     '    for r in range(out_n):\n'
                                     '        row = []\n'
                                     '        for c in range(out_n):\n'
                                     '            val = max(matrix[r*pool_size + i][c*pool_size + j] for i in '
                                     'range(pool_size) for j in range(pool_size))\n'
                                     '            row.append(val)\n'
                                     '        out.append(row)\n'
                                     '    return out\n',
                    'starter_code': 'def max_pool_2d(matrix: list, pool_size: int) -> list:\n'
                                    '    # Return pooled matrix\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2x2 pooling on 4x4',
                                    'expected': [[6, 8], [9, 7]],
                                    'input': [[[1, 3, 2, 4], [5, 6, 7, 8], [9, 1, 3, 2], [4, 5, 6, 7]], 2]}],
                    'title': '2D Max Pooling Layer'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'kernel size <= image size',
                           'difficulty': 'Intermediate',
                           'explanation': 'Cross-correlation / convolution operation in CNN feature extractors.',
                           'function_name': 'conv2d_valid',
                           'hint': 'Slide kernel across valid positions, sum products.',
                           'id': 'c3-m3-l1-i',
                           'prompt': 'Write `conv2d_valid(image, kernel)`: output size `(H - K_h + 1) x (W - K_w + '
                                     '1)`. Element is sum of elementwise products of kernel and receptive window.',
                           'solution_code': 'def conv2d_valid(image: list, kernel: list) -> list:\n'
                                            '    H, W = len(image), len(image[0])\n'
                                            '    kH, kW = len(kernel), len(kernel[0])\n'
                                            '    out_H, out_W = H - kH + 1, W - kW + 1\n'
                                            '    out = []\n'
                                            '    for r in range(out_H):\n'
                                            '        row = []\n'
                                            '        for c in range(out_W):\n'
                                            '            val = sum(image[r + i][c + j] * kernel[i][j] for i in '
                                            'range(kH) for j in range(kW))\n'
                                            '            row.append(val)\n'
                                            '        out.append(row)\n'
                                            '    return out\n',
                           'starter_code': 'def conv2d_valid(image: list, kernel: list) -> list:\n'
                                           '    # Return convolution feature map\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Diagonal kernel conv',
                                           'expected': [[6, 8], [12, 14]],
                                           'input': [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, 1]]]}],
                           'title': '2D Valid Convolution (Single Channel)'}},
 (3, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'image is 2D list of pixel values',
                      'difficulty': 'Advance',
                      'explanation': 'PyTorch torchvision.transforms.RandomHorizontalFlip implementation.',
                      'function_name': 'horizontal_flip_augmentation',
                      'hint': '[row[::-1] for row in image]',
                      'id': 'c3-m3-l2-a',
                      'prompt': 'Write `horizontal_flip_augmentation(image)` reversing pixels along horizontal axis: '
                                '`row[::-1]` for each row.',
                      'solution_code': 'def horizontal_flip_augmentation(image: list) -> list:\n'
                                       '    return [row[::-1] for row in image]\n',
                      'starter_code': 'def horizontal_flip_augmentation(image: list) -> list:\n'
                                      '    # Return flipped image\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Reverses each row horizontally',
                                      'expected': [[3, 2, 1], [6, 5, 4]],
                                      'input': [[[1, 2, 3], [4, 5, 6]]]}],
                      'title': 'Image Horizontal Flip Data Augmentation'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'tensor_3d is 3D list of numbers',
                    'difficulty': 'Basic',
                    'explanation': 'PyTorch nn.Flatten() transition from conv layers to linear classification heads.',
                    'function_name': 'flatten_feature_maps',
                    'hint': '[x for ch in tensor_3d for row in ch for x in row].',
                    'id': 'c3-m3-l2-b',
                    'prompt': 'Write `flatten_feature_maps(tensor_3d)` where tensor_3d is `[channels][height][width]`. '
                              'Return 1D list in channel-major order.',
                    'solution_code': 'def flatten_feature_maps(tensor_3d: list) -> list:\n'
                                     '    return [x for ch in tensor_3d for row in ch for x in row]\n',
                    'starter_code': 'def flatten_feature_maps(tensor_3d: list) -> list:\n'
                                    '    # Return flat 1D vector\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Flattens 2x2x2 to length 8',
                                    'expected': [1, 2, 3, 4, 5, 6, 7, 8],
                                    'input': [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]]}],
                    'title': 'Flatten Multi-Channel Feature Maps'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(predicted_logits) == len(true_classes) >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Top-1 classification accuracy on ImageNet and computer vision benchmarks.',
                           'function_name': 'top1_accuracy_score',
                           'hint': 'Find argmax of each logits row, compare to true class.',
                           'id': 'c3-m3-l2-i',
                           'prompt': 'Write `top1_accuracy_score(predicted_logits, true_classes)` where sample '
                                     'prediction is argmax of logits. Return accuracy fraction rounded to 4 decimals.',
                           'solution_code': 'def top1_accuracy_score(predicted_logits: list, true_classes: list) -> '
                                            'float:\n'
                                            '    correct = sum(1 for row, tc in zip(predicted_logits, true_classes) if '
                                            'row.index(max(row)) == tc)\n'
                                            '    return round(correct / len(true_classes), 4)\n',
                           'starter_code': 'def top1_accuracy_score(predicted_logits: list, true_classes: list) -> '
                                           'float:\n'
                                           '    # Return accuracy fraction in [0, 1]\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '2 of 3 correct',
                                           'expected': 0.6667,
                                           'input': [[[2.1, 0.5], [0.1, 1.8], [0.9, 0.2]], [0, 1, 1]]}],
                           'title': 'Top-1 Classification Accuracy'}},
 (4, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'current_step <= total_steps',
                      'difficulty': 'Advance',
                      'explanation': 'PyTorch CosineAnnealingWarmRestarts learning rate schedule.',
                      'function_name': 'warmup_cosine_lr',
                      'hint': 'import math; branch on current_step < warmup_steps, use math.cos.',
                      'id': 'c3-m4-l1-a',
                      'prompt': 'Write `warmup_cosine_lr(base_lr, current_step, warmup_steps, total_steps)`: if '
                                'current_step < warmup_steps, `base_lr * (current_step / warmup_steps)`. Else `0.5 * '
                                'base_lr * (1 + cos(pi * (current_step - warmup_steps)/(total_steps - '
                                'warmup_steps)))`. Round to 6 decimals.',
                      'solution_code': 'def warmup_cosine_lr(base_lr: float, current_step: int, warmup_steps: int, '
                                       'total_steps: int) -> float:\n'
                                       '    import math\n'
                                       '    if current_step < warmup_steps:\n'
                                       '        return round(base_lr * (current_step / warmup_steps), 6)\n'
                                       '    progress = (current_step - warmup_steps) / (total_steps - warmup_steps)\n'
                                       '    decay = 0.5 * (1.0 + math.cos(math.pi * progress))\n'
                                       '    return round(base_lr * decay, 6)\n',
                      'starter_code': 'def warmup_cosine_lr(base_lr: float, current_step: int, warmup_steps: int, '
                                      'total_steps: int) -> float:\n'
                                      '    # Return current learning rate\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Halfway through warmup = 0.0005',
                                      'expected': 0.0005,
                                      'input': [0.001, 5, 10, 100]},
                                     {'desc': 'At final step lr decays to 0.0',
                                      'expected': 0.0,
                                      'input': [0.001, 100, 10, 100]}],
                      'title': 'Linear Warmup Cosine Decay Learning Rate Scheduler'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'named_params is list of parameter name strings',
                    'difficulty': 'Basic',
                    'explanation': 'Transfer learning parameter freezing: param.requires_grad = False.',
                    'function_name': 'freeze_model_parameters',
                    'hint': '{p: not p.startswith(freeze_prefix) for p in named_params}',
                    'id': 'c3-m4-l1-b',
                    'prompt': 'Write `freeze_model_parameters(named_params, freeze_prefix)` returning dict `{name: '
                              'requires_grad}` where `requires_grad = False` if name starts with freeze_prefix else '
                              '`True`.',
                    'solution_code': 'def freeze_model_parameters(named_params: list, freeze_prefix: str) -> dict:\n'
                                     '    return {p: not p.startswith(freeze_prefix) for p in named_params}\n',
                    'starter_code': 'def freeze_model_parameters(named_params: list, freeze_prefix: str) -> dict:\n'
                                    '    # Return requires_grad mapping\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Freezes backbone, trains classifier',
                                    'expected': {'backbone.bn1.weight': False,
                                                 'backbone.conv1.weight': False,
                                                 'classifier.weight': True},
                                    'input': [['backbone.conv1.weight', 'backbone.bn1.weight', 'classifier.weight'],
                                              'backbone']}],
                    'title': 'Pretrained Model Parameter Freeze'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'embedding is list of numbers',
                           'difficulty': 'Intermediate',
                           'explanation': 'Visual feature embedding normalization for cosine similarity search.',
                           'function_name': 'normalize_feature_embedding',
                           'hint': 'norm = sum(x**2)**0.5; divide and round.',
                           'id': 'c3-m4-l1-i',
                           'prompt': 'Write `normalize_feature_embedding(embedding)` dividing each element by L2 norm '
                                     '`sqrt(sum(x**2))`. Round to 4 decimals. If norm is 0 return embedding.',
                           'solution_code': 'def normalize_feature_embedding(embedding: list) -> list:\n'
                                            '    norm = (sum(x**2 for x in embedding)) ** 0.5\n'
                                            '    if norm == 0: return embedding\n'
                                            '    return [round(x / norm, 4) for x in embedding]\n',
                           'starter_code': 'def normalize_feature_embedding(embedding: list) -> list:\n'
                                           '    # Return unit length embedding\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Norm is 5.0 -> [0.6, 0.8]',
                                           'expected': [0.6, 0.8],
                                           'input': [[3.0, 4.0]]}],
                           'title': 'ResNet Feature Vector L2 Normalization'}},
 (4, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'distance >= 0, margin > 0',
                      'difficulty': 'Advance',
                      'explanation': 'Siamese metric learning loss function for one-shot similarity.',
                      'function_name': 'contrastive_loss',
                      'hint': 'Check is_similar flag, compute respective half-squared term.',
                      'id': 'c3-m4-l2-a',
                      'prompt': 'Write `contrastive_loss(distance, is_similar, margin)`: if is_similar: `0.5 * '
                                'distance^2`. Else: `0.5 * max(0, margin - distance)^2`. Round to 4 decimals.',
                      'solution_code': 'def contrastive_loss(distance: float, is_similar: bool, margin: float) -> '
                                       'float:\n'
                                       '    if is_similar:\n'
                                       '        return round(0.5 * (distance ** 2), 4)\n'
                                       '    return round(0.5 * (max(0.0, margin - distance) ** 2), 4)\n',
                      'starter_code': 'def contrastive_loss(distance: float, is_similar: bool, margin: float) -> '
                                      'float:\n'
                                      '    # Return contrastive loss\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Similar pair 0.5 * 0.16 = 0.08',
                                      'expected': 0.08,
                                      'input': [0.4, True, 1.0]},
                                     {'desc': 'Dissimilar pair 0.5 * (1.0 - 0.4)^2 = 0.5 * 0.36 = 0.18',
                                      'expected': 0.18,
                                      'input': [0.4, False, 1.0]}],
                      'title': 'Contrastive Loss for Siamese Networks'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': '0 < decay_rate <= 1, num_layers >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Discriminative fine-tuning where lower layers train with smaller learning rates.',
                    'function_name': 'apply_layer_lr_multipliers',
                    'hint': 'Compute decay factor based on layer depth.',
                    'id': 'c3-m4-l2-b',
                    'prompt': 'Write `apply_layer_lr_multipliers(base_lr, decay_rate, num_layers)` returning list of '
                              'learning rates where layer `i` has lr = `base_lr * (decay_rate ** (num_layers - 1 - '
                              'i))`. Round to 6 decimals.',
                    'solution_code': 'def apply_layer_lr_multipliers(base_lr: float, decay_rate: float, num_layers: '
                                     'int) -> list:\n'
                                     '    return [round(base_lr * (decay_rate ** (num_layers - 1 - i)), 6) for i in '
                                     'range(num_layers)]\n',
                    'starter_code': 'def apply_layer_lr_multipliers(base_lr: float, decay_rate: float, num_layers: '
                                    'int) -> list:\n'
                                    '    # Return per-layer learning rates\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Layer 0: 0.01*0.25, Layer 1: 0.01*0.5, Layer 2: 0.01*1.0',
                                    'expected': [0.0025, 0.005, 0.01],
                                    'input': [0.01, 0.5, 3]}],
                    'title': 'Discriminative Layer Learning Rate Multiplier'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'all parameters are floats',
                           'difficulty': 'Intermediate',
                           'explanation': 'AdamW decoupled weight decay optimization algorithm.',
                           'function_name': 'apply_weight_decay',
                           'hint': 'weight * (1.0 - lr * weight_decay) - lr * gradient',
                           'id': 'c3-m4-l2-i',
                           'prompt': 'Write `apply_weight_decay(weight, gradient, lr, weight_decay)`: `w_new = weight '
                                     '* (1 - lr * weight_decay) - lr * gradient`. Round to 4 decimals.',
                           'solution_code': 'def apply_weight_decay(weight: float, gradient: float, lr: float, '
                                            'weight_decay: float) -> float:\n'
                                            '    return round(weight * (1.0 - lr * weight_decay) - (lr * gradient), '
                                            '4)\n',
                           'starter_code': 'def apply_weight_decay(weight: float, gradient: float, lr: float, '
                                           'weight_decay: float) -> float:\n'
                                           '    # Return updated weight\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '1.0 * (1 - 0.001) - 0.001 = 0.998',
                                           'expected': 0.998,
                                           'input': [1.0, 0.1, 0.01, 0.1]}],
                           'title': 'L2 Weight Decay Regularization Step'}},
 (5, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'sequence is list of floats',
                      'difficulty': 'Advance',
                      'explanation': 'Unrolling recurrent networks over time (BPTT).',
                      'function_name': 'unroll_rnn_sequence',
                      'hint': 'Loop over sequence, update curr_h and append.',
                      'id': 'c3-m5-l1-a',
                      'prompt': 'Write `unroll_rnn_sequence(sequence, h0, w_x, w_h)`: iteratively computes `h_t = '
                                'max(0.0, x_t * w_x + h_{t-1} * w_h)`. Return list of hidden states `[h_1, ..., h_T]` '
                                'rounded to 2 decimals.',
                      'solution_code': 'def unroll_rnn_sequence(sequence: list, h0: float, w_x: float, w_h: float) -> '
                                       'list:\n'
                                       '    h = h0\n'
                                       '    res = []\n'
                                       '    for x in sequence:\n'
                                       '        h = max(0.0, (x * w_x) + (h * w_h))\n'
                                       '        res.append(round(h, 2))\n'
                                       '    return res\n',
                      'starter_code': 'def unroll_rnn_sequence(sequence: list, h0: float, w_x: float, w_h: float) -> '
                                      'list:\n'
                                      '    # Return trajectory of hidden states\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'h1 = 1*2 = 2.0; h2 = 2*2 + 2*0.5 = 5.0',
                                      'expected': [2.0, 5.0],
                                      'input': [[1.0, 2.0], 0.0, 2.0, 0.5]}],
                      'title': 'Sequence Unroll Hidden Trajectory'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all inputs are floats',
                    'difficulty': 'Basic',
                    'explanation': 'PyTorch nn.RNNCell forward recurrence formula.',
                    'function_name': 'rnn_cell_forward',
                    'hint': 'import math; math.tanh(x_t * w_ih + h_prev * w_hh + bias).',
                    'id': 'c3-m5-l1-b',
                    'prompt': 'Write `rnn_cell_forward(x_t, h_prev, w_ih, w_hh, bias)` computing `tanh(x_t * w_ih + '
                              'h_prev * w_hh + bias)`. Round to 4 decimals with math.tanh.',
                    'solution_code': 'def rnn_cell_forward(x_t: float, h_prev: float, w_ih: float, w_hh: float, bias: '
                                     'float) -> float:\n'
                                     '    import math\n'
                                     '    z = (x_t * w_ih) + (h_prev * w_hh) + bias\n'
                                     '    return round(math.tanh(z), 4)\n',
                    'starter_code': 'def rnn_cell_forward(x_t: float, h_prev: float, w_ih: float, w_hh: float, bias: '
                                    'float) -> float:\n'
                                    '    # Return next hidden state h_t\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '0.2 + 0.2 + 0.1 = 0.5 -> tanh(0.5) = 0.4621',
                                    'expected': 0.4621,
                                    'input': [1.0, 0.5, 0.2, 0.4, 0.1]}],
                    'title': 'RNN Single Hidden State Transition'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'steps >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Mathematical demonstration of the vanishing gradient problem in deep '
                                          'recurrent networks.',
                           'function_name': 'simulate_gradient_decay',
                           'hint': 'Multiply initial_gradient by weight raised to steps.',
                           'id': 'c3-m5-l1-i',
                           'prompt': 'Write `simulate_gradient_decay(initial_gradient, weight, steps)`: '
                                     '`initial_gradient * (weight ** steps)`. Round to 6 decimals.',
                           'solution_code': 'def simulate_gradient_decay(initial_gradient: float, weight: float, '
                                            'steps: int) -> float:\n'
                                            '    return round(initial_gradient * (weight ** steps), 6)\n',
                           'starter_code': 'def simulate_gradient_decay(initial_gradient: float, weight: float, steps: '
                                           'int) -> float:\n'
                                           '    # Return attenuated gradient\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Gradient diminishes exponentially',
                                           'expected': 0.000977,
                                           'input': [1.0, 0.5, 10]}],
                           'title': 'Vanishing Gradient Jacobian Decay'}},
 (5, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(forward_h) == len(backward_h)',
                      'difficulty': 'Advance',
                      'explanation': 'PyTorch BiLSTM bidirectional context aggregation.',
                      'function_name': 'bidirectional_hidden_merge',
                      'hint': '[f + b for f, b in zip(forward_h, backward_h)]',
                      'id': 'c3-m5-l2-a',
                      'prompt': 'Write `bidirectional_hidden_merge(forward_h, backward_h)` concatenating forward and '
                                'backward hidden vectors at each timestep: `[f + b for f, b in zip(forward_h, '
                                'backward_h)]`.',
                      'solution_code': 'def bidirectional_hidden_merge(forward_h: list, backward_h: list) -> list:\n'
                                       '    return [f + b for f, b in zip(forward_h, backward_h)]\n',
                      'starter_code': 'def bidirectional_hidden_merge(forward_h: list, backward_h: list) -> list:\n'
                                      '    # Return merged sequence\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Concatenates forward and reverse states',
                                      'expected': [[1, 2, 5, 6], [3, 4, 7, 8]],
                                      'input': [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]}],
                      'title': 'Bidirectional Hidden State Concatenation'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all inputs are floats',
                    'difficulty': 'Basic',
                    'explanation': 'LSTM forget gate f_t deciding information retention.',
                    'function_name': 'lstm_forget_gate',
                    'hint': 'import math; sigmoid formula.',
                    'id': 'c3-m5-l2-b',
                    'prompt': 'Write `lstm_forget_gate(x, h_prev, w_x, w_h, bias)`: `1 / (1 + exp(-(x*w_x + h*w_h + '
                              'bias)))`. Round to 4 decimals.',
                    'solution_code': 'def lstm_forget_gate(x: float, h_prev: float, w_x: float, w_h: float, bias: '
                                     'float) -> float:\n'
                                     '    import math\n'
                                     '    z = (x * w_x) + (h_prev * w_h) + bias\n'
                                     '    return round(1.0 / (1.0 + math.exp(-z)), 4)\n',
                    'starter_code': 'def lstm_forget_gate(x: float, h_prev: float, w_x: float, w_h: float, bias: '
                                    'float) -> float:\n'
                                    '    # Return forget gate value in (0, 1)\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Sigmoid(0) = 0.5', 'expected': 0.5, 'input': [0.0, 0.0, 1.0, 1.0, 0.0]}],
                    'title': 'LSTM Forget Gate Activation'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'f_t, i_t in [0, 1]',
                           'difficulty': 'Intermediate',
                           'explanation': 'Additive constant error carousel solving vanishing gradients in LSTMs.',
                           'function_name': 'lstm_cell_state_update',
                           'hint': '(f_t * c_prev) + (i_t * c_tilde)',
                           'id': 'c3-m5-l2-i',
                           'prompt': 'Write `lstm_cell_state_update(c_prev, f_t, i_t, c_tilde)`: `c_t = (f_t * c_prev) '
                                     '+ (i_t * c_tilde)`. Round to 4 decimals.',
                           'solution_code': 'def lstm_cell_state_update(c_prev: float, f_t: float, i_t: float, '
                                            'c_tilde: float) -> float:\n'
                                            '    return round((f_t * c_prev) + (i_t * c_tilde), 4)\n',
                           'starter_code': 'def lstm_cell_state_update(c_prev: float, f_t: float, i_t: float, c_tilde: '
                                           'float) -> float:\n'
                                           '    # Return new cell state c_t\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '0.9*2 + 0.5*1 = 1.8 + 0.5 = 2.3',
                                           'expected': 2.3,
                                           'input': [2.0, 0.9, 0.5, 1.0]}],
                           'title': 'LSTM Cell State Additive Update'}},
 (6, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'attention_matrix is square 2D list',
                      'difficulty': 'Advance',
                      'explanation': 'Autoregressive decoder masking ensuring tokens cannot attend to subsequent '
                                     'positions.',
                      'function_name': 'apply_causal_mask',
                      'hint': 'Iterate i and j, replace if j > i.',
                      'id': 'c3-m6-l1-a',
                      'prompt': 'Write `apply_causal_mask(attention_matrix, mask_value)`: set `attention_matrix[i][j] '
                                '= mask_value` for all `j > i` (future tokens).',
                      'solution_code': 'def apply_causal_mask(attention_matrix: list, mask_value: float) -> list:\n'
                                       '    n = len(attention_matrix)\n'
                                       '    return [[attention_matrix[i][j] if j <= i else mask_value for j in '
                                       'range(n)] for i in range(n)]\n',
                      'starter_code': 'def apply_causal_mask(attention_matrix: list, mask_value: float) -> list:\n'
                                      '    # Return causally masked matrix\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Top right element masked to -1e9',
                                      'expected': [[1.0, -1000000000.0], [3.0, 4.0]],
                                      'input': [[[1.0, 2.0], [3.0, 4.0]], -1000000000.0]}],
                      'title': 'Causal Lower-Triangular Attention Mask'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(query) == len(key) == d_k >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Scaled dot product prevents vanishing gradients in large embedding dimensions.',
                    'function_name': 'scaled_dot_attention_score',
                    'hint': 'sum(q * k for q, k in zip(query, key)) / (d_k ** 0.5)',
                    'id': 'c3-m6-l1-b',
                    'prompt': 'Write `scaled_dot_attention_score(query, key, d_k)`: `dot(query, key) / sqrt(d_k)`. '
                              'Round to 4 decimals.',
                    'solution_code': 'def scaled_dot_attention_score(query: list, key: list, d_k: int) -> float:\n'
                                     '    dot = sum(q * k for q, k in zip(query, key))\n'
                                     '    return round(dot / (d_k ** 0.5), 4)\n',
                    'starter_code': 'def scaled_dot_attention_score(query: list, key: list, d_k: int) -> float:\n'
                                    '    # Return scaled attention score\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'dot = 4.0, / sqrt(2) = 2.8284',
                                    'expected': 2.8284,
                                    'input': [[1.0, 2.0], [2.0, 1.0], 2]}],
                    'title': 'Scaled Dot-Product Attention Score'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'scores_vector is non-empty list of floats',
                           'difficulty': 'Intermediate',
                           'explanation': 'Self-attention weight distribution over value tokens.',
                           'function_name': 'attention_softmax_weights',
                           'hint': 'import math; exp(s - max(s)) / sum.',
                           'id': 'c3-m6-l1-i',
                           'prompt': 'Write `attention_softmax_weights(scores_vector)` computing softmax over score '
                                     'vector. Round to 4 decimals.',
                           'solution_code': 'def attention_softmax_weights(scores_vector: list) -> list:\n'
                                            '    import math\n'
                                            '    mx = max(scores_vector)\n'
                                            '    exps = [math.exp(s - mx) for s in scores_vector]\n'
                                            '    tot = sum(exps)\n'
                                            '    return [round(e / tot, 4) for e in exps]\n',
                           'starter_code': 'def attention_softmax_weights(scores_vector: list) -> list:\n'
                                           '    # Return attention distribution\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Equal scores yield equal 0.5 attention',
                                           'expected': [0.5, 0.5],
                                           'input': [[0.0, 0.0]]}],
                           'title': 'Attention Weight Softmax Normalization'}},
 (6, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all heads have same row count and width',
                      'difficulty': 'Advance',
                      'explanation': 'Multi-head attention final linear projection input preparation.',
                      'function_name': 'concat_multihead_outputs',
                      'hint': 'For each row r: [x for head in head_outputs for x in head[r]].',
                      'id': 'c3-m6-l2-a',
                      'prompt': 'Write `concat_multihead_outputs(head_outputs)` where head_outputs is list of `h` head '
                                'matrices each of size `N x d_k`. Concatenate heads horizontally to return `N x (h * '
                                'd_k)`.',
                      'solution_code': 'def concat_multihead_outputs(head_outputs: list) -> list:\n'
                                       '    N = len(head_outputs[0])\n'
                                       '    return [[x for head in head_outputs for x in head[r]] for r in range(N)]\n',
                      'starter_code': 'def concat_multihead_outputs(head_outputs: list) -> list:\n'
                                      '    # Return concatenated multi-head tensor\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Combines two 2x2 heads into 2x4',
                                      'expected': [[1, 2, 5, 6], [3, 4, 7, 8]],
                                      'input': [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]]}],
                      'title': 'Concatenate Multi-Head Attention Outputs'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'd_model >= 1, num_heads >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'Multi-head attention projection dimensionality constraint.',
                    'function_name': 'split_heads_dimension',
                    'hint': 'Check modulo and return integer division.',
                    'id': 'c3-m6-l2-b',
                    'prompt': 'Write `split_heads_dimension(d_model, num_heads)`: check `d_model % num_heads == 0`. If '
                              'yes, return `d_model // num_heads`, else return -1.',
                    'solution_code': 'def split_heads_dimension(d_model: int, num_heads: int) -> int:\n'
                                     '    return d_model // num_heads if d_model % num_heads == 0 else -1\n',
                    'starter_code': 'def split_heads_dimension(d_model: int, num_heads: int) -> int:\n'
                                    '    # Return head dimension d_k or -1\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '512 / 8 = 64', 'expected': 64, 'input': [512, 8]},
                                   {'desc': 'Not divisible -> -1', 'expected': -1, 'input': [512, 7]}],
                    'title': 'Multi-Head Projection Split'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'd_model >= 2',
                           'difficulty': 'Intermediate',
                           'explanation': 'Vaswani et al. Attention Is All You Need static positional embeddings.',
                           'function_name': 'sinusoidal_positional_encoding',
                           'hint': 'import math; calculate frequency divider.',
                           'id': 'c3-m6-l2-i',
                           'prompt': 'Write `sinusoidal_positional_encoding(pos, i, d_model)`: if i % 2 == 0: `sin(pos '
                                     '/ (10000^(2*i / d_model)))`. Else: `cos(pos / (10000^(2*(i-1) / d_model)))`. '
                                     'Round to 4 decimals.',
                           'solution_code': 'def sinusoidal_positional_encoding(pos: int, i: int, d_model: int) -> '
                                            'float:\n'
                                            '    import math\n'
                                            '    idx = i if i % 2 == 0 else i - 1\n'
                                            '    freq = 10000.0 ** (idx / d_model)\n'
                                            '    angle = pos / freq\n'
                                            '    val = math.sin(angle) if i % 2 == 0 else math.cos(angle)\n'
                                            '    return round(val, 4)\n',
                           'starter_code': 'def sinusoidal_positional_encoding(pos: int, i: int, d_model: int) -> '
                                           'float:\n'
                                           '    # Return positional encoding value\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'sin(0) = 0.0', 'expected': 0.0, 'input': [0, 0, 512]},
                                          {'desc': 'cos(0) = 1.0', 'expected': 1.0, 'input': [0, 1, 512]}],
                           'title': 'Sinusoidal Positional Encoding (Single Dimension)'}}}
