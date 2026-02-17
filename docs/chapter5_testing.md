# บทที่ 5
# การทดสอบระบบ (System Testing)

## 5.1 การทดสอบฟังก์ชันการทำงาน (Functional Testing)
ผลการทดสอบฟังก์ชันหลัก (General User Flow) จำนวน 14 Test Cases:

**ตารางที่ 5.1** ผลการทดสอบฟังก์ชันหลัก

| Test Case | Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | สมัครสมาชิก (Register) | บันทึกข้อมูลลง DB, Redirect ไปหน้า Login | ทำงานถูกต้อง | ✅ Pass |
| **TC-02** | เข้าสู่ระบบ (Login) | เข้าสู่หน้า Tournament List, สร้าง Session | ทำงานถูกต้อง | ✅ Pass |
| **TC-03** | สร้างทัวร์นาเมนต์ | สร้าง Record ใหม่ในสถานะ Draft | ทำงานถูกต้อง | ✅ Pass |
| **TC-04** | อัปโหลดรูป (Bulk) | รูปถูกบันทึกใน Media Folder, สร้าง Competitor ตามจำนวน | ทำงานถูกต้อง | ✅ Pass |
| **TC-05** | เริ่มการแข่งขัน (Generate Bracket) | สถานะเปลี่ยนเป็น In Progress, รอบแรกถูกสร้าง | ทำงานถูกต้อง | ✅ Pass |

## 5.2 การทดสอบฟีเจอร์พิเศษ (Special Features)

**ตารางที่ 5.2** ผลการทดสอบระบบ Lobby และ Real-time

| Test Case | Description | Result | Status |
| :--- | :--- | :--- | :--- |
| **TC-Lobby-01** | เข้าร่วมด้วย PIN (Correct) | เข้าสู่ห้องรอ, ชื่อปรากฏบนหน้าจอ Host | สำเร็จ | ✅ Pass |
| **TC-Lobby-02** | เข้าร่วมด้วย PIN (Wrong) | แจ้งเตือน "Invalid PIN" | สำเร็จ | ✅ Pass |
| **TC-Vote-01** | การโหวต (Normal) | คะแนนเพิ่มขึ้น, Bar Chart ขยับ | สำเร็จ | ✅ Pass |
| **TC-Vote-02** | โหวตซ้ำ (Duplicate) | แจ้งเตือน "You already voted", คะแนนไม่เพิ่ม | สำเร็จ | ✅ Pass |
| **TC-Timer-01** | เวลาหมด (Timeout) | ปิดรับโหวต, คำนวณผล, เปลี่ยนคู่ถัดไป | สำเร็จ | ✅ Pass |

## 5.3 การทดสอบประสิทธิภาพ (Non-Functional Testing)

**ตารางที่ 5.4** ผลการทดสอบประสิทธิภาพ

| Metric | Target | Result | Note |
| :--- | :--- | :--- | :--- |
| **Page Load Time** | < 2.0s | 0.8s - 1.2s | ทดสอบบน Localhost |
| **Concurrent Users** | 50 Users | Stable | ทดสอบด้วย Apache JMeter |
| **Responsive** | Mobile View | 100% Compatible | ทดสอบบน iPhone/Android |

## 5.4 การยืนยันการติดตั้งระบบ (Deployment Verification)
1.  **Docker Containers:** 3 Containers (`web`, `db`, `nginx`) สถานะ **Up (Healthy)**
2.  **Database Connection:** Django เชื่อมต่อ PostgreSQL ได้สมบูรณ์ ผ่าน Port 5432 (Internal)
3.  **Static Files:** Nginx ให้บริการไฟล์ CSS/JS ได้ถูกต้อง ไม่เกิด 404 Error

## 5.5 สรุปผลการทดสอบ
ระบบ BattleHub ผ่านการทดสอบตามแผนการที่วางไว้ ทั้งในด้านฟังก์ชัน (Functional) ความถูกต้องของตรรกะ (Logic) และประสิทธิภาพเบื้องต้น (Performance) โดยสามารถทำงานได้จริงบนสภาพแวดล้อม Docker
