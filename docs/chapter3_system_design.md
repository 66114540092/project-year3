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
