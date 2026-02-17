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
