บทที่ 2
ทฤษฎีที่เกี่ยวข้อง

2.1 Django Framework
Django เป็น Web Framework ภาษา Python ที่ใช้สถาปัตยกรรมแบบ MTV (Model-Template-View) โดยมีคุณสมบัติเด่นคือ "Batteries included" หมายความว่ามาพร้อมเครื่องมือสำเร็จรูปมากมาย เช่น ระบบ Authentication, ORM, Admin Panel และ Form Validation

ในโครงงานนี้ใช้ Django เวอร์ชัน 5.0 ซึ่งมีคุณสมบัติที่เหมาะสมกับการพัฒนา ได้แก่
- Django ORM สำหรับจัดการฐานข้อมูลโดยไม่ต้องเขียน SQL โดยตรง
- Django Templates สำหรับสร้างหน้าเว็บ
- Django Auth สำหรับระบบ Login/Logout
- CSRF Protection สำหรับป้องกันการโจมตีแบบ Cross-Site Request Forgery

2.2 Docker และ Containerization
Docker เป็นเทคโนโลยี Containerization ที่ช่วยให้สามารถ package แอปพลิเคชันพร้อม dependencies ทั้งหมดเป็น Container ที่สามารถรันได้ทุกเครื่องที่มี Docker โดยไม่ต้องกังวลเรื่อง environment ที่แตกต่างกัน

ข้อดีของการใช้ Docker:
- Consistency: รันได้เหมือนกันทุกเครื่อง
- Isolation: แต่ละ Container แยกกันอิสระ
- Scalability: สามารถเพิ่มจำนวน Container ได้ง่าย
- Easy Deployment: Deploy ได้รวดเร็วด้วยคำสั่งเดียว

ในโครงงานนี้ใช้ Docker Compose จัดการ 3 containers:
1) db: PostgreSQL database
2) web: Django application บน Gunicorn
3) nginx: Reverse proxy server

2.3 PostgreSQL Database
PostgreSQL เป็น Open-source Relational Database ที่มีความเสถียรและรองรับ features ขั้นสูง เหมาะสำหรับ Production environment

ข้อดีของ PostgreSQL เมื่อเปรียบเทียบกับ SQLite:
- รองรับ Concurrent connections หลายคนพร้อมกัน
- มี ACID compliance ที่แข็งแกร่ง
- รองรับ JSON data type
- มี Extensions มากมาย
ในโครงงานนี้ใช้ PostgreSQL 15 Alpine (lightweight version)

2.4 AJAX Polling และ Real-time Web
AJAX (Asynchronous JavaScript and XML) เป็นเทคนิคที่ช่วยให้หน้าเว็บสามารถสื่อสารกับ Server โดยไม่ต้อง refresh หน้าใหม่ทั้งหมด

รูปแบบ Real-time ที่ใช้ในโครงงานนี้คือ Polling โดย JavaScript จะส่ง request ไปยัง Server ทุก 2 วินาที เพื่อดึงข้อมูลล่าสุด เช่น จำนวน vote และเวลาที่เหลือ

ข้อดีของ Polling:
- ง่ายต่อการ implement ไม่ต้องใช้เทคโนโลยีเพิ่มเติม
- ทำงานได้กับทุก browser
- ไม่ต้องการ persistent connection

ข้อเสียของ Polling:
- มี overhead จากการส่ง request ซ้ำๆ
- มี delay เล็กน้อย (latency ตาม interval ที่กำหนด)

2.5 Tailwind CSS
Tailwind CSS เป็น Utility-first CSS Framework ที่ให้ class เล็กๆ สำหรับ style แต่ละ property โดยตรง แทนที่จะเป็น component สำเร็จรูปเหมือน Bootstrap

ข้อดีของ Tailwind CSS:
- Highly customizable: ปรับแต่งได้ทุกส่วน
- No unused CSS: build เฉพาะ class ที่ใช้จริง
- Responsive design: มี responsive prefix เช่น md:, lg:
- เหมาะกับ Dark theme: มี class dark: สำหรับ dark mode

ในโครงงานนี้ใช้ Tailwind CSS CDN เพื่อความสะดวกในการพัฒนา

2.6 ระบบ Bracket Tournament
Bracket Tournament (หรือ Knockout Tournament) เป็นรูปแบบการแข่งขันที่ผู้แพ้จะถูกคัดออกทันที ผู้ชนะจะเข้าสู่รอบถัดไปจนเหลือผู้ชนะคนสุดท้าย

โครงสร้าง Bracket แบบ Single Elimination:
- รอบที่ 1: n คน แข่งกัน ได้ผู้ชนะ n/2 คน
- รอบที่ 2: n/2 คน แข่งกัน ได้ผู้ชนะ n/4 คน
- รอบสุดท้าย: 2 คน แข่งกัน ได้แชมป์ 1 คน

จำนวนรอบ = log2(จำนวนผู้เข้าแข่งขัน)
- 2 คน = 1 รอบ
- 4 คน = 2 รอบ
- 8 คน = 3 รอบ
- 16 คน = 4 รอบ

2.7 Kahoot-style Lobby
Kahoot เป็นแพลตฟอร์ม Game-based Learning ที่มีชื่อเสียงด้านการออกแบบ UX สำหรับการเข้าร่วมกิจกรรมแบบง่ายดาย โดยใช้ระบบ PIN Code

แนวคิดหลักของ Kahoot-style Lobby:
1) Host สร้าง session และได้รับ PIN Code
2) ผู้เล่นเข้าเว็บ → กรอก PIN → กรอก Nickname
3) Host เห็นรายชื่อผู้เข้าร่วมแบบ Real-time
4) Host กด Start เมื่อพร้อม

ในโครงงานนี้ได้นำแนวคิดดังกล่าวมาประยุกต์ใช้กับระบบ Tournament

2.8 งานวิจัยที่เกี่ยวข้อง
2.8.1 ระบบจัดการการแข่งขันออนไลน์
มีหลายแพลตฟอร์มที่ให้บริการจัดการ Tournament เช่น Challonge, Toornament อย่างไรก็ตาม แพลตฟอร์มเหล่านี้ไม่ได้เน้นระบบโหวต Real-time หรือ Kahoot-style Lobby

2.8.2 ระบบโหวตออนไลน์
มีงานวิจัยหลายชิ้นที่พัฒนาระบบโหวตออนไลน์ เช่น ระบบเลือกตั้ง ระบบประเมินผล แต่ส่วนใหญ่ไม่ได้ออกแบบมาสำหรับการแข่งขันแบบ Bracket

โครงงาน BattleHub จึงพัฒนาขึ้นเพื่อรวมจุดเด่นของทั้ง Tournament Management และ Real-time Voting ไว้ในแพลตฟอร์มเดียว
