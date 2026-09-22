from django.db import models
from django.conf import settings
from django.utils import timezone

class JournalEntry(models.Model):
    MOOD_CHOICES = (
        ('GREAT', '😄 Great'),
        ('GOOD', '🙂 Good'),
        ('CALM', '😌 Calm'),
        ('ANXIOUS', '😰 Anxious'),
        ('TIRED', '😴 Tired'),
        ('SAD', '😔 Sad'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField(default=timezone.now)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='GOOD')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username}'s Journal - {self.date} ({self.get_mood_display()})"


class SleepRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sleep_records')
    date = models.DateField(default=timezone.now)
    bedtime = models.TimeField(help_text="Time went to bed")
    wake_time = models.TimeField(help_text="Time woke up")
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, help_text="Total sleep duration in hours")
    quality_rating = models.IntegerField(default=4, help_text="Rating 1 to 5 stars")
    disturbances = models.TextField(blank=True, null=True, help_text="Notes on wakeups or disturbances")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} Sleep - {self.duration_hours}h on {self.date}"


class PhysicalActivity(models.Model):
    INTENSITY_CHOICES = (
        ('LOW', 'Low (Walking, Yoga)'),
        ('MODERATE', 'Moderate (Jogging, Cycling)'),
        ('HIGH', 'High (HIIT, Running, Gym)'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField(default=timezone.now)
    exercise_type = models.CharField(max_length=100, help_text="e.g. Morning Jog, Yoga, Cycling")
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES, default='MODERATE')
    calories_burned = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.exercise_type} ({self.duration_minutes} mins) - {self.user.username}"


class WaterIntake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='water_intakes')
    date = models.DateField(default=timezone.now)
    glasses_logged = models.PositiveIntegerField(default=0, help_text="Number of 250ml glasses logged")
    goal_glasses = models.PositiveIntegerField(default=8, help_text="Daily goal in glasses")

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    @property
    def percentage(self):
        if self.goal_glasses == 0:
            return 100
        return min(int((self.glasses_logged / self.goal_glasses) * 100), 100)

    def __str__(self):
        return f"{self.user.username} Hydration - {self.glasses_logged}/{self.goal_glasses} glasses"


class Habit(models.Model):
    FREQUENCY_CHOICES = (
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=150, help_text="e.g., 10 Min Meditation, No Sugar")
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='DAILY')
    streak_count = models.PositiveIntegerField(default=0)
    is_completed_today = models.BooleanField(default=False)
    last_completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Streak: {self.streak_count} days)"
