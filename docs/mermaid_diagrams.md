# Mermaid Diagrams สำหรับบทที่ 3

## รูปที่ 3.1 แผนภาพสถาปัตยกรรมระบบ

```mermaid
flowchart LR
    subgraph Client
        A[ผู้ใช้ Browser]
    end
    
    subgraph Docker
        B[Nginx :80]
        C[Gunicorn/Django :8000]
        D[(PostgreSQL :5432)]
        E[Static Files]
        F[Media Files]
    end
    
    A -->|HTTP Request| B
    B -->|Proxy Pass| C
    C -->|Query| D
    C --> E
    C --> F
    B -->|Serve Static| E
    B -->|Serve Media| F
```


## รูปที่ 3.3 Use Case Diagram

```mermaid
flowchart TB
    subgraph Actors
        G((Guest))
        M((Member))
        AD((Admin))
    end
    
    subgraph "Use Cases"
        UC1[ดูรายการทัวร์นาเมนต์]
        UC2[สมัครสมาชิก]
        UC3[เข้าสู่ระบบ]
        UC4[สร้างทัวร์นาเมนต์]
        UC5[อัปโหลดผู้เข้าแข่งขัน]
        UC6[โหวต]
        UC7[แก้ไขโปรไฟล์]
        UC8[ดู Dashboard]
        UC9[จัดการทัวร์นาเมนต์]
        UC10[จัดการผู้ใช้]
    end
    
    G --> UC1
    G --> UC2
    G --> UC3
    
    M --> UC1
    M --> UC4
    M --> UC5
    M --> UC6
    M --> UC7
    
    AD --> UC1
    AD --> UC4
    AD --> UC8
    AD --> UC9
    AD --> UC10
```


## รูปที่ 3.4 Class Diagram

```mermaid
classDiagram
    User "1" -- "1" Profile : has
    User "1" -- "*" Tournament : creates
    Tournament "1" -- "*" Competitor : contains
    Tournament "1" -- "*" Match : has
    Match "1" -- "*" MatchVote : receives
    User "1" -- "*" MatchVote : casts
    
    class User {
        +int id
        +string username
        +string email
        +string password
        +bool is_staff
    }
    
    class Profile {
        +int id
        +int user_id
        +image avatar
        +text bio
    }
    
    class Tournament {
        +int id
        +string name
        +text description
        +string category
        +int bracket_size
        +string status
        +int current_round
        +int created_by
        +champion()
        +current_match()
    }
    
    class Competitor {
        +int id
        +int tournament_id
        +string name
        +image image
    }
    
    class Match {
        +int id
        +int tournament_id
        +int round_number
        +int index_in_round
        +int competitor1_id
        +int competitor2_id
        +int winner_id
        +bool is_finished
        +votes_for_competitor1()
        +votes_for_competitor2()
    }
    
    class MatchVote {
        +int id
        +int match_id
        +int user_id
        +string choice
    }
```


## รูปที่ 3.5 Sequence Diagram กระบวนการโหวต

```mermaid
sequenceDiagram
    participant U as ผู้ใช้
    participant B as Browser/JS
    participant D as Django View
    participant DB as PostgreSQL
    
    U->>B: คลิกโหวต
    B->>D: AJAX POST /vote/
    D->>DB: ตรวจสอบ MatchVote
    DB-->>D: ยังไม่เคยโหวต
    D->>DB: INSERT MatchVote
    DB-->>D: OK
    D-->>B: JSON response
    B-->>U: อัปเดต UI
    
    loop ทุก 3 วินาที
        B->>D: GET /match-status/
        D->>DB: SELECT votes
        DB-->>D: votes data
        D-->>B: JSON{votes_a, votes_b}
        B-->>U: อัปเดต vote count
    end
```


## รูปที่ 3.6 ER Diagram

```mermaid
erDiagram
    USER ||--|| PROFILE : has
    USER ||--o{ TOURNAMENT : creates
    USER ||--o{ MATCHVOTE : casts
    TOURNAMENT ||--o{ COMPETITOR : contains
    TOURNAMENT ||--o{ MATCH : has
    MATCH ||--o{ MATCHVOTE : receives
    MATCH }o--|| COMPETITOR : competitor1
    MATCH }o--|| COMPETITOR : competitor2
    MATCH }o--o| COMPETITOR : winner
    
    USER {
        int id PK
        string username
        string email
        string password
        bool is_staff
        datetime date_joined
    }
    
    PROFILE {
        int id PK
        int user_id FK
        image avatar
        text bio
    }
    
    TOURNAMENT {
        int id PK
        string name
        text description
        string category
        int bracket_size
        string status
        int current_round
        int created_by FK
        datetime created_at
    }
    
    COMPETITOR {
        int id PK
        int tournament_id FK
        string name
        image image
        datetime created_at
    }
    
    MATCH {
        int id PK
        int tournament_id FK
        int round_number
        int index_in_round
        int competitor1_id FK
        int competitor2_id FK
        int winner_id FK
        bool is_finished
    }
    
    MATCHVOTE {
        int id PK
        int match_id FK
        int user_id FK
        string choice
        datetime created_at
    }
```
