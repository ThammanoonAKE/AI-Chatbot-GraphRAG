# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an advanced AI-powered Thai legal case search system with **GraphRAG (Graph Retrieval-Augmented Generation)** that combines:
- **React frontend** with Material-UI and glass morphism design
- **FastAPI backend** (main.py) with GraphRAG capabilities
- **Knowledge Graph** for understanding relationships between legal entities
- **FAISS vector search** enhanced with graph-based context
- **Thai legal case data** stored as JSON files (1000 cases in json_cases/)
- **Google Gemini AI** for advanced legal analysis and reasoning

## Architecture

### Core Components
- `main.py` - Main FastAPI application with GraphRAG and enhanced search capabilities
- `src/graphrag/` - GraphRAG implementation with knowledge graph and retriever
- `src/components/` - React frontend components with Material-UI
- `json_cases/` - Directory containing 1000 Thai legal case files (1.json to 1000.json)
- `data/embeddings/` - Vector embeddings, FAISS index, and metadata
- `data/graphs/` - Knowledge graph data and community structures
- `package.json` & `vite.config.js` - React/Vite frontend configuration

### Search Types
The system supports 6 search modes via `SearchType` enum:
- `SIMILARITY` - Semantic vector search using embeddings
- `CASE_NUMBER` - Exact case number matching (format: xxxx/yyyy)  
- `JUDGE` - Judge name matching with fuzzy logic
- `CASE_TYPE` - Case type filtering (อาญา, แพ่ง, แรงงาน, ภาษี, etc.)
- `GRAPHRAG` - Enhanced search with knowledge graph traversal and context
- `COMBINED` - Intelligent hybrid search with GraphRAG integration (default)

### Key Functions
- `load_documents_from_folder()` - Processes JSON files into searchable chunks
- `search_similar_cases()` - Vector similarity search using FAISS
- `search_with_graphrag()` - GraphRAG-enhanced search with knowledge graph context
- `search_by_case_number()` - Direct case number lookup
- `search_by_judge()` - Judge name search with normalization
- `generate_response()` - AI chat with GraphRAG-enhanced legal context

### GraphRAG Components
- `LegalKnowledgeGraph` - Builds and manages knowledge graph from legal cases
- `GraphRAGRetriever` - Combines vector search with graph traversal for enhanced results
- Community detection using Louvain algorithm for clustering related cases
- Relationship extraction between cases, judges, legal concepts, and case types

## Development Setup

### Environment
- **Python 3.10+** (confirmed working version)
- **Node.js 16+** for React frontend
- **Virtual environment**: `venv/` directory (already configured)

### Required Dependencies
Install dependencies using the provided files:

**Python Backend:**
```bash
pip install -r requirements.txt
```

**React Frontend:**
```bash
npm install
```

### Key Python Packages
- `fastapi` & `uvicorn` - Web framework and server
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Text embeddings
- `google-generativeai` - Gemini AI integration
- `networkx` - Knowledge graph processing
- `community` - Graph community detection
- `python-dotenv` - Environment variable management

### Running the Application

**Backend (Terminal 1):**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Start FastAPI server
python main.py
```
- Runs on http://localhost:8000
- Auto-loads and indexes case data on first run
- Builds knowledge graph automatically
- API docs available at http://localhost:8000/docs

**Frontend (Terminal 2):**
```bash
# Start React development server
npm run dev
```
- React app runs on http://localhost:3000
- Connects to backend API automatically via proxy
- Hot reloading for development

### Data Processing
- Case JSON files are automatically processed into text chunks
- FAISS index is built on first run and cached in `data/embeddings/`
- Knowledge graph is constructed and saved in `data/graphs/`
- Embeddings use `all-MiniLM-L6-v2` model
- Thai text normalization and keyword extraction applied
- Community detection groups related legal entities

## API Endpoints

**Core Endpoints:**
- `POST /chat` - Main chat interface with GraphRAG-enhanced AI responses
- `POST /search` - Advanced multi-criteria search with GraphRAG
- `GET /search/case/{case_number}` - Case number lookup
- `GET /search/judge/{judge_name}` - Judge-based search
- `GET /search/type/{case_type}` - Case type filtering
- `GET /info/statistics` - System and graph statistics
- `GET /graph/stats` - Knowledge graph statistics

## Security Considerations

✅ **Environment Variables**: The Gemini API key is now properly stored in `.env` file and loaded using `python-dotenv`. Never commit `.env` file to version control.

## Thai Language Processing

The system includes specialized Thai text processing:
- Unicode normalization for Thai characters
- Legal keyword extraction (มาตรา, คดี, etc.)
- Judge name normalization with title removal
- Case type detection using pattern matching

## Performance Notes

- Index building can take time on first run (1000+ cases)
- FAISS uses IVF (Inverted File) index for fast similarity search
- Text chunking with overlap for better context matching
- Batch processing for embeddings generation

## Testing

Test the system by:
1. **Backend**: Run `python main.py` and verify server starts with GraphRAG initialization
2. **Frontend**: Run `npm run dev` and test React interface at http://localhost:3000
3. **API Testing**: Use API docs at http://localhost:8000/docs for endpoint testing
4. **GraphRAG Testing**: Query with Thai legal terms and verify graph-enhanced results
5. **Graph Stats**: Check `/graph/stats` endpoint to verify knowledge graph is built correctly

## Modular Architecture

The codebase has been refactored into a clean modular structure:

### 📁 Core Modules
- `src/config.py` - Configuration management and environment variables
- `src/search/` - All search engines (vector, traditional, GraphRAG, manager)
- `src/ai/` - AI response generation with Gemini
- `src/models/` - Data models, enums, and Pydantic schemas
- `src/api/` - FastAPI routes and endpoints
- `src/processing/` - Text processing and data loading utilities
- `src/graphrag/` - Knowledge graph and GraphRAG implementation

### 🚀 Running Commands
```bash
# Setup everything
npm run setup

# Run full stack (recommended)
python run_dev.py

# Or run separately:
# Backend: python main.py
# Frontend: npm run dev
```

### 📖 Architecture Documentation
- `ARCHITECTURE.md` - Detailed system architecture and module breakdown
- `README.md` - User-facing documentation and setup guide

## Configuration Files

- `.env` - Environment variables (API keys, paths, parameters)
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies and scripts
- `vite.config.js` - Frontend build configuration
- `.gitignore` - Excludes sensitive and generated files
- `run_dev.py` - Development startup script