# Lab 3: Design Diagrams (BattleHub)

This document contains the Class Diagram and Data Flow Diagrams (DFD) for the BattleHub project.

## 1. Class Diagram

This diagram represents the database schema and relationships between models, grouped by their respective Django Apps.

```mermaid
classDiagram
    %% Relationships
    User "1" -- "1" Profile : has
    User "1" -- "*" Tournament : creates
    User "1" -- "*" Comment : writes
    User "1" -- "*" MatchVote : casts
    User "1" -- "*" Participant : joins as
    
    Tournament "*" -- "*" Tag : categorized by
    Tournament "1" -- "*" Competitor : contains
    Tournament "1" -- "*" Match : organizes
    Tournament "1" -- "*" Comment : has
    Tournament "1" -- "*" Participant : has players

    Match "1" -- "2" Competitor : features
    Match "1" -- "1" Competitor : winner
    Match "1" -- "*" MatchVote : receives
    Match "1" -- "*" MatchComment : has chat

    Participant "1" -- "0..1" User : linked to

    namespace Accounts_App {
        class User {
            +username
            +email
            +password
        }
        class Profile {
            +avatar
            +bio
            +created_at
        }
    }

    namespace Tournaments_App {
        class Tournament {
            +name
            +description
            +category
            +language
            +bracket_size
            +status
            +pin_code
            +is_ready()
        }
        class Tag {
            +name
            +slug
        }
        class Competitor {
            +name
            +image
        }
        class Match {
            +round
            +is_finished
            +votes_for_c1()
            +votes_for_c2()
        }
        class MatchVote {
            +choice
            +created_at
        }
        class Participant {
            +nickname
            +session_id
        }
        class Comment {
            +text
        }
        class MatchComment {
            +message
            +nickname
        }
    }
```

## 2. Data Flow Diagram (DFD)

### Level 0: Context Diagram

Overview of the system and its interactions with external entities.

```mermaid
flowchart TD
    User([User / Player])
    Creator([Tournament Creator])
    System(BattleHub System)

    %% Admin Flow
    Creator -->|1. Create Tournament| System
    Creator -->|2. Manage Matches| System
    System -->|Tournament Status| Creator

    %% User Flow
    User -->|3. Join via PIN| System
    User -->|4. Vote & Comment| System
    System -->|Live Updates| User

    style System fill:#f9f,stroke:#333,stroke-width:2px,color:black
    style User fill:#fff,stroke:#333
    style Creator fill:#fff,stroke:#333
```

### Level 1: System Processes

Detailed breakdown with clear separation of layers to minimize overlapping lines.

```mermaid
flowchart TD
    %% 1. Actors Layer
    subgraph Actors [External Entities]
        direction LR
        User([User])
        Creator([Creator])
    end

    %% 2. Process Layer
    subgraph System [BattleHub Core Processes]
        direction TB
        
        %% Auth
        P1(1. Authentication)
        
        %% Tournament Mgmt
        subgraph AdminFeatures [Tournament Management]
            P2(2. Create/Edit)
            P3(3. Match Control)
        end
        
        %% Live Interaction
        subgraph Interaction [Live Tournament]
            P4(4. Join Lobby)
            P5(5. Voting & Chat)
        end
    end

    %% 3. Data Layer
    subgraph Data [Data Storage]
        DB[(Database)]
    end

    %% --- Flows ---
    
    %% Auth Flow
    User --> P1
    Creator --> P1
    P1 -->|Verify Creds| DB
    
    %% Admin Flows
    Creator -->|Create| P2
    Creator -->|Start Match| P3
    P2 -->|Save Tourn| DB
    P3 -->|Update Match| DB
    
    %% User Flows
    User -->|PIN Code| P4
    User -->|Vote Choice| P5
    
    %% Data Flows
    DB -->|Tourn Info| P4
    DB -->|Match State| P5
    P4 -->|Add Participant| DB
    P5 -->|Save Vote| DB
    
    %% Internal
    P3 -.->|Trigger Round| P5
    
    %% Styling
    style DB fill:#eee,stroke:#333,stroke-width:4px
    style Actors fill:#fff,stroke:#000
    style System fill:#f0f8ff,stroke:#666,stroke-dasharray: 5 5
```

### Note
- **Design Improvement**: Uses Top-Down (TD) layout with subgraphs to organize the flow from Actors down to the Database, reducing intersecting lines.
