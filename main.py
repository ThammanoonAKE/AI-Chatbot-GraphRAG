"""
Thai Legal GraphRAG Chatbot - Main Application Entry Point

A sophisticated AI-powered chatbot that combines GraphRAG with traditional vector search
to provide intelligent legal case analysis and recommendations for Thai legal documents.
"""

import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import config
from src.api import router

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Thai Legal GraphRAG API", 
    version="2.0",
    description="Enhanced Legal Case Search with GraphRAG and React Frontend",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("🚀 Thai Legal GraphRAG API starting...")
    
    # Initialize embeddings and knowledge graph on startup
    logger.info("📊 Initializing embeddings and knowledge graph...")
    try:
        from src.search import SearchManager
        # Initialize SearchManager to build embeddings and graph
        search_manager = SearchManager()
        logger.info("✅ Embeddings and knowledge graph initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize embeddings: {e}")
        logger.warning("⚠️ Server will continue but search functionality may be limited")
    
    logger.info("📡 Available endpoints:")
    logger.info("   - POST /chat - Chat with AI assistant (GraphRAG-enhanced)")
    logger.info("   - POST /search - Advanced search with knowledge graph")
    logger.info("   - GET /search/case/{case_number} - Search by case number")
    logger.info("   - GET /search/judge/{judge_name} - Search by judge name")
    logger.info("   - GET /search/type/{case_type} - Search by case type")
    logger.info("   - GET /info/case-types - Get case types")
    logger.info("   - GET /info/judges - Get judges list")
    logger.info("   - GET /info/statistics - Get system statistics")
    logger.info("   - GET /graph/stats - Get knowledge graph statistics")
    logger.info(f"🌐 Server running at: http://{config.API_HOST}:{config.API_PORT}")
    logger.info(f"📚 API Documentation: http://{config.API_HOST}:{config.API_PORT}/docs")
    logger.info("🔗 React Frontend: http://localhost:3000 (after npm run dev)")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("👋 Thai Legal GraphRAG API shutting down...")

if __name__ == "__main__":
    # Run the application
    print("Thai Legal GraphRAG API starting...")
    print("Features:")
    print("   - GraphRAG-enhanced search")
    print("   - Knowledge graph relationships") 
    print("   - Community detection")
    print("   - React frontend")
    print("   - Environment-based configuration")
    print("   - Modular architecture")
    print()
    print(f"Server: http://{config.API_HOST}:{config.API_PORT}")
    print(f"API Docs: http://{config.API_HOST}:{config.API_PORT}/docs")
    print("Frontend: http://localhost:3000 (run 'npm run dev')")
    print()
    
    uvicorn.run(
        "main:app",  # Use string reference for hot reloading
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,  # Enable hot reloading in development
        log_level="info"
    )