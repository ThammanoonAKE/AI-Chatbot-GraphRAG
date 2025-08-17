"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel
from typing import Optional
from .enums import SearchType

class MessageRequest(BaseModel):
    message: str
    search_type: SearchType = SearchType.COMBINED
    case_type: Optional[str] = None
    judge_name: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    search_type: SearchType = SearchType.COMBINED
    case_type: Optional[str] = None
    judge_name: Optional[str] = None
    k: int = 5