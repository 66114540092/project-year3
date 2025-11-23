from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TournamentForm, CompetitorForm, CommentForm
from .models import Tournament, Competitor, Match, MatchVote


def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(
        request,
        "tournaments/tournament_list.html",
        {"tournaments": tournaments},
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
    """หน้าอัปโหลดรูปผู้เข้าแข่งขัน"""
    tournament = get_object_or_404(Tournament, pk=pk, created_by=request.user)

    if tournament.status != "draft":
        messages.info(request, "Tournament already published.")
        return redirect("tournaments:tournament_detail", pk=pk)

    if request.method == "POST":
        form = CompetitorForm(request.POST, request.FILES)
        if form.is_valid():
            competitor = form.save(commit=False)
            competitor.tournament = tournament
            competitor.save()
            messages.success(request, "Competitor added.")
            return redirect("tournaments:add_competitors", pk=tournament.pk)
    else:
        form = CompetitorForm()

    competitors = tournament.competitors.all()
    count = competitors.count()
    can_publish = tournament.is_ready_to_publish()

    return render(
        request,
        "tournaments/add_competitors.html",
        {
            "tournament": tournament,
            "form": form,
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

    winners = list(
        Competitor.objects.filter(
            wins__tournament=tournament,
            wins__round_number=current_round,
        ).distinct()
    )

    # ลบแมตช์ของ next_round ถ้ามีอยู่ก่อน
    tournament.matches.filter(round_number=next_round).delete()

    index = 1
    for i in range(0, len(winners), 2):
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

    return render(
        request,
        "tournaments/summary.html",
        {"tournament": tournament, "rounds": rounds, "champion": champion},
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
