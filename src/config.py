"""
Configuration module for Thai Legal GraphRAG system
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Application configuration settings"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    
    # File Paths
    JSON_FOLDER: str = os.getenv('JSON_FOLDER', 'json_cases')
    EMBEDDINGS_FOLDER: str = os.getenv('EMBEDDINGS_FOLDER', 'data/embeddings')
    GRAPHS_FOLDER: str = os.getenv('GRAPHS_FOLDER', 'data/graphs')
    
    # API Configuration
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
    API_PORT: int = int(os.getenv('API_PORT', 8000))
    
    # GraphRAG Configuration
    MAX_CONTEXT: int = int(os.getenv('MAX_CONTEXT', 1000))
    CHUNK_SIZE: int = int(os.getenv('CHUNK_SIZE', 300))
    CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP', 30))
    MIN_CHUNK_SIZE: int = int(os.getenv('MIN_CHUNK_SIZE', 80))
    MAX_DISPLAY_LENGTH: int = int(os.getenv('MAX_DISPLAY_LENGTH', 150))
    
    # Graph Parameters
    COMMUNITY_RESOLUTION: float = float(os.getenv('COMMUNITY_RESOLUTION', 1.0))
    MIN_COMMUNITY_SIZE: int = int(os.getenv('MIN_COMMUNITY_SIZE', 3))
    MAX_GRAPH_DEPTH: int = int(os.getenv('MAX_GRAPH_DEPTH', 3))
    
    # File paths (computed)
    @property
    def INDEX_FILE(self) -> str:
        return os.path.join(self.EMBEDDINGS_FOLDER, "index_ivf.faiss")
    
    @property
    def EMBEDDING_FILE(self) -> str:
        return os.path.join(self.EMBEDDINGS_FOLDER, "embeddings.npy")
    
    @property
    def METADATA_FILE(self) -> str:
        return os.path.join(self.EMBEDDINGS_FOLDER, "metadata.json")
    
    def validate(self) -> bool:
        """Validate required configuration"""
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        return True

# Global config instance
config = Config()
config.validate()