Benchmark 1: Naive RAG

params:
  - chunking: none
  - embeder: all-MiniLM-L6-v2
  - retriever: embedding retriever, top_k=5
  - prompt: naive_rag_prompt
  - llm: llama3.1 70B
  - meta: none
  - no sources and not tool reference from prompt
  -------------------------------------------------
  - MRR: 0.73
  - individual MRR: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.25, 1.0, 1.0, 0.5, 0.5, 0.25, 1.0, 0.2, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0]


Benchmark 2: Reranker

  - chunking: none
  - embeder: all-MiniLM-L6-v2
  - retriever: embedding retriever, top_k=5
  - prompt: naive_rag_prompt
  - llm: llama3.1 70B
  - meta: none
  - better prompt for sources and docs
  - reranker topk_k = 5
  -------------------------------------------------
  - MRR: 0.79
  -individual MRR: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0]


Benchmark 3: Reranker + topk = 10

  - chunking: none
  - embeder: all-MiniLM-L6-v2
  - retriever: embedding retriever, top_k=10
  - prompt: naive_rag_prompt
  - llm: llama3.1 70B
  - meta: none
  - better prompt for sources and docs
  - reranker topk_k = 10
  -------------------------------------------------
  - MRR: 0.79
  - individual MRR: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0]

Thoughts:

  Questions:
    - "What was the book value of IMF gold reserves compared to their market value?",
    - "Which country expressed the ability to veto plans to sell IMF gold?",
    - "What did Gordon Brown call the meeting where G7 finance ministers backed debt relief plans?",
  have 0 score

Benchmark 4: Automatic metadata extraction

  - chunking: none
  - embeder: all-MiniLM-L6-v2
  - retriever: embedding retriever, top_k=10
  - prompt: naive_rag_prompt
  - llm: llama3.1 70B
  - meta: none
  - better prompt for sources and docs
  - reranker topk_k = 10
  -------------------------------------------------
  - MRR: 0.79
  - individual MRR: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0]


Benchmark 5: HyDE

  - chunking: none
  - embeder: all-MiniLM-L6-v2
  - retriever: embedding retriever, top_k=10
  - prompt: naive_rag_prompt
  - llm: llama3.1 70B
  - meta: none
  - better prompt for sources and docs
  - reranker topk_k = 10
  -------------------------------------------------
  - MRR: 0.79
  - individual MRR: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.25, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0]
