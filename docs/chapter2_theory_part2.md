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
