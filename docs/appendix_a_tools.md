# ภาคผนวก ก
# การติดตั้งเครื่องมือที่ใช้พัฒนาโปรแกรม

การติดตั้งเครื่องมือที่ใช้ในการพัฒนาเว็บแอพพลิเคชันระบบจัดการการแข่งขันและโหวตแบบเรียลไทม์ (BattleHub) มีโปรแกรมที่จำเป็นในการพัฒนาระบบดังต่อไปนี้

## ก.1 การติดตั้ง Visual Studio Code
1.  ดาวน์โหลดโปรแกรม Visual Studio Code จากเว็บไซต์ https://code.visualstudio.com/
2.  ทำการติดตั้งโปรแกรมตามขั้นตอนมาตรฐาน (Default Installation)
3.  เปิดโปรแกรม Visual Studio Code และติดตั้ง Extensions ที่จำเป็น เช่น Python, Django, Docker

*(รูปที่ ก.1 หน้าต่างเว็บไซต์สำหรับดาวน์โหลด Visual Studio Code)*

*(รูปที่ ก.2 หน้าต่างโปรแกรม Visual Studio Code เมื่อติดตั้งเสร็จสมบูรณ์)*

## ก.2 การติดตั้ง Python
1.  ดาวน์โหลด Python เวอร์ชัน 3.11 ขึ้นไปจากเว็บไซต์ https://www.python.org/downloads/
2.  รันไฟล์ติดตั้ง และต้องเลือกติ๊กถูกที่ช่อง **"Add Python to PATH"** ก่อนกด Install
3.  ตรวจสอบการติดตั้งโดยเปิด Command Line แล้วพิมพ์คำสั่ง `python --version`

*(รูปที่ ก.3 หน้าต่างตัวเลือกการติดตั้ง Python (Add Python to PATH))*

*(รูปที่ ก.4 หน้าต่าง Command Line แสดงเวอร์ชันของ Python ที่ติดตั้งแล้ว)*

## ก.3 การติดตั้ง Docker
1.  ดาวน์โหลด Docker Desktop จากเว็บไซต์ https://www.docker.com/products/docker-desktop/
2.  ทำการติดตั้งและ Restart เครื่องคอมพิวเตอร์ 1 ครั้ง
3.  เปิดโปรแกรม Docker Desktop และรอจนกว่าสถานะจะขึ้นเป็น **"Engine Running"** (สีเขียว)

*(รูปที่ ก.5 หน้าต่างโปรแกรม Docker Desktop แสดงสถานะ Engine Running)*
