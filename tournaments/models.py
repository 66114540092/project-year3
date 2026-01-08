from django.db import models
from django.contrib.auth.models import User
import math


class Tournament(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("open", "Open"),
        ("finished", "Finished"),
    ]

    BRACKET_SIZE_CHOICES = [
        (2, "2"),
        (4, "4"),
        (8, "8"),
        (16, "16"),
    ]
    
    CATEGORY_CHOICES = [
        ("gaming", "Gaming"),
        ("sports", "Sports"),
        ("music", "Music"),
        ("movies", "Movies"),
        ("anime", "Anime"),
        ("food", "Food"),
        ("fashion", "Fashion"),
        ("tech", "Technology"),
        ("art", "Art & Design"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="other")
    language = models.CharField(max_length=50, blank=True)
    thumbnail = models.ImageField(upload_to="tournament_thumbnails/", blank=True, null=True)

    bracket_size = models.PositiveIntegerField(choices=BRACKET_SIZE_CHOICES, default=4)
    voting_duration_seconds = models.PositiveIntegerField(default=60)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    current_round = models.PositiveIntegerField(default=1)

    created_by = models.ForeignKey(
        User,
        related_name="created_tournaments",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def total_rounds(self) -> int:
        """จำนวนรอบทั้งหมด = log2(bracket_size)"""
        return int(math.log2(self.bracket_size)) if self.bracket_size else 0

    def current_match(self):
        """ดึงแมตช์ที่กำลังเล่นอยู่ (ของ current_round ที่ยังไม่ finished)"""
        return (
            self.matches.filter(round_number=self.current_round, is_finished=False)
            .order_by("index_in_round")
            .first()
        )

    def is_ready_to_publish(self) -> bool:
        """พร้อม publish ถ้ามี competitors ครบตาม bracket_size"""
        return self.competitors.count() == self.bracket_size

    def champion(self):
        """ดึงแชมป์ของทัวร์นาเมนต์ (แมตช์รอบสุดท้าย)"""
        if self.status != "finished":
            return None
        last_round = self.total_rounds
        final_match = (
            self.matches.filter(round_number=last_round, is_finished=True)
            .order_by("index_in_round")
            .first()
        )
        return final_match.winner if final_match else None


class Competitor(models.Model):
    """รูปผู้เข้าแข่งขันใน Tournament (ตัวที่ใช้ให้คนโหวต)"""

    tournament = models.ForeignKey(
        Tournament,
        related_name="competitors",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="competitors/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name or f"Competitor {self.pk}"


class Match(models.Model):
    """แมตช์ 1v1 ในทัวร์นาเมนต์"""

    tournament = models.ForeignKey(
        Tournament,
        related_name="matches",
        on_delete=models.CASCADE,
    )
    round_number = models.PositiveIntegerField()
    index_in_round = models.PositiveIntegerField()  # ลำดับแมตช์ในรอบนั้น (1, 2, 3,...)

    competitor1 = models.ForeignKey(
        Competitor,
        related_name="matches_as_competitor1",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    competitor2 = models.ForeignKey(
        Competitor,
        related_name="matches_as_competitor2",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    winner = models.ForeignKey(
        Competitor,
        related_name="wins",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_finished = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["round_number", "index_in_round"]

    def __str__(self):
        return f"Round {self.round_number} Match {self.index_in_round} ({self.tournament.name})"

    def votes_for_competitor1(self):
        return self.votes.filter(choice="1").count()

    def votes_for_competitor2(self):
        return self.votes.filter(choice="2").count()


class MatchVote(models.Model):
    """โหวตของ user ต่อ match"""

    CHOICES = [
        ("1", "Competitor 1"),
        ("2", "Competitor 2"),
    ]

    match = models.ForeignKey(
        Match,
        related_name="votes",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name="match_votes",
        on_delete=models.CASCADE,
    )
    choice = models.CharField(max_length=1, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("match", "user")

    def __str__(self):
        return f"{self.user} -> {self.match} ({self.choice})"


class Comment(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.tournament}"
