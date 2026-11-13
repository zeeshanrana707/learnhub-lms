"""Course 6: Modern Web Engineering with Flask - Topic-Specific Challenges."""

CHALLENGES = {
    (1, 1): {
        'basic': {
            'id': 'c6-m1-l1-b',
            'difficulty': 'Basic',
            'badge_class': 'bg-success',
            'title': 'WSGI Environment Status Code Mapper',
            'function_name': 'map_status_string',
            'prompt': 'Write `map_status_string(status_code)` that returns the standard HTTP status line (e.g. 200 -> "200 OK", 404 -> "404 Not Found", 500 -> "500 Internal Server Error", 201 -> "201 Created", 400 -> "400 Bad Request"). If unknown, return f"{status_code} Unknown".',
            'constraints': '100 <= status_code <= 599',
            'starter_code': 'def map_status_string(status_code: int) -> str:\n    # Return status line\n    pass\n',
            'test_cases': [
                {'desc': 'OK', 'input': [200], 'expected': '200 OK'},
                {'desc': 'Not Found', 'input': [404], 'expected': '404 Not Found'},
                {'desc': 'Created', 'input': [201], 'expected': '201 Created'},
                {'desc': 'Unknown', 'input': [999], 'expected': '999 Unknown'}
            ],
            'hint': 'Use a dictionary lookup with .get(status_code, f"{status_code} Unknown").',
            'solution_code': 'def map_status_string(status_code: int) -> str:\n    table = {200: "200 OK", 201: "201 Created", 400: "400 Bad Request", 404: "404 Not Found", 500: "500 Internal Server Error"}\n    return table.get(status_code, f"{status_code} Unknown")\n',
            'explanation': 'WSGI start_response() takes a status string matching standard RFC HTTP tokens.'
        },
        'intermediate': {
            'id': 'c6-m1-l1-i',
            'difficulty': 'Intermediate',
            'badge_class': 'bg-primary',
            'title': 'Flask Application Configuration Loader',
            'function_name': 'load_flask_config',
            'prompt': 'Write `load_flask_config(env_dict, prefix="FLASK_")` that extracts all keys beginning with prefix, removes the prefix, lowercase them, and parses "true"/"false" strings to booleans and numeric strings to ints/floats.',
            'constraints': 'env_dict is a dict of string keys/values',
            'starter_code': 'def load_flask_config(env_dict: dict, prefix: str = "FLASK_") -> dict:\n    # Extract and parse config keys\n    pass\n',
            'test_cases': [
                {'desc': 'Config parsing', 'input': [{'FLASK_DEBUG': 'true', 'FLASK_PORT': '5000', 'SECRET': 'xyz'}], 'expected': {'debug': True, 'port': 5000}},
                {'desc': 'No prefix matches', 'input': [{'DATABASE_URL': 'sqlite:///db.sqlite3'}], 'expected': {}}
            ],
            'hint': 'Check k.startswith(prefix). Strip prefix, .lower(), then parse value.',
            'solution_code': 'def load_flask_config(env_dict: dict, prefix: str = "FLASK_") -> dict:\n    res = {}\n    for k, v in env_dict.items():\n        if k.startswith(prefix):\n            clean_key = k[len(prefix):].lower()\n            if v.lower() == "true": parsed = True\n            elif v.lower() == "false": parsed = False\n            elif v.isdigit(): parsed = int(v)\n            else: parsed = v\n            res[clean_key] = parsed\n    return res\n',
            'explanation': 'Flask app.config.from_prefixed_env() pattern for 12-factor cloud apps.'
        },
        'advance': {
            'id': 'c6-m1-l1-a',
            'difficulty': 'Advance',
            'badge_class': 'bg-purple',
            'title': 'WSGI Middleware Request Timer & Logger',
            'function_name': 'simulate_wsgi_middleware',
            'prompt': 'Write `simulate_wsgi_middleware(environ, app_handler, timing_ms)` that invokes `app_handler(environ)` and injects a "X-Response-Time-Ms" header into the returned response headers list `[(k, v)]`.',
            'constraints': 'timing_ms >= 0',
            'starter_code': 'def simulate_wsgi_middleware(environ: dict, app_handler, timing_ms: int) -> tuple:\n    # Invoke handler and append X-Response-Time-Ms\n    pass\n',
            'test_cases': [
                {'desc': 'Injects timing header', 'input': [{'PATH_INFO': '/api'}, 'app_handler', 42], 'expected': (200, [('Content-Type', 'application/json'), ('X-Response-Time-Ms', '42')], '{"ok":true}')}
            ],
            'hint': 'Call app_handler(environ). Unpack status, headers, body, append (key, str(timing_ms)), return tuple.',
            'solution_code': 'def simulate_wsgi_middleware(environ: dict, app_handler, timing_ms: int) -> tuple:\n    status, headers, body = app_handler(environ)\n    new_headers = list(headers) + [("X-Response-Time-Ms", str(timing_ms))]\n    return (status, new_headers, body)\n',
            'explanation': 'Demonstrates standard PEP 3333 WSGI middleware wrapping techniques.'
        }
    },
    (1, 2): {
        'basic': {
            'id': 'c6-m1-l2-b',
            'difficulty': 'Basic',
            'badge_class': 'bg-success',
            'title': 'Flask URL Converter Pattern Matcher',
            'function_name': 'match_flask_int_rule',
            'prompt': 'Write `match_flask_int_rule(path_template, actual_path)` for simple `<int:var>` converter. E.g., template="/users/<int:user_id>" and actual="/users/42" returns `{"user_id": 42}`. If non-matching or not integer, return None.',
            'constraints': 'Single variable in template',
            'starter_code': 'def match_flask_int_rule(path_template: str, actual_path: str):\n    # Extract integer parameter or return None\n    pass\n',
            'test_cases': [
                {'desc': 'Match int', 'input': ['/users/<int:user_id>', '/users/42'], 'expected': {'user_id': 42}},
                {'desc': 'Mismatch non-int', 'input': ['/users/<int:user_id>', '/users/alice'], 'expected': None},
                {'desc': 'Prefix mismatch', 'input': ['/posts/<int:post_id>', '/users/10'], 'expected': None}
            ],
            'hint': 'Split both paths by "/". Find where <int:name> appears and parse corresponding part as int.',
            'solution_code': 'def match_flask_int_rule(path_template: str, actual_path: str):\n    t_parts = path_template.strip("/").split("/")\n    a_parts = actual_path.strip("/").split("/")\n    if len(t_parts) != len(a_parts): return None\n    res = {}\n    for tp, ap in zip(t_parts, a_parts):\n        if tp.startswith("<int:") and tp.endswith(">"):\n            param = tp[5:-1]\n            if not ap.isdigit(): return None\n            res[param] = int(ap)\n        elif tp != ap:\n            return None\n    return res\n',
            'explanation': 'Flask Werkzeug routing Map and Rule compiler matches URL converters.'
        },
        'intermediate': {
            'id': 'c6-m1-l2-i',
            'difficulty': 'Intermediate',
            'badge_class': 'bg-primary',
            'title': 'HTTP Method Router Dispatcher',
            'function_name': 'dispatch_flask_route',
            'prompt': 'Write `dispatch_flask_route(registered_methods, request_method, view_func)` that calls `view_func()` if `request_method.upper()` is in `registered_methods`. Otherwise returns `(405, "Method Not Allowed")`.',
            'constraints': 'request_method is string',
            'starter_code': 'def dispatch_flask_route(registered_methods: list, request_method: str, view_func):\n    # Call view_func or return 405\n    pass\n',
            'test_cases': [
                {'desc': 'Allowed GET', 'input': [['GET', 'POST'], 'GET', 'view_func'], 'expected': (200, 'Success')},
                {'desc': 'Disallowed DELETE', 'input': [['GET', 'POST'], 'DELETE', 'view_func'], 'expected': (405, 'Method Not Allowed')}
            ],
            'hint': 'Check if request_method.upper() in [m.upper() for m in registered_methods].',
            'solution_code': 'def dispatch_flask_route(registered_methods: list, request_method: str, view_func):\n    allowed = [m.upper() for m in registered_methods]\n    if request_method.upper() in allowed:\n        return view_func()\n    return (405, "Method Not Allowed")\n',
            'explanation': 'Flask automatically enforces the methods argument on @app.route() and generates 405 responses.'
        },
        'advance': {
            'id': 'c6-m1-l2-a',
            'difficulty': 'Advance',
            'badge_class': 'bg-purple',
            'title': 'Subdomain Routing Regex Evaluator',
            'function_name': 'resolve_subdomain',
            'prompt': 'Write `resolve_subdomain(host_header, server_name)` that extracts the subdomain. E.g. host="user.acme.com", server_name="acme.com" -> "user". If host == server_name or not ending in server_name, return None.',
            'constraints': 'host and server_name are non-empty strings',
            'starter_code': 'def resolve_subdomain(host_header: str, server_name: str):\n    # Extract subdomain or None\n    pass\n',
            'test_cases': [
                {'desc': 'Tenant subdomain', 'input': ['tenant1.example.com', 'example.com'], 'expected': 'tenant1'},
                {'desc': 'Apex domain', 'input': ['example.com', 'example.com'], 'expected': None},
                {'desc': 'Different domain', 'input': ['tenant.other.com', 'example.com'], 'expected': None}
            ],
            'hint': 'Check host_header.endswith("." + server_name). Return host[:-len(server_name)-1].',
            'solution_code': 'def resolve_subdomain(host_header: str, server_name: str):\n    suffix = "." + server_name\n    if host_header.endswith(suffix):\n        return host_header[:-len(suffix)]\n    return None\n',
            'explanation': 'Flask Blueprint subdomain routing allows multi-tenant SaaS architectures.'
        }
    },
    (1, 3): {
        'basic': {
            'id': 'c6-m1-l3-b',
            'difficulty': 'Basic',
            'badge_class': 'bg-success',
            'title': 'Query Parameter Parser with Defaults',
            'function_name': 'parse_query_args',
            'prompt': 'Write `parse_query_args(query_dict, key, default_val, expected_type)` that retrieves `key` from `query_dict`. If present, casts to `expected_type` (int, float, str). If missing or casting raises ValueError, returns `default_val`.',
            'constraints': 'query_dict maps str to str',
            'starter_code': 'def parse_query_args(query_dict: dict, key: str, default_val, expected_type):\n    # Return cast value or default\n    pass\n',
            'test_cases': [
                {'desc': 'Valid page int', 'input': [{'page': '3'}, 'page', 1, 'int'], 'expected': 3},
                {'desc': 'Invalid int returns default', 'input': [{'page': 'abc'}, 'page', 1, 'int'], 'expected': 1},
                {'desc': 'Missing key returns default', 'input': [{}, 'limit', 20, 'int'], 'expected': 20}
            ],
            'hint': 'Use try-except around expected_type(query_dict[key]).',
            'solution_code': 'def parse_query_args(query_dict: dict, key: str, default_val, expected_type):\n    if key not in query_dict:\n        return default_val\n    try:\n        return expected_type(query_dict[key])\n    except (ValueError, TypeError):\n        return default_val\n',
            'explanation': 'Replicates Flask request.args.get(key, default, type=int).'
        },
        'intermediate': {
            'id': 'c6-m1-l3-i',
            'difficulty': 'Intermediate',
            'badge_class': 'bg-primary',
            'title': 'Form Payload Validator & Sanitizer',
            'function_name': 'validate_contact_form',
            'prompt': 'Write `validate_contact_form(form_data)` that validates required fields "name" and "email". Both must be non-empty strings. Email must contain "@" and ".". Returns `(True, {"name": name.strip(), "email": email.strip()})` if valid, or `(False, "error message")`.',
            'constraints': 'form_data is a dict',
            'starter_code': 'def validate_contact_form(form_data: dict) -> tuple:\n    # Return (is_valid, data_or_error)\n    pass\n',
            'test_cases': [
                {'desc': 'Valid form', 'input': [{'name': ' Alice ', 'email': 'alice@domain.com'}], 'expected': (True, {'name': 'Alice', 'email': 'alice@domain.com'})},
                {'desc': 'Missing email', 'input': [{'name': 'Bob'}], 'expected': (False, 'Missing email')},
                {'desc': 'Invalid email format', 'input': [{'name': 'Charlie', 'email': 'notanemail'}], 'expected': (False, 'Invalid email format')}
            ],
            'hint': 'Check "name" in form_data and "email" in form_data. Validate "@" and "." in email.',
            'solution_code': 'def validate_contact_form(form_data: dict) -> tuple:\n    name = form_data.get("name", "").strip()\n    email = form_data.get("email", "").strip()\n    if not name:\n        return (False, "Missing name")\n    if not email:\n        return (False, "Missing email")\n    if "@" not in email or "." not in email.split("@")[-1]:\n        return (False, "Invalid email format")\n    return (True, {"name": name, "email": email})\n',
            'explanation': 'Essential validation pattern before storing user inputs to database.'
        },
        'advance': {
            'id': 'c6-m1-l3-a',
            'difficulty': 'Advance',
            'badge_class': 'bg-purple',
            'title': 'Flask Request Context Stack Manager',
            'function_name': 'simulate_context_stack',
            'prompt': 'Write a class or function `simulate_context_stack(requests)` that manages a stack of request contexts. For each request dict in requests: pushes context, attaches "request_id", executes handler, and pops on exit ensuring LIFO cleanup.',
            'constraints': 'requests is a list of dicts',
            'starter_code': 'def simulate_context_stack(requests: list) -> list:\n    # Return list of processed request IDs in order\n    pass\n',
            'test_cases': [
                {'desc': 'Process requests', 'input': [[{'id': 'req-1'}, {'id': 'req-2'}]], 'expected': ['req-1', 'req-2']}
            ],
            'hint': 'Loop requests, push to stack, record execution, pop from stack.',
            'solution_code': 'def simulate_context_stack(requests: list) -> list:\n    stack = []\n    processed = []\n    for r in requests:\n        stack.append(r)\n        processed.append(stack[-1]["id"])\n        stack.pop()\n    return processed\n',
            'explanation': 'Flask uses Werkzeug LocalStack for thread-safe context resolution.'
        }
    }
}
