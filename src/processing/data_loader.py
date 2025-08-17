"""
Data loading utilities for legal case documents
"""

import os
import json
import logging
from typing import List, Dict, Tuple
from tqdm import tqdm

from .text_utils import clean_text, chunk_text_with_overlap, normalize_judge_name, extract_keywords
from .legal_utils import detect_case_type
from src.config import config

logger = logging.getLogger(__name__)

def load_documents_from_folder(folder_path: str) -> Tuple[List[str], List[Dict]]:
    """Load and process legal documents from JSON folder"""
    docs = []
    metadatas = []
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    
    for filename in tqdm(json_files, desc="Loading files", ncols=70):
        full_path = os.path.join(folder_path, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                entries = [data] if isinstance(data, dict) else data
                
                for entry in entries:
                    title = entry.get("title", "ไม่มีชื่อ")
                    decision_id = entry.get("decision_id", "ไม่ระบุ")
                    summary = entry.get("summary", "")
                    full_text = entry.get("full_text", "")
                    base_text = summary or full_text
                    
                    if not base_text:
                        continue
                    
                    litigants = entry.get("litigants", {})
                    judges = entry.get("judges", [])
                    
                    case_type = detect_case_type(base_text, title)
                    
                    litigant_info = ""
                    if litigants:
                        plaintiff = litigants.get("โจทก์", "")
                        defendant = litigants.get("จำเลย", "")
                        if plaintiff:
                            litigant_info += f" โจทก์: {plaintiff[:50]}..."
                        if defendant:
                            litigant_info += f" จำเลย: {defendant[:50]}..."
                    
                    full_context = clean_text(base_text + litigant_info)
                    chunks = chunk_text_with_overlap(full_context)
                    
                    for i, chunk in enumerate(chunks):
                        if len(chunk.strip()) < config.MIN_CHUNK_SIZE:
                            continue
                        
                        docs.append(chunk)
                        metadatas.append({
                            "source": filename,
                            "title": title,
                            "decision_id": decision_id,
                            "case_type": case_type,
                            "judges": judges,
                            "judges_normalized": [normalize_judge_name(j) for j in judges],
                            "judges_original": judges,
                            "chunk_id": i,
                            "total_chunks": len(chunks),
                            "keywords": extract_keywords(chunk),
                            "litigants": litigants,
                            "related_sections": entry.get("related_sections", {}),
                            "full_summary": base_text  # เพิ่มข้อมูลเต็มไว้
                        })
        except Exception as e:
            logger.warning(f"Error loading {filename}: {e}")
            continue
    
    return docs, metadatas