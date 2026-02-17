# บทที่ 2
# ทฤษฎีและงานวิจัยที่เกี่ยวข้อง (Theory and Related Literature)

การพัฒนาระบบเว็บแอปพลิเคชันจัดการแข่งขันและตัดสินผลโหวตแบบเรียลไทม์ (BattleHub) จำเป็นต้องศึกษาทฤษฎี หลักการทางวิศวกรรมซอฟต์แวร์ และงานวิจัยที่เกี่ยวข้องเพื่อให้ระบบมีประสิทธิภาพ ปลอดภัย และตอบสนองความต้องการของผู้ใช้งานได้อย่างครบถ้วน ในบทนี้จะกล่าวถึงทฤษฎีและเทคโนโลยีที่ใช้ในการพัฒนา โดยแบ่งเนื้อหาออกเป็นส่วนสำคัญต่าง ๆ ดังนี้

---

## 2.1 ทฤษฎีวิศวกรรมซอฟต์แวร์ (Software Engineering Theory)

วิศวกรรมซอฟต์แวร์ (Software Engineering) เป็นศาสตร์ที่เกี่ยวข้องกับการผลิตซอฟต์แวร์ที่มีคุณภาพ ภายใต้ข้อจำกัดของเวลาและงบประมาณ โดยประยุกต์ใช้หลักการทางวิศวกรรมในการวิเคราะห์ ออกแบบ พัฒนา ทดสอบ และบำรุงรักษาซอฟต์แวร์

### 2.1.1 วงจรการพัฒนาระบบ (Software Development Life Cycle: SDLC)
SDLC คือกระบวนการที่เป็นระบบในการสร้างซอฟต์แวร์ที่มีคุณภาพสูง โดยแบ่งออกเป็นระยะต่าง ๆ เพื่อให้มั่นใจว่าซอฟต์แวร์ที่ได้จะตรงตามความต้องการของผู้ใช้และสามารถตรวจสอบได้ ในการพัฒนา BattleHub คณะผู้จัดทำได้เลือกใช้รูปแบบการพัฒนาแบบผสมผสานระหว่าง **Iterative Model** และแนวคิด **Agile Methodology** เพื่อให้สามารถปรับปรุงและแก้ไขระบบได้อย่างรวดเร็ว

#### 1. ระยะการวางแผนและการวิเคราะห์ (Planning and Requirement Analysis)
ในขั้นตอนนี้ ทีมผู้พัฒนาได้ทำการศึกษารูปแบบการจัดการแข่งขัน E-Sports และกิจกรรมโหวตในปัจจุบัน พบปัญหาหลักคือความล่าช้าในการรวบรวมคะแนนและความยุ่งยากในการจับคู่แข่งขันด้วยมือ จึงได้รวบรวมความต้องการ (Requirements) ทั้ง Functional และ Non-Functional Requirements ดังนี้:
*   **Functional Requirements:** ระบบต้องสามารถสร้างสายการแข่งขันอัตโนมัติ (Bracket Generation), รองรับการโหวตแบบ Real-time, และมีระบบจัดการผู้ใช้งาน (User Management)
*   **Non-Functional Requirements:** ระบบต้องมีความปลอดภัย (Security), รองรับผู้ใช้งานพร้อมกันได้ (Concurrency), และมีหน้าจอที่ตอบสนองรวดเร็ว (Responsiveness)

#### 2. ระยะการออกแบบระบบ (System Design)
เป็นการนำผลวิเคราะห์มาออกแบบโครงสร้างระบบ โดยครอบคลุมถึง:
*   **System Architecture:** ออกแบบสถาปัตยกรรมแบบ Monolithic โดยใช้ Django Framework เป็นแกนหลัก
*   **Database Design:** ออกแบบฐานข้อมูลเชิงสัมพันธ์ (ERV-Diagram) โดยยึดหลัก Normalization เพื่อลดความซ้ำซ้อน
*   **User Interface Design:** ออกแบบหน้าจอ (Wireframe & Mockup) โดยเน้นหลักการ User-Centered Design (UCD) เพื่อให้ใช้งานง่าย

#### 3. ระยะการพัฒนา (Implementation)
ดำเนินการเขียนโปรแกรม (Coding) ตามที่ได้ออกแบบไว้ โดยแบ่งออกเป็น Module ย่อยๆ เช่น Module จัดการผู้ใช้, Module การแข่งขัน, และ Module การแสดงผล เพื่อให้ง่ายต่อการตรวจสอบและแก้ไข (Modular Programming) โดยใช้ Git เป็นเครื่องมือในการจัดการ version control

#### 4. ระยะการทดสอบ (Testing)
ทดสอบระบบใน 2 ระดับหลัก คือ:
*   **Unit Testing:** ทดสอบการทำงานของแต่ละฟังก์ชันย่อย เช่น ฟังก์ชันคำนวณคะแนน, ฟังก์ชันสร้างคู่แข่งขัน
*   **System Testing:** ทดสอบภาพรวมของระบบเมื่อนำทุกส่วนมาประกอบกัน เพื่อหาข้อผิดพลาด (Bugs) และตรวจสอบว่าตอบโจทย์ความต้องการหรือไม่

#### 5. ระยะการติดตั้งและการบำรุงรักษา (Deployment and Maintenance)
นำระบบขึ้นติดตั้งบน Server จำลองโดยใช้ Docker เพื่อลดปัญหาความแตกต่างของสภาพแวดล้อม (Environment Discrepancy) และเตรียมแผนสำหรับการแก้ไขข้อผิดพลาดที่อาจเกิดขึ้นภายหลัง (Maintenance)

### 2.1.2 สถาปัตยกรรม Model-View-Template (MVT)
BattleHub พัฒนาโดยใช้ Django Framework ซึ่งยึดตามสถาปัตยกรรมแบบ **MVT (Model-View-Template)** ซึ่งมีลักษณะคล้ายคลึงกับ MVC (Model-View-Controller) ที่เป็นมาตรฐานสากล แต่มีการแบ่งหน้าที่แตกต่างกันเล็กน้อย ดังตารางเปรียบเทียบต่อไปนี้:

**ตารางที่ 2.1** เปรียบเทียบสถาปัตยกรรม MVC และ MVT

| องค์ประกอบ | MVC (General Concept) | MVT (Django Implementation) | หน้าที่ความรับผิดชอบ (Responsibilities) |
| :--- | :--- | :--- | :--- |
| **ส่วนจัดการข้อมูล** | **Model** | **Model** | กำหนดโครงสร้างข้อมูล (Schema), ความสัมพันธ์ (Relationships), และกฎเกณฑ์ความถูกต้อง (Validation) ทำหน้าที่ติดต่อกับฐานข้อมูลโดยตรง |
| **ส่วนควบคุมการทำงาน** | **Controller** | **View** | รับ Request จากผู้ใช้, ประมวลผล Business Logic, ตัดสินใจเลือกข้อมูลจาก Model, และส่งข้อมูลไปยังส่วนแสดงผล |
| **ส่วนแสดงผล** | **View** | **Template** | รับผิดชอบเรื่องการนำเสนอข้อมูล (Presentation Layer) ในรูปแบบ HTML/CSS เพื่อส่งกลับไปยังผู้ใช้ |

การเลือกใช้ MVT Architecture ช่วยให้การพัฒนา BattleHub มีข้อดีดังนี้:
1.  **Separation of Concerns:** แยกส่วน Logic (Python) ออกจาก Presentation (HTML) อย่างชัดเจน ทำให้นักพัฒนา Backend และ Frontend สามารถทำงานร่วมกันได้ง่าย
2.  **Rapid Development:** ลดความซับซ้อนในการเขียน SQL ด้วยการใช้ ORM (Object-Relational Mapping) ผ่าน Model
3.  **Reusability:** Template สามารถนำกลับมาใช้ซ้ำได้ (Template Inheritance) ทำให้ code สะอาดและดูแลรักษาง่าย

---

## 2.2 เทคโนโลยีเว็บแอปพลิเคชัน (Web Application Technologies)

การพัฒนาเว็บแอปพลิเคชันสมัยใหม่จำเป็นต้องมีความเข้าใจในโปรโตคอลการสื่อสารและโครงสร้างพื้นฐานของระบบเครือข่าย เพื่อให้ระบบทำงานได้อย่างมีประสิทธิภาพ

### 2.2.1 โปรโตคอล HTTP และวงจรการทำงาน (HTTP Protocol & Request-Response Cycle)
**HTTP (Hypertext Transfer Protocol)** เป็นโปรโตคอลมาตรฐานในการแลกเปลี่ยนข้อมูลบน World Wide Web โดยทำงานในรูปแบบ **Client-Server Model**
1.  **Client (Web Browser):** ผู้ใช้ทำการกระทำ (Click, Submit Form) ซึ่งจะถูกแปลงเป็น HTTP Request ส่งไปยัง Server
2.  **Server (Web Server):** รับ Request และส่งต่อให้ Application (Django) ประมวลผล จากนั้นส่งคืนผลลัพธ์ในรูปแบบ HTTP Response

**องค์ประกอบสำคัญของ HTTP Request/Response ที่ใช้ใน BattleHub:**
*   **Methods:**
    *   `GET`: ใช้สำหรับดึงข้อมูล (เช่น การดูรายการทัวร์นาเมนต์)
    *   `POST`: ใช้สำหรับส่งข้อมูลเพื่อประมวลผล (เช่น การสมัครสมาชิก, การกดโหวต) โดยจะมีการแนบ CSRF Token เพื่อความปลอดภัย
*   **Status Codes:**
    *   `200 OK`: ดำเนินการสำเร็จ
    *   `302 Found`: เปลี่ยนเส้นทาง (Redirect) ไปยังหน้าอื่น
    *   `403 Forbidden`: ปฏิเสธการเข้าถึง (เช่น ไม่มีสิทธิ์ Admin, CSRF Failed)
    *   `404 Not Found`: ไม่พบหน้าที่ร้องขอ
    *   `500 Internal Server Error`: เกิดข้อผิดพลาดที่ฝั่ง Server

### 2.2.2 การเปรียบเทียบเทคโนโลยี Real-time (WebSockets vs AJAX Polling)
ฟีเจอร์ "Real-time Update" เป็นหัวใจสำคัญของ BattleHub เพื่อแสดงคะแนนโหวตและสถานะ Lobby ทันทีที่มีการเปลี่ยนแปลง ผู้พัฒนาได้ศึกษาเปรียบเทียบ 2 เทคโนโลยีหลัก:

#### 1. WebSockets (Full-Duplex Communication)
WebSockets เป็นโปรโตคอลที่เปิดช่องทางการสื่อสารแบบสองทาง (Bi-directional) ค้างไว้ระหว่าง Client และ Server ทำให้ Server สามารถ "Push" ข้อมูลไปหา Client ได้ทันทีโดยไม่ต้องรอให้ Client ร้องขอ
*   **ข้อดี:** Latency ต่ำมาก (ระดับ Millisecond), ลด Overhead ของ Header ในการส่งข้อมูลซ้ำๆ
*   **ข้อเสีย:** มีความซับซ้อนในการ Implement สูง, ต้องใช้ State-full connection ซึ่งกินทรัพยากร Server หากมีผู้ใช้จำนวนมาก (C10k Problem), การจัดการ Proxy/Firewall อาจยุ่งยาก

#### 2. AJAX Polling (Client-Pull Communication)
AJAX (Asynchronous JavaScript and XML) Polling คือเทคนิคที่ Client ส่ง HTTP Request ไปถาม Server เป็นระยะๆ (เช่น ทุก 2 วินาที) ว่า "มีข้อมูลใหม่หรือไม่?"
*   **ข้อดี:** ง่ายต่อการพัฒนา (Simplicity) เพราะใช้ HTTP มาตรฐาน, Stateless (ไม่เปลือง Connection ค้าง), เข้ากันได้กับทุก Infrastructure เดิม
*   **ข้อเสีย:** อาจมีความล่าช้า (Latency) ระหว่างรอบการ Poll (เช่น ข้อมูลมาช้าไป 1.9 วินาที), สร้าง Traffic จำนวนมากหาก Poll ถี่เกินไป

**บทสรุปการเลือกใช้เทคโนโลยี:**
BattleHub เลือกใช้ **AJAX Short Polling** (Interval 2000ms) โดยมีเหตุผลสนับสนุนดังนี้:
1.  **ความเหมาะสมกับบริบท:** การแข่งขันโหวตไม่ได้ต้องการความเร็วระดับ Millisecond เหมือนเกม FPS การดีเลย์ 1-2 วินาที เป็นสิ่งที่ยอมรับได้สำหรับประสบการณ์ผู้ใช้ (User Experience)
2.  **ความคุ้มค่า (Cost-Benefit):** การใช้ Polling ลดความซับซ้อนของ Server Architecture ไม่ต้องติดตั้งบริการเสริมอย่าง Redis หรือใช้ ASGI Server (Daphne/Uvicorn) ทำให้ Deployment ง่ายและประหยัดทรัพยากร
3.  **ความเสถียร:** หาก Connection หลุด การ Polling จะเชื่อมต่อใหม่ได้ง่ายกว่า (Auto-retry) ในขณะที่ WebSocket อาจต้องมี logic การ Reconnect ที่ซับซ้อน

### 2.2.3 เทคโนโลยีฐานข้อมูล (Database Technology: PostgreSQL)
ระบบเลือกใช้ **PostgreSQL** ซึ่งเป็นระบบจัดการฐานข้อมูลเชิงสัมพันธ์ (RDBMS) แบบ Open Source ขั้นสูง
*   **ACID Compliant:** รองรับ Atomicity, Consistency, Isolation, Durability อย่างสมบูรณ์ มั่นใจได้ว่าข้อมูลคะแนนโหวตจะไม่สูญหายหรือผิดเพี้ยนแม้ระบบล่ม
*   **JSONB Support:** รองรับการเก็บข้อมูลแบบ NoSQL (JSON) ซึ่งมีประโยชน์ในการเก็บ Config ของทัวร์นาเมนต์ที่มีความยืดหยุ่นสูง หรือเก็บ Audit Logs
*   **Concurrency Control:** ใช้ MVCC (Multiversion Concurrency Control) ช่วยให้รองรับการอ่านและเขียนข้อมูลพร้อมกันได้ดีกว่า SQLite ซึ่งมีการล็อกทั้งไฟล์ (Database Locking) เหมาะสำหรับสถานการณ์ having multiple voters voting simultaneously.

---

*(จบบริบูรณ์ส่วนที่ 1: ทฤษฎีวิศวกรรมซอฟต์แวร์และเทคโนโลยีเว็บแอปพลิเคชัน)*
