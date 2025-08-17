"""
Text processing utilities for Thai legal documents
"""

from .text_utils import (
    clean_text,
    normalize_unicode,
    extract_keywords,
    truncate_text,
    chunk_text_with_overlap,
    normalize_judge_name,
    similarity_score,
    find_best_match
)

from .legal_utils import (
    detect_case_type,
    extract_case_type
)

from .data_loader import load_documents_from_folder

__all__ = [
    'clean_text',
    'normalize_unicode', 
    'extract_keywords',
    'truncate_text',
    'chunk_text_with_overlap',
    'normalize_judge_name',
    'similarity_score',
    'find_best_match',
    'detect_case_type',
    'extract_case_type',
    'load_documents_from_folder'
]