"""
Traditional search methods (case number, judge, case type)
"""

import re
import logging
from typing import List, Dict, Set
from src.config import config
from src.processing import truncate_text, normalize_judge_name, find_best_match

logger = logging.getLogger(__name__)

class TraditionalSearchEngine:
    """Traditional search methods for exact matches"""
    
    def __init__(self, docs: List[str], metadatas: List[Dict]):
        self.docs = docs
        self.metadatas = metadatas
    
    def search_by_case_number(self, case_number: str, k: int = config.MAX_CONTEXT) -> List[Dict]:
        """ค้นหาด้วยหมายเลขคดี"""
        results = []
        seen_cases = set()
        
        clean_case_number = case_number.strip()
        
        for i, metadata in enumerate(self.metadatas):
            decision_id = metadata.get("decision_id", "")
            
            # Exact match only for case numbers
            matches = [
                clean_case_number == decision_id,
                clean_case_number.replace("/", "-") == decision_id,
                clean_case_number.replace("-", "/") == decision_id
            ]
            
            if any(matches):
                if decision_id in seen_cases:
                    continue
                seen_cases.add(decision_id)
                
                text = self.docs[i]
                truncated_text = truncate_text(text)
                
                result = {
                    "text": truncated_text,
                    "title": metadata["title"],
                    "source": metadata["source"],
                    "decision_id": decision_id,
                    "case_type": metadata.get("case_type", "ไม่ระบุ"),
                    "judges": metadata.get("judges", []),
                    "similarity": 1.0,
                    "keywords": metadata.get("keywords", []),
                    "litigants": metadata.get("litigants", {}),
                    "related_sections": metadata.get("related_sections", {}),
                    "full_summary": metadata.get("full_summary", "")
                }
                results.append(result)
                
                if len(results) >= k:
                    break
        
        return results
    
    def search_by_judge(self, judge_name: str, k: int = config.MAX_CONTEXT) -> List[Dict]:
        """ค้นหาด้วยชื่อผู้พิพากษา"""
        results = []
        seen_cases = set()
        
        query_normalized = normalize_judge_name(judge_name)
        
        # รวบรวมรายชื่อผู้พิพากษาทั้งหมด
        all_judges = []
        for metadata in self.metadatas:
            all_judges.extend(metadata.get("judges", []))
        
        matched_judges = find_best_match(judge_name, all_judges, threshold=0.5)
        
        for i, metadata in enumerate(self.metadatas):
            judges = metadata.get("judges", [])
            judges_normalized = metadata.get("judges_normalized", [])
            
            match_found = False
            
            # ตรวจสอบจากชื่อที่ตรงกัน
            for judge in judges:
                if judge in matched_judges:
                    match_found = True
                    break
            
            # ตรวจสอบจากชื่อที่ normalize แล้ว
            if not match_found:
                for judge_norm in judges_normalized:
                    if query_normalized in judge_norm or judge_norm in query_normalized:
                        match_found = True
                        break
            
            # ตรวจสอบในข้อความด้วย
            if not match_found:
                text_lower = self.docs[i].lower()
                if judge_name.lower() in text_lower or query_normalized in text_lower:
                    match_found = True
            
            if match_found:
                decision_id = metadata["decision_id"]
                if decision_id in seen_cases:
                    continue
                seen_cases.add(decision_id)
                
                text = self.docs[i]
                truncated_text = truncate_text(text)
                
                result = {
                    "text": truncated_text,
                    "title": metadata["title"],
                    "source": metadata["source"],
                    "decision_id": decision_id,
                    "case_type": metadata.get("case_type", "ไม่ระบุ"),
                    "judges": metadata.get("judges", []),
                    "similarity": 1.0,
                    "keywords": metadata.get("keywords", []),
                    "litigants": metadata.get("litigants", {}),
                    "related_sections": metadata.get("related_sections", {}),
                    "full_summary": metadata.get("full_summary", "")
                }
                results.append(result)
                
                if len(results) >= k:
                    break
        
        return results
    
    def search_by_case_type(self, case_type: str, k: int = config.MAX_CONTEXT) -> List[Dict]:
        """ค้นหาด้วยประเภทคดี"""
        results = []
        seen_cases = set()
        
        for i, metadata in enumerate(self.metadatas):
            if metadata.get("case_type", "") == case_type:
                decision_id = metadata["decision_id"]
                if decision_id in seen_cases:
                    continue
                seen_cases.add(decision_id)
                
                text = self.docs[i]
                truncated_text = truncate_text(text)
                
                result = {
                    "text": truncated_text,
                    "title": metadata["title"],
                    "source": metadata["source"],
                    "decision_id": decision_id,
                    "case_type": metadata.get("case_type", "ไม่ระบุ"),
                    "judges": metadata.get("judges", []),
                    "similarity": 1.0,
                    "keywords": metadata.get("keywords", []),
                    "litigants": metadata.get("litigants", {}),
                    "related_sections": metadata.get("related_sections", {}),
                    "full_summary": metadata.get("full_summary", "")
                }
                results.append(result)
                
                if len(results) >= k:
                    break
        
        return results