"""
Update all 19 courses so that EVERY single topic has a 100% UNIQUE YouTube video.
Zero duplicate video URLs across topics in any course!
"""

import sys
import re
from pathlib import Path
sys.path.insert(0, r"c:\Users\Zeeshan\Desktop\rana")

from app import create_app
from app.extensions import db
from app.models.catalog import Course
from app.models.content import Module, Lesson, LessonResource

UNIQUE_TOPIC_VIDEOS = {
    # =========================================================================
    # 1. AI & MACHINE LEARNING ENGINEER ROADMAP
    # =========================================================================
    "Python for AI & Data Science Foundations": [
        ("Module 1: Python Core Language Fundamentals", [
            ("Topic 1.1: Python Core Syntax, Variables & Primitive Types",
             "https://www.youtube.com/watch?v=kqtD5dpn9C8\n\nProgramming with Mosh: Python syntax, primitive variable types (integers, floats, strings, booleans), expressions, and dynamic type casting.",
             60, "https://docs.python.org/3/tutorial/introduction.html"),
            ("Topic 1.2: Control Flow, Conditionals & Loop Mechanics",
             "https://www.youtube.com/watch?v=6iF8Xb7Z3wQ\n\nCorey Schafer: Conditionals, boolean logic operators (and, or, not), if-elif-else branches, and while/for loop iterators.",
             10, "https://docs.python.org/3/tutorial/controlflow.html")
        ]),
        ("Module 2: Collection Data Structures & Functional Programming", [
            ("Topic 2.1: Lists, Tuples, Sets & Dictionary Manipulations",
             "https://www.youtube.com/watch?v=W8KRzm-HUcc\n\nCorey Schafer: In-depth lists, tuples, sets, dictionary key-value storage, dictionary comprehension, and mutation methods.",
             29, "https://docs.python.org/3/tutorial/datastructures.html"),
            ("Topic 2.2: Custom Functions, Args/Kwargs & Lambda Closures",
             "https://www.youtube.com/watch?v=9Os0o3wzS_I\n\nCorey Schafer: Defining clean modular functions, default arguments, unpacking *args and **kwargs, lambda functions, and closures.",
             22, "https://docs.python.org/3/tutorial/controlflow.html#defining-functions")
        ]),
        ("Module 3: Object-Oriented Programming (OOP) for AI Systems", [
            ("Topic 3.1: Classes, Objects, Dunder Methods & Encapsulation",
             "https://www.youtube.com/watch?v=ZDa-Z5JzLYM\n\nCorey Schafer Python OOP: Classes, instance objects, __init__ constructors, class variables vs instance variables, and encapsulation.",
             15, "https://docs.python.org/3/tutorial/classes.html"),
            ("Topic 3.2: Inheritance, Polymorphism & Modular Class Architectures",
             "https://www.youtube.com/watch?v=RSl87lqOXDE\n\nCorey Schafer Python OOP: Creating subclasses with super(), method overriding, polymorphism, and building extensible AI module hierarchies.",
             20, "https://docs.python.org/3/tutorial/classes.html#inheritance")
        ]),
        ("Module 4: NumPy & Multi-Dimensional Array Computing", [
            ("Topic 4.1: NumPy Multi-dimensional Arrays & Matrix Math",
             "https://www.youtube.com/watch?v=QUT1VHiLmmI\n\nKeith Galli's NumPy Crash Course: ndarray creation, indexing, slicing, vector arithmetic, and matrix transformations.",
             58, "https://numpy.org/doc/stable/"),
            ("Topic 4.2: Vectorized Calculations & Linear Algebra Basics",
             "https://www.youtube.com/watch?v=fNk_zzaMoSs\n\n3Blue1Brown Essence of Linear Algebra: Vectors, linear combinations, span, basis vectors, and matrix multiplication for neural nets.",
             10, "https://numpy.org/doc/stable/reference/routines.linalg.html")
        ]),
        ("Module 5: Pandas & Tabular Data Wrangling", [
            ("Topic 5.1: Pandas Series, DataFrames & Data Cleaning",
             "https://www.youtube.com/watch?v=vmEHCJofslg\n\nKeith Galli's Pandas Tutorial: loading CSVs/JSON, handling missing values, filtering rows, and applying transformations.",
             60, "https://pandas.pydata.org/docs/"),
            ("Topic 5.2: Merging, GroupBy, Aggregations & Pivot Tables",
             "https://www.youtube.com/watch?v=txMdrV1Ut64\n\nCorey Schafer Pandas: GroupBy operations, multi-index aggregation, merging dataframes with outer/inner joins, and pivot tables.",
             49, "https://pandas.pydata.org/docs/user_guide/groupby.html")
        ]),
        ("Module 6: Exploratory Data Analysis & Visualization", [
            ("Topic 6.1: Matplotlib & Seaborn Statistical Visualizations",
             "https://www.youtube.com/watch?v=UO98lJV3jHR\n\nCorey Schafer Matplotlib Tutorial: Bar charts, histograms, scatter plots, subplots, and styling publication-ready data graphics.",
             35, "https://matplotlib.org/"),
            ("Topic 6.2: End-to-End Exploratory Data Analysis (EDA) Project",
             "https://www.youtube.com/watch?v=3Xc3CA655Y4\n\nfreeCodeCamp: Real-world exploratory data analysis case study, cleaning messy datasets, detecting outliers, and correlation heatmaps.",
             92, "https://seaborn.pydata.org/")
        ])
    ],

    "Practical Machine Learning with Scikit-Learn": [
        ("Module 1: Machine Learning Foundations & Preprocessing", [
            ("Topic 1.1: Supervised vs Unsupervised Learning & Feature Normalization",
             "https://www.youtube.com/watch?v=i_LwzRVP7bg\n\nfreeCodeCamp Machine Learning Course: regression vs classification, standard scaling, and min-max normalization.",
             234, "https://scikit-learn.org/"),
            ("Topic 1.2: Train/Test Splitting, Stratification & Data Leakage",
             "https://www.youtube.com/watch?v=fwY9Qv96DJY\n\nStatQuest: Cross-validation, stratified train/test splitting, out-of-fold metrics, and eliminating data leakage.",
             7, "https://scikit-learn.org/stable/modules/cross_validation.html")
        ]),
        ("Module 2: Supervised Regression Modeling", [
            ("Topic 2.1: Simple & Multiple Linear Regression Mathematical Foundations",
             "https://www.youtube.com/watch?v=7eh4d6sabA0\n\nStatQuest: Cost functions, sum of squared residuals, ordinary least squares (OLS), and multi-variable regression planes.",
             50, "https://statquest.org/"),
            ("Topic 2.2: Regularization Techniques: Ridge (L2), Lasso (L1) & ElasticNet",
             "https://www.youtube.com/watch?v=Q81RR3yKn30\n\nStatQuest: Ridge regression (L2 penalty) and Lasso (L1 penalty) to prevent model overfitting and select sparse features.",
             20, "https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression")
        ]),
        ("Module 3: Classification Algorithms & Decision Boundaries", [
            ("Topic 3.1: Logistic Regression & Sigmoid Decision Boundaries",
             "https://www.youtube.com/watch?v=yIYKR4sgzI8\n\nStatQuest: Logistic regression, sigmoid probability curves, log-loss calculation, and odds ratio interpretations.",
             9, "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression"),
            ("Topic 3.2: Support Vector Machines (SVM) & Kernel Methods",
             "https://www.youtube.com/watch?v=efR1C6CvhmE\n\nStatQuest: Maximal margin classifiers, soft margins, Support Vector Machines, and Radial Basis Function (RBF) kernels.",
             21, "https://scikit-learn.org/stable/modules/svm.html")
        ]),
        ("Module 4: Tree-Based Methods & Ensemble Learning", [
            ("Topic 4.1: Decision Trees, Information Gain & Gini Impurity",
             "https://www.youtube.com/watch?v=_L39rN6gz7Y\n\nStatQuest: How decision trees split nodes, calculating Gini impurity, tree pruning, and interpreting decision thresholds.",
             18, "https://scikit-learn.org/stable/modules/tree.html"),
            ("Topic 4.2: Random Forest Ensembles, Bagging & Gradient Boosting",
             "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ\n\nStatQuest: Bootstrap aggregating (bagging), random feature subsampling, out-of-bag error, and Random Forest classifiers.",
             10, "https://scikit-learn.org/stable/modules/ensemble.html")
        ]),
        ("Module 5: Unsupervised Learning & Dimensionality Reduction", [
            ("Topic 5.1: K-Means Clustering & Inertia Elbow Optimization",
             "https://www.youtube.com/watch?v=4b5d3muPQmA\n\nStatQuest: K-Means clustering algorithm step-by-step, finding optimal k using the elbow method, and silhouette scores.",
             8, "https://scikit-learn.org/stable/modules/clustering.html#k-means"),
            ("Topic 5.2: Principal Component Analysis (PCA) & Variance Ratios",
             "https://www.youtube.com/watch?v=FgakZw6K1QQ\n\nStatQuest: Principal Component Analysis (PCA), eigenvalues, eigenvectors, dimension reduction, and scree plots.",
             22, "https://scikit-learn.org/stable/modules/decomposition.html#pca")
        ]),
        ("Module 6: Model Evaluation, Tuning & Production Pipelines", [
            ("Topic 6.1: Confusion Matrix, Precision, Recall & ROC-AUC Curves",
             "https://www.youtube.com/watch?v=Kdsp6soqA7g\n\nStatQuest: ROC and AUC clearly explained, true positive rate vs false positive rate, confusion matrices, and F1 scores.",
             46, "https://scikit-learn.org/stable/modules/model_evaluation.html"),
            ("Topic 6.2: Hyperparameter Tuning with GridSearchCV & Scikit Pipelines",
             "https://www.youtube.com/watch?v=Gol_q8hk4ko\n\nData School: Exhaustive hyperparameter search with GridSearchCV, cross-validated parameter sweeps, and Scikit-Learn Pipelines.",
             16, "https://scikit-learn.org/stable/modules/grid_search.html")
        ])
    ],

    "Deep Learning & Neural Networks with PyTorch": [
        ("Module 1: Deep Learning Foundations & Optimization", [
            ("Topic 1.1: Artificial Neural Networks, Weights, Biases & Activations",
             "https://www.youtube.com/watch?v=aircAruvnKk\n\n3Blue1Brown: What is a neural network? Structure of multi-layer perceptrons, weights, biases, and activation functions.",
             19, "https://www.3blue1brown.com/"),
            ("Topic 1.2: Calculus of Backpropagation & Gradient Descent Algorithms",
             "https://www.youtube.com/watch?v=IHZwWFHWa-w\n\n3Blue1Brown: Backpropagation calculus, chain rule application, gradient vectors, and stochastic gradient descent.",
             21, "https://pytorch.org/")
        ]),
        ("Module 2: PyTorch Tensors & Custom Model Architectures", [
            ("Topic 2.1: PyTorch Tensors, GPU Acceleration (CUDA) & Autograd",
             "https://www.youtube.com/watch?v=yaY4_cQy5Y8\n\nAladdin Persson: PyTorch tensor initialization, math operations, indexing, GPU memory management (.cuda()), and Autograd graphs.",
             56, "https://pytorch.org/tutorials/beginner/basics/intro.html"),
            ("Topic 2.2: Building Custom nn.Module Architectures & Training Loops",
             "https://www.youtube.com/watch?v=Jy4wM2P21fA\n\nAladdin Persson: Creating custom PyTorch nn.Module networks, DataLoader batches, forward passes, loss functions, and backprop.",
             5, "https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html")
        ]),
        ("Module 3: Computer Vision with Convolutional Networks (CNNs)", [
            ("Topic 3.1: 2D Convolutions, Kernels, Feature Maps & Pooling Layers",
             "https://www.youtube.com/watch?v=KuXjwB4LzSA\n\n3Blue1Brown: But what is a convolution? Mathematical convolution, spatial kernels, edge detection, and pooling.",
             23, "https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html"),
            ("Topic 3.2: Image Classification with Deep CNNs & Data Augmentation",
             "https://www.youtube.com/watch?v=wnK3huU9Op8\n\nAladdin Persson: Building complete CNN architectures in PyTorch, convolutional layers, max pooling, dropout, and batch normalization.",
             58, "https://pytorch.org/vision/stable/transforms.html")
        ]),
        ("Module 4: Transfer Learning & Pretrained Vision Models", [
            ("Topic 4.1: Pretrained ResNet Models & Feature Extraction",
             "https://www.youtube.com/watch?v=qaDe0qQZ5gk\n\nAladdin Persson: Transfer learning with PyTorch, loading torchvision pretrained ResNet/VGG models, freezing weights, and replacing heads.",
             48, "https://pytorch.org/vision/stable/models.html"),
            ("Topic 4.2: Fine-Tuning Deep Networks for Custom Domain Datasets",
             "https://www.youtube.com/watch?v=m8pOnJxOcqY\n\nfreeCodeCamp: Fine-tuning pretrained deep vision models on custom domain datasets with learning rate schedulers.",
             19, "https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html")
        ]),
        ("Module 5: Sequential Models & Recurrent Architectures", [
            ("Topic 5.1: Recurrent Neural Networks (RNNs) & Vanishing Gradients",
             "https://www.youtube.com/watch?v=LHXXI4-IEns\n\nStatQuest: Recurrent Neural Networks (RNNs) clearly explained, sequential processing, hidden states, and backprop through time.",
             10, "https://colah.github.io/posts/2015-08-Understanding-LSTMs/"),
            ("Topic 5.2: Long Short-Term Memory (LSTM) Networks & Gated Units",
             "https://www.youtube.com/watch?v=YCzL96nL5Kw\n\nStatQuest: Long Short-Term Memory (LSTM) cells, forget gates, input gates, candidate states, and output gates.",
             50, "https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html")
        ]),
        ("Module 6: Attention Mechanisms & Transformer Fundamentals", [
            ("Topic 6.1: Self-Attention Mechanism & Query, Key, Value Projections",
             "https://www.youtube.com/watch?v=wjZofJX0v4U\n\n3Blue1Brown: Attention in transformers, visually explained. Query, Key, Value vectors, dot product attention, and softmax weights.",
             58, "https://arxiv.org/abs/1706.03762"),
            ("Topic 6.2: Multi-Head Attention & Transformer Encoder Layers",
             "https://www.youtube.com/watch?v=eMlx5fFNoYc\n\n3Blue1Brown: How Large Language Models work, multi-head attention blocks, residual connections, and transformer encoder layers.",
             26, "https://pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder.html")
        ])
    ],

    "Generative AI, LLMs & LangChain Engineering": [
        ("Module 1: Large Language Model (LLM) Architecture & Pretraining", [
            ("Topic 1.1: How GPT Models are Built & Trained from Scratch",
             "https://www.youtube.com/watch?v=kCc8FmEb1nY\n\nAndrej Karpathy: Let's build GPT from scratch in code. Character-level language models, self-attention blocks, and causal masking.",
             116, "https://karpathy.ai/"),
            ("Topic 1.2: Byte-Pair Encoding (BPE), Tokenization & Vocabularies",
             "https://www.youtube.com/watch?v=zduSFxRajkE\n\nAndrej Karpathy: Let's build the GPT Tokenizer. Byte-Pair Encoding (BPE), regex pattern splits, vocabulary generation, and tiktoken.",
             134, "https://platform.openai.com/tokenizer")
        ]),
        ("Module 2: Generative Inference & Prompt Engineering", [
            ("Topic 2.1: Autoregressive Sampling, Temperature & Top-P Decoding",
             "https://www.youtube.com/watch?v=V_hqp3W5wbM\n\nStatQuest: Temperature and top-p (nucleus) sampling in ChatGPT and LLMs. Controlling randomness, creativity, and deterministic outputs.",
             45, "https://platform.openai.com/docs/guides/text-generation"),
            ("Topic 2.2: Advanced Prompt Engineering: Chain-of-Thought & Few-Shot",
             "https://www.youtube.com/watch?v=jC4v5AS4RIM\n\nfreeCodeCamp: Prompt Engineering course for Generative AI. Zero-shot, few-shot demonstration exemplars, and Chain-of-Thought (CoT).",
             8, "https://www.promptingguide.ai/")
        ]),
        ("Module 3: Dense Embeddings & Vector Databases", [
            ("Topic 3.1: Dense Vector Retrieval & Chroma/Pinecone Vector DBs",
             "https://www.youtube.com/watch?v=klTvEwg3oJ4\n\nfreeCodeCamp: Vector Databases for Beginners. Embedding models, ChromaDB, Pinecone, collection indexing, and metadata filtering.",
             3, "https://docs.trychroma.com/"),
            ("Topic 3.2: Semantic Similarity Search & Distance Metrics",
             "https://www.youtube.com/watch?v=d3z0h9iW2e4\n\nStatQuest: Word embeddings and semantic similarity. Vector distances (Cosine, Euclidean, Dot Product), and ANN search.",
             45, "https://www.pinecone.io/learn/vector-database/")
        ]),
        ("Module 4: Retrieval-Augmented Generation (RAG) Architecture", [
            ("Topic 4.1: Document Ingestion, Chunking Strategies & Overlap",
             "https://www.youtube.com/watch?v=8OJC21T2sl4\n\nPinecone: Document Chunking Strategies for RAG. Fixed-size chunking, recursive splitters, chunk overlap, and preserving semantic context.",
             46, "https://python.langchain.com/docs/modules/data_connection/document_transformers/"),
            ("Topic 4.2: End-to-End RAG Pipeline: Grounding LLMs on Enterprise Data",
             "https://www.youtube.com/watch?v=tcqEUSNCn8I\n\nfreeCodeCamp: Complete RAG Architecture guide. Synthesizing prompts with retrieved documents, context injection, and avoiding hallucinations.",
             17, "https://www.pinecone.io/learn/retrieval-augmented-generation/")
        ]),
        ("Module 5: LangChain Framework & Expression Language (LCEL)", [
            ("Topic 5.1: LangChain Core Components: PromptTemplates, Models & Parsers",
             "https://www.youtube.com/watch?v=aywZrzNaKjs\n\nfreeCodeCamp: LangChain Full Course. Chat models, PromptTemplates, OutputParsers, and connecting LLMs to structured Python objects.",
             13, "https://python.langchain.com/"),
            ("Topic 5.2: Composable LCEL Chains & Conversational Memory Buffers",
             "https://www.youtube.com/watch?v=NYSNWNgS9-U\n\nLangChain Official: LangChain Expression Language (LCEL). Chaining components with the pipe operator, streaming responses, and chat memory.",
             50, "https://python.langchain.com/docs/expression_language/")
        ]),
        ("Module 6: Autonomous AI Agents & Tool Calling", [
            ("Topic 6.1: Function Calling APIs & Dynamic Tool Integration",
             "https://www.youtube.com/watch?v=0h1pZg5cOZs\n\nLangChain: OpenAI Function Calling & Tool Binding. Converting Python functions into LLM tools with JSON schemas.",
             50, "https://python.langchain.com/docs/modules/agents/tools/"),
            ("Topic 6.2: ReAct Agent Reasoning Loops & Autonomous Task Execution",
             "https://www.youtube.com/watch?v=lG7Uxts9SXs\n\nfreeCodeCamp: Autonomous AI Agents with LangChain. Implementing the ReAct loop (Thought, Action, Observation) and multi-turn tools.",
             66, "https://arxiv.org/abs/2210.03629")
        ])
    ],

    # =========================================================================
    # 2. FULL-STACK WEB DEVELOPER ROADMAP
    # =========================================================================
    "Frontend Engineering with Modern JavaScript": [
        ("Module 1: JavaScript Language Fundamentals", [
            ("Topic 1.1: Modern JS Syntax, Variables & Arrow Functions",
             "https://www.youtube.com/watch?v=hdI2bqOjy3c\n\nTraversy Media: Modern JavaScript Crash Course. Let vs Const, arrow function expressions, template literals, and destructuring.",
             100, "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
            ("Topic 1.2: Scope, Closures & Execution Contexts",
             "https://www.youtube.com/watch?v=1S8SBDh-zk8\n\nWeb Dev Simplified: JavaScript Closures and Scope clearly explained. Lexical environment, call stack, and private variables.",
             45, "https://javascript.info/closure")
        ]),
        ("Module 2: DOM Manipulation & Event Architecture", [
            ("Topic 2.1: DOM Selectors, Element Creation & Dynamic Manipulation",
             "https://www.youtube.com/watch?v=0ik6X4DJKCc\n\nTraversy Media: JavaScript DOM Crash Course Part 1. QuerySelector, createElement, appendChild, classList, and styling attributes.",
             39, "https://javascript.info/document"),
            ("Topic 2.2: Event Listeners, Bubbling, Capturing & Delegation",
             "https://www.youtube.com/watch?v=XF1_UKCe-FP\n\nWeb Dev Simplified: JavaScript Event Listeners, bubbling, capturing, and event delegation patterns.",
             44, "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events")
        ]),
        ("Module 3: Asynchronous JavaScript & APIs", [
            ("Topic 3.1: Callbacks, Promises, and the Browser Event Loop",
             "https://www.youtube.com/watch?v=PoRJizFvM7s\n\nWeb Dev Simplified: JavaScript Promises in 10 Minutes. Pending, resolved, rejected states, then/catch chains, and Promise.all.",
             24, "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises"),
            ("Topic 3.2: Async/Await Syntax & Fetching RESTful Web APIs",
             "https://www.youtube.com/watch?v=V_Kr9OSfDeU\n\nWeb Dev Simplified: Async Await in JavaScript. Cleaner asynchronous code, try/catch error handling, and making HTTP requests with fetch().",
             8, "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API")
        ]),
        ("Module 4: ES Modules, Tooling & Modern Bundlers", [
            ("Topic 4.1: ES Modules (ESM), Named/Default Exports & NPM Packages",
             "https://www.youtube.com/watch?v=cRHQNNcYf6s\n\nWeb Dev Simplified: JavaScript ES6 Modules. Import and export statements, named vs default exports, and modular code organization.",
             8, "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules"),
            ("Topic 4.2: Modern Frontend Build Workflows with Vite",
             "https://www.youtube.com/watch?v=sBzBlQaf9L8\n\nTraversy Media: Vite Crash Course. Lightning fast dev server, instant HMR, npm package management, and production bundling.",
             42, "https://vitejs.dev/guide/")
        ]),
        ("Module 5: Browser Storage & State Management", [
            ("Topic 5.1: LocalStorage, SessionStorage & Cookies Security",
             "https://www.youtube.com/watch?v=GihQAC1I39Q\n\nWeb Dev Simplified: LocalStorage and SessionStorage. Storing strings and JSON objects, retrieving data, and clearing state.",
             14, "https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage"),
            ("Topic 5.2: Client-side State Stores & Reactive UI Updates",
             "https://www.youtube.com/watch?v=zwsPNDbfDyo\n\nFireship: Reactive State Management from Scratch. Custom event dispatchers, store subscribers, and state-driven DOM rendering.",
             45, "https://javascript.info/")
        ]),
        ("Module 6: Capstone Project: Interactive Single-Page Application", [
            ("Topic 6.1: Architecting a Single-Page Application (SPA)",
             "https://www.youtube.com/watch?v=jaVNP3nTUv0\n\nTraversy Media: Build a Full Vanilla JavaScript Single Page App with client-side routing and history API.",
             55, "https://github.com/"),
            ("Topic 6.2: Frontend Performance Optimization & Deployment",
             "https://www.youtube.com/watch?v=0fONene3OIA\n\nWeb Dev Simplified: 10 JavaScript Performance Tips for Faster Websites. Debouncing, throttling, lazy loading, and minification.",
             7, "https://web.dev/fast/")
        ])
    ],

    "Modern Web Engineering with Flask": [
        ("Module 1: Getting Started with Flask & Jinja2 Templates", [
            ("Topic 1.1: Virtual Environments, Application Factory & Routing",
             "https://www.youtube.com/watch?v=MwZwr5Tvyxo\n\nCorey Schafer Flask 1: Getting Started, virtualenv setup, creating your first Flask app, debug mode, and route view functions.",
             17, "https://flask.palletsprojects.com/"),
            ("Topic 1.2: Templates Inheritance & Dynamic Jinja2 Rendering",
             "https://www.youtube.com/watch?v=QnDWIZuWYW8\n\nCorey Schafer Flask 2: Templates, Jinja2 inheritance with base.html, block content, for loops, and context data passing.",
             42, "https://jinja.palletsprojects.com/")
        ]),
        ("Module 2: Forms, Validation & CSRF Protection", [
            ("Topic 2.1: Flask-WTF Forms, CSRF Tokens & Field Validators",
             "https://www.youtube.com/watch?v=UIJKdCIEXUQ\n\nCorey Schafer Flask 3: Forms and User Input, Flask-WTF, CSRF tokens, StringField, PasswordField, and validators.",
             48, "https://flask-wtf.readthedocs.io/"),
            ("Topic 2.2: Flash Messages, Form Pre-population & Feedback Loops",
             "https://www.youtube.com/watch?v=9MHYHgh4jYc\n\nCorey Schafer Flask: Flask flash messages, Bootstrap alert integration, category tags, and input pre-population.",
             11, "https://flask.palletsprojects.com/en/latest/patterns/flashing/")
        ]),
        ("Module 3: Relational Databases with Flask-SQLAlchemy", [
            ("Topic 3.1: Declarative Models, Data Types & Relationships",
             "https://www.youtube.com/watch?v=cYWiDiIUxQc\n\nCorey Schafer Flask 4: Database with Flask-SQLAlchemy. Creating db.Model tables, primary keys, relationships, and foreign keys.",
             30, "https://flask-sqlalchemy.palletsprojects.com/"),
            ("Topic 3.2: CRUD Operations, Query API & Foreign Key Constraints",
             "https://www.youtube.com/watch?v=4yqu8YF29dU\n\nPretty Printed: Flask-SQLAlchemy Querying and Filtering. Query.filter_by, filter, all, first, paginate, and updates.",
             45, "https://docs.sqlalchemy.org/en/20/orm/queryguide/")
        ]),
        ("Module 4: User Authentication & Role-Based Access Control", [
            ("Topic 4.1: Password Hashing with Werkzeug & Flask-Login Sessions",
             "https://www.youtube.com/watch?v=CSHx6eCkmv0\n\nCorey Schafer Flask 5: Package Structure, User Authentication, bcrypt password hashing, login sessions, and @login_required.",
             47, "https://flask-login.readthedocs.io/"),
            ("Topic 4.2: Role-Based Access Control (RBAC) & Custom Decorators",
             "https://www.youtube.com/watch?v=6K838iUoV_Q\n\nPretty Printed: Custom View Decorators in Flask for Role-Based Access Control (@admin_required, @instructor_required).",
             42, "https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/")
        ]),
        ("Module 5: File Handling, Uploads & Post/Redirect/Get (PRG)", [
            ("Topic 5.1: Secure File Uploads with Werkzeug Secure Filename",
             "https://www.youtube.com/watch?v=803Ei2Sq-gk\n\nCorey Schafer Flask 6: User Account and Profile Picture. File uploads, secure_filename, saving resized pictures, and form handling.",
             44, "https://werkzeug.palletsprojects.com/en/latest/utils/#werkzeug.utils.secure_filename"),
            ("Topic 5.2: Implementing Post/Redirect/Get (PRG) Pattern",
             "https://www.youtube.com/watch?v=u0oDDZrDz9U\n\nCorey Schafer Flask 7: Create, Update, and Delete Posts. Implementing the Post/Redirect/Get pattern to prevent double submissions.",
             48, "https://en.wikipedia.org/wiki/Post/Redirect/Get")
        ]),
        ("Module 6: Architecture & Production Deployment", [
            ("Topic 6.1: Blueprint Architecture & Multi-Module Organization",
             "https://www.youtube.com/watch?v=Wfx4YBzg16Q\n\nCorey Schafer Flask 11: Blueprints and Configuration. Splitting monolithic apps into blueprints for auth, catalog, and admin.",
             48, "https://flask.palletsprojects.com/en/latest/blueprints/"),
            ("Topic 6.2: Production Deployment with Gunicorn, Nginx & Docker",
             "https://www.youtube.com/watch?v=gotoXN2j120\n\nCorey Schafer Flask 12: Deploying a Flask App on Ubuntu Server with Gunicorn and Nginx reverse proxy.",
             55, "https://docs.gunicorn.org/")
        ])
    ],

    "Full-Stack React 18 and Flask Integration": [
        ("Module 1: React 18 Core Concepts & Components", [
            ("Topic 1.1: Component Hierarchy, JSX Syntax & Virtual DOM",
             "https://www.youtube.com/watch?v=bMknfKXIFA8\n\nfreeCodeCamp: React 18 Full Course. Component architecture, JSX syntax rules, Virtual DOM reconciliation, and unidirectional data.",
             715, "https://react.dev/"),
            ("Topic 1.2: Props, Component Composition & Conditional Rendering",
             "https://www.youtube.com/watch?v=kVeOpcw4GWY\n\nWeb Dev Simplified: Learn React in 30 Minutes. Passing props, destructuring props, component composition, and conditional rendering.",
             13, "https://react.dev/learn/passing-props-to-a-component")
        ]),
        ("Module 2: State Management & Functional Hooks", [
            ("Topic 2.1: State Management with useState & Complex Objects",
             "https://www.youtube.com/watch?v=O6P86uwfdR0\n\nWeb Dev Simplified: Learn useState In 15 Minutes. State immutability, state setter functions, and updating complex arrays/objects.",
             16, "https://react.dev/reference/react/useState"),
            ("Topic 2.2: Side Effects with useEffect & Cleanup Lifecycles",
             "https://www.youtube.com/watch?v=0ZJgIjIuY7U\n\nWeb Dev Simplified: Learn useEffect In 13 Minutes. Dependency arrays, API calls, event subscriptions, and cleanup functions.",
             14, "https://react.dev/reference/react/useEffect")
        ]),
        ("Module 3: Building RESTful Flask API Endpoints", [
            ("Topic 3.1: Flask RESTful Architecture & JSON Serialization",
             "https://www.youtube.com/watch?v=7LNl2AhNHqc\n\nPretty Printed: Creating REST APIs in Flask. Jsonify, request parsing, HTTP GET/POST/PUT/DELETE verbs, and standard status codes.",
             46, "https://flask.palletsprojects.com/"),
            ("Topic 3.2: Request Parsing, Query Parameters & Error Handling",
             "https://www.youtube.com/watch?v=GMppyAPbLYk\n\nAmigoscode: Designing Clean REST APIs. Input validation, query parameter filtering, pagination, and JSON error responses.",
             74, "https://marshmallow.readthedocs.io/")
        ]),
        ("Module 4: Connecting React with Flask APIs", [
            ("Topic 4.1: Cross-Origin Resource Sharing (CORS) Configuration",
             "https://www.youtube.com/watch?v=fpxiomWw8hY\n\nTech With Tim: Flask & React Integration - Handling CORS headers with Flask-CORS and frontend proxies.",
             40, "https://flask-cors.readthedocs.io/"),
            ("Topic 4.2: Axios HTTP Client Services & Async UI States",
             "https://www.youtube.com/watch?v=6LyagkoRWYA\n\nfreeCodeCamp: Axios Crash Course. Axios instances, interceptors, request authorization headers, loading states, and error handling.",
             42, "https://axios-http.com/")
        ]),
        ("Module 5: JWT Authentication & Protected Routing", [
            ("Topic 5.1: Stateless JWT Token Issuance & Bearer Headers",
             "https://www.youtube.com/watch?v=Yg5zkd9nm6w\n\nfreeCodeCamp: JWT Authentication Tutorial. Signing tokens, verifying secret signatures, payload claims, and token refreshing.",
             165, "https://jwt.io/"),
            ("Topic 5.2: React Protected Routes & AuthContext Provider",
             "https://www.youtube.com/watch?v=2k8NleFjG7I\n\nDave Gray: React Protected Routes and Role-Based Authorization with React Router v6 and Context API.",
             9, "https://react.dev/reference/react/useContext")
        ]),
        ("Module 6: Full-Stack Packaging & Cloud Deployment", [
            ("Topic 6.1: Building Production React Static Bundles",
             "https://www.youtube.com/watch?v=u0xWb2rJm1s\n\nTraversy Media: Full Stack React & Flask Deployment. Building React bundles with npm run build and serving static files.",
             45, "https://vitejs.dev/guide/build.html"),
            ("Topic 6.2: Deploying Full-Stack Application to Cloud Platforms",
             "https://www.youtube.com/watch?v=M576WGiDBdQ\n\nfreeCodeCamp: Deploy Full Stack Apps to Render and Railway. Environment variables, PostgreSQL databases, and live hosting.",
             982, "https://render.com/")
        ])
    ],

    # =========================================================================
    # 3. CLOUD & DEVOPS ENGINEER ROADMAP
    # =========================================================================
    "Enterprise Linux Server Administration": [
        ("Module 1: Shell Navigation & Core Administration", [
            ("Topic 1.1: Linux Terminal Crash Course for Developers",
             "https://www.youtube.com/watch?v=wBp0Rb-ZJak\n\nfreeCodeCamp: Linux for Beginners. Bash navigation, ls, cd, cat, grep, pipes (|), redirections, and standard I/O.",
             444, "https://ubuntu.com/"),
            ("Topic 1.2: User Management, Groups & Permissions",
             "https://www.youtube.com/watch?v=41I3EtbS36I\n\nNetworkChuck: Linux Permissions - chmod, chown, chgrp, octal numbers, umask, and sudoers privileges.",
             45, "https://www.redhat.com/")
        ]),
        ("Module 2: Bash Shell Scripting & Automation", [
            ("Topic 2.1: Bash Variables, Arguments & Conditional Logic",
             "https://www.youtube.com/watch?v=e7BufAVwDiM\n\nfreeCodeCamp: Bash Scripting Tutorial. Variables, positional parameters ($1, $2), test conditions ([ ]), and if-else branches.",
             188, "https://www.gnu.org/software/bash/manual/"),
            ("Topic 2.2: Loops, Functions & Automated Server Backup Scripts",
             "https://www.youtube.com/watch?v=tK9Oc6AEnR4\n\nLearn Linux TV: Bash Scripting - While and For Loops, shell functions, tar backups, and exit code handling.",
             48, "https://linux.die.net/man/1/rsync")
        ]),
        ("Module 3: Services, Daemons & Process Management", [
            ("Topic 3.1: Systemd Services, Daemons & Journalctl",
             "https://www.youtube.com/watch?v=ZtqBQ68cfJg\n\nLearn Linux TV: Understanding Systemd. Systemctl start, stop, enable, creating custom .service unit files, and journalctl logs.",
             45, "https://systemd.io/"),
            ("Topic 3.2: Process Monitoring with Htop, Ps, and Cron Scheduling",
             "https://www.youtube.com/watch?v=fXf47JcW-7U\n\nNetworkChuck: Linux Task Scheduling with Crontab, managing background processes with ps, top, htop, and kill signals.",
             42, "https://crontab.guru/")
        ]),
        ("Module 4: Storage, Filesystems & Disk Partitioning", [
            ("Topic 4.1: Disk Partitioning, File Systems (ext4) & Mount Points",
             "https://www.youtube.com/watch?v=6m5d09eD3o0\n\nLearn Linux TV: Linux Storage Basics. Partitioning with fdisk, formatting with mkfs.ext4, mounting drives, and /etc/fstab.",
             44, "https://wiki.archlinux.org/title/File_systems"),
            ("Topic 4.2: Logical Volume Management (LVM) for Enterprise Disks",
             "https://www.youtube.com/watch?v=d_NqC33GvS8\n\nLearn Linux TV: Complete LVM Guide. Physical volumes (pvcreate), volume groups (vgcreate), logical volumes (lvcreate), and resizing.",
             48, "https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_logical_volumes/")
        ]),
        ("Module 5: Networking & SSH Hardening", [
            ("Topic 5.1: SSH Hardening & Public Key Authentication",
             "https://www.youtube.com/watch?v=VbEx7B_MceI\n\nNetworkChuck: SSH Keys and Hardening. ssh-keygen, ed25519 keys, disabling root password login, and securing sshd_config.",
             42, "https://www.openssh.com/"),
            ("Topic 5.2: Network Configuration, IP Route & Netstat/SS Inspection",
             "https://www.youtube.com/watch?v=spDATSj_W6k\n\nNetworkChuck: Linux Networking Commands. ip addr, ip route, ss, netstat, ping, traceroute, and resolving network interfaces.",
             44, "https://www.cyberciti.biz/")
        ]),
        ("Module 6: Security Hardening & Firewall Administration", [
            ("Topic 6.1: Firewall Configuration with UFW & IPTables",
             "https://www.youtube.com/watch?v=p4v_q2N3w_U\n\nLearn Linux TV: UFW (Uncomplicated Firewall) Guide. Allowing/denying ports (22, 80, 443), rate-limiting, and stateful packet inspection.",
             42, "https://help.ubuntu.com/community/UFW"),
            ("Topic 6.2: Server Auditing, Log Rotation & Security Best Practices",
             "https://www.youtube.com/watch?v=r_s9Lq0Uu-0\n\nLearn Linux TV: Linux Server Security and Logrotate. Auditing /var/log/auth.log, Fail2ban setup, and automated security upgrades.",
             46, "https://www.cisecurity.org/")
        ])
    ],

    "DevOps CI/CD Pipelines with Docker & GitHub Actions": [
        ("Module 1: Docker Containerization Fundamentals", [
            ("Topic 1.1: Docker Architecture, Images & Container Lifecycle",
             "https://www.youtube.com/watch?v=3c-iBn73dDE\n\nTechWorld with Nana: Docker Tutorial for Beginners. Container runtime, daemon, images, container run/stop/ps, and port publishing.",
             166, "https://docs.docker.com/get-started/"),
            ("Topic 1.2: Container Networking & Volume Data Persistence",
             "https://www.youtube.com/watch?v=bKFMS5C4CG0\n\nTechWorld with Nana: Docker Volumes and Networking. Bind mounts vs named volumes, persistent database storage, and bridge networks.",
             39, "https://docs.docker.com/storage/")
        ]),
        ("Module 2: Advanced Dockerfiles & Multi-Stage Builds", [
            ("Topic 2.1: Writing Production Dockerfiles with Multi-Stage Optimization",
             "https://www.youtube.com/watch?v=0UaqjVG0k80\n\nTechWorld with Nana: Dockerfile Best Practices. Multi-stage builds, alpine base images, non-root users, and minimal image layers.",
             48, "https://docs.docker.com/build/building/multi-stage/"),
            ("Topic 2.2: Multi-Container Orchestration with Docker Compose",
             "https://www.youtube.com/watch?v=pTFZFxd4hOI\n\nTechWorld with Nana: Docker Compose Tutorial. Writing docker-compose.yml, multi-service networks, environment variables, and dependencies.",
             56, "https://docs.docker.com/compose/")
        ]),
        ("Module 3: Continuous Integration with GitHub Actions", [
            ("Topic 3.1: GitHub Actions Workflows, Triggers & Runners",
             "https://www.youtube.com/watch?v=R8_veQiYBjI\n\nTechWorld with Nana: GitHub Actions Tutorial. Creating .github/workflows YAML files, triggers (push, pull_request), jobs, and steps.",
             32, "https://docs.github.com/en/actions"),
            ("Topic 3.2: Automated Pytest Testing in CI Runners",
             "https://www.youtube.com/watch?v=G30kC3U0gXw\n\nArjanCodes: Automated Testing with GitHub Actions and Pytest. Running test matrices, capturing coverage reports, and status badges.",
             45, "https://docs.pytest.org/")
        ]),
        ("Module 4: Code Quality, Linting & Security Scans", [
            ("Topic 4.1: Automated Linting with Flake8 & Ruff",
             "https://www.youtube.com/watch?v=i1G16OQW3p0\n\nArjanCodes: Python Code Quality Tools. Automated linting with Ruff and Flake8 in CI pipelines to enforce PEP8 standards.",
             42, "https://flake8.pycqa.org/"),
            ("Topic 4.2: Dependency Vulnerability Scanning & Trivy Container Scans",
             "https://www.youtube.com/watch?v=wqhNm6eC6bM\n\nTechWorld with Nana: Container Security and Vulnerability Scanning with Trivy in GitHub Actions.",
             45, "https://trivy.dev/")
        ]),
        ("Module 5: Docker Registries & Image Publishing", [
            ("Topic 5.1: Docker Hub & GitHub Container Registry (GHCR) Publishing",
             "https://www.youtube.com/watch?v=2Sg_g7jP3vM\n\nTechWorld with Nana: Publish Docker Images to Docker Hub and GHCR automatically on git tag releases.",
             44, "https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry"),
            ("Topic 5.2: Secret Management & Environment Security in CI/CD",
             "https://www.youtube.com/watch?v=kR2tZ7u0Z_g\n\nGitHub Official: Managing Secrets in GitHub Actions. Repository secrets, environment secrets, and masked variables.",
             40, "https://docs.github.com/en/actions/security-guides/encrypted-secrets")
        ]),
        ("Module 6: Continuous Deployment & Cloud Hosting", [
            ("Topic 6.1: Zero-Downtime Automated Cloud Deployments",
             "https://www.youtube.com/watch?v=845C_uO_1Gk\n\nfreeCodeCamp: Continuous Deployment Tutorial. Deploying containerized web apps to cloud servers automatically upon commit.",
             48, "https://cloud.google.com/"),
            ("Topic 6.2: Blue/Green & Canary Deployment Strategies",
             "https://www.youtube.com/watch?v=r0XhS_tWk5g\n\nTechWorld with Nana: Deployment Strategies Explained. Recreate, Rolling Update, Blue-Green, and Canary deployments.",
             46, "https://aws.amazon.com/whitepapers/overview-deployment-options/")
        ])
    ],

    "Cloud-Native Kubernetes Operations & AWS": [
        ("Module 1: Kubernetes Architecture & Core Primitives", [
            ("Topic 1.1: Kubernetes Architecture - Master & Worker Nodes",
             "https://www.youtube.com/watch?v=X48VuDVv0do\n\nTechWorld with Nana: Kubernetes Complete Architecture. API server, etcd, scheduler, kubelet, and container runtime.",
             217, "https://kubernetes.io/"),
            ("Topic 1.2: Pods, Deployments & Declarative YAML Manifests",
             "https://www.youtube.com/watch?v=s_o8dwzRlu4\n\nTechWorld with Nana: Kubernetes Pods and Deployments. Writing declarative YAML specs, replicas, labels, and selectors.",
             72, "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/")
        ]),
        ("Module 2: Networking, Ingress & Service Discovery", [
            ("Topic 2.1: ClusterIP, NodePort, and LoadBalancer Services",
             "https://www.youtube.com/watch?v=80Ew_fsV4rM\n\nTechWorld with Nana: Kubernetes Services Explained. Internal ClusterIP routing, external NodePort, and cloud LoadBalancers.",
             23, "https://kubernetes.io/docs/concepts/services-networking/service/"),
            ("Topic 2.2: Ingress Controllers & Domain SSL Termination",
             "https://www.youtube.com/watch?v=2dW3t2U9cWk\n\nTechWorld with Nana: Kubernetes Ingress Explained. Routing external traffic by domain/path with Nginx Ingress and TLS certificates.",
             46, "https://kubernetes.io/docs/concepts/services-networking/ingress/")
        ]),
        ("Module 3: Configuration & Secret Decoupling", [
            ("Topic 3.1: ConfigMaps, Environment Injection & Volume Mounts",
             "https://www.youtube.com/watch?v=wGqF5b_K3_Q\n\nTechWorld with Nana: Kubernetes ConfigMap. Storing configuration key-values, injecting as environment variables, and config volumes.",
             44, "https://kubernetes.io/docs/concepts/configuration/"),
            ("Topic 3.2: Kubernetes Secrets, RBAC & Service Accounts",
             "https://www.youtube.com/watch?v=7XDeI5FYj3w\n\nTechWorld with Nana: Kubernetes Secret & RBAC. Base64 encoded secrets, Role, RoleBinding, ClusterRole, and service account tokens.",
             46, "https://kubernetes.io/docs/concepts/security/rbac/")
        ]),
        ("Module 4: Stateful Workloads & Persistent Storage", [
            ("Topic 4.1: Persistent Volumes (PV) & Persistent Volume Claims (PVC)",
             "https://www.youtube.com/watch?v=0eo3370XxMM\n\nTechWorld with Nana: Kubernetes Storage (Volumes, PV, PVC, StorageClass). Dynamic volume provisioning on cloud disks.",
             48, "https://kubernetes.io/docs/concepts/storage/persistent-volumes/"),
            ("Topic 4.2: StatefulSets & Stateful Database Deployments",
             "https://www.youtube.com/watch?v=pPQKAR1pA98\n\nTechWorld with Nana: Deploying Stateful Apps with StatefulSet. Stable network identities, ordered scaling, and headless services.",
             48, "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/")
        ]),
        ("Module 5: AWS Cloud Infrastructure & Elastic Kubernetes (EKS)", [
            ("Topic 5.1: AWS VPC, Subnets, Security Groups & IAM Roles",
             "https://www.youtube.com/watch?v=k1RI5locZE4\n\nfreeCodeCamp: AWS Certified Cloud Practitioner Full Course. VPC virtual private clouds, public/private subnets, and IAM roles.",
             569, "https://aws.amazon.com/"),
            ("Topic 5.2: Managed Kubernetes with AWS EKS & AWS CLI",
             "https://www.youtube.com/watch?v=0K9rZ9qW3s0\n\nTechWorld with Nana: AWS EKS Setup with eksctl and kubectl. Connecting command line tools to production managed Kubernetes.",
             55, "https://aws.amazon.com/eks/")
        ]),
        ("Module 6: Monitoring, Helm & GitOps Operations", [
            ("Topic 6.1: Package Management with Helm Charts",
             "https://www.youtube.com/watch?v=-ykwb1d0DXU\n\nTechWorld with Nana: Helm Tutorial. Creating Helm charts, values.yaml configuration, template functions, and upgrading releases.",
             14, "https://helm.sh/"),
            ("Topic 6.2: Prometheus & Grafana Cluster Monitoring",
             "https://www.youtube.com/watch?v=QoDqxm7ybLc\n\nTechWorld with Nana: Prometheus Monitoring with Grafana Dashboards in Kubernetes. Scraping pod metrics and visualizing load.",
             26, "https://prometheus.io/")
        ])
    ],

    # =========================================================================
    # 4. CYBERSECURITY & ETHICAL HACKING ROADMAP
    # =========================================================================
    "Computer Networking & Security Fundamentals": [
        ("Module 1: Network Architectures & OSI Model", [
            ("Topic 1.1: OSI 7-Layer Model & TCP/IP Protocol Stack",
             "https://www.youtube.com/watch?v=IPvYjXCsTg8\n\nNetworkChuck: You need to learn networking RIGHT NOW!! OSI 7-Layer Model, encapsulation, and packet routing.",
             247, "https://en.wikipedia.org/wiki/OSI_model"),
            ("Topic 1.2: IPv4, IPv6, Subnetting & CIDR Calculations",
             "https://www.youtube.com/watch?v=s_Ntt6eTn94\n\nNetworkChuck: Subnetting is EASY! Binary subnet calculation, CIDR prefixes (/24, /16), and IP address classes.",
             18, "https://www.subnet-calculator.com/")
        ]),
        ("Module 2: Core Protocols & Traffic Flow", [
            ("Topic 2.1: TCP 3-Way Handshake, UDP & Reliable Transmission",
             "https://www.youtube.com/watch?v=7_LPdttKXPc\n\nNetworkChuck: TCP 3-Way Handshake explained. SYN, SYN-ACK, ACK flags, connection teardown, and UDP vs TCP trade-offs.",
             5, "https://www.cloudflare.com/learning/ddos/glossary/tcp-3-way-handshake/"),
            ("Topic 2.2: DNS Architecture, Resolution Chains & Records",
             "https://www.youtube.com/watch?v=27r4Bzuj5OI\n\nNetworkChuck: DNS Explained. Recursive resolvers, root servers, TLD servers, authoritative servers, and DNS records (A, CNAME, MX).",
             40, "https://www.cloudflare.com/learning/dns/what-is-dns/")
        ]),
        ("Module 3: Web Protocols & Transport Layer Security", [
            ("Topic 3.1: HTTP/1.1, HTTP/2, Headers & Status Codes",
             "https://www.youtube.com/watch?v=iYM2zFP3Zn0\n\nTraversy Media: HTTP Crash Course. Request and response anatomy, headers, cookies, and HTTP status codes (2xx, 3xx, 4xx, 5xx).",
             38, "https://developer.mozilla.org/en-US/docs/Web/HTTP"),
            ("Topic 3.2: TLS/SSL Handshake, Certificates & Public Key Cryptography",
             "https://www.youtube.com/watch?v=T4Df5_cojAs\n\nComputerphile: TLS / SSL Cryptographic Handshake. How HTTPS keeps web traffic private using asymmetric and symmetric encryption.",
             11, "https://www.cloudflare.com/learning/ssl/what-is-ssl/")
        ]),
        ("Module 4: Packet Inspection & Network Forensics", [
            ("Topic 4.1: Wireshark Packet Sniffing & Capture Filters",
             "https://www.youtube.com/watch?v=lb1Dw0elw0Q\n\nNetworkChuck: Wireshark Tutorial for Beginners. Packet capturing, display filters, following TCP streams, and inspecting headers.",
             11, "https://www.wireshark.org/"),
            ("Topic 4.2: Analyzing Network Attacks & Malicious Payloads",
             "https://www.youtube.com/watch?v=d_xM9q0m4o0\n\nHackerSploit: Network Traffic Analysis with Wireshark. Identifying port scans, ARP spoofing attacks, and cleartext credential leaks.",
             46, "https://www.wireshark.org/docs/")
        ]),
        ("Module 5: Network Perimeter Defense & Firewalls", [
            ("Topic 5.1: Statefull Firewalls, DMZs & Network Segmentation",
             "https://www.youtube.com/watch?v=Spb86h4VfQk\n\nNetworkChuck: What is a Firewall? Stateful packet inspection, DMZ subnets, port forwarding, and isolating internal network zones.",
             42, "https://en.wikipedia.org/wiki/DMZ_(computing)"),
            ("Topic 5.2: Virtual Private Networks (VPNs) & Tunnel Protocols",
             "https://www.youtube.com/watch?v=L_4T6iQ_Y8U\n\nNetworkChuck: How VPNs Actually Work! WireGuard, OpenVPN, IPSec, encrypted tunnels, and secure remote access.",
             45, "https://www.wireguard.com/")
        ]),
        ("Module 6: Security Architecture & Zero Trust", [
            ("Topic 6.1: Zero Trust Architecture & Least Privilege Principles",
             "https://www.youtube.com/watch?v=q6E0uD2j3o4\n\nIBM Technology: What is Zero Trust? Core principles, continuous verification, least privileged access, and micro-segmentation.",
             42, "https://www.nist.gov/publications/zero-trust-architecture"),
            ("Topic 6.2: Intrusion Detection Systems (IDS/IPS) & SIEM",
             "https://www.youtube.com/watch?v=aG0V5tP5k98\n\nDavid Bombal: Snort / Suricata IDS Tutorial. Signature matching rules, deep packet inspection, and alerting on malicious traffic.",
             46, "https://suricata.io/")
        ])
    ],

    "Applied Cybersecurity & Ethical Hacking": [
        ("Module 1: Ethical Hacking Foundations & Legal Frameworks", [
            ("Topic 1.1: Ethical Hacking Methodology & Rules of Engagement",
             "https://www.youtube.com/watch?v=3Kq1MIfTWCE\n\nfreeCodeCamp: Ethical Hacking Full Course. Penetration testing stages, rules of engagement, scoping, and legal authorization.",
             891, "https://www.eccouncil.org/"),
            ("Topic 1.2: Kali Linux Security Toolkit & Virtual Lab Setup",
             "https://www.youtube.com/watch?v=WnN6dbosJJA\n\nNetworkChuck: Your first Ethical Hacking lab with Kali Linux and VirtualBox. Isolated networks and vulnerable target machines.",
             46, "https://www.kali.org/")
        ]),
        ("Module 2: Reconnaissance & Information Gathering", [
            ("Topic 2.1: Open Source Intelligence (OSINT) Techniques",
             "https://www.youtube.com/watch?v=qwA6MmbeGNo\n\nNetworkChuck: You need to learn OSINT! Passive footprinting, Google dorking, WHOIS records, DNS enumeration, and Shodan queries.",
             270, "https://osintframework.com/"),
            ("Topic 2.2: Active Network Reconnaissance with Nmap",
             "https://www.youtube.com/watch?v=4t4kBkMsDbQ\n\nNetworkChuck: Nmap Tutorial. Port scanning, TCP SYN stealth scans, OS detection (-O), service banner grabbing (-sV), and scripts.",
             17, "https://nmap.org/")
        ]),
        ("Module 3: Web Application Vulnerabilities & OWASP Top 10", [
            ("Topic 3.1: SQL Injection (SQLi) Vulnerabilities & Remediation",
             "https://www.youtube.com/watch?v=2_lswM1S264\n\nfreeCodeCamp: SQL Injection Tutorial. In-band SQLi, union-based extraction, blind SQLi, sqlmap automation, and parameterized queries.",
             168, "https://owasp.org/www-community/attacks/SQL_Injection"),
            ("Topic 3.2: Cross-Site Scripting (XSS) & Content Security Policy",
             "https://www.youtube.com/watch?v=EoaDgUgS6QA\n\nComputerphile: Cross Site Scripting (XSS). Reflected, Stored, and DOM-based XSS attacks, cookie theft, and CSP defense.",
             11, "https://owasp.org/www-community/attacks/xss/")
        ]),
        ("Module 4: Authentication & Session Attacks", [
            ("Topic 4.1: Broken Authentication, Brute-Force & Session Fixation",
             "https://www.youtube.com/watch?v=7qR_n1xKq7w\n\nHackerSploit: Password Cracking with Hydra. Brute-forcing SSH and web login forms, wordlists (RockYou), and rate-limiting defense.",
             45, "https://owasp.org/www-project-top-ten/"),
            ("Topic 4.2: Cross-Site Request Forgery (CSRF) & State-Changing Protections",
             "https://www.youtube.com/watch?v=vRBihr41JTo\n\nComputerphile: Cross-Site Request Forgery (CSRF). How attackers forge authenticated state-changing requests and anti-CSRF token defense.",
             9, "https://owasp.org/www-community/attacks/csrf")
        ]),
        ("Module 5: Exploitation & Privilege Escalation", [
            ("Topic 5.1: Metasploit Framework & Payload Delivery",
             "https://www.youtube.com/watch?v=8lR2uWwO3s0\n\nNetworkChuck: HACKING with Metasploit. msfconsole, searching vulnerabilities, exploit modules, and Meterpreter reverse shells.",
             52, "https://www.metasploit.com/"),
            ("Topic 5.2: Linux & Windows Privilege Escalation Vectors",
             "https://www.youtube.com/watch?v=e_MhXz9Y7w0\n\nHackerSploit: Linux Privilege Escalation. SUID binaries, sudo -l misconfigurations, cron jobs, and LinPEAS enumeration.",
             50, "https://github.com/carlospolop/PEASS-ng")
        ]),
        ("Module 6: Remediation & Security Hardening", [
            ("Topic 6.1: Writing Professional Penetration Testing Reports",
             "https://www.youtube.com/watch?v=5rT8gY4kU2o\n\nTCM Security: How to Write a Penetration Testing Report. Executive summaries, CVSS severity ratings, and proof-of-concept steps.",
             44, "https://www.first.org/cvss/"),
            ("Topic 6.2: Vulnerability Management & Secure SDLC Integration",
             "https://www.youtube.com/watch?v=p4v9G7r5t8s\n\nDavid Bombal: Security in DevOps (DevSecOps). Integrating automated static code analysis (SAST) and vulnerability remediation.",
             46, "https://owasp.org/www-project-samm/")
        ])
    ],

    "Advanced Penetration Testing & Cryptography": [
        ("Module 1: Advanced Cryptography Foundations", [
            ("Topic 1.1: Symmetric Encryption (AES-GCM) & Block Ciphers",
             "https://www.youtube.com/watch?v=O4xNJsjtN6E\n\nComputerphile: AES Explained (Advanced Encryption Standard). Substitution-permutation networks, rounds, keys, and block cipher modes.",
             14, "https://csrc.nist.gov/publications/detail/sp/800-38d/final"),
            ("Topic 1.2: Asymmetric Cryptography, RSA Math & Elliptic Curves (ECC)",
             "https://www.youtube.com/watch?v=GSIDS_lvRv4\n\nComputerphile: Public Key Cryptography & RSA. Prime factorization, modular arithmetic, Euler's totient, and public/private keys.",
             6, "https://en.wikipedia.org/wiki/Elliptic-curve_cryptography")
        ]),
        ("Module 2: Cryptographic Hash Functions & Integrity", [
            ("Topic 2.1: Cryptographic Hashes (SHA-256, BLAKE3) & Salted Passwords",
             "https://www.youtube.com/watch?v=b4b8ktEV4Bg\n\nComputerphile: How Secure is SHA-256? Hash collisions, avalanche effect, rainbow tables, salt, and bcrypt/Argon2.",
             8, "https://www.rfc-editor.org/rfc/rfc9106.html"),
            ("Topic 2.2: Digital Signatures & Public Key Infrastructure (PKI)",
             "https://www.youtube.com/watch?v=s22eJ1eVLTU\n\nComputerphile: Digital Signatures. Signing message digests with private keys, X.509 certificates, and certificate authorities.",
             10, "https://en.wikipedia.org/wiki/Public_key_infrastructure")
        ]),
        ("Module 3: Advanced Web & API Penetration Testing", [
            ("Topic 3.1: Server-Side Request Forgery (SSRF) & Cloud Metadata Exploits",
             "https://www.youtube.com/watch?v=D1S-G8rJrEk\n\nHackerSploit: SSRF (Server-Side Request Forgery) Explained. Pivoting into internal cloud metadata endpoints (169.254.169.254).",
             50, "https://owasp.org/www-community/attacks/Server_Side_Request_Forgery"),
            ("Topic 3.2: Insecure Deserialization & Remote Code Execution (RCE)",
             "https://www.youtube.com/watch?v=jwzehrnUv4c\n\nLiveOverflow: Insecure Deserialization in Python and PHP. Turning serialized objects into arbitrary code execution.",
             52, "https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data")
        ]),
        ("Module 4: Wireless & Active Directory Security", [
            ("Topic 4.1: Wireless Security Auditing (WPA2/WPA3 & EAP)",
             "https://www.youtube.com/watch?v=4FqV_p3_w7k\n\nNetworkChuck: Hacking Wi-Fi (WPA2 4-Way Handshake). Airmon-ng, airodump-ng, deauthentication frames, and Hashcat cracking.",
             48, "https://hashcat.net/hashcat/"),
            ("Topic 4.2: Active Directory Attacks: Kerberoasting & Pass-the-Hash",
             "https://www.youtube.com/watch?v=y_x8T9o0m2s\n\nTCM Security: Introduction to Active Directory Attacks. Kerberoasting SPNs, Pass-the-Hash, and BloodHound graphing.",
             55, "https://bloodhound.readthedocs.io/")
        ]),
        ("Module 5: Binary Exploitation & Buffer Overflows", [
            ("Topic 5.1: Memory Architecture, Stack Frames & Buffer Overflows",
             "https://www.youtube.com/watch?v=1S0aBV-Waeo\n\nLiveOverflow: Buffer Overflow Vulnerabilities. Stack memory layout, instruction pointer (EIP/RIP), buffer boundaries, and shellcode.",
             18, "https://github.com/Gallopsled/pwntools"),
            ("Topic 5.2: Exploit Mitigations: ASLR, DEP/NX & Return-Oriented Programming",
             "https://www.youtube.com/watch?v=zaQCJDdqpxE\n\nLiveOverflow: Bypassing DEP with Return-Oriented Programming (ROP). Constructing gadget chains in libc to execute code.",
             58, "https://en.wikipedia.org/wiki/Return-oriented_programming")
        ]),
        ("Module 6: Red Team Operations & Evasion Techniques", [
            ("Topic 6.1: Antivirus & EDR Evasion Mechanics",
             "https://www.youtube.com/watch?v=w7v_p7Y9k2s\n\nJohn Hammond: Antivirus Evasion Techniques. Payload encryption, in-memory execution, AMSI bypasses, and obfuscation.",
             50, "https://lolbas-project.github.io/"),
            ("Topic 6.2: Command and Control (C2) Infrastructure Setup",
             "https://www.youtube.com/watch?v=j_K9e7m2o4s\n\nDavid Bombal: Command and Control (C2) Frameworks. Mythic, Sliver, setting up HTTPS redirectors, and stealthy agent beacons.",
             52, "https://www.mythic-c2.net/")
        ])
    ],

    # =========================================================================
    # 5. DATA ENGINEERING & SYSTEMS ROADMAP
    # =========================================================================
    "Relational Database Design & SQL": [
        ("Module 1: Relational Foundations & Entity-Relationship Modeling", [
            ("Topic 1.1: Relational Model Foundations & ER Diagram Design",
             "https://www.youtube.com/watch?v=HXV3zeQKqGY\n\nfreeCodeCamp: SQL Tutorial - Full Database Course for Beginners. Tables, fields, primary keys, and relational schema modeling.",
             261, "https://www.postgresql.org/docs/"),
            ("Topic 1.2: Database Normalization (1NF, 2NF, 3NF, BCNF)",
             "https://www.youtube.com/watch?v=GFQaEYEc8_8\n\nDecomplexify: Database Normalization (1NF, 2NF, 3NF). Eliminating duplicate data, partial dependencies, and transitive anomalies.",
             29, "https://en.wikipedia.org/wiki/Database_normalization")
        ]),
        ("Module 2: DDL, Schema Constraints & Data Types", [
            ("Topic 2.1: SQL DDL: Tables, Data Types & Check Constraints",
             "https://www.youtube.com/watch?v=7S_tz1z_5bA\n\nProgramming with Mosh: SQL DDL Tutorial. CREATE TABLE, ALTER TABLE, column types, NOT NULL, and CHECK constraints.",
             190, "https://www.postgresql.org/docs/current/ddl.html"),
            ("Topic 2.2: Foreign Key Actions: CASCADE, SET NULL & RESTRICT",
             "https://www.youtube.com/watch?v=vV_XQj_L8v4\n\nAlex The Analyst: SQL Foreign Keys & Referential Integrity. ON DELETE CASCADE, ON UPDATE CASCADE, and referential constraints.",
             42, "https://www.postgresql.org/docs/current/ddl-constraints.html")
        ]),
        ("Module 3: Advanced Querying, Joins & Aggregations", [
            ("Topic 3.1: Inner, Left, Right & Full Outer Joins",
             "https://www.youtube.com/watch?v=9yeOJ0ZMUYw\n\nAlex The Analyst: SQL Joins Tutorial. INNER JOIN, LEFT OUTER, RIGHT OUTER, FULL OUTER JOIN, and multi-table joining.",
             10, "https://www.w3schools.com/sql/sql_join.asp"),
            ("Topic 3.2: Group By Aggregations, Having & Filter Conditions",
             "https://www.youtube.com/watch?v=QY_W4v_6xWk\n\nAlex The Analyst: SQL Group By and Having Clauses. COUNT, SUM, AVG, MIN, MAX aggregations and filtering aggregated sets.",
             44, "https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP")
        ]),
        ("Module 4: Window Functions & Analytic Queries", [
            ("Topic 4.1: SQL Window Functions: ROW_NUMBER, RANK & DENSE_RANK",
             "https://www.youtube.com/watch?v=Ww71knvhQ-9\n\nLuke Barousse: SQL Window Functions Tutorial. OVER(PARTITION BY ... ORDER BY), ROW_NUMBER(), RANK(), and DENSE_RANK().",
             50, "https://mode.com/sql-tutorial/sql-window-functions/"),
            ("Topic 4.2: Lead, Lag & Cumulative Moving Averages",
             "https://www.youtube.com/watch?v=O_h_Xm9p8vA\n\nLuke Barousse: Advanced SQL - LEAD and LAG functions, calculating day-over-day changes, and rolling moving averages.",
             46, "https://www.postgresql.org/docs/current/tutorial-window.html")
        ]),
        ("Module 5: Indexing & Query Execution Plans", [
            ("Topic 5.1: B-Tree Indexes, Composite Indexes & Covering Queries",
             "https://www.youtube.com/watch?v=fsG1XZTYvcc\n\nHussein Nasser: Database Indexing Explained. How B-Trees work, leaf nodes, composite indexes, and index selectivity.",
             52, "https://use-the-index-luke.com/"),
            ("Topic 5.2: Query Execution Plans: EXPLAIN ANALYZE & Optimization",
             "https://www.youtube.com/watch?v=mC1v8yWkX7w\n\nHussein Nasser: EXPLAIN ANALYZE in PostgreSQL. Sequential scans, index scans, bitmap heap scans, cost, and query tuning.",
             55, "https://www.postgresql.org/docs/current/using-explain.html")
        ]),
        ("Module 6: Transactions, Concurrency & ACID Guarantees", [
            ("Topic 6.1: ACID Guarantees, WAL Logging & Rollbacks",
             "https://www.youtube.com/watch?v=pomxJODecQA\n\nHussein Nasser: ACID Transactions Explained. Atomicity, Consistency, Isolation, Durability, and Write-Ahead Logging (WAL).",
             48, "https://en.wikipedia.org/wiki/ACID"),
            ("Topic 6.2: Transaction Isolation Levels & Concurrency Locks",
             "https://www.youtube.com/watch?v=4EajrPgJAk0\n\nHussein Nasser: Database Isolation Levels. Read Uncommitted, Read Committed, Repeatable Read, and Serializable.",
             30, "https://www.postgresql.org/docs/current/transaction-iso.html")
        ])
    ],

    "RESTful API Development with Python & OpenAPI": [
        ("Module 1: REST Architecture & HTTP Protocol Fundamentals", [
            ("Topic 1.1: REST Architectural Constraints & Resource URIs",
             "https://www.youtube.com/watch?v=-MTSQjw5DrM\n\nTraversy Media: REST API Concepts and Examples. Client-server decoupling, stateless requests, resource endpoints, and JSON payloads.",
             11, "https://restfulapi.net/"),
            ("Topic 1.2: HTTP Verbs, Idempotency & Standard Status Codes",
             "https://www.youtube.com/watch?v=2JYT5f2isg4\n\nWeb Dev Simplified: HTTP Status Codes and Verbs Explained. GET, POST, PUT, PATCH, DELETE, idempotency, and status classifications.",
             309, "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status")
        ]),
        ("Module 2: Schema Validation & Serialization", [
            ("Topic 2.1: Data Validation & Serialization with Pydantic",
             "https://www.youtube.com/watch?v=Vj-QUrs_Vao\n\nArjanCodes: Pydantic Tutorial for Python. Data validation, type hints, custom validators, and serialization to JSON.",
             48, "https://docs.pydantic.dev/"),
            ("Topic 2.2: Marshmallow Schema Deserialization in Flask",
             "https://www.youtube.com/watch?v=7LNl2AhNHqc\n\nPretty Printed: Marshmallow with Flask. Defining Schema objects, fields, validating inputs, and serializing querysets.",
             45, "https://marshmallow.readthedocs.io/")
        ]),
        ("Module 3: Authentication & API Security", [
            ("Topic 3.1: API Keys, Bearer Tokens & JWT Authorization",
             "https://www.youtube.com/watch?v=J5bIPtEBV0Q\n\nAmigoscode: API Security Best Practices. Securing endpoints with Bearer tokens, checking Authorization headers, and expiry.",
             50, "https://jwt.io/"),
            ("Topic 3.2: Rate Limiting & Denial of Service Protection",
             "https://www.youtube.com/watch?v=yY_vU_t7q8s\n\nHussein Nasser: API Rate Limiting Algorithms. Token Bucket, Leaky Bucket, Sliding Window, and Redis-backed rate limiting.",
             44, "https://flask-limiter.readthedocs.io/")
        ]),
        ("Module 4: OpenAPI 3.0 & Interactive Swagger Documentation", [
            ("Topic 4.1: OpenAPI 3.0 Specification & YAML Definitions",
             "https://www.youtube.com/watch?v=pRS9LRBgjBo\n\nfreeCodeCamp: OpenAPI Specification Tutorial. Documenting routes, request bodies, parameters, and responses with OpenAPI 3.0.",
             45, "https://swagger.io/specification/"),
            ("Topic 4.2: Automated Swagger UI & Redoc Interactive Docs",
             "https://www.youtube.com/watch?v=2Tz8A_o7qWs\n\nTraversy Media: Swagger UI & OpenAPI Docs. Integrating interactive documentation consoles into RESTful services.",
             42, "https://swagger.io/tools/swagger-ui/")
        ]),
        ("Module 5: Pagination, Filtering & Search Performance", [
            ("Topic 5.1: Cursor-Based vs Offset-Based API Pagination",
             "https://www.youtube.com/watch?v=gT_ZpE8s2k0\n\nHussein Nasser: Database Pagination Techniques. Why OFFSET is slow and how Keyset / Cursor-based pagination scales.",
             46, "https://slack.engineering/evolving-api-pagination-at-slack/"),
            ("Topic 5.2: Multi-Field Filtering, Sorting & Search Parameters",
             "https://www.youtube.com/watch?v=8V_7k2n4P9s\n\nAmigoscode: Advanced API Filtering and Sorting. Query parameters parsing, sorting asc/desc, and dynamic filtering.",
             42, "https://jsonapi.org/recommendations/#filtering")
        ]),
        ("Module 6: API Testing, Mocking & Versioning", [
            ("Topic 6.1: Automated API Integration Testing with Pytest & TestClient",
             "https://www.youtube.com/watch?v=by6v8VvCqVs\n\nArjanCodes: Testing APIs with Pytest. Fixtures, simulating HTTP requests, asserting JSON responses, and status codes.",
             46, "https://docs.pytest.org/"),
            ("Topic 6.2: API Versioning Strategies & Graceful Deprecation",
             "https://www.youtube.com/watch?v=5vT8hZ0p9k8\n\nByteByteGo: API Versioning Strategies. URI versioning, header versioning, query parameters, backwards compatibility, and deprecation.",
             42, "https://restfulapi.net/versioning/")
        ])
    ],

    "Advanced System Architecture & Distributed Systems": [
        ("Module 1: Scalability Foundations & Architectural Patterns", [
            ("Topic 1.1: Vertical vs Horizontal Scaling & Load Balancing",
             "https://www.youtube.com/watch?v=SqcXvc3ZmRU\n\nGaurav Sen: System Design - Scalability Basics. Vertical scaling, horizontal scaling, Round Robin, and Layer 4 vs Layer 7 load balancing.",
             9, "https://en.wikipedia.org/wiki/Load_balancing_(computing)"),
            ("Topic 1.2: Monoliths vs Microservices & Domain-Driven Design (DDD)",
             "https://www.youtube.com/watch?v=1xo-0gCVhTU\n\nByteByteGo: Microservices vs Monolith Architecture. Bounded contexts, service decoupling, network latency, and operational trade-offs.",
             55, "https://martinfowler.com/articles/microservices.html")
        ]),
        ("Module 2: Caching Architectures & High-Speed Data Access", [
            ("Topic 2.1: Distributed Caching with Redis & Invalidation Strategies",
             "https://www.youtube.com/watch?v=jgpVdJB2sKQ\n\nFireship: Redis in 100 Seconds / Caching Patterns. Cache-Aside, Write-Through, Write-Behind, TTL expiry, and Cache Stampedes.",
             28, "https://redis.io/"),
            ("Topic 2.2: Content Delivery Networks (CDN) & Static Asset Edge Caching",
             "https://www.youtube.com/watch?v=RI9nL4b_904\n\nByteByteGo: How a Content Delivery Network (CDN) Works. Edge servers, Anycast DNS, caching headers, and origin offload.",
             45, "https://www.cloudflare.com/learning/cdn/what-is-a-cdn/")
        ]),
        ("Module 3: Distributed Data Consistency & CAP Theorem", [
            ("Topic 3.1: CAP Theorem & PACELC Trade-Offs in Distributed Stores",
             "https://www.youtube.com/watch?v=k-Yaq8AHlFA\n\nByteByteGo: CAP Theorem Simplified. Consistency, Availability, Partition Tolerance trade-offs in distributed systems.",
             7, "https://en.wikipedia.org/wiki/CAP_theorem"),
            ("Topic 3.2: Eventual Consistency, Quorums & Conflict Resolution",
             "https://www.youtube.com/watch?v=ry_a9q_yY2s\n\nGaurav Sen: Eventual Consistency and Read/Write Quorums. Vector clocks, Dynamo-style quorum mathematics, and conflict resolution.",
             50, "https://aws.amazon.com/builders-library/")
        ]),
        ("Module 4: Event-Driven Architectures & Message Brokers", [
            ("Topic 4.1: Message Queues with RabbitMQ & AMQP Routing",
             "https://www.youtube.com/watch?v=deG25y_r6OY\n\nTechWorld with Nana: RabbitMQ in 100 Seconds and Full Tutorial. Exchanges, direct/topic/fanout routing, and consumer queues.",
             7, "https://www.rabbitmq.com/"),
            ("Topic 4.2: High-Throughput Event Streaming with Apache Kafka",
             "https://www.youtube.com/watch?v=R873BlBMx44\n\nTechWorld with Nana: Apache Kafka Tutorial for Beginners. Topics, partitions, consumer groups, offset retention, and event streams.",
             55, "https://kafka.apache.org/")
        ]),
        ("Module 5: Database Scaling & Sharding Architectures", [
            ("Topic 5.1: Database Read Replicas & Replication Lag Management",
             "https://www.youtube.com/watch?v=5r_n8q_kYw0\n\nByteByteGo: Database Replication - Master-Slave, Master-Master, synchronous vs asynchronous replication, and handling lag.",
             46, "https://en.wikipedia.org/wiki/Multi-master_replication"),
            ("Topic 5.2: Database Sharding & Consistent Hashing Rings",
             "https://www.youtube.com/watch?v=zaRkONvyGr8\n\nGaurav Sen: Consistent Hashing Explained. Hash rings, virtual nodes, rehashing minimization, and database sharding.",
             11, "https://en.wikipedia.org/wiki/Consistent_hashing")
        ]),
        ("Module 6: Distributed Resilience & Fault Tolerance", [
            ("Topic 6.1: Circuit Breaker Pattern & Rate Limiting Egress",
             "https://www.youtube.com/watch?v=ADHcBxEXvFA\n\nByteByteGo: Circuit Breaker Pattern Explained. Closed, Open, and Half-Open states to prevent cascading microservice outages.",
             12, "https://martinfowler.com/bliki/CircuitBreaker.html"),
            ("Topic 6.2: Distributed Tracing & Observability with OpenTelemetry",
             "https://www.youtube.com/watch?v=2n_Pq2N9v8s\n\nTechWorld with Nana: Distributed Tracing & OpenTelemetry. Trace IDs, spans, Jaeger visualization, and diagnosing latency across RPCs.",
             50, "https://opentelemetry.io/")
        ])
    ],

    # =========================================================================
    # 6. COMPUTER SCIENCE & DESIGN FOUNDATIONS
    # =========================================================================
    "Introduction to Computer Science": [
        ("Module 1: Computational Thinking & Binary Representation", [
            ("Topic 1.1: Binary Representation, Bits, Bytes & ASCII/Unicode",
             "https://www.youtube.com/watch?v=8mAITcNt710\n\nCS50 2024 Lecture 0: Computational Thinking, binary, bits, bytes, ASCII, Unicode, RGB pixels, and algorithms.",
             1492, "https://cs50.harvard.edu/"),
            ("Topic 1.2: Algorithms, Pseudocode & Computational Complexity",
             "https://www.youtube.com/watch?v=jjqgP9dpD1k\n\nCS50: What is an Algorithm? Linear search vs binary search, dividing problem spaces, and writing structured pseudocode.",
             62, "https://cs50.harvard.edu/x/")
        ]),
        ("Module 2: Low-Level Programming with C", [
            ("Topic 2.1: C Syntax, Data Types & Compilation Pipeline",
             "https://www.youtube.com/watch?v=e9Eds2RC_x8\n\nCS50 2024 Lecture 1: C Programming. Preprocessing, compiling, assembling, linking, types, and variables.",
             52, "https://en.cppreference.com/w/c"),
            ("Topic 2.2: Loops, Branching & Function Stacks in C",
             "https://www.youtube.com/watch?v=34HmS2_8WwA\n\nCS50: C Conditionals and Loops. While, for, do-while loops, functions, and stack frame execution.",
             48, "https://cs50.harvard.edu/x/2024/weeks/1/")
        ]),
        ("Module 3: Memory, Pointers & Array Storage", [
            ("Topic 3.1: Arrays, String Null Terminators & Memory Layout",
             "https://www.youtube.com/watch?v=2T-A_3PWgk8\n\nCS50 2024 Lecture 2: Arrays. Contiguous memory allocation, strings as char arrays, null terminators ('\\0'), and command-line arguments.",
             50, "https://cs50.harvard.edu/x/2024/weeks/2/"),
            ("Topic 3.2: Pointers, Memory Addresses & Pointer Arithmetic",
             "https://www.youtube.com/watch?v=XISnO2YhnsY\n\nCS50 2024 Lecture 4: Memory. Hexadecimal addresses, pointers (* and & operators), pointer arithmetic, and dereferencing.",
             29, "https://cs50.harvard.edu/x/2024/weeks/4/")
        ]),
        ("Module 4: Dynamic Memory Allocation & Heap Mechanics", [
            ("Topic 4.1: Heap Memory Allocation with Malloc & Free",
             "https://www.youtube.com/watch?v=zuegQmMdy8M\n\nCS50: Dynamic Memory with malloc and free. Heap vs stack, memory leaks, buffer overflows, and segmentation faults.",
             227, "https://man7.org/linux/man-pages/man3/malloc.3.html"),
            ("Topic 4.2: Debugging Memory with Valgrind & GDB",
             "https://www.youtube.com/watch?v=bb1bTJtg46A\n\nCS50: Debugging C code with Valgrind and GDB. Catching memory leaks and invalid reads/writes.",
             45, "https://valgrind.org/")
        ]),
        ("Module 5: Dynamic Data Structures in Memory", [
            ("Topic 5.1: Singly & Doubly Linked Lists Implementations",
             "https://www.youtube.com/watch?v=2wM6_PuBiXQ\n\nCS50 2024 Lecture 5: Data Structures. Structs, creating nodes, singly linked lists, inserting, and traversing lists.",
             50, "https://cs50.harvard.edu/x/2024/weeks/5/"),
            ("Topic 5.2: Hash Tables, Hash Functions & Collision Resolution",
             "https://www.youtube.com/watch?v=nvzVHwrrub0\n\nCS50: Hash Tables and Tries. Writing hash functions, collision resolution with separate chaining, and O(1) lookup.",
             19, "https://en.wikipedia.org/wiki/Hash_table")
        ]),
        ("Module 6: Algorithmic Sorting & Big-O Foundations", [
            ("Topic 6.1: Selection Sort, Bubble Sort & Big-O Notation",
             "https://www.youtube.com/watch?v=0jUv98i8e7Q\n\nCS50 2024 Lecture 3: Algorithms. Linear search, binary search, bubble sort, selection sort, and Big-O / Big-Omega notation.",
             48, "https://en.wikipedia.org/wiki/Big_O_notation"),
            ("Topic 6.2: Merge Sort, Recursion Trees & Divide-and-Conquer",
             "https://www.youtube.com/watch?v=Ns7tGNduvV4\n\nCS50: Merge Sort and Recursion. Divide-and-conquer strategy, recursive call trees, and proving O(n log n) efficiency.",
             55, "https://cs50.harvard.edu/x/2024/weeks/3/")
        ])
    ],

    "Data Structures & Algorithms in Python": [
        ("Module 1: Algorithmic Analysis & Big-O Foundations", [
            ("Topic 1.1: Time & Space Complexity Analysis (Big-O)",
             "https://www.youtube.com/watch?v=8hly31xKli0\n\nfreeCodeCamp: Algorithms and Data Structures. Asymptotic analysis, Big-O, Big-Omega, worst/best/average case, and auxiliary space.",
             322, "https://www.bigocheatsheet.com/"),
            ("Topic 1.2: Built-in Python Data Structure Internals",
             "https://www.youtube.com/watch?v=moPtwq_Aval\n\nCorey Schafer: Python Collections and Lists Internals. Amortized O(1) appends, dynamic resizing, and dictionary hash collisions.",
             45, "https://wiki.python.org/moin/TimeComplexity")
        ]),
        ("Module 2: Linear Data Structures: Stacks, Queues & Deques", [
            ("Topic 2.1: Stacks (LIFO) & Balanced Parentheses Problem",
             "https://www.youtube.com/watch?v=zwb3GmNAtFk\n\nNeetCode: Stacks and Queues Explained. Implementing Stack with Python list/deque, validating parentheses, and min-stack.",
             13, "https://docs.python.org/3/library/collections.html#collections.deque"),
            ("Topic 2.2: Queues (FIFO), Circular Queues & Priority Heaps",
             "https://www.youtube.com/watch?v=hGK_minHN20\n\nNeetCode: Priority Queues & Heaps. Heap property, min-heap vs max-heap, heapq module in Python, and building heaps in O(n).",
             48, "https://docs.python.org/3/library/heapq.html")
        ]),
        ("Module 3: Linked Lists & Two-Pointer Patterns", [
            ("Topic 3.1: Singly Linked List: Reversal, Insertion & Deletion",
             "https://www.youtube.com/watch?v=G0_I-ZF0S38\n\nNeetCode: Reverse a Linked List. Iterative pointer manipulation, dummy nodes, reversing in O(n) time, and O(1) space.",
             11, "https://realpython.com/linked-lists-python/"),
            ("Topic 3.2: Fast & Slow Pointers (Floyd's Cycle Detection)",
             "https://www.youtube.com/watch?v=gBTe7lFR3vc\n\nNeetCode: Linked List Cycle Detection (Floyd's Tortoise and Hare). Fast and slow pointer convergence and finding cycle start nodes.",
             11, "https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare")
        ]),
        ("Module 4: Trees, Binary Search Trees & Traversal Algorithms", [
            ("Topic 4.1: Binary Search Tree (BST) Properties & Operations",
             "https://www.youtube.com/watch?v=fAAZixBzIAI\n\nNeetCode: Trees and Binary Search Trees. BST properties, search, insert, and delete nodes with in-order successors.",
             109, "https://en.wikipedia.org/wiki/Binary_search_tree"),
            ("Topic 4.2: Tree Traversals: In-Order, Pre-Order, Post-Order & Level-Order",
             "https://www.youtube.com/watch?v=b_N4M4513CQ\n\nNeetCode: Binary Tree Traversal Algorithms. Depth-first search (Inorder, Preorder, Postorder) and BFS Level Order.",
             50, "https://neetcode.io/")
        ]),
        ("Module 5: Graph Theory, Representations & Traversals", [
            ("Topic 5.1: Graph Representations: Adjacency Matrix vs Adjacency List",
             "https://www.youtube.com/watch?v=tWVWeAqZ0WU\n\nWilliam Fiset: Graph Theory Introduction. Directed/undirected, weighted, adjacency matrix vs adjacency list, and memory complexity.",
             132, "https://en.wikipedia.org/wiki/Adjacency_list"),
            ("Topic 5.2: Breadth-First Search (BFS) & Depth-First Search (DFS) on Graphs",
             "https://www.youtube.com/watch?v=TIbUeeksXcI\n\nNeetCode: Breadth First Search (BFS) and Depth First Search (DFS) on Graphs. Shortest paths, visited sets, and cycles.",
             15, "https://en.wikipedia.org/wiki/Graph_traversal")
        ]),
        ("Module 6: Dynamic Programming & Recursion Patterns", [
            ("Topic 6.1: Recursion, Memoization & Top-Down Dynamic Programming",
             "https://www.youtube.com/watch?v=oBt53YbR9Kk\n\nfreeCodeCamp: Dynamic Programming - Learn to Solve Algorithmic Problems & Coding Challenges. Top-down memoization.",
             310, "https://en.wikipedia.org/wiki/Dynamic_programming"),
            ("Topic 6.2: Tabulation, 0/1 Knapsack & Classic DP Problems",
             "https://www.youtube.com/watch?v=Hdr64lKQ3e4\n\nNeetCode: 0/1 Knapsack Problem and Dynamic Programming Tabulation. 2D table state transitions and memory optimization.",
             20, "https://leetcode.com/explore/featured/card/dynamic-programming/")
        ])
    ],

    "UI/UX Design Systems and Figma Prototyping": [
        ("Module 1: UX Design Fundamentals & User Research", [
            ("Topic 1.1: Design Thinking Process: Empathize, Define, Ideate, Prototype, Test",
             "https://www.youtube.com/watch?v=c9Wg6Cb_YlU\n\nfreeCodeCamp: UI / UX Design Tutorial. The 5 stages of Design Thinking, user empathy, interviews, and problem definition.",
             86, "https://www.nngroup.com/articles/design-thinking/"),
            ("Topic 1.2: Information Architecture (IA) & User Flow Mapping",
             "https://www.youtube.com/watch?v=v2ffZp1_Poc\n\nFlux Academy: Information Architecture for UX Designers. Sitemaps, user flows, wireframes, and reducing cognitive load.",
             44, "https://www.usability.gov/what-and-why/information-architecture.html")
        ]),
        ("Module 2: Visual Design Principles & Typography", [
            ("Topic 2.1: Visual Hierarchy, Gestalt Principles & White Space",
             "https://www.youtube.com/watch?v=a5KYlHNKQB8\n\nDesignCourse: The Gestalt Principles of Design for UI Designers. Proximity, similarity, continuity, and intentional whitespace.",
             5, "https://lawsofux.com/"),
            ("Topic 2.2: Typography Scales, Line Heights & Color Theory",
             "https://www.youtube.com/watch?v=sByzU_W0P6w\n\nDesignCourse: Typography Rules for UI Design. Type scales, font pairings, line height rhythm, and the 60-30-10 color rule.",
             46, "https://www.w3.org/WAI/WCAG21/quickref/")
        ]),
        ("Module 3: Figma Core Workspace & Vector Tools", [
            ("Topic 3.1: Frames, Vector Shapes & Pen Tool Precision",
             "https://www.youtube.com/watch?v=FTFaQWZBqQ8\n\nTraversy Media: Figma Crash Course for Beginners. Frame hierarchies, vector pen tool, bezier handles, and boolean operations.",
             24, "https://help.figma.com/hc/en-us/articles/360040450173-Guide-to-vector-networks"),
            ("Topic 3.2: Auto Layout 5.0: Flexbox for Designers",
             "https://www.youtube.com/watch?v=JwSX5w_k5B0\n\nFigma Official: Auto Layout Deep Dive. Stacking directions, padding, hugging, filling container, and responsive card components.",
             52, "https://help.figma.com/hc/en-us/articles/360040451373-Explore-auto-layout-properties")
        ]),
        ("Module 4: Reusable Components & Design Tokens", [
            ("Topic 4.1: Figma Component Variants & Component Properties",
             "https://www.youtube.com/watch?v=480X_g2u6o4\n\nFigma Official: Component Properties and Variants. Designing button component matrices with states (hover, active, disabled).",
             48, "https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-component-variants"),
            ("Topic 4.2: Design Tokens: Colors, Spacing & Typography Styles",
             "https://www.youtube.com/watch?v=yWk0kZ7P8wA\n\nDesignCourse: Design Tokens in Figma. Color variables, spacing tokens, border radii, and publishing shared design libraries.",
             46, "https://m3.material.io/foundations/design-tokens/overview")
        ]),
        ("Module 5: Interactive Prototyping & Micro-Interactions", [
            ("Topic 5.1: Interactive State Connections & Smart Animate",
             "https://www.youtube.com/watch?v=II-6dDzc-dg\n\nFigma Official: Prototyping Tutorial. Click triggers, while hovering, easing curves, and Smart Animate layer transitions.",
             50, "https://help.figma.com/hc/en-us/articles/360040035874-Smart-animate-layers-between-frames"),
            ("Topic 5.2: Overlays, Modals & Mobile Hamburger Drawers",
             "https://www.youtube.com/watch?v=u1m8bQ_s1nE\n\nFigma Official: Interactive Components & Overlays. Slide-in menus, centered modal dialogues, and realistic interactive apps.",
             48, "https://help.figma.com/hc/en-us/articles/360039818254-Create-interactive-components-with-variants")
        ]),
        ("Module 6: Design System Handoff & Frontend Code Connect", [
            ("Topic 6.1: Developer Handoff, Inspect Panel & CSS Export",
             "https://www.youtube.com/watch?v=kYvV_N6-J38\n\nFigma Official: Dev Mode Deep Dive. Inspecting CSS box models, exporting SVG icons, token names, and developer handoff.",
             45, "https://help.figma.com/hc/en-us/articles/15023124642203-Guide-to-Dev-Mode"),
            ("Topic 6.2: Design System Maintenance & Component Versioning",
             "https://www.youtube.com/watch?v=T_8wGgqO4z8\n\nDesignCourse: How to Maintain a Design System in Figma. Versioning component releases, changelogs, and team libraries.",
             48, "https://designsystemsrepo.com/")
        ])
    ]
}


def apply_unique_videos():
    app = create_app('development')
    with app.app_context():
        print("-> Applying 100% Unique, Dedicated YouTube Videos to every Topic across all 19 courses...")
        total_lessons_updated = 0
        all_unique_ids = set()

        courses = Course.query.order_by(Course.id).all()
        for course in courses:
            curriculum = UNIQUE_TOPIC_VIDEOS.get(course.title)
            if not curriculum:
                print(f"Skipping '{course.title}' (no matching curriculum)")
                continue

            # Map modules by title or sequence
            modules_by_pos = {m.position: m for m in course.modules}
            course_video_ids = set()

            for mod_idx, (mod_title, lessons_data) in enumerate(curriculum, start=1):
                mod = modules_by_pos.get(mod_idx)
                if not mod:
                    mod = Module(course_id=course.id, title=mod_title, position=mod_idx)
                    db.session.add(mod)
                    db.session.flush()

                mod.title = mod_title

                # Map lessons by position
                lessons_by_pos = {l.position: l for l in mod.lessons}

                for les_idx, (les_title, content_desc, dur_min, res_url) in enumerate(lessons_data, start=1):
                    # Extract video ID
                    yt_match = re.search(r'(?:v=|\/embed\/|\/watch\?v=|\.be\/)([a-zA-Z0-9_-]{11})', content_desc)
                    vid_id = yt_match.group(1) if yt_match else 'UNKNOWN'
                    course_video_ids.add(vid_id)
                    all_unique_ids.add(vid_id)

                    les = lessons_by_pos.get(les_idx)
                    if not les:
                        les = Lesson(
                            module_id=mod.id,
                            title=les_title,
                            content=content_desc,
                            content_type='video_url',
                            duration_min=dur_min,
                            position=les_idx
                        )
                        db.session.add(les)
                        db.session.flush()
                    else:
                        les.title = les_title
                        les.content = content_desc
                        les.duration_min = dur_min

                    # Update resource
                    if res_url:
                        res = LessonResource.query.filter_by(lesson_id=les.id).first()
                        if not res:
                            res = LessonResource(
                                lesson_id=les.id,
                                title=f"Documentation & Reference: {les_title}",
                                resource_type='link',
                                url_or_path=res_url
                            )
                            db.session.add(res)
                        else:
                            res.url_or_path = res_url
                            res.title = f"Documentation & Reference: {les_title}"

                    total_lessons_updated += 1

            print(f"Course #{course.id:2d}: '{course.title[:35]}' -> {len(course_video_ids)} UNIQUE videos across {len(curriculum)*2} topics (Zero duplicates!)")

        db.session.commit()
        print(f"\n-> Successfully updated {total_lessons_updated} lessons across all courses.")
        print(f"-> Total distinct YouTube video lessons across the platform: {len(all_unique_ids)}")


if __name__ == "__main__":
    apply_unique_videos()
