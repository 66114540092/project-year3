# บทที่ 4
# การพัฒนาระบบ

ในบทนี้จะกล่าวถึงรายละเอียดการพัฒนาระบบ BattleHub ซึ่งพัฒนาด้วย Django Framework โดยแบ่งเนื้อหาออกเป็นโครงสร้างแอปพลิเคชัน, การตั้งค่าระบบ, การจัดการไฟล์, การพัฒนาฟังก์ชันหลักตาม Use Case และการจัดการส่วนติดต่อผู้ใช้ (UI/UX)

## 4.1 โครงสร้างแอปพลิเคชันและการตั้งค่า (Project Configuration)

### 4.1.1 การจัดการ Settings.py สำหรับการเชื่อมต่อฐานข้อมูลและ Static Files

ไฟล์ `settings.py` เป็นหัวใจหลักในการกำหนดค่าการทำงานของ Django Project ในระบบ BattleHub ได้มีการกำหนดค่าสำคัญดังนี้:

**1. การลงทะเบียนแอปพลิเคชัน (Installed Apps)**
เพื่อให้ Django รู้จักและสามารถทำงานร่วมกับแอปพลิเคชันที่สร้างขึ้นใหม่ จำเป็นต้องเพิ่มชื่อ App เข้าไปในตัวแปร `INSTALLED_APPS` โดยระบบนี้ได้เพิ่มแอปพลิเคชันหลัก 3 ตัว ได้แก่:

```python
INSTALLED_APPS = [
    # Django Default Apps...
    'django.contrib.admin',
    'django.contrib.auth',
    
    # BattleHub Apps
    'accounts',        # จัดการ User & Profile
    'tournaments',     # จัดการระบบแข่งขันและ Lobby
    'custom_admin',    # ระบบ Dashboard ของ Admin (แยกจาก Django Admin ปกติ)
    
    # Third-party Apps
    'tailwind',        # สำหรับจัดการ CSS Framework
    'theme',           # แอปพลิเคชันสำหรับ Theme ของ Tailwind
    'django_cleanup',  # ช่วยลบไฟล์รูปภาพเมื่อมีการลบข้อมูลใน DB
]
```

**2. การเชื่อมต่อฐานข้อมูล (Database Configuration)**
ระบบเลือกใช้ **PostgreSQL** เป็นฐานข้อมูลหลักสำหรับ Production เนื่องจากมีประสิทธิภาพสูงและรองรับข้อมูลเชิงสัมพันธ์ที่ซับซ้อน (โดยในสภาพแวดล้อม Local Development อาจใช้ SQLite เพื่อความสะดวก)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'battlehub_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**3. การจัดการไฟล์สถิตและมีเดีย (Static & Media Files)**
กำหนดเส้นทางสำหรับเก็บไฟล์ Static (CSS, JS) และ Media (รูปภาพที่ผู้สู้อัปโหลด เช่น รูปปกทัวร์นาเมนต์):

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 4.1.2 การออกแบบระบบ URL Routing (Urls.py) แบบแยกแอปพลิเคชัน

เพื่อให้ระบบมีความเป็นระเบียบและง่ายต่อการขยายผลในอนาคต โครงการได้ออกแบบ URL Routing แบบกระจาย (Decentralized Routing) โดยใช้ฟังก์ชัน `include()` ในไฟล์ `battlehub/urls.py` เพื่อเชื่อมต่อไปยัง URL ของแต่ละแอปพลิเคชันแยกกัน ดังนี้:

**ไฟล์: battlehub/urls.py (Project Level)**
```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # 1. Redirect Root URL ไปยังหน้า Tournament List ทันที เพื่อ UX ที่ดี
    path("", RedirectView.as_view(pattern_name="tournaments:tournament_list", permanent=False)),
    
    # 2. Django Admin (Backend System)
    path("admin/", admin.site.urls),
    
    # 3. Include URL ของแต่ละ App
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("tournaments/", include(("tournaments.urls", "tournaments"), namespace="tournaments")),
    path("admin-panel/", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),
]
```

การกำหนด `namespace` (เช่น `namespace="tournaments"`) ช่วยให้สามารถอ้างอิง URL ใน Template ได้อย่างถูกต้องและไม่ซ้ำซ้อน เช่น `{% url 'tournaments:play' pk=tournament.id %}`

---

## 4.2 โครงสร้างไฟล์และโฟลเดอร์ของระบบ (Django Directory Structure)

### 4.2.1 โครงสร้างระดับโครงการ (Project Level: battlehub/) และหน้าที่ของไฟล์ WSGI/ASGI

โครงสร้างไฟล์ของ Django Project ถูกจัดวางตามมาตรฐาน MVT (Model-View-Template) โดยมีโฟลเดอร์ `battlehub/` ทำหน้าที่เป็นศูนย์กลางการตั้งค่า (Configuration Center) ของระบบ ประกอบด้วยไฟล์สำคัญดังนี้:

*   **manage.py:** เครื่องมือ Command-line สำหรับจัดการโปรเจกต์ (เช่น `runserver`, `makemigrations`, `migrate`, `createsuperuser`)
*   **battlehub/settings.py:** ไฟล์ตั้งค่าหลักของระบบ (Database, Installed Apps, Static Files, Middleware)
*   **battlehub/urls.py:** ประตูทางเข้าหลัก (Main Gateway) ของ URL Routing ทั้งหมด
*   **battlehub/wsgi.py:** (Web Server Gateway Interface) สำหรับการ Deploy บน Web Server มาตรฐาน (Synchronous)
*   **battlehub/asgi.py:** (Asynchronous Server Gateway Interface) รองรับการทำงานแบบ Asynchronous สำหรับฟีเจอร์ Real-time ในอนาคต

### 4.2.2 โครงสร้างระดับแอปพลิเคชัน (App Level: accounts, tournaments, custom_admin)

ระบบ BattleHub ถูกแบ่งออกเป็น 3 แอปพลิเคชันหลักตามหน้าที่การทำงาน (Modular Design) ดังนี้:

1.  **accounts/**: รับผิดชอบระบบสมาชิกทั้งหมด
    *   จัดการ Sign Up, Login, Logout
    *   จัดการ User Profile (Avatar, Bio)
2.  **tournaments/**: หัวใจหลักของระบบ
    *   จัดการข้อมูล Tournament, Competitor, Match
    *   ระบบการแข่งขัน, การโหวต, และ Lobby
3.  **custom_admin/**: ระบบหลังบ้านสำหรับผู้ดูแล
    *   Dashboard สรุปสถิติ
    *   เครื่องมือจัดการ Users และ Tournaments (Ban, Delete, Force Finish)

### 4.2.3 หน้าที่ของไฟล์สำคัญในแต่ละแอปพลิเคชัน

ในแต่ละแอปพลิเคชัน จะประกอบด้วยไฟล์มาตรฐานที่ทำหน้าที่เฉพาะเจาะจงตามหลักการ Separation of Concerns:

*   **models.py:** กำหนดโครงสร้างข้อมูล (Database Schema) โดยใช้ Django ORM
*   **views.py:** เขียน Logic การทำงานหลัก (Business Logic) รับ Request ประมวลผล และส่ง Response กลับ
*   **forms.py:** สร้างแบบฟอร์มสำหรับการรับข้อมูลจากผู้ใช้ ตรวจสอบความถูกต้อง (Validation) และบันทึกลง Model
*   **urls.py:** กำหนดเส้นทาง URL ภายในแอปพลิเคชันนั้นๆ
*   **admin.py:** ลงทะเบียน Model เพื่อให้บริหารจัดการได้ผ่าน Django Admin Interface
*   **apps.py:** ตั้งค่าและลงทะเบียน Config ของแอปพลิเคชัน

### 4.2.4 การจัดหมวดหมู่ไฟล์เทมเพลต (Templates Hierarchy) และไฟล์สถิต (Static Files)

ระบบแยกไฟล์ HTML และไฟล์ Static (CSS, JS, Images) ไว้อย่างชัดเจนเพื่อความเป็นระเบียบ:

*   **templates/**: เก็บไฟล์ HTML โดยแบ่งโฟลเดอร์ย่อยตามชื่อ App
    *   `templates/base.html`: ไฟล์โครงร่างหลัก (Layout)
    *   `templates/accounts/`: (login.html, signup.html, profile.html)
    *   `templates/tournaments/`: (tournament_list.html, play.html, summary.html)
    *   `templates/custom_admin/`: (dashboard.html, reports.html)
*   **static/**: เก็บไฟล์ CSS, JavaScript และรูปภาพที่ใช้ร่วมกัน
    *   `static/css/style.css`: ไฟล์ CSS หลัก
    *   `static/images/`: โลโก้และรูปภาพไอคอน
    *   (Bootstrap/Tailwind CDN ถูกเรียกใช้ผ่าน Base Template โดยตรง)

---

## 4.3 การพัฒนาฟังก์ชันการทำงานด้วย Django (Core Implementation)

### 4.3.1 การขยายความสามารถของ User Model ผ่าน Profile Model

เพื่อให้ระบบสามารถเก็บข้อมูลเพิ่มเติมของผู้ใช้ เช่น รูปประจำตัว (Avatar) และคำแนะนำตัว (Bio) โดยไม่กระทบกับโครงสร้างหลักของ Django User (auth_user) จึงได้ใช้เทคนิค **One-to-One Link** สร้าง Model `Profile` เชื่อมต่อกับ `User`

**ไฟล์: accounts/models.py**
```python
class Profile(models.Model):
    # เชื่อมต่อกับ User แบบ 1-ต่อ-1 (1 User มี 1 Profile เท่านั้น)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
```

**การสร้าง Profile อัตโนมัติด้วย Signals (Signals.py)**
เพื่อความสะดวกและป้องกันข้อมูลไม่ครบถ้วน ระบบใช้ Django Signals (`post_save`) เพื่อดักจับเหตุการณ์ "เมื่อ User ถูกสร้าง" ให้ทำการ "สร้าง Profile" ให้ทันทีโดยอัตโนมัติ

**ไฟล์: accounts/signals.py**
```python
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

### 4.3.2 การเขียน Logic ใน Views.py (Core Business Logic)

ส่วนนี้จะอธิบายขั้นตอนการทำงานของระบบ (Business Logic) โดยละเอียด ซึ่งสอดคล้องกับแผนภาพลำดับ (Sequence Diagram) ที่ได้ออกแบบไว้ในบทที่ 3 โดยแบ่งออกเป็น 3 ส่วนหลัก ได้แก่ ส่วนผู้ใช้งานทั่วไป (Guest Flow), ส่วนสมาชิก (Member Flow), และส่วนผู้ดูแลระบบ (Admin Flow)

#### **1. SD-01: การดูรายการทัวร์นาเมนต์ (Guest Browsing)**
*   **ฟังก์ชัน (View):** `TournamentListView`
*   **คำอธิบาย (Goal):** ทำหน้าที่ดึงข้อมูลรายการทัวร์นาเมนต์ทั้งหมดที่มีสถานะ "เปิดรับสมัคร" (Open) หรือ "จบการแข่งขันแล้ว" (Finished) มาแสดงผลให้ผู้ใช้ทั่วไปได้รับทราบ
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **รับ Request:** ระบบรับ HTTP GET Request จากผู้ใช้งาน
    2.  **Query Data:** ทำการดึงข้อมูลจาก Database ผ่าน Django ORM โดยใช้คำสั่ง `Tournament.objects.filter()` โดยกรองเฉพาะทัวร์นาเมนต์ที่มีสถานะเป็น `open` หรือ `finished` เท่านั้น
    3.  **Filter & Search:** ตรวจสอบ Parameter จาก URL (Query String) หากมีการระบุคำค้นหาหรือหมวดหมู่ ระบบจะทำการกรองผลลัพธ์เพิ่มเติม
    4.  **Pagination:** หากผลลัพธ์มีจำนวนมาก ระบบจะแบ่งหน้า (Pagination) เพื่อไม่ให้โหลดข้อมูลหนักเกินไป
    5.  **Render Template:** ส่งข้อมูล Context (รายการทัวร์นาเมนต์) ไปยังไฟล์เทมเพลต `tournament_list.html` เพื่อแสดงผล
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    def tournament_list(request):
        # รับค่า Search Query และ Filter จาก URL
        search_query = request.GET.get("search", "")
        selected_status = request.GET.get("status", "")

        # Base Query: เรียงตามวันที่ล่าสุด
        tournaments = Tournament.objects.all().order_by('-created_at')

        # 1. Logic การค้นหา (Search)
        if search_query:
            tournaments = tournaments.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        # 2. Logic การกรองสถานะ (Filter)
        if selected_status:
            tournaments = tournaments.filter(status=selected_status)

        # ... (Pagination & Context setup) ...

        return render(request, "tournaments/tournament_list.html", context)
    ```

#### **2. SD-02: การสมัครสมาชิก (Guest Authentication - Sign Up)**
*   **ฟังก์ชัน (View):** `signup_view`
*   **คำอธิบาย (Goal):** จัดการกระบวนการลงทะเบียนสมาชิกใหม่ พร้อมทั้งสร้างข้อมูลส่วนตัว (Profile) อัตโนมัติ
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **Validate Request:** ตรวจสอบว่าเป็น HTTP POST หรือไม่ หากเป็น POST จะรับข้อมูลจากแบบฟอร์ม `CustomSignUpForm`
    2.  **Form Validation:** ตรวจสอบความถูกต้องของข้อมูล (เช่น รูปแบบอีเมล, รหัสผ่านที่ตรงกัน, ชื่อผู้ใช้ซ้ำ)
    3.  **Save User:** หากข้อมูลถูกต้อง จะบันทึกข้อมูลลงตาราง `auth_user`
    4.  **Signal Trigger:** ระบบ Django Signal (`post_save`) จะทำงานอัตโนมัติเพื่อสร้างข้อมูลในตาราง `accounts_profile` ที่ผูกกับ User นั้นๆ
    5.  **Login Immediately:** ทำการล็อกอินผู้ใช้ทันทีหลังสมัครเสร็จสิ้น (Auto-login)
    6.  **Redirect:** ส่งผู้ใช้งานไปยังหน้าแรก (Homepage)
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    def signup_view(request):
        if request.method == "POST":
            form = CustomSignUpForm(request.POST)
            # ตรวจสอบความถูกต้องของข้อมูล
            if form.is_valid():
                user = form.save()
                # หมายเหตุ: Signal (post_save) ใน models.py จะทำงานอัตโนมัติเพื่อสร้าง Profile
                
                # Login ทันทีหลังสมัครเสร็จ
                login(request, user)
                return redirect("tournaments:tournament_list")
        else:
            form = CustomSignUpForm()
        return render(request, "accounts/signup.html", {"form": form})
    ```

#### **3. SD-03: การสร้างทัวร์นาเมนต์ (Member Tournament Management)**
*   **ฟังก์ชัน (View):** `create_tournament_view`
*   **คำอธิบาย (Goal):** สำหรับสมาชิกที่เข้าสู่ระบบแล้ว ใช้ในการสร้างทัวร์นาเมนต์ใหม่
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **Authentication Check:** ใช้ Decorator `@login_required` ตรวจสอบสิทธิ์ว่าผู้ใช้ล็อกอินแล้วหรือไม่
    2.  **Process Form:** รับข้อมูลจาก `TournamentForm` (ชื่อ, รายละเอียด, รูปภาพปก)
    3.  **Assign Creator:** กำหนดให้ฟิลด์ `created_by` เป็น User ปัจจุบัน (`request.user`)
    4.  **Set Initial Status:** กำหนดสถานะเริ่มต้นเป็น `draft` (ฉบับร่าง)
    5.  **Save to DB:** บันทึกข้อมูลลงฐานข้อมูล
    6.  **Redirect:** เปลี่ยนเส้นทางไปยังหน้าอัปโหลดผู้เข้าแข่งขัน
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    @login_required
    def tournament_create(request):
        if request.method == "POST":
            form = TournamentForm(request.POST, request.FILES)
            if form.is_valid():
                # ยังไม่ Save ลง DB ทันที เพราะต้องเติมข้อมูลผู้สร้างก่อน
                tournament = form.save(commit=False)
                tournament.created_by = request.user
                tournament.status = "draft"  # กำหนดสถานะเริ่มต้น
                tournament.current_round = 1
                tournament.save()
                
                return redirect("tournaments:add_competitors", pk=tournament.pk)
        else:
            form = TournamentForm()
        return render(request, "tournaments/tournament_form.html", {"form": form})
    ```

#### **4. SD-04: ระบบห้องพักรอ (Member Lobby System)**
*   **ฟังก์ชัน (View & API):** `join_lobby_view` และ `lobby_status_api`
*   **คำอธิบาย (Goal):** จัดการการเข้าร่วม Lobby แบบ Real-time ผู้เล่นสามารถเข้าร่วมด้วย PIN Code และ Host สามารถเห็นรายชื่อผู้เข้าร่วมทันที
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **Join Lobby (Validation):** ผู้เล่นกรอก PIN และชื่อเล่น ระบบตรวจสอบ PIN ว่าตรงกับทัวร์นาเมนต์หรือไม่ และตรวจสอบชื่อซ้ำ
    2.  **Create Participant:** หากถูกต้อง ระบบสร้าง Object `Participant` ผูกกับ Session ของผู้เล่น
    3.  **Polling Mechanism:** ฝั่ง Frontend (JavaScript) จะส่ง AJAX Request ไปยัง API ทุกๆ 3 วินาที
    4.  **Return Status:** API ตรวจสอบสถานะทัวร์นาเมนต์และคืนค่า JSON ที่ประกอบด้วยรายชื่อผู้เข้าร่วมปัจจุบัน และสถานะ (`waiting` หรือ `started`)
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    def join_lobby(request):
        """ตรวจสอบ PIN เพื่อเข้าร่วม Lobby"""
        if request.method == "POST":
            pin = request.POST.get('pin', '').strip()
            # ค้นหาทัวร์นาเมนต์จาก PIN
            tournament = Tournament.objects.filter(pin_code=pin).first()
            
            if tournament.status not in ['waiting', 'open']:
                messages.error(request, "This tournament is not accepting participants.")
                return redirect('tournaments:join_lobby')
            
            # ส่งไปหน้ากรอกชื่อเล่น (Nickname)
            return redirect('tournaments:join_lobby_confirm', pk=tournament.pk)
        return render(request, 'tournaments/join_lobby_pin.html')

    def participant_status(request, pk):
        """API สำหรับ Polling รายชื่อผู้เข้าร่วม"""
        tournament = get_object_or_404(Tournament, pk=pk)
        participants = tournament.participants.all()
        
        # ส่งข้อมูลกลับเป็น JSON
        return JsonResponse({
            'status': tournament.status,
            'participant_count': participants.count(),
            'participants': participants_data, # List of nicknames
            'redirect_url': redirect_url, # URL สำหรับ Redirect เมื่อเริ่มเกม
        })
    ```

#### **5. SD-05: ระบบโหวตและการแข่งขัน (Gameplay & Voting Logic)**
*   **ฟังก์ชัน (API):** `vote_view` และ `next_match_api`
*   **คำอธิบาย (Goal):** จัดการการลงคะแนนแบบ Real-time และคำนวณผลแพ้ชนะเมื่อหมดเวลา
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **Receive Vote (AJAX):** รับค่า `choice` ('1' หรือ '2') ผ่าน AJAX POST
    2.  **Constraint Check:** ตรวจสอบ `unique_together` ในตาราง `MatchVote` เพื่อป้องกันการโหวตซ้ำ (ถ้าโหวตแล้วจะเป็นการอัปเดตแทน)
    3.  **Update Score:** บันทึกคะแนนลงฐานข้อมูล
    4.  **Timer Logic:** เมื่อเวลาหมด Frontend จะเรียก API เพื่อขอข้อมูลแมตช์ถัดไป
    5.  **Determine Winner:** Server คำนวณคะแนนรวม อัปเดตผู้ชนะ (`winner_id`) ในตาราง Match และส่งข้อมูล JSON ของแมตช์คู่ถัดไปกลับมา
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    @require_POST
    def vote_submit(request, pk):
        """บันทึกคะแนนโหวต (AJAX)"""
        # ... (Get tournament & match logic) ...
        
        # ใช้ update_or_create เพื่อป้องกันการโหวตซ้ำ (ถ้ามีแล้ว = แก้ไข)
        vote_obj, created = MatchVote.objects.update_or_create(
            match=current_match,
            user=request.user,
            defaults={'choice': choice}
        )
        
        return JsonResponse({'success': True, 'created': created, 'choice': choice})

    def vote_update(request, pk):
        """API ตรวจสอบสถานะแมตช์และเวลา (Polling)"""
        # ... (Calculate votes & percentages) ...
        
        # คำนวณเวลาถอยหลัง (Server-side Timer)
        if current_match.started_at:
            elapsed = (timezone.now() - current_match.started_at).total_seconds()
            time_remaining = max(0, tournament.voting_duration_seconds - int(elapsed))
            
            # AUTO-FINISH Logic: เมื่อเวลาหมดและแมตช์ยังไม่จบ
            if time_remaining <= 0 and not current_match.is_finished:
                # คำนวณหาผู้ชนะจากผลโหวตสูงสุด
                winner = current_match.competitor1 if votes_c1 > votes_c2 else current_match.competitor2
                current_match.winner = winner
                current_match.is_finished = True
                current_match.save()
                
                return JsonResponse({'status': 'finished', ...})
                
        return JsonResponse({ 'match': { ... }, 'time_remaining': time_remaining })
    ```

#### **6. SD-06: การจัดการผู้ใช้โดยผู้ดูแลระบบ (Admin User Management)**
*   **ฟังก์ชัน (View):** `admin_ban_user`
*   **คำอธิบาย (Goal):** ผู้ดูแลระบบสามารถระงับการใช้งานบัญชีสมาชิกที่ทำผิดกฎ
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **Permission Check:** ตรวจสอบสิทธิ์ด้วย Decorator `@admin_required` (ต้องเป็น is_staff=True)
    2.  **Retrieve User:** ดึงข้อมูล User เป้าหมายจาก ID
    3.  **Update Status:** แก้ไขสถานะ `is_active` เป็น `False` (ทำให้ล็อกอินไม่ได้)
    4.  **Log Action:** สร้างบันทึกในตาราง `AuditLog` ระบุว่าใครเป็นคนแบน และแบนใคร
    5.  **Redirect:** กลับไปยังหน้า Dashboard
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    @admin_required
    def admin_ban_user(request, pk):
        if request.method == 'POST':
            user = get_object_or_404(User, pk=pk)
            
            # ป้องกันการแบน Superuser
            if user.is_superuser:
                return redirect('custom_admin:user_list')
            
            # ปรับสถานะเป็น Inactive
            user.is_active = False
            user.save()
            
            # บันทึก Audit Log เพื่อตรวจสอบย้อนหลัง
            AuditLog.objects.create(
                user=request.user,
                action='BAN',
                target_model='User',
                details=f'Banned user: {user.username} (ID: {pk})',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f'User "{user.username}" has been banned.')
        
        return redirect('custom_admin:user_list')
    ```

#### **7. SD-07: การจัดการเนื้อหาโดยผู้ดูแลระบบ (Admin Content Management)**
*   **ฟังก์ชัน (View):** `admin_delete_tournament`
*   **คำอธิบาย (Goal):** ผู้ดูแลระบบสามารถลบทัวร์นาเมนต์ที่ไม่เหมาะสมออกจากระบบ
*   **ขั้นตอนการทำงาน (Logic):**
    1.  **Permission Check:** ตรวจสอบสิทธิ์ Admin
    2.  **Retrieve & Delete:** ดึงข้อมูล Tournament และสั่ง `delete()`
    3.  **Cascade Delete:** ระบบ Django จะลบข้อมูลที่เกี่ยวข้องทั้งหมด (Matches, Comments, Competitors) ให้อัตโนมัติ (CASCADE)
    4.  **Cleanup Files:** Library `django-cleanup` จะลบไฟล์รูปภาพออกจาก Server เพื่อคืนพื้นที่
    5.  **Log Action:** บันทึกการลบลงใน `AuditLog`
*   **ตัวอย่างโค้ด (Implementation):**
    ```python
    @admin_required
    def admin_delete_tournament(request, pk):
        if request.method == 'POST':
            tournament = get_object_or_404(Tournament, pk=pk)
            name = tournament.name
            
            # บันทึก Audit Log ก่อนลบ
            AuditLog.objects.create(
                user=request.user,
                action='DELETE',
                target_model='Tournament',
                details=f'Deleted tournament: {name} (ID: {pk})',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # ลบ Tournament (Django Cascade จะลบข้อมูลลูกให้อัตโนมัติ)
            tournament.delete()
            messages.success(request, f'Tournament "{name}" has been deleted.')
        
        return redirect('custom_admin:tournament_list')
    ```

### 4.3.3 การสร้างและจัดการฟอร์มด้วย Django Forms (Forms.py)

Django Forms ช่วยลดความซับซ้อนในการจัดการ HTML Form และการตรวจสอบข้อมูล (Validation) โดยในระบบนี้ใช้ `ModelForm` เพื่อเชื่อมโยง Form เข้ากับ Model โดยตรง

**ตัวอย่าง 1: TournamentForm (tournaments/forms.py)**
ใช้สำหรับสร้างและแก้ไขทัวร์นาเมนต์ โดยมีการกำหนด Widget เพื่อปรับแต่ง CSS Classes ให้เข้ากับธีม

```python
class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "description", "category", "language", "thumbnail", "bracket_size", "voting_duration_seconds"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bh-input', 'placeholder': 'Enter tournament name'}),
            'description': forms.Textarea(attrs={'class': 'bh-textarea', 'rows': 4}),
            # ...
        }
```

**ตัวอย่าง 2: CustomSignUpForm (accounts/forms.py)**
ขยายความสามารถจาก `UserCreationForm` เดิมของ Django เพื่อเพิ่มการรับค่า Email (ซึ่งปกติ Django UserCreationForm ไม่บังคับ)

```python
class CustomSignUpForm(UserCreationForm):
    # เพิ่ม Field Email เข้ามาในฟอร์มสมัครสมาชิก
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

---

## 4.4 การจัดการรูปแบบและการออกแบบ (Theming)

### 4.4.1 การบูรณาการ CSS Frameworks (Tailwind CSS & FontAwesome)

เพื่อการออกแบบ UI ที่ทันสมัยและตอบสนองได้ดี (Responsive) ระบบเลือกใช้ **Tailwind CSS** ผ่าน CDN และกำหนด Configuration Script ในส่วน `<head>` ของ `base.html` เพื่อ Custom ธีมสีให้เป็นเอกลักษณ์ (Dark Gaming Theme)

```html
<!-- Tailwind CSS Setup -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          slate: { 850: '#1a2234', 950: '#0a0f1a' }, # Custom Dark Backgrounds
          primary: '#667eea',                        # Brand Color
        }
      }
    }
  }
</script>
```

นอกจากนี้ยังมีการใช้ **Font Awesome v6.5** เพื่อแสดงผลไอคอนต่างๆ ในระบบ เช่น ถ้วยรางวัล (trophy), มงกุฎ (crown), และโล่ป้องกัน (shield)

### 4.4.2 การใช้ Template Inheritance และการสร้าง Reusable Components

เพื่อลดความซ้ำซ้อนของโค้ด HTML ระบบใช้ฟีเจอร์ Template Inheritance ของ Django:

1.  **Base Template (`base.html`):** เป็นไฟล์แม่แบบหลักที่ประกอบด้วยโครงสร้าง HTML, Header, Footer, และการโหลด CSS/JS
2.  **Content Block (`{% block content %}`):** พื้นที่สำหรับแทรกเนื้อหาของแต่ละหน้า
3.  **Child Templates:** หน้าเว็บอื่นๆ (เช่น `tournament_list.html`) จะสืบทอดจาก `base.html` โดยใช้คำสั่ง `{% extends 'base.html' %}` และเขียนเนื้อหาเฉพาะส่วนลงใน Block

**ตัวอย่างโครงสร้างไฟล์ base.html:**
```html
<!doctype html>
<html lang="en">
<head>
    <title>{% block title %}BattleHub{% endblock %}</title>
    <!-- Load CSS/JS here -->
</head>
<body class="bg-slate-950 text-gray-200">
    <!-- Navbar (Reusable) -->
    {% include 'navbar.html' %} 

    <!-- Main Content Area -->
    <main>
        {% if messages %} ... {% endif %} <!-- Flash Messages -->
        
        {% block content %}
        <!-- เนื้อหาแต่ละหน้าจะถูกแทรกตรงนี้ -->
        {% endblock %}
    </main>

    <!-- Footer (Reusable) -->
    <footer>...</footer>
</body>
</html>
```
