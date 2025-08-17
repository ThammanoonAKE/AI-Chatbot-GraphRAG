import os
import json
import pickle
import networkx as nx
import numpy as np
from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import community as community_louvain
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class LegalKnowledgeGraph:
    """
    Knowledge Graph for Thai Legal Cases using GraphRAG approach
    Creates relationships between cases, judges, legal concepts, and entities
    """
    
    def __init__(self, embeddings_folder: str, graphs_folder: str):
        self.embeddings_folder = embeddings_folder
        self.graphs_folder = graphs_folder
        self.graph = nx.Graph()
        self.entity_embeddings = {}
        self.communities = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
        self.case_documents = {}
        self.entity_types = {
            'case': set(),
            'judge': set(),
            'legal_concept': set(),
            'case_type': set(),
            'law_section': set()
        }
        
        # Ensure directories exist
        os.makedirs(embeddings_folder, exist_ok=True)
        os.makedirs(graphs_folder, exist_ok=True)
    
    def extract_entities(self, case_data: Dict) -> Dict[str, Set[str]]:
        """Extract entities from legal case data"""
        entities = defaultdict(set)
        
        # Case entity
        case_id = case_data.get('decision_id', '')
        if case_id:
            entities['case'].add(case_id)
        
        # Judge entities
        judges = case_data.get('judges', [])
        for judge in judges:
            if judge and judge.strip():
                entities['judge'].add(judge.strip())
        
        # Case type entity
        case_type = case_data.get('case_type', '')
        if case_type and case_type != 'ไม่ระบุ':
            entities['case_type'].add(case_type)
        
        # Legal sections
        related_sections = case_data.get('related_sections', {})
        for law_type, sections in related_sections.items():
            for section in sections:
                if section:
                    entities['law_section'].add(f"{law_type} {section}")
        
        # Extract legal concepts from text
        text = case_data.get('summary', '') or case_data.get('full_text', '')
        if text:
            legal_concepts = self._extract_legal_concepts(text)
            entities['legal_concept'].update(legal_concepts)
        
        return entities
    
    def _extract_legal_concepts(self, text: str) -> Set[str]:
        """Extract legal concepts from case text using pattern matching"""
        legal_concepts = set()
        
        # Common Thai legal terms
        legal_terms = [
            'ลักทรัพย์', 'บุกรุก', 'เคหสถาน', 'พยายาม', 'ฆ่า', 'ทำร้าย', 'โจรกรรม',
            'ฉ้อโกง', 'ยักยอก', 'ข่มขืน', 'ลูกหนี้', 'เจ้าหนี้', 'สัญญา', 'ผิดสัญญา',
            'ค่าเสียหาย', 'ดอกเบี้ย', 'จำนอง', 'จำนำ', 'หย่า', 'อุปการะ', 'มรดก',
            'ที่ดิน', 'กรรมสิทธิ์', 'ข้าราชการ', 'ทุจริต', 'ประมูล', 'ภาษี', 'อากร',
            'ครอบครัว', 'บุตร', 'สมรส', 'แรงงาน', 'ลูกจ้าง', 'นายจ้าง'
        ]
        
        text_lower = text.lower()
        for term in legal_terms:
            if term in text_lower:
                legal_concepts.add(term)
        
        return legal_concepts
    
    def build_graph(self, cases_data: List[Dict]) -> None:
        """Build knowledge graph from legal cases data"""
        logger.info("Building knowledge graph...")
        
        # Store case documents for TF-IDF
        self.case_documents = {}
        
        # Extract all entities
        all_entities = defaultdict(set)
        case_entities = {}
        
        for case_data in tqdm(cases_data, desc="Extracting entities"):
            case_id = case_data.get('decision_id', '')
            if not case_id:
                continue
                
            entities = self.extract_entities(case_data)
            case_entities[case_id] = entities
            
            # Store document text for TF-IDF
            text = case_data.get('summary', '') or case_data.get('full_text', '')
            self.case_documents[case_id] = text
            
            # Collect all entities by type
            for entity_type, entity_set in entities.items():
                all_entities[entity_type].update(entity_set)
                self.entity_types[entity_type].update(entity_set)
        
        # Add nodes to graph
        for entity_type, entity_set in all_entities.items():
            for entity in entity_set:
                self.graph.add_node(entity, type=entity_type)
        
        # Add edges based on relationships
        self._add_case_relationships(case_entities)
        self._add_similarity_relationships(cases_data)
        
        logger.info(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
    
    def _add_case_relationships(self, case_entities: Dict[str, Dict]) -> None:
        """Add direct relationships between entities within cases"""
        for case_id, entities in case_entities.items():
            # Connect case to all its entities
            for entity_type, entity_set in entities.items():
                for entity in entity_set:
                    if entity != case_id:
                        self.graph.add_edge(case_id, entity, relation='contains')
            
            # Connect entities within same case
            all_case_entities = []
            for entity_set in entities.values():
                all_case_entities.extend(entity_set)
            
            # Connect judges to case type (judges who handle specific case types)
            if 'judge' in entities and 'case_type' in entities:
                for judge in entities['judge']:
                    for case_type in entities['case_type']:
                        self.graph.add_edge(judge, case_type, relation='handles')
            
            # Connect judges to legal concepts
            if 'judge' in entities and 'legal_concept' in entities:
                for judge in entities['judge']:
                    for concept in entities['legal_concept']:
                        weight = self.graph.get_edge_data(judge, concept, {}).get('weight', 0) + 1
                        self.graph.add_edge(judge, concept, relation='deals_with', weight=weight)
    
    def _add_similarity_relationships(self, cases_data: List[Dict]) -> None:
        """Add similarity relationships between cases using TF-IDF"""
        logger.info("Computing case similarities...")
        
        # Prepare documents for TF-IDF
        case_ids = []
        documents = []
        
        for case_data in cases_data:
            case_id = case_data.get('decision_id', '')
            if case_id and case_id in self.case_documents:
                case_ids.append(case_id)
                documents.append(self.case_documents[case_id])
        
        if len(documents) < 2:
            return
        
        # Compute TF-IDF matrix
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Add similarity edges (only for high similarity)
            threshold = 0.3
            for i, case_id_1 in enumerate(case_ids):
                for j, case_id_2 in enumerate(case_ids):
                    if i < j and similarity_matrix[i][j] > threshold:
                        self.graph.add_edge(
                            case_id_1, case_id_2, 
                            relation='similar_to',
                            weight=similarity_matrix[i][j]
                        )
        except Exception as e:
            logger.warning(f"Failed to compute similarities: {e}")
    
    def detect_communities(self) -> None:
        """Detect communities in the knowledge graph"""
        logger.info("Detecting communities...")
        
        try:
            # Use Louvain algorithm for community detection
            partition = community_louvain.best_partition(self.graph)
            
            # Group entities by community
            communities = defaultdict(list)
            for node, community_id in partition.items():
                communities[community_id].append(node)
            
            # Filter out small communities
            min_size = 3
            self.communities = {
                cid: nodes for cid, nodes in communities.items() 
                if len(nodes) >= min_size
            }
            
            logger.info(f"Detected {len(self.communities)} communities")
            
        except Exception as e:
            logger.warning(f"Community detection failed: {e}")
    
    def get_related_entities(self, entity: str, max_depth: int = 2, max_results: int = 10) -> List[Tuple[str, str, float]]:
        """Get entities related to the given entity using graph traversal"""
        if entity not in self.graph:
            return []
        
        related = []
        visited = set([entity])
        
        # BFS traversal
        queue = [(entity, 0, 1.0)]  # (node, depth, score)
        
        while queue and len(related) < max_results:
            current, depth, score = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    
                    # Calculate relationship score
                    edge_data = self.graph.get_edge_data(current, neighbor, {})
                    edge_weight = edge_data.get('weight', 1.0)
                    relation_type = edge_data.get('relation', 'related')
                    
                    # Adjust score based on depth and edge weight
                    neighbor_score = score * (edge_weight / (depth + 1))
                    
                    if neighbor != entity:
                        node_type = self.graph.nodes[neighbor].get('type', 'unknown')
                        related.append((neighbor, node_type, neighbor_score))
                    
                    # Continue traversal
                    queue.append((neighbor, depth + 1, neighbor_score))
        
        # Sort by score and return top results
        related.sort(key=lambda x: x[2], reverse=True)
        return related[:max_results]
    
    def get_community_context(self, entity: str) -> List[str]:
        """Get community context for entity-based reasoning"""
        if entity not in self.graph:
            return []
        
        # Find entity's community
        for community_id, nodes in self.communities.items():
            if entity in nodes:
                # Return other entities in the same community
                context_entities = [node for node in nodes if node != entity]
                return context_entities[:20]  # Limit context size
        
        return []
    
    def save_graph(self, filename: str = 'legal_knowledge_graph.pkl') -> None:
        """Save the knowledge graph to disk"""
        filepath = os.path.join(self.graphs_folder, filename)
        
        graph_data = {
            'graph': self.graph,
            'communities': self.communities,
            'entity_types': self.entity_types,
            'case_documents': self.case_documents
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(graph_data, f)
        
        logger.info(f"Knowledge graph saved to {filepath}")
    
    def load_graph(self, filename: str = 'legal_knowledge_graph.pkl') -> bool:
        """Load the knowledge graph from disk"""
        filepath = os.path.join(self.graphs_folder, filename)
        
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'rb') as f:
                graph_data = pickle.load(f)
            
            self.graph = graph_data.get('graph', nx.Graph())
            self.communities = graph_data.get('communities', {})
            self.entity_types = graph_data.get('entity_types', defaultdict(set))
            self.case_documents = graph_data.get('case_documents', {})
            
            logger.info(f"Knowledge graph loaded from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load knowledge graph: {e}")
            return False
    
    def get_graph_stats(self) -> Dict:
        """Get statistics about the knowledge graph"""
        stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'communities': len(self.communities),
            'entity_types': {
                entity_type: len(entities) 
                for entity_type, entities in self.entity_types.items()
            }
        }
        
        if self.graph.number_of_nodes() > 0:
            stats['average_degree'] = sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
            stats['density'] = nx.density(self.graph)
        
        return stats