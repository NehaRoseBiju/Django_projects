from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import JournalEntry, SleepRecord, PhysicalActivity, WaterIntake, Habit
from .forms import JournalForm, SleepForm, ActivityForm, HabitForm

@login_required
def wellness_index(request):
    today = timezone.now().date()
    journals = JournalEntry.objects.filter(user=request.user)[:5]
    sleeps = SleepRecord.objects.filter(user=request.user)[:5]
    activities = PhysicalActivity.objects.filter(user=request.user)[:5]
    habits = Habit.objects.filter(user=request.user)
    water, _ = WaterIntake.objects.get_or_create(user=request.user, date=today)

    context = {
        'journals': journals,
        'sleeps': sleeps,
        'activities': activities,
        'habits': habits,
        'water': water,
    }
    return render(request, 'wellness/index.html', context)


@login_required
def add_journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Journal entry saved successfully!")
            return redirect('wellness:index')
    else:
        form = JournalForm()
    return render(request, 'wellness/add_journal.html', {'form': form})


@login_required
def add_sleep(request):
    if request.method == 'POST':
        form = SleepForm(request.POST)
        if form.is_valid():
            sleep = form.save(commit=False)
            sleep.user = request.user
            sleep.save()
            messages.success(request, "Sleep record logged!")
            return redirect('wellness:index')
    else:
        form = SleepForm()
    return render(request, 'wellness/add_sleep.html', {'form': form})


@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            act = form.save(commit=False)
            act.user = request.user
            act.save()
            messages.success(request, "Physical activity recorded!")
            return redirect('wellness:index')
    else:
        form = ActivityForm()
    return render(request, 'wellness/add_activity.html', {'form': form})


@login_required
def log_water(request):
    today = timezone.now().date()
    water, _ = WaterIntake.objects.get_or_create(user=request.user, date=today)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            water.glasses_logged += 1
        elif action == 'subtract' and water.glasses_logged > 0:
            water.glasses_logged -= 1
        water.save()
        messages.success(request, f"Updated hydration: {water.glasses_logged} glasses.")
    return redirect('wellness:index')


@login_required
def toggle_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.now().date()
    
    if habit.last_completed_date == today:
        habit.is_completed_today = False
        if habit.streak_count > 0:
            habit.streak_count -= 1
        habit.last_completed_date = None
        messages.info(request, f"Habit '{habit.title}' unchecked.")
    else:
        habit.is_completed_today = True
        habit.streak_count += 1
        habit.last_completed_date = today
        messages.success(request, f"Streak +1! Completed '{habit.title}'. Keep it up!")
        
    habit.save()
    return redirect('wellness:index')


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            h = form.save(commit=False)
            h.user = request.user
            h.save()
            messages.success(request, "New wellness habit created!")
            return redirect('wellness:index')
    else:
        form = HabitForm()
    return render(request, 'wellness/add_habit.html', {'form': form})
