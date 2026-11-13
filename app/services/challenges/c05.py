"""Course 5 topic-specific programming challenges."""

CHALLENGES = {(1, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'multiplier is float',
                      'difficulty': 'Advance',
                      'explanation': 'ES6 Rest parameters `...args`.',
                      'function_name': 'multiply_rest_params',
                      'hint': 'Use *values to gather arguments into a tuple.',
                      'id': 'c5-m1-l1-a',
                      'prompt': 'Write `multiply_rest_params(multiplier, *values)` multiplying each element in values '
                                'by multiplier. Return list of rounded floats (2 decimals).',
                      'solution_code': 'def multiply_rest_params(multiplier: float, *values) -> list:\n'
                                       '    return [round(float(v * multiplier), 2) for v in values]\n',
                      'starter_code': 'def multiply_rest_params(multiplier: float, *values) -> list:\n'
                                      '    # Return scaled values\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Scales 10 and 20 by 1.5',
                                      'expected': [15.0, 30.0],
                                      'input': [1.5, 10, 20]}],
                      'title': 'Rest Parameter Variable Multiplier'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'numbers is list of integers',
                    'difficulty': 'Basic',
                    'explanation': 'ES6 Array.prototype.filter and map equivalent.',
                    'function_name': 'filter_even_squares',
                    'hint': 'List comprehension with modulo filter.',
                    'id': 'c5-m1-l1-b',
                    'prompt': 'Write `filter_even_squares(numbers)` returning `[x**2 for x in numbers if x % 2 == 0]`.',
                    'solution_code': 'def filter_even_squares(numbers: list) -> list:\n'
                                     '    return [x**2 for x in numbers if x % 2 == 0]\n',
                    'starter_code': 'def filter_even_squares(numbers: list) -> list:\n'
                                    '    # Return squares of even numbers\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '2^2=4, 4^2=16', 'expected': [4, 16], 'input': [[1, 2, 3, 4]]}],
                    'title': 'Even Square Numbers Filter (ES6 Arrow Functions)'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'user_payload is dict',
                           'difficulty': 'Intermediate',
                           'explanation': 'JavaScript ES6 object destructuring and default values.',
                           'function_name': 'normalize_user_keys',
                           'hint': 'Extract keys and lower email.',
                           'id': 'c5-m1-l1-i',
                           'prompt': 'Write `normalize_user_keys(user_payload)` extracting `first_name` and '
                                     '`last_name` and returning `{"full_name": f"{first_name} {last_name}".strip(), '
                                     '"email": user_payload.get("email", "").lower()}`.',
                           'solution_code': 'def normalize_user_keys(user_payload: dict) -> dict:\n'
                                            '    fn = user_payload.get("first_name", "")\n'
                                            '    ln = user_payload.get("last_name", "")\n'
                                            '    return {"full_name": f"{fn} {ln}".strip(), "email": '
                                            'user_payload.get("email", "").lower()}\n',
                           'starter_code': 'def normalize_user_keys(user_payload: dict) -> dict:\n'
                                           '    # Return normalized user dict\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Combines name, lowers email',
                                           'expected': {'email': 'john@example.com', 'full_name': 'John Doe'},
                                           'input': [{'email': 'JOHN@Example.com',
                                                      'first_name': 'John',
                                                      'last_name': 'Doe'}]}],
                           'title': 'Destructured Object Key Normalizer'}},
 (1, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'var_name is string',
                      'difficulty': 'Advance',
                      'explanation': 'JavaScript execution context lexical environment scope chain traversal.',
                      'function_name': 'resolve_variable_in_scope_chain',
                      'hint': 'Iterate through scopes in order, return as soon as var_name in scope.',
                      'id': 'c5-m1-l2-a',
                      'prompt': 'Write `resolve_variable_in_scope_chain(var_name, scope_chain)` where scope_chain is '
                                'list of scope dicts from innermost to outermost. Return value from first scope '
                                'containing var_name, or None if not found.',
                      'solution_code': 'def resolve_variable_in_scope_chain(var_name: str, scope_chain: list):\n'
                                       '    for s in scope_chain:\n'
                                       '        if var_name in s:\n'
                                       '            return s[var_name]\n'
                                       '    return None\n',
                      'starter_code': 'def resolve_variable_in_scope_chain(var_name: str, scope_chain: list):\n'
                                      '    # Return resolved value\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Shadowed outer x=20, returns 10',
                                      'expected': 10,
                                      'input': ['x', [{'y': 2}, {'x': 10}, {'x': 20}]]}],
                      'title': 'Execution Context Scope Chain Resolver'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'operations in ["inc", "dec", "reset"]',
                    'difficulty': 'Basic',
                    'explanation': 'Closure lexical scope encapsulating private state.',
                    'function_name': 'simulate_counter_sequence',
                    'hint': 'Track c = 0, modify based on operation.',
                    'id': 'c5-m1-l2-b',
                    'prompt': 'Write `simulate_counter_sequence(operations)` where operations is list of strings '
                              '("inc", "dec", "reset"). Start at 0. Return final integer value.',
                    'solution_code': 'def simulate_counter_sequence(operations: list) -> int:\n'
                                     '    c = 0\n'
                                     '    for op in operations:\n'
                                     '        if op == "inc": c += 1\n'
                                     '        elif op == "dec": c -= 1\n'
                                     '        elif op == "reset": c = 0\n'
                                     '    return c\n',
                    'starter_code': 'def simulate_counter_sequence(operations: list) -> int:\n'
                                    '    # Return final counter value\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '1 + 1 - 1 + 1 = 2',
                                    'expected': 2,
                                    'input': [['inc', 'inc', 'dec', 'inc']]},
                                   {'desc': 'Reset to 0', 'expected': 1, 'input': [['inc', 'reset', 'inc']]}],
                    'title': 'Stateful Counter Simulation'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'a, b, c are numbers',
                           'difficulty': 'Intermediate',
                           'explanation': 'Currying functional transformation `f(a)(b)(c)`.',
                           'function_name': 'curried_add_three',
                           'hint': 'Return float(a + b + c)',
                           'id': 'c5-m1-l2-i',
                           'prompt': 'Write `curried_add_three(a, b, c)` returning sum `a + b + c`.',
                           'solution_code': 'def curried_add_three(a: float, b: float, c: float) -> float:\n'
                                            '    return float(a + b + c)\n',
                           'starter_code': 'def curried_add_three(a: float, b: float, c: float) -> float:\n'
                                           '    # Return sum\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '1+2+3=6', 'expected': 6.0, 'input': [1, 2, 3]}],
                           'title': 'Curried Binary Function Evaluator'}},
 (2, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'raw_text is string',
                      'difficulty': 'Advance',
                      'explanation': 'DOM-based XSS prevention encoding.',
                      'function_name': 'sanitize_html_string',
                      'hint': 'Replace & first, then others.',
                      'id': 'c5-m2-l1-a',
                      'prompt': 'Write `sanitize_html_string(raw_text)` replacing `&` with `&amp;`, `<` with `&lt;`, '
                                '`>` with `&gt;`, `"` with `&quot;`, and `\'` with `&#x27;`.',
                      'solution_code': 'def sanitize_html_string(raw_text: str) -> str:\n'
                                       '    return raw_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", '
                                       '"&gt;").replace(\'"\', "&quot;").replace("\'", "&#x27;")\n',
                      'starter_code': 'def sanitize_html_string(raw_text: str) -> str:\n'
                                      '    # Return sanitized HTML\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Escapes dangerous HTML',
                                      'expected': '&lt;script&gt;alert(&quot;hi&quot;)&lt;/script&gt;',
                                      'input': ['<script>alert("hi")</script>']}],
                      'title': 'User Input HTML Entity Sanitizer'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all strings non-empty',
                    'difficulty': 'Basic',
                    'explanation': 'DOM element creation and innerHTML serialization.',
                    'function_name': 'build_html_tag_string',
                    'hint': 'f"<{tag} class=\\"{class_name}\\">{content}</{tag}>"',
                    'id': 'c5-m2-l1-b',
                    'prompt': 'Write `build_html_tag_string(tag, content, class_name)`: `<{tag} '
                              'class="{class_name}">{content}</{tag}>`.',
                    'solution_code': 'def build_html_tag_string(tag: str, content: str, class_name: str) -> str:\n'
                                     '    return f"<{tag} class=\\"{class_name}\\">{content}</{tag}>"\n',
                    'starter_code': 'def build_html_tag_string(tag: str, content: str, class_name: str) -> str:\n'
                                    '    # Return HTML string\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Builds tag with class',
                                    'expected': '<div class="card">Hello</div>',
                                    'input': ['div', 'Hello', 'card']}],
                    'title': 'HTML Tag String Builder'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'node is valid tree dict',
                           'difficulty': 'Intermediate',
                           'explanation': 'DOM tree recursive traversal.',
                           'function_name': 'dom_max_depth',
                           'hint': '1 + max([dom_max_depth(c) for c in node["children"]], default=0)',
                           'id': 'c5-m2-l1-i',
                           'prompt': 'Write `dom_max_depth(node)` where node is dict `{"tag": str, "children": '
                                     '[nodes]}`. Leaf with empty children has depth 1. Return max depth.',
                           'solution_code': 'def dom_max_depth(node: dict) -> int:\n'
                                            '    if not node.get("children"):\n'
                                            '        return 1\n'
                                            '    return 1 + max(dom_max_depth(c) for c in node["children"])\n',
                           'starter_code': 'def dom_max_depth(node: dict) -> int:\n    # Return max depth\n    pass\n',
                           'test_cases': [{'desc': 'div -> p has depth 2',
                                           'expected': 2,
                                           'input': [{'children': [{'children': [], 'tag': 'p'}], 'tag': 'div'}]}],
                           'title': 'DOM Tree Max Depth Calculator'}},
 (2, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'call_timestamps is sorted list of ints, delay_ms >= 1',
                      'difficulty': 'Advance',
                      'explanation': 'Client-side debounce utility preventing search-bar UI hammering.',
                      'function_name': 'simulate_debounce_triggers',
                      'hint': 'Track pending timer, clear and reset on each call, push when time gap > delay.',
                      'id': 'c5-m2-l2-a',
                      'prompt': 'Write `simulate_debounce_triggers(call_timestamps, delay_ms)` returning list of '
                                'timestamps where the debounced function actually fires (fires at call_time + delay_ms '
                                'if no subsequent call within delay_ms).',
                      'solution_code': 'def simulate_debounce_triggers(call_timestamps: list, delay_ms: int) -> list:\n'
                                       '    if not call_timestamps: return []\n'
                                       '    fires = []\n'
                                       '    for i in range(len(call_timestamps)):\n'
                                       '        curr = call_timestamps[i]\n'
                                       '        if i == len(call_timestamps) - 1 or call_timestamps[i+1] > curr + '
                                       'delay_ms:\n'
                                       '            fires.append(curr + delay_ms)\n'
                                       '    return fires\n',
                      'starter_code': 'def simulate_debounce_triggers(call_timestamps: list, delay_ms: int) -> list:\n'
                                      '    # Return firing timestamps\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '100 cancelled by 150 (fires at 250); 300 fires at 400; 500 fires at 600',
                                      'expected': [250, 400, 600],
                                      'input': [[100, 150, 300, 500], 100]}],
                      'title': 'Debounce Event Trigger Timeline'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'required_selector is string',
                    'difficulty': 'Basic',
                    'explanation': 'Event delegation `event.target.matches(".btn")`.',
                    'function_name': 'is_delegated_target_match',
                    'hint': 'required_selector in target_class_list',
                    'id': 'c5-m2-l2-b',
                    'prompt': 'Write `is_delegated_target_match(target_class_list, required_selector)` checking if '
                              'required_selector is present in target_class_list.',
                    'solution_code': 'def is_delegated_target_match(target_class_list: list, required_selector: str) '
                                     '-> bool:\n'
                                     '    return required_selector in target_class_list\n',
                    'starter_code': 'def is_delegated_target_match(target_class_list: list, required_selector: str) -> '
                                    'bool:\n'
                                    '    # Return True if target matches\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Matches class',
                                    'expected': True,
                                    'input': [['btn', 'btn-primary'], 'btn-primary']}],
                    'title': 'Event Delegation Selector Match'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'parent_map is acyclic',
                           'difficulty': 'Intermediate',
                           'explanation': 'Browser event bubbling propagation path up the DOM hierarchy.',
                           'function_name': 'bubble_event_path',
                           'hint': 'While curr in parent_map, append parent and advance.',
                           'id': 'c5-m2-l2-i',
                           'prompt': 'Write `bubble_event_path(node_id, parent_map)` starting at node_id, walking up '
                                     'parent_map `{child: parent}` until node has no parent. Return list of visited '
                                     'node_ids in order.',
                           'solution_code': 'def bubble_event_path(node_id: str, parent_map: dict) -> list:\n'
                                            '    path = [node_id]\n'
                                            '    curr = node_id\n'
                                            '    while curr in parent_map:\n'
                                            '        curr = parent_map[curr]\n'
                                            '        path.append(curr)\n'
                                            '    return path\n',
                           'starter_code': 'def bubble_event_path(node_id: str, parent_map: dict) -> list:\n'
                                           '    # Return bubbling path\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Bubbles from button to document',
                                           'expected': ['button', 'card', 'body', 'document'],
                                           'input': ['button',
                                                     {'body': 'document', 'button': 'card', 'card': 'body'}]}],
                           'title': 'DOM Event Propagation Path Bubbler'}},
 (3, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all inputs are lists of strings',
                      'difficulty': 'Advance',
                      'explanation': 'JavaScript V8 event loop microtask vs macrotask execution order.',
                      'function_name': 'event_loop_drain_order',
                      'hint': 'sync_tasks + microtasks + macrotasks',
                      'id': 'c5-m3-l1-a',
                      'prompt': 'Write `event_loop_drain_order(sync_tasks, microtasks, macrotasks)` returning list of '
                                'tasks in order: all sync_tasks first, then all microtasks (Promises), then macrotasks '
                                '(setTimeout).',
                      'solution_code': 'def event_loop_drain_order(sync_tasks: list, microtasks: list, macrotasks: '
                                       'list) -> list:\n'
                                       '    return list(sync_tasks) + list(microtasks) + list(macrotasks)\n',
                      'starter_code': 'def event_loop_drain_order(sync_tasks: list, microtasks: list, macrotasks: '
                                      'list) -> list:\n'
                                      '    # Return execution order\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Sync then Micro then Macro',
                                      'expected': ['s1', 'p1', 'p2', 't1'],
                                      'input': [['s1'], ['p1', 'p2'], ['t1']]}],
                      'title': 'Event Loop Task Priority Queue'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'is_successful is bool',
                    'difficulty': 'Basic',
                    'explanation': 'ES6 Promise settled state modeling.',
                    'function_name': 'simulate_promise_state',
                    'hint': 'Check is_successful and return dict.',
                    'id': 'c5-m3-l1-b',
                    'prompt': 'Write `simulate_promise_state(is_successful, value_or_error)` returning `{"status": '
                              '"fulfilled", "value": value_or_error}` if successful else `{"status": "rejected", '
                              '"reason": value_or_error}`.',
                    'solution_code': 'def simulate_promise_state(is_successful: bool, value_or_error) -> dict:\n'
                                     '    if is_successful:\n'
                                     '        return {"status": "fulfilled", "value": value_or_error}\n'
                                     '    return {"status": "rejected", "reason": value_or_error}\n',
                    'starter_code': 'def simulate_promise_state(is_successful: bool, value_or_error) -> dict:\n'
                                    '    # Return promise state\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Fulfilled promise',
                                    'expected': {'status': 'fulfilled', 'value': 'data'},
                                    'input': [True, 'data']},
                                   {'desc': 'Rejected promise',
                                    'expected': {'reason': 'Network error', 'status': 'rejected'},
                                    'input': [False, 'Network error']}],
                    'title': 'Promise State Simulator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'promise_results is non-empty list',
                           'difficulty': 'Intermediate',
                           'explanation': 'Promise.all fail-fast concurrency semantics.',
                           'function_name': 'promise_all_settle',
                           'hint': 'Check for first rejected, else gather all data.',
                           'id': 'c5-m3-l1-i',
                           'prompt': 'Write `promise_all_settle(promise_results)` where each item is `{"status": '
                                     '"fulfilled"/"rejected", "data": ...}`. If any rejected, return `{"status": '
                                     '"rejected", "error": first_rejected_data}`. Else return `{"status": "fulfilled", '
                                     '"results": [data1, data2...]}`.',
                           'solution_code': 'def promise_all_settle(promise_results: list) -> dict:\n'
                                            '    results = []\n'
                                            '    for p in promise_results:\n'
                                            '        if p["status"] == "rejected":\n'
                                            '            return {"status": "rejected", "error": p["data"]}\n'
                                            '        results.append(p["data"])\n'
                                            '    return {"status": "fulfilled", "results": results}\n',
                           'starter_code': 'def promise_all_settle(promise_results: list) -> dict:\n'
                                           '    # Return Promise.all outcome\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'All fulfilled',
                                           'expected': {'results': [1, 2], 'status': 'fulfilled'},
                                           'input': [[{'data': 1, 'status': 'fulfilled'},
                                                      {'data': 2, 'status': 'fulfilled'}]]}],
                           'title': 'Promise.all Settlement Gate'}},
 (3, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'base_delay > 0, max_retries >= 1, backoff_factor >= 1',
                      'difficulty': 'Advance',
                      'explanation': 'Resilient network fetch retry intervals.',
                      'function_name': 'calculate_retry_delays',
                      'hint': 'Multiply base_delay by backoff_factor raised to power i.',
                      'id': 'c5-m3-l2-a',
                      'prompt': 'Write `calculate_retry_delays(base_delay, max_retries, backoff_factor)`: `[base_delay '
                                '* (backoff_factor ** i) for i in range(max_retries)]`. Round to 2 decimals.',
                      'solution_code': 'def calculate_retry_delays(base_delay: float, max_retries: int, '
                                       'backoff_factor: float) -> list:\n'
                                       '    return [round(base_delay * (backoff_factor ** i), 2) for i in '
                                       'range(max_retries)]\n',
                      'starter_code': 'def calculate_retry_delays(base_delay: float, max_retries: int, backoff_factor: '
                                      'float) -> list:\n'
                                      '    # Return list of delay values\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Doubling delays: 100, 200, 400',
                                      'expected': [100.0, 200.0, 400.0],
                                      'input': [100.0, 3, 2.0]}],
                      'title': 'Exponential Backoff Request Retrier'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'params is dict',
                    'difficulty': 'Basic',
                    'explanation': 'URLSearchParams query string serialization.',
                    'function_name': 'build_query_string',
                    'hint': 'If not params return "". Sort keys, format k=v, join with &.',
                    'id': 'c5-m3-l2-b',
                    'prompt': 'Write `build_query_string(params)` returning `"?" + "&".join(f"{k}={v}" for k in '
                              'sorted(params))` or `""` if params is empty.',
                    'solution_code': 'def build_query_string(params: dict) -> str:\n'
                                     '    if not params: return ""\n'
                                     '    return "?" + "&".join(f"{k}={params[k]}" for k in sorted(params.keys()))\n',
                    'starter_code': 'def build_query_string(params: dict) -> str:\n'
                                    '    # Return query string\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Sorts keys and formats',
                                    'expected': '?page=1&q=search',
                                    'input': [{'page': 1, 'q': 'search'}]}],
                    'title': 'API Query Parameter String Builder'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'json_str is string',
                           'difficulty': 'Intermediate',
                           'explanation': 'Defensive client-side response parsing.',
                           'function_name': 'safe_json_parse',
                           'hint': 'import json; try json.loads, except Exception return fallback.',
                           'id': 'c5-m3-l2-i',
                           'prompt': 'Write `safe_json_parse(json_str, fallback)` parsing json_str with json.loads. '
                                     'Return fallback on ValueError or TypeError.',
                           'solution_code': 'def safe_json_parse(json_str: str, fallback):\n'
                                            '    import json\n'
                                            '    try: return json.loads(json_str)\n'
                                            '    except Exception: return fallback\n',
                           'starter_code': 'def safe_json_parse(json_str: str, fallback):\n'
                                           '    # Return parsed object or fallback\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Parses valid JSON',
                                           'expected': {'a': 1},
                                           'input': ['{"a": 1}', {}]},
                                          {'desc': 'Returns fallback', 'expected': [], 'input': ['invalid json', []]}],
                           'title': 'Safe JSON Parse with Fallback'}},
 (4, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'fields is list of dicts',
                      'difficulty': 'Advance',
                      'explanation': 'HTML5 new FormData() serialization semantics.',
                      'function_name': 'serialize_form_data',
                      'hint': 'Track occurrences, convert single value to list if seen multiple times.',
                      'id': 'c5-m4-l1-a',
                      'prompt': 'Write `serialize_form_data(fields)` where fields is list of `{"name": str, "value": '
                                'str}`. Return dict `{name: value}`. If duplicate names exist, value becomes list of '
                                'values.',
                      'solution_code': 'def serialize_form_data(fields: list) -> dict:\n'
                                       '    res = {}\n'
                                       '    for f in fields:\n'
                                       '        k, v = f["name"], f["value"]\n'
                                       '        if k not in res:\n'
                                       '            res[k] = v\n'
                                       '        elif isinstance(res[k], list):\n'
                                       '            res[k].append(v)\n'
                                       '        else:\n'
                                       '            res[k] = [res[k], v]\n'
                                       '    return res\n',
                      'starter_code': 'def serialize_form_data(fields: list) -> dict:\n'
                                      '    # Return serialized form data\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Multi-value field becomes list',
                                      'expected': {'tags': ['js', 'web'], 'user': 'zee'},
                                      'input': [[{'name': 'tags', 'value': 'js'},
                                                 {'name': 'tags', 'value': 'web'},
                                                 {'name': 'user', 'value': 'zee'}]]}],
                      'title': 'HTML5 FormData Serializer'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'email is string',
                    'difficulty': 'Basic',
                    'explanation': 'HTML5 email input client-side constraint validation.',
                    'function_name': 'is_valid_email_format',
                    'hint': 'Split by @, check 2 parts, check dot in domain.',
                    'id': 'c5-m4-l1-b',
                    'prompt': 'Write `is_valid_email_format(email)` checking if email has exactly one "@", non-empty '
                              'local part before "@", and domain after "@" containing at least one "." with characters '
                              'on both sides.',
                    'solution_code': 'def is_valid_email_format(email: str) -> bool:\n'
                                     '    if "@" not in email or email.count("@") != 1: return False\n'
                                     '    local, domain = email.split("@")\n'
                                     '    if not local or "." not in domain: return False\n'
                                     '    d_parts = domain.split(".")\n'
                                     '    return all(len(p) > 0 for p in d_parts)\n',
                    'starter_code': 'def is_valid_email_format(email: str) -> bool:\n'
                                    '    # Return True if valid email format\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Valid email', 'expected': True, 'input': ['user@example.com']},
                                   {'desc': 'Missing dot in domain', 'expected': False, 'input': ['user@com']}],
                    'title': 'Email Format Validator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'password is string',
                           'difficulty': 'Intermediate',
                           'explanation': 'Client-side authentication password policy validation.',
                           'function_name': 'check_password_strength',
                           'hint': 'Check len >= 8, any(c.isdigit()), any(c.isupper()), any(c.islower()).',
                           'id': 'c5-m4-l1-i',
                           'prompt': 'Write `check_password_strength(password)` returning dict `{"is_valid": bool, '
                                     '"missing": [missing_rules]}` where rules are "min_8_chars", "has_digit", '
                                     '"has_upper", "has_lower".',
                           'solution_code': 'def check_password_strength(password: str) -> dict:\n'
                                            '    missing = []\n'
                                            '    if len(password) < 8: missing.append("min_8_chars")\n'
                                            '    if not any(c.isdigit() for c in password): '
                                            'missing.append("has_digit")\n'
                                            '    if not any(c.isupper() for c in password): '
                                            'missing.append("has_upper")\n'
                                            '    if not any(c.islower() for c in password): '
                                            'missing.append("has_lower")\n'
                                            '    return {"is_valid": len(missing) == 0, "missing": missing}\n',
                           'starter_code': 'def check_password_strength(password: str) -> dict:\n'
                                           '    # Return password rules report\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Meets all rules',
                                           'expected': {'is_valid': True, 'missing': []},
                                           'input': ['Secret123']}],
                           'title': 'Password Complexity Rules Checker'}},
 (4, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'len(item_widths) >= 2',
                      'difficulty': 'Advance',
                      'explanation': 'Browser flexbox layout engine space-between distribution algorithm.',
                      'function_name': 'calculate_flex_offsets',
                      'hint': 'Calculate gap, advance current_x by item_width + gap.',
                      'id': 'c5-m4-l2-a',
                      'prompt': 'Write `calculate_flex_offsets(container_width, item_widths)`: computes start X '
                                'positions of items under `justify-content: space-between`. Gap = `(container_width - '
                                'sum(item_widths)) / (len(item_widths) - 1)`. Round to 2 decimals.',
                      'solution_code': 'def calculate_flex_offsets(container_width: float, item_widths: list) -> '
                                       'list:\n'
                                       '    gap = (container_width - sum(item_widths)) / (len(item_widths) - 1)\n'
                                       '    res = []\n'
                                       '    curr = 0.0\n'
                                       '    for w in item_widths:\n'
                                       '        res.append(round(curr, 2))\n'
                                       '        curr += w + gap\n'
                                       '    return res\n',
                      'starter_code': 'def calculate_flex_offsets(container_width: float, item_widths: list) -> list:\n'
                                      '    # Return list of start positions\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Total gap 200 split over 2 intervals = 100 gap',
                                      'expected': [0.0, 200.0, 400.0],
                                      'input': [500.0, [100.0, 100.0, 100.0]]}],
                      'title': 'Flexbox Space-Between Offset Calculator'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all dimensions >= 0',
                    'difficulty': 'Basic',
                    'explanation': 'Standard CSS box model dimensional calculation.',
                    'function_name': 'calculate_box_model_width',
                    'hint': 'Sum content with double padding, border, and margin.',
                    'id': 'c5-m4-l2-b',
                    'prompt': 'Write `calculate_box_model_width(content_w, padding_w, border_w, margin_w)`: `content_w '
                              '+ 2*padding_w + 2*border_w + 2*margin_w`.',
                    'solution_code': 'def calculate_box_model_width(content_w: float, padding_w: float, border_w: '
                                     'float, margin_w: float) -> float:\n'
                                     '    return float(content_w + 2 * padding_w + 2 * border_w + 2 * margin_w)\n',
                    'starter_code': 'def calculate_box_model_width(content_w: float, padding_w: float, border_w: '
                                    'float, margin_w: float) -> float:\n'
                                    '    # Return total outer box width\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '100 + 20 + 4 + 10 = 134',
                                    'expected': 134.0,
                                    'input': [100.0, 10.0, 2.0, 5.0]}],
                    'title': 'CSS Box Model Total Width'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'viewport_width > 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'CSS media queries and responsive design grid systems.',
                           'function_name': 'classify_viewport_breakpoint',
                           'hint': 'Compare width against standard Bootstrap responsive breakpoints.',
                           'id': 'c5-m4-l2-i',
                           'prompt': 'Write `classify_viewport_breakpoint(viewport_width)`: returns "xs" (< 576), "sm" '
                                     '(576 to < 768), "md" (768 to < 992), "lg" (992 to < 1200), or "xl" (>= 1200).',
                           'solution_code': 'def classify_viewport_breakpoint(viewport_width: int) -> str:\n'
                                            '    if viewport_width < 576: return "xs"\n'
                                            '    elif viewport_width < 768: return "sm"\n'
                                            '    elif viewport_width < 992: return "md"\n'
                                            '    elif viewport_width < 1200: return "lg"\n'
                                            '    return "xl"\n',
                           'starter_code': 'def classify_viewport_breakpoint(viewport_width: int) -> str:\n'
                                           '    # Return breakpoint name\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Mobile screen is xs', 'expected': 'xs', 'input': [375]},
                                          {'desc': 'Tablet is md', 'expected': 'md', 'input': [800]}],
                           'title': 'Responsive Breakpoint Classifier'}},
 (5, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all timestamps positive ints',
                      'difficulty': 'Advance',
                      'explanation': 'Client-side session TTL invalidation.',
                      'function_name': 'is_session_expired',
                      'hint': 'Compare elapsed time with max_age_seconds.',
                      'id': 'c5-m5-l1-a',
                      'prompt': 'Write `is_session_expired(created_at_epoch, max_age_seconds, current_epoch)`: True if '
                                '`current_epoch - created_at_epoch >= max_age_seconds`, else False.',
                      'solution_code': 'def is_session_expired(created_at_epoch: int, max_age_seconds: int, '
                                       'current_epoch: int) -> bool:\n'
                                       '    return (current_epoch - created_at_epoch) >= max_age_seconds\n',
                      'starter_code': 'def is_session_expired(created_at_epoch: int, max_age_seconds: int, '
                                      'current_epoch: int) -> bool:\n'
                                      '    # Return True if session expired\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Elapsed 400 >= max_age 300 -> expired',
                                      'expected': True,
                                      'input': [1000, 300, 1400]},
                                     {'desc': 'Elapsed 200 < max_age 300 -> valid',
                                      'expected': False,
                                      'input': [1000, 300, 1200]}],
                      'title': 'Session Expiration Time Checker'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'key is string',
                    'difficulty': 'Basic',
                    'explanation': 'Web Storage API requirement that values be stored as strings.',
                    'function_name': 'serialize_storage_item',
                    'hint': 'import json; json.dumps(value)',
                    'id': 'c5-m5-l1-b',
                    'prompt': 'Write `serialize_storage_item(key, value)` returning `{"key": key, "value": '
                              'json.dumps(value)}`.',
                    'solution_code': 'def serialize_storage_item(key: str, value) -> dict:\n'
                                     '    import json\n'
                                     '    return {"key": key, "value": json.dumps(value)}\n',
                    'starter_code': 'def serialize_storage_item(key: str, value) -> dict:\n'
                                    '    # Return serialized storage pair\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Serializes dict to JSON string',
                                    'expected': {'key': 'theme', 'value': '{"dark": true}'},
                                    'input': ['theme', {'dark': True}]}],
                    'title': 'LocalStorage JSON Serializer'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'cookie_str is string',
                           'difficulty': 'Intermediate',
                           'explanation': 'HTTP document.cookie header parsing.',
                           'function_name': 'parse_cookie_header',
                           'hint': 'Split by ";", then split each pair by "=".',
                           'id': 'c5-m5-l1-i',
                           'prompt': 'Write `parse_cookie_header(cookie_str)` parsing `"key1=val1; key2=val2"` into '
                                     '`{key: val}` with stripped strings.',
                           'solution_code': 'def parse_cookie_header(cookie_str: str) -> dict:\n'
                                            '    if not cookie_str.strip(): return {}\n'
                                            '    res = {}\n'
                                            '    for pair in cookie_str.split(";"): \n'
                                            '        if "=" in pair:\n'
                                            '            k, v = pair.split("=", 1)\n'
                                            '            res[k.strip()] = v.strip()\n'
                                            '    return res\n',
                           'starter_code': 'def parse_cookie_header(cookie_str: str) -> dict:\n'
                                           '    # Return cookies dict\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Parses 2 cookies',
                                           'expected': {'session': 'abc123', 'user_id': '42'},
                                           'input': ['session=abc123; user_id=42']}],
                           'title': 'Cookie Header String Parser'}},
 (5, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'dpr >= 1.0',
                      'difficulty': 'Advance',
                      'explanation': 'Retina display sharpness adjustment using window.devicePixelRatio.',
                      'function_name': 'scale_retina_canvas',
                      'hint': 'Multiply css dimensions by devicePixelRatio.',
                      'id': 'c5-m5-l2-a',
                      'prompt': 'Write `scale_retina_canvas(css_w, css_h, dpr)`: buffer size = `[int(css_w * dpr), '
                                'int(css_h * dpr)]`. Return `{"buffer_size": [bw, bh], "dpr": dpr}`.',
                      'solution_code': 'def scale_retina_canvas(css_w: int, css_h: int, dpr: float) -> dict:\n'
                                       '    return {"buffer_size": [int(css_w * dpr), int(css_h * dpr)], "dpr": dpr}\n',
                      'starter_code': 'def scale_retina_canvas(css_w: int, css_h: int, dpr: float) -> dict:\n'
                                      '    # Return retina canvas spec\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Doubles buffer size for 2x DPR',
                                      'expected': {'buffer_size': [600, 300], 'dpr': 2.0},
                                      'input': [300, 150, 2.0]}],
                      'title': 'High-DPI Retina Canvas Coordinate Scaler'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'img_w > 0, img_h > 0, canvas_max > 0',
                    'difficulty': 'Basic',
                    'explanation': 'HTML5 Canvas 2D context image rendering scale.',
                    'function_name': 'calculate_canvas_fit',
                    'hint': 'scale = canvas_max / max(img_w, img_h); return w*scale, h*scale.',
                    'id': 'c5-m5-l2-b',
                    'prompt': 'Write `calculate_canvas_fit(img_w, img_h, canvas_max)` scaling image to fit inside '
                              '`canvas_max x canvas_max` preserving aspect ratio. Return `{"w": round(w, 1), "h": '
                              'round(h, 1)}`.',
                    'solution_code': 'def calculate_canvas_fit(img_w: float, img_h: float, canvas_max: float) -> '
                                     'dict:\n'
                                     '    scale = canvas_max / max(img_w, img_h)\n'
                                     '    return {"w": round(img_w * scale, 1), "h": round(img_h * scale, 1)}\n',
                    'starter_code': 'def calculate_canvas_fit(img_w: float, img_h: float, canvas_max: float) -> dict:\n'
                                    '    # Return scaled dimensions\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Scales width to 400, height to 300',
                                    'expected': {'h': 300.0, 'w': 400.0},
                                    'input': [800.0, 600.0, 400.0]}],
                    'title': 'Canvas Aspect Ratio Preserver'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'total_seconds >= 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'HTML5 Video player progress timestamp formatting.',
                           'function_name': 'format_media_timestamp',
                           'hint': 'Compute hours, mins, secs; format with :02d.',
                           'id': 'c5-m5-l2-i',
                           'prompt': 'Write `format_media_timestamp(total_seconds)` returning `"MM:SS"` or '
                                     '`"HH:MM:SS"` if hours > 0, padded with zero.',
                           'solution_code': 'def format_media_timestamp(total_seconds: int) -> str:\n'
                                            '    h = total_seconds // 3600\n'
                                            '    m = (total_seconds % 3600) // 60\n'
                                            '    s = total_seconds % 60\n'
                                            '    if h > 0: return f"{h:02d}:{m:02d}:{s:02d}"\n'
                                            '    return f"{m:02d}:{s:02d}"\n',
                           'starter_code': 'def format_media_timestamp(total_seconds: int) -> str:\n'
                                           '    # Return formatted timestamp\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '1 min 5 sec', 'expected': '01:05', 'input': [65]},
                                          {'desc': '1 hr 1 min 5 sec', 'expected': '01:01:05', 'input': [3665]}],
                           'title': 'Media Timestamp Formatter'}},
 (6, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'graph is DAG with no circular dependencies',
                      'difficulty': 'Advance',
                      'explanation': 'JavaScript bundler dependency graph resolution order.',
                      'function_name': 'topological_bundle_order',
                      'hint': "Compute in-degrees of dependencies, Kahn's algorithm.",
                      'id': 'c5-m6-l1-a',
                      'prompt': 'Write `topological_bundle_order(dependency_graph)` where graph is `{module: '
                                '[dependencies]}`. Return list of modules in valid bundle order (dependencies appear '
                                'before the module that imports them).',
                      'solution_code': 'def topological_bundle_order(dependency_graph: dict) -> list:\n'
                                       '    res = []\n'
                                       '    visited = set()\n'
                                       '    def dfs(node):\n'
                                       '        if node in visited: return\n'
                                       '        visited.add(node)\n'
                                       '        for dep in dependency_graph.get(node, []):\n'
                                       '            dfs(dep)\n'
                                       '        res.append(node)\n'
                                       '    for mod in sorted(dependency_graph.keys()): dfs(mod)\n'
                                       '    return res\n',
                      'starter_code': 'def topological_bundle_order(dependency_graph: dict) -> list:\n'
                                      '    # Return load order\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'utils before app',
                                      'expected': ['utils.js', 'app.js'],
                                      'input': [{'app.js': ['utils.js'], 'utils.js': []}]}],
                      'title': 'Module Dependency Topological Sort'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'base_path and relative_import are strings',
                    'difficulty': 'Basic',
                    'explanation': 'Webpack / Vite ES module path resolution.',
                    'function_name': 'resolve_module_path',
                    'hint': 'Handle ./ prefix and join with base_path.',
                    'id': 'c5-m6-l1-b',
                    'prompt': 'Write `resolve_module_path(base_path, relative_import)`: if relative_import starts with '
                              '"./", replace "./" with `base_path + "/"`. Strip double slashes.',
                    'solution_code': 'def resolve_module_path(base_path: str, relative_import: str) -> str:\n'
                                     '    if relative_import.startswith("./"):\n'
                                     '        rel = relative_import[2:]\n'
                                     '        return f"{base_path.rstrip(\'/\')}/{rel}"\n'
                                     '    return relative_import\n',
                    'starter_code': 'def resolve_module_path(base_path: str, relative_import: str) -> str:\n'
                                    '    # Return resolved module path\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Resolves relative import',
                                    'expected': 'src/components/Button.js',
                                    'input': ['src/components', './Button.js']}],
                    'title': 'ES6 Module Relative Path Resolver'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'all_exports and imported_names are lists of strings',
                           'difficulty': 'Intermediate',
                           'explanation': 'Bundler static dead code elimination (Tree Shaking).',
                           'function_name': 'tree_shake_exports',
                           'hint': 'Set difference: sorted(list(set(all_exports) - set(imported_names))).',
                           'id': 'c5-m6-l1-i',
                           'prompt': 'Write `tree_shake_exports(all_exports, imported_names)` returning sorted list of '
                                     'unused exports that can be eliminated (in all_exports but NOT in '
                                     'imported_names).',
                           'solution_code': 'def tree_shake_exports(all_exports: list, imported_names: list) -> list:\n'
                                            '    return sorted(list(set(all_exports) - set(imported_names)))\n',
                           'starter_code': 'def tree_shake_exports(all_exports: list, imported_names: list) -> list:\n'
                                           '    # Return dead exports to shake\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Eliminates multiply and subtract',
                                           'expected': ['multiply', 'subtract'],
                                           'input': [['add', 'subtract', 'multiply'], ['add']]}],
                           'title': 'Tree-Shaking Dead Code Export Eliminator'}},
 (6, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'starts at "/"',
                      'difficulty': 'Advance',
                      'explanation': 'HTML5 History API window.history.pushState and back() modeling.',
                      'function_name': 'simulate_history_navigation',
                      'hint': 'Track history stack and current index.',
                      'id': 'c5-m6-l2-a',
                      'prompt': 'Write `simulate_history_navigation(actions)` where action is `["push", url]` or '
                                '`["back", count]`. Return current URL at end.',
                      'solution_code': 'def simulate_history_navigation(actions: list) -> str:\n'
                                       '    stack = ["/"]\n'
                                       '    idx = 0\n'
                                       '    for act, val in actions:\n'
                                       '        if act == "push":\n'
                                       '            stack = stack[:idx + 1]\n'
                                       '            stack.append(val)\n'
                                       '            idx = len(stack) - 1\n'
                                       '        elif act == "back":\n'
                                       '            idx = max(0, idx - val)\n'
                                       '    return stack[idx]\n',
                      'starter_code': 'def simulate_history_navigation(actions: list) -> str:\n'
                                      '    # Return current active URL\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Pushes /home, /about, then goes back to /home',
                                      'expected': '/home',
                                      'input': [[['push', '/home'], ['push', '/about'], ['back', 1]]]}],
                      'title': 'Browser History Stack Simulator'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'url is string',
                    'difficulty': 'Basic',
                    'explanation': 'Single Page Application (SPA) hash-based client routing.',
                    'function_name': 'extract_hash_route',
                    'hint': 'Split by #, return second part or "/".',
                    'id': 'c5-m6-l2-b',
                    'prompt': 'Write `extract_hash_route(url)` extracting the path after `#`. If no `#`, return `"/"`.',
                    'solution_code': 'def extract_hash_route(url: str) -> str:\n'
                                     '    if "#" in url:\n'
                                     '        part = url.split("#", 1)[1]\n'
                                     '        return part if part else "/"\n'
                                     '    return "/"\n',
                    'starter_code': 'def extract_hash_route(url: str) -> str:\n    # Return hash route\n    pass\n',
                    'test_cases': [{'desc': 'Extracts /dashboard',
                                    'expected': '/dashboard',
                                    'input': ['http://localhost/#/dashboard']},
                                   {'desc': 'Default /', 'expected': '/', 'input': ['http://localhost/']}],
                    'title': 'SPA Hash Route Extractor'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'pattern and actual_path start with /',
                           'difficulty': 'Intermediate',
                           'explanation': 'Client-side SPA router dynamic path parsing (e.g. React Router, Vue '
                                          'Router).',
                           'function_name': 'match_route_params',
                           'hint': 'Split both by "/", compare lengths, match :param.',
                           'id': 'c5-m6-l2-i',
                           'prompt': 'Write `match_route_params(pattern, actual_path)` matching parameterized patterns '
                                     'like `"/users/:id/posts/:post_id"`. Return dict `{param_name: value}` if '
                                     'segments count match, else None.',
                           'solution_code': 'def match_route_params(pattern: str, actual_path: str):\n'
                                            '    p_parts = pattern.strip("/").split("/")\n'
                                            '    a_parts = actual_path.strip("/").split("/")\n'
                                            '    if len(p_parts) != len(a_parts): return None\n'
                                            '    params = {}\n'
                                            '    for p, a in zip(p_parts, a_parts):\n'
                                            '        if p.startswith(":"): params[p[1:]] = a\n'
                                            '        elif p != a: return None\n'
                                            '    return params\n',
                           'starter_code': 'def match_route_params(pattern: str, actual_path: str):\n'
                                           '    # Return params dict or None\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Extracts id: 42',
                                           'expected': {'id': '42'},
                                           'input': ['/users/:id', '/users/42']}],
                           'title': 'Dynamic Route Parameter Pattern Matcher'}}}
