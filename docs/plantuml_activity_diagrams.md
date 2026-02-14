# BattleHub — Activity Diagrams (รวมตามหมวด)

ก็อปทั้ง block ไปวางที่ [plantuml.com](https://www.plantuml.com/plantuml/uml/) ได้เลย — ได้ภาพเดียวต่อหมวด

---

## 1. Activity Diagram: Guest (UC-01 ถึง UC-06)

```plantuml
@startuml AD_Guest_All

skinparam defaultFontName "Tahoma"
skinparam shadowing false
skinparam backgroundColor White
skinparam activity {
    BackgroundColor #E3F2FD
    BorderColor #1565C0
}

|Guest|
start

:Open BattleHub Website;

fork

    |Guest|
    :== UC-01: View Tournament List ==;
    :Browse /tournaments/;
    :System loads tournaments\n(status: open/finished)\nsorted by newest;
    :Display tournament cards;

fork again

    |Guest|
    :== UC-02: Search & Filter ==;
    :Enter keyword or select\ncategory/status filter;
    :System filters results;
    if (Results found?) then (yes)
        :Display matching cards;
    else (no)
        :Display "No tournaments found";
    endif

fork again

    |Guest|
    :== UC-03: View Tournament Detail ==;
    :Click tournament card;
    :System loads detail\n(description, competitors, comments);
    :Display detail page;

fork again

    |Guest|
    :== UC-04: View Leaderboard ==;
    :Open /leaderboard/;
    :System ranks users by\ntournament count;
    :Display ranking table;

end fork

|Guest|
if (Want to interact?) then (yes)

    if (Has account?) then (no)
        :== UC-05: Register ==;
        :Fill registration form\n(username, email, password);
        :System validates data;
        if (Valid?) then (yes)
            :Create user + profile;
            :Redirect to login;
        else (no)
            :Display errors;
            stop
        endif
    else (yes)
    endif

    :== UC-06: Login ==;
    :Enter username + password;
    :System verifies credentials;
    if (Valid?) then (yes)
        if (Account active?) then (yes)
            :Create session;
            :Redirect as Member;
        else (banned)
            :Display "Account banned";
            stop
        endif
    else (no)
        :Display "Invalid credentials";
        stop
    endif

else (no)
    :Continue browsing as Guest;
endif

stop

@enduml
```

---

## 2. Activity Diagram: Member (UC-07 ถึง UC-25)

```plantuml
@startuml AD_Member_All

skinparam defaultFontName "Tahoma"
skinparam shadowing false
skinparam backgroundColor White
skinparam activity {
    BackgroundColor #E8F5E9
    BorderColor #2E7D32
}

start

:Member is logged in;

split

    :== UC-08: Edit Profile ==;
    :Update username, email,\nbio, avatar;
    :System validates + saves;

split again

    :== UC-07: Logout ==;
    :Click Logout;
    :Destroy session;
    :Return to Guest;
    stop

split again

    :== Tournament Creation Flow ==;

    :== UC-09: Create Tournament ==;
    :Fill form (name, desc, category,\nbracket_size, vote_duration, thumbnail);
    :System saves as "Draft";

    :== UC-12: Upload Competitors ==;
    repeat
        :Upload images + enter names;
        :System saves competitors;
        if (Want to remove?) then (yes)
            :== UC-13: Delete Competitor ==;
            :Remove selected competitor;
        else (no)
        endif
    repeat while (Count < bracket_size?) is (yes)

    :== UC-10: Edit Tournament ==;
    note right : Optional: edit details\nbefore publishing

    :== UC-14: Open Lobby ==;
    :Generate PIN Code;
    :Status: "Draft" -> "Waiting";

    :== UC-11: Delete Tournament ==;
    note right : Optional: can delete\nat any point if owner

    :== UC-18: Open Lobby ==;
    :Generate 6-digit PIN;
    :Status: "Open" -> "Waiting";

    :== UC-19: Start Tournament ==;
    :Owner clicks "Start";
    :Status: "Waiting" -> "Open";
    :First match activated;

split again

    :== Join Tournament Flow ==;

    :== UC-15: Join via PIN ==;
    :Enter 6-digit PIN;
    :System validates PIN;

    :== UC-16: Enter Nickname ==;
    :Enter display nickname;
    :System saves participant;

    :== UC-17: Wait in Lobby ==;
    :Wait for owner to start;
    :Auto-redirect when started;

end split

:== Voting Phase ==;

repeat
    :== UC-20: Vote for Competitor ==;
    :Display match (A vs B)\n+ countdown timer;
    :Member votes for one competitor;
    :System saves vote;
    :Timer expires -> count votes;
    :Winner determined;

    :== UC-21: View Live Bracket ==;
    note right : Optional: view bracket\nduring tournament

    :== UC-22: Live Chat ==;
    note right : Optional: chat with\nother participants

repeat while (More matches?) is (yes)

:== UC-23: View Summary ==;
:Status: "Open" -> "Finished";
:Display champion + statistics;

:== UC-24: Comment on Tournament ==;
note right : Optional: leave comment\non tournament page

:== UC-25: Report Content ==;
note right : Optional: report\ninappropriate comment

stop

@enduml
```

---

## 3. Activity Diagram: Admin (UC-26 ถึง UC-35)

```plantuml
@startuml AD_Admin_All

skinparam defaultFontName "Tahoma"
skinparam shadowing false
skinparam backgroundColor White
skinparam activity {
    BackgroundColor #FCE4EC
    BorderColor #C62828
}

start

:Admin logs in (is_staff = true);

:== UC-26: View Dashboard ==;
:Display stats cards\n(users, tournaments, reports);
:Display recent activity table;

split

    :== User Management ==;

    :== UC-27: Manage Users ==;
    :View all users list;

    if (Action needed?) then (Ban/Unban)
        :== UC-28: Ban / Unban User ==;
        :Toggle user is_active;
        :Save to Audit Log;
    elseif (Delete) then
        :== UC-29: Delete User ==;
        if (Target is superuser?) then (no)
            :Delete user + CASCADE data;
            :Save to Audit Log;
        else (yes)
            :Deny: cannot delete superuser;
        endif
    else (no action)
    endif

split again

    :== Tournament Management ==;

    :== UC-30: Moderate Tournaments ==;
    :View all tournaments list;

    if (Action needed?) then (Force Finish)
        :== UC-31: Force Finish ==;
        :Set status = "finished";
        :Save to Audit Log;
    elseif (Delete Comment) then
        :== UC-34: Delete Comment ==;
        :Remove inappropriate comment;
        :Save to Audit Log;
    else (no action)
    endif

split again

    :== Report Management ==;

    :== UC-32: Manage Reports ==;
    :View all reports\n(filter by status);

    :== UC-33: Resolve / Dismiss ==;
    if (Decision?) then (Resolve)
        :Set status = "resolved";
        :Save to Audit Log;
    else (Dismiss)
        :Set status = "dismissed";
        :Save to Audit Log;
    endif

end split

:== UC-35: View Audit Logs ==;
:Review all admin actions\n(who, what, when);

stop

@enduml
```
