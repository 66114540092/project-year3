บทที่ 3 การออกแบบระบบ


3.1 สถาปัตยกรรมระบบ

ระบบ BattleHub ใช้สถาปัตยกรรมแบบ Containerized ผ่าน Docker เพื่อให้ง่ายต่อการ deploy และ scale ในอนาคต โดยแบ่งออกเป็น 3 ส่วนหลัก ได้แก่ Web Server, Application Server และ Database Server

โครงสร้างการทำงานของระบบมีลำดับดังนี้

ผู้ใช้ (Browser) → Nginx → Docker Container (Gunicorn/Django) → PostgreSQL

รายละเอียดแต่ละ Layer มีดังนี้

1) Client Layer คือส่วนที่ผู้ใช้เข้าถึงผ่าน Browser โดยหน้า Frontend ใช้ HTML5 สำหรับโครงสร้าง, Tailwind CSS สำหรับจัดรูปแบบ และ JavaScript สำหรับ AJAX polling เพื่อดึงข้อมูลแบบ real-time

2) Web Server Layer คือ Nginx ทำหน้าที่เป็น reverse proxy รับ request ที่ port 80 และส่งต่อไปยัง application server รวมถึงให้บริการ static files และ media files

3) Application Layer คือ Django framework ทำงานบน Gunicorn WSGI server ภายใน Docker container ทำหน้าที่จัดการเรื่อง authentication, business logic และ API endpoints

4) Database Layer คือ PostgreSQL ที่ทำหน้าที่เก็บข้อมูลผู้ใช้ ทัวร์นาเมนต์ ผู้เข้าแข่งขัน และผลโหวตทั้งหมด

(รูปที่ 3.1 แผนภาพสถาปัตยกรรมระบบ)

บันทึกการเปลี่ยนแปลง Tech Stack

เวอร์ชัน 1.0 (มกราคม 2569) ได้ทำการเปลี่ยนจาก SQLite เป็น PostgreSQL เนื่องจาก PostgreSQL รองรับ concurrent users ได้ดีกว่าใน production environment โดยในช่วงพัฒนา local ยังคงใช้ SQLite เพื่อความสะดวก แต่ production ใช้ PostgreSQL ผ่าน Docker


3.2 ความต้องการของระบบ

3.2.1 ความต้องการด้านฟังก์ชัน (Functional Requirements)

FR-01 ระบบลงทะเบียนและเข้าสู่ระบบ
ผู้ใช้สามารถสมัครสมาชิก เข้าสู่ระบบ และออกจากระบบได้ โดยรหัสผ่านจะถูกเข้ารหัสด้วย PBKDF2

FR-02 สร้างทัวร์นาเมนต์
สมาชิกสามารถสร้างทัวร์นาเมนต์แบบ knockout ได้ โดยกำหนดขนาด bracket ได้ 2, 4, 8 หรือ 16 คน

FR-03 อัปโหลดผู้เข้าแข่งขัน
ระบบรองรับการอัปโหลดรูปหลายรูปพร้อมกัน (Bulk Upload) ผ่านการลากและวาง (Drag and Drop)

FR-04 ระบบโหวต real-time
ผู้ใช้โหวตแล้วเห็นผลทันทีผ่าน AJAX polling โดย browser จะดึงข้อมูลจาก server ทุก 3 วินาที

FR-05 ระบบ Admin Dashboard
ผู้ดูแลระบบสามารถดูสถิติภาพรวม จัดการทัวร์นาเมนต์ และจัดการผู้ใช้ได้

3.2.2 ความต้องการด้านอื่นๆ (Non-Functional Requirements)

NFR-01 ความเร็ว
ระบบต้องโหลดหน้าไม่เกิน 2 วินาที

NFR-02 ความปลอดภัย
ระบบต้องมี CSRF protection ทุกฟอร์ม

NFR-03 Responsive Design
หน้าเว็บต้องใช้งานได้ทั้ง Desktop และ Mobile


3.3 การออกแบบ UI

ระบบใช้ธีม Dark Gaming Theme เพื่อให้เข้ากับบรรยากาศการแข่งขัน โดยมีหลักการออกแบบดังนี้

สีพื้นหลังเข้ม (#0a0f1a) เพื่อลดความเมื่อยล้าสายตาเมื่อใช้งานนาน

สี Accent ใช้ฟ้าและม่วง gradient เพื่อสร้างความรู้สึกตื่นเต้น เหมาะกับบรรยากาศการแข่งขัน

มี glow effect และ animation เพิ่มความน่าสนใจ

ใช้ Font Awesome icons ทั้งระบบเพื่อความสม่ำเสมอ

(รูปที่ 3.2 ตัวอย่างหน้าจอหลักของระบบ)


3.4 Use Case Diagram

ระบบมีผู้ใช้งาน 3 ประเภท ได้แก่

1) Guest คือผู้เยี่ยมชมที่ยังไม่ได้ login สามารถดูรายการทัวร์นาเมนต์ สมัครสมาชิก และเข้าสู่ระบบได้

2) Member คือสมาชิกที่ลงทะเบียนแล้ว สามารถสร้างทัวร์นาเมนต์ อัปโหลดผู้เข้าแข่งขัน โหวต และแก้ไขโปรไฟล์ได้

3) Admin คือผู้ดูแลระบบ สามารถดู Dashboard จัดการทัวร์นาเมนต์ และจัดการผู้ใช้ทั้งหมดได้

(รูปที่ 3.3 Use Case Diagram)


3.5 Class Diagram

ระบบประกอบด้วย Django Models หลักดังนี้

User เก็บข้อมูลผู้ใช้ ประกอบด้วย id, username, email, password

Profile เก็บข้อมูลโปรไฟล์เพิ่มเติม ประกอบด้วย id, user_id (FK), avatar, bio มีความสัมพันธ์แบบ one-to-one กับ User

Tournament เก็บข้อมูลทัวร์นาเมนต์ ประกอบด้วย id, name, bracket_size, status, created_by (FK) มีความสัมพันธ์แบบ many-to-one กับ User

Competitor เก็บข้อมูลผู้เข้าแข่งขัน ประกอบด้วย id, tournament_id (FK), name, image มีความสัมพันธ์แบบ many-to-one กับ Tournament

Match เก็บข้อมูลแมตช์ ประกอบด้วย id, tournament_id (FK), competitor_a (FK), competitor_b (FK), votes_a, votes_b, winner (FK)

Vote เก็บข้อมูลการโหวต ประกอบด้วย id, match_id (FK), user_id (FK), competitor_id (FK)

(รูปที่ 3.4 Class Diagram)


3.6 Sequence Diagram

กระบวนการโหวต Real-time มีลำดับดังนี้

1) ผู้ใช้คลิกโหวตที่รูปผู้เข้าแข่งขัน
2) JavaScript ส่ง AJAX POST request ไปยัง /vote/
3) Django ตรวจสอบว่าผู้ใช้โหวตแล้วหรือยัง
4) ถ้ายังไม่เคยโหวต ระบบบันทึก Vote และอัปเดต count
5) Server ส่ง JSON response กลับมา พร้อมจำนวน votes_a และ votes_b
6) JavaScript อัปเดตหน้าจอ
7) ทุกๆ 3 วินาที browser จะ poll ข้อมูลใหม่จาก server

(รูปที่ 3.5 Sequence Diagram กระบวนการโหวต)


3.7 Data Model

ระบบมีตารางในฐานข้อมูลดังนี้

ตาราง User เก็บข้อมูลผู้ใช้ มี id เป็น Primary Key

ตาราง Profile เก็บโปรไฟล์ มี id เป็น Primary Key และ user_id เป็น Foreign Key อ้างอิงไปยัง User

ตาราง Tournament เก็บทัวร์นาเมนต์ มี id เป็น Primary Key และ created_by เป็น Foreign Key อ้างอิงไปยัง User

ตาราง Competitor เก็บผู้เข้าแข่งขัน มี id เป็น Primary Key และ tournament_id เป็น Foreign Key อ้างอิงไปยัง Tournament

ตาราง Match เก็บแมตช์ มี id เป็น Primary Key และมี Foreign Keys ได้แก่ tournament_id, competitor_a, competitor_b, winner

ตาราง Vote เก็บการโหวต มี id เป็น Primary Key และมี Foreign Keys ได้แก่ match_id, user_id, competitor_id

(รูปที่ 3.6 ER Diagram)
