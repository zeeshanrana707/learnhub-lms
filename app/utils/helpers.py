import os
import re
import unicodedata
from datetime import datetime, timezone
from flask import request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.admin import AuditLog

def slugify(text: str) -> str:
    """Generate a clean URL slug from a text title."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


def log_action(user, action: str, entity_type: str, entity_id: int = None, details: str = None):
    """Create an entry in the AuditLog."""
    try:
        user_id = user.id if user and getattr(user, 'is_authenticated', False) else None
        ip = request.remote_addr if request else '127.0.0.1'
        entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        # Audit logging should never crash the main transaction
        db.session.rollback()
        if current_app and current_app.logger:
            current_app.logger.warning(f"Failed to write audit log: {e}")


def allowed_file(filename: str) -> bool:
    """Check if uploaded file extension is in ALLOWED_EXTENSIONS."""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'zip'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_file(file_storage, subfolder: str = 'submissions') -> str:
    """Save an uploaded file safely and return its relative URL/path."""
    filename = secure_filename(file_storage.filename)
    if not filename:
        return ''
    # prefix timestamp to prevent collisions
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(target_dir, exist_ok=True)
    full_path = os.path.join(target_dir, unique_filename)
    file_storage.save(full_path)
    return f"uploads/{subfolder}/{unique_filename}"


def extract_youtube_id(text: str) -> str | None:
    """Extract 11-character YouTube video ID from various URL patterns."""
    if not text:
        return None
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def get_lesson_breakdown(lesson) -> dict:
    """Generate structured key components and explanations for any video lesson."""
    title = getattr(lesson, 'title', 'Lecture Overview')
    content = getattr(lesson, 'content', '') or ''
    module = getattr(lesson, 'module', None)
    module_title = module.title if module else ''
    course = module.course if module else None
    course_title = course.title if course else ''

    # Clean out raw YouTube URLs from display notes
    clean_lines = []
    for line in content.splitlines():
        if 'youtube.com' in line or 'youtu.be' in line:
            continue
        clean_lines.append(line)
    clean_text = '\n'.join(clean_lines).strip()

    paragraphs = [p.strip() for p in clean_text.split('\n\n') if p.strip()]
    overview = paragraphs[0] if paragraphs else f"In this lecture, students master {title} as part of {module_title}."

    t_lower = title.lower()
    m_lower = module_title.lower()
    c_lower = course_title.lower()
    full_str = f"{t_lower} {m_lower} {c_lower} {clean_text.lower()}"

    # 1. Python Language & OOP
    if any(k in full_str for k in ['syntax', 'variables & operators', 'primitive types']):
        components = [
            {"title": "Primitive Data Types", "desc": "Integer, float, string, and boolean representations with dynamic typing and memory binding.", "icon": "bi-type", "badge": "Syntax"},
            {"title": "Operators & Logic", "desc": "PEMDAS math operations, comparison chaining, and logical boolean flow (and/or/not).", "icon": "bi-calculator", "badge": "Logic"},
            {"title": "Conditional Branching", "desc": "If, elif, and else decision trees with whitespace-indented block execution.", "icon": "bi-signpost-split", "badge": "Control Flow"},
            {"title": "Dynamic Interpolation", "desc": "String formatting using Python 3 f-strings and explicit type casting conventions.", "icon": "bi-code-square", "badge": "Formatting"}
        ]
    elif any(k in full_str for k in ['data structures: lists', 'dictionaries', 'tuples', 'sets']):
        components = [
            {"title": "Lists & Slicing", "desc": "Ordered mutable sequences, zero-based indexing, slicing intervals, and in-place list methods.", "icon": "bi-list-ol", "badge": "Lists"},
            {"title": "Dictionaries (Hash Maps)", "desc": "Key-value pair mappings with O(1) average lookup times, .keys(), .values(), and .items().", "icon": "bi-key", "badge": "Hash Maps"},
            {"title": "Tuples & Sets", "desc": "Immutable coordinate tuples and unique-value sets with intersection/union set mathematics.", "icon": "bi-collection", "badge": "Sets/Tuples"},
            {"title": "Comprehensions", "desc": "Idiomatic list and dictionary comprehensions replacing verbose procedural loops.", "icon": "bi-lightning-charge", "badge": "Idiomatic"}
        ]
    # 2. NumPy & Math
    elif any(k in full_str for k in ['numpy', 'vector computing', 'ndarray']):
        components = [
            {"title": "ndarray Architecture", "desc": "Contiguous memory layout, fixed-type elements, multidimensional shapes, and strides.", "icon": "bi-grid-3x3", "badge": "Memory"},
            {"title": "Vectorized Execution", "desc": "SIMD parallel element-wise arithmetic eliminating slow Python for-loop bottlenecks.", "icon": "bi-cpu", "badge": "Performance"},
            {"title": "Broadcasting Rules", "desc": "Implicit dimension expansion allowing arithmetic between matrices of differing shapes.", "icon": "bi-arrows-angle-expand", "badge": "Broadcasting"},
            {"title": "Matrix Multiplication", "desc": "Dot products and 2D matrix multiplication (@ operator) foundational for neural weights.", "icon": "bi-asterisk", "badge": "Linear Algebra"}
        ]
    # 3. Pandas & EDA
    elif any(k in full_str for k in ['pandas', 'data cleaning', 'eda', 'dataframes']):
        components = [
            {"title": "Series vs DataFrame", "desc": "1D labeled arrays and 2D tabular structures with heterogeneous column typing.", "icon": "bi-table", "badge": "Tabular"},
            {"title": "Row & Column Indexing", "desc": "Label-based selection via .loc[] and integer-position slicing using .iloc[].", "icon": "bi-cursor", "badge": "Indexing"},
            {"title": "Data Imputation & Nulls", "desc": "Detecting missing values with .isna(), applying imputation with .fillna() or .dropna().", "icon": "bi-brush", "badge": "Cleaning"},
            {"title": "Groupby & Aggregation", "desc": "Split-apply-combine workflow calculating segment statistics, sums, and distributions.", "icon": "bi-pie-chart", "badge": "Analytics"}
        ]
    elif any(k in full_str for k in ['matplotlib', 'seaborn', 'visualization', 'exploratory data']):
        components = [
            {"title": "Figure & Axes Hierarchy", "desc": "Object-oriented Matplotlib canvas structure with figures, subplots, and titles.", "icon": "bi-bounding-box", "badge": "Layout"},
            {"title": "Statistical Plots", "desc": "Histograms for feature distributions, box plots for outliers, and scatter plots.", "icon": "bi-bar-chart-line", "badge": "Distributions"},
            {"title": "Correlation Heatmaps", "desc": "Pairwise Pearson correlation matrices highlighting multi-collinear predictors.", "icon": "bi-thermometer-half", "badge": "Insights"},
            {"title": "Data Preparation", "desc": "Systematic dataset profiling and feature extraction before training predictive models.", "icon": "bi-search", "badge": "Workflow"}
        ]
    # 4. Scikit-Learn & Machine Learning
    elif any(k in full_str for k in ['supervised', 'regression', 'decision tree', 'random forest', 'scikit']):
        components = [
            {"title": "Supervised Learning", "desc": "Continuous target forecasting (regression) vs discrete class boundary separation.", "icon": "bi-bezier2", "badge": "Modeling"},
            {"title": "Feature Scaling", "desc": "StandardScaler (Z-score) and MinMaxScaler preventing feature domination in gradient descent.", "icon": "bi-sliders", "badge": "Preprocessing"},
            {"title": "Ensemble Methods", "desc": "Bootstrap aggregating (bagging) and Random Forest decorrelation of decision trees.", "icon": "bi-diagram-2", "badge": "Ensembles"},
            {"title": "Cross-Validation", "desc": "K-fold cross validation preventing data leakage and ensuring generalized test accuracy.", "icon": "bi-check2-square", "badge": "Validation"}
        ]
    elif any(k in full_str for k in ['confusion matrix', 'hyperparameter', 'gridsearch', 'roc-auc']):
        components = [
            {"title": "Confusion Matrix Analysis", "desc": "True Positives, False Positives, False Negatives, and precision-recall trade-offs.", "icon": "bi-grid", "badge": "Diagnostics"},
            {"title": "ROC-AUC Curves", "desc": "Area Under the Receiver Operating Characteristic curve measuring threshold sensitivity.", "icon": "bi-graph-up", "badge": "Evaluation"},
            {"title": "GridSearchCV", "desc": "Exhaustive hyperparameter parameter search finding optimal model configurations.", "icon": "bi-gear-wide-connected", "badge": "Tuning"},
            {"title": "Model Persistence", "desc": "Serializing trained pipelines using Joblib/Pickle for production deployment.", "icon": "bi-save", "badge": "Serialization"}
        ]
    # 5. Deep Learning & PyTorch
    elif any(k in full_str for k in ['neural network', 'weights, biases', 'backpropagation']):
        components = [
            {"title": "Perceptron Foundations", "desc": "Linear layer transformations y = Wx + b followed by non-linear activation functions.", "icon": "bi-diagram-3", "badge": "Perceptrons"},
            {"title": "Non-Linear Activations", "desc": "ReLU, Sigmoid, and Softmax introducing non-linearity to learn complex manifolds.", "icon": "bi-activity", "badge": "Activations"},
            {"title": "Backpropagation Calculus", "desc": "Automated differentiation via the chain rule computing partial loss gradients.", "icon": "bi-calculator-fill", "badge": "Calculus"},
            {"title": "Gradient Optimizers", "desc": "Stochastic Gradient Descent (SGD) and Adam adjusting weights across training epochs.", "icon": "bi-sliders2", "badge": "Optimizers"}
        ]
    elif any(k in full_str for k in ['cnn', 'convolution', 'feature maps', 'pooling']):
        components = [
            {"title": "2D Convolution Kernels", "desc": "Sliding matrix filters capturing spatial hierarchies like edges, textures, and shapes.", "icon": "bi-aspect-ratio", "badge": "Filters"},
            {"title": "Spatial Pooling", "desc": "Max pooling and average pooling reducing dimensionality while preserving spatial features.", "icon": "bi-fullscreen-exit", "badge": "Pooling"},
            {"title": "PyTorch nn.Module", "desc": "Structuring neural network layers with forward() passes and automatic autograd graphs.", "icon": "bi-boxes", "badge": "PyTorch"},
            {"title": "Transfer Learning", "desc": "Fine-tuning pretrained ResNet and EfficientNet backbones for custom classification tasks.", "icon": "bi-arrow-repeat", "badge": "Transfer"}
        ]
    # 6. Generative AI, LLMs & LangChain
    elif any(k in full_str for k in ['gpt', 'transformer', 'attention', 'llm', 'karpathy']):
        components = [
            {"title": "Self-Attention Mechanism", "desc": "Query, Key, and Value dot-product projections weighing contextual token importance.", "icon": "bi-eye", "badge": "Attention"},
            {"title": "Tokenization & Embeddings", "desc": "Byte-pair encoding (BPE) mapping text tokens into high-dimensional latent space.", "icon": "bi-card-text", "badge": "Embeddings"},
            {"title": "Autoregressive Generation", "desc": "Next-token probability prediction, temperature sampling, and top-p decoding.", "icon": "bi-cpu-fill", "badge": "Inference"},
            {"title": "Transformer Architecture", "desc": "Multi-head attention coupled with feedforward networks, layer norm, and residual skips.", "icon": "bi-stack", "badge": "Architecture"}
        ]
    elif any(k in full_str for k in ['rag', 'vector database', 'chroma', 'pinecone', 'langchain']):
        components = [
            {"title": "Dense Vector Embeddings", "desc": "Encoding unstructured documents into dense semantic vectors using embedding models.", "icon": "bi-pin-map", "badge": "Embeddings"},
            {"title": "Vector Databases (Chroma)", "desc": "Storing and indexing embeddings with Approximate Nearest Neighbor (HNSW) search.", "icon": "bi-database-fill", "badge": "Vector DB"},
            {"title": "Chunking Strategies", "desc": "Recursive character text splitters with semantic overlap ensuring cohesive context.", "icon": "bi-scissors", "badge": "Chunking"},
            {"title": "Contextual Retrieval", "desc": "Injecting grounded document chunks into prompt templates to eliminate hallucinations.", "icon": "bi-shield-check", "badge": "Grounding"}
        ]
    # 7. Web Development (JS, Flask, APIs)
    elif any(k in full_str for k in ['javascript', 'dom', 'async', 'promise', 'fetch']):
        components = [
            {"title": "Modern ES6+ Syntax", "desc": "Let/const scoping, arrow functions, destructuring assignments, and template literals.", "icon": "bi-filetype-js", "badge": "Syntax"},
            {"title": "DOM Manipulation", "desc": "Selecting elements via querySelector, dispatching event listeners, and updating nodes.", "icon": "bi-cursor-fill", "badge": "DOM"},
            {"title": "Asynchronous Event Loop", "desc": "Call stack, task queue, microtasks, Promise chaining, and async/await syntax.", "icon": "bi-arrow-repeat", "badge": "Async"},
            {"title": "REST API Fetching", "desc": "Handling HTTP GET/POST requests using the browser Fetch API with error handling.", "icon": "bi-cloud-download", "badge": "HTTP"}
        ]
    elif any(k in full_str for k in ['flask', 'restful api', 'jinja', 'route', 'sqlalchemy']):
        components = [
            {"title": "Routing & View Functions", "desc": "Decorating endpoints with @app.route, parameter extraction, and request dispatch.", "icon": "bi-signpost", "badge": "Routing"},
            {"title": "Jinja2 Dynamic Views", "desc": "Template inheritance with base layouts, conditional blocks, loops, and custom filters.", "icon": "bi-code-slash", "badge": "Templates"},
            {"title": "Flask-WTF & Security", "desc": "CSRF protection tokens, field validation rules, and sanitized request body parsing.", "icon": "bi-shield-lock", "badge": "Security"},
            {"title": "Flask-SQLAlchemy ORM", "desc": "Declarative database models, relationships, queries, migrations, and atomic commits.", "icon": "bi-database", "badge": "ORM"}
        ]
    # 8. DevOps, Docker & Kubernetes
    elif any(k in full_str for k in ['docker', 'container', 'dockerfile', 'compose']):
        components = [
            {"title": "Containerization Fundamentals", "desc": "Linux kernel namespaces, cgroups, and isolated immutable filesystem layers.", "icon": "bi-box-seam", "badge": "Isolation"},
            {"title": "Dockerfile Multi-stage Builds", "desc": "Directives: FROM, RUN, COPY, WORKDIR, and EXPOSE optimizing lightweight image sizes.", "icon": "bi-file-earmark-code", "badge": "Build"},
            {"title": "Networking & Port Mapping", "desc": "Container bridge networks, DNS service resolution, and host port publishing (-p).", "icon": "bi-hdd-network", "badge": "Networking"},
            {"title": "Persistent Data Volumes", "desc": "Named volume mounts and bind mounts decoupling application state from containers.", "icon": "bi-hdd", "badge": "Storage"}
        ]
    elif any(k in full_str for k in ['kubernetes', 'k8s', 'cluster', 'deployment', 'pod']):
        components = [
            {"title": "Cluster Architecture", "desc": "Control plane (API Server, etcd, scheduler) managing worker nodes and kubelet agents.", "icon": "bi-hdd-stack", "badge": "Architecture"},
            {"title": "Pods & Deployments", "desc": "Declarative YAML resource manifests, replica sets, and zero-downtime rolling updates.", "icon": "bi-layers", "badge": "Workloads"},
            {"title": "Services & Ingress", "desc": "ClusterIP, NodePort, and LoadBalancer abstractions exposing resilient internal apps.", "icon": "bi-diagram-3", "badge": "Services"},
            {"title": "ConfigMaps & Secrets", "desc": "Decoupling configuration parameters and cryptographic credentials from containers.", "icon": "bi-key-fill", "badge": "Config"}
        ]
    # 9. Cybersecurity & Networking
    elif any(k in full_str for k in ['wireshark', 'network', 'owasp', 'penetration', 'security', 'hacking']):
        components = [
            {"title": "Protocol Stack Inspection", "desc": "Analyzing Ethernet frames, IP packet headers, TCP three-way handshakes, and UDP.", "icon": "bi-shield-shaded", "badge": "Protocols"},
            {"title": "Traffic Capture & Filters", "desc": "Applying capture and display filters to trace suspicious payload behavior in Wireshark.", "icon": "bi-search", "badge": "Packet Analysis"},
            {"title": "Vulnerability Analysis", "desc": "Identifying injection vectors, improper authentication, and insecure direct object references.", "icon": "bi-exclamation-triangle", "badge": "OWASP"},
            {"title": "Defense & Hardening", "desc": "Input sanitization, parameterized queries, least-privilege access, and defense-in-depth.", "icon": "bi-shield-check", "badge": "Hardening"}
        ]
    # 10. Databases & Systems
    elif any(k in full_str for k in ['sql', 'database', 'join', 'indexing', 'query']):
        components = [
            {"title": "Relational Modeling", "desc": "Entity normalization (1NF-3NF), primary/foreign key integrity, and relational schemas.", "icon": "bi-table", "badge": "Schema"},
            {"title": "Query Filtering & Sorting", "desc": "SELECT statements, WHERE predicates, logical conjunctions, and indexed ORDER BY clauses.", "icon": "bi-filter", "badge": "Filtering"},
            {"title": "Multi-Table Joins", "desc": "INNER, LEFT, RIGHT, and FULL OUTER JOINs combining related multi-entity datasets.", "icon": "bi-intersect", "badge": "Joins"},
            {"title": "B-Tree Indexing", "desc": "Clustered vs non-clustered indexes optimizing logarithmic O(log N) lookup speeds.", "icon": "bi-speedometer2", "badge": "Performance"}
        ]
    # 11. Computer Science & CS50
    elif any(k in full_str for k in ['cs50', 'pointer', 'memory', 'algorithm', 'big-o', 'binary']):
        components = [
            {"title": "Computational Thinking", "desc": "Binary representations, ASCII encoding, memory addressing, and CPU execution cycles.", "icon": "bi-mortarboard", "badge": "Foundations"},
            {"title": "Memory & Pointers", "desc": "Stack vs Heap allocation, memory addresses (&), pointer dereferencing (*), and malloc/free.", "icon": "bi-memory", "badge": "Memory"},
            {"title": "Algorithmic Complexity", "desc": "Big-O notation analyzing worst-case time and space efficiency of sorting and search.", "icon": "bi-graph-up-arrow", "badge": "Big-O"},
            {"title": "Dynamic Data Structures", "desc": "Linked lists, hash tables, and binary search trees overcoming fixed-array limitations.", "icon": "bi-diagram-3-fill", "badge": "Data Structures"}
        ]
    else:
        # Generic intelligent breakdown
        components = [
            {"title": "Core Foundations & Theory", "desc": f"Theoretical principles and architectural concepts governing {title}.", "icon": "bi-journal-check", "badge": "Core Theory"},
            {"title": "Step-by-Step Implementation", "desc": "Hands-on coding, practical tooling, and workflow patterns demonstrated in the lecture.", "icon": "bi-tools", "badge": "Hands-On"},
            {"title": "Engineering Best Practices", "desc": "Industry standards, edge cases to handle, and performance optimizations.", "icon": "bi-shield-check", "badge": "Best Practices"},
            {"title": "Roadmap Next Steps", "desc": f"Connecting this topic to your broader milestone progression in {module_title}.", "icon": "bi-arrow-right-circle", "badge": "Roadmap Context"}
        ]

    takeaways = [
        f"Master the core operational patterns and technical terminology of {title}.",
        f"Understand the architectural rationale and production use cases in {module_title}.",
        f"Apply this lecture's hands-on demonstrations directly in course projects and upcoming quizzes."
    ]

    why_it_matters = f"This lecture provides critical technical competencies required in the {course_title} curriculum. Understanding these principles ensures you possess production-ready skills for software engineering and technical interviews."

    return {
        "title": title,
        "clean_text": clean_text,
        "overview": overview,
        "components": components,
        "takeaways": takeaways,
        "why_it_matters": why_it_matters
    }

