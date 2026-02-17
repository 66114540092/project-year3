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
