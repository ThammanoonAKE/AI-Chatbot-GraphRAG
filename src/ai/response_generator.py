"""
AI response generation using Google Gemini
"""

import re
import logging
from typing import List, Dict, Optional
import google.generativeai as genai

from src.config import config
from src.models.enums import SearchType

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generates AI responses using Gemini"""
    
    def __init__(self):
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini AI model"""
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("✅ Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            raise
    
    def is_legal_query(self, query: str) -> bool:
        """Check if query is legal-related"""
        legal_keywords = [
            "คดี", "หมายเลขคดี", "คำพิพากษา", "ผู้พิพากษา", "อาญา", "แพ่ง", "แรงงาน", "ภาษี", 
            "จำเลย", "โจทก์", "ฎีกา", "ฟ้อง", "คำสั่ง", "ศาล", "กฎหมาย", "มาตรา", "พระราชบัญญัติ",
            "ประมวลกฎหมาย", "ข้อบังคับ", "กฎกระทรวง", "คดีความ", "ประเด็นกฎหมาย", "คำฟ้อง",
            "คำร้อง", "อุทธรณ์", "ฟื้นฟูคดี", "ล้มละลาย", "หย่าร้าง", "มรดก", "ทรัพย์สิน",
            "สัญญา", "ละเมิด", "ความรับผิด", "ค่าเสียหาย", "ดอกเบี้ย", "ประกัน", "จำนำ",
            "จำนอง", "เช่า", "ขาย", "ซื้อ", "บริษัท", "ห้างหุ้นส่วน", "ลิขสิทธิ์", "สิทธิบัตร",
            "เครื่องหมายการค้า", "ครอบครัว", "บุตร", "สมรส", "อำนาจปกครอง", "ปกครอง",
            "ทหาร", "ตำรวจ", "รัฐ", "ข้าราชการ", "พนักงาน", "ลูกจ้าง", "นายจ้าง", "สหภาพแรงงาน"
        ]
        
        # Check for case numbers and judge mentions
        case_number_pattern = r"\d{1,6}/\d{2,4}"
        has_case_number = re.search(case_number_pattern, query)
        
        # Also check for simple number patterns that could be case numbers
        simple_number_pattern = r"^\d+/\d+$"
        has_simple_case_number = re.search(simple_number_pattern, query.strip())
        
        judge_pattern = r"ผู้พิพากษา\s*[\w\s]+"
        has_judge_mention = re.search(judge_pattern, query)
        
        has_legal_keywords = any(keyword in query for keyword in legal_keywords)
        
        return has_legal_keywords or has_case_number or has_judge_mention or has_simple_case_number
    
    def generate_non_legal_response(self) -> str:
        """Generate response for non-legal queries"""
        return """🚫 ระบบนี้ตอบเฉพาะคำถามเกี่ยวกับคดีเท่านั้น

สามารถสอบถามได้เกี่ยวกับ:
📋 หมายเลขคดี (เช่น 1234/2567)
👨‍⚖️ ชื่อผู้พิพากษา
📂 ประเภทคดี (อาญา, แพ่ง, แรงงาน, ภาษี)
🔍 ประเด็นกฎหมายที่เกี่ยวข้อง
📖 คำพิพากษาที่คล้ายคลึง

กรุณาระบุข้อมูลคดีที่ต้องการค้นหา"""
    
    def generate_no_results_response(self) -> str:
        """Generate response when no results found"""
        return """❌ ไม่พบข้อมูลคดีที่เกี่ยวข้อง

💡 ข้อเสนอแนะ:
• ลองใช้หมายเลขคดีที่ชัดเจน (เช่น 1234/2567)
• ระบุชื่อผู้พิพากษาที่ต้องการค้นหา
• ระบุประเภทคดี (อาญา, แพ่ง, แรงงาน, ภาษี)
• ใช้คำค้นหาที่เกี่ยวข้องกับกฎหมาย"""
    
    def generate_response(self, query: str, contexts: List[Dict], search_method: str) -> str:
        """Generate AI response from contexts"""
        if not contexts:
            return self.generate_no_results_response()
        
        # Build context for AI response
        context_data = []
        seen_cases = set()
        
        for ctx in contexts:
            decision_id = ctx.get('decision_id', '')
            
            # Skip duplicate cases, but collect all chunks first
            if decision_id in seen_cases:
                continue
            seen_cases.add(decision_id)
            
            judges_text = ", ".join(ctx['judges']) if ctx['judges'] else "ไม่ระบุ"
            
            # Use full summary if available, otherwise combine chunks
            full_case_text = ctx.get('full_summary', '')
            if not full_case_text:
                # Fallback: collect all chunks for this case to reconstruct full text
                full_text_parts = []
                for context_item in contexts:
                    if context_item.get('decision_id') == decision_id:
                        full_text_parts.append(context_item.get('text', ''))
                full_case_text = " ".join(full_text_parts)
            
            # Include GraphRAG context if available
            graph_info = ""
            if 'graph_context' in ctx:
                graph_ctx = ctx['graph_context']
                if graph_ctx.get('related_concepts'):
                    concepts = [c['entity'] for c in graph_ctx['related_concepts'][:3]]
                    graph_info = f" (แนวคิดที่เกี่ยวข้อง: {', '.join(concepts)})"
            
            # Include litigants info
            litigants_info = ""
            litigants = ctx.get('litigants', {})
            if litigants:
                plaintiff = litigants.get('โจทก์', '')
                defendant = litigants.get('จำเลย', '')
                if plaintiff:
                    litigants_info += f"\nโจทก์: {plaintiff}"
                if defendant:
                    litigants_info += f"\nจำเลย: {defendant}"
            
            context_info = f"คดี {ctx['decision_id']} (ประเภท: {ctx['case_type']}) ผู้พิพากษา: {judges_text}{graph_info}{litigants_info}"
            context_data.append(f"{context_info}\n{full_case_text}")
        
        combined_context = "\n---\n".join(context_data)
        
        # Enhanced prompt with GraphRAG context
        prompt = f"""
คุณเป็นผู้ช่วยทางกฎหมายไทยที่เชี่ยวชาญในการวิเคราะห์คำพิพากษา พร้อมระบบ GraphRAG ที่ช่วยวิเคราะห์ความเชื่อมโยงระหว่างคดี

ข้อมูลคดีที่เกี่ยวข้อง (ค้นหาด้วย {search_method}):
{combined_context}

คำถาม: {query}

**สำคัญ: ให้วิเคราะห์และสกัดข้อมูลทั้งหมดจากข้อความคำพิพากษาที่ให้มา โดยอ่านอย่างละเอียดและครบถ้วน แล้วนำเสนอในรูปแบบที่มีรายละเอียดและครบถ้วนเหมือนกับการสรุปคำพิพากษาฉบับเต็ม**

กรุณาตอบในรูปแบบต่อไปนี้:

🏛️ คำพิพากษาศาลฎีกาที่ [หมายเลขคดี] เกี่ยวข้องกับ [ประเด็นหลัก] ใน [สถานที่/เหตุการณ์] โดย [รายละเอียดสำคัญ]

## 📋 **ข้อมูลคดี**
- **หมายเลขคดี**: [ระบุหมายเลขคดี]
- **ประเภท**: [ประเภทคดี] 
- **โจทก์**: [ดึงจาก litigants.โจทก์ หรือ litigants.plaintiff]
- **จำเลย**: [ดึงจาก litigants.จำเลย หรือ litigants.defendant]
- **ผู้พิพากษา**: [รายชื่อผู้พิพากษา]

## 📖 **สรุปคำพิพากษาฉบับเต็ม**

### 🏠 **ข้อเท็จจริง**
[สรุปข้อเท็จจริงอย่างละเอียดจากข้อความที่ให้มา รวมถึงสถานที่เกิดเหตุ บุคคลที่เกี่ยวข้อง และเหตุการณ์ที่เกิดขึ้น]

### ⚖️ **ประเด็นกฎหมายสำคัญ**
[วิเคราะห์ประเด็นทางกฎหมายที่สำคัญจากเนื้อหาคำพิพากษา แบ่งเป็นหัวข้อย่อยตามประเด็น]

### 🏛️ **วิวัฒนาการการพิจารณา**
#### **ศาลชั้นต้น**
[การพิจารณาและคำพิพากษาของศาลชั้นต้น]

#### **ศาลอุทธรณ์**
[การพิจารณาและคำพิพากษาของศาลอุทธรณ์ ถ้ามี]

#### **ศาลฎีกา (คำพิพากษาสุดท้าย)**
[การวินิจฉัยและคำพิพากษาของศาลฎีกา]

### 📜 **มาตราที่เกี่ยวข้อง**
[รายการมาตราและกฎหมายที่เกี่ยวข้องจากข้อความ]

### ⚖️ **ผลการตัดสิน**
[ผลการตัดสินขั้นสุดท้าย รวมถึงโทษหรือคำสั่งของศาล]

### 🎯 **หลักการสำคัญ**
[สกัดหลักการทางกฎหมายที่สำคัญจากคำพิพากษา]

🔗 **ความเชื่อมโยง**: [วิเคราะห์ความเชื่อมโยงกับคดีอื่นๆ หรือแนวคิดทางกฎหมายที่เกี่ยวข้อง]

**หลักการสำคัญ:**
- อ่านและวิเคราะห์ข้อความคำพิพากษาทั้งหมดอย่างละเอียด
- สกัดข้อมูลทุกส่วนที่มีอยู่ในข้อความและนำเสนออย่างครบถ้วน
- จัดระเบียบข้อมูลให้เป็นหมวดหมู่ที่เข้าใจง่าย
- ถ้าข้อมูลมีครบถ้วนในข้อความ ให้นำเสนอทั้งหมด อย่าบอกว่า "ไม่มีข้อมูล"
- ใช้ข้อมูลจากคำพิพากษาที่ให้มาเป็นหลัก และวิเคราะห์อย่างละเอียด
"""
        
        try:
            response = self.model.generate_content(prompt)
            bot_reply = response.text.strip()
            
            # Add search statistics
            unique_cases = len(set(ctx['decision_id'] for ctx in contexts))
            case_types = list(set(ctx['case_type'] for ctx in contexts))
            unique_judges = len(set(judge for ctx in contexts for judge in ctx['judges']))
            
            stats = f"\n\n📊 ผลการค้นหา: {search_method}"
            stats += f"\n📁 อ้างอิงจาก {unique_cases} คดี"
            if case_types:
                stats += f" | ประเภท: {', '.join(case_types)}"
            if unique_judges > 0:
                stats += f" | ผู้พิพากษา: {unique_judges} คน"
            
            # Show important cases
            important_cases = [ctx['decision_id'] for ctx in contexts[:3]]
            if important_cases:
                stats += f"\n🔍 คดีที่สำคัญ: {', '.join(important_cases)}"
            
            # Add GraphRAG insights if available
            graphrag_cases = [ctx for ctx in contexts if ctx.get('source') == 'graph_discovery']
            if graphrag_cases:
                stats += f"\n🕸️ คดีที่ค้นพบผ่าน Graph: {len(graphrag_cases)} คดี"
            
            bot_reply += stats
            return bot_reply
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"⚠️ เกิดข้อผิดพลาดในการประมวลผล: {str(e)}\nกรุณาลองใหม่อีกครั้ง"