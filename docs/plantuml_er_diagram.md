# 3.7 แบบจำลองข้อมูล (Data Model)

แบบจำลองข้อมูลแสดงโครงสร้างการจัดเก็บข้อมูลในระบบจัดการฐานข้อมูล (Database Schema) โดยระบบ BattleHub ใช้ฐานข้อมูลเชิงสัมพันธ์ (Relational Database) ในการจัดเก็บข้อมูล ซึ่งประกอบด้วยตาราง (Entities) และความสัมพันธ์ (Relationships) ดังแสดงในแผนภาพ Entity Relationship Diagram (ERD)

---

## 3.7.1 Entity Relationship Diagram (ERD)

```plantuml
@startuml ER_Diagram

' Hide the spot
hide circle

' Avoid problems with angled crows feet
skinparam linetype ortho

skinparam class {
    BackgroundColor White
    BorderColor #333333
    ArrowColor #333333
}

' ============================================================
'  Auth & Accounts
' ============================================================

entity "auth_user" as User {
    *id : integer <<PK>>
    --
    username : varchar(150)
    email : varchar(254)
    password : varchar(128)
    first_name : varchar(150)
    last_name : varchar(150)
    is_active : boolean
    is_staff : boolean
    is_superuser : boolean
    date_joined : datetime
    last_login : datetime
}

entity "accounts_profile" as Profile {
    *id : integer <<PK>>
    --
    *user_id : integer <<FK>>
    avatar : varchar(100)
    bio : text
    created_at : datetime
    updated_at : datetime
}

' ============================================================
'  Tournaments App
' ============================================================

entity "tournaments_tournament" as Tournament {
    *id : integer <<PK>>
    --
    name : varchar(200)
    description : text
    category : varchar(100)
    thumbnail : varchar(100)
    bracket_size : integer
    voting_duration_seconds : integer
    pin_code : varchar(6)
    status : varchar(20)
    current_round : integer
    *created_by_id : integer <<FK>>
    created_at : datetime
    updated_at : datetime
}

entity "tournaments_competitor" as Competitor {
    *id : integer <<PK>>
    --
    *tournament_id : integer <<FK>>
    name : varchar(200)
    image : varchar(100)
    created_at : datetime
}

entity "tournaments_match" as Match {
    *id : integer <<PK>>
    --
    *tournament_id : integer <<FK>>
    round_number : integer
    index_in_round : integer
    *competitor1_id : integer <<FK>>
    *competitor2_id : integer <<FK>>
    winner_id : integer <<FK, Nullable>>
    is_finished : boolean
    started_at : datetime
    created_at : datetime
}

entity "tournaments_matchvote" as MatchVote {
    *id : integer <<PK>>
    --
    *match_id : integer <<FK>>
    *user_id : integer <<FK>>
    choice : varchar(2)
    created_at : datetime
}

entity "tournaments_comment" as Comment {
    *id : integer <<PK>>
    --
    *tournament_id : integer <<FK>>
    *user_id : integer <<FK>>
    text : text
    created_at : datetime
}

entity "tournaments_matchcomment" as MatchComment {
    *id : integer <<PK>>
    --
    *match_id : integer <<FK>>
    *user_id : integer <<FK>>
    text : varchar(200)
    created_at : datetime
}

entity "tournaments_participant" as Participant {
    *id : integer <<PK>>
    --
    *tournament_id : integer <<FK>>
    user_id : integer <<FK, Nullable>>
    nickname : varchar(50)
    session_key : varchar(100)
    joined_at : datetime
}

' ============================================================
'  Custom Admin App
' ============================================================

entity "custom_admin_report" as Report {
    *id : integer <<PK>>
    --
    *reporter_id : integer <<FK>>
    reason : text
    status : varchar(20)
    target_user_id : integer <<FK, Nullable>>
    target_tournament_id : integer <<FK, Nullable>>
    target_match_comment_id : integer <<FK, Nullable>>
    target_tournament_comment_id : integer <<FK, Nullable>>
    admin_note : text
    created_at : datetime
    updated_at : datetime
}

entity "custom_admin_auditlog" as AuditLog {
    *id : integer <<PK>>
    --
    *user_id : integer <<FK>>
    action : varchar(50)
    target_model : varchar(50)
    details : text
    ip_address : varchar(39)
    created_at : datetime
}

' ============================================================
'  Relationships (Crow's Foot Notation)
' ============================================================

' User 1 -- 1 Profile
User ||..|| Profile

' User 1 -- N Many
User ||..o{ Tournament
User ||..o{ MatchVote
User ||..o{ Comment
User ||..o{ MatchComment
User ||..o{ Participant
User ||..o{ Report
User ||..o{ AuditLog

' Tournament 1 -- N Many
Tournament ||..|{ Competitor
Tournament ||..|{ Match
Tournament ||..o{ Comment
Tournament ||..o{ Participant

' Match 1 -- N Many
Match ||..o{ MatchVote
Match ||..o{ MatchComment

' Competitor 1 -- N Match (Competing)
Competitor }|..o{ Match

' Report N -- 1 Target (Zero or One)
Report }o..o| User
Report }o..o| Tournament
Report }o..o| Comment
Report }o..o| MatchComment

@enduml
```

(รูปที่ 3.12 แผนภาพความสัมพันธ์ของข้อมูล Entity Relationship Diagram)

คำอธิบายแผนภาพ:
จากภาพที่ 3.12 แสดงโครงสร้างความสัมพันธ์ของตารางในฐานข้อมูล โดยมีตาราง `auth_user` เป็นศูนย์กลาง เชื่อมโยงกับตารางอื่น ๆ ดังนี้:
1.  **Users & Profiles**: `auth_user` มีความสัมพันธ์แบบ One-to-One กับ `accounts_profile` เพื่อเก็บข้อมูลเพิ่มเติมของผู้ใช้
2.  **Tournaments System**:
    *   `tournaments_tournament` ถูกสร้างโดย User และประกอบด้วย `tournaments_competitor` (ผู้เข้าแข่งขัน)
    *   `tournaments_match` เก็บข้อมูลการจับคู่แข่งขัน เชื่อมโยงกับ Competitor 2 คน (คู่แข่ง) และ 1 คน (ผู้ชนะ)
    *   `tournaments_matchvote` เก็บคะแนนโหวต เชื่อมโยง User กับ Match (User 1 คน โหวตได้ 1 ครั้งต่อ Match)
    *   `tournaments_participant` เก็บข้อมูลผู้เข้าร่วม Lobby
3.  **Social Interactions**:
    *   `tournaments_comment` เก็บความคิดเห็นในทัวร์นาเมนต์
    *   `tournaments_matchcomment` เก็บแชทสดในแมตช์
4.  **Admin & Moderation**:
    *   `custom_admin_report` เก็บข้อมูลการรายงาน เชื่อมโยงกับ User (ผู้แจ้ง) และเป้าหมายปลายทาง (User, Tournament, Comment, Chat) ผ่าน Nullable Foreign Keys
    *   `custom_admin_auditlog` บันทึกประวัติการกระทำของผู้ดูแลระบบ

---

## 3.7.2 พจนานุกรมข้อมูล (Data Dictionary)

รายละเอียดโครงสร้างตาราง (Table Schema) ของระบบ BattleHub มีดังนี้

### 1. ตาราง auth_user (Users)
ตารางจัดเก็บข้อมูลบัญชีผู้ใช้งานระบบ (Default Django User Model)

| Field Name | Data Type | Key | Description |
| :--- | :--- | :--- | :--- |
| id | Integer | PK | รหัสประจำตัวผู้ใช้งาน (Auto Increment) |
| username | Varchar(150) | UQ | ชื่อผู้ใช้งาน (Unique) |
| email | Varchar(254) | | อีเมลผู้ใช้งาน |
| password | Varchar(128) | | รหัสผ่าน (Hashed) |
| is_active | Boolean | | สถานะบัญชี (True=ปกติ, False=ระงับการใช้งาน) |
| is_staff | Boolean | | สิทธิ์ผู้ดูแลระบบ (True=Admin) |
| date_joined | Datetime | | วันที่สมัครสมาชิก |

### 2. ตาราง tournaments_tournament (Tournaments)
ตารางจัดเก็บข้อมูลทัวร์นาเมนต์

| Field Name | Data Type | Key | Description |
| :--- | :--- | :--- | :--- |
| id | Integer | PK | รหัสทัวร์นาเมนต์ |
| name | Varchar(200) | | ชื่อทัวร์นาเมนต์ |
| category | Varchar(100) | | หมวดหมู่ (Anime, Game, etc.) |
| bracket_size | Integer | | จำนวนผู้เข้าแข่งขัน (2, 4, 8, 16) |
| status | Varchar(20) | | สถานะ (draft, waiting, open, finished) |
| pinning_code | Varchar(6) | | รหัส PIN 6 หลักสำหรับเข้าร่วม Lobby |
| created_by_id | Integer | FK | รหัสผู้สร้างทัวร์นาเมนต์ (Ref: auth_user) |
| created_at | Datetime | | วันที่สร้าง |

### 3. ตาราง tournaments_match (Matches)
ตารางจัดเก็บข้อมูลแมตช์การแข่งขัน

| Field Name | Data Type | Key | Description |
| :--- | :--- | :--- | :--- |
| id | Integer | PK | รหัสแมตช์ |
| tournament_id | Integer | FK | รหัสทัวร์นาเมนต์ (Ref: tournaments_tournament) |
| round_number | Integer | | รอบที่แข่งขัน (1, 2, 3...) |
| index_in_round | Integer | | ลำดับแมตช์ในรอบนั้น |
| competitor1_id | Integer | FK | ผู้เข้าแข่งขันฝ่ายที่ 1 (Ref: tournaments_competitor) |
| competitor2_id | Integer | FK | ผู้เข้าแข่งขันฝ่ายที่ 2 (Ref: tournaments_competitor) |
| winner_id | Integer | FK | ผู้ชนะในแมตช์นั้น (Nullable) |
| is_finished | Boolean | | สถานะจบการแข่งขัน |

*(เนื้อหาตารางอื่น ๆ ละไว้ในฐานที่เข้าใจ หรือสามารถเพิ่มเติมได้ตามต้องการ)*
