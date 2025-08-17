"""
Main search manager that coordinates different search engines
"""

import re
import logging
from typing import List, Dict, Optional
from collections import deque

from src.config import config
from src.models.enums import SearchType
from src.processing.legal_utils import extract_case_type
from .vector_search import VectorSearchEngine
from .traditional_search import TraditionalSearchEngine
from .graphrag_search import GraphRAGSearchEngine

logger = logging.getLogger(__name__)

class SearchManager:
    """Coordinates different search strategies"""
    
    def __init__(self):
        self.vector_engine = VectorSearchEngine()
        self.traditional_engine = None
        self.graphrag_engine = GraphRAGSearchEngine()
        self._is_initialized = False
        self.chat_memory = deque(maxlen=3)
    
    def initialize(self):
        """Initialize all search engines"""
        if self._is_initialized:
            return
        
        logger.info("Initializing search manager...")
        
        # Initialize vector search first
        self.vector_engine.initialize()
        
        # Get documents for traditional search
        docs, metadatas = self.vector_engine.get_documents()
        self.traditional_engine = TraditionalSearchEngine(docs, metadatas)
        
        # Initialize GraphRAG
        self.graphrag_engine.initialize()
        
        # Build knowledge graph from metadata
        cases_data = self._convert_metadata_to_cases(metadatas)
        self.graphrag_engine.load_or_build_graph(cases_data)
        
        self._is_initialized = True
        logger.info("✅ Search manager ready")
    
    def _convert_metadata_to_cases(self, metadatas: List[Dict]) -> List[Dict]:
        """Convert metadata to cases data for graph building"""
        cases_data = []
        seen_cases = set()
        
        for meta in metadatas:
            decision_id = meta.get('decision_id', '')
            if decision_id and decision_id not in seen_cases:
                seen_cases.add(decision_id)
                case_data = {
                    'decision_id': decision_id,
                    'title': meta.get('title', ''),
                    'summary': meta.get('full_summary', ''),
                    'judges': meta.get('judges', []),
                    'case_type': meta.get('case_type', ''),
                    'litigants': meta.get('litigants', {}),
                    'related_sections': meta.get('related_sections', {})
                }
                cases_data.append(case_data)
        
        return cases_data
    
    def search(self, query: str, search_type: SearchType = SearchType.COMBINED,
               case_type: Optional[str] = None, judge_name: Optional[str] = None,
               k: int = config.MAX_CONTEXT) -> List[Dict]:
        """Main search interface"""
        if not self._is_initialized:
            self.initialize()
        
        if search_type == SearchType.CASE_NUMBER:
            return self.traditional_engine.search_by_case_number(query, k)
        elif search_type == SearchType.JUDGE:
            return self.traditional_engine.search_by_judge(query, k)
        elif search_type == SearchType.CASE_TYPE:
            return self.traditional_engine.search_by_case_type(query, k)
        elif search_type == SearchType.SIMILARITY:
            return self.vector_engine.search_similar(query, k)
        elif search_type == SearchType.GRAPHRAG:
            return self._search_with_graphrag(query, k)
        else:  # COMBINED
            return self._combined_search(query, case_type, judge_name, k)
    
    def _search_with_graphrag(self, query: str, k: int) -> List[Dict]:
        """GraphRAG-enhanced search"""
        # First get vector results
        vector_results = self.vector_engine.search_similar(query, k)
        
        # Enhance with GraphRAG
        enhanced_results = self.graphrag_engine.search_with_graphrag(
            query, vector_results, k
        )
        
        return enhanced_results
    
    def _combined_search(self, query: str, case_type: Optional[str] = None,
                        judge_name: Optional[str] = None, k: int = config.MAX_CONTEXT) -> List[Dict]:
        """Intelligent combined search strategy"""
        
        # Check for case number first
        if re.search(r'\d+/\d+', query):
            results = self.traditional_engine.search_by_case_number(query, k)
            if results:
                return results
        
        # Try judge search
        if judge_name:
            results = self.traditional_engine.search_by_judge(judge_name, k)
            if results:
                return results
        
        # Check for judge in query
        judge_match = re.search(r'ผู้พิพากษา\s*(\w+)', query)
        if judge_match:
            judge = judge_match.group(1)
            results = self.traditional_engine.search_by_judge(judge, k)
            if results:
                return results
        
        # Case type search
        if case_type:
            case_results = self.traditional_engine.search_by_case_type(case_type, k)
            if case_results:
                # Combine with GraphRAG for better results
                graphrag_results = self._search_with_graphrag(query, k)
                
                combined_results = []
                seen_cases = set()
                
                for result in case_results:
                    if result["decision_id"] not in seen_cases:
                        combined_results.append(result)
                        seen_cases.add(result["decision_id"])
                
                for result in graphrag_results:
                    if result["decision_id"] not in seen_cases:
                        combined_results.append(result)
                        seen_cases.add(result["decision_id"])
                
                return combined_results[:k]
        
        # Check for case type in query
        extracted_case_type = extract_case_type(query)
        if extracted_case_type:
            results = self.traditional_engine.search_by_case_type(extracted_case_type, k)
            if results:
                return results
        
        # Default to GraphRAG search
        return self._search_with_graphrag(query, k)
    
    def get_graph_stats(self) -> Dict:
        """Get knowledge graph statistics"""
        if not self._is_initialized:
            self.initialize()
        return self.graphrag_engine.get_graph_stats()
    
    def get_entity_recommendations(self, entity: str, entity_type: str = None) -> List[Dict]:
        """Get entity-based recommendations"""
        if not self._is_initialized:
            self.initialize()
        return self.graphrag_engine.get_entity_recommendations(entity, entity_type)
    
    def explain_retrieval(self, case_id: str, query: str) -> Dict:
        """Explain retrieval reasoning"""
        if not self._is_initialized:
            self.initialize()
        return self.graphrag_engine.explain_retrieval(case_id, query)