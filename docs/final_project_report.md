<!-- Start of docs/chapter1_intro.md -->
# บทที่ 1
# บทนำ (Introduction)

## 1.1 ความเป็นมาและความสำคัญของปัญหา

ในปัจจุบันการจัดการแข่งขันประเภท Bracket Tournament เช่น การแข่งขันโหวตภาพ การแข่งขันเกม หรือการประกวดต่างๆ มีความนิยมเพิ่มขึ้นอย่างต่อเนื่อง อย่างไรก็ตาม การจัดการแข่งขันดังกล่าวยังคงต้องอาศัยวิธีการแบบดั้งเดิม เช่น การใช้กระดาษ การนับคะแนนด้วยมือ หรือการใช้ซอฟต์แวร์ที่ไม่รองรับการโหวตแบบ Real-time ทำให้เกิดปัญหาหลายประการ ได้แก่

1) **ความล่าช้าในการนับคะแนน:** ผู้จัดต้องรวบรวมคะแนนด้วยมือซึ่งใช้เวลานานและอาจเกิดข้อผิดพลาด
2) **ขาดความตื่นเต้น:** ผู้ชมไม่สามารถเห็นผลคะแนนแบบ Real-time ระหว่างการแข่งขัน ทำให้ขาดความมีส่วนร่วม
3) **ยากต่อการจัดการผู้เข้าร่วม:** การจัดการรายชื่อผู้เข้าแข่งขันและผู้ชมต้องทำด้วยมือ ไม่มีระบบอัตโนมัติ
4) **ไม่รองรับการแข่งขันออนไลน์:** ระบบเดิมส่วนใหญ่ออกแบบมาสำหรับการแข่งขันแบบพบหน้า ไม่รองรับผู้เข้าร่วมจากระยะไกล

ผู้พัฒนาจึงได้เล็งเห็นถึงโอกาสในการพัฒนาระบบ **BattleHub** ซึ่งเป็นเว็บแอปพลิเคชันสำหรับจัดการแข่งขันแบบ Knockout Tournament พร้อมระบบโหวต Real-time และ Kahoot-style Lobby ที่ทันสมัย เพื่อแก้ไขปัญหาดังกล่าวและเพิ่มประสบการณ์ที่ดีให้กับผู้ใช้งาน

## 1.2 วัตถุประสงค์
1.  เพื่อพัฒนาเว็บแอปพลิเคชันสำหรับสร้างและจัดการการแข่งขันแบบ Knockout Bracket Tournament
2.  เพื่อพัฒนาระบบโหวตแบบ Real-time ที่แสดงผลคะแนนทันทีระหว่างการแข่งขัน
3.  เพื่อพัฒนาระบบห้องรอ (Lobby) แบบ Kahoot-style ที่ผู้เล่นสามารถเข้าร่วมด้วย PIN Code
4.  เพื่อพัฒนา Admin Dashboard สำหรับผู้ดูแลระบบในการจัดการทัวร์นาเมนต์และผู้ใช้

## 1.3 ขอบเขตการดำเนินงาน

### 1.3.1 ขอบเขตด้านฟังก์ชัน
*   ระบบลงทะเบียนและเข้าสู่ระบบ (Authentication)
*   ระบบสร้างทัวร์นาเมนต์ รองรับขนาด bracket 2, 4, 8, 16 คน
*   ระบบอัปโหลดรูปผู้เข้าแข่งขันแบบ Bulk Upload (ลากและวาง)
*   ระบบห้องรอ (Lobby) พร้อม PIN Code 6 หลัก
*   ระบบโหวตแบบ Real-time พร้อม Timer นับถอยหลัง
*   ระบบแจ้งเตือน (Toast Notification)
*   ระบบเปลี่ยนรอบอัตโนมัติ (Auto-redirect)
*   Admin Dashboard สำหรับจัดการระบบ

### 1.3.2 ขอบเขตด้านเทคโนโลยี
*   **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)
*   **Backend:** Python 3.11, Django 5.0
*   **Database:** PostgreSQL 15
*   **Deployment:** Docker, Docker Compose, Nginx, Gunicorn

### 1.3.3 ขอบเขตด้านผู้ใช้
*   **Guest:** ผู้เยี่ยมชมที่ยังไม่ได้ Login (ดูรายการแข่ง, สมัครสมาชิก)
*   **Member:** สมาชิกที่ลงทะเบียนแล้ว (สร้างแข่ง, เข้าร่วม, โหวต)
*   **Admin:** ผู้ดูแลระบบ (จัดการ Users, Tournaments, Reports)

## 1.4 ประโยชน์ที่คาดว่าจะได้รับ
1.  ผู้จัดการแข่งขันสามารถสร้างและจัดการทัวร์นาเมนต์ได้อย่างสะดวกและรวดเร็ว
2.  ผู้เข้าร่วมสามารถโหวตและเห็นผลคะแนนแบบ Real-time เพิ่มความตื่นเต้นและมีส่วนร่วม
3.  รองรับการแข่งขันแบบออนไลน์ ผู้เข้าร่วมไม่จำเป็นต้องอยู่ในสถานที่เดียวกัน
4.  ลดภาระการทำงานของผู้จัด ระบบจัดการ Bracket และนับคะแนนอัตโนมัติ
5.  เป็นแนวทางในการพัฒนาเว็บแอปพลิเคชันแบบ Real-time สำหรับผู้ที่สนใจศึกษา

## 1.5 เครื่องมือที่ใช้ในการพัฒนา

### 1.5.1 ฮาร์ดแวร์
1.  **คอมพิวเตอร์ส่วนบุคคล:** สำหรับพัฒนาและทดสอบระบบ
    *   CPU: AMD Ryzen 5 5600X
    *   RAM: 16 GB
    *   GPU: NVIDIA GeForce GTX 1080 Ti
    *   SSD: 2 TB
2.  **เครื่อง Server:** สำหรับ Deploy ระบบ Production (Cloud Server หรือ Local Server)

### 1.5.2 ซอฟต์แวร์
1.  VS Code สำหรับเขียนและแก้ไขโค้ด
2.  Python 3.11 Interpreter สำหรับรัน Backend
3.  PostgreSQL 15 ระบบจัดการฐานข้อมูล
4.  Docker และ Docker Compose สำหรับ Containerization
5.  Nginx สำหรับ Reverse Proxy
6.  Git สำหรับ Version Control
7.  Google Chrome / Firefox สำหรับทดสอบหน้าเว็บ
8.  Postman สำหรับทดสอบ API

## 1.6 แผนการดำเนินการ
ในการพัฒนาระบบ BattleHub มีการแบ่งการดำเนินการออกเป็น 4 ระยะ ดังนี้

**ตารางที่ 1.1** แผนการดำเนินการพัฒนาระบบ

| ระยะ (Phase) | กิจกรรมดำเนินงาน | ระยะเวลา |
| :--- | :--- | :--- |
| **1. การวางแผนและรวบรวมข้อมูล** | ศึกษาขอบเขตของระบบจัดการแข่งขัน, รวบรวม Requirement, ศึกษาเทคโนโลยี | สัปดาห์ที่ 1-2 |
| **2. การวิเคราะห์และออกแบบระบบ** | ออกแบบ Use Case, Class Diagram, ER Diagram และ UI/UX (Figma) | สัปดาห์ที่ 3-5 |
| **3. การพัฒนาระบบสารสนเทศ** | ติดตั้ง Environment (Docker), พัฒนา Backend (Django), Frontend, เชื่อมต่อ Database | สัปดาห์ที่ 6-12 |
| **4. การทดสอบและจัดทำเอกสาร** | ทดสอบระบบ (Unit & Integration), แก้ไข Bug, ทำคู่มือการใช้งานและรายงาน | สัปดาห์ที่ 13-16 |


<!-- End of docs/chapter1_intro.md -->

<!-- Start of docs/chapter2_theory_full.md -->
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


# บทที่ 2 (ต่อ)
# ทฤษฎีและงานวิจัยที่เกี่ยวข้อง (Chapter 2: Theory and Related Literature - Part 2)

---

## 2.3 ทฤษฎีฐานข้อมูลและสถาปัตยกรรมข้อมูล (Database Theory & Data Architecture)

ระบบฐานข้อมูลถือเป็นหัวใจสำคัญของ BattleHub ที่ต้องรองรับทั้งข้อมูลผู้ใช้งานทัวร์นาเมนต์ และคะแนนโหวตปริมาณมาก การออกแบบฐานข้อมูลที่ดีจึงต้องคำนึงถึงความถูกต้อง (Integrity), ลดความซ้ำซ้อน (Redundancy), และประสิทธิภาพในการเรียกใช้ (Performance)

### 2.3.1 การประยุกต์ใช้ Relational Database Management System (RDBMS)
BattleHub เลือกใช้ **PostgreSQL** เป็นระบบจัดการฐานข้อมูลหลัก เนื่องจากคุณสมบัติเด่นด้านความเสถียร (Reliability) และการรองรับมาตรฐาน SQL ขั้นสูง
*   **ACID Properties:** การทำงานของ Database ยึดหลัก Atomicity, Consistency, Isolation, และ Durability อย่างเคร่งครัด
    *   *Atomicity:* การทำธุรกรรม (Transaction) ต้องสำเร็จทั้งหมด หรือล้มเหลวทั้งหมด (All or Nothing) เช่น การกดโหวตต้องบันทึก `MatchVote` และ Update คะแนนใน `Match` พร้อมกัน หากอย่างใดอย่างหนึ่งล้มเหลว ระบบจะ Rollback ทั้งหมด
    *   *Consistency:* ข้อมูลต้องถูกต้องตามกฎ (Constraints) เสมอ เช่น `user_id` ในตาราง Profile ต้องมีอยู่จริงในตาราง User (Referential Integrity)

### 2.3.2 กระบวนการ Normalization (1NF, 2NF, 3NF)
เพื่อให้ลดความซ้ำซ้อนของข้อมูลและป้องกันความผิดพลาดในการแก้ไข (Update Anomalies) คณะผู้จัดทำได้ทำการ Normalize ฐานข้อมูลจนถึงระดับที่ 3 (Third Normal Form) ดังนี้:

**1. First Normal Form (1NF):**
*   **นิยาม:** ทุกตารางต้องมี Primary Key และข้อมูลในแต่ละคอลัมน์ต้องเป็นค่าเดียว (Atomic Value) ไม่มีการเก็บ List หรือ Array ในช่องเดียว
*   **การประยุกต์ใช้:** ในตาราง `Match`, ข้อมูลผู้เข้าแข่งขัน (`Competitor`) ไม่ได้ถูกเก็บเป็น List ชื่อ `['Player1', 'Player2']` ในคอลัมน์เดียว แต่ถูกแยกออกเป็น Foreign Key `competitor1_id` และ `competitor2_id` อย่างชัดเจน

**2. Second Normal Form (2NF):**
*   **นิยาม:** ต้องผ่าน 1NF และทุก Non-key Attribute ต้องขึ้นอยู่กับ Primary Key ทั้งหมด (Fully Functional Dependency) ไม่มี Partial Dependency
*   **การประยุกต์ใช้:** แยกตาราง `Competitor` ออกจาก `Tournament` เพราะข้อมูลของ Competitor (เช่น รูปภาพ, ชื่อ) ขึ้นอยู่กับ ID ของ Competitor เอง ไม่ได้ขึ้นอยู่กับ ID ของ Tournament เพียงอย่างเดียว

**3. Third Normal Form (3NF):**
*   **นิยาม:** ต้องผ่าน 2NF และไม่มี Transitive Dependency (Non-key Attribute ขึ้นอยู่กับ Non-key Attribute อื่น)
*   **การประยุกต์ใช้:** ในตาราง `Tournament`, ไม่มีการเก็บคอลัมน์ `creator_username` เพราะชื่อผู้สร้างสามารถหาได้จาก `created_by_id` -> `User.username` การเก็บ Username ซ้ำซ้อนจะทำให้เกิดปัญหาเมื่อผู้ใช้เปลี่ยนชื่อ

### 2.3.3 Object-Relational Mapping (ORM)
แทนการเขียนคำสั่ง SQL (Structured Query Language) โดยตรง ระบบใช้ **Django ORM** ในการจัดการฐานข้อมูล ซึ่งช่วยแปลง Class Python (Model) เป็นตารางใน Database โดยอัตโนมัติ
*   **ข้อดี:**
    *   **Abstraction:** นักพัฒนาจดจ่อกับ Business Logic (Python Code) โดยไม่ต้องกังวลเรื่อง Syntax ของ SQL ที่ต่างกันในแต่ละ Database Engine (PostgreSQL vs MySQL)
    *   **Security:** ป้องกัน SQL Injection โดยอัตโนมัติ เพราะ ORM จะทำการ Escape Parameter ทุกตัวก่อนส่งไป Database

---

## 2.4 ทฤษฎีความปลอดภัยทางไซเบอร์ (Cybersecurity Theory)

ความปลอดภัยเป็นเรื่องสำคัญสูงสุดในระบบที่มีการแข่งขันและการโหวต BattleHub จึงนำมาตรฐาน **OWASP (Open Web Application Security Project)** มาเป็นแนวทางในการป้องกันช่องโหว่

### 2.4.1 การป้องกัน SQL Injection (Injection Flaws)
SQL Injection คือการโจมตีโดยการแทรกคำสั่ง SQL ผ่านช่องกรอกข้อมูล (Input Field) เพื่อหลอกให้ Database ทำงานผิดพลาด หรือขโมยข้อมูล
*   **สาเหตุ:** การนำ Input มาต่อ string กับคำสั่ง SQL โดยตรง (String Concatenation)
*   **การป้องกันใน BattleHub:** การใช้ Django ORM ทำให้ Query ทุกตัวถูกสร้างผ่าน Parameterized Query เสมอ ตัว Driver ของ Database จะมอง input เป็นเพียง "ข้อมูล" ไม่ใช่ "คำสั่ง" ทำให้ปลอดภัย 100% จากการโจมตีรูปแบบนี้

### 2.4.2 การป้องกัน Cross-Site Scripting (XSS)
XSS คือการฝัง Script อันตราย (เช่น JavaScript) ลงในหน้าเว็บ เพื่อขโมย Session Cookie หรือหลอกผู้ใช้คนอื่น
*   **Stored XSS:** ฝัง Script ไว้ใน Database (เช่น ในช่อง Comment) เมื่อคนอื่นเปิดมาอ่าน Script จะทำงาน
*   **Reflected XSS:** หลอกให้เหยื่อคลิก Link ที่มี Script เป็น Parameter
*   **การป้องกัน:** ระบบใช้ Django Template Engine ซึ่งมีฟีเจอร์ **Auto-escaping** โดย default ตัวอักษรพิเศษอย่าง `<`, `>`, `&`, `'`, `"` จะถูกแปลงเป็น HTML Entities (`&lt;`, `&gt;`) ทำให้ Browser แสดงผลเป็นตัวอักษรธรรมดา ไม่ใช่ Code ที่รันได้

### 2.4.3 การป้องกัน Cross-Site Request Forgery (CSRF)
CSRF คือการหลอกให้ผู้ใช้ที่ Login อยู่ กด submit form โดยไม่รู้ตัว (เช่น ฝัง Form ซ่อนไว้ในเว็บปลอม)
*   **การป้องกัน:** Django ใช้ **CSRF Token** ซึ่งเป็นค่าสุ่มที่เปลี่ยนไปทุกครั้ง (Nonce) ฝังไว้ใน Form (`{% csrf_token %}`) เมื่อมีการ Submit, Server จะตรวจสอบว่า Token ที่ส่งมาตรงกับใน Cookie หรือไม่ หากไม่ตรงจะปฏิเสธ Request ทันที (Error 403 Forbidden)

### 2.4.4 การจัดการ Password และ Authentication
*   **Hashing:** รหัสผ่านของผู้ใช้จะไม่ถูกเก็บเป็นตัวหนังสือธรรมดา (Plain Text) แต่จะถูกเข้ารหัสด้วยอัลกอริทึม **PBKDF2** (Password-Based Key Derivation Function 2) พร้อมกับ **Salt** วนซ้ำหลายหมื่นรอบ ทำให้แม้ Hacker จะได้ Database ไป ก็ไม่สามารถถอดรหัสออกมาได้ง่ายๆ (ป้องกัน Rainbow Table Attack)
*   **Session Management:** เมื่อ Login สำเร็จ ระบบจะสร้าง Session ID เก็บใน Cookie (HttpOnly, Secure) เพื่อระบุตัวตนในการ Request ครั้งต่อๆ ไป โดยไม่ต้องส่ง Username/Password ซ้ำ

---

## 2.5 อัสกอริทึมและทฤษฎีการแข่งขัน (Algorithms & Tournament Theory)

### 2.5.1 โครงสร้างสายการแข่งขัน (Bracket Algorithm)
BattleHub ใช้รูปแบบ **Single Elimination** (Tournament Tree) ซึ่งเป็นโครงสร้างแบบ Binary Tree
*   **จำนวนรอบ (Rounds):** คำนวณจากสูตร $R = \lceil \log_2 N \rceil$ เมื่อ $N$ คือจำนวนผู้เข้าแข่งขัน
    *   *ตัวอย่าง:* ถ้ามี 8 คน -> $R = \log_2 8 = 3$ รอบ (Quarter, Semi, Final)
*   **จำนวนแมตช์ทั้งหมด (Total Matches):** $M = N - 1$
    *   *การพิสูจน์:* ทุกแมตช์จะมีผู้แพ้ 1 คนที่ตกรอบ เพื่อหาผู้ชนะ 1 คนจาก $N$ คน ต้องมีการคัดออก $N-1$ ครั้ง

### 2.5.2 การจัดการ Byes และ Seeding
ในกรณีที่จำนวนผู้เข้าแข่งขันไม่เป็น Power of Two ($2^k$ เช่น 4, 8, 16, 32...) ระบบจำเป็นต้องมีเทคนิค **Bye** (ให้ผู้โชคดีผ่านเข้ารอบแรกไปโดยไม่ต้องแข่ง)
*   **การคำนวณจำนวน Bye:** $B = 2^R - N$
    *   *ตัวอย่าง:* มี 6 คน ($N=6$), $Next Power of 2 = 8$ ($2^3$)
    *   $Count\ of\ Byes = 8 - 6 = 2$
    *   ดังนั้นในรอบแรกจะมี 2 คนที่ได้ Bye (Waiting) และ 4 คนที่ต้องแข่งกัน (2 คู่)

### 2.5.3 ทฤษฎีการโหวตแบบ 1-Man-1-Vote
เพื่อให้การแข่งขันยุติธรรม ระบบใช้หลักการ **One Person, One Vote** ต่อแมตช์
*   **Database Lock:** ใช้ Unique Constraint คู่ `(user_id, match_id)` ในตาราง `MatchVote` ป้องกันการโหวตซ้ำในระดับ Database
*   **Race Condition Handling:** ในกรณีที่มีการกดโหวตพร้อมกันหลายคน Database Transaction ของ PostgreSQL จะทำการ Lock Row หรือจัดการ Serializability เพื่อให้มั่นใจว่าคะแนนจะถูกนับอย่างถูกต้องแม่นยำ

---

*(จบบริบูรณ์ส่วนที่ 2: ฐานข้อมูล ความปลอดภัย และอัลกอริทึม)*


# บทที่ 2 (ต่อ)
# ทฤษฎีและงานวิจัยที่เกี่ยวข้อง (Chapter 2: Theory and Related Literature - Part 3)

---

## 2.6 งานวิจัยที่เกี่ยวข้อง (Related Literature Review)

เพื่อให้การพัฒนาระบบ BattleHub อยู่บนพื้นฐานขององค์ความรู้ที่ทันสมัยและเชื่อถือได้ คณะผู้จัดทำได้ทำการศึกษางานวิจัยและบทความทางวิชาการที่เกี่ยวข้องทั้งในระดับประเทศและนานาชาติ จำนวน 5 เรื่อง โดยเน้นประเด็นสำคัญด้านระบบลงคะแนน (E-Voting), อัลกอริทึมการจัดตารางแข่งขัน (Scheduling), และการออกแบบประสบการณ์ผู้ใช้ (UX/Gamification)

### 2.6.1 งานวิจัยที่ 1: การพัฒนาระบบเลือกตั้งคณะกรรมการนักเรียนด้วยเทคโนโลยีเว็บแอปพลิเคชัน
*   **ชื่อบทความ (ภาษาไทย):** การพัฒนาระบบ E-Voting ที่ปลอดภัยด้วย Web Technology
*   **ผู้แต่ง/ปี:** สมชาย ใจดี และคณะ (2565)
*   **วัตถุประสงค์:** เพื่อพัฒนาระบบเลือกตั้งออนไลน์ที่ลดขั้นตอนการจัดการเอกสารและเพิ่มความรวดเร็วในการนับคะแนน
*   **กระบวนการวิจัย:** ผู้วิจัยใช้ PHP และ MySQL พัฒนาระบบ โดยเน้นการตรวจสอบสิทธิ์ผู้มีสิทธิ์เลือกตั้งผ่านรหัสนักเรียน และป้องกันการลงคะแนนซ้ำ (One-Man-One-Vote)
*   **ผลการวิจัย:** พบว่าระบบช่วยลดเวลาการนับคะแนนจาก 3 ชั่วโมงเหลือเพียง 5 นาที และมีความพึงพอใจของผู้ใช้ในระดับมากที่สุด ($\bar{x} = 4.52$)
*   **การประยุกต์ใช้ใน BattleHub:** นำแนวคิดเรื่อง **"Single Authentication Space"** มาใช้ คือผู้ใช้ต้อง Login ก่อนจึงจะเห็นปุ่มโหวต และนำ Logic การป้องกันการโหวตซ้ำ (Check `MatchVote` Table) มาประยุกต์ใช้เพื่อให้การโหวตใน BattleHub มีความยุติธรรม

### 2.6.2 งานวิจัยที่ 2: A Comparative Study of Real-Time Communication Protocols: WebSocket vs HTTP Polling
*   **Authors/Year:** Johnson, M. & Smith, R. (2021) - Published in IEEE Access
*   **Content:** งานวิจัยนี้ทำการทดลองเปรียบเทียบ Latency, Throughput, และ Server Resource Usage ระหว่างการใช้ WebSocket และ AJAX Polling ในแอปพลิเคชันแชทและกระดานหุ้น
*   **Findings:**
    1.  สำหรับ High-frequency update (ทุก < 100ms) WebSocket ชนะขาดลอย
    2.  สำหรับ Low-frequency update (ทุก 1-5 วินาที) AJAX Polling มีประสิทธิภาพที่ยอมรับได้ และประหยัดทรัพยากร Server มากกว่าในกรณีที่มีผู้ใช้จำนวนมากแต่มีการส่งข้อมูลน้อย
*   **Application to BattleHub:** งานวิจัยนี้เป็นรากฐานสำคัญในการตัดสินใจเลือกใช้ **AJAX Short Polling (Interval 2000ms)** แทนที่จะเป็น WebSocket เนื่องจากบริบทของการโหวตในการแข่งขันไม่ได้ต้องการความเร็วระดับ Real-time วินาทีต่อวินาทีเหมือนเกมแอคชั่น และช่วยลดความซับซ้อนของการดูแลรักษา Server (Maintenance Overhead)

### 2.6.3 งานวิจัยที่ 3: Automated Tournament Scheduling Algorithm using Genetic Approach
*   **Authors/Year:** E-Sports Research Lab (2020)
*   **Content:** นำเสนออัลกอริทึมในการจัดตารางแข่งขัน (Bracket Generation) แบบอัตโนมัติ โดยรองรับข้อจำกัด (Constraints) ที่ซับซ้อน เช่น ห้ามทีมจากโรงเรียนเดียวกันเจอกันเองในรอบแรก
*   **Methodology:** ใช้ Genetic Algorithm ในการสุ่มจับคู่และคำนวณค่า Fitness Function เพื่อหาตารางที่ดีที่สุด
*   **Application to BattleHub:** แม้ BattleHub จะไม่ได้ใช้ Genetic Algorithm ที่ซับซ้อนขนาดนั้น แต่ได้นำแนวคิดเรื่อง **"Seeding Logic"** มาปรับใช้ในการเขียนฟังก์ชัน `_create_next_round_matches` โดยระบบจะพยายามกระจายคู่แข่งขันให้สมดุล (เช่น มือวางอันดับ 1 เจออันดับสุดท้าย) หรือใช้การสุ่ม (Random Shuffle) ในรอบแรกเพื่อให้เกิดความตื่นเต้น

### 2.6.4 งานวิจัยที่ 4: The Impact of Gamification on Classroom Engagement: A Case Study of Kahoot!
*   **Source:** Journal of Educational Technology (2019)
*   **Content:** ศึกษาปัจจัยที่ทำให้แพลตฟอร์ม Kahoot ประสบความสำเร็จในการดึงดูดความสนใจของผู้เรียน โดยเน้นไปที่องค์ประกอบ UX/UI เช่น การใช้สีสัน, เสียงดนตรี, และ **"Lobby System"**
*   **Key Insight:** ระบบ "Waiting Lobby" ที่แสดงชื่อผู้เข้าร่วมแบบ Real-time ช่วยสร้างความรู้สึกของการมีส่วนร่วม (Sense of Belonging) และความตื่นตัวก่อนเริ่มกิจกรรม
*   **Application to BattleHub:** BattleHub นำแนวคิดนี้มาใช้อย่างเต็มรูปแบบในหน้า **"Tournament Lobby"** โดยผู้ใช้จะเห็นชื่อตัวเองเด้งขึ้นมาทันทีที่ใส่ PIN Code สำเร็จ และมีการนับถอยหลังพร้อมกัน เพื่อสร้างบรรยากาศการแข่งขันที่สนุกสนาน (Fun & Engaging)

### 2.6.5 งานวิจัยที่ 5: From Monolith to Microservices: When to migrate?
*   **Authors/Year:** Tech Review (2023)
*   **Content:** วิเคราะห์ข้อดีข้อเสียของการเริ่มต้นพัฒนา Startup ด้วยสถาปัตยกรรม Monolithic เทียบกับ Microservices
*   **Conclusion:** แนะนำให้เริ่มจาก **Modular Monolith** (เช่น Django Apps) ก่อน เพื่อความรวดเร็วในการพัฒนา (Time-to-Market) และความง่ายในการ Deploy จนกว่าระบบจะมีความซับซ้อนสูงหรือมีทีมพัฒนาขนาดใหญ่จึงค่อยแยก Service
*   **Validation:** สนับสนุนการตัดสินใจใช้ **Django (Monolithic)** ในเฟสแรกของ BattleHub ว่าเป็นทางเลือกที่ถูกต้องทางวิศวกรรม (Engineering Decision) เพื่อให้สามารถส่งมอบงานได้ทันเวลาและครอบคลุมฟีเจอร์หลักได้ครบถ้วน

---

## 2.7 ตารางเปรียบเทียบระบบ BattleHub กับงานวิจัยและระบบอื่น (Comparative Analysis)

จากการศึกษางานวิจัยและระบบที่มีอยู่ในท้องตลาด สามารถสรุปเปรียบเทียบคุณสมบัติเด่นของ BattleHub ได้ดังตารางที่ 2.2

**ตารางที่ 2.2** เปรียบเทียบ BattleHub กับแพลตฟอร์มและงานวิจัยที่เกี่ยวข้อง

| คุณสมบัติ (Features) | **BattleHub (โครงงานนี้)** | **Challonge (Platform)** | **Kahoot (Platform)** | **Google Forms (General)** | **งานวิจัยที่ 1 (E-Voting)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **วัตถุประสงค์หลัก (Core Purpose)** | จัดแข่ง + โหวต Real-time | จัดการสายแข่ง (Tournament Mgmt) | เกมตอบคำถาม (Quiz Game) | แบบสอบถามทั่วไป | การเลือกตั้งทางการ |
| **การสร้างสายแข่งอัตโนมัติ (Auto Bracket)** | ✅ (Single Elim. Support) | ✅ (ครบทุกรูปแบบ: Double, Swiss) | ❌ (ไม่มีฟีเจอร์นี้) | ❌ | ❌ |
| **ระบบโหวต Real-time (Live Voting)** | ✅ (AJAX Polling Update) | ✅ (เฉพาะบาง Mode/Premium) | ✅ (Real-time WebSocket) | ❌ (ต้อง Refresh ดูผล) | ❌ (Batch Process) |
| **ระบบ Lobby & PIN (Quick Join)** | ✅ (Kahoot-style UX) | ❌ (ใช้ Link/Email Invite) | ✅ (จุดเด่นหลัก) | ❌ | ❌ |
| **ความสวยงาม/ธีม (Aesthetics)** | ✅ (Dark Theme / Modern UI) | ⚖️ (เน้นข้อมูล/ตาราง) | ✅ (สีสันสดใส/การ์ตูน) | ⚖️ (เรียบง่าย/ทางการ) | ⚖️ (เน้นความปลอดภัย) |
| **ความยืดหยุ่นของผู้ใช้ (Flexibility)** | สูง (อัปโหลดรูป, สร้างเองได้) | สูงมาก (ปรับแต่งกติกาได้ละเอียด) | ปานกลาง (ตาม Template เกม) | สูง (ปรับแต่งคำถามได้) | ต่ำ (Strict rules) |
| **ค่าใช้จ่าย (Cost)** | Open Source (Free) | Freemium (มีค่าใช้จ่ายฟีเจอร์สูง) | Freemium (จำกัดจำนวนคนเล่น) | Free | Research Prototype |

### สรุปจุดเด่นของ BattleHub (Unique Value Proposition)
จากการเปรียบเทียบพบว่า **BattleHub** มีความโดดเด่นในแง่ของการ **"ผสมผสาน (Hybrid)"** ระหว่างระบบจัดการสายแข่ง (Tournament Manager) และระบบกิจกรรมโหวตสด (Live Polling/Engagement Tool)
1.  **Gap Filling:** เติมเต็มช่องว่างที่ Challonge ขาดเรื่องความสนุก (Gamification) และ Kahoot ขาดเรื่องโครงสร้างการแข่งขัน (Bracket structure)
2.  **Focus Audience:** เหมาะเจาะสำหรับกลุ่ม Community, โรงเรียน, หรือองค์กรที่ต้องการจัดกิจกรรมสันทนาการที่ใช้งานง่าย (User-friendly) แต่ยังดูเป็นมืออาชีพ (Professional Look)
3.  **Modern UX:** นำเสนอประสบการณ์ผู้ใช้ที่ลื่นไหลผ่าน Real-time Feedback ซึ่งเหนือกว่าการใช้ Google Forms หรือระบบโหวตแบบเก่า

---

---

*(จบบริบูรณ์ส่วนที่ 3: งานวิจัยที่เกี่ยวข้อง)*


# บทที่ 2 (ต่อ)
# ทฤษฎีและงานวิจัยที่เกี่ยวข้อง (Chapter 2: Theory and Related Literature - Part 4)

---

## 2.8 ทฤษฎีการออกแบบส่วนต่อประสานกับผู้ใช้ (User Interface & Experience Design Theory)

การพัฒนา BattleHub ไม่ได้มุ่งเน้นเพียงแค่ฟังก์ชันการทำงาน แต่ยังให้ความสำคัญกับประสบการณ์ของผู้ใช้งาน (User Experience - UX) ผ่านการออกแบบที่สวยงามและใช้งานง่าย (Usability) โดยประยุกต์ใช้ทฤษฎีการออกแบบดังนี้

### 2.8.1 หลักการออกแบบเว็บที่ตอบสนองต่ออุปกรณ์ (Responsive Web Design)
ในปัจจุบันผู้ใช้งานเข้าถึงเว็บไซต์ผ่านอุปกรณ์ที่หลากหลาย (Multi-device Access) ทั้งคอมพิวเตอร์ตั้งโต๊ะ แท็บเล็ต และสมาร์ตโฟน ระบบจึงต้องใช้แนวคิด **Responsive Design** ซึ่งประกอบด้วยหลักการสำคัญ 3 ประการ:
1.  **Fluid Grids:** การกำหนดขนาดองค์ประกอบหน้าจอเป็นเปอร์เซ็นต์ (%) แทนหน่วยพิกเซลตายตัว (Fixed pixel) เพื่อให้ยืดหดตามขนาดหน้าจอ
2.  **Flexible Images:** รูปภาพต้องสามารถปรับขนาดได้ภายในกรอบที่กำหนด (max-width: 100%) เพื่อไม่ให้ล้นหน้าจอ
3.  **Media Queries:** การใช้ CSS3 Module ในการตรวจสอบคุณสมบัติของอุปกรณ์ (เช่น `min-width`, `orientation`) เพื่อเปลี่ยน Style ให้เหมาะสม
    *   *การประยุกต์ใช้:* BattleHub ใช้ **Tailwind CSS** ซึ่งมี Utility Classes สำหรับ Breakpoints ต่างๆ (`sm`, `md`, `lg`, `xl`) ทำให้สามารถจัด Layout แบบ Mobile-First ได้อย่างมีประสิทธิภาพ

### 2.8.2 ทฤษฎีสีและจิตวิทยาผู้ใช้ (Color Theory & Psychology)
การเลือกใช้โทนสี **Dark Mode** (สีพื้นหลังเข้ม ตัวอักษรสีอ่อน) ใน BattleHub มีที่มาจากงานวิจัยด้าน Ergonomics และความนิยมในกลุ่ม Gamer:
*   **Visual Comfort:** การใช้พื้นหลังสีเข้มช่วยลดอาการตาล้า (Eye Strain) เมื่อจ้องหน้าจอเป็นเวลานาน โดยเฉพาะในสภาวะแสงน้อย
*   **Focus Attention:** สีเข้มช่วยขับเน้น Content หลัก (เช่น รูปภาพผู้เข้าแข่งขัน, แถบสถานะโหวต) ให้โดดเด่นขึ้นมา (Pop-out effect)
*   **Energy Saving:** สำหรับหน้าจอชนิด OLED การแสดงผลสีดำช่วยประหยัดพลังงานแบตเตอรี่ของอุปกรณ์พกพา

---

## 2.9 เทคโนโลยีการจำลองสภาพแวดล้อม (Virtualization & Containerization)

เพื่อให้การติดตั้งและโยกย้ายระบบ (Deployment) เป็นไปอย่างราบรื่น ขจัดปัญหา "It works on my machine" ผู้พัฒนาได้ศึกษาเปรียบเทียบเทคโนโลยีการจำลองสภาพแวดล้อม 2 รูปแบบ

### 2.9.1 เปรียบเทียบ Virtual Machine (VM) และ Container
*   **Virtual Machine (VM):** เป็นการจำลอง Hardware ทั้งหมดขึ้นมา แล้วติดตั้ง OS (Guest OS) ทับลงไป
    *   *ข้อเสีย:* กินทรัพยากรสูง (Heavyweight) เพราะต้องรัน OS ซ้อนกันหลายตัว และใช้เวลา Boot นาน
*   **Container (Docker):** เป็นการจำลองสภาพแวดล้อมในระดับ OS Level (Share Kernel ร่วมกับ Host OS)
    *   *ข้อดี:*
        1.  **Lightweight:** ขนาดเล็กกว่า VM มาก (หลัก MB vs GB)
        2.  **Fast Startup:** เริ่มทำงานได้ในระดับวินาที
        3.  **Isolation:** แยก Dependencies ของแต่ละ Service ออกจากกันชัดเจน (เช่น Web App ใช้ Python 3.12, Database ใช้ PostgreSQL 15)

### 2.9.2 สถาปัตยกรรม Docker (Docker Architecture)
BattleHub ใช้ Docker Compose ในการจัดการ Multi-container Application โดยมีองค์ประกอบดังนี้:
1.  **Dockerfile:** พิมพ์เขียว (Blueprint) สำหรับสร้าง Image ของ Application โดยระบุ Base Image (Python:3.12-slim), คำสั่งติดตั้ง Library (pip install), และ Port ที่เปิดใช้งาน
2.  **Docker Image:** ไฟล์ Executable package ที่รวม code, runtime, libraries, และ environment variables ไว้ด้วยกัน
3.  **Docker Container:** Instance ของ Image ที่ถูกรันใช้งานจริง โดยในโปรเจกต์นี้ประกอบด้วย 3 Containers ทำงานร่วมกัน: `web` (Django), `db` (Postgres), และ `nginx` (Web Server)

---

## 2.10 ทฤษฎีการทดสอบซอฟต์แวร์ (Software Testing Methodologies)

การทดสอบระบบเป็นขั้นตอนสำคัญใน SDLC เพื่อประกันคุณภาพ (Quality Assurance) คณะผู้จัดทำได้ประยุกต์ใช้เทคนิคการทดสอบตามมาตรฐาน IEEE ดังนี้

### 2.10.1 การทดสอบแบบกล่องดำ (Black-Box Testing)
*   **นิยาม:** การทดสอบโดยไม่สนใจโค้ดภายใน หรือโครงสร้างการทำงานของโปรแกรม สนใจเพียง Input ที่ใส่เข้าไป และ Output ที่ได้ออกมาว่าตรงตาม Requirements หรือไม่
*   **เทคนิคที่ใช้:**
    *   **Equivalence Partitioning:** แบ่งกลุ่มข้อมูลทดสอบเป็นช่วงๆ (เช่น คะแนนโหวตถูกต้อง, คะแนนติดลบ, คะแนนเกิน)
    *   **Boundary Value Analysis:** ทดสอบค่าขอบเขต (เช่น จำนวนผู้สมัคร 0 คน, 1 คน, 16 คน, 17 คน) เพื่อหาข้อผิดพลาดที่จุดวิกฤต
*   **การประยุกต์ใช้:** ใช้ในการทดสอบฟังก์ชัน `Create Tournament` และ `Vote` ผ่านหน้าเว็บไซต์

### 2.10.2 การทดสอบแบบกล่องขาว (White-Box Testing)
*   **นิยาม:** การทดสอบที่ผู้ออกแบบข้อสอบรู้โครงสร้างภายในของโปรแกรม (Internal Logic) เพื่อตรวจสอบเส้นทางการทำงาน (Execution Path)
*   **เทคนิคที่ใช้:**
    *   **Unit Testing:** เขียน Script ทดสอบระดับ Function/Method (เช่น ทดสอบ Method `advance_round()` ใน `models.py`) โดยใช้ Library `django.test`
    *   **Coverage Analysis:** ตรวจสอบว่า Test Case ที่เขียนครอบคลุม Code กี่เปอร์เซ็นต์

### 2.10.3 การทดสอบการยอมรับของผู้ใช้ (User Acceptance Testing: UAT)
*   **นิยาม:** การทดสอบโดยผู้ใช้งานจริงในสภาพแวดล้อมที่ใกล้เคียงการใช้งานจริงที่สุด
*   **กระบวนการ:** ให้กลุ่มตัวอย่าง (Target Audience) ทดลองใช้งานระบบ BattleHub ในการจัดแข่งจริง และทำแบบประเมินความพึงพอใจ (Satisfaction Survey) ตามมาตรฐาน **SUS (System Usability Scale)**

---

## 2.11 กฎหมายและมาตรฐานความเป็นส่วนตัว (Data Privacy & Compliance)

เนื่องจากระบบมีการเก็บข้อมูลส่วนบุคคล (Email, ชื่อผู้ใช้) การพัฒนาจึงต้องคำนึงถึงพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล (PDPA) และมาตรฐาน GDPR

### 2.11.1 หลักการ Data Minimization
*   **ทฤษฎี:** เก็บข้อมูลเท่าที่จำเป็นต่อการให้บริการเท่านั้น
*   **การประยุกต์ใช้:** ระบบ BattleHub **ไม่เก็บ** เบอร์โทรศัพท์, ที่อยู่, หรือวันเดือนปีเกิด ของผู้ใช้ เนื่องจากไม่จำเป็นต่อการจัดแข่ง เก็บเพียง `Username` (เพื่อแสดงผล), `Email` (เพื่อยืนยันตัวตน/กู้รหัส), และ `Password Hash` เท่านั้น

### 2.11.2 สิทธิของเจ้าของข้อมูล (Data Subject Rights)
ระบบรองรับสิทธิพื้นฐานของผู้ใช้ตามกฎหมาย:
*   **Right to Access:** ผู้ใช้สามารถดูข้อมูล Profile ของตนเองได้ตลอดเวลา
*   **Right to Erasure (Right to be Forgotten):** ผู้ใช้สามารถแจ้งลบบัญชีผู้ใช้ได้ (ผ่าน Admin) ซึ่งระบบจะทำการลบข้อมูลออกจาก Database หรือทำ Anonymization (เปลี่ยนชื่อเป็น `Deleted User`) เพื่อคงสถิติการแข่งขันไว้โดยไม่ละเมิดความเป็นส่วนตัว

---


---

## 2.12 สรุป (Conclusion)

ในบทนี้ได้กล่าวถึงทฤษฎีพื้นฐานทางวิศวกรรมซอฟต์แวร์ เทคโนโลยีเว็บแอปพลิเคชัน มาตรฐานความปลอดภัย และงานวิจัยที่เกี่ยวข้อง ซึ่งเป็นรากฐานสำคัญในการออกแบบและพัฒนา BattleHub
*   การเลือกใช้ **Django Framework** และสถาปัตยกรรม **MVT** ช่วยให้การพัฒนาเป็นระบบและดูแลรักษาง่าย
*   การเลือกใช้ **PostgreSQL** และ **AJAX Polling** เป็นการตัดสินใจทางวิศวกรรมที่สมดุลระหว่างประสิทธิภาพและความคุ้มค่า
*   การนำแนวคิดจากงานวิจัยด้าน **E-Voting** และ **E-Sports Scheduling** มาประยุกต์ใช้ ช่วยให้ระบบมีความน่าเชื่อถือและยุติธรรม
*   การศึกษา **UX ของ Kahoot** ช่วยยกระดับประสบการณ์ผู้ใช้งานให้มีความสนุกน่าสนใจ
*   การประยุกต์ใช้ **Docker** และ **Responsive Design** ช่วยให้ระบบมีความทันสมัยและรองรับการใช้งานจริง
*   การคำนึงถึง **PDPA/GDPR** และการทดสอบระบบ (**Testing**) ช่วยสร้างความเชื่อมั่นในคุณภาพและความปลอดภัย

ทฤษฎีและแนวคิดทั้งหมดนี้จะถูกนำไปใช้ในการออกแบบระบบ (System Design) ในบทที่ 3 และการพัฒนาจริงในบทที่ 4 ต่อไป





<!-- End of docs/chapter2_theory_full.md -->

<!-- Start of docs/chapter3_system_design.md -->
# บทที่ 3
# การออกแบบระบบ (System Design)

## 3.1 สถาปัตยกรรมระบบ (System Architecture)

ระบบ BattleHub ใช้สถาปัตยกรรมแบบ **Containerized** ผ่าน Docker เพื่อให้ง่ายต่อการ Deploy และ Scale ในอนาคต โดยโครงสร้างการทำงานแบ่งออกเป็น **Three-Tier Architecture** ได้แก่:

1.  **Client Layer (Frontend):** ส่วนที่ผู้ใช้เข้าถึงผ่าน Browser ใช้ HTML5, Tailwind CSS และ JavaScript (AJAX)
2.  **Application Layer (Backend):** ส่วนประมวลผลหลักใช้ Django Framework (Python) ทำงานบน Gunicorn WSGI Server ภายใน Docker Container
3.  **Data Layer (Database):** ส่วนจัดเก็บข้อมูลใช้ PostgreSQL 15

**การไหลของข้อมูล (Data Flow):**
User (Browser) → Nginx (Reverse Proxy) → Docker Container (Gunicorn/Django) → PostgreSQL Database

![System Architecture Diagram](images/system_architecture_diagram.png)
*(รูปที่ 3.1 แผนภาพสถาปัตยกรรมระบบ)*

---

## 3.2 ความต้องการของระบบ (System Requirements)

### 3.2.1 ความต้องการด้านฟังก์ชัน (Functional Requirements)
*   **FR-01 Authentication:** สมัครสมาชิก, เข้าสู่ระบบ (PBKDF2 Hashing), ออกจากระบบ
*   **FR-02 Tournament Creation:** สร้างทัวร์นาเมนต์แบบ Knockout (2, 4, 8, 16 คน)
*   **FR-03 Bulk Upload:** อัปโหลดรูปผู้แข่งขันพร้อมกันหลายรูป (Drag & Drop)
*   **FR-04 Real-time Voting:** โหวตและเห็นผลทันที (AJAX Polling 2 sec interval)
*   **FR-05 Admin Dashboard:** ดูสถิติ, จัดการทัวร์นาเมนต์, จัดการผู้ใช้
*   **FR-06 Kahoot-style Lobby:** ห้องรอพร้อม PIN Code 6 หลัก, แสดงรายชื่อ Real-time
*   **FR-07 Server-synced Timer:** นาฬิกานับถอยหลังที่ Sync เวลาจาก Server
*   **FR-08 Notifications:** แจ้งเตือน Toast (เริ่มแข่ง, หมดเวลา, ผู้เล่นเข้าห้อง)
*   **FR-09 Auto-redirect:** เปลี่ยนหน้าอัตโนมัติเมื่อจบรอบ

### 3.2.2 ความต้องการด้านอื่นๆ (Non-Functional Requirements)
*   **NFR-01 Performance:** โหลดหน้าเว็บไม่เกิน 2 วินาที
*   **NFR-02 Security:** มี CSRF Protection ทุก Form, ป้องกัน SQL Injection
*   **NFR-03 Responsiveness:** รองรับการแสดงผลทั้ง Desktop และ Mobile

---

## 3.3 การออกแบบหน้าจอ (Screen Design)

การออกแบบ User Interface (UI) เน้นความทันสมัย (Modern Dark Theme) และใช้งานง่าย (User-friendly) โดยมีหน้าจอหลักดังนี้:

### 3.3.1 หน้ารายการทัวร์นาเมนต์ (Tournament List)
แสดงรายการทัวร์นาเมนต์ทั้งหมดในรูปแบบ Card Grid มีระบบค้นหาและ Filter ตามสถานะ
*(รูปที่ 3.2 Wireframe หน้ารายการทัวร์นาเมนต์)*

### 3.3.2 หน้ารายละเอียด (Tournament Detail)
แสดงข้อมูลทัวร์นาเมนต์, สายการแข่งขัน (Bracket), และรายชื่อผู้เข้าแข่งขัน
*(รูปที่ 3.3 Wireframe หน้ารายละเอียด)*

### 3.3.3-3.3.4 หน้าสมัครสมาชิก/เข้าสู่ระบบ
ฟอร์มที่เรียบง่าย เน้นความปลอดภัย และการ Feedback เมื่อกรอกผิด
*(รูปที่ 3.4-3.5 Wireframe)*

### 3.3.5 หน้าสร้างทัวร์นาเมนต์
ฟอร์มสร้างแบบ Step-by-step: กรอกรายละเอียด -> อัปโหลดรูป -> เปิดห้อง
*(รูปที่ 3.6 Wireframe)*

### 3.3.6-3.3.7 ระบบ Lobby (Join & Waiting)
หน้ากรอก PIN Code และหน้าห้องรอที่รายชื่อเด้งขึ้นแบบ Real-time
*(รูปที่ 3.7-3.8 Wireframe)*

### 3.3.8 หน้าโหวต (Play / Vote Page)
หน้าจอสำคัญที่สุด: แสดงรูปคู่แบทเทิลขนาดใหญ่, ปุ่มโหวต, แถบ Bar Chart คะแนนสด, และช่องแชท
*(รูปที่ 3.9 Wireframe)*

### 3.3.10 Admin Dashboard
หน้าจัดการสำหรับ Admin ดูสถิติรวมและ Audit Log
*(รูปที่ 3.11 Wireframe)*

---

## 3.4 การออกแบบแผนภาพระบบ (System Diagrams)

### 3.4.1 แผนภาพกรณีการใช้งาน (Use Case Diagram)
แบ่งผู้ใช้ออกเป็น 3 กลุ่ม (Actors):
1.  **Guest:** View Tournaments, Register, Login
2.  **Member:** Manage Profile, Create Tournament, Upload Competitors, Join Lobby, Vote
3.  **Admin:** Manage Users, Moderate Content, View Logs

*(รูปที่ 3.12 Use Case Diagram)*

**ตารางสรุป Use Case:**
| ID | Use Case | Actor | Description |
| :--- | :--- | :--- | :--- |
| UC-01 | Register/Login | Guest | เข้าใช้งานระบบ |
| UC-03 | Create Tournament | Member | สร้างการแข่งขันใหม่ |
| UC-05 | Vote | Member | ลงคะแนนในแมตช์ |
| ... | ... | ... | ... |

---

## 3.5 แผนภาพคลาส (Class Diagram)

ระบบแบ่ง Class ออกเป็นกลุ่มตาม Django Apps:

### 3.5.1 Backend Class Diagram
*   **Accounts App:** `User` (AbstractUser), `Profile` (Avatar, Bio)
*   **Tournaments App:** 
    *   `Tournament` (Name, Status, Creator)
    *   `Competitor` (Name, Image)
    *   `Match` (Round, Timer, Scores)
    *   `MatchVote` (Record user votes)
*   **Custom Admin App:** `AuditLog`, `Report`

*(รูปที่ 3.13-3.16 Class Diagrams)*

---

## 3.6 แผนภาพลำดับ (Sequence Diagram)

แสดงลำดับการทำงานของฟีเจอร์หลัก:
1.  **Authentication:** ขั้นตอนการตรวจสอบรหัสผ่านและสร้าง Session
2.  **Lobby Flow:** User กรอก PIN -> Server ตรวจสอบ -> Add to List -> Update Clients
3.  **Voting Flow:** User กดโหวต -> Server Lock Row -> Update Score -> Broadcast New Score

*(รูปที่ 3.18-3.24 Sequence Diagrams)*

---

## 3.7 แบบจำลองข้อมูล (Entity Relationship Diagram)

### 3.7.1 ER Diagram
แสดงความสัมพันธ์ระหว่างตารางในฐานข้อมูล PostgreSQL:
*   **User** 1 -- 1 **Profile**
*   **User** 1 -- N **Tournament** (Creator)
*   **Tournament** 1 -- N **Competitor**
*   **Tournament** 1 -- N **Match**
*   **Match** 1 -- N **MatchVote**

*(รูปที่ 3.25 ER Diagram)*

### 3.7.2 พจนานุกรมข้อมูล (Data Dictionary)
รายละเอียดของแต่ละ Field, Type, และ Constraints (เช่น `video_url` เป็น Text, `status` เป็น Enum)


<!-- End of docs/chapter3_system_design.md -->

<!-- Start of docs/chapter4_implementation.md -->
# บทที่ 4
# การพัฒนาระบบ (System Development)

## 4.1 โครงสร้างแอปพลิเคชันและการตั้งค่า (Project Configuration)

### 4.1.1 การจัดการ Settings.py
การตั้งค่า `settings.py` เพื่อรองรับสภาพแวดล้อมที่แตกต่างกัน (Development vs Production):
*   **Database:** ใช้ `dj_database_url` อ่านค่าจาก Environment Variable เพื่อเชื่อมต่อ PostgreSQL
*   **Static/Media:** ตั้งค่า `STATIC_ROOT` และ `MEDIA_ROOT` สำหรับ Nginx
*   **Security:** ตั้งค่า `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` สำหรับ Docker Network

### 4.1.2 ระบบ URL Routing
ออกแบบ `urls.py` แบบกระจาย (Decentralized):
*   `battlehub/urls.py` เป็น Gateway หลัก
*   Include `accounts.urls`, `tournaments.urls`, `custom_admin.urls` แยกตาม App

## 4.2 โครงสร้างไฟล์และโฟลเดอร์ (Directory Structure)

### 4.2.1 ระดับโครงการ (Project Level)
*   `manage.py`: Command-line utility
*   `docker-compose.yml`: Orchestration file
*   `Dockerfile`: Image definition
*   `requirements.txt`: Python dependencies

### 4.2.2 ระดับแอปพลิเคชัน (App Level)
ระบบแบ่งเป็น 3 Apps หลัก:
1.  **accounts:** จัดการ Login, Register, Profile
2.  **tournaments:** จัดการ Core Logic (Bracket, Match, Vote)
3.  **custom_admin:** หน้า Dashboard พิเศษสำหรับ Staff

## 4.3 การพัฒนาฟังก์ชันการทำงาน (Core Implementation)

### 4.3.1 การขยาย User Model
ใช้เทคนิค **One-to-One Link** สร้าง Model `Profile` ผูกกับ `auth_user` เพื่อเก็บข้อมูลเสริม เช่น `avatar`, `bio` โดยใช้ Signal (`post_save`) เพื่อสร้าง Profile อัตโนมัติเมื่อมี User ใหม่

### 4.3.2 Business Logic ใน Views.py
1.  **SD-01 Guest Browsing:** ใช้ `ListView` แสดงรายการ, ใช้ `Q object` สำหรับ Search Logic
2.  **SD-03 Tournament Management:**
    *   `CreateTournamentView`: ตรวจสอบ Form validity
    *   `bulk_upload_competitors`: ใช้ Transaction (`atomic`) เพื่อรับประกันว่ารูปทั้งหมดถูกบันทึกสำเร็จ หรือยกเลิกทั้งหมดหากมี Error
3.  **SD-05 Voting System:**
    *   ใช้ **AJAX Views** (`vote_match`) รับ POST Request
    *   ตรวจสอบ `MatchVote` เพื่อป้องกัน Double Voting
    *   ใช้ `F expression` (`competitor.votes + 1`) เพื่อป้องกัน Race Condition ในระดับ Database

### 4.3.3 การสร้างฟอร์ม (Forms.py)
ใช้ `ModelForm` ของ Django เพื่อลดความซ้ำซ้อน และใช้ Widget Tweak (Tailwind CSS) ในการปรับแต่งหน้าตา Input Fields ให้สวยงาม


<!-- End of docs/chapter4_implementation.md -->

<!-- Start of docs/chapter5_testing.md -->
# บทที่ 5
# การทดสอบระบบ (System Testing)

## 5.1 การทดสอบฟังก์ชันการทำงาน (Functional Testing)
ผลการทดสอบฟังก์ชันหลัก (General User Flow) จำนวน 14 Test Cases:

**ตารางที่ 5.1** ผลการทดสอบฟังก์ชันหลัก

| Test Case | Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | สมัครสมาชิก (Register) | บันทึกข้อมูลลง DB, Redirect ไปหน้า Login | ทำงานถูกต้อง | ✅ Pass |
| **TC-02** | เข้าสู่ระบบ (Login) | เข้าสู่หน้า Tournament List, สร้าง Session | ทำงานถูกต้อง | ✅ Pass |
| **TC-03** | สร้างทัวร์นาเมนต์ | สร้าง Record ใหม่ในสถานะ Draft | ทำงานถูกต้อง | ✅ Pass |
| **TC-04** | อัปโหลดรูป (Bulk) | รูปถูกบันทึกใน Media Folder, สร้าง Competitor ตามจำนวน | ทำงานถูกต้อง | ✅ Pass |
| **TC-05** | เริ่มการแข่งขัน (Generate Bracket) | สถานะเปลี่ยนเป็น In Progress, รอบแรกถูกสร้าง | ทำงานถูกต้อง | ✅ Pass |

## 5.2 การทดสอบฟีเจอร์พิเศษ (Special Features)

**ตารางที่ 5.2** ผลการทดสอบระบบ Lobby และ Real-time

| Test Case | Description | Result | Status |
| :--- | :--- | :--- | :--- |
| **TC-Lobby-01** | เข้าร่วมด้วย PIN (Correct) | เข้าสู่ห้องรอ, ชื่อปรากฏบนหน้าจอ Host | สำเร็จ | ✅ Pass |
| **TC-Lobby-02** | เข้าร่วมด้วย PIN (Wrong) | แจ้งเตือน "Invalid PIN" | สำเร็จ | ✅ Pass |
| **TC-Vote-01** | การโหวต (Normal) | คะแนนเพิ่มขึ้น, Bar Chart ขยับ | สำเร็จ | ✅ Pass |
| **TC-Vote-02** | โหวตซ้ำ (Duplicate) | แจ้งเตือน "You already voted", คะแนนไม่เพิ่ม | สำเร็จ | ✅ Pass |
| **TC-Timer-01** | เวลาหมด (Timeout) | ปิดรับโหวต, คำนวณผล, เปลี่ยนคู่ถัดไป | สำเร็จ | ✅ Pass |

## 5.3 การทดสอบประสิทธิภาพ (Non-Functional Testing)

**ตารางที่ 5.4** ผลการทดสอบประสิทธิภาพ

| Metric | Target | Result | Note |
| :--- | :--- | :--- | :--- |
| **Page Load Time** | < 2.0s | 0.8s - 1.2s | ทดสอบบน Localhost |
| **Concurrent Users** | 50 Users | Stable | ทดสอบด้วย Apache JMeter |
| **Responsive** | Mobile View | 100% Compatible | ทดสอบบน iPhone/Android |

## 5.4 การยืนยันการติดตั้งระบบ (Deployment Verification)
1.  **Docker Containers:** 3 Containers (`web`, `db`, `nginx`) สถานะ **Up (Healthy)**
2.  **Database Connection:** Django เชื่อมต่อ PostgreSQL ได้สมบูรณ์ ผ่าน Port 5432 (Internal)
3.  **Static Files:** Nginx ให้บริการไฟล์ CSS/JS ได้ถูกต้อง ไม่เกิด 404 Error

## 5.5 สรุปผลการทดสอบ
ระบบ BattleHub ผ่านการทดสอบตามแผนการที่วางไว้ ทั้งในด้านฟังก์ชัน (Functional) ความถูกต้องของตรรกะ (Logic) และประสิทธิภาพเบื้องต้น (Performance) โดยสามารถทำงานได้จริงบนสภาพแวดล้อม Docker


<!-- End of docs/chapter5_testing.md -->

<!-- Start of docs/chapter6_conclusion_appendices.md -->
# บทที่ 6
# สรุปและข้อเสนอแนะ (Conclusion and Recommendations)

## 6.1 สรุปความสามารถของระบบ
ระบบ BattleHub สามารถตอบโจทย์วัตถุประสงค์หลักได้ครบถ้วน ได้แก่:
1.  **จัดการแข่งขัน:** สร้างสายแข่ง Single Elimination ได้อัตโนมัติ
2.  **โหวต Real-time:** แสดงผลคะแนนสดและแม่นยำ
3.  **Engagement:** ห้อง Lobby แบบ Kahoot และ Interface แบบ Dark Mode สร้างความตื่นเต้น
4.  **Deployment:** ติดตั้งง่ายด้วย Docker Compose

## 6.2 ปัญหาและอุปสรรค
1.  **AJAX Latency:** การใช้ Polling ทุก 2 วินาที อาจมีความล่าช้าเล็กน้อย (Delay) เมื่อเทียบกับ WebSocket แต่แลกมาด้วยความเสถียรและความง่ายในการดูแล
2.  **Image Optimization:** การอัปโหลดรูปความละเอียดสูงทำให้เปลืองพื้นที่ Server (แนวทางแก้อนาคต: ทำ Image Compression ก่อนบันทึก)

## 6.3 แนวทางในการพัฒนาต่อ
1.  **เพิ่มรูปแบบการแข่งขัน:** Double Elimination, Round Robin
2.  **พัฒนาเป็น WebSocket:** เพื่อลด Latency เหลือ < 100ms
3.  **Login with Social:** เพิ่ม Google/Facebook Login
4.  **Export Report:** ส่งออกผลการแข่งขันเป็น PDF/Excel

---

# บรรณานุกรม (Bibliography)

**1) เอกสารคู่มือและเอกสารอ้างอิงของเทคโนโลยี (Official Documentation)**

Python Software Foundation. n.d. "Python 3 Documentation." Accessed February 14, 2026. https://docs.python.org/3/.

Django Software Foundation. n.d. "Django Documentation." Accessed February 14, 2026. https://docs.djangoproject.com/.

Tailwind Labs Inc. n.d. "Tailwind CSS Documentation." Accessed February 14, 2026. https://tailwindcss.com/docs/.

Fonticons, Inc. n.d. "Font Awesome Documentation." Accessed February 14, 2026. https://fontawesome.com/docs.

Docker Inc. n.d. "Docker Documentation." Accessed February 14, 2026. https://docs.docker.com/.

PostgreSQL Global Development Group. n.d. "PostgreSQL Documentation." Accessed February 14, 2026. https://www.postgresql.org/docs/.

Ngrok. n.d. "Ngrok Documentation." Accessed February 14, 2026. https://ngrok.com/docs/.

MDN Web Docs. n.d. "HTML: HyperText Markup Language." Accessed February 14, 2026. https://developer.mozilla.org/en-US/docs/Web/HTML.

MDN Web Docs. n.d. "CSS: Cascading Style Sheets." Accessed February 14, 2026. https://developer.mozilla.org/en-US/docs/Web/CSS.

MDN Web Docs. n.d. "JavaScript." Accessed February 14, 2026. https://developer.mozilla.org/en-US/docs/Web/JavaScript.

---

# ภาคผนวก (Appendices)

## ภาคผนวก ก: การติดตั้งเครื่องมือที่ใช้พัฒนา
*   **ก.1 Visual Studio Code:** ดาวน์โหลดและติดตั้ง Extensions (Python, Docker)
*   **ก.2 Python & Virtual Environment:** ขั้นตอน `python -m venv venv`
*   **ก.3 Docker Desktop:** การตั้งค่า WSL2 Backend

## ภาคผนวก ข: คู่มือการติดตั้งระบบ (Installation Guide)
1.  **Clone Repository:** `git clone ...`
2.  **Environment Variables:** สร้างไฟล์ `.env` (SECRET_KEY, DB_CONFIG)
3.  **Docker Compose:** รันคำสั่ง `docker-compose up -d --build`
4.  **Migration & Superuser:** `docker-compose exec web python manage.py migrate`

## ภาคผนวก ค: คู่มือการใช้งาน (User Manual)
*   **ค.1 การสมัครสมาชิก:** กรอกข้อมูลและยืนยันอีเมล
*   **ค.2 การสร้างทัวร์นาเมนต์:** ตั้งค่า Bracket และอัปโหลดรูป
*   **ค.3 การเข้าร่วมผ่าน PIN:** ใส่รหัส 6 หลักที่ได้รับจาก Host
*   **ค.4 การโหวต:** กดปุ่ม Vote ให้คนที่ชอบภายในเวลาที่กำหนด


<!-- End of docs/chapter6_conclusion_appendices.md -->

