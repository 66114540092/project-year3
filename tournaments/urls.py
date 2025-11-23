from django.urls import path
from . import views

app_name = "tournaments"

urlpatterns = [
    path("", views.tournament_list, name="tournament_list"),
    path("create/", views.tournament_create, name="tournament_create"),
    path("<int:pk>/", views.tournament_detail, name="tournament_detail"),
    path("<int:pk>/edit/", views.tournament_update, name="tournament_update"),
    path("<int:pk>/delete/", views.tournament_delete, name="tournament_delete"),

    path("<int:pk>/competitors/", views.add_competitors, name="add_competitors"),
    path("<int:pk>/publish/", views.publish_tournament, name="publish"),

    path("<int:pk>/play/", views.play, name="play"),
    path("<int:pk>/match/<int:match_id>/finish/", views.finish_match, name="finish_match"),

    path("<int:pk>/summary/", views.summary, name="summary"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
]
