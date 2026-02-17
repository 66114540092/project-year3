# BattleHub Defense Cheat Sheet 🛡️
**เป้าหมาย:** เอาตัวรอดจากการสอบสัมภาษณ์และการเขียนโค้ดสด (Live Coding)
**เน้น:** `tournaments/models.py` (ตามที่อาจารย์บอก)

---

## 🎯 Part 1: เข้าใจโครงสร้าง `models.py` (ต้องตอบได้!)

อาจารย์มักถามว่า **"ทำไมออกแบบแบบนี้?"** หรือ **"ตารางนี้คืออะไร?"**

### 1. Model: `Tournament` (หัวใจหลัก)
*   **หน้าที่:** เก็บข้อมูลการแข่ง (ชื่อ, กติกา, สถานะ)
*   **จุดที่ต้องแม่น:**
    *   `status`: ใช้เก็บสถานะ (`draft`, `waiting`, `open`, `finished`) -> **ใช้คุม Flow ของระบบ**
    *   `bracket_size`: ขนาดกระดาน (2, 4, 8, 16) -> **ใช้คำนวณจำนวนรอบ (Log2)**
    *   `pin_code`: เก็บ PIN 6 หลัก -> **ใช้ให้คน Join ห้อง Lobby**
*   **คำถามปราบเซียน:**
    *   Q: "ทำไม `created_by` ต้องใช้ `ForeignKey`?"
    *   A: "เพราะ 1 User สร้างได้หลาย Tournament ครับ (One-to-Many Relationship)"

### 2. Model: `Match` (ตัวจัดการจับคู่)
*   **หน้าที่:** เก็บข้อมูลการแข่ง **รายคู่** (ใครเจอใคร, ใครชนะ)
*   **จุดที่ต้องแม่น:**
    *   `round_number`: บอกว่าอยู่รอบไหน (1=รอบแรก, 2=รอบรอง, 3=ชิง)
    *   `index_in_round`: บอกว่าเป็นคู่ที่เท่าไหร่ในรอบนั้น
    *   `competitor1/2`: เชื่อมกับตาราง `Competitor` (คนที่แข่ง)
    *   `winner`: เก็บคนที่ชนะ (ถ้ายังไม่แข่งจะเป็น `null`)

### 3. Model: `Participant` (คนดู/คนโหวต)
*   **หน้าที่:** เก็บคนที่เข้ามาในห้อง Lobby (ผ่าน PIN Code)
*   **จุดที่ต้องแม่น:**
    *   `session_key`: เก็บ Session ID (สำหรับคนที่ไม่ Login ก็เล่นได้)

---

## 💻 Part 2: เก็งข้อสอบ "Live Coding" (models.py)

ถ้าอาจารย์สั่ง: **"ไหนลองแก้โค้ดเพิ่ม Field ให้ดูหน่อยซิ"**

### โจทย์ 1: เพิ่ม field เก็บข้อมูลใหม่
**คำสั่ง:** "เพิ่ม field `is_active` ให้ Tournament หน่อย เอาไว้ปิด/เปิดทัวร์"
**วิธีทำ:**
1.  เปิดไฟล์ `tournaments/models.py`
2.  ไปที่ class `Tournament`
3.  เพิ่มบรรทัดนี้:
```python
is_active = models.BooleanField(default=True)
```
**(เทคนิค: จำชนิด Field ให้ได้หลักๆ คือ `CharField`, `IntegerField`, `BooleanField`, `DateTimeField`)**

---

### โจทย์ 2: เขียน Method (Function) ใน Model
**คำสั่ง:** "เขียนฟังก์ชันใน Model Tournament ให้นับว่ามีคนแข่งครบหรือยัง"
**วิธีทำ:**
เขียนเพิ่มใน class `Tournament`:
```python
def is_full(self):
    # เช็คว่าจำนวนผู้เข้าแข่งขัน (competitors) เท่ากับขนาดบราเก็ตไหม
    return self.competitors.count() >= self.bracket_size
```

---

### โจทย์ 3: การ Query ข้อมูล (Django ORM)
**คำสั่ง:** "ดึง Tournament ทั้งหมดที่เป็นสถานะ 'Open' มาให้ดูหน่อย"
**วิธีทำ:** (อาจารย์อาจให้พิมพ์ใน Shell หรือ Views)
```python
# ดึงทั้งหมดที่ status = 'open'
open_tournaments = Tournament.objects.filter(status='open')

# ดึงอันล่าสุด
latest = Tournament.objects.last()

# นับจำนวน
count = Tournament.objects.count()
```

---

## ⚠️ Part 3: จุดที่ห้ามพลาด (Common Mistakes)

1.  **แก้ Model แล้วต้องทำอะไรต่อ?**
    *   ตอบ: "ต้องรัน `makemigrations` และ `migrate` ครับ เพื่อให้ Database อัปเดตตามโค้ด" (ท่องไว้ให้ขึ้นใจ!)

2.  **`on_delete=models.CASCADE` คืออะไร?**
    *   ตอบ: "ถ้าตัวแม่ถูกลบ ตัวลูกจะถูกลบตามครับ" (เช่น ถ้าลบ Tournament -> Match และ Competitor ข้างในจะหายไปด้วย)

3.  **`related_name` คืออะไร?**
    *   ตอบ: "ชื่อเล่นที่เอาไว้เรียกย้อนกลับครับ" (เช่น จาก User อยากรู้ว่าสร้าง Tournament อะไรบ้าง ก็เรียก `user.created_tournaments.all()` ได้เลย)

---

## 🚀 สรุปสั้นๆ ก่อนเข้าห้องสอบ
1.  **จำความสัมพันธ์:** Tournament -> (1:N) -> Match / Competitor
2.  **จำคำสั่ง Field:** `models.CharField`, `models.ForeignKey`
3.  **จำคำสั่ง Query:** `.filter()`, `.get()`, `.create()`

**“สู้ๆ ครับลูกพี่! โค้ดชุดนี้เราเขียนมากับมือ ตอบได้แน่นอน!”** ✌️
