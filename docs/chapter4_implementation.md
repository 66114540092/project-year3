บทที่ 4 การพัฒนาระบบ (ผลการดำเนินงาน)


4.1 การติดตั้งสถาปัตยกรรมระบบ

การตั้งค่า Docker Compose

ระบบใช้ Docker Compose ในการจัดการ 3 services หลัก ได้แก่ db (PostgreSQL), web (Django/Gunicorn) และ nginx (Reverse Proxy)

ไฟล์ docker-compose.yml มีการตั้งค่าดังนี้

Service db ใช้ image postgres:15-alpine ตั้งชื่อ container เป็น battlehub_db กำหนด environment variables สำหรับชื่อฐานข้อมูล ชื่อผู้ใช้ และรหัสผ่าน พร้อมทั้งกำหนด volume สำหรับเก็บข้อมูลถาวร

Service web ใช้ Dockerfile ในการ build ตั้งชื่อ container เป็น battlehub_web รันคำสั่ง migrate, collectstatic และ gunicorn ตามลำดับ กำหนด environment variables สำหรับ DEBUG=False และข้อมูลการเชื่อมต่อ database

Service nginx ใช้ image nginx:alpine ตั้งชื่อ container เป็น battlehub_nginx เปิด port 80 สำหรับรับ traffic จากภายนอก

การตั้งค่า Django settings.py

ระบบใช้ environment variables เพื่อแยก development กับ production โดยถ้ามี POSTGRES_DB ใน environment จะใช้ PostgreSQL แต่ถ้าไม่มีจะใช้ SQLite สำหรับ development

นอกจากนี้ยังตั้งค่า DEBUG=False สำหรับ production, ใช้ WhiteNoise สำหรับ serve static files และกำหนด ALLOWED_HOSTS

วิธีการ Deploy

1) รันคำสั่ง docker-compose up --build -d
2) ระบบจะ migrate database อัตโนมัติ
3) Static files จะถูก collect อัตโนมัติ
4) เข้าใช้งานที่ http://localhost:80

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

ฝั่ง Frontend ใช้ JavaScript จัดการ drag and drop events เมื่อผู้ใช้ลากไฟล์มาวาง ระบบจะอ่านไฟล์ด้วย FileReader และแสดง preview พร้อมช่องกรอกชื่อ

ฝั่ง Backend ใช้ Django view รับ request.FILES.getlist เพื่อรับไฟล์หลายไฟล์ และ request.POST.getlist เพื่อรับชื่อหลายชื่อ จากนั้นสร้าง Competitor objects ทีละตัวโดยตรวจสอบไม่ให้เกิน bracket size ที่กำหนด

4.3.2 ระบบ Real-time Polling

ใช้ JavaScript setInterval ดึงข้อมูลจาก server ทุก 3 วินาที เพื่อให้ผู้ใช้เห็นจำนวน vote ที่อัปเดตจากผู้ใช้คนอื่น

ฝั่ง Frontend ใช้ fetch API ส่ง request ไปยัง endpoint /api/match-status/ ทุก 3 วินาที เมื่อได้ response กลับมาจะอัปเดตจำนวน vote และ progress bar บนหน้าจอ ถ้าแมตช์จบแล้วจะหยุด polling และแสดงผู้ชนะ

ฝั่ง Backend ใช้ Django view ตรวจสอบว่าผู้ใช้เคยโหวตแล้วหรือยัง ถ้ายังไม่เคยจะบันทึก Vote และอัปเดต count จากนั้นส่ง JSON response กลับไป


4.4 ผลการทดสอบ

4.4.1 ทดสอบฟังก์ชันการทำงาน

TC-01 ทดสอบสมัครสมาชิก คาดหวังว่าสร้าง account สำเร็จ ผลจริงคือสำเร็จ สถานะผ่าน

TC-02 ทดสอบเข้าสู่ระบบ คาดหวังว่า login ได้ ผลจริงคือได้ สถานะผ่าน

TC-03 ทดสอบสร้างทัวร์นาเมนต์ คาดหวังว่าบันทึกสำเร็จ ผลจริงคือสำเร็จ สถานะผ่าน

TC-04 ทดสอบอัปโหลด 4 รูป คาดหวังว่าสร้าง 4 competitors ผลจริงคือสร้างได้ 4 คน สถานะผ่าน

TC-05 ทดสอบโหวต คาดหวังว่าเพิ่ม count +1 ผลจริงคือเพิ่มแล้ว สถานะผ่าน

TC-06 ทดสอบโหวตซ้ำ คาดหวังว่าไม่ให้โหวต ผลจริงคือบล็อกได้ สถานะผ่าน

TC-07 ทดสอบ Real-time update คาดหวังว่าเห็น vote ใหม่ ผลจริงคืออัปเดตทุก 3 วินาที สถานะผ่าน

TC-08 ทดสอบ Docker deploy คาดหวังว่า containers ทำงาน ผลจริงคือทำงานปกติ สถานะผ่าน

4.4.2 ทดสอบ Non-Functional

ทดสอบเวลาโหลดหน้า เป้าหมายไม่เกิน 2 วินาที ผลจริง 1.2 วินาที สถานะผ่าน

ทดสอบ CSRF Protection เป้าหมายทุกฟอร์ม ผลจริงมีทุกฟอร์ม สถานะผ่าน

ทดสอบ Responsive เป้าหมายใช้งานได้บน mobile ผลจริงปรับ layout ได้ สถานะผ่าน


4.5 การยืนยันการ Deploy

สถานะ Containers หลังจาก deploy

battlehub_db มีสถานะ Up (healthy) เปิด port 5432

battlehub_nginx มีสถานะ Up เปิด port 0.0.0.0:80 ไปยัง 80

battlehub_web มีสถานะ Up เปิด port 8000

ช่องทางเข้าใช้งาน

เว็บหลักสำหรับผู้ใช้ทั่วไป เข้าที่ http://localhost

Django Admin สำหรับจัดการข้อมูล เข้าที่ http://localhost/admin

Custom Dashboard สำหรับดูสถิติ เข้าที่ http://localhost/admin-panel

(รูปที่ 4.6 ผลการทดสอบเข้าใช้งานผ่าน browser)
