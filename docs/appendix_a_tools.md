ภาคผนวก ก 
การติดตั้งเครื่องมือที่ใช้พัฒนาโปรแกรม

ก.1 การติดตั้ง Python
1) ดาวน์โหลด Python 3.11 จาก https://www.python.org/downloads/
2) รันไฟล์ติดตั้ง เลือก "Add Python to PATH"
3) ตรวจสอบการติดตั้งด้วยคำสั่ง python --version

ก.2 การติดตั้ง Docker Desktop
1) ดาวน์โหลด Docker Desktop จาก https://www.docker.com/products/docker-desktop/
2) รันไฟล์ติดตั้งและ Restart เครื่อง
3) เปิด Docker Desktop และรอให้ Engine พร้อมใช้งาน
4) ตรวจสอบด้วยคำสั่ง docker --version และ docker-compose --version

ก.3 การติดตั้ง VS Code
1) ดาวน์โหลด VS Code จาก https://code.visualstudio.com/
2) รันไฟล์ติดตั้ง
3) ติดตั้ง Extensions ที่แนะนำ:
    - Python
    - Django
    - Docker
    - Prettier

ก.4 การติดตั้ง Git
1) ดาวน์โหลด Git จาก https://git-scm.com/downloads
2) รันไฟล์ติดตั้ง เลือก Default Options
3) ตรวจสอบด้วยคำสั่ง git --version

ก.5 การติดตั้ง PostgreSQL (สำหรับ Development)
1) ดาวน์โหลด PostgreSQL 15 จาก https://www.postgresql.org/download/
2) รันไฟล์ติดตั้ง กำหนดรหัสผ่าน superuser
3) ตรวจสอบด้วย pgAdmin หรือ psql
