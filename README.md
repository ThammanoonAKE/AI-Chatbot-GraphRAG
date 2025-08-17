# ระบบค้นหาคดีกฎหมายไทย พร้อม GraphRAG

🏛️ **ระบบค้นหาคดีกฎหมายไทยขั้นสูงพร้อม GraphRAG และหน้าเว็บ React**

แชทบอท AI ที่ทันสมัยซึ่งผสมผสาน **GraphRAG (Graph Retrieval-Augmented Generation)** กับการค้นหาด้วย Vector เพื่อให้การวิเคราะห์คดีกฎหมายและคำแนะนำที่ชาญฉลาดสำหรับเอกสารกฎหมายไทย

## ✨ คุณสมบัติเด่น

### 🧠 เทคโนโลยี GraphRAG
- **สร้างกราฟความรู้**: สร้างความสัมพันธ์ระหว่างคดี ผู้พิพากษา แนวคิดทางกฎหมาย และประเภทคดีโดยอัตโนมัติ
- **การค้นหากลุ่มข้อมูล**: ระบุกลุ่มคดีที่เกี่ยวข้องกันด้วย Louvain algorithm
- **การค้นหาที่ดีขึ้น**: ผสมผสานการค้นหาด้วย Vector similarity กับ Context จากกราฟ
- **วิเคราะห์ความสัมพันธ์**: ค้นพบความเชื่อมโยงที่ซ่อนอยู่ระหว่างหน่วยงานทางกฎหมาย

### 🔍 ความสามารถในการค้นหาขั้นสูง
- **การค้นหาหลายรูปแบบ**: หมายเลขคดี ชื่อผู้พิพากษา ประเภทคดี แนวคิดทางกฎหมาย
- **การค้นหาเชิงความหมาย**: Vector embeddings ใช้ Sentence Transformers
- **ผลลัพธ์ที่เสริมด้วยกราฟ**: คดีที่เกี่ยวข้องเพิ่มเติมจากการสำรวจกราฟความรู้
- **การตรวจจับเจตนาอัจฉริยะ**: กำหนดกลยุทธ์การค้นหาโดยอัตโนมัติตามคำสอบถาม

### 🎯 การวิเคราะห์ด้วย AI
- **การรวม Google Gemini**: การวิเคราะห์และการใช้เหตุผลข้อความทางกฎหมายขั้นสูง
- **การตอบสนองเชิงบริบท**: ใช้ทั้ง Vector และ Graph context เพื่อคำตอบที่ครอบคลุม
- **รองรับภาษาไทย**: การประมวลผลข้อความไทยและการทำให้เป็นมาตรฐานเฉพาะ
- **ความเชี่ยวชาญด้านกฎหมาย**: เน้นศัพท์และแนวคิดทางกฎหมายไทย

### 🖥️ หน้าเว็บสมัยใหม่
- **React 18**: อินเทอร์เฟซผู้ใช้ที่ทันสมัย
- **Material-UI**: องค์ประกอบการออกแบบแบบมืออาชีพ
- **Framer Motion**: ภาพเคลื่อนไหวและการเปลี่ยนผ่านที่ราบรื่น
- **Glass Morphism**: เอฟเฟกต์ภาพที่สวยงาม
- **แชทแบบเรียลไทม์**: อินเทอร์เฟซการสนทนาแบบโต้ตอบ

## 🏗️ สถาปัตยกรรม

```
ระบบกฎหมายไทย GraphRAG
├── Frontend (React + Vite)
│   ├── React Components
│   ├── Material-UI Design
│   └── API Integration
├── Backend (FastAPI + Python)
│   ├── GraphRAG Engine
│   ├── Vector Search (FAISS)
│   ├── Knowledge Graph (NetworkX)
│   └── AI Integration (Gemini)
└── Data Processing
    ├── คดีกฎหมายไทย (JSON)
    ├── Vector Embeddings
    └── Knowledge Graph
```

## 📦 การติดตั้ง

### ความต้องการเบื้องต้น
- **Python 3.10+**
- **Node.js 16+**
- **Git**

### 1. ดาวน์โหลดโปรเจ็ค
```bash
git clone <repository-url>
cd AI-Chatbot-GraphRAG
```

### 2. ตั้งค่า Backend
```bash
# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# ติดตั้ง Python dependencies
pip install -r requirements.txt
```

### 3. ตั้งค่า Frontend
```bash
# ติดตั้ง Node.js dependencies
npm install
```

### 4. การกำหนดค่าสภาพแวดล้อม
```bash
# คัดลอก template สภาพแวดล้อม
cp .env.example .env

# แก้ไขไฟล์ .env ด้วย API keys ของคุณ
# จำเป็น: GEMINI_API_KEY
```

### 5. การเตรียมข้อมูล
- วางไฟล์ JSON คดีกฎหมายไทยในไดเรกทอรี `json_cases/`
- แต่ละไฟล์ JSON ควรมี metadata ของคดี (decision_id, title, summary, judges, ฯลฯ)

## 🚀 การรันแอปพลิเคชัน

### โหมดพัฒนา

#### เริ่ม Backend (Terminal 1)
```bash
# เปิดใช้งาน virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# เริ่ม FastAPI server
python main.py
```
Backend ทำงานที่: `http://localhost:8000`

#### เริ่ม Frontend (Terminal 2)
```bash
# เริ่ม React development server
npm run dev
```
Frontend ทำงานที่: `http://localhost:3000`

### Production
```bash
# สร้าง React frontend
npm run build

# เริ่ม production server
python main.py
```

## 📊 องค์ประกอบ GraphRAG

### โครงสร้างกราฟความรู้
- **โหนด**: คดี, ผู้พิพากษา, แนวคิดทางกฎหมาย, ประเภทคดี, มาตราที่เกี่ยวข้อง
- **ขอบ**: ความสัมพันธ์เช่น "ประกอบด้วย", "ดำเนินการ", "คล้ายกับ", "เกี่ยวข้องกับ"
- **ชุมชน**: กลุ่มของเอนทิตีที่เกี่ยวข้องกันที่ตรวจพบโดยอัตโนมัติ

### การค้นหาที่เสริมด้วยกราฟ
1. **การค้นหา Vector**: การค้นคืนเบื้องต้นตามความคล้ายคลึง
2. **การสำรวจกราฟ**: ค้นหาเอนทิตีที่เกี่ยวข้องผ่านกราฟความรู้
3. **บริบทชุมชน**: รวมเอนทิตีจากชุมชนเดียวกัน
4. **การให้คะแนนความเกี่ยวข้อง**: ผสมผสานคะแนนตาม Vector และกราฟ

### ประเภทความสัมพันธ์
- `contains`: คดีประกอบด้วยแนวคิดทางกฎหมาย/ผู้พิพากษา
- `handles`: ผู้พิพากษาดำเนินการประเภทคดี
- `similar_to`: คดีที่มีความคล้ายคลึงสูง
- `deals_with`: ผู้พิพากษาเกี่ยวข้องกับแนวคิดทางกฎหมาย
- `related`: ความสัมพันธ์ทั่วไป

## 🔧 การกำหนดค่า

### ตัวแปรสภาพแวดล้อม (.env)
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# เส้นทาง
JSON_FOLDER=json_cases
EMBEDDINGS_FOLDER=data/embeddings
GRAPHS_FOLDER=data/graphs

# การกำหนดค่า API
API_HOST=0.0.0.0
API_PORT=8000

# พารามิเตอร์ GraphRAG
MAX_CONTEXT=10000          # จำนวนตัวอักษรสูงสุดที่ส่งให้ AI
CHUNK_SIZE=8000           # ขนาดของแต่ละชิ้นข้อมูล
CHUNK_OVERLAP=800         # ส่วนที่ทับซ้อนระหว่างชิ้นข้อมูล
MIN_CHUNK_SIZE=500        # ขนาดข้อมูลขั้นต่ำ
COMMUNITY_RESOLUTION=1.0  # ความละเอียดในการจัดกลุ่ม
MIN_COMMUNITY_SIZE=3      # ขนาดกลุ่มขั้นต่ำ
MAX_GRAPH_DEPTH=3         # ความลึกสูงสุดของกราฟ
```

### ประเภทการค้นหา
- `similarity`: การค้นหาเชิงความหมายด้วย Vector
- `case_number`: การจับคู่หมายเลขคดีที่แน่นอน
- `judge`: การค้นหาชื่อผู้พิพากษาด้วย fuzzy matching
- `case_type`: กรองตามหมวดหมู่คดี
- `graphrag`: การค้นหาเสริมด้วยกราฟความรู้
- `combined`: การค้นหาหลายกลยุทธ์อย่างชาญฉลาด (ค่าเริ่มต้น)

## 📡 จุดปลาย API

### แชทและค้นหา
- `POST /chat` - แชท AI ด้วยการเสริม GraphRAG
- `POST /search` - การค้นหาขั้นสูงด้วยเกณฑ์หลายอย่าง
- `GET /search/case/{case_number}` - ค้นหาตามหมายเลขคดี
- `GET /search/judge/{judge_name}` - ค้นหาตามชื่อผู้พิพากษา
- `GET /search/type/{case_type}` - ค้นหาตามประเภทคดี

### ข้อมูล
- `GET /info/case-types` - ประเภทคดีที่มีอยู่
- `GET /info/judges` - ผู้พิพากษาในระบบ
- `GET /info/statistics` - สถิติระบบ
- `GET /graph/stats` - สถิติกราฟความรู้

### เอกสาร
- `GET /docs` - เอกสาร API แบบโต้ตอบ
- `GET /` - ข้อมูล API และจุดปลาย

## 🏛️ คุณสมบัติด้านกฎหมาย

### ประเภทคดีกฎหมายไทย
- **อาญา** (Criminal)
- **แพ่ง** (Civil)
- **แรงงาน** (Labor)
- **ภาษี** (Tax)
- **ปกครอง** (Administrative)
- **ครอบครัว** (Family)
- **ทรัพย์สินทางปัญญา** (Intellectual Property)

### การสกัดแนวคิดทางกฎหมาย
- การตรวจจับศัพท์และแนวคิดทางกฎหมายโดยอัตโนมัติ
- การอ้างอิงมาตรากฎหมายไทย
- การรู้จำรูปแบบหมายเลขคดี
- การทำให้ชื่อผู้พิพากษาเป็นมาตรฐาน
- การระบุความสัมพันธ์ทางกฎหมาย

### การประมวลผลข้อความ
- การทำให้ Unicode ไทยเป็นมาตรฐาน
- การสกัดคำสำคัญทางกฎหมาย
- การแบ่งเอกสารด้วยการทับซ้อน
- การให้คะแนนความคล้ายคลึงสำหรับข้อความไทย

## 🛠️ การพัฒนา

### โครงสร้างโปรเจ็ค
```
AI-Chatbot-GraphRAG/
├── src/
│   ├── api/                # API routes และ handlers
│   ├── ai/                 # AI response generation
│   ├── config/             # การกำหนดค่าระบบ
│   ├── graphrag/           # การใช้งาน GraphRAG
│   │   ├── knowledge_graph.py
│   │   └── graph_retriever.py
│   ├── models/             # Data models และ schemas
│   ├── processing/         # การประมวลผลข้อความ
│   ├── search/             # เครื่องมือค้นหาต่างๆ
│   └── utils/              # ฟังก์ชันยูทิลิตี้
├── src/components/         # React components
├── data/
│   ├── embeddings/         # Vector embeddings
│   └── graphs/            # ข้อมูลกราฟความรู้
├── json_cases/            # ข้อมูลคดีกฎหมาย
├── main.py                # FastAPI backend
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies
└── vite.config.js        # การกำหนดค่า Vite
```

### การเพิ่มคุณสมบัติใหม่
1. **ประเภทการค้นหาใหม่**: ขยาย enum `SearchType` และใช้งานฟังก์ชันค้นหา
2. **ความสัมพันธ์กราฟ**: เพิ่มประเภทขอบใหม่ใน `LegalKnowledgeGraph`
3. **องค์ประกอบ UI**: สร้างองค์ประกอบ React ใน `src/components/`
4. **จุดปลาย API**: เพิ่ม FastAPI routes ใหม่ใน API modules

## 📈 ประสิทธิภาพและการปรับขนาด

### คุณสมบัติการเพิ่มประสิทธิภาพ
- **การจัดทำดัชนี FAISS**: การค้นหาความคล้ายคลึงที่รวดเร็วสำหรับชุดข้อมูลขนาดใหญ่
- **การประมวลผลแบบกลุ่ม**: การสร้าง embedding ที่มีประสิทธิภาพ
- **การแคชกราฟ**: การจัดเก็บกราฟความรู้แบบถาวร
- **การตรวจจับชุมชน**: ลดพื้นที่การค้นหาผ่านการจัดกลุ่ม

### ข้อพิจารณาการปรับขนาด
- **FAISS แบบกระจาย**: สำหรับการรวบรวมคดีขนาดใหญ่
- **ฐานข้อมูลกราฟ**: การรวม Neo4j สำหรับกราฟที่ซับซ้อน
- **เลเยอร์แคช**: Redis สำหรับการสอบถามที่พบบ่อย
- **การปรับสมดุลภาระ**: อินสแตนซ์ backend หลายตัว

## 🔒 ความปลอดภัยและความเป็นส่วนตัว

### การป้องกันข้อมูล
- การจัดการ API key ตามสภาพแวดล้อม
- ไม่มีความลับ hardcode ในโค้ด
- การสื่อสาร API ที่ปลอดภัย
- การตรวจสอบและทำความสะอาดข้อมูลนำเข้า

### การปฏิบัติตามกฎหมาย
- เน้นเอกสารกฎหมายสาธารณะ
- ไม่จัดเก็บข้อมูลส่วนบุคคล
- ร่องรอยการตรวจสอบสำหรับการวิจัยทางกฎหมาย
- แนวปฏิบัติ AI ที่มีจริยธรรม

## 🤝 การมีส่วนร่วม

1. Fork repository
2. สร้าง feature branch: `git checkout -b feature/new-feature`
3. Commit การเปลี่ยนแปลง: `git commit -am 'Add new feature'`
4. Push ไปยัง branch: `git push origin feature/new-feature`
5. ส่ง Pull Request

## 📜 ใบอนุญาต

โปรเจ็คนี้ได้รับอนุญาตภายใต้ MIT License - ดูไฟล์ [LICENSE](LICENSE) สำหรับรายละเอียด

## 🙏 กิตติกรรมประกาศ

- **Sentence Transformers** สำหรับ embeddings หลายภาษา
- **FAISS** สำหรับการค้นหาความคล้ายคลึงที่มีประสิทธิภาพ
- **NetworkX** สำหรับการประมวลผลกราฟ
- **Google Gemini** สำหรับการวิเคราะห์ที่ขับเคลื่อนด้วย AI
- **React & Material-UI** สำหรับ frontend ที่ทันสมัย
- **FastAPI** สำหรับ backend ที่มีประสิทธิภาพสูง



---

**แชทบอทกฎหมายไทย GraphRAG** - พัฒนาการวิจัยทางกฎหมายด้วย AI และกราฟความรู้ 🏛️⚡