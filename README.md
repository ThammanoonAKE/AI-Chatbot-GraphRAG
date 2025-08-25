# Thai Legal Case Search System with GraphRAG

🏛️ **Advanced Thai Legal Case Search System with GraphRAG and React Frontend**

A sophisticated AI-powered chatbot that combines **GraphRAG (Graph Retrieval-Augmented Generation)** with traditional vector search to provide intelligent legal case analysis and recommendations for Thai legal documents.

## ✨ Key Features

### 🧠 GraphRAG Technology
- **Knowledge Graph Construction**: Automatically builds relationships between cases, judges, legal concepts, and case types
- **Community Detection**: Identifies clusters of related cases using Louvain algorithm
- **Enhanced Search**: Combines vector similarity search with graph-based context
- **Relationship Analysis**: Discovers hidden connections between legal entities

### 🔍 Advanced Search Capabilities
- **Multi-Modal Search**: Case numbers, judge names, case types, legal concepts
- **Semantic Search**: Vector embeddings using Sentence Transformers
- **Graph-Enhanced Results**: Additional related cases from knowledge graph traversal
- **Intelligent Intent Detection**: Automatically determines search strategy based on query

### 🎯 AI-Powered Analysis
- **Google Gemini Integration**: Advanced legal text analysis and reasoning
- **Contextual Responses**: Uses both vector and graph context for comprehensive answers
- **Thai Language Support**: Specialized Thai text processing and normalization
- **Legal Domain Expertise**: Focus on Thai legal terminology and concepts

### 🖥️ Modern Web Interface
- **React 18**: Modern, responsive user interface
- **Material-UI**: Professional design components
- **Framer Motion**: Smooth animations and transitions
- **Glass Morphism**: Beautiful visual effects
- **Real-time Chat**: Interactive conversational interface

## 🏗️ Architecture

```
Thai Legal GraphRAG System
├── Frontend (React + Vite)
│   ├── React Components
│   ├── Material-UI Design
│   └── API Integration
├── Backend (FastAPI + Python)
│   ├── GraphRAG Engine
│   ├── Vector Search (FAISS)
│   ├── Knowledge Graph (NetworkX)
│   └── AI Integration (Gemini)
└── Data Processing
    ├── Thai Legal Cases (JSON)
    ├── Vector Embeddings
    └── Knowledge Graph
```

## 📦 Installation

### Prerequisites
- **Python 3.11+**
- **Node.js 16+**
- **Git**

### 1. Clone Repository
```bash
git clone https://github.com/your-username/AI-Chatbot-GraphRAG.git
cd AI-Chatbot-GraphRAG
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
# Install Node.js dependencies
npm install
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
# Required: GEMINI_API_KEY
```

### 5. Data Preparation
- Place Thai legal case JSON files in the `json_cases/` directory
- Each JSON file should contain case metadata (decision_id, title, summary, judges, etc.)

## 🚀 Running the Application

### Development Mode

#### Start Backend (Terminal 1)
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Start FastAPI server
python main.py
```
Backend runs at: `http://localhost:8000`

#### Start Frontend (Terminal 2)
```bash
# Start React development server
npm run dev
```
Frontend runs at: `http://localhost:3000`

### Production Mode
```bash
# Build React frontend
npm run build

# Start production server
python main.py
```

## 🚀 Deployment

### Backend on Render
- Configured with `render.yaml` for easy deployment
- Supports Python 3.11 with optimized dependencies
- Auto-builds embeddings and knowledge graph on startup

### Frontend on Vercel
- Configured with `vercel.json` for seamless deployment
- Environment variables for backend API connection
- Global CDN for fast worldwide access

## 📊 GraphRAG Components

### Knowledge Graph Structure
- **Nodes**: Cases, Judges, Legal Concepts, Case Types, Related Articles
- **Edges**: Relationships like "contains", "handles", "similar_to", "related_to"
- **Communities**: Automatically detected clusters of related entities

### Graph-Enhanced Search
1. **Vector Search**: Initial retrieval based on similarity
2. **Graph Traversal**: Find related entities through knowledge graph
3. **Community Context**: Include entities from same community
4. **Relevance Scoring**: Combine vector and graph-based scores

### Relationship Types
- `contains`: Case contains legal concepts/judges
- `handles`: Judge handles case types
- `similar_to`: High similarity between cases
- `deals_with`: Judge deals with legal concepts
- `related`: General relationship

## 🔧 Configuration

### Environment Variables (.env)
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Paths
JSON_FOLDER=json_cases
EMBEDDINGS_FOLDER=data/embeddings
GRAPHS_FOLDER=data/graphs

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# GraphRAG Parameters
MAX_CONTEXT=10000          # Maximum characters sent to AI
CHUNK_SIZE=8000           # Size of each text chunk
CHUNK_OVERLAP=800         # Overlap between chunks
MIN_CHUNK_SIZE=500        # Minimum chunk size
COMMUNITY_RESOLUTION=1.0  # Community detection resolution
MIN_COMMUNITY_SIZE=3      # Minimum community size
MAX_GRAPH_DEPTH=3         # Maximum graph traversal depth
```

### Search Types
- `similarity`: Semantic vector search
- `case_number`: Exact case number matching
- `judge`: Judge name search with fuzzy matching
- `case_type`: Case type filtering
- `graphrag`: Graph-enhanced search
- `combined`: Intelligent multi-strategy search (default)

## 📡 API Endpoints

### Chat and Search
- `POST /chat` - AI chat with GraphRAG enhancement
- `POST /search` - Advanced multi-criteria search
- `GET /search/case/{case_number}` - Search by case number
- `GET /search/judge/{judge_name}` - Search by judge name
- `GET /search/type/{case_type}` - Search by case type

### Information
- `GET /info/case-types` - Available case types
- `GET /info/judges` - System judges
- `GET /info/statistics` - System statistics
- `GET /graph/stats` - Knowledge graph statistics

### Documentation
- `GET /docs` - Interactive API documentation
- `GET /` - API information and endpoints

## 🏛️ Legal Domain Features

### Thai Legal Case Types
- **อาญา** (Criminal)
- **แพ่ง** (Civil)
- **แรงงาน** (Labor)
- **ภาษี** (Tax)
- **ปกครอง** (Administrative)
- **ครอบครัว** (Family)
- **ทรัพย์สินทางปัญญา** (Intellectual Property)

### Legal Concept Extraction
- Automatic detection of legal terms and concepts
- Thai legal article references
- Case number pattern recognition
- Judge name normalization
- Legal relationship identification

### Text Processing
- Thai Unicode normalization
- Legal keyword extraction
- Document chunking with overlap
- Similarity scoring for Thai text

## 🛠️ Development

### Project Structure
```
AI-Chatbot-GraphRAG/
├── src/
│   ├── api/                # API routes and handlers
│   ├── ai/                 # AI response generation
│   ├── config/             # System configuration
│   ├── graphrag/           # GraphRAG implementation
│   │   ├── knowledge_graph.py
│   │   └── graph_retriever.py
│   ├── models/             # Data models and schemas
│   ├── processing/         # Text processing utilities
│   ├── search/             # Search engines
│   └── utils/              # Utility functions
├── src/components/         # React components
├── data/
│   ├── embeddings/         # Vector embeddings
│   └── graphs/            # Knowledge graph data
├── json_cases/            # Legal case data
├── main.py                # FastAPI backend
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies
└── vite.config.js        # Vite configuration
```

### Adding New Features
1. **New Search Types**: Extend `SearchType` enum and implement search functions
2. **Graph Relationships**: Add new edge types in `LegalKnowledgeGraph`
3. **UI Components**: Create React components in `src/components/`
4. **API Endpoints**: Add new FastAPI routes in API modules

## 📈 Performance and Scalability

### Optimization Features
- **FAISS Indexing**: Fast similarity search for large datasets
- **Batch Processing**: Efficient embedding generation
- **Graph Caching**: Persistent knowledge graph storage
- **Community Detection**: Reduces search space through clustering

### Scaling Considerations
- **Distributed FAISS**: For large case collections
- **Graph Databases**: Neo4j integration for complex graphs
- **Caching Layer**: Redis for frequent queries
- **Load Balancing**: Multiple backend instances

## 🔒 Security and Privacy

### Data Protection
- Environment-based API key management
- No hardcoded secrets in code
- Secure API communication
- Input validation and sanitization

### Legal Compliance
- Focus on public legal documents
- No personal data storage
- Audit trails for legal research
- Ethical AI practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sentence Transformers** for multilingual embeddings
- **FAISS** for efficient similarity search
- **NetworkX** for graph processing
- **Google Gemini** for AI-powered analysis
- **React & Material-UI** for modern frontend
- **FastAPI** for high-performance backend

---

**Thai Legal GraphRAG Chatbot** - Advancing legal research with AI and knowledge graphs 🏛️⚡