Benchmark 1: Naive RAG

params:

  - chunking: none
  - embeder: all-MiniLM-L6-v2 
  - retriever: embedding retriever, top_k=5
  - prompt: naive_rag_prompt
  - llm: llama3.1 70B
  - meta: none

Results:

MRR: 
