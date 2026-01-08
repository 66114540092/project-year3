# Chapter 3: System Design

## 3.1 System Architecture

BattleHub utilizes a modern containerized architecture designed for scalability and ease of deployment. The system follows a multi-tier architecture pattern with clear separation of concerns.

### Architecture Flow

```
User (Browser) → Nginx (Reverse Proxy) → Docker Container (Gunicorn/Django) → SQLite Database
```

**Component Description:**

1. **Client Layer (Browser):** Users access the application through modern web browsers. The frontend is built with HTML5, Tailwind CSS, and vanilla JavaScript for interactive features like real-time voting updates via AJAX polling.

2. **Web Server Layer (Nginx):** Nginx serves as a reverse proxy, handling incoming HTTP requests on port 80. It efficiently serves static files (CSS, JS, images) and forwards dynamic requests to the application server.

3. **Application Layer (Gunicorn/Django):** The Django framework runs under Gunicorn WSGI server inside a Docker container. This layer handles:
   - User authentication and session management
   - Business logic for tournament creation and voting
   - API endpoints for AJAX requests
   - Template rendering

4. **Database Layer (SQLite):** Data persistence is managed through SQLite database, storing user accounts, tournaments, competitors, votes, and match results.

### Tech Stack Revision Log

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 1.0 | January 2026 | Changed database from PostgreSQL to SQLite | Deployment agility - SQLite provides simpler setup for Version 1.0 without requiring separate database container configuration. This allows for rapid prototyping and easier data portability during the initial development phase. |

> **Note:** Future versions may migrate to PostgreSQL for improved concurrent write performance and advanced query capabilities as the user base grows.

---

## 3.2 System Requirements

### 3.2.1 Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-01 | User Authentication | Users can register, login, and logout. Password security with Django's built-in validators. |
| FR-02 | Tournament Creation | Members can create knockout-style tournaments with customizable bracket sizes (2, 4, 8, 16 participants). |
| FR-03 | Bulk Image Upload | Support for uploading multiple competitor images simultaneously with drag-and-drop interface. |
| FR-04 | Real-time Voting | AJAX-based voting system that updates vote counts without page refresh using polling mechanism. |
| FR-05 | Tournament Progression | Automatic advancement of winners to next rounds until champion is declared. |
| FR-06 | Winner Animation | Visual celebration animation displayed when tournament concludes. |
| FR-07 | Admin Dashboard | Administrative interface for monitoring system statistics, managing users, and overseeing tournaments. |
| FR-08 | Comment System | Users can leave comments on tournament pages. |

### 3.2.2 Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Response Time | Page load time < 2 seconds under normal conditions |
| NFR-02 | Security | CSRF protection on all forms, secure password hashing (PBKDF2) |
| NFR-03 | Responsive Design | UI adapts to desktop, tablet, and mobile screen sizes |
| NFR-04 | Browser Compatibility | Support for Chrome, Firefox, Safari, Edge (latest 2 versions) |
| NFR-05 | Availability | System designed to run continuously via Docker with auto-restart |

---

## 3.3 UI Design

### Design Philosophy: Dark Gaming Theme

BattleHub employs a "Dark Gaming Theme" interface designed to create an immersive, competitive atmosphere that appeals to the gaming community.

**Key Design Elements:**

1. **Color Palette:**
   - Primary Background: Deep slate (#0a0f1a) - reduces eye strain during extended use
   - Accent Colors: Blue (#3b82f6) and Purple (#8b5cf6) gradients - energetic, tournament feel
   - Text: Light gray (#e5e7eb) - high contrast for readability

2. **Visual Features:**
   - Glassmorphism effects on cards and modals
   - Glow effects (box-shadow) on interactive elements
   - Gradient buttons with hover animations
   - Trophy icons and gaming-inspired iconography (Font Awesome)

3. **Layout Principles:**
   - Card-based design for tournament listings
   - Grid layout for competitor display during voting
   - Responsive navigation with user dropdown menu

4. **Interaction Feedback:**
   - Hover effects with smooth transitions
   - Loading states during AJAX operations
   - Toast notifications for user actions

*(Wireframe images to be inserted)*

---

## 3.4 Use Case Diagram

### Actors

| Actor | Description |
|-------|-------------|
| Guest | Unauthenticated visitor who can view public content |
| Member | Registered user who can create and participate in tournaments |
| Admin | System administrator with full management capabilities |

### Use Cases by Actor

**Guest:**
- UC-01: View tournament list
- UC-02: View tournament details
- UC-03: Register account
- UC-04: Login

**Member (includes Guest capabilities):**
- UC-05: Create tournament
- UC-06: Upload competitors (bulk)
- UC-07: Publish tournament
- UC-08: Vote in tournaments
- UC-09: Post comments
- UC-10: View profile
- UC-11: Edit profile
- UC-12: Change password
- UC-13: Logout

**Admin (includes Member capabilities):**
- UC-14: Access admin dashboard
- UC-15: View system statistics
- UC-16: Manage all tournaments
- UC-17: Delete any tournament
- UC-18: View user list

---

## 3.5 Class Diagram

### Django Models Overview

```
┌─────────────────┐       ┌─────────────────┐
│      User       │       │    Profile      │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │──1:1──│ id (PK)         │
│ username        │       │ user_id (FK)    │
│ email           │       │ avatar          │
│ password        │       │ bio             │
│ is_staff        │       └─────────────────┘
│ date_joined     │
└─────────────────┘
        │
        │ 1:N (created_by)
        ▼
┌─────────────────┐       ┌─────────────────┐
│   Tournament    │       │      Tag        │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │──M:N──│ id (PK)         │
│ name            │       │ name            │
│ description     │       │ label           │
│ thumbnail       │       └─────────────────┘
│ bracket_size    │
│ status          │
│ created_by (FK) │
│ created_at      │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│   Competitor    │
├─────────────────┤
│ id (PK)         │
│ tournament (FK) │
│ name            │
│ image           │
│ created_at      │
└─────────────────┘
        │
        │ Referenced in Match
        ▼
┌─────────────────┐       ┌─────────────────┐
│     Match       │       │      Vote       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │──1:N──│ id (PK)         │
│ tournament (FK) │       │ match_id (FK)   │
│ round_number    │       │ user_id (FK)    │
│ competitor_a(FK)│       │ competitor (FK) │
│ competitor_b(FK)│       │ created_at      │
│ winner (FK)     │       └─────────────────┘
│ votes_a         │
│ votes_b         │
│ is_finished     │
└─────────────────┘
```

### Model Relationships

- **User ↔ Profile:** One-to-One (Django signals auto-create profile)
- **User → Tournament:** One-to-Many (user creates multiple tournaments)
- **Tournament → Competitor:** One-to-Many (tournament has multiple competitors)
- **Tournament ↔ Tag:** Many-to-Many (categorization)
- **Tournament → Match:** One-to-Many (tournament contains multiple matches)
- **Match → Vote:** One-to-Many (match receives multiple votes)

---

## 3.6 Sequence Diagram

### Real-time Voting Process

```
User          Browser/JS        Django View       Database
 │                │                  │                │
 │  Click Vote    │                  │                │
 │───────────────>│                  │                │
 │                │  AJAX POST       │                │
 │                │  /vote/{match}/  │                │
 │                │─────────────────>│                │
 │                │                  │  Check User    │
 │                │                  │  Session       │
 │                │                  │───────────────>│
 │                │                  │<───────────────│
 │                │                  │                │
 │                │                  │  Record Vote   │
 │                │                  │───────────────>│
 │                │                  │<───────────────│
 │                │                  │                │
 │                │                  │  Update Count  │
 │                │                  │───────────────>│
 │                │                  │<───────────────│
 │                │                  │                │
 │                │  JSON Response   │                │
 │                │  {votes_a, votes_b, winner}       │
 │                │<─────────────────│                │
 │                │                  │                │
 │  Update UI     │                  │                │
 │  (Vote Counts) │                  │                │
 │<───────────────│                  │                │
 │                │                  │                │
 │      [Loop every 3 seconds]       │                │
 │                │  AJAX GET        │                │
 │                │  /match-status/  │                │
 │                │─────────────────>│                │
 │                │  JSON (latest)   │                │
 │                │<─────────────────│                │
 │  Auto-refresh  │                  │                │
 │<───────────────│                  │                │
```

### Process Description

1. **Vote Submission:** User clicks on a competitor's image to vote
2. **AJAX Request:** JavaScript sends POST request to `/vote/{match_id}/`
3. **Server Processing:** Django view validates session, creates Vote record, updates match counts
4. **Response:** JSON response containing updated `votes_a`, `votes_b`, and `winner` (if determined)
5. **UI Update:** JavaScript updates vote count display without page reload
6. **Polling:** `setInterval` polls `/match-status/` every 3 seconds for real-time updates from other users

---

## 3.7 Data Model / Entity Model

### Entity-Relationship Diagram

| Entity | Attributes | Keys |
|--------|------------|------|
| **User** | id, username, email, password, is_staff, is_active, date_joined | PK: id |
| **Profile** | id, user_id, avatar, bio | PK: id, FK: user_id → User |
| **Tournament** | id, name, description, thumbnail, bracket_size, status, created_by, created_at | PK: id, FK: created_by → User |
| **Tag** | id, name, label | PK: id |
| **TournamentTag** | tournament_id, tag_id | FK: tournament_id → Tournament, FK: tag_id → Tag |
| **Competitor** | id, tournament_id, name, image, created_at | PK: id, FK: tournament_id → Tournament |
| **Match** | id, tournament_id, round_number, competitor_a, competitor_b, winner, votes_a, votes_b, is_finished | PK: id, FKs: tournament_id, competitor_a, competitor_b, winner |
| **Vote** | id, match_id, user_id, competitor_id, created_at | PK: id, FKs: match_id, user_id, competitor_id |
| **MatchComment** | id, match_id, user_id, text, created_at | PK: id, FKs: match_id, user_id |

### Cardinality Summary

- User (1) ─── creates ───> (N) Tournament
- Tournament (1) ─── contains ───> (N) Competitor
- Tournament (1) ─── has ───> (N) Match
- Match (1) ─── receives ───> (N) Vote
- User (1) ─── casts ───> (N) Vote
