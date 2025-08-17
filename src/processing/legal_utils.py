"""
Legal-specific text processing utilities
"""

import re
from typing import Optional
from src.models.enums import CaseType

def detect_case_type(text: str, title: str = "") -> str:
    """ตรวจสอบประเภทคดีจากเนื้อหา"""
    combined_text = f"{title} {text}".lower()
    
    # คดีอาญา
    criminal_patterns = [
        r'ลักทรัพย์|โจรกรรม|ฆ่า|ทำร้าย|ข่มขืน|ฉ้อโกง|ยักยอก|บุกรุก|พยายาม',
        r'ประมวลกฎหมายอาญา|มาตรา\s*\d+.*อาญา|ความผิดฐาน',
        r'จำเลย|โจทก์.*อัยการ|พนักงานอัยการ'
    ]
    
    # คดีแพ่ง
    civil_patterns = [
        r'ผิดสัญญา|ค่าเสียหาย|ดอกเบี้ย|จำนอง|จำนำ|หนี้|เจ้าหนี้|ลูกหนี้',
        r'ประมวลกฎหมายแพ่ง|กรรมสิทธิ์|ที่ดิน|อสังหาริมทรัพย์',
        r'หย่า|อุปการะ|มรดก|ทรัพย์สิน|นิติกรรม'
    ]
    
    # คดีปกครอง
    admin_patterns = [
        r'ข้าราชการ|เจ้าหน้าที่|ภาษี|อากร|ใบอนุญาต|ประมูล',
        r'กฎหมายปกครอง|ศาลปกครอง|การจัดซื้อ|การจัดจ้าง'
    ]
    
    # คดีแรงงาน
    labor_patterns = [
        r'ลูกจ้าง|นายจ้าง|ค่าจ้าง|ค่าแรง|เงินชดเชย|ประกันสังคม',
        r'กฎหมายแรงงาน|ศาลแรงงาน|การเลิกจ้าง'
    ]
    
    # ตรวจสอบประเภทคดี
    for pattern in criminal_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return CaseType.CRIMINAL.value
    
    for pattern in civil_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return CaseType.CIVIL.value
    
    for pattern in admin_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return CaseType.ADMINISTRATIVE.value
    
    for pattern in labor_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return CaseType.LABOR.value
    
    return "ไม่ระบุ"

def extract_case_type(text: str) -> Optional[str]:
    """สกัดประเภทคดีจากข้อความ"""
    case_type_mapping = {
        "อาญา": "อาญา",
        "แพ่ง": "แพ่ง", 
        "แรงงาน": "แรงงาน",
        "ภาษี": "ภาษี",
        "คดีอาญา": "อาญา",
        "คดีแพ่ง": "แพ่ง",
        "คดีแรงงาน": "แรงงาน", 
        "คดีภาษี": "ภาษี",
        "ปกครอง": "ปกครอง",
        "ครอบครัว": "ครอบครัว",
        "ล้มละลาย": "ล้มละลาย",
        "ทรัพย์สินทางปัญญา": "ทรัพย์สินทางปัญญา"
    }
    
    text_lower = text.lower()
    for keyword, case_type in case_type_mapping.items():
        if keyword.lower() in text_lower:
            return case_type
    
    return None