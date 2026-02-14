@startuml sequence_legend_samples

skinparam defaultFontName "Tahoma"
skinparam shadowing false
skinparam backgroundColor White
skinparam sequence {
    ArrowColor #333333
    LifeLineBorderColor #555555
    ParticipantBackgroundColor #E3F2FD
    ParticipantBorderColor #1565C0
}

' 1. Alt / Else Fragment
alt เงื่อนไข (Condition)
    :Do something;
else อื่นๆ (Else)
    :Do other thing;
end

' 2. Opt Fragment
opt ทางเลือก (Option)
    :Do optional thing;
end

' 3. Loop Fragment
loop วนซ้ำ (Loop)
    :Repeat task;
end

' 4. Ref Fragment
ref over : อ้างอิง (Reference)

@enduml
