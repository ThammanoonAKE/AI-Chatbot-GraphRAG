"""
FastAPI routes for the legal search system
"""

import logging
from collections import deque
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from src.models import MessageRequest, SearchRequest, SearchType, CaseType
from src.search import SearchManager
from src.ai import ResponseGenerator

logger = logging.getLogger(__name__)

# Initialize components
search_manager = SearchManager()
response_generator = ResponseGenerator()
chat_memory = deque(maxlen=3)

# Create router
router = APIRouter()

@router.post("/chat")
async def chat_api(request: MessageRequest):
    """Chat API with GraphRAG capabilities"""
    user_input = request.message.strip()
    if not user_input:
        return {"reply": "กรุณาส่งข้อความที่ต้องการถาม"}
    
    try:
        chat_memory.append((user_input, None))
        
        # Check if query is legal-related
        if not response_generator.is_legal_query(user_input):
            return {"reply": response_generator.generate_non_legal_response()}
        
        # Perform search
        contexts = search_manager.search(
            query=user_input,
            search_type=request.search_type,
            case_type=request.case_type,
            judge_name=request.judge_name
        )
        
        # Determine search method for response
        search_method = _get_search_method_description(user_input, request.search_type)
        
        # Generate AI response
        reply = response_generator.generate_response(user_input, contexts, search_method)
        
        chat_memory[-1] = (user_input, reply)
        return {"reply": reply}
        
    except Exception as e:
        logger.error(f"Error in /chat: {e}")
        return {"reply": "เกิดข้อผิดพลาดในการประมวลผล"}

@router.post("/search")
async def search_api(request: SearchRequest):
    """Advanced search API with GraphRAG"""
    try:
        results = search_manager.search(
            query=request.query,
            search_type=request.search_type,
            case_type=request.case_type,
            judge_name=request.judge_name,
            k=request.k
        )
        
        return {
            "results": results,
            "total_found": len(results),
            "search_type": request.search_type,
            "query": request.query
        }
    except Exception as e:
        logger.error(f"Error in /search: {e}")
        return {"error": f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}"}

@router.get("/search/case/{case_number}")
async def search_case_number(case_number: str, k: int = Query(5, ge=1, le=20)):
    """ค้นหาด้วยหมายเลขคดี"""
    try:
        results = search_manager.search(
            query=case_number,
            search_type=SearchType.CASE_NUMBER,
            k=k
        )
        return {
            "results": results,
            "total_found": len(results),
            "case_number": case_number
        }
    except Exception as e:
        logger.error(f"Error in case search: {e}")
        return {"error": f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}"}

@router.get("/search/judge/{judge_name}")
async def search_judge(judge_name: str, k: int = Query(5, ge=1, le=20)):
    """ค้นหาด้วยชื่อผู้พิพากษา"""
    try:
        results = search_manager.search(
            query=judge_name,
            search_type=SearchType.JUDGE,
            k=k
        )
        return {
            "results": results,
            "total_found": len(results),
            "judge_name": judge_name
        }
    except Exception as e:
        logger.error(f"Error in judge search: {e}")
        return {"error": f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}"}

@router.get("/search/type/{case_type}")
async def search_case_type_api(case_type: str, k: int = Query(5, ge=1, le=20)):
    """ค้นหาด้วยประเภทคดี"""
    try:
        results = search_manager.search(
            query=case_type,
            search_type=SearchType.CASE_TYPE,
            k=k
        )
        return {
            "results": results,
            "total_found": len(results),
            "case_type": case_type
        }
    except Exception as e:
        logger.error(f"Error in case type search: {e}")
        return {"error": f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}"}

@router.get("/info/case-types")
async def get_case_types():
    """ดูประเภทคดีทั้งหมดที่มีในระบบ"""
    try:
        search_manager.initialize()
        docs, metadatas = search_manager.vector_engine.get_documents()
        
        case_types = {}
        for metadata in metadatas:
            case_type = metadata.get("case_type", "ไม่ระบุ")
            if case_type in case_types:
                case_types[case_type] += 1
            else:
                case_types[case_type] = 1
        
        return {
            "case_types": case_types,
            "total_types": len(case_types)
        }
    except Exception as e:
        logger.error(f"Error getting case types: {e}")
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@router.get("/info/judges")
async def get_judges():
    """ดูรายชื่อผู้พิพากษาทั้งหมดที่มีในระบบ"""
    try:
        search_manager.initialize()
        docs, metadatas = search_manager.vector_engine.get_documents()
        
        judges_count = {}
        all_judges = set()
        
        for metadata in metadatas:
            judges = metadata.get("judges", [])
            for judge in judges:
                if judge:
                    all_judges.add(judge)
                    if judge in judges_count:
                        judges_count[judge] += 1
                    else:
                        judges_count[judge] = 1
        
        sorted_judges = dict(sorted(judges_count.items(), key=lambda x: x[1], reverse=True))
        
        return {
            "judges": sorted_judges,
            "total_judges": len(all_judges),
            "top_10_judges": dict(list(sorted_judges.items())[:10])
        }
    except Exception as e:
        logger.error(f"Error getting judges: {e}")
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@router.get("/info/statistics")
async def get_statistics():
    """ดูสถิติทั่วไปของระบบ"""
    try:
        search_manager.initialize()
        docs, metadatas = search_manager.vector_engine.get_documents()
        
        unique_cases = set()
        case_types = {}
        judges_count = {}
        
        for metadata in metadatas:
            decision_id = metadata.get("decision_id", "")
            if decision_id:
                unique_cases.add(decision_id)
            
            case_type = metadata.get("case_type", "ไม่ระบุ")
            case_types[case_type] = case_types.get(case_type, 0) + 1
            
            judges = metadata.get("judges", [])
            for judge in judges:
                if judge:
                    judges_count[judge] = judges_count.get(judge, 0) + 1
        
        # Get graph statistics
        graph_stats = search_manager.get_graph_stats()
        
        return {
            "total_cases": len(unique_cases),
            "total_chunks": len(docs),
            "total_judges": len(judges_count),
            "case_types_distribution": case_types,
            "top_5_judges": dict(list(sorted(judges_count.items(), key=lambda x: x[1], reverse=True))[:5]),
            "graph_statistics": graph_stats
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@router.get("/graph/stats")
async def get_graph_stats():
    """Get knowledge graph statistics"""
    try:
        stats = search_manager.get_graph_stats()
        return {"graph_stats": stats}
    except Exception as e:
        logger.error(f"Error getting graph stats: {e}")
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@router.get("/case/full/{case_number}")
async def get_full_case_details(case_number: str):
    """ดูข้อมูลคดีแบบเต็มจากหมายเลขคดี"""
    try:
        # Initialize search manager
        search_manager.initialize()
        
        # Get all documents and metadatas
        docs, metadatas = search_manager.vector_engine.get_documents()
        
        # Find the case
        for i, metadata in enumerate(metadatas):
            if metadata.get("decision_id") == case_number:
                # Get the full case data
                case_data = {
                    "decision_id": metadata.get("decision_id", ""),
                    "title": metadata.get("title", ""),
                    "summary": metadata.get("summary", ""),
                    "related_sections": metadata.get("related_sections", {}),
                    "source": metadata.get("source", ""),
                    "litigants": metadata.get("litigants", {}),
                    "judges": metadata.get("judges", []),
                    "lower_and_appeal_courts": metadata.get("lower_and_appeal_courts", []),
                    "case_type": metadata.get("case_type", ""),
                    "year": metadata.get("year", ""),
                    "chunk_content": docs[i] if i < len(docs) else ""
                }
                
                return {
                    "case": case_data,
                    "found": True
                }
        
        return {
            "case": None,
            "found": False,
            "message": f"ไม่พบคดีหมายเลข {case_number}"
        }
        
    except Exception as e:
        logger.error(f"Error getting full case details: {e}")
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@router.get("/")
async def root():
    """API Information"""
    return {
        "message": "Thai Legal GraphRAG API",
        "version": "2.0",
        "features": [
            "GraphRAG-enhanced search",
            "Knowledge graph relationships",
            "Community detection",
            "React frontend",
            "Environment-based configuration"
        ],
        "endpoints": {
            "chat": "POST /chat - Chat with AI legal assistant",
            "search": "POST /search - Advanced search with GraphRAG",
            "search_case": "GET /search/case/{case_number} - Search by case number",
            "search_judge": "GET /search/judge/{judge_name} - Search by judge name",
            "search_type": "GET /search/type/{case_type} - Search by case type",
            "case_full": "GET /case/full/{case_number} - Get complete case details",
            "case_types": "GET /info/case-types - Get all case types",
            "judges": "GET /info/judges - Get all judges",
            "statistics": "GET /info/statistics - Get system statistics",
            "graph_stats": "GET /graph/stats - Get knowledge graph statistics"
        },
        "search_types": [e.value for e in SearchType],
        "case_types": [e.value for e in CaseType]
    }

def _get_search_method_description(query: str, search_type: SearchType) -> str:
    """Get description of search method used"""
    import re
    
    if search_type == SearchType.CASE_NUMBER:
        case_match = re.search(r'\d+/\d+', query)
        return f"หมายเลขคดี {case_match.group() if case_match else query}"
    elif search_type == SearchType.JUDGE:
        return f"ผู้พิพากษา {query}"
    elif search_type == SearchType.CASE_TYPE:
        return f"ประเภทคดี {query}"
    elif search_type == SearchType.SIMILARITY:
        return "ความคล้ายคลึง"
    elif search_type == SearchType.GRAPHRAG:
        return "GraphRAG (ปัญญาประดิษฐ์)"
    else:  # COMBINED
        # Auto-detect method
        if re.search(r'\d+/\d+', query):
            case_number = re.search(r'\d+/\d+', query).group()
            return f"หมายเลขคดี {case_number}"
        elif re.search(r'ผู้พิพากษา\s*(\w+)', query):
            judge_match = re.search(r'ผู้พิพากษา\s*(\w+)', query)
            return f"ผู้พิพากษา {judge_match.group(1) if judge_match else ''}"
        else:
            return "GraphRAG (ปัญญาประดิษฐ์)"