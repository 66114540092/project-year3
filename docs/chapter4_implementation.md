บทที่ 4
การพัฒนาระบบ

4.1 การติดตั้งสถาปัตยกรรมระบบ

การตั้งค่า Docker Compose
ระบบใช้ Docker Compose ในการจัดการ 3 services หลัก ได้แก่ db (PostgreSQL), web (Django/Gunicorn) และ nginx (Reverse Proxy)
ไฟล์ docker-compose.yml มีการตั้งค่าดังนี้
- Service db ใช้ image postgres:15-alpine ตั้งชื่อ container เป็น battlehub_db กำหนด environment variables สำหรับชื่อฐานข้อมูล ชื่อผู้ใช้ และรหัสผ่าน พร้อมทั้งกำหนด volume สำหรับเก็บข้อมูลถาวร
- Service web ใช้ Dockerfile ในการ build ตั้งชื่อ container เป็น battlehub_web รันคำสั่ง migrate, collectstatic และ gunicorn ตามลำดับ กำหนด environment variables สำหรับ DEBUG=False และข้อมูลการเชื่อมต่อ database
- Service nginx ใช้ image nginx:alpine ตั้งชื่อ container เป็น battlehub_nginx เปิด port 80 สำหรับรับ traffic จากภายนอก

การตั้งค่า Django settings.py
ระบบใช้ environment variables เพื่อแยก development กับ production โดยถ้ามี POSTGRES_DB ใน environment จะใช้ PostgreSQL แต่ถ้าไม่มีจะใช้ SQLite สำหรับ development
นอกจากนี้ยังตั้งค่า DEBUG=False สำหรับ production, ใช้ WhiteNoise สำหรับ serve static files และกำหนด ALLOWED_HOSTS

วิธีการ Deploy
1) รันคำสั่ง docker-compose up --build -d
2) ระบบจะ migrate database อัตโนมัติ
3) Static files จะถูก collect อัตโนมัติ
4) เข้าใช้งานที่ https://c271a6310f28.ngrok-free.app

(รูปที่ 4.1 ผลการรัน docker-compose ps แสดง containers ที่ทำงาน)

4.2 หน้าจอการใช้งาน

4.2.1 หน้าแรก - รายการทัวร์นาเมนต์
หน้าแรกแสดงรายการทัวร์นาเมนต์ทั้งหมดในรูปแบบ Grid โดยแต่ละการ์ดจะแสดงรูป thumbnail ของทัวร์นาเมนต์ ชื่อทัวร์นาเมนต์ สถานะ (Draft/Live/Finished) และจำนวนผู้เข้าแข่งขัน
มีระบบ search สำหรับค้นหาตามชื่อ และ filter สำหรับกรองตาม category และ status

(รูปที่ 4.2 หน้าแรกแสดงรายการทัวร์นาเมนต์)

4.2.2 หน้าโหวต - Battle Arena
หน้าโหวตแสดงผู้เข้าแข่งขัน 2 คนเทียบกัน ผู้ใช้คลิกที่รูปเพื่อโหวต โดยจะแสดงจำนวน vote แบบ real-time มี progress bar แสดงสัดส่วน vote และมีตัวนับเวลาถ้าเปิดใช้งาน

(รูปที่ 4.3 หน้า Battle Arena สำหรับโหวต)

4.2.3 หน้าประกาศผู้ชนะ
เมื่อทัวร์นาเมนต์จบ ระบบจะแสดง animation ฉลองผู้ชนะ โดยมี confetti effect แสดงรูปผู้ชนะขนาดใหญ่ และแสดงสถิติจำนวน vote ที่ได้รับ

(รูปที่ 4.4 หน้าประกาศผู้ชนะพร้อม animation)

4.2.4 Admin Dashboard
หน้า admin แสดงสถิติภาพรวมของระบบ ได้แก่ จำนวนผู้ใช้ทั้งหมด จำนวนทัวร์นาเมนต์ จำนวน vote ทั้งหมด และรายการกิจกรรมล่าสุด

(รูปที่ 4.5 หน้า Admin Dashboard)


4.3 การพัฒนาฟีเจอร์หลัก

4.3.1 ระบบอัปโหลดแบบ Bulk Upload
ผู้ใช้สามารถลากไฟล์หลายไฟล์มาวางได้พร้อมกัน โดยระบบจะแสดง preview ของแต่ละรูปพร้อมช่องกรอกชื่อผู้เข้าแข่งขัน
- ฝั่ง Frontend ใช้ JavaScript จัดการ drag and drop events เมื่อผู้ใช้ลากไฟล์มาวาง ระบบจะอ่านไฟล์ด้วย FileReader และแสดง preview พร้อมช่องกรอกชื่อ
- ฝั่ง Backend ใช้ Django view รับ request.FILES.getlist เพื่อรับไฟล์หลายไฟล์ และ request.POST.getlist เพื่อรับชื่อหลายชื่อ จากนั้นสร้าง Competitor objects ทีละตัวโดยตรวจสอบไม่ให้เกิน bracket size ที่กำหนด

4.3.2 ระบบ Real-time Polling
ใช้ JavaScript setInterval ดึงข้อมูลจาก server ทุก 2 วินาที เพื่อให้ผู้ใช้เห็นจำนวน vote ที่อัปเดตจากผู้ใช้คนอื่น
- ฝั่ง Frontend ใช้ fetch API ส่ง request ไปยัง endpoint /vote_update/ ทุก 2 วินาที เมื่อได้ response กลับมาจะอัปเดตจำนวน vote, progress bar และเวลาที่เหลือ ถ้า server ส่ง redirect_url มา JavaScript จะเปลี่ยนหน้าอัตโนมัติ
- ฝั่ง Backend ใช้ Django view ตรวจสอบเวลาที่เหลือ (time_remaining) และ auto-finish match เมื่อหมดเวลา จากนั้นส่ง JSON response กลับไป

4.3.3 ระบบ Kahoot-style Lobby
ผู้สร้างทัวร์นาเมนต์สามารถเปิด Lobby ให้ผู้เล่นเข้าร่วมผ่าน PIN Code 6 หลักที่ระบบ generate อัตโนมัติ
- ฝั่ง Frontend มี 2 หน้า:
    1) หน้ากรอก PIN: ผู้เล่นกรอกรหัส 6 หลักเพื่อหาทัวร์นาเมนต์
    2) หน้า Waiting Lobby: แสดงรายชื่อผู้เข้าร่วมแบบ Real-time โดย Host จะเห็นปุ่ม "Start Tournament"
- ฝั่ง Backend มี endpoints:
    - join_lobby_pin: รับ PIN แล้ว redirect ไปหน้ากรอก nickname
    - waiting_lobby: แสดงรายชื่อผู้เข้าร่วม
    - participant_status: API สำหรับ polling รายชื่อผู้เข้าร่วม real-time

(รูปที่ 4.6 หน้า Join via PIN)
(รูปที่ 4.7 หน้า Waiting Lobby)

4.3.4 ระบบ Server-synced Timer
เพื่อป้องกันผู้ใช้โกงเวลา (เช่น ตั้งนาฬิกาคอมพิวเตอร์ช้ากว่าปกติ) ระบบใช้เวลาจาก Server เป็นหลัก
- ฝั่ง Frontend:
    - ใช้ time_remaining จาก server sync ทุก 2 วินาที
    - ถ้าเวลาต่างกันเกิน 2 วินาที จะ reset countdown ใหม่
    - แสดง Toast notification เมื่อเหลือ 10 วินาที
- ฝั่ง Backend:
    - เก็บ started_at ใน Match model
    - คำนวณ time_remaining = voting_duration_seconds - elapsed
    - เมื่อ time_remaining <= 0 จะ auto-finish match

(รูปที่ 4.8 หน้า Play แสดง Timer นับถอยหลัง)

4.3.5 ระบบ Toast Notifications
เพิ่ม Toast notification แบบ slide-in จากขวาเพื่อแจ้งเตือนผู้ใช้
ประเภท Notification:
- Warning (สีเหลือง): "เหลือเวลา 10 วินาที!"
- Success (สีเขียว): "หมดเวลา!", "เกมเริ่มแล้ว!"
- Info (สีฟ้า): "มีผู้เล่นเข้าร่วม!"
ใช้ CSS animation @keyframes slideIn/slideOut และ backdrop-filter blur

(รูปที่ 4.9 ตัวอย่าง Toast Notification)

4.3.6 ระบบ Auto-redirect
เมื่อแมตช์จบหรือทัวร์นาเมนต์จบ ระบบจะเปลี่ยนหน้าอัตโนมัติ
Logic การ redirect:
- เมื่อแมตช์จบ (timer หมด) → server ตรวจสอบว่ารอบนี้จบทุกแมตช์หรือยัง
- ถ้ายังมีรอบถัดไป → สร้าง next round matches และ redirect ไป /bracket/
- ถ้าเป็นรอบสุดท้าย → เปลี่ยน tournament.status = 'finished' และ redirect ไป /summary/
ฝั่ง Frontend: ตรวจสอบ redirect_url ใน response ทุกครั้งที่ poll และเปลี่ยนหน้าด้วย window.location.href
