"""
Enums for search types and case types
"""

from enum import Enum

class SearchType(str, Enum):
    SIMILARITY = "similarity"
    CASE_NUMBER = "case_number"
    JUDGE = "judge"
    CASE_TYPE = "case_type"
    COMBINED = "combined"
    GRAPHRAG = "graphrag"

class CaseType(str, Enum):
    CRIMINAL = "อาญา"
    CIVIL = "แพ่ง"
    ADMINISTRATIVE = "ปกครอง"
    CONSTITUTIONAL = "รัฐธรรมนูญ"
    LABOR = "แรงงาน"
    TAX = "ภาษี"
    INTELLECTUAL = "ทรัพย์สินทางปัญญา"