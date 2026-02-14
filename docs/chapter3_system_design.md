บทที่ 3
การออกแบบระบบ

3.1 สถาปัตยกรรมระบบ
ระบบ BattleHub ใช้สถาปัตยกรรมแบบ Containerized ผ่าน Docker เพื่อให้ง่ายต่อการ deploy และ scale ในอนาคต โดยแบ่งออกเป็น 3 ส่วนหลัก ได้แก่ Web Server, Application Server และ Database Server

โครงสร้างการทำงานของระบบมีลำดับดังนี้
ผู้ใช้ (Browser) → Nginx → Docker Container (Gunicorn/Django) → PostgreSQL

รายละเอียดแต่ละ Layer มีดังนี้
1) Client Layer คือส่วนที่ผู้ใช้เข้าถึงผ่าน Browser โดยหน้า Frontend ใช้ HTML5 สำหรับโครงสร้าง, Tailwind CSS สำหรับจัดรูปแบบ และ JavaScript สำหรับ AJAX polling เพื่อดึงข้อมูลแบบ real-time
2) Web Server Layer คือ Nginx ทำหน้าที่เป็น reverse proxy รับ request ที่ port 80 และส่งต่อไปยัง application server รวมถึงให้บริการ static files และ media files
3) Application Layer คือ Django framework ทำงานบน Gunicorn WSGI server ภายใน Docker container ทำหน้าที่จัดการเรื่อง authentication, business logic และ API endpoints
4) Database Layer คือ PostgreSQL ที่ทำหน้าที่เก็บข้อมูลผู้ใช้ ทัวร์นาเมนต์ ผู้เข้าแข่งขัน และผลโหวตทั้งหมด

(รูปที่ 3.1 แผนภาพสถาปัตยกรรมระบบ)

บันทึกการเปลี่ยนแปลง Tech Stack:
เวอร์ชัน 1.0 (มกราคม 2569) ได้ทำการเปลี่ยนจาก SQLite เป็น PostgreSQL เนื่องจาก PostgreSQL รองรับ concurrent users ได้ดีกว่าใน production environment โดยในช่วงพัฒนา local ยังคงใช้ SQLite เพื่อความสะดวก แต่ production ใช้ PostgreSQL ผ่าน Docker

3.2 ความต้องการของระบบ

3.2.1 ความต้องการด้านฟังก์ชัน (Functional Requirements)
FR-01 ระบบลงทะเบียนและเข้าสู่ระบบ
ผู้ใช้สามารถสมัครสมาชิก เข้าสู่ระบบ และออกจากระบบได้ โดยรหัสผ่านจะถูกเข้ารหัสด้วย PBKDF2

FR-02 สร้างทัวร์นาเมนต์
สมาชิกสามารถสร้างทัวร์นาเมนต์แบบ knockout ได้ โดยกำหนดขนาด bracket ได้ 2, 4, 8 หรือ 16 คน

FR-03 อัปโหลดผู้เข้าแข่งขัน
ระบบรองรับการอัปโหลดรูปหลายรูปพร้อมกัน (Bulk Upload) ผ่านการลากและวาง (Drag and Drop)

FR-04 ระบบโหวต real-time
ผู้ใช้โหวตแล้วเห็นผลทันทีผ่าน AJAX polling โดย browser จะดึงข้อมูลจาก server ทุก 3 วินาที

FR-05 ระบบ Admin Dashboard
ผู้ดูแลระบบสามารถดูสถิติภาพรวม จัดการทัวร์นาเมนต์ และจัดการผู้ใช้ได้

FR-06 ระบบ Kahoot-style Lobby
ผู้สร้างทัวร์นาเมนต์สามารถเปิดห้องรอ (Lobby) พร้อม PIN Code 6 หลัก ผู้เล่นสามารถเข้าร่วมด้วยการกรอก PIN และ Nickname โดย Host จะเห็นรายชื่อผู้เข้าร่วมแบบ Real-time

FR-07 ระบบ Timer แบบ Server-synced
ระบบมีนาฬิกานับถอยหลังที่ sync กับ Server ป้องกันผู้ใช้โกงเวลา เมื่อหมดเวลาระบบจะตัดสินผู้ชนะอัตโนมัติ

FR-08 ระบบ Toast Notifications
ระบบแจ้งเตือนแบบ Real-time เช่น "เหลือเวลา 10 วินาที", "หมดเวลา!", "มีผู้เล่นเข้าร่วม!" เพื่อเพิ่มประสบการณ์ผู้ใช้

FR-09 ระบบ Auto-redirect
เมื่อจบแมตช์หรือทัวร์นาเมนต์ ระบบจะเปลี่ยนหน้าอัตโนมัติไปยังหน้ารอบถัดไปหรือหน้าสรุปผล โดยไม่ต้องให้ผู้ใช้กด refresh


3.2.2 ความต้องการด้านอื่นๆ (Non-Functional Requirements)
NFR-01 ความเร็ว
ระบบต้องโหลดหน้าไม่เกิน 2 วินาที
NFR-02 ความปลอดภัย
ระบบต้องมี CSRF protection ทุกฟอร์ม
NFR-03 Responsive Design
หน้าเว็บต้องใช้งานได้ทั้ง Desktop และ Mobile


3.3 การออกแบบ UI
ระบบใช้ธีม Dark Gaming Theme เพื่อให้เข้ากับบรรยากาศการแข่งขัน โดยมีหลักการออกแบบดังนี้
- สีพื้นหลังเข้ม (#0a0f1a) เพื่อลดความเมื่อยล้าสายตาเมื่อใช้งานนาน
- สี Accent ใช้ฟ้าและม่วง gradient เพื่อสร้างความรู้สึกตื่นเต้น เหมาะกับบรรยากาศการแข่งขัน
- มี glow effect และ animation เพิ่มความน่าสนใจ
- ใช้ Font Awesome icons ทั้งระบบเพื่อความสม่ำเสมอ

(รูปที่ 3.2 ตัวอย่างหน้าจอหลักของระบบ)


3.4 Use Case Diagram
ระบบมีผู้ใช้งาน 3 ประเภท ได้แก่
1) Guest คือผู้เยี่ยมชมที่ยังไม่ได้ login สามารถดูรายการทัวร์นาเมนต์ สมัครสมาชิก และเข้าสู่ระบบได้
2) Member คือสมาชิกที่ลงทะเบียนแล้ว สามารถสร้างทัวร์นาเมนต์ อัปโหลดผู้เข้าแข่งขัน โหวต และแก้ไขโปรไฟล์ได้
3) Admin คือผู้ดูแลระบบ สามารถดู Dashboard จัดการทัวร์นาเมนต์ และจัดการผู้ใช้ทั้งหมดได้

(รูปที่ 3.3 Use Case Diagram)


3.5 Class Diagram
แผนภาพคลาสของระบบ BattleHub ถูกจัดทำแยกเป็น 2 ส่วน ได้แก่ ฝั่ง Backend (Django Models, Views, Forms) และฝั่ง Frontend (HTML Templates, JavaScript Components)

3.5.1 Backend Class Diagram
ระบบฝั่ง Backend พัฒนาด้วย Django Framework แบ่งออกเป็น 3 Django App ดังนี้

3.5.1.1 Accounts App
รับผิดชอบระบบจัดการบัญชีผู้ใช้งาน ประกอบด้วย
- User (Django Built-in) เก็บข้อมูลบัญชีผู้ใช้ ประกอบด้วย id, username, email, password, is_active (สถานะบัญชี), is_staff (สิทธิ์ผู้ดูแล), date_joined
- Profile เก็บข้อมูลโปรไฟล์เพิ่มเติม ประกอบด้วย id, user (OneToOneField), avatar (ImageField), bio (TextField) มีความสัมพันธ์แบบ One-to-One กับ User ถูกสร้างอัตโนมัติผ่าน Django post_save signal เมื่อสมัครสมาชิก
- CustomSignUpForm สืบทอดจาก UserCreationForm เพิ่มช่อง email สำหรับสมัครสมาชิก
- ProfileUpdateForm ใช้แก้ไข email มี clean_email() ตรวจสอบ email ซ้ำ
- ProfileForm ใช้แก้ไข avatar และ bio
- AccountsViews ประกอบด้วย signup_view (สมัครสมาชิก), profile_view (ดูโปรไฟล์), edit_profile_view (แก้ไขโปรไฟล์)

(รูปที่ 3.4 แผนภาพคลาส Backend — Accounts App)

3.5.1.2 Tournaments App
เป็น App หลักและใหญ่ที่สุดของระบบ รับผิดชอบฟังก์ชันการทำงานทั้งหมดของทัวร์นาเมนต์ ประกอบด้วย
- Tournament เก็บข้อมูลทัวร์นาเมนต์ ประกอบด้วย id, name, description, category, thumbnail (ImageField), bracket_size (2, 4, 8 หรือ 16), voting_duration_seconds, pin_code (6 หลัก), status (draft, waiting, open, finished), current_round, created_by (FK → User) มีเมธอด total_rounds(), current_match(), is_ready_to_publish(), champion()
- Competitor เก็บข้อมูลผู้เข้าแข่งขัน ประกอบด้วย id, tournament (FK), name, image (ImageField) มีความสัมพันธ์แบบ Many-to-One กับ Tournament
- Match เก็บข้อมูลแมตช์ 1v1 ประกอบด้วย id, tournament (FK), round_number, index_in_round, competitor1 (FK), competitor2 (FK), winner (FK, nullable), is_finished, started_at มีเมธอด votes_for_competitor1(), votes_for_competitor2()
- MatchVote เก็บข้อมูลการโหวต ประกอบด้วย id, match (FK), user (FK), choice ('1' หรือ '2'), created_at มี unique_together constraint (match, user) ป้องกันโหวตซ้ำ แต่อนุญาตให้เปลี่ยนใจได้
- Comment เก็บความคิดเห็นในหน้ารายละเอียด ประกอบด้วย id, tournament (FK), user (FK), text (TextField), created_at
- MatchComment เก็บข้อความแชทสดระหว่างโหวต ประกอบด้วย id, match (FK), user (FK), text (varchar 200), created_at จำกัด 200 ตัวอักษร
- Participant เก็บข้อมูลผู้เข้าร่วม Lobby ประกอบด้วย id, tournament (FK), user (FK, nullable), nickname (varchar 50), session_key, joined_at มี unique_together constraint (tournament, user)
- TournamentForm ใช้สร้างและแก้ไขทัวร์นาเมนต์ (name, description, category, thumbnail, bracket_size, voting_duration_seconds)
- CompetitorForm ใช้อัปโหลดผู้เข้าแข่งขัน (name, image)
- CommentForm ใช้เขียนความคิดเห็น (text)
- TournamentViews จัดการ Server-Side Rendering 14 ฟังก์ชัน ได้แก่ tournament_list, tournament_detail, tournament_create, tournament_update, tournament_delete, add_competitors, delete_competitor, publish_tournament, play, finish_match, summary, bracket_transition, add_comment, leaderboard
- TournamentAPI จัดการ AJAX Endpoint 12 ฟังก์ชัน ได้แก่ vote_update, vote_submit, get_match_comments, post_match_comment, report_match_comment, report_tournament_comment, join_lobby, join_lobby_confirm, waiting_lobby, open_lobby, start_tournament, participant_status

(รูปที่ 3.5 แผนภาพคลาส Backend — Tournaments App)

3.5.1.3 Custom Admin App
รับผิดชอบระบบจัดการสำหรับผู้ดูแลระบบ ประกอบด้วย
- Report เก็บข้อมูลการรายงานปัญหา ประกอบด้วย id, reporter (FK → User), reason (TextField), status (pending, resolved, dismissed) รองรับ 4 ประเภทเป้าหมายผ่าน Nullable Foreign Key ได้แก่ target_user, target_match_comment, target_tournament_comment, target_tournament มี admin_note สำหรับบันทึกภายใน
- AuditLog เก็บประวัติการดำเนินการของผู้ดูแลระบบ ประกอบด้วย id, user (FK → Admin), action (varchar 50 เช่น BAN, DELETE, FORCE_FINISH), target_model (varchar 50), details (TextField), ip_address (GenericIPAddress), created_at
- AdminViews ประกอบด้วย 14 ฟังก์ชัน ได้แก่ admin_dashboard, admin_tournament_list, admin_user_list, admin_user_detail, admin_delete_tournament, admin_force_finish_tournament, admin_ban_user, admin_unban_user, admin_delete_user, admin_audit_logs, admin_reports, admin_resolve_report, admin_dismiss_report, admin_delete_comment ทุกฟังก์ชันถูกป้องกันด้วย @admin_required decorator ที่ตรวจสอบ is_staff = True

(รูปที่ 3.6 แผนภาพคลาส Backend — Custom Admin App)

(รูปที่ 3.7 แผนภาพคลาส Backend ภาพรวม — แสดงความเชื่อมโยงระหว่าง App)

3.5.2 Frontend Class Diagram
ระบบฝั่ง Frontend แบ่งออกเป็น 2 ส่วน ดังนี้

ส่วน Templates (HTML Pages)
- BasePage เป็น Template หลักที่ทุกหน้าสืบทอด ประกอบด้วย Navbar, Content Block, Footer และ Toast Container
- TournamentListPage หน้ารายการทัวร์นาเมนต์ มีช่องค้นหา ตัวกรองหมวดหมู่ ตัวกรองสถานะ และ Pagination
- TournamentDetailPage หน้ารายละเอียด แสดงข้อมูลทัวร์นาเมนต์ ตารางผู้เข้าแข่งขัน และส่วนความคิดเห็น
- CreateTournamentPage หน้าสร้างทัวร์นาเมนต์ มี Form และ Preview รูปปก
- AddCompetitorsPage หน้าอัปโหลดผู้เข้าแข่งขัน มี Progress Bar, Upload Area และปุ่ม Publish
- PlayPage หน้าโหวต เป็นหน้าที่ซับซ้อนที่สุด ใช้ JavaScript Component 4 ตัว ได้แก่ TimerComponent, VoteManager, LiveChatComponent, BracketRenderer
- LobbyPage หน้าห้องพักรอ แสดง PIN, รายชื่อผู้เข้าร่วม และปุ่มเริ่มแข่ง
- SummaryPage หน้าสรุปผล แสดงผู้ชนะเลิศและตารางผลทุกแมตช์
- AdminDashboardPage หน้าแดชบอร์ดผู้ดูแลระบบ ใช้ Template แยก (base_admin.html) มี Sidebar, Stats Cards และ Activity Table

ส่วน JavaScript Components
- TimerComponent จัดการตัวนับเวลาถอยหลัง มีเมธอด startCountdown(), stopCountdown(), onTimerExpire(), updateDisplay()
- VoteManager จัดการการลงคะแนนและอัปเดตแถบเปอร์เซ็นต์แบบ Real-time มีเมธอด submitVote(), fetchVoteUpdate(), updateVoteBar(), pollForUpdates()
- LiveChatComponent จัดการแชทสดระหว่างโหวต มีเมธอด sendMessage(), fetchMessages(), appendMessage(), startPolling(), stopPolling()
- LobbyPoller ตรวจสอบสถานะห้องพักรอทุก 3 วินาที มีเมธอด fetchParticipantStatus(), updateParticipantList(), checkTournamentStarted(), redirectToPlay()
- AJAXClient คลาสกลางสำหรับเรียก API ผ่าน HTTP มีเมธอด get(), post(), getCookie() จัดการ CSRF Token อัตโนมัติ
- ToastManager จัดการข้อความแจ้งเตือนแบบ Pop-up มีเมธอด showSuccess(), showError(), showWarning(), autoDismiss()
- BracketRenderer วาดสายการแข่งขันในรูปแบบแผนผัง Tournament Bracket มีเมธอด renderBracket(), highlightCurrentMatch(), updateMatchResult()

ทุก Component ที่สื่อสารกับ Backend ใช้ AJAXClient เป็นตัวกลาง TimerComponent มีความสัมพันธ์เชิง Trigger กับ VoteManager เมื่อเวลาหมดลง

(รูปที่ 3.8 แผนภาพคลาส Frontend)


3.6 Sequence Diagram
แผนภาพลำดับของระบบ BattleHub แสดงขั้นตอนการทำงานของระบบเมื่อผู้ใช้งานดำเนินกิจกรรมต่าง ๆ โดยแบ่งตามบทบาท 3 กลุ่ม ทุกคลาสที่ปรากฏในแผนภาพลำดับอ้างอิงจากแผนภาพคลาสในหัวข้อ 3.5

3.6.1 Sequence Diagram ส่วนผู้ใช้งานทั่วไป (Guest Flow)
เมื่อผู้เยี่ยมชมเปิดหน้ารายการทัวร์นาเมนต์ TournamentListPage ส่ง Request ไปยัง TournamentViews ซึ่งดึงข้อมูลจาก Tournament Model เฉพาะสถานะ open และ finished ผู้เยี่ยมชมสามารถค้นหาและกรองด้วยคำค้น หมวดหมู่ และสถานะ รวมถึงดูรายละเอียดทัวร์นาเมนต์ผ่าน TournamentDetailPage
การสมัครสมาชิกใช้ CustomSignUpForm ตรวจสอบความถูกต้อง เมื่อผ่านจะสร้าง User และ Profile ถูกสร้างอัตโนมัติผ่าน Django Signal จากนั้นสร้าง Session และเข้าสู่ระบบทันที
การเข้าสู่ระบบตรวจสอบข้อมูลยืนยันตัวตนผ่าน Django Authentication โดยมี 3 ผลลัพธ์ คือ สำเร็จ ข้อมูลไม่ถูกต้อง และบัญชีถูกระงับ

(รูปที่ 3.9 Sequence Diagram ส่วนผู้ใช้งานทั่วไป)

3.6.2 Sequence Diagram ส่วนสมาชิก (Member Flow)
ส่วนนี้เป็นหัวใจหลักของระบบ BattleHub ครอบคลุม 10 Use Case หลัก ดังนี้
1) สร้างทัวร์นาเมนต์ — สมาชิกกรอกข้อมูลผ่าน CreateTournamentPage โดย TournamentForm ตรวจสอบความถูกต้อง ระบบสร้าง Tournament ในสถานะ "Draft"
2) อัปโหลดผู้เข้าแข่งขัน — อัปโหลดรูปภาพผ่าน CompetitorForm ระบบแสดง Progress Bar ติดตามจำนวน เมื่อครบตาม bracket_size ปุ่ม Publish จะแสดง
3) Publish — ระบบสุ่มลำดับผู้เข้าแข่งขันและสร้าง Match objects สำหรับทุกรอบ เปลี่ยนสถานะเป็น "Open"
4) เปิด Lobby — ระบบสร้าง PIN 6 หลัก เปลี่ยนสถานะเป็น "Waiting"
5) เข้าร่วมด้วย PIN — ผู้เข้าร่วมกรอก PIN และชื่อเล่น ระบบสร้าง Participant
6) รอใน Lobby — LobbyPoller ใช้ AJAXClient ส่ง Request ไปยัง TournamentAPI ทุก 3 วินาทีเพื่ออัปเดตรายชื่อแบบ Real-time
7) เริ่มการแข่งขัน — Host กดเริ่ม LobbyPoller ตรวจพบการเปลี่ยนแปลงสถานะและ redirect ทุกคนไปหน้าโหวต
8) โหวต — PlayPage เริ่มต้น TimerComponent, VoteManager, LiveChatComponent, BracketRenderer พร้อมกัน การโหวตส่งผ่าน AJAX MatchVote ใช้ unique_together ป้องกันโหวตซ้ำ แถบเปอร์เซ็นต์อัปเดตทุก 2 วินาที
9) แชทสด — ส่งข้อความผ่าน MatchComment Polling ทุก 2 วินาที
10) เมื่อ Timer หมด — ระบบเปรียบเทียบคะแนนและเดินเกมไปแมตช์ถัดไป รอบถัดไป หรือจบทัวร์นาเมนต์แล้วแสดง SummaryPage

(รูปที่ 3.10 Sequence Diagram ส่วนสมาชิก)

3.6.3 Sequence Diagram ส่วนผู้ดูแลระบบ (Admin Flow)
เมื่อผู้ดูแลระบบเปิดหน้า AdminDashboardPage ระบบตรวจสอบสิทธิ์ผ่าน @admin_required decorator ที่ตรวจสอบ is_staff = True จากนั้น AdminViews ดึงข้อมูลสถิติจาก User, Tournament, Report และ AuditLog
การระงับบัญชีดำเนินการโดยเปลี่ยน is_active ของ User เป็น False พร้อมตรวจสอบว่าไม่สามารถ Ban ตนเองหรือ Superuser ได้ การบังคับจบทัวร์นาเมนต์เปลี่ยนสถานะเป็น "finished"
การจัดการรายงานมี 2 ทางเลือก คือ Resolve (แก้ไขแล้ว) และ Dismiss (ปัดทิ้ง) ทุกการดำเนินการถูกบันทึกลง AuditLog โดยอัตโนมัติ ประกอบด้วยชื่อผู้ดำเนินการ ประเภทการกระทำ เป้าหมาย รายละเอียด และ IP Address เพื่อความโปร่งใสและตรวจสอบย้อนหลังได้

(รูปที่ 3.11 Sequence Diagram ส่วนผู้ดูแลระบบ)


3.7 Data Model
ระบบ BattleHub มีตารางในฐานข้อมูล PostgreSQL ดังนี้
- ตาราง auth_user (Django Built-in) เก็บข้อมูลผู้ใช้ มี id เป็น Primary Key
- ตาราง accounts_profile เก็บโปรไฟล์ มี user_id เป็น Foreign Key อ้างอิงไปยัง auth_user แบบ One-to-One
- ตาราง tournaments_tournament เก็บทัวร์นาเมนต์ มี created_by เป็น Foreign Key อ้างอิงไปยัง auth_user
- ตาราง tournaments_competitor เก็บผู้เข้าแข่งขัน มี tournament_id เป็น Foreign Key อ้างอิงไปยัง tournaments_tournament
- ตาราง tournaments_match เก็บแมตช์ มี Foreign Keys ได้แก่ tournament_id, competitor1_id, competitor2_id, winner_id
- ตาราง tournaments_matchvote เก็บการโหวต มี Foreign Keys ได้แก่ match_id, user_id พร้อม Unique Constraint (match_id, user_id)
- ตาราง tournaments_comment เก็บความคิดเห็น มี Foreign Keys ได้แก่ tournament_id, user_id
- ตาราง tournaments_matchcomment เก็บแชทสด มี Foreign Keys ได้แก่ match_id, user_id
- ตาราง tournaments_participant เก็บผู้เข้าร่วม Lobby มี Foreign Keys ได้แก่ tournament_id, user_id พร้อม Unique Constraint (tournament_id, user_id)
- ตาราง custom_admin_report เก็บรายงาน มี Nullable Foreign Keys ได้แก่ reporter_id, target_user_id, target_match_comment_id, target_tournament_comment_id, target_tournament_id
- ตาราง custom_admin_auditlog เก็บประวัติการดำเนินการ มี user_id เป็น Foreign Key อ้างอิงไปยัง auth_user

(รูปที่ 3.12 ER Diagram)
