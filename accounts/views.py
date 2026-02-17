# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomSignUpForm, ProfileUpdateForm, ProfileForm
from .models import Profile
from django.contrib.auth import login

def signup_view(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tournaments:tournament_list")
    else:
        form = CustomSignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_view(request):
    """User profile page"""
    from tournaments.models import Tournament
    
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    user_tournaments = Tournament.objects.filter(created_by=request.user).order_by('-created_at')[:6]
    # Stats
    from tournaments.models import Tournament, Participant, MatchVote
    
    total_created = Tournament.objects.filter(created_by=request.user).count()
    total_participants = Participant.objects.filter(tournament__created_by=request.user).count()
    total_votes = MatchVote.objects.filter(match__tournament__created_by=request.user).count()

    return render(request, "accounts/profile.html", {
        "profile_user": request.user,
        "profile": profile,
        "user_tournaments": user_tournaments,
        "total_created": total_created,
        "total_participants": total_participants,
        "total_votes": total_votes,
    })


@login_required
def edit_profile_view(request):
    """Edit user profile - update email, avatar, bio"""
    from tournaments.models import Tournament
    
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:profile")
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })
