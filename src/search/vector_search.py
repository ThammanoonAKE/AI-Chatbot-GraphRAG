"""
Vector-based similarity search using FAISS
"""

import os
import json
import faiss
import numpy as np
import logging
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from src.config import config
from src.processing import load_documents_from_folder, truncate_text

logger = logging.getLogger(__name__)

class VectorSearchEngine:
    """FAISS-based vector similarity search engine"""
    
    def __init__(self):
        self.index = None
        self.doc_embeddings = None
        self.docs = None
        self.metadatas = None
        self.embedding_model = None
        self._is_loaded = False
        
    def initialize(self):
        """Initialize embedding model and load/create index"""
        if self._is_loaded:
            return
            
        logger.info("Initializing vector search engine...")
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise
        
        # Load or create index
        self._load_or_create_index()
        self._is_loaded = True
        logger.info("✅ Vector search engine ready")
    
    def _load_or_create_index(self):
        """Load existing index or create new one"""
        # Create directories if they don't exist
        os.makedirs(config.EMBEDDINGS_FOLDER, exist_ok=True)
        
        # Try to load existing index
        if (os.path.exists(config.INDEX_FILE) and 
            os.path.exists(config.EMBEDDING_FILE) and 
            os.path.exists(config.METADATA_FILE)):
            try:
                self.index = faiss.read_index(config.INDEX_FILE)
                self.doc_embeddings = np.load(config.EMBEDDING_FILE)
                with open(config.METADATA_FILE, "r", encoding="utf-8") as f:
                    self.metadatas = json.load(f)
                self.docs = [meta["text"] for meta in self.metadatas]
                logger.info(f"✅ Loaded {len(self.docs)} chunks from existing index")
                return
            except Exception as e:
                logger.warning(f"Error loading existing index: {e}")
        
        # Create new index
        logger.info("Creating new vector index...")
        self.docs, self.metadatas = load_documents_from_folder(config.JSON_FOLDER)
        
        if not self.docs:
            raise ValueError("No documents found to index")
        
        # Create embeddings
        self._create_embeddings()
        
        # Save index
        self._save_index()
    
    def _create_embeddings(self):
        """Create embeddings for all documents"""
        logger.info("🧠 Creating embeddings...")
        batch_size = 32
        doc_embeddings = []
        
        for i in tqdm(range(0, len(self.docs), batch_size), desc="Embeddings", ncols=70):
            batch = self.docs[i:i + batch_size]
            try:
                batch_embeddings = self.embedding_model.encode(
                    batch,
                    convert_to_numpy=True,
                    show_progress_bar=False
                )
                doc_embeddings.extend(batch_embeddings)
            except Exception as e:
                logger.error(f"Error encoding batch {i}: {e}")
                continue
        
        self.doc_embeddings = np.array(doc_embeddings)
        
        # Create FAISS index
        d = self.doc_embeddings.shape[1]
        nlist = min(100, len(self.docs) // 10)
        quantizer = faiss.IndexFlatL2(d)
        self.index = faiss.IndexIVFFlat(quantizer, d, nlist)
        self.index.train(self.doc_embeddings)
        self.index.add(self.doc_embeddings)
        self.index.nprobe = min(20, nlist)
    
    def _save_index(self):
        """Save index to disk"""
        try:
            faiss.write_index(self.index, config.INDEX_FILE)
            np.save(config.EMBEDDING_FILE, self.doc_embeddings)
            
            # Add text to metadata for saving
            for i in range(len(self.metadatas)):
                self.metadatas[i]["text"] = self.docs[i]
            
            with open(config.METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.metadatas, f, ensure_ascii=False, indent=2)
            
            logger.info("✅ Index saved successfully")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def search_similar(self, query: str, k: int = config.MAX_CONTEXT, 
                      similarity_threshold: float = 0.4) -> List[Dict]:
        """Search for similar cases using vector similarity"""
        if not self._is_loaded:
            self.initialize()
        
        try:
            query_vec = self.embedding_model.encode([query])
            search_k = min(k * 2, len(self.docs))
            distances, indices = self.index.search(np.array(query_vec), search_k)
            
            results = []
            seen_cases = set()
            
            for i, idx in enumerate(indices[0]):
                if idx == -1:
                    continue
                
                distance = distances[0][i]
                similarity = 1 / (1 + distance)
                
                if similarity < similarity_threshold:
                    continue
                
                metadata = self.metadatas[idx]
                decision_id = metadata["decision_id"]
                
                if decision_id in seen_cases:
                    continue
                seen_cases.add(decision_id)
                
                text = self.docs[idx]
                truncated_text = truncate_text(text)
                
                result = {
                    "text": truncated_text,
                    "title": metadata["title"],
                    "source": metadata["source"],
                    "decision_id": decision_id,
                    "case_type": metadata.get("case_type", "ไม่ระบุ"),
                    "judges": metadata.get("judges", []),
                    "similarity": similarity,
                    "keywords": metadata.get("keywords", []),
                    "litigants": metadata.get("litigants", {}),
                    "related_sections": metadata.get("related_sections", {}),
                    "full_summary": metadata.get("full_summary", "")
                }
                results.append(result)
                
                if len(results) >= k:
                    break
            
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results
        
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def get_documents(self) -> tuple:
        """Get all documents and metadata"""
        if not self._is_loaded:
            self.initialize()
        return self.docs, self.metadatas