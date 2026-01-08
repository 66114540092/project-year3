from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TournamentForm, CompetitorForm, CommentForm
from .models import Tournament, Competitor, Match, MatchVote


from django.db.models import Q
from django.core.paginator import Paginator

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

    # หลังปิดแมตช์นี้ ตรวจว่า tournament ควรเดินรอบต่อไปไหม
    # ทำใน view play() ตอนเข้าอีกครั้ง
    messages.success(request, f"Match finished. Winner: {winner.name or winner.pk}")
    return redirect("tournaments:play", pk=pk)


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
    
    matches_json = json.dumps(matches_data, cls=DjangoJSONEncoder)

    return render(
        request,
        "tournaments/summary.html",
        {"tournament": tournament, "rounds": rounds, "champion": champion, "matches_json": matches_json},
    )


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
        return JsonResponse({
            'status': tournament.status,
            'match': None,
            'redirect_url': f'/tournaments/{pk}/summary/' if tournament.status == 'finished' else None
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
    
    return JsonResponse({
        'status': tournament.status,
        'match': {
            'id': current_match.id,
            'round': current_match.round_number,
            'is_finished': current_match.is_finished,
            'competitor1': {
                'id': current_match.competitor_1.id,
                'name': current_match.competitor_1.name,
                'image': current_match.competitor_1.image.url if current_match.competitor_1.image else None,
                'votes': votes_c1,
                'percentage': pct_c1,
            },
            'competitor2': {
                'id': current_match.competitor_2.id,
                'name': current_match.competitor_2.name,
                'image': current_match.competitor_2.image.url if current_match.competitor_2.image else None,
                'votes': votes_c2,
                'percentage': pct_c2,
            },
            'total_votes': total_votes,
        },
        'user_vote': user_vote,
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
