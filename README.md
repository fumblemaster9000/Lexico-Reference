# Lexico-Reference
## Project Directory Architecture

multi-format-rag-pipeline/
├── data/                  # Local directory for dropping raw test documents
├── src/                   # Source directory holding isolated logical modules
│   ├── __init__.py        # Initializes 'src' as an importable Python package
│   ├── parser.py          # Multi-format routing, text extraction, and OCR fallback
│   ├── splitter.py        # Recursive text chunking and overlap management
│   ├── retriever.py       # ChromaDB vector initialization, BM25 indexing, and RRF math
│   └── pipeline.py        # Context prompt orchestration and LLM connection bindings
├── .gitignore             # Tells Git to ignore system caches, virtual environments, and keys
├── main.py                # System entry point launching the FastAPI Web Server environment
└── requirements.txt       # Unified index of external framework dependencies