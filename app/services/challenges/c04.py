"""Course 4 topic-specific programming challenges."""

CHALLENGES = {(1, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all inputs positive ints',
                      'difficulty': 'Advance',
                      'explanation': 'Analytical parameter scaling laws for transformer autoregressive decoders.',
                      'function_name': 'estimate_transformer_parameters',
                      'hint': 'embed = vocab_size * d_model; per_layer = 12 * (d_model**2); return embed + num_layers '
                              '* per_layer.',
                      'id': 'c4-m1-l1-a',
                      'prompt': 'Write `estimate_transformer_parameters(num_layers, d_model, vocab_size)`: embedding '
                                'params = `vocab_size * d_model`, per layer attention params = `4 * (d_model**2)`, '
                                'feedforward params = `8 * (d_model**2)`. Return total parameters count.',
                      'solution_code': 'def estimate_transformer_parameters(num_layers: int, d_model: int, vocab_size: '
                                       'int) -> int:\n'
                                       '    embed = vocab_size * d_model\n'
                                       '    layer_params = 12 * (d_model ** 2)\n'
                                       '    return embed + (num_layers * layer_params)\n',
                      'starter_code': 'def estimate_transformer_parameters(num_layers: int, d_model: int, vocab_size: '
                                      'int) -> int:\n'
                                      '    # Return total parameter count\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'GPT-2 Small approx 124M params (sans final projection)',
                                      'expected': 123532032,
                                      'input': [12, 768, 50257]}],
                      'title': 'Transformer Parameter Counter'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'token counts >= 0, prices >= 0',
                    'difficulty': 'Basic',
                    'explanation': 'Token-based billing economics for commercial foundation models.',
                    'function_name': 'estimate_llm_cost',
                    'hint': '(prompt_tokens / 1000) * prompt_price_per_1k + (completion_tokens / 1000) * '
                            'comp_price_per_1k',
                    'id': 'c4-m1-l1-b',
                    'prompt': 'Write `estimate_llm_cost(prompt_tokens, completion_tokens, prompt_price_per_1k, '
                              'comp_price_per_1k)`. Compute total dollar cost rounded to 4 decimals.',
                    'solution_code': 'def estimate_llm_cost(prompt_tokens: int, completion_tokens: int, '
                                     'prompt_price_per_1k: float, comp_price_per_1k: float) -> float:\n'
                                     '    cost = (prompt_tokens / 1000.0) * prompt_price_per_1k + (completion_tokens / '
                                     '1000.0) * comp_price_per_1k\n'
                                     '    return round(cost, 4)\n',
                    'starter_code': 'def estimate_llm_cost(prompt_tokens: int, completion_tokens: int, '
                                    'prompt_price_per_1k: float, comp_price_per_1k: float) -> float:\n'
                                    '    # Return total dollar cost\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '1.0*0.0015 + 0.5*0.002 = 0.0025',
                                    'expected': 0.0025,
                                    'input': [1000, 500, 0.0015, 0.002]}],
                    'title': 'LLM Inference Cost Calculator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'cross_entropy_loss >= 0',
                           'difficulty': 'Intermediate',
                           'explanation': 'Perplexity exponentiates cross-entropy loss, representing effective '
                                          'vocabulary branching factor.',
                           'function_name': 'perplexity_from_loss',
                           'hint': 'import math; math.exp(cross_entropy_loss)',
                           'id': 'c4-m1-l1-i',
                           'prompt': 'Write `perplexity_from_loss(cross_entropy_loss)`: `e^(cross_entropy_loss)`. '
                                     'Round to 2 decimals using math.exp.',
                           'solution_code': 'def perplexity_from_loss(cross_entropy_loss: float) -> float:\n'
                                            '    import math\n'
                                            '    return round(math.exp(cross_entropy_loss), 2)\n',
                           'starter_code': 'def perplexity_from_loss(cross_entropy_loss: float) -> float:\n'
                                           '    # Return perplexity\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Perplexity 1.0 on zero loss', 'expected': 1.0, 'input': [0.0]},
                                          {'desc': 'e^2.3026 ~ 10.0', 'expected': 10.0, 'input': [2.3026]}],
                           'title': 'Perplexity from Cross-Entropy Loss'}},
 (1, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'vocab is set or list of strings',
                      'difficulty': 'Advance',
                      'explanation': 'WordPiece / SentencePiece maximal-matching greedy tokenization.',
                      'function_name': 'subword_greedy_tokenize',
                      'hint': 'While len(word) > 0, find longest prefix in vocab.',
                      'id': 'c4-m1-l2-a',
                      'prompt': 'Write `subword_greedy_tokenize(word, vocab)` finding longest matching prefix in vocab '
                                'repeatedly to tokenize word. If no prefix matches, append character itself.',
                      'solution_code': 'def subword_greedy_tokenize(word: str, vocab: list) -> list:\n'
                                       '    v_set = set(vocab)\n'
                                       '    tokens = []\n'
                                       '    curr = word\n'
                                       '    while curr:\n'
                                       '        matched = False\n'
                                       '        for l in range(len(curr), 0, -1):\n'
                                       '            prefix = curr[:l]\n'
                                       '            if prefix in v_set:\n'
                                       '                tokens.append(prefix)\n'
                                       '                curr = curr[l:]\n'
                                       '                matched = True\n'
                                       '                break\n'
                                       '        if not matched:\n'
                                       '            tokens.append(curr[0])\n'
                                       '            curr = curr[1:]\n'
                                       '    return tokens\n',
                      'starter_code': 'def subword_greedy_tokenize(word: str, vocab: list) -> list:\n'
                                      '    # Return list of subwords\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Greedy prefix segmentation',
                                      'expected': ['un', 'break', 'able'],
                                      'input': ['unbreakable', ['un', 'break', 'able', 'break']]}],
                      'title': 'Subword Vocabulary Inverted Tokenizer'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'at least one word has length >= 2',
                    'difficulty': 'Basic',
                    'explanation': 'Core iteration step of Sennrich et al. Byte-Pair Encoding subword tokenization.',
                    'function_name': 'find_most_frequent_bpe_pair',
                    'hint': 'Count all pairs (word[i], word[i+1]) across all words.',
                    'id': 'c4-m1-l2-b',
                    'prompt': 'Write `find_most_frequent_bpe_pair(tokenized_words)` where each word is a list of '
                              'sub-tokens (e.g. `[["l", "o", "w"], ["l", "o", "w", "e", "r"]]`). Return most frequent '
                              'adjacent pair `(t1, t2)`. Tie-break lexicographically.',
                    'solution_code': 'def find_most_frequent_bpe_pair(tokenized_words: list) -> tuple:\n'
                                     '    counts = {}\n'
                                     '    for w in tokenized_words:\n'
                                     '        for i in range(len(w) - 1):\n'
                                     '            pair = (w[i], w[i+1])\n'
                                     '            counts[pair] = counts.get(pair, 0) + 1\n'
                                     '    max_c = max(counts.values())\n'
                                     '    best_pairs = [p for p, c in counts.items() if c == max_c]\n'
                                     '    return sorted(best_pairs)[0]\n',
                    'starter_code': 'def find_most_frequent_bpe_pair(tokenized_words: list) -> tuple:\n'
                                    '    # Return (t1, t2) pair\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '("l", "o") and ("o", "w") both appear 2 times, ("l", "o") wins tie-break',
                                    'expected': ('l', 'o'),
                                    'input': [[['l', 'o', 'w'], ['l', 'o', 'w', 'e', 'r']]]}],
                    'title': 'Byte-Pair Encoding (BPE) Pair Counter'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'len(pair_to_merge) == 2',
                           'difficulty': 'Intermediate',
                           'explanation': 'Greedy vocabulary expansion token rewriting.',
                           'function_name': 'merge_bpe_pair',
                           'hint': 'Loop through with index i, if match append t1+t2 and advance 2.',
                           'id': 'c4-m1-l2-i',
                           'prompt': 'Write `merge_bpe_pair(tokenized_word, pair_to_merge)` replacing adjacent '
                                     '`pair_to_merge[0]` and `pair_to_merge[1]` with concatenated string `t1+t2`.',
                           'solution_code': 'def merge_bpe_pair(tokenized_word: list, pair_to_merge: list) -> list:\n'
                                            '    res = []\n'
                                            '    i = 0\n'
                                            '    p1, p2 = pair_to_merge[0], pair_to_merge[1]\n'
                                            '    while i < len(tokenized_word):\n'
                                            '        if i < len(tokenized_word) - 1 and tokenized_word[i] == p1 and '
                                            'tokenized_word[i+1] == p2:\n'
                                            '            res.append(p1 + p2)\n'
                                            '            i += 2\n'
                                            '        else:\n'
                                            '            res.append(tokenized_word[i])\n'
                                            '            i += 1\n'
                                            '    return res\n',
                           'starter_code': 'def merge_bpe_pair(tokenized_word: list, pair_to_merge: list) -> list:\n'
                                           '    # Return merged token list\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Merges "l" and "o" into "lo"',
                                           'expected': ['lo', 'w'],
                                           'input': [['l', 'o', 'w'], ['l', 'o']]}],
                           'title': 'Merge BPE Token Pair'}},
 (2, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': '0 < p <= 1.0, sum(probabilities) == 1.0',
                      'difficulty': 'Advance',
                      'explanation': 'Holtzman et al. Nucleus sampling dynamically adapting sampling pool size.',
                      'function_name': 'top_p_nucleus_indices',
                      'hint': 'Accumulate sum, break as soon as cumulative >= p.',
                      'id': 'c4-m2-l1-a',
                      'prompt': 'Write `top_p_nucleus_indices(probabilities, p)` where probabilities is a sorted '
                                'descending distribution. Return 0-indexed indices whose cumulative probability '
                                'reaches or exceeds p.',
                      'solution_code': 'def top_p_nucleus_indices(probabilities: list, p: float) -> list:\n'
                                       '    cum = 0.0\n'
                                       '    indices = []\n'
                                       '    for i, prob in enumerate(probabilities):\n'
                                       '        indices.append(i)\n'
                                       '        cum += prob\n'
                                       '        if cum >= p:\n'
                                       '            break\n'
                                       '    return indices\n',
                      'starter_code': 'def top_p_nucleus_indices(probabilities: list, p: float) -> list:\n'
                                      '    # Return nucleus indices\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '0.5 + 0.3 = 0.8 >= 0.75',
                                      'expected': [0, 1],
                                      'input': [[0.5, 0.3, 0.15, 0.05], 0.75]}],
                      'title': 'Top-P (Nucleus) Cumulative Probability Mask'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'temperature > 0',
                    'difficulty': 'Basic',
                    'explanation': 'Controls randomness and entropy during LLM autoregressive generation.',
                    'function_name': 'apply_temperature_scaling',
                    'hint': 'Divide each logit by temperature.',
                    'id': 'c4-m2-l1-b',
                    'prompt': 'Write `apply_temperature_scaling(logits, temperature)`: `[x / temperature for x in '
                              'logits]`. Round to 4 decimals.',
                    'solution_code': 'def apply_temperature_scaling(logits: list, temperature: float) -> list:\n'
                                     '    return [round(x / temperature, 4) for x in logits]\n',
                    'starter_code': 'def apply_temperature_scaling(logits: list, temperature: float) -> list:\n'
                                    '    # Return scaled logits\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Sharpen logits at temp 0.5',
                                    'expected': [4.0, 8.0],
                                    'input': [[2.0, 4.0], 0.5]},
                                   {'desc': 'Flatten logits at temp 2.0',
                                    'expected': [1.0, 2.0],
                                    'input': [[2.0, 4.0], 2.0]}],
                    'title': 'Temperature-Scaled Logits'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': '1 <= k <= len(logits)',
                           'difficulty': 'Intermediate',
                           'explanation': 'Truncates low-probability tail in top-k autoregressive decoding.',
                           'function_name': 'top_k_filtering_mask',
                           'hint': 'Find threshold = sorted(logits, reverse=True)[k-1], replace smaller values.',
                           'id': 'c4-m2-l1-i',
                           'prompt': 'Write `top_k_filtering_mask(logits, k, mask_value)`: keeps top k logits, sets '
                                     'all others to mask_value.',
                           'solution_code': 'def top_k_filtering_mask(logits: list, k: int, mask_value: float) -> '
                                            'list:\n'
                                            '    thresh = sorted(logits, reverse=True)[k - 1]\n'
                                            '    return [x if x >= thresh else mask_value for x in logits]\n',
                           'starter_code': 'def top_k_filtering_mask(logits: list, k: int, mask_value: float) -> '
                                           'list:\n'
                                           '    # Return filtered logits\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Keeps 50.0 and 20.0',
                                           'expected': [-1000000000.0, 50.0, 20.0, -1000000000.0],
                                           'input': [[10.0, 50.0, 20.0, 5.0], 2, -1000000000.0]}],
                           'title': 'Top-K Logits Filtering Mask'}},
 (2, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'reasoning_chains is non-empty list',
                      'difficulty': 'Advance',
                      'explanation': 'Self-consistency decoding across sampled reasoning paths.',
                      'function_name': 'self_consistency_vote',
                      'hint': 'Count occurrences of final_answer, find max and divide by len.',
                      'id': 'c4-m2-l2-a',
                      'prompt': 'Write `self_consistency_vote(reasoning_chains)` where each chain is `{"reasoning": '
                                'str, "final_answer": str}`. Return the most frequent final_answer and its confidence '
                                'score `count / total` rounded to 2 decimals.',
                      'solution_code': 'def self_consistency_vote(reasoning_chains: list) -> dict:\n'
                                       '    counts = {}\n'
                                       '    for c in reasoning_chains:\n'
                                       '        ans = c["final_answer"]\n'
                                       '        counts[ans] = counts.get(ans, 0) + 1\n'
                                       '    best = max(counts, key=counts.get)\n'
                                       '    conf = round(counts[best] / len(reasoning_chains), 2)\n'
                                       '    return {"answer": best, "confidence": conf}\n',
                      'starter_code': 'def self_consistency_vote(reasoning_chains: list) -> dict:\n'
                                      '    # Return {"answer": ..., "confidence": ...}\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '2 of 3 vote 42',
                                      'expected': {'answer': '42', 'confidence': 0.67},
                                      'input': [[{'final_answer': '42', 'reasoning': 'r1'},
                                                 {'final_answer': '42', 'reasoning': 'r2'},
                                                 {'final_answer': '10', 'reasoning': 'r3'}]]}],
                      'title': 'Self-Consistency Majority Vote Synthesizer'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all strings non-empty',
                    'difficulty': 'Basic',
                    'explanation': 'In-context few-shot learning conditioning.',
                    'function_name': 'build_few_shot_prompt',
                    'hint': 'Assemble system message, examples with newlines, and query.',
                    'id': 'c4-m2-l2-b',
                    'prompt': 'Write `build_few_shot_prompt(system_msg, examples, user_query)` where examples is list '
                              'of `(input, output)` pairs. Format: `{system_msg}\\n\\nInput: {in}\\nOutput: '
                              '{out}...\\n\\nInput: {user_query}\\nOutput:`.',
                    'solution_code': 'def build_few_shot_prompt(system_msg: str, examples: list, user_query: str) -> '
                                     'str:\n'
                                     '    ex_str = "\\n".join(f"Input: {i}\\nOutput: {o}" for i, o in examples)\n'
                                     '    return f"{system_msg}\\n\\n{ex_str}\\n\\nInput: {user_query}\\nOutput:"\n',
                    'starter_code': 'def build_few_shot_prompt(system_msg: str, examples: list, user_query: str) -> '
                                    'str:\n'
                                    '    # Return formatted prompt\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Standard 1-shot formatting',
                                    'expected': 'Translate to French\n'
                                                '\n'
                                                'Input: hello\n'
                                                'Output: bonjour\n'
                                                '\n'
                                                'Input: bye\n'
                                                'Output:',
                                    'input': ['Translate to French', [['hello', 'bonjour']], 'bye']}],
                    'title': 'Few-Shot Prompt Builder'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'model_response is multiline string',
                           'difficulty': 'Intermediate',
                           'explanation': 'Chain-of-Thought intermediate reasoning step extraction.',
                           'function_name': 'extract_cot_steps',
                           'hint': 'Filter lines with line.startswith("Step ") and "Step" in line.',
                           'id': 'c4-m2-l2-i',
                           'prompt': 'Write `extract_cot_steps(model_response)`: extracts lines starting with "Step '
                                     'X:" (e.g. "Step 1: calculate sum") into a list of step descriptions.',
                           'solution_code': 'def extract_cot_steps(model_response: str) -> list:\n'
                                            '    return [line.strip() for line in model_response.splitlines() if '
                                            'line.strip().startswith("Step ")]\n',
                           'starter_code': 'def extract_cot_steps(model_response: str) -> list:\n'
                                           '    # Return list of reasoning steps\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Extracts 2 CoT steps',
                                           'expected': ['Step 1: Compute tax', 'Step 2: Add tip'],
                                           'input': ['Let me think.\n'
                                                     'Step 1: Compute tax\n'
                                                     'Step 2: Add tip\n'
                                                     'Final Answer: 42']}],
                           'title': 'Chain-of-Thought (CoT) Step Extractor'}},
 (3, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'candidates is non-empty list of dicts',
                      'difficulty': 'Advance',
                      'explanation': 'Maximal Marginal Relevance balances retrieval relevance with document diversity.',
                      'function_name': 'mmr_select_next',
                      'hint': 'Calculate MMR formula for each candidate and select max.',
                      'id': 'c4-m3-l1-a',
                      'prompt': 'Write `mmr_select_next(candidates, selected, lambda_param)`: score = `lambda_param * '
                                'c["sim_to_query"] - (1 - lambda_param) * max(sim(c, s) for s in selected)`. If '
                                'selected is empty, score is `sim_to_query`. Return doc_id of highest scoring '
                                'candidate.',
                      'solution_code': 'def mmr_select_next(candidates: list, selected: list, lambda_param: float) -> '
                                       'str:\n'
                                       '    best_id, best_score = None, -1e9\n'
                                       '    for c in candidates:\n'
                                       '        sim_q = c["sim_to_query"]\n'
                                       '        if not selected or not c.get("sim_to_selected"):\n'
                                       '            score = sim_q\n'
                                       '        else:\n'
                                       '            max_red = max(c["sim_to_selected"])\n'
                                       '            score = (lambda_param * sim_q) - ((1.0 - lambda_param) * max_red)\n'
                                       '        if score > best_score:\n'
                                       '            best_score = score\n'
                                       '            best_id = c["id"]\n'
                                       '    return best_id\n',
                      'starter_code': 'def mmr_select_next(candidates: list, selected: list, lambda_param: float) -> '
                                      'str:\n'
                                      '    # Return best candidate id\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'c2 has higher diversity: 0.5*0.7 - 0.5*0.1 = 0.3 > c1 (0.05)',
                                      'expected': 'c2',
                                      'input': [[{'id': 'c1', 'sim_to_query': 0.9, 'sim_to_selected': [0.8]},
                                                 {'id': 'c2', 'sim_to_query': 0.7, 'sim_to_selected': [0.1]}],
                                                ['s1'],
                                                0.5]}],
                      'title': 'Maximal Marginal Relevance (MMR) Selector'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all embeddings normalized and non-empty',
                    'difficulty': 'Basic',
                    'explanation': 'Chroma / Pinecone top-K approximate nearest neighbor retrieval.',
                    'function_name': 'rank_documents_by_similarity',
                    'hint': 'Calculate dot product for each doc, sort with key=lambda x: x["score"], reverse=True.',
                    'id': 'c4-m3-l1-b',
                    'prompt': 'Write `rank_documents_by_similarity(query_emb, doc_embeddings)` where doc_embeddings is '
                              '`[{"id": doc_id, "embedding": vec}]`. Return sorted list of doc_ids in descending order '
                              'of dot product with query_emb.',
                    'solution_code': 'def rank_documents_by_similarity(query_emb: list, doc_embeddings: list) -> '
                                     'list:\n'
                                     '    scored = []\n'
                                     '    for d in doc_embeddings:\n'
                                     '        score = sum(q * e for q, e in zip(query_emb, d["embedding"]))\n'
                                     '        scored.append((d["id"], score))\n'
                                     '    scored.sort(key=lambda x: x[1], reverse=True)\n'
                                     '    return [d[0] for d in scored]\n',
                    'starter_code': 'def rank_documents_by_similarity(query_emb: list, doc_embeddings: list) -> list:\n'
                                    '    # Return sorted doc_ids\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'doc2 dot=0.8 > doc1 dot=0.0',
                                    'expected': ['doc2', 'doc1'],
                                    'input': [[1.0, 0.0],
                                              [{'embedding': [0.0, 1.0], 'id': 'doc1'},
                                               {'embedding': [0.8, 0.6], 'id': 'doc2'}]]}],
                    'title': 'Cosine Similarity Document Ranking'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'dense_ranks and sparse_ranks are ordered doc_id lists, k >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Hybrid search score fusion combining dense vector embeddings and BM25 '
                                          'keywords.',
                           'function_name': 'reciprocal_rank_fusion',
                           'hint': 'Map 1-indexed position for each doc in both lists.',
                           'id': 'c4-m3-l1-i',
                           'prompt': 'Write `reciprocal_rank_fusion(dense_ranks, sparse_ranks, k)`: for each doc '
                                     '`score = 1/(k + r_dense) + 1/(k + r_sparse)` where rank `r` is 1-indexed. Return '
                                     'dict of `{doc: round(score, 4)}`.',
                           'solution_code': 'def reciprocal_rank_fusion(dense_ranks: list, sparse_ranks: list, k: int) '
                                            '-> dict:\n'
                                            '    docs = set(dense_ranks) | set(sparse_ranks)\n'
                                            '    res = {}\n'
                                            '    for d in docs:\n'
                                            '        s = 0.0\n'
                                            '        if d in dense_ranks: s += 1.0 / (k + dense_ranks.index(d) + 1)\n'
                                            '        if d in sparse_ranks: s += 1.0 / (k + sparse_ranks.index(d) + 1)\n'
                                            '        res[d] = round(s, 4)\n'
                                            '    return res\n',
                           'starter_code': 'def reciprocal_rank_fusion(dense_ranks: list, sparse_ranks: list, k: int) '
                                           '-> dict:\n'
                                           '    # Return RRF scores\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Symmetric rank 1 and 2 give equal 1/61 + 1/62 = 0.0325',
                                           'expected': {'docA': 0.0325, 'docB': 0.0325},
                                           'input': [['docA', 'docB'], ['docB', 'docA'], 60]}],
                           'title': 'Reciprocal Rank Fusion (RRF)'}},
 (3, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'graph_edges is `{node: [neighbors]}`',
                      'difficulty': 'Advance',
                      'explanation': 'Hierarchical Navigable Small World (HNSW) graph greedy routing.',
                      'function_name': 'hnsw_greedy_step',
                      'hint': 'Compute dist from query to current_node and all neighbors.',
                      'id': 'c4-m3-l2-a',
                      'prompt': 'Write `hnsw_greedy_step(current_node, query_vec, node_vectors, graph_edges)`: finds '
                                'neighbor of current_node in graph_edges that is strictly closer to query_vec than '
                                'current_node. If found, returns closest neighbor id, else returns current_node.',
                      'solution_code': 'def hnsw_greedy_step(current_node: str, query_vec: list, node_vectors: dict, '
                                       'graph_edges: dict) -> str:\n'
                                       '    def dist(n):\n'
                                       '        v = node_vectors[n]\n'
                                       '        return sum((a - b)**2 for a, b in zip(query_vec, v))\n'
                                       '    curr_dist = dist(current_node)\n'
                                       '    best_node, best_d = current_node, curr_dist\n'
                                       '    for nbr in graph_edges.get(current_node, []):\n'
                                       '        d = dist(nbr)\n'
                                       '        if d < best_d:\n'
                                       '            best_d = d\n'
                                       '            best_node = nbr\n'
                                       '    return best_node\n',
                      'starter_code': 'def hnsw_greedy_step(current_node: str, query_vec: list, node_vectors: dict, '
                                      'graph_edges: dict) -> str:\n'
                                      '    # Return next hop node id\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'n2 [5,5] is closer to [10,10] than n1 [0,0]',
                                      'expected': 'n2',
                                      'input': ['n1',
                                                [10, 10],
                                                {'n1': [0, 0], 'n2': [5, 5], 'n3': [1, 1]},
                                                {'n1': ['n2', 'n3']}]}],
                      'title': 'HNSW Greedy Graph Routing Step'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'len(vec1) == len(vec2)',
                    'difficulty': 'Basic',
                    'explanation': 'L2 vector distance metric used in vector database indexes.',
                    'function_name': 'embedding_l2_distance',
                    'hint': 'Subtract, square, sum, sqrt.',
                    'id': 'c4-m3-l2-b',
                    'prompt': 'Write `embedding_l2_distance(vec1, vec2)`: `sqrt(sum((v1 - v2)**2))`. Round to 4 '
                              'decimals.',
                    'solution_code': 'def embedding_l2_distance(vec1: list, vec2: list) -> float:\n'
                                     '    return round(sum((a - b)**2 for a, b in zip(vec1, vec2)) ** 0.5, 4)\n',
                    'starter_code': 'def embedding_l2_distance(vec1: list, vec2: list) -> float:\n'
                                    '    # Return L2 distance\n'
                                    '    pass\n',
                    'test_cases': [{'desc': '3-4-5 distance = 0.5',
                                    'expected': 0.5,
                                    'input': [[0.0, 0.0], [0.3, 0.4]]}],
                    'title': 'Euclidean Embedding Distance'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'codebook is non-empty list of centroids',
                           'difficulty': 'Intermediate',
                           'explanation': 'Product Quantization (PQ) vector compression in FAISS / Milvus.',
                           'function_name': 'quantize_to_codebook',
                           'hint': 'Calculate squared distance to each centroid, return argmin.',
                           'id': 'c4-m3-l2-i',
                           'prompt': 'Write `quantize_to_codebook(vector, codebook)` returning index of nearest '
                                     'centroid in codebook by L2 distance.',
                           'solution_code': 'def quantize_to_codebook(vector: list, codebook: list) -> int:\n'
                                            '    dists = [sum((a - b)**2 for a, b in zip(vector, c)) for c in '
                                            'codebook]\n'
                                            '    return dists.index(min(dists))\n',
                           'starter_code': 'def quantize_to_codebook(vector: list, codebook: list) -> int:\n'
                                           '    # Return codebook index\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Tied distance to 0,0 and 2,2 -> picks first (0)',
                                           'expected': 0,
                                           'input': [[1.0, 1.0], [[0.0, 0.0], [2.0, 2.0], [10.0, 10.0]]]}],
                           'title': 'Vector Quantization Codebook Nearest Centroid'}},
 (4, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'source_filename is non-empty string',
                      'difficulty': 'Advance',
                      'explanation': 'Document metadata schemas for filtered vector store queries.',
                      'function_name': 'enrich_chunks_with_metadata',
                      'hint': 'Enumerate chunks, compute token_count with len(text.split()).',
                      'id': 'c4-m4-l1-a',
                      'prompt': 'Write `enrich_chunks_with_metadata(chunks, source_filename)` returning list of dicts '
                                '`{"chunk_id": f"{source_filename}_c{i}", "source": source_filename, "token_count": '
                                'len(text.split()), "text": text}`.',
                      'solution_code': 'def enrich_chunks_with_metadata(chunks: list, source_filename: str) -> list:\n'
                                       '    return [{"chunk_id": f"{source_filename}_c{i}", "source": source_filename, '
                                       '"token_count": len(c.split()), "text": c} for i, c in enumerate(chunks)]\n',
                      'starter_code': 'def enrich_chunks_with_metadata(chunks: list, source_filename: str) -> list:\n'
                                      '    # Return enriched chunk dicts\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Adds metadata',
                                      'expected': [{'chunk_id': 'doc.pdf_c0',
                                                    'source': 'doc.pdf',
                                                    'text': 'Hello world',
                                                    'token_count': 2},
                                                   {'chunk_id': 'doc.pdf_c1',
                                                    'source': 'doc.pdf',
                                                    'text': 'RAG pipelines rule',
                                                    'token_count': 3}],
                                      'input': [['Hello world', 'RAG pipelines rule'], 'doc.pdf']}],
                      'title': 'Chunk Metadata Enrichment'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'chunk_size > chunk_overlap >= 0',
                    'difficulty': 'Basic',
                    'explanation': 'LangChain CharacterTextSplitter document segmentation.',
                    'function_name': 'chunk_text_by_chars',
                    'hint': 'step = chunk_size - chunk_overlap. Loop while start < len(text).',
                    'id': 'c4-m4-l1-b',
                    'prompt': 'Write `chunk_text_by_chars(text, chunk_size, chunk_overlap)`: creates substrings of '
                              'length chunk_size, advancing by `chunk_size - chunk_overlap`. Disallow infinite loops '
                              '(advance >= 1).',
                    'solution_code': 'def chunk_text_by_chars(text: str, chunk_size: int, chunk_overlap: int) -> '
                                     'list:\n'
                                     '    step = max(1, chunk_size - chunk_overlap)\n'
                                     '    chunks = []\n'
                                     '    for i in range(0, len(text), step):\n'
                                     '        ch = text[i : i + chunk_size]\n'
                                     '        if ch: chunks.append(ch)\n'
                                     '        if i + chunk_size >= len(text): break\n'
                                     '    return chunks\n',
                    'starter_code': 'def chunk_text_by_chars(text: str, chunk_size: int, chunk_overlap: int) -> list:\n'
                                    '    # Return list of text chunks\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Advance by 3 each time',
                                    'expected': ['abcde', 'defgh', 'ghij'],
                                    'input': ['abcdefghij', 5, 2]}],
                    'title': 'Fixed-Length Text Chunker'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'markdown_text contains markdown headers',
                           'difficulty': 'Intermediate',
                           'explanation': 'LangChain MarkdownHeaderTextSplitter structured document chunking.',
                           'function_name': 'split_markdown_sections',
                           'hint': 'Iterate lines, track current header and accumulate content lines.',
                           'id': 'c4-m4-l1-i',
                           'prompt': 'Write `split_markdown_sections(markdown_text)` splitting on lines starting with '
                                     '`# ` (H1) or `## ` (H2). Return list of dicts `{"header": header_title, '
                                     '"content": section_text}`.',
                           'solution_code': 'def split_markdown_sections(markdown_text: str) -> list:\n'
                                            '    sections = []\n'
                                            '    curr_header, curr_lines = None, []\n'
                                            '    for line in markdown_text.splitlines():\n'
                                            '        if line.startswith("# ") or line.startswith("## "):\n'
                                            '            if curr_header:\n'
                                            '                sections.append({"header": curr_header, "content": '
                                            '"\\n".join(curr_lines).strip()})\n'
                                            '            curr_header = line.strip()\n'
                                            '            curr_lines = []\n'
                                            '        else:\n'
                                            '            curr_lines.append(line)\n'
                                            '    if curr_header:\n'
                                            '        sections.append({"header": curr_header, "content": '
                                            '"\\n".join(curr_lines).strip()})\n'
                                            '    return sections\n',
                           'starter_code': 'def split_markdown_sections(markdown_text: str) -> list:\n'
                                           '    # Return list of header sections\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Splits into 2 sections',
                                           'expected': [{'content': 'Intro text', 'header': '# Title'},
                                                        {'content': 'Details here', 'header': '## Section 1'}],
                                           'input': ['# Title\nIntro text\n## Section 1\nDetails here']}],
                           'title': 'Recursive Markdown Header Splitter'}},
 (4, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'doc_snippets is `{doc_id: snippet_text}`',
                      'difficulty': 'Advance',
                      'explanation': 'Perplexity-style inline academic source citation generation.',
                      'function_name': 'annotate_citations',
                      'hint': 'Count word overlaps with each doc, append best doc_id if overlap > 0.',
                      'id': 'c4-m4-l2-a',
                      'prompt': 'Write `annotate_citations(answer_sentences, doc_snippets)`: for each sentence, find '
                                'doc snippet with highest word overlap count. If overlap > 0, append ` [{doc_id}]` to '
                                'sentence. Return annotated text joined by space.',
                      'solution_code': 'def annotate_citations(answer_sentences: list, doc_snippets: dict) -> str:\n'
                                       '    annotated = []\n'
                                       '    for sent in answer_sentences:\n'
                                       '        s_words = set(sent.lower().replace(".", "").split())\n'
                                       '        best_doc, best_cnt = None, 0\n'
                                       '        for doc_id, snip in doc_snippets.items():\n'
                                       '            snip_words = set(snip.lower().split())\n'
                                       '            cnt = len(s_words & snip_words)\n'
                                       '            if cnt > best_cnt:\n'
                                       '                best_cnt = cnt\n'
                                       '                best_doc = doc_id\n'
                                       '        if best_doc:\n'
                                       '            annotated.append(f"{sent} [{best_doc}]")\n'
                                       '        else:\n'
                                       '            annotated.append(sent)\n'
                                       '    return " ".join(annotated)\n',
                      'starter_code': 'def annotate_citations(answer_sentences: list, doc_snippets: dict) -> str:\n'
                                      '    # Return text with citations\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Cites D1',
                                      'expected': 'LMS supports quizzes. [D1]',
                                      'input': [['LMS supports quizzes.'],
                                                {'D1': 'LMS supports interactive quizzes and coding challenges.'}]}],
                      'title': 'Source Citation Annotator'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'documents is non-empty list of strings',
                    'difficulty': 'Basic',
                    'explanation': 'Standard Retrieval-Augmented Generation context stuffing prompt template.',
                    'function_name': 'synthesize_rag_context',
                    'hint': 'Format each doc with [Doc i+1]: and join with newlines.',
                    'id': 'c4-m4-l2-b',
                    'prompt': 'Write `synthesize_rag_context(documents, query)` formatting: `Context:\\n[Doc 1]: '
                              '{d1}\\n[Doc 2]: {d2}...\\n\\nQuestion: {query}\\nAnswer:`',
                    'solution_code': 'def synthesize_rag_context(documents: list, query: str) -> str:\n'
                                     '    docs_str = "\\n".join(f"[Doc {i+1}]: {d}" for i, d in enumerate(documents))\n'
                                     '    return f"Context:\\n{docs_str}\\n\\nQuestion: {query}\\nAnswer:"\n',
                    'starter_code': 'def synthesize_rag_context(documents: list, query: str) -> str:\n'
                                    '    # Return grounded RAG prompt\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Builds standard context',
                                    'expected': 'Context:\n'
                                                '[Doc 1]: Antigravity is fast\n'
                                                '[Doc 2]: Antigravity has tools\n'
                                                '\n'
                                                'Question: What is Antigravity?\n'
                                                'Answer:',
                                    'input': [['Antigravity is fast', 'Antigravity has tools'],
                                              'What is Antigravity?']}],
                    'title': 'RAG Context Synthesizer'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'generated_answer is non-empty string',
                           'difficulty': 'Intermediate',
                           'explanation': 'RAG triad grounding / faithfulness automated verification heuristic.',
                           'function_name': 'detect_grounding_overlap',
                           'hint': 'Extract words as set(context_text.lower().split()), check generated words.',
                           'id': 'c4-m4-l2-i',
                           'prompt': 'Write `detect_grounding_overlap(generated_answer, context_text)`: compute '
                                     'fraction of words in generated_answer that appear in context_text '
                                     '(case-insensitive). Round to 2 decimals.',
                           'solution_code': 'def detect_grounding_overlap(generated_answer: str, context_text: str) -> '
                                            'float:\n'
                                            '    c_words = set(context_text.lower().split())\n'
                                            '    ans_words = generated_answer.lower().split()\n'
                                            '    if not ans_words: return 0.0\n'
                                            '    grounded = sum(1 for w in ans_words if w in c_words)\n'
                                            '    return round(grounded / len(ans_words), 2)\n',
                           'starter_code': 'def detect_grounding_overlap(generated_answer: str, context_text: str) -> '
                                           'float:\n'
                                           '    # Return grounding overlap fraction in [0, 1]\n'
                                           '    pass\n',
                           'test_cases': [{'desc': '3 of 6 words grounded -> 3/6 = 0.5',
                                           'expected': 0.5,
                                           'input': ['Paris is the capital of France', 'Paris is a city in France']}],
                           'title': 'Hallucination Lexical Overlap Check'}},
 (5, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'runnables is non-empty list of callables',
                      'difficulty': 'Advance',
                      'explanation': 'LangChain Expression Language (LCEL) chain piping `chain = prompt | model | '
                                     'parser`.',
                      'function_name': 'run_lcel_pipe',
                      'hint': 'Loop over runnables and update curr = fn(curr).',
                      'id': 'c4-m5-l1-a',
                      'prompt': 'Write `run_lcel_pipe(initial_input, runnables)` sequentially passing output of '
                                'runnable `i` as input to `i+1`. Each runnable is a function or lambda.',
                      'solution_code': 'def run_lcel_pipe(initial_input, runnables: list):\n'
                                       '    curr = initial_input\n'
                                       '    for r in runnables:\n'
                                       '        curr = r(curr)\n'
                                       '    return curr\n',
                      'starter_code': 'def run_lcel_pipe(initial_input, runnables: list):\n'
                                      '    # Return final output\n'
                                      '    pass\n',
                      'test_cases': [{'desc': '(10+5)*2 = 30',
                                      'expected': 30,
                                      'input': [10, [3, 2]]}],
                      'title': 'Runnable Sequence LCEL Pipe Runner'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'all template variables present in variables_dict',
                    'difficulty': 'Basic',
                    'explanation': 'LangChain PromptTemplate.format() variable substitution.',
                    'function_name': 'render_langchain_template',
                    'hint': 'template_str.format(**variables_dict)',
                    'id': 'c4-m5-l1-b',
                    'prompt': 'Write `render_langchain_template(template_str, variables_dict)` substituting '
                              '`{var_name}` with its string value in variables_dict.',
                    'solution_code': 'def render_langchain_template(template_str: str, variables_dict: dict) -> str:\n'
                                     '    return template_str.format(**variables_dict)\n',
                    'starter_code': 'def render_langchain_template(template_str: str, variables_dict: dict) -> str:\n'
                                    '    # Return formatted string\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Substitutes name and count',
                                    'expected': 'Hello Zee, you have 5 alerts.',
                                    'input': ['Hello {name}, you have {count} alerts.', {'count': 5, 'name': 'Zee'}]}],
                    'title': 'LangChain PromptTemplate Formatter'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'raw_output is string',
                           'difficulty': 'Intermediate',
                           'explanation': 'LangChain JsonOutputParser robustness against LLM code block artifacts.',
                           'function_name': 'parse_json_markdown_output',
                           'hint': 'Strip code fences and use json.loads inside try-except.',
                           'id': 'c4-m5-l1-i',
                           'prompt': 'Write `parse_json_markdown_output(raw_output)` stripping surrounding ```json ... '
                                     '``` code fence if present, then parsing JSON into a Python dict. If invalid '
                                     'return `{}`.',
                           'solution_code': 'def parse_json_markdown_output(raw_output: str) -> dict:\n'
                                            '    import json\n'
                                            '    cleaned = raw_output.strip()\n'
                                            '    if cleaned.startswith("```json"):\n'
                                            '        cleaned = cleaned[len("```json"):].strip()\n'
                                            '    if cleaned.startswith("```"):\n'
                                            '        cleaned = cleaned[3:].strip()\n'
                                            '    if cleaned.endswith("```"):\n'
                                            '        cleaned = cleaned[:-3].strip()\n'
                                            '    try:\n'
                                            '        return json.loads(cleaned)\n'
                                            '    except Exception:\n'
                                            '        return {}\n',
                           'starter_code': 'def parse_json_markdown_output(raw_output: str) -> dict:\n'
                                           '    # Return parsed dictionary\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Extracts JSON from markdown fences',
                                           'expected': {'code': 200, 'status': 'ok'},
                                           'input': ['```json\n{"status": "ok", "code": 200}\n```']}],
                           'title': 'JsonOutputParser Markdown Stripper'}},
 (5, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'each valid line enclosed in parentheses with commas',
                      'difficulty': 'Advance',
                      'explanation': 'ConversationKnowledgeGraphMemory semantic triple storage.',
                      'function_name': 'extract_entity_triples',
                      'hint': 'Strip parens, split by comma, strip each part.',
                      'id': 'c4-m5-l2-a',
                      'prompt': 'Write `extract_entity_triples(triples_text)` where text has lines `(Subject, '
                                'Predicate, Object)`. Parse into list of dicts `{"subject": s, "predicate": p, '
                                '"object": o}` with whitespace stripped.',
                      'solution_code': 'def extract_entity_triples(triples_text: str) -> list:\n'
                                       '    res = []\n'
                                       '    for line in triples_text.splitlines():\n'
                                       '        l = line.strip()\n'
                                       '        if l.startswith("(") and l.endswith(")"):\n'
                                       '            parts = [p.strip() for p in l[1:-1].split(",")]\n'
                                       '            if len(parts) == 3:\n'
                                       '                res.append({"subject": parts[0], "predicate": parts[1], '
                                       '"object": parts[2]})\n'
                                       '    return res\n',
                      'starter_code': 'def extract_entity_triples(triples_text: str) -> list:\n'
                                      '    # Return list of triple dicts\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Extracts 2 triples',
                                      'expected': [{'object': 'Google', 'predicate': 'WorksAt', 'subject': 'Alice'},
                                                   {'object': 'NYC', 'predicate': 'LivesIn', 'subject': 'Bob'}],
                                      'input': ['(Alice, WorksAt, Google)\n(Bob, LivesIn, NYC)']}],
                      'title': 'Entity Memory Knowledge Graph Extraction'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'k >= 1',
                    'difficulty': 'Basic',
                    'explanation': 'LangChain ConversationBufferWindowMemory token conservation.',
                    'function_name': 'conversation_window_memory',
                    'hint': 'Slice history[-k:]',
                    'id': 'c4-m5-l2-b',
                    'prompt': 'Write `conversation_window_memory(history, k)` returning the last `k` conversation '
                              'turns (each turn is `[user_msg, ai_msg]`). If len(history) <= k, return all.',
                    'solution_code': 'def conversation_window_memory(history: list, k: int) -> list:\n'
                                     '    return history[-k:] if k > 0 else []\n',
                    'starter_code': 'def conversation_window_memory(history: list, k: int) -> list:\n'
                                    '    # Return last k turns\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Keeps last 2 turns',
                                    'expected': [['question', 'answer'], ['thanks', 'welcome']],
                                    'input': [[['hi', 'hello'], ['question', 'answer'], ['thanks', 'welcome']], 2]}],
                    'title': 'Conversation Buffer Window Memory'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'max_tokens >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Sliding window context truncation preventing context window overflow.',
                           'function_name': 'compact_memory_by_budget',
                           'hint': 'Iterate from back, accumulate words until exceeding budget, reverse kept.',
                           'id': 'c4-m5-l2-i',
                           'prompt': 'Write `compact_memory_by_budget(messages, max_tokens)`: keeping newest messages '
                                     'whose combined word count is <= max_tokens. Return kept messages in original '
                                     'chronological order.',
                           'solution_code': 'def compact_memory_by_budget(messages: list, max_tokens: int) -> list:\n'
                                            '    kept = []\n'
                                            '    cur_tokens = 0\n'
                                            '    for m in reversed(messages):\n'
                                            '        tokens = len(m.split())\n'
                                            '        if cur_tokens + tokens <= max_tokens:\n'
                                            '            kept.append(m)\n'
                                            '            cur_tokens += tokens\n'
                                            '        else:\n'
                                            '            break\n'
                                            '    return list(reversed(kept))\n',
                           'starter_code': 'def compact_memory_by_budget(messages: list, max_tokens: int) -> list:\n'
                                           '    # Return messages within budget\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Keeps 5 words total',
                                           'expected': ['Middle context here', 'Newest prompt'],
                                           'input': [['Old greeting here', 'Middle context here', 'Newest prompt'],
                                                     5]}],
                           'title': 'Memory Token Budget Compactor'}},
 (6, 1): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'all strings non-empty',
                      'difficulty': 'Advance',
                      'explanation': 'OpenAI Chat Completions API protocol tool response serialization.',
                      'function_name': 'format_tool_response_message',
                      'hint': 'Return dictionary with role="tool" and content=str(result).',
                      'id': 'c4-m6-l1-a',
                      'prompt': 'Write `format_tool_response_message(tool_call_id, tool_name, result)` returning '
                                'OpenAI format: `{"role": "tool", "tool_call_id": tool_call_id, "name": tool_name, '
                                '"content": str(result)}`.',
                      'solution_code': 'def format_tool_response_message(tool_call_id: str, tool_name: str, result) -> '
                                       'dict:\n'
                                       '    return {"role": "tool", "tool_call_id": tool_call_id, "name": tool_name, '
                                       '"content": str(result)}\n',
                      'starter_code': 'def format_tool_response_message(tool_call_id: str, tool_name: str, result) -> '
                                      'dict:\n'
                                      '    # Return tool message dict\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Formats tool result message',
                                      'expected': {'content': "{'temp': 72}",
                                                   'name': 'get_weather',
                                                   'role': 'tool',
                                                   'tool_call_id': 'call_123'},
                                      'input': ['call_123', 'get_weather', {'temp': 72}]}],
                      'title': 'Tool Result Message Formatter'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'tool_call is dict with "name" and "arguments" dict',
                    'difficulty': 'Basic',
                    'explanation': 'Pydantic / OpenAI function calling parameter validation.',
                    'function_name': 'validate_tool_call_schema',
                    'hint': 'all(p in tool_call.get("arguments", {}) for p in required_params)',
                    'id': 'c4-m6-l1-b',
                    'prompt': 'Write `validate_tool_call_schema(tool_call, required_params)` checking if '
                              '`tool_call["arguments"]` contains all required_params. Return True if valid, False '
                              'otherwise.',
                    'solution_code': 'def validate_tool_call_schema(tool_call: dict, required_params: list) -> bool:\n'
                                     '    args = tool_call.get("arguments", {})\n'
                                     '    return all(p in args for p in required_params)\n',
                    'starter_code': 'def validate_tool_call_schema(tool_call: dict, required_params: list) -> bool:\n'
                                    '    # Return True if valid schema\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Has required query',
                                    'expected': True,
                                    'input': [{'arguments': {'query': 'python'}, 'name': 'search'}, ['query']]}],
                    'title': 'OpenAI Tool Call Schema Validator'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'tool_registry is dict of {str: callable}',
                           'difficulty': 'Intermediate',
                           'explanation': 'Agent runtime tool dispatcher executing LLM requested functions.',
                           'function_name': 'dispatch_tool_call',
                           'hint': 'Check if tool_name in tool_registry, call with **arguments.',
                           'id': 'c4-m6-l1-i',
                           'prompt': 'Write `dispatch_tool_call(tool_name, arguments, tool_registry)`: executes '
                                     '`tool_registry[tool_name](**arguments)` if registered, else returns `{"error": '
                                     'f"Tool {tool_name} not found"}`.',
                           'solution_code': 'def dispatch_tool_call(tool_name: str, arguments: dict, tool_registry: '
                                            'dict):\n'
                                            '    if tool_name not in tool_registry:\n'
                                            '        return {"error": f"Tool {tool_name} not found"}\n'
                                            '    try:\n'
                                            '        return tool_registry[tool_name](**arguments)\n'
                                            '    except Exception as e:\n'
                                            '        return {"error": str(e)}\n',
                           'starter_code': 'def dispatch_tool_call(tool_name: str, arguments: dict, tool_registry: '
                                           'dict):\n'
                                           '    # Return tool execution result\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Executes add',
                                           'expected': 8,
                                           'input': ['add',
                                                     {'a': 5, 'b': 3},
                                                     {'add': "dummy_callable"}]}],
                           'title': 'Dynamic Tool Dispatcher'}},
 (6, 2): {'advance': {'badge_class': 'bg-purple',
                      'constraints': 'steps is list of dicts',
                      'difficulty': 'Advance',
                      'explanation': 'Agent scratchpad history maintaining execution state across turns.',
                      'function_name': 'format_agent_scratchpad',
                      'hint': 'Join formatted blocks with "\\n\\n".',
                      'id': 'c4-m6-l2-a',
                      'prompt': 'Write `format_agent_scratchpad(steps)` where each step is `{"thought": str, "action": '
                                'str, "observation": str}`. Return formatted string: `Thought: {t}\\nAction: '
                                '{a}\\nObservation: {o}` for each step separated by double newlines.',
                      'solution_code': 'def format_agent_scratchpad(steps: list) -> str:\n'
                                       '    blocks = [f"Thought: {s[\'thought\']}\\nAction: '
                                       '{s[\'action\']}\\nObservation: {s[\'observation\']}" for s in steps]\n'
                                       '    return "\\n\\n".join(blocks)\n',
                      'starter_code': 'def format_agent_scratchpad(steps: list) -> str:\n'
                                      '    # Return formatted scratchpad\n'
                                      '    pass\n',
                      'test_cases': [{'desc': 'Single turn scratchpad',
                                      'expected': 'Thought: Check weather\nAction: get_temp("SF")\nObservation: 65F',
                                      'input': [[{'action': 'get_temp("SF")',
                                                  'observation': '65F',
                                                  'thought': 'Check weather'}]]}],
                      'title': 'ReAct Agent Scratchpad Formatter'},
          'basic': {'badge_class': 'bg-success',
                    'constraints': 'llm_output contains Thought: and Action:',
                    'difficulty': 'Basic',
                    'explanation': 'Yao et al. ReAct (Reason + Act) autonomous agent loop parsing.',
                    'function_name': 'parse_react_step',
                    'hint': 'Extract lines starting with Thought: and Action:.',
                    'id': 'c4-m6-l2-b',
                    'prompt': 'Write `parse_react_step(llm_output)` extracting `"Thought: ..."` and `"Action: ..."` '
                              'from output. Return `{"thought": thought_str, "action": action_str}`.',
                    'solution_code': 'def parse_react_step(llm_output: str) -> dict:\n'
                                     '    t, a = "", ""\n'
                                     '    for line in llm_output.splitlines():\n'
                                     '        l = line.strip()\n'
                                     '        if l.startswith("Thought:"): t = l[len("Thought:"):].strip()\n'
                                     '        elif l.startswith("Action:"): a = l[len("Action:"):].strip()\n'
                                     '    return {"thought": t, "action": a}\n',
                    'starter_code': 'def parse_react_step(llm_output: str) -> dict:\n'
                                    '    # Return thought and action dict\n'
                                    '    pass\n',
                    'test_cases': [{'desc': 'Parses ReAct output',
                                    'expected': {'action': 'search("python")', 'thought': 'I need to search.'},
                                    'input': ['Thought: I need to search.\n'
                                              'Action: search("python")\n'
                                              'Observation: ...']}],
                    'title': 'ReAct Agent Thought-Action Parser'},
          'intermediate': {'badge_class': 'bg-primary',
                           'constraints': 'current_iteration >= 1, max_iterations >= 1',
                           'difficulty': 'Intermediate',
                           'explanation': 'Infinite loop prevention circuit breaker in autonomous agents.',
                           'function_name': 'is_agent_loop_terminated',
                           'hint': 'Check >= max_iterations or action == "FINISH".',
                           'id': 'c4-m6-l2-i',
                           'prompt': 'Write `is_agent_loop_terminated(current_iteration, max_iterations, '
                                     'last_action)`: returns True if current_iteration >= max_iterations OR '
                                     'last_action == "FINISH", else False.',
                           'solution_code': 'def is_agent_loop_terminated(current_iteration: int, max_iterations: int, '
                                            'last_action: str) -> bool:\n'
                                            '    return current_iteration >= max_iterations or last_action == '
                                            '"FINISH"\n',
                           'starter_code': 'def is_agent_loop_terminated(current_iteration: int, max_iterations: int, '
                                           'last_action: str) -> bool:\n'
                                           '    # Return True if agent should stop\n'
                                           '    pass\n',
                           'test_cases': [{'desc': 'Terminates on max iterations',
                                           'expected': True,
                                           'input': [5, 5, 'search()']},
                                          {'desc': 'Terminates on FINISH action',
                                           'expected': True,
                                           'input': [2, 10, 'FINISH']}],
                           'title': 'Agent Max Iterations Safeguard'}}}
