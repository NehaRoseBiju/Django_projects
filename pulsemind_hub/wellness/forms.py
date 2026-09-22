from django import forms
from .models import JournalEntry, SleepRecord, PhysicalActivity, WaterIntake, Habit

class JournalForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['mood', 'content']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Express your feelings, reflections or daily thoughts...'}),
        }

class SleepForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['bedtime', 'wake_time', 'duration_hours', 'quality_rating', 'disturbances']
        widgets = {
            'bedtime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'wake_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'quality_rating': forms.Select(choices=[(i, f"{i} Stars {'★'*i}") for i in range(1, 6)], attrs={'class': 'form-select'}),
            'disturbances': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional notes on disturbances'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = PhysicalActivity
        fields = ['exercise_type', 'duration_minutes', 'intensity', 'calories_burned']
        widgets = {
            'exercise_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Morning Run, Yoga'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'intensity': forms.Select(attrs={'class': 'form-select'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'frequency']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10 Min Meditation, Hydrate 2L'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
        }
