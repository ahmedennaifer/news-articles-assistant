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
