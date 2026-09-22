from django.contrib import admin
from wellness.models import JournalEntry, SleepRecord, PhysicalActivity, WaterIntake, Habit

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood', 'created_at']
    list_filter = ['mood', 'date']

@admin.register(SleepRecord)
class SleepRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'duration_hours', 'quality_rating']

@admin.register(PhysicalActivity)
class PhysicalActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_type', 'duration_minutes', 'calories_burned', 'date']

@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'glasses_logged', 'goal_glasses']

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'frequency', 'streak_count', 'is_completed_today']
