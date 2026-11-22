# Lecture 05 Answers

## Exercises

- Answering model (`[model]` shown during execution): gemini-3.5-flash-lite
- Comparison question: "In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?"
- Target materials: Full context used all 8 documents and 398 pages supplied in lectures.json. Vector search, Tree, and Graph used the 214-page bundle for Lectures 01-03. These methods therefore did not have identical scope; the full-context prompt used 369,491 characters and 95,824 input tokens.

### Verified Answer

- LoRA freezes the original/pretrained weights (W). It does not update those weights.
- LoRA trains only the small added low-rank matrices (A) and (B); their product represents the weight change. The trainable portion can be less than 1% of the total model.
- QLoRA adds 4-bit compression/quantization of the original base weights, keeping memory use lower while LoRA adapters are trained. The direct evidence is lec02-main-p052 (Japanese source p.52; corresponding translated PDF p.75).

### Results by Method

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---:|---:|---:|---:|
| Full context | Correct. LoRA freezes the original weights and trains only the low-rank A and B matrices. QLoRA additionally quantizes/compresses the frozen base weights to 4 bits. | Lecture 2, translated PDF p.75 / lec02-main-p052 | 2.94 | 95,824 / 178 | 1 | $0.029192 |
| Vector search | Correct and concise. The answer identified frozen original weights, trainable A and B matrices, and 4-bit base-weight compression. | Directly retrieved lec02-main-p052; p.51 was found by search alone but was not the direct tool-return citation. | 2.77 | 2,759 / 197 | 2 | $0.001320 |
| Tree | Retrieval succeeded, but the answer was incomplete/directness failed. It reached p.52 and phrased the facts as questions and hints instead of delivering the direct answer. | Retrieved lec02-main-p052, "LoRA and QLoRA: adapting a large model on one GPU" | 4.44 | 9,442 / 287 | 5 | $0.003550 |
| Graph | Correct and concise. It returned the frozen original weights, trainable low-rank matrices A and B, and 4-bit compression. | lec02-main-p052; Japanese source p.52 / translated PDF p.75 | 5.41 | 5,188 / 202 | 2 | $0.002061 |

<!-- State when a method was not run or a cost was unavailable. Use a separate table for each additional question. -->

- Pages found by running search alone, and what their text confirmed:
  - lec02-main-p052 is the direct evidence page. It states that LoRA freezes the original weights and trains only matrices A and B, while QLoRA quantizes/compresses the original weights to 4 bits.
  - lec02-main-p051 provides the broader PEFT comparison: LoRA freezes the base model and adds a small trainable component, while QLoRA adds 4-bit compression.
  - p.60 and p.61 are related to the QLoRA exercise but do not improve the conceptual answer.
- Tool calls shown by --trace:
  - Full context made no retrieval tool calls.
  - Vector search called search_materials({'query': 'LoRA freeze train QLoRA add'}) once.
  - Tree called browse_tree for the root, lec02-main, lec02-main-s045, and lec02-main-p052.
  - Graph called search_graph({'query': 'Lecture 02 LoRA freeze train QLoRA'}) once.
- Examples where retrieved information was insufficient, or was retrieved but not used in the answer:
  - The initial Vector and Tree runs encountered HTTP 503 responses and were rerun successfully.
  - Tree retrieved p.52 but the agent's learning-support instructions kept the response at hint level rather than a direct answer.
  - Vector search found some adjacent or exercise pages, but p.52 alone was sufficient to answer the question.
- Method I would adopt for this use case: Graph or Vector search. Both were correct and used less input than full context. Vector search was fastest and least expensive. Graph is useful when an answer may span related terms or adjacent slides, but for this direct two-sentence fact, the extra expansion is unnecessary.
- Observations and limitations:
  - Full context used much more input and cost, but produced the clearest complete answer.
  - This is a one-question comparison, so it cannot establish which method is generally best.
  - API 503 responses and model variability may affect exact time and cost values.

### Additional Comparison Question: Memory and Compaction

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---:|---:|---:|---:|
| Basic Vector RAG | Correct. Compaction summarizes history within the same session; memory uses external storage across sessions. It also stated that daily notes are filtered before entering long-term memory. | First call: p.65 and p.39; second call: p.40 | 3.99 | 6,043 / 282 | 3 | $0.002518 |
| Advanced Hybrid RAG | Correct. It gave the same distinctions and directly cited the Claude and OpenClaw examples. | p.39 for same-session compaction and cross-session memory; p.40 for selective nightly promotion; p.65 also supported the mechanism | 7.57 | 4,780 / 373 | 2 | $0.002366 |

## Homework

- Level attempted: Advanced
- What I did:
  - Implemented a Hybrid retrieval mode in [app/retrieval.py](/workspaces/lecture-ai-engineering-2026-en/app/retrieval.py).
  - Added search_hybrid in [app/tools.py](/workspaces/lecture-ai-engineering-2026-en/app/tools.py).
  - Added HYBRID_INSTRUCTIONS and the hybrid agent mode in [app/agent.py](/workspaces/lecture-ai-engineering-2026-en/app/agent.py).
  - Added a focused unit test in [tests/test_tools.py](/workspaces/lecture-ai-engineering-2026-en/tests/test_tools.py).
- Comparison question and conditions held fixed:
  - "In Lecture 03, how does compaction differ from memory across sessions? Do all daily notes go into long-term memory?"
  - Model: gemini-3.5-flash-lite
  - Target: Lectures 01-03 bundled materials
  - Normal RAG: search_materials with the default RAG_TOP_K
  - Advanced RAG: vector seeds, Graph expansion, and ±1 adjacent pages within the same document
- Data structure and retrieval design:
  - Pages are stored as JSON by document, section, and page in lectures.json.
  - The Graph data stores page nodes and relationships for adjacent pages and shared terms.
  - The Hybrid method:
    1. Takes the top 3 vector-search seeds.
    2. Runs Graph expansion with 2 hops.
    3. Adds the immediately preceding and following pages within the same document.
    4. Deduplicates page IDs and limits the merged result to the existing Graph maximum of 10 pages.
  - Optimization: search_hybrid now passes its already-computed vector seeds into Graph expansion, so the query is embedded once instead of twice.
- Results:
  - Search alone retrieved p.65, p.39, p.38, p.40, and p.13. This already contained a nearly complete evidence set.
  - Basic RAG answered correctly after two search_materials calls.
  - Hybrid RAG answered correctly with one search_hybrid call and cited p.39 and p.40, which directly distinguish compaction, cross-session memory, and selective promotion to long-term memory.
  - Hybrid RAG used less input and cost but more output and slightly more time than Basic RAG.
- Examples of improvements and remaining failures or limitations:
  - Improvement: the pipeline deliberately retains adjacent context, reducing the chance that p.40 is isolated from the p.39 comparison.
  - Improvement: the agent received a page set identified through vector, graph, and adjacency sources rather than one retrieval ranking alone.
  - Remaining failure: the adjacent-page rule is generic and may include irrelevant neighboring slides.
  - Residual limitation: Graph expansion and adjacent-page ranking are fixed heuristics; a production system could tune hop count, result limit, and adjacency weight using a held-out evaluation set.
  - Remaining limitation: no ground-truth answer set or repeated-run benchmark was used, so these results measure only this run.
- Verification:
  - Focused tests passed: 10 passed.
  - The new retrieval test verified that a vector seed and a ±1 adjacent page are both returned and deduplicated.
- Observations and questions:
  - Hybrid retrieval is reasonable for multi-slide explanatory or comparative questions.
  - It is less useful for short factual questions such as LoRA/QLoRA, where the direct p.52 page alone is sufficient.
  - Adoption decision: adopt it selectively for comparison and cross-page questions, not as the default for every query.
