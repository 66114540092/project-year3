from django import forms
from .models import Tournament, Competitor, Comment


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            "name",
            "description",
            "category",
            "language",
            "thumbnail",
            "bracket_size",
            "voting_duration_seconds",
        ]


class CompetitorForm(forms.ModelForm):
    class Meta:
        model = Competitor
        fields = ["name", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Share your thoughts...",
                }
            )
        }
