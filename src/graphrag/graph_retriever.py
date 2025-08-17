import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
import logging
from .knowledge_graph import LegalKnowledgeGraph

logger = logging.getLogger(__name__)

class GraphRAGRetriever:
    """
    GraphRAG-based retriever that combines traditional vector search 
    with knowledge graph traversal for enhanced legal case retrieval
    """
    
    def __init__(self, knowledge_graph: LegalKnowledgeGraph):
        self.kg = knowledge_graph
        
    def retrieve_with_graph_context(self, 
                                   query: str,
                                   vector_results: List[Dict],
                                   max_graph_depth: int = 2,
                                   context_weight: float = 0.3) -> List[Dict]:
        """
        Enhance vector search results with graph-based context
        
        Args:
            query: User query
            vector_results: Initial vector search results
            max_graph_depth: Maximum depth for graph traversal
            context_weight: Weight for graph-based context (0-1)
        
        Returns:
            Enhanced results with graph context
        """
        if not vector_results:
            return []
        
        enhanced_results = []
        seen_cases = set()
        
        for result in vector_results:
            case_id = result.get('decision_id', '')
            if not case_id or case_id in seen_cases:
                continue
            
            seen_cases.add(case_id)
            
            # Get graph context for this case
            graph_context = self._get_case_graph_context(case_id, max_graph_depth)
            
            # Enhance result with graph context
            enhanced_result = result.copy()
            enhanced_result['graph_context'] = graph_context
            
            # Calculate graph-enhanced relevance score
            original_score = result.get('similarity', 0.5)
            graph_score = self._calculate_graph_relevance(case_id, query, graph_context)
            
            # Combine scores
            enhanced_score = (1 - context_weight) * original_score + context_weight * graph_score
            enhanced_result['enhanced_similarity'] = enhanced_score
            enhanced_result['graph_relevance'] = graph_score
            
            enhanced_results.append(enhanced_result)
        
        # Add additional related cases from graph
        additional_cases = self._find_additional_relevant_cases(
            query, [r['decision_id'] for r in enhanced_results], max_results=5
        )
        
        for case_data in additional_cases:
            if case_data['decision_id'] not in seen_cases:
                enhanced_results.append(case_data)
                seen_cases.add(case_data['decision_id'])
        
        # Sort by enhanced similarity
        enhanced_results.sort(key=lambda x: x.get('enhanced_similarity', x.get('similarity', 0)), reverse=True)
        
        return enhanced_results
    
    def _get_case_graph_context(self, case_id: str, max_depth: int = 2) -> Dict:
        """Get comprehensive graph context for a case"""
        context = {
            'related_entities': [],
            'community_members': [],
            'similar_cases': [],
            'related_judges': [],
            'related_concepts': []
        }
        
        if case_id not in self.kg.graph:
            return context
        
        # Get related entities through graph traversal
        related_entities = self.kg.get_related_entities(case_id, max_depth=max_depth, max_results=20)
        
        # Categorize related entities
        for entity, entity_type, score in related_entities:
            entity_info = {
                'entity': entity,
                'type': entity_type,
                'relevance_score': score
            }
            
            context['related_entities'].append(entity_info)
            
            # Categorize by type
            if entity_type == 'case':
                context['similar_cases'].append(entity_info)
            elif entity_type == 'judge':
                context['related_judges'].append(entity_info)
            elif entity_type == 'legal_concept':
                context['related_concepts'].append(entity_info)
        
        # Get community context
        community_members = self.kg.get_community_context(case_id)
        context['community_members'] = [
            {'entity': member, 'type': self.kg.graph.nodes.get(member, {}).get('type', 'unknown')}
            for member in community_members[:10]
        ]
        
        return context
    
    def _calculate_graph_relevance(self, case_id: str, query: str, graph_context: Dict) -> float:
        """Calculate relevance score based on graph context"""
        score = 0.0
        
        # Query terms for matching
        query_terms = set(query.lower().split())
        
        # Score based on related entities
        for entity_info in graph_context.get('related_entities', []):
            entity = entity_info['entity'].lower()
            entity_score = entity_info['relevance_score']
            
            # Check if entity matches query terms
            if any(term in entity for term in query_terms):
                score += entity_score * 0.5
        
        # Score based on community context
        community_score = len(graph_context.get('community_members', [])) * 0.1
        score += min(community_score, 0.3)  # Cap community bonus
        
        # Score based on number of similar cases (diversity bonus)
        similar_cases_bonus = min(len(graph_context.get('similar_cases', [])) * 0.05, 0.2)
        score += similar_cases_bonus
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _find_additional_relevant_cases(self, query: str, existing_case_ids: Set[str], max_results: int = 5) -> List[Dict]:
        """Find additional relevant cases using graph relationships"""
        additional_cases = []
        
        # Extract entities from query
        query_entities = self._extract_query_entities(query)
        
        # Find cases related to query entities
        for entity in query_entities:
            if entity in self.kg.graph:
                related_entities = self.kg.get_related_entities(entity, max_depth=2)
                
                for related_entity, entity_type, score in related_entities:
                    if (entity_type == 'case' and 
                        related_entity not in existing_case_ids and 
                        len(additional_cases) < max_results):
                        
                        # Create basic case info
                        case_info = {
                            'decision_id': related_entity,
                            'similarity': score * 0.7,  # Lower than vector results
                            'enhanced_similarity': score * 0.7,
                            'graph_relevance': score,
                            'source': 'graph_discovery',
                            'text': f"Case discovered through graph relationship with {entity}",
                            'title': f"Related case: {related_entity}",
                            'case_type': 'ไม่ระบุ',
                            'judges': [],
                            'keywords': [],
                            'litigants': {},
                            'related_sections': {}
                        }
                        
                        additional_cases.append(case_info)
        
        return additional_cases
    
    def _extract_query_entities(self, query: str) -> List[str]:
        """Extract potential entities from user query"""
        entities = []
        query_lower = query.lower()
        
        # Check for case numbers (pattern: xxxx/yyyy)
        import re
        case_number_pattern = r'\d{2,6}/\d{2,4}'
        case_numbers = re.findall(case_number_pattern, query)
        entities.extend(case_numbers)
        
        # Check for judge names (pattern: ผู้พิพากษา xxx)
        judge_pattern = r'ผู้พิพากษา\s*(\w+)'
        judge_matches = re.findall(judge_pattern, query)
        entities.extend(judge_matches)
        
        # Check for legal concepts
        legal_concepts = [
            'ลักทรัพย์', 'บุกรุก', 'เคหสถาน', 'พยายาม', 'ฆ่า', 'ทำร้าย', 'โจรกรรม',
            'ฉ้อโกง', 'ยักยอก', 'ข่มขืน', 'ลูกหนี้', 'เจ้าหนี้', 'สัญญา', 'ผิดสัญญา',
            'ค่าเสียหาย', 'ดอกเบี้ย', 'จำนอง', 'จำนำ', 'หย่า', 'อุปการะ', 'มรดก',
            'ที่ดิน', 'กรรมสิทธิ์', 'ข้าราชการ', 'ทุจริต', 'ประมูล', 'ภาษี', 'อากร'
        ]
        
        for concept in legal_concepts:
            if concept in query:
                entities.append(concept)
        
        # Check for case types
        case_types = ['อาญา', 'แพ่ง', 'แรงงาน', 'ภาษี', 'ปกครอง', 'ครอบครัว']
        for case_type in case_types:
            if case_type in query:
                entities.append(case_type)
        
        return entities
    
    def get_entity_recommendations(self, entity: str, entity_type: str = None) -> List[Dict]:
        """Get recommendations based on specific entity"""
        if entity not in self.kg.graph:
            return []
        
        related_entities = self.kg.get_related_entities(entity, max_depth=2, max_results=15)
        
        recommendations = []
        for related_entity, rel_type, score in related_entities:
            if rel_type == 'case':  # Focus on case recommendations
                rec = {
                    'entity': related_entity,
                    'type': rel_type,
                    'relevance_score': score,
                    'relationship_reason': f"Related to {entity} through {rel_type} relationship"
                }
                recommendations.append(rec)
        
        return recommendations
    
    def explain_retrieval(self, case_id: str, query: str) -> Dict:
        """Provide explanation for why a case was retrieved"""
        explanation = {
            'case_id': case_id,
            'query': query,
            'retrieval_reasons': [],
            'graph_connections': [],
            'community_info': None
        }
        
        if case_id not in self.kg.graph:
            explanation['retrieval_reasons'].append("Case not found in knowledge graph")
            return explanation
        
        # Get graph context
        graph_context = self._get_case_graph_context(case_id)
        
        # Analyze connections
        query_entities = self._extract_query_entities(query)
        
        for entity in query_entities:
            if entity in self.kg.graph:
                # Check if there's a path between query entity and case
                try:
                    if self.kg.graph.has_edge(entity, case_id):
                        explanation['graph_connections'].append({
                            'entity': entity,
                            'connection': 'direct',
                            'relationship': self.kg.graph.get_edge_data(entity, case_id).get('relation', 'related')
                        })
                    else:
                        # Check for shortest path
                        if nx.has_path(self.kg.graph, entity, case_id):
                            path = nx.shortest_path(self.kg.graph, entity, case_id)
                            if len(path) <= 3:  # Only short paths
                                explanation['graph_connections'].append({
                                    'entity': entity,
                                    'connection': 'indirect',
                                    'path_length': len(path) - 1,
                                    'path': path
                                })
                except:
                    pass
        
        # Community information
        for community_id, members in self.kg.communities.items():
            if case_id in members:
                explanation['community_info'] = {
                    'community_id': community_id,
                    'community_size': len(members),
                    'related_cases': [m for m in members if m != case_id and self.kg.graph.nodes.get(m, {}).get('type') == 'case'][:5]
                }
                break
        
        return explanation