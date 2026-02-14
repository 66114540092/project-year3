@startuml BattleHub_UseCase_Diagram
' ============================================================
'  BattleHub - Use Case Diagram (Final Version)
'  Online Tournament & Voting System
' ============================================================

left to right direction
skinparam packageStyle rectangle
skinparam defaultFontName "Tahoma"
skinparam shadowing false
skinparam backgroundColor White

skinparam usecase {
    BackgroundColor #FAFAFA
    BorderColor #333333
    FontSize 11
}

skinparam actor {
    FontSize 12
    FontStyle bold
}

' ============================================================
'  Actors (Outside System Boundary)
' ============================================================
actor "Guest" as Guest
actor "Member" as Member
actor "Admin" as Admin

Guest <|-- Member
Member <|-- Admin

' ============================================================
'  System Boundary
' ============================================================
rectangle "BattleHub System" {

    ' --- Public ---
    usecase "(UC-01)\nView Tournament List" as UC01
    usecase "(UC-02)\nSearch & Filter" as UC02
    usecase "(UC-03)\nView Tournament Detail" as UC03
    usecase "(UC-04)\nView Leaderboard" as UC04
    usecase "(UC-05)\nRegister" as UC05
    usecase "(UC-06)\nLogin" as UC06

    ' --- Member ---
    usecase "(UC-07)\nLogout" as UC07
    usecase "(UC-08)\nEdit Profile" as UC08
    usecase "(UC-09)\nCreate Tournament" as UC09
    usecase "(UC-10)\nEdit Tournament" as UC10
    usecase "(UC-11)\nDelete Tournament" as UC11
    usecase "(UC-12)\nUpload Competitors" as UC12
    usecase "(UC-13)\nDelete Competitor" as UC13
    usecase "(UC-14)\nPublish Tournament" as UC14
    usecase "(UC-15)\nJoin via PIN" as UC15
    usecase "(UC-16)\nEnter Nickname" as UC16
    usecase "(UC-17)\nWait in Lobby" as UC17
    usecase "(UC-18)\nOpen Lobby" as UC18
    usecase "(UC-19)\nStart Tournament" as UC19
    usecase "(UC-20)\nVote for Competitor" as UC20
    usecase "(UC-21)\nView Live Bracket" as UC21
    usecase "(UC-22)\nLive Chat" as UC22
    usecase "(UC-23)\nView Summary" as UC23
    usecase "(UC-24)\nComment on Tournament" as UC24
    usecase "(UC-25)\nReport Content" as UC25

    ' --- Admin ---
    usecase "(UC-26)\nView Dashboard" as UC26
    usecase "(UC-27)\nManage Users" as UC27
    usecase "(UC-28)\nBan / Unban User" as UC28
    usecase "(UC-29)\nDelete User" as UC29
    usecase "(UC-30)\nModerate Tournaments" as UC30
    usecase "(UC-31)\nForce Finish" as UC31
    usecase "(UC-32)\nManage Reports" as UC32
    usecase "(UC-33)\nResolve / Dismiss" as UC33
    usecase "(UC-34)\nDelete Comment" as UC34
    usecase "(UC-35)\nView Audit Logs" as UC35
}

' ============================================================
'  Actor Associations (Solid Line, No Arrows)
' ============================================================

' --- Guest (6 use cases) ---
Guest -- UC01
Guest -- UC02
Guest -- UC03
Guest -- UC04
Guest -- UC05
Guest -- UC06

' --- Member (14 use cases) ---
Member -- UC07
Member -- UC08
Member -- UC09
Member -- UC10
Member -- UC11
Member -- UC12
Member -- UC15
Member -- UC18
Member -- UC20
Member -- UC21
Member -- UC22
Member -- UC23
Member -- UC24
Member -- UC25

' --- Admin (5 use cases) ---
Admin -- UC26
Admin -- UC27
Admin -- UC30
Admin -- UC32
Admin -- UC35

' ============================================================
'  <<include>> (Mandatory - MUST happen every time)
' ============================================================
UC15 ..> UC16 : <<include>>
UC16 ..> UC17 : <<include>>

' ============================================================
'  <<extend>> (Optional - MAY happen additionally)
' ============================================================
UC09 <.. UC14 : <<extend>>
UC12 <.. UC13 : <<extend>>
UC18 <.. UC19 : <<extend>>
UC27 <.. UC28 : <<extend>>
UC27 <.. UC29 : <<extend>>
UC30 <.. UC31 : <<extend>>
UC30 <.. UC34 : <<extend>>
UC32 <.. UC33 : <<extend>>

@enduml