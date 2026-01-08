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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bh-input', 'placeholder': 'Enter tournament name'}),
            'description': forms.Textarea(attrs={'class': 'bh-textarea', 'rows': 4, 'placeholder': 'Describe your tournament...'}),
            'category': forms.Select(attrs={'class': 'bh-select'}),
            'language': forms.TextInput(attrs={'class': 'bh-input', 'placeholder': 'e.g. English, Thai'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'bh-input'}),
            'bracket_size': forms.Select(attrs={'class': 'bh-select'}),
            'voting_duration_seconds': forms.NumberInput(attrs={'class': 'bh-input', 'placeholder': '60'}),
        }


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
