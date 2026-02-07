from django.urls import path
from . import views

app_name = "tournaments"

urlpatterns = [
    path("", views.tournament_list, name="tournament_list"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("create/", views.tournament_create, name="tournament_create"),
    path("<int:pk>/", views.tournament_detail, name="tournament_detail"),
    path("<int:pk>/edit/", views.tournament_update, name="tournament_update"),
    path("<int:pk>/delete/", views.tournament_delete, name="tournament_delete"),

    path("<int:pk>/competitors/", views.add_competitors, name="add_competitors"),
    path("<int:pk>/publish/", views.publish_tournament, name="publish"),

    path("<int:pk>/play/", views.play, name="play"),
    path("<int:pk>/match/<int:match_id>/finish/", views.finish_match, name="finish_match"),

    path("<int:pk>/summary/", views.summary, name="summary"),
    path("<int:pk>/bracket/", views.bracket_transition, name="bracket_transition"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
    
    # AJAX endpoints for real-time play
    path("<int:pk>/api/vote-update/", views.vote_update, name="vote_update"),
    path("<int:pk>/api/vote-submit/", views.vote_submit, name="vote_submit"),
    
    # Live comments during match
    path("<int:pk>/api/match/<int:match_id>/comments/", views.get_match_comments, name="get_match_comments"),
    path("<int:pk>/api/match/<int:match_id>/comments/post/", views.post_match_comment, name="post_match_comment"),
    path("<int:pk>/api/comments/<int:comment_id>/report/", views.report_match_comment, name="report_comment"),
    path("<int:pk>/api/tournament-comments/<int:comment_id>/report/", views.report_tournament_comment, name="report_tournament_comment"),
    
    # Lobby System
    path("join/", views.join_lobby, name="join_lobby"),
    path("<int:pk>/join/", views.join_lobby_confirm, name="join_lobby_confirm"),
    path("<int:pk>/lobby/", views.waiting_lobby, name="waiting_lobby"),
    path("<int:pk>/open-lobby/", views.open_lobby, name="open_lobby"),
    path("<int:pk>/start/", views.start_tournament, name="start_tournament"),
    path("<int:pk>/api/participants/", views.participant_status, name="participant_status"),
]
