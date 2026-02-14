from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .forms import TournamentForm, CompetitorForm, CommentForm
from .models import Tournament, Competitor, Match, MatchVote, Participant, generate_pin_code


from django.db.models import Q
from django.core.paginator import Paginator
from custom_admin.models import Report


def tournament_list(request):
    """
    Shows list of tournaments with Search & Filter
    """
    search_query = request.GET.get("search", "")
    selected_tag = request.GET.get("tag", "")
    selected_status = request.GET.get("status", "")

    tournaments = Tournament.objects.all().order_by('-created_at')

    # 1. Search
    if search_query:
        tournaments = tournaments.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # 2. Filter by Status
    if selected_status:
        tournaments = tournaments.filter(status=selected_status)

    # 3. Filter by Tag (Category)
    if selected_tag:
        tournaments = tournaments.filter(category=selected_tag)

    # 4. Get Categories from Model Choices (consistent with create form)
    all_tags = []
    for value, label in Tournament.CATEGORY_CHOICES:
        all_tags.append({
            'name': value,
            'label': label,
            'is_selected': (value == selected_tag)
        })

    # 5. Pagination
    paginator = Paginator(tournaments, 12)  # 12 items per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tournaments": page_obj,
        "page_obj": page_obj,
        "all_tags": all_tags,
        "search_query": search_query,
        "selected_tag": selected_tag,
        "selected_status": selected_status,
        # Status choices for template loop (avoiding == in template)
        "status_choices": [
            {"value": "draft", "label": "📝 Draft", "is_selected": selected_status == "draft"},
            {"value": "open", "label": "🔴 Live", "is_selected": selected_status == "open"},
            {"value": "finished", "label": "✅ Finished", "is_selected": selected_status == "finished"},
        ],
    }

    return render(
        request,
        "tournaments/tournament_list.html",
        context,
    )


def leaderboard(request):
    """Leaderboard page showing top voters, creators, and weekly highlights"""
    # Weekly timeframe
    one_week_ago = timezone.now() - timedelta(days=7)
    
    # Top Voters THIS WEEK (users who voted the most this week)
    top_voters = User.objects.filter(
        match_votes__created_at__gte=one_week_ago
    ).annotate(
        vote_count=Count('match_votes', filter=Q(match_votes__created_at__gte=one_week_ago))
    ).order_by('-vote_count')[:10]
    
    # Top Creators THIS WEEK (users who created tournaments this week)
    top_creators = User.objects.filter(
        created_tournaments__created_at__gte=one_week_ago
    ).annotate(
        tournament_count=Count('created_tournaments', filter=Q(created_tournaments__created_at__gte=one_week_ago))
    ).order_by('-tournament_count')[:10]
    
    # Weekly Stats
    weekly_finished = Tournament.objects.filter(
        status='finished',
        created_at__gte=one_week_ago
    ).count()
    
    weekly_votes = MatchVote.objects.filter(
        created_at__gte=one_week_ago
    ).count()
    
    weekly_new_users = User.objects.filter(
        date_joined__gte=one_week_ago
    ).count()
    
    # Hot Tournaments THIS WEEK (most votes this week)
    hot_tournaments = Tournament.objects.filter(
        status__in=['open', 'finished'],
        created_at__gte=one_week_ago
    ).annotate(
        total_votes=Count('matches__votes', filter=Q(matches__votes__created_at__gte=one_week_ago))
    ).order_by('-total_votes')[:5]
    
    # Recently Finished (this week)
    recently_finished = Tournament.objects.filter(
        status='finished',
        created_at__gte=one_week_ago
    ).order_by('-created_at')[:5]
    
    # Hall of Fame - ALL TIME (this stays as all-time for prestige)
    hall_of_fame = Competitor.objects.annotate(
        win_count=Count('wins')
    ).filter(win_count__gt=0).order_by('-win_count')[:10]
    
    context = {
        'top_voters': top_voters,
        'top_creators': top_creators,
        'weekly_finished': weekly_finished,
        'weekly_votes': weekly_votes,
        'weekly_new_users': weekly_new_users,
        'hot_tournaments': hot_tournaments,
        'recently_finished': recently_finished,
        'hall_of_fame': hall_of_fame,
    }
    
    return render(request, "tournaments/leaderboard.html", context)


def tournament_detail(request, pk):
    """หน้า detail รวมข้อมูล, competitor, comments, summary link"""
    tournament = get_object_or_404(Tournament, pk=pk)
    competitors = tournament.competitors.all()
    comments = tournament.comments.select_related("user")

    context = {
        "tournament": tournament,
        "competitors": competitors,
        "comments": comments,
        "comment_form": CommentForm(),
    }
    return render(request, "tournaments/tournament_detail.html", context)


@login_required
def tournament_create(request):
    if request.method == "POST":
        form = TournamentForm(request.POST, request.FILES)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.status = "draft"
            tournament.current_round = 1
            tournament.save()
            messages.success(request, "Tournament created. Now add competitors.")
            return redirect("tournaments:add_competitors", pk=tournament.pk)
    else:
        form = TournamentForm()

    return render(
        request,
        "tournaments/tournament_form.html",
        {"form": form, "title": "Create Tournament"},
    )


@login_required
def tournament_update(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = TournamentForm(request.POST, request.FILES, instance=tournament)
        if form.is_valid():
            form.save()
            messages.success(request, "Tournament updated.")
            return redirect("tournaments:tournament_detail", pk=tournament.pk)
    else:
        form = TournamentForm(instance=tournament)

    # If the tournament has been started (not draft), prevent changing bracket_size and voting duration
    try:
        if tournament.status != "draft":
            if "bracket_size" in form.fields:
                form.fields["bracket_size"].disabled = True
            if "voting_duration_seconds" in form.fields:
                form.fields["voting_duration_seconds"].disabled = True
    except Exception:
        # If form isn't initialized for some reason, skip disabling
        pass

    return render(
        request,
        "tournaments/tournament_form.html",
        {"form": form, "title": "Edit Tournament"},
    )


@login_required
def tournament_delete(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)
    if request.method == "POST":
        tournament.delete()
        messages.success(request, "Tournament deleted.")
        return redirect("tournaments:tournament_list")
    return render(
        request,
        "tournaments/tournament_confirm_delete.html",
        {"tournament": tournament},
    )


@login_required
def add_competitors(request, pk):
    """หน้าอัปโหลดรูปผู้เข้าแข่งขัน - supports bulk upload"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)

    if tournament.status != "draft":
        messages.info(request, "Tournament already published.")
        return redirect("tournaments:tournament_detail", pk=pk)

    if request.method == "POST":
        # Handle bulk upload
        images = request.FILES.getlist('images')
        names = request.POST.getlist('names')
        
        if images:
            # Calculate remaining slots
            current_count = tournament.competitors.count()
            remaining = tournament.bracket_size - current_count
            
            # Limit uploads to remaining slots
            images_to_add = images[:remaining]
            added_count = 0
            
            for i, image in enumerate(images_to_add):
                name = names[i] if i < len(names) else ""
                Competitor.objects.create(
                    tournament=tournament,
                    name=name.strip(),
                    image=image
                )
                added_count += 1
            
            if added_count > 0:
                messages.success(request, f"Added {added_count} competitor{'s' if added_count > 1 else ''}.")
            
            if len(images) > remaining:
                messages.warning(request, f"Only {remaining} slots were available. {len(images) - remaining} image(s) were not added.")
        else:
            messages.error(request, "Please select at least one image.")
        
        return redirect("tournaments:add_competitors", pk=tournament.pk)

    competitors = tournament.competitors.all()
    count = competitors.count()
    can_publish = tournament.is_ready_to_publish()

    return render(
        request,
        "tournaments/add_competitors.html",
        {
            "tournament": tournament,
            "competitors": competitors,
            "count": count,
            "can_publish": can_publish,
        },
    )


@login_required
def delete_competitor(request, pk, comp_id):
    """ลบผู้เข้าแข่งขันออกจาก tournament (ต้องเป็น draft เท่านั้น)"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)
    if tournament.status != "draft":
        messages.error(request, "Cannot delete competitors after tournament is published.")
        return redirect("tournaments:tournament_detail", pk=pk)
    competitor = get_object_or_404(Competitor, pk=comp_id, tournament=tournament)
    name = competitor.name or f"Competitor {comp_id}"
    competitor.delete()
    messages.success(request, f'Removed "{name}" from the tournament.')
    return redirect("tournaments:add_competitors", pk=pk)


@login_required
def publish_tournament(request, pk):
    """generate bracket + เปิด tournament"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)

    if tournament.status != "draft":
        messages.info(request, "Tournament already published.")
        return redirect("tournaments:tournament_detail", pk=pk)

    competitors = list(tournament.competitors.all())
    if len(competitors) != tournament.bracket_size:
        messages.error(
            request,
            f"You must have exactly {tournament.bracket_size} competitors to publish.",
        )
        return redirect("tournaments:add_competitors", pk=pk)

    # สร้างแมตช์รอบแรก (round 1)
    # จับคู่ทีละ 2 รูปตามลำดับ
    tournament.matches.all().delete()  # เคลียร์ bracket เดิมถ้ามี
    round_number = 1
    index = 1
    for i in range(0, len(competitors), 2):
        c1 = competitors[i]
        c2 = competitors[i + 1]
        Match.objects.create(
            tournament=tournament,
            round_number=round_number,
            index_in_round=index,
            competitor1=c1,
            competitor2=c2,
            is_finished=False,
        )
        index += 1

    tournament.status = "open"
    tournament.current_round = 1
    tournament.save()

    messages.success(request, "Tournament published. Ready to play.")
    return redirect("tournaments:play", pk=pk)


@login_required
def play(request, pk):
    """หน้าเล่น (current match 1v1 + โหวต)"""
    tournament = get_object_or_404(Tournament, pk=pk)

    if tournament.status == "finished":
        messages.info(request, "Tournament is finished.")
        return redirect("tournaments:summary", pk=pk)

    current_match = tournament.current_match()

    # ไม่มีแมตช์ active แล้ว แต่อาจมีรอบถัดไปที่ยังไม่สร้าง
    if not current_match:
        # เช็คว่า รอบนี้จบทุกแมตช์หรือยัง
        unfinished = tournament.matches.filter(
            round_number=tournament.current_round,
            is_finished=False,
        ).exists()

        if unfinished:
            # ยังมีแมตช์รออยู่แต่ข้อมูลเพี้ยน
            messages.error(request, "No active match but tournament not finished. Please check data.")
            return redirect("tournaments:tournament_detail", pk=pk)

        # ทุกแมตช์ในรอบนี้จบแล้ว → ถ้ามีรอบถัดไป ให้สร้าง
        if tournament.current_round < tournament.total_rounds:
            _create_next_round_matches(tournament)
            tournament.current_round += 1
            tournament.save()
            current_match = tournament.current_match()
        else:
            # ไม่มีรอบถัดไป → tournament จบ
            tournament.status = "finished"
            tournament.save()
            return redirect("tournaments:summary", pk=pk)

    # Set started_at if this is the first time someone accesses this match
    if current_match and not current_match.started_at:
        current_match.started_at = timezone.now()
        current_match.save(update_fields=['started_at'])

    # handle vote
    if request.method == "POST":
        choice = request.POST.get("choice")
        if choice not in ["1", "2"]:
            messages.error(request, "Invalid choice.")
            return redirect("tournaments:play", pk=pk)

        vote_obj, created = MatchVote.objects.get_or_create(
            match=current_match,
            user=request.user,
            defaults={"choice": choice},
        )
        if not created:
            vote_obj.choice = choice
            vote_obj.save()
            messages.success(request, "Your vote has been updated.")
        else:
            messages.success(request, "Your vote has been recorded.")

        return redirect("tournaments:play", pk=pk)

    # GET แสดงหน้าปัจจุบัน
    user_vote = None
    if request.user.is_authenticated and current_match:
        user_vote = MatchVote.objects.filter(
            match=current_match,
            user=request.user,
        ).first()

    context = {
        "tournament": tournament,
        "match": current_match,
        "user_vote": user_vote,
    }
    return render(request, "tournaments/play.html", context)


@login_required
def finish_match(request, pk, match_id):
    """ให้ creator กดปิดแมตช์ → เลือกผู้ชนะจากคะแนน และเดินเกมต่อ"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)
    match = get_object_or_404(Match, pk=match_id, tournament=tournament)

    if request.method != "POST":
        return redirect("tournaments:play", pk=pk)

    if match.is_finished:
        messages.info(request, "Match already finished.")
        return redirect("tournaments:play", pk=pk)

    votes1 = match.votes_for_competitor1()
    votes2 = match.votes_for_competitor2()

    if votes1 == votes2:
        # กรณีเสมอ: เอา competitor1 ชนะไปก่อน (ง่าย ๆ)
        winner = match.competitor1
    else:
        winner = match.competitor1 if votes1 > votes2 else match.competitor2

    match.winner = winner
    match.is_finished = True
    match.save()

    messages.success(request, f"Match finished. Winner: {winner.name or winner.pk}")
    
    # Check if all matches in current round are finished
    unfinished_in_round = tournament.matches.filter(
        round_number=tournament.current_round,
        is_finished=False
    ).exists()
    
    if not unfinished_in_round:
        # All matches in this round finished
        if tournament.current_round < tournament.total_rounds:
            # Create next round matches
            _create_next_round_matches(tournament)
            tournament.current_round += 1
            tournament.save()
        else:
            # Final round finished - tournament is done
            tournament.status = 'finished'
            tournament.save()
    
    # Check if tournament has only 1 round (2 competitors) - skip bracket view
    # Or if tournament is now finished
    next_match = tournament.current_match()
    if tournament.status == 'finished' or tournament.total_rounds <= 1 or not next_match:
        # For finished tournaments or 2-competitor tournaments, go directly to summary
        return redirect("tournaments:summary", pk=pk)
    
    # Otherwise show bracket transition for multi-round tournaments
    return redirect("tournaments:bracket_transition", pk=pk)


def _create_next_round_matches(tournament: Tournament):
    """สร้างแมตช์ของรอบถัดไปจาก winners ของรอบก่อนหน้า"""
    current_round = tournament.current_round
    next_round = current_round + 1

    # ดึงแมตช์ของ round ปัจจุบัน เรียงตาม index
    current_matches = tournament.matches.filter(
        round_number=current_round
    ).order_by("index_in_round")

    winners = []
    for m in current_matches:
        if m.winner:
            winners.append(m.winner)

    # ลบแมตช์ของ next_round ถ้ามีอยู่ก่อน
    tournament.matches.filter(round_number=next_round).delete()

    index = 1
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            c1 = winners[i]
            c2 = winners[i + 1]
        Match.objects.create(
            tournament=tournament,
            round_number=next_round,
            index_in_round=index,
            competitor1=c1,
            competitor2=c2,
            is_finished=False,
        )
        index += 1


def summary(request, pk):
    """หน้าสรุปผลทัวร์นาเมนต์"""
    tournament = get_object_or_404(Tournament, pk=pk)
    matches = tournament.matches.select_related(
        "competitor1", "competitor2", "winner"
    ).all()

    rounds = {}
    for m in matches:
        rounds.setdefault(m.round_number, []).append(m)

    champion = tournament.champion()

    import json
    from django.core.serializers.json import DjangoJSONEncoder

    # Serialize matches for JS consumption to avoid template tag issues
    matches_data = []
    for m in matches:
        matches_data.append({
            'round_number': m.round_number,
            'competitor1_name': m.competitor1.name if m.competitor1 else '?',
            'competitor2_name': m.competitor2.name if m.competitor2 else '?',
            'votes1': m.votes_for_competitor1(),
            'votes2': m.votes_for_competitor2(),
            'winner_name': m.winner.name if m.winner else None,
            'is_finished': m.is_finished,
        })
    
    # Calculate total votes server-side for robustness
    total_votes = sum(m.votes_for_competitor1() + m.votes_for_competitor2() for m in matches)

    return render(
        request,
        "tournaments/summary.html",
        {
            "tournament": tournament, 
            "rounds": rounds, 
            "champion": champion, 
            "matches_data": matches_data,
            "total_votes": total_votes
        },
    )


def bracket_transition(request, pk):
    """Bracket view transition page - shows bracket and auto-redirects to next match"""
    tournament = get_object_or_404(Tournament, pk=pk)
    
    # Check if we need to create next round matches
    next_match = tournament.current_match()
    
    if not next_match:
        # Check if current round is complete but tournament isn't finished
        all_current_round_finished = not tournament.matches.filter(
            round_number=tournament.current_round,
            is_finished=False
        ).exists()
        
        if all_current_round_finished and tournament.current_round < tournament.total_rounds:
            # Create next round matches
            _create_next_round_matches(tournament)
            tournament.current_round += 1
            tournament.save()
            next_match = tournament.current_match()
        elif all_current_round_finished:
            # Tournament is truly finished
            tournament.status = "finished"
            tournament.save()
            return redirect('tournaments:summary', pk=pk)
    
    # Get all matches for bracket display
    matches = tournament.matches.select_related(
        "competitor1", "competitor2", "winner"
    ).order_by("round_number", "index_in_round")

    # Group matches by round
    rounds = {}
    for m in matches:
        rounds.setdefault(m.round_number, []).append(m)

    context = {
        "tournament": tournament,
        "rounds": rounds,
        "next_match": next_match,
        "total_rounds": tournament.total_rounds,
    }
    return render(request, "tournaments/bracket_transition.html", context)


@login_required
def add_comment(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.tournament = tournament
            c.user = request.user
            c.save()
            messages.success(request, "Comment posted.")
    return redirect("tournaments:tournament_detail", pk=pk)


# AJAX Endpoints for Real-time Play Interface
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


def vote_update(request, pk):
    """AJAX endpoint to get current match state (votes, timer, status)"""
    tournament = get_object_or_404(Tournament, pk=pk)
    current_match = tournament.current_match()
    
    if not current_match:
        # No active match - determine where to redirect
        if tournament.status == 'finished':
            redirect_url = f'/tournaments/{pk}/summary/'
        else:
            # Tournament not finished but no current match = between matches
            # Redirect to bracket for multi-round or play for next match
            if tournament.total_rounds <= 1:
                redirect_url = f'/tournaments/{pk}/summary/'
            else:
                redirect_url = f'/tournaments/{pk}/bracket/'
        
        return JsonResponse({
            'status': tournament.status,
            'match': None,
            'redirect_url': redirect_url
        })
    
    # Get vote counts
    votes_c1 = current_match.votes.filter(choice='1').count()
    votes_c2 = current_match.votes.filter(choice='2').count()
    total_votes = votes_c1 + votes_c2
    
    # Calculate percentages
    pct_c1 = round((votes_c1 / total_votes * 100) if total_votes > 0 else 50)
    pct_c2 = 100 - pct_c1
    
    # Get user's current vote
    user_vote = None
    if request.user.is_authenticated:
        vote_obj = MatchVote.objects.filter(match=current_match, user=request.user).first()
        if vote_obj:
            user_vote = vote_obj.choice
    
    # Calculate server-side time remaining
    time_remaining = None
    if current_match.started_at:
        elapsed = (timezone.now() - current_match.started_at).total_seconds()
        time_remaining = max(0, tournament.voting_duration_seconds - int(elapsed))
        
        # AUTO-FINISH: If time has expired and match not finished, finish it now
        if time_remaining <= 0 and not current_match.is_finished:
            # Determine winner by votes
            if votes_c1 == votes_c2:
                winner = current_match.competitor1  # Tie-breaker: competitor1 wins
            else:
                winner = current_match.competitor1 if votes_c1 > votes_c2 else current_match.competitor2
            
            current_match.winner = winner
            current_match.is_finished = True
            current_match.save()
            
            # Check if all matches in current round are finished
            unfinished_in_round = tournament.matches.filter(
                round_number=tournament.current_round,
                is_finished=False
            ).exists()
            
            if not unfinished_in_round:
                # All matches in this round finished
                if tournament.current_round < tournament.total_rounds:
                    # Create next round matches
                    _create_next_round_matches(tournament)
                    tournament.current_round += 1
                    tournament.save()
                else:
                    # Final round finished - tournament is done
                    tournament.status = 'finished'
                    tournament.save()
            
            # Determine redirect URL
            if tournament.status == 'finished' or tournament.total_rounds <= 1:
                redirect_url = f'/tournaments/{pk}/summary/'
            else:
                redirect_url = f'/tournaments/{pk}/bracket/'
            
            return JsonResponse({
                'status': tournament.status,
                'match': None,
                'redirect_url': redirect_url,
                'time_remaining': 0
            })
    else:
        time_remaining = tournament.voting_duration_seconds
    
    return JsonResponse({
        'status': tournament.status,
        'match': {
            'id': current_match.id,
            'round': current_match.round_number,
            'is_finished': current_match.is_finished,
            'competitor1': {
                'id': current_match.competitor1.id,
                'name': current_match.competitor1.name,
                'image': current_match.competitor1.image.url if current_match.competitor1.image else None,
                'votes': votes_c1,
                'percentage': pct_c1,
            },
            'competitor2': {
                'id': current_match.competitor2.id,
                'name': current_match.competitor2.name,
                'image': current_match.competitor2.image.url if current_match.competitor2.image else None,
                'votes': votes_c2,
                'percentage': pct_c2,
            },
            'total_votes': total_votes,
        },
        'user_vote': user_vote,
        'time_remaining': time_remaining,
        'redirect_url': None
    })


@require_POST
def vote_submit(request, pk):
    """AJAX endpoint to submit/update vote"""
    tournament = get_object_or_404(Tournament, pk=pk)
    current_match = tournament.current_match()
    
    if not current_match or tournament.status == 'finished':
        return JsonResponse({'success': False, 'error': 'No active match'})
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Must be logged in'})
    
    try:
        data = json.loads(request.body)
        choice = data.get('choice')
    except:
        choice = request.POST.get('choice')
    
    if choice not in ['1', '2']:
        return JsonResponse({'success': False, 'error': 'Invalid choice'})
    
    vote_obj, created = MatchVote.objects.update_or_create(
        match=current_match,
        user=request.user,
        defaults={'choice': choice}
    )
    
    return JsonResponse({
        'success': True,
        'created': created,
        'choice': choice
    })


@login_required
def get_match_comments(request, pk, match_id):
    """AJAX endpoint to get live comments for a match"""
    from .models import MatchComment
    
    match = get_object_or_404(Match, pk=match_id, tournament_id=pk)
    
    # Get last_id from query params to only return new comments
    last_id = request.GET.get('last_id', 0)
    try:
        last_id = int(last_id)
    except:
        last_id = 0
    
    comments = match.live_comments.filter(id__gt=last_id).select_related('user')[:50]
    
    comments_data = []
    for c in comments:
        comments_data.append({
            'id': c.id,
            'username': c.user.username,
            'text': c.text,
            'time': c.created_at.strftime('%H:%M:%S')
        })
    
    return JsonResponse({
        'success': True,
        'comments': comments_data,
        'last_id': comments_data[-1]['id'] if comments_data else last_id
    })


@login_required
@require_POST
def post_match_comment(request, pk, match_id):
    """AJAX endpoint to post a live comment during match"""
    from .models import MatchComment
    
    match = get_object_or_404(Match, pk=match_id, tournament_id=pk)
    
    # Rate limiting: 1 comment per 3 seconds
    from django.utils import timezone
    from datetime import timedelta
    
    recent_comment = MatchComment.objects.filter(
        match=match,
        user=request.user,
        created_at__gte=timezone.now() - timedelta(seconds=3)
    ).first()
    
    if recent_comment:
        return JsonResponse({'success': False, 'error': 'Too fast! Wait 3 seconds.'})
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()[:200]  # Max 200 chars
    except:
        text = request.POST.get('text', '').strip()[:200]
    
    if not text:
        return JsonResponse({'success': False, 'error': 'Empty message'})
    
    comment = MatchComment.objects.create(
        match=match,
        user=request.user,
        text=text
    )
    
    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'username': request.user.username,
            'text': comment.text,
            'time': comment.created_at.strftime('%H:%M:%S')
        }
    })


@login_required
@require_POST
def report_match_comment(request, pk, comment_id):
    """AJAX endpoint to report a match comment"""
    from .models import MatchComment
    
    # Verify tournament exists (safety check)
    get_object_or_404(Tournament, pk=pk)
    
    comment = get_object_or_404(MatchComment, pk=comment_id)
    
    # Check if user already reported this comment
    existing_report = Report.objects.filter(
        reporter=request.user,
        target_match_comment=comment
    ).exists()
    
    if existing_report:
        return JsonResponse({'success': False, 'error': 'You already reported this comment.'})
    
    try:
        data = json.loads(request.body)
        reason = data.get('reason', '').strip()
    except:
        reason = request.POST.get('reason', '').strip()
        
    if not reason:
        reason = "No reason provided"
    
    Report.objects.create(
        reporter=request.user,
        reason=reason,
        target_match_comment=comment,
        status='pending'
    )
    
    return JsonResponse({'success': True})


@login_required
@require_POST
def report_tournament_comment(request, pk, comment_id):
    """AJAX endpoint to report a tournament discussion comment"""
    from .models import Comment
    
    # Verify tournament exists
    get_object_or_404(Tournament, pk=pk)
    
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if user already reported this comment
    existing_report = Report.objects.filter(
        reporter=request.user,
        target_tournament_comment=comment
    ).exists()
    
    if existing_report:
        return JsonResponse({'success': False, 'error': 'You already reported this comment.'})
    
    try:
        data = json.loads(request.body)
        reason = data.get('reason', '').strip()
    except:
        reason = request.POST.get('reason', '').strip()
        
    if not reason:
        reason = "No reason provided"
    
    Report.objects.create(
        reporter=request.user,
        reason=reason,
        target_tournament_comment=comment,
        status='pending'
    )
    
    return JsonResponse({'success': True})


def join_lobby(request):
    """Page to enter PIN and join a tournament lobby"""
    if request.method == "POST":
        pin = request.POST.get('pin', '').strip()
        
        if not pin:
            messages.error(request, "Please enter a PIN code.")
            return redirect('tournaments:join_lobby')
        
        tournament = Tournament.objects.filter(pin_code=pin).first()
        
        if not tournament:
            messages.error(request, "Invalid PIN code.")
            return redirect('tournaments:join_lobby')
        
        if tournament.status not in ['waiting', 'open']:
            messages.error(request, "This tournament is not accepting participants.")
            return redirect('tournaments:join_lobby')
        
        # Redirect to nickname entry page
        return redirect('tournaments:join_lobby_confirm', pk=tournament.pk)
    
    return render(request, 'tournaments/join_lobby_pin.html')


@login_required
def join_lobby_confirm(request, pk):
    """Page to enter nickname after PIN is validated"""
    tournament = get_object_or_404(Tournament, pk=pk)
    
    if tournament.status not in ['waiting', 'open']:
        messages.error(request, "This tournament is not accepting participants.")
        return redirect('tournaments:join_lobby')
    
    # Auto-join for Host (Tournament Creator)
    if request.user.is_authenticated and request.user == tournament.created_by:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        # 1. Try to find by User
        participant = Participant.objects.filter(tournament=tournament, user=request.user).first()
        
        # 2. If not found, try to find by Session (e.g. was anonymous before)
        if not participant:
            participant = Participant.objects.filter(tournament=tournament, session_key=session_key).first()
        
        if participant:
            # Update existing
            participant.user = request.user
            participant.nickname = request.user.username
            participant.session_key = session_key # Ensure session key is set
            participant.save()
        else:
            # Create new
            Participant.objects.create(
                tournament=tournament,
                user=request.user,
                nickname=request.user.username,
                session_key=session_key
            )
            
        return redirect('tournaments:waiting_lobby', pk=tournament.pk)
    
    if request.method == "POST":
        nickname = request.POST.get('nickname', '').strip()
        
        if not nickname:
            messages.error(request, "Please enter a nickname.")
            return render(request, 'tournaments/join_lobby.html', {'tournament': tournament})
        
        # Create or update participant
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        
        # 1. Try to find by User
        participant = Participant.objects.filter(tournament=tournament, user=request.user).first()
        
        # 2. If not found, try to find by Session
        if not participant:
            participant = Participant.objects.filter(tournament=tournament, session_key=session_key).first()
        
        if participant:
            participant.user = request.user
            participant.nickname = nickname
            participant.session_key = session_key
            participant.save()
        else:
            Participant.objects.create(
                tournament=tournament,
                user=request.user,
                nickname=nickname,
                session_key=session_key
            )
        
        messages.success(request, f"Welcome, {nickname}!")
        return redirect('tournaments:waiting_lobby', pk=tournament.pk)
    
    return render(request, 'tournaments/join_lobby.html', {'tournament': tournament})


def waiting_lobby(request, pk):
    """Waiting lobby page - shows participants and waits for host to start"""
    tournament = get_object_or_404(Tournament, pk=pk)
    
    # If tournament is already live, redirect to play
    if tournament.status == 'open':
        return redirect('tournaments:play', pk=pk)
    
    if tournament.status == 'finished':
        return redirect('tournaments:summary', pk=pk)
    
    participants = tournament.participants.all()
    
    context = {
        'tournament': tournament,
        'participants': participants,
        'is_host': request.user == tournament.created_by,
    }
    return render(request, 'tournaments/waiting_lobby.html', context)


@login_required
def open_lobby(request, pk):
    """Host opens the lobby - generates PIN and sets status to waiting"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)
    
    if tournament.status != 'draft':
        messages.info(request, "Tournament already published.")
        return redirect('tournaments:waiting_lobby', pk=pk)
    
    # Check if tournament is ready
    if not tournament.is_ready_to_publish():
        messages.error(request, f"You need exactly {tournament.bracket_size} competitors to open the lobby.")
        return redirect('tournaments:add_competitors', pk=pk)
    
    # Generate unique PIN
    while True:
        pin = generate_pin_code()
        if not Tournament.objects.filter(pin_code=pin).exists():
            break
    
    tournament.pin_code = pin
    tournament.status = 'waiting'
    tournament.save()
    
    messages.success(request, f"Lobby opened! Share PIN: {pin}")
    return redirect('tournaments:waiting_lobby', pk=pk)


@login_required
def start_tournament(request, pk):
    """Host starts the tournament from waiting lobby"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)
    
    if request.method != 'POST':
        return redirect('tournaments:waiting_lobby', pk=pk)
    
    if tournament.status != 'waiting':
        messages.error(request, "Tournament is not in waiting state.")
        return redirect('tournaments:tournament_detail', pk=pk)
    
    # Generate bracket
    competitors = list(tournament.competitors.all())
    tournament.matches.all().delete()
    
    round_number = 1
    index = 1
    for i in range(0, len(competitors), 2):
        c1 = competitors[i]
        c2 = competitors[i + 1]
        Match.objects.create(
            tournament=tournament,
            round_number=round_number,
            index_in_round=index,
            competitor1=c1,
            competitor2=c2,
            is_finished=False,
        )
        index += 1
    
    tournament.status = 'open'
    tournament.current_round = 1
    tournament.save()
    
    messages.success(request, "Tournament started!")
    return redirect('tournaments:play', pk=pk)


def participant_status(request, pk):
    """AJAX endpoint to get participant list and tournament status"""
    tournament = get_object_or_404(Tournament, pk=pk)
    participants = tournament.participants.all()
    
    participants_data = [
        {'nickname': p.nickname, 'joined_at': p.joined_at.strftime('%H:%M')}
        for p in participants
    ]
    
    redirect_url = None
    if tournament.status == 'open':
        redirect_url = f'/tournaments/{pk}/play/'
    elif tournament.status == 'finished':
        redirect_url = f'/tournaments/{pk}/summary/'
    
    return JsonResponse({
        'status': tournament.status,
        'participant_count': participants.count(),
        'participants': participants_data,
        'redirect_url': redirect_url,
    })
