"""
Text processing utilities for Thai legal documents
"""

import re
import unicodedata
from typing import List
from difflib import SequenceMatcher
from src.config import config

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0E00-\u0E7F\w\s.,!?()-]', '', text)
    return text.strip()

def normalize_unicode(text: str) -> str:
    """ปรับปรุงการจัดการ Unicode และตัวอักษรพิเศษ"""
    if not text:
        return ""
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def extract_keywords(text: str) -> List[str]:
    """Extract legal keywords from text"""
    keywords = []
    
    # กฎหมาย - มาตรา
    legal_terms = re.findall(r'(?:มาตรา|มา\.)\s*\d+(?:\(\d+\))?', text, re.IGNORECASE)
    keywords.extend(legal_terms)
    
    # หมายเลขคดี
    case_numbers = re.findall(r'\d+/\d+', text)
    keywords.extend(case_numbers)
    
    # คำสำคัญทางกฎหมาย
    legal_keywords = [
        'ลักทรัพย์', 'บุกรุก', 'เคหสถาน', 'พยายาม', 'ฆ่า', 'ทำร้าย', 'โจรกรรม',
        'ฉ้อโกง', 'ยักยอก', 'ข่มขืน', 'ลูกหนี้', 'เจ้าหนี้', 'สัญญา', 'ผิดสัญญา',
        'ค่าเสียหาย', 'ดอกเบี้ย', 'จำนอง', 'จำนำ', 'หย่า', 'อุปการะ', 'มรดก',
        'ที่ดิน', 'กรรมสิทธิ์', 'ข้าราชการ', 'ทุจริต', 'ประมูล', 'ภาษี', 'อากร'
    ]
    
    for keyword in legal_keywords:
        if keyword in text:
            keywords.append(keyword)
    
    return keywords

def truncate_text(text: str, max_length: int = None) -> str:
    """Truncate text to specified length"""
    if max_length is None:
        max_length = config.MAX_DISPLAY_LENGTH
        
    if len(text) <= max_length:
        return text
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    last_period = truncated.rfind('.')
    cut_point = max(last_space, last_period)
    if cut_point > max_length * 0.8:
        truncated = text[:cut_point]
    return truncated + "..."

def chunk_text_with_overlap(text: str, max_length: int = None, overlap: int = None) -> List[str]:
    """Split text into overlapping chunks"""
    if max_length is None:
        max_length = config.CHUNK_SIZE
    if overlap is None:
        overlap = config.CHUNK_OVERLAP
        
    if len(text) <= max_length:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_length, len(text))
        if end < len(text):
            space_pos = text.rfind(' ', start, end)
            if space_pos != -1 and space_pos > start + config.MIN_CHUNK_SIZE:
                end = space_pos
        chunk = text[start:end].strip()
        if len(chunk) >= config.MIN_CHUNK_SIZE:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def normalize_judge_name(name: str) -> str:
    """ปรับปรุงการจัดการชื่อผู้พิพากษา"""
    if not name:
        return ""
    
    name = normalize_unicode(name)
    name = re.sub(r'\s+', ' ', name.strip().lower())
    
    # ลบคำนำหน้า
    prefixes = [
        'นาย', 'นาง', 'นางสาว', 'ดร\.', 'ศาสตราจารย์', 'รองศาสตราจารย์',
        'ผู้พิพากษา', 'ผู้พิพากษาหัวหน้า', 'ผู้พิพากษาที่ปรึกษา',
        'ประธานศาลฎีกา', 'รองประธานศาลฎีกา', 'ผู้พิพากษาศาลฎีกา'
    ]
    
    for prefix in prefixes:
        pattern = rf'^{prefix}\s*'
        name = re.sub(pattern, '', name)
    
    name = re.sub(r'[\d\.\,\(\)\-\:]', '', name)
    name = re.sub(r'\s+', ' ', name.strip())
    
    return name

def similarity_score(str1: str, str2: str) -> float:
    """คำนวณคะแนนความคล้ายคลึงระหว่างสองสตริง"""
    return SequenceMatcher(None, str1, str2).ratio()

def find_best_match(query: str, candidates: List[str], threshold: float = 0.6) -> List[str]:
    """หาคำที่ตรงกันที่สุดจากรายการผู้สมัคร"""
    matches = []
    query_normalized = normalize_judge_name(query)
    
    for candidate in candidates:
        candidate_normalized = normalize_judge_name(candidate)
        
        if query_normalized in candidate_normalized or candidate_normalized in query_normalized:
            matches.append(candidate)
            continue
        
        score = similarity_score(query_normalized, candidate_normalized)
        if score >= threshold:
            matches.append(candidate)
    
    return matches