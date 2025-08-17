"""
GraphRAG-enhanced search combining vector search with knowledge graph
"""

import logging
from typing import List, Dict
from src.config import config
from src.graphrag.knowledge_graph import LegalKnowledgeGraph
from src.graphrag.graph_retriever import GraphRAGRetriever

logger = logging.getLogger(__name__)

class GraphRAGSearchEngine:
    """GraphRAG-enhanced search engine"""
    
    def __init__(self):
        self.knowledge_graph = None
        self.graph_retriever = None
        self._is_loaded = False
    
    def initialize(self):
        """Initialize GraphRAG components"""
        if self._is_loaded:
            return
            
        logger.info("Initializing GraphRAG search engine...")
        
        try:
            self.knowledge_graph = LegalKnowledgeGraph(
                config.EMBEDDINGS_FOLDER, 
                config.GRAPHS_FOLDER
            )
            self.graph_retriever = GraphRAGRetriever(self.knowledge_graph)
            self._is_loaded = True
            logger.info("✅ GraphRAG components initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize GraphRAG: {e}")
            raise
    
    def load_or_build_graph(self, cases_data: List[Dict] = None):
        """Load existing graph or build new one"""
        if not self._is_loaded:
            self.initialize()
        
        logger.info("📊 Loading knowledge graph...")
        if not self.knowledge_graph.load_graph():
            if not cases_data:
                raise ValueError("No cases data provided for graph building")
            
            logger.info("Building new knowledge graph...")
            self.knowledge_graph.build_graph(cases_data)
            self.knowledge_graph.detect_communities()
            self.knowledge_graph.save_graph()
        
        graph_stats = self.knowledge_graph.get_graph_stats()
        logger.info(f"✅ Knowledge graph loaded: {graph_stats}")
    
    def search_with_graphrag(self, query: str, vector_results: List[Dict], 
                           k: int = config.MAX_CONTEXT) -> List[Dict]:
        """Enhance vector search results with GraphRAG"""
        if not self._is_loaded:
            raise RuntimeError("GraphRAG engine not initialized")
        
        try:
            # Enhance with GraphRAG
            enhanced_results = self.graph_retriever.retrieve_with_graph_context(
                query=query,
                vector_results=vector_results,
                max_graph_depth=config.MAX_GRAPH_DEPTH,
                context_weight=0.3
            )
            
            return enhanced_results[:k]
            
        except Exception as e:
            logger.error(f"Error in GraphRAG search: {e}")
            return vector_results  # Fallback to original results
    
    def get_entity_recommendations(self, entity: str, entity_type: str = None) -> List[Dict]:
        """Get entity-based recommendations"""
        if not self._is_loaded:
            return []
        
        return self.graph_retriever.get_entity_recommendations(entity, entity_type)
    
    def explain_retrieval(self, case_id: str, query: str) -> Dict:
        """Explain why a case was retrieved"""
        if not self._is_loaded:
            return {}
        
        return self.graph_retriever.explain_retrieval(case_id, query)
    
    def get_graph_stats(self) -> Dict:
        """Get knowledge graph statistics"""
        if not self._is_loaded:
            return {}
        
        return self.knowledge_graph.get_graph_stats()