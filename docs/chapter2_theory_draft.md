# บทที่ 2: ทฤษฎีและงานวิจัยที่เกี่ยวข้อง (Theory and Related Research)

## 2.1 ทฤษฎีเกี่ยวกับการแข่งขัน (Tournament Theory)
- **ประเภทของการแข่งขัน**
    - Single Elimination (แพ้คัดออก) - ใช้ใน BattleHub
    - Double Elimination (แพ้สองครั้งคัดออก)
    - Round Robin (พบกันหมด)
    - Swiss System
- **โครงสร้าง Bracket (Bracket Structure)**
    - การคำนวณจำนวนรอบ (Rounds = log2(N))
    - การจัดวางคู่แข่งขัน (Seeding)
    - การจัดการ Byes (ในกรณีผู้แข่งไม่ครบจำนวน $2^n$)

## 2.2 ระบบการลงคะแนนและการตัดสินใจ (Voting Systems & Decision Making)
- **ทฤษฎีการโหวต (Voting Theory)**
    - Majority Vote (เสียงข้างมาก) - ใช้ใน BattleHub
    - Plurality Vote
    - Ranked Voting (Instant Runoff)
- **ปัญหาในการโหวตออนไลน์**
    - Sybil Attack (การปั๊มโหวต)
    - Vote Manipulation
    - การแก้ปัญหา: Authentication Required, Rate Limiting, CAPTCHA

## 2.3 เทคโนโลยีเว็บแอปพลิเคชัน (Web Application Technologies)
- **สถาปัตยกรรม Model-View-Template (MVT)**
    - เปรียบเทียบ MVC cs MVT
    - ประโยชน์ของ Django Framework
- **การสื่อสารแบบ Real-time (Real-time Communication)**
    - **AJAX Polling** (Short Polling) - รูปแบบที่ BattleHub เลือกใช้
        - หลักการทำงาน (Request-Response Loop)
        - ข้อดี vs ข้อเสีย
    - **Long Polling**
    - **WebSocket** (Full Duplex)
        - Django Channels
        - เปรียบเทียบ Performance & Complexity
- **Database Management Systems (RDMS)**
    - ACID Properties
    - PostgreSQL Features (JSONB, Full-text Search)

## 2.4 เครื่องมือที่ใช้ในการพัฒนา (Development Tools)
- **Language:** Python 3.12
- **Framework:** Django 5.0
- **Frontend Stack:** HTML5, CSS3, JavaScript (Vanilla ES6+), Tailwind CSS
- **Database:** PostgreSQL
- **Diagram Tools:** PlantUML (Code-as-Diagram)

## 2.5 งานวิจัยที่เกี่ยวข้อง (Related Research)
**ตารางเปรียบเทียบเทคนิคจากงานวิจัย (Comparison of Related Works)**

| ชื่องานวิจัย (Author, Year) | เทคนิคที่ใช้ (Methodology) | ข้อดี (Pros) | ข้อจำกัด (Cons) | การนำมาประยุกต์ใช้ใน BattleHub |
| :--- | :--- | :--- | :--- | :--- |
| **Research A: Online Tournament Management System using Genetic Algorithm** (2020) | Genetic Algorithm สำหรับจัดตารางแข่ง | จัดตารางได้มีประสิทธิภาพสูง ลดความขัดแย้งของเวลา | ซับซ้อน ใช้ทรัพยากรเครื่องสูง | นำแนวคิดเรื่อง Bracket Generation มาปรับใช้แบบสุ่ม (Random Shuffle) แทนเพื่อความรวดเร็ว |
| **Research B: Real-time Voting Platform with WebSocket** (2021) | WebSocket, Node.js | ข้อมูล Real-time มาก Latency ต่ำ | ต้องใช้ Server พิเศษ (Redis layer) จัดการ Connection ยาก | เลือกใช้ AJAX Polling แทนเพื่อลดความซับซ้อนของ Server Architecture เนื่องจาก Update Rate ไม่ถี่มาก (2-3 วินาที) |
| **Research C: Anti-Cheat Mechanisms in Online E-Sports** (2019) | AI Behavior Analysis | ตรวจจับการโกงได้แม่นยำ | ต้องใช้ Dataset มหาศาลในการ Train | ใช้ระบบ Audit Log และ Manual Moderation แทน เนื่องจากสโคปงานเน้น Community ขนาดเล็ก |
| **Research D: Crowd-sourced Judging Systems** (2022) | Weighted Voting (ให้คะแนนตามเครดิต) | คะแนนมีความน่าเชื่อถือสูง | ระบบคำนวณซับซ้อน ผู้ใช้ใหม่อาจรู้สึกไม่ยุติธรรม | ใช้ระบบ 1 Man 1 Vote ที่เท่าเทียมกัน แต่ป้องกัน Sybil Attack ด้วย User Authentication |
| **Research E: Scalable Web Architecture for High Traffic Events** (2023) | Microservices, Load Balancer | รองรับคนได้หลักล้าน | Cost สูง ดูแลรักษายาก | ใช้ Monolithic Architecture (Django) ที่ดูแลง่าย เหมาะกับ Phase แรกของโปรเจกต์ |

## 2.6 สรุป (Conclusion)
- สรุปเทคโนโลยีที่เลือกใช้ว่าเหมาะสมกับ Requirement และ Resource ที่มีอย่างไร
- ยืนยันว่าการเลือกใช้ **Django + AJAX Polling** เหมาะสมที่สุดสำหรับ BattleHub ในแง่ของ Maintainability vs Performance
