from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitLog
from gamification.models import UserProfile
from datetime import date, timedelta
import csv
from django.http import HttpResponse


@login_required
def add_habit(request):

    if request.method == 'POST':

        Habit.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            frequency=request.POST.get('frequency')
        )

        return redirect('dashboard')

    return render(request, 'add_habit.html')


@login_required
def edit_habit(request, id):

    habit = Habit.objects.get(
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        habit.title = request.POST.get('title')
        habit.description = request.POST.get('description')
        habit.category = request.POST.get('category')
        habit.frequency = request.POST.get('frequency')

        habit.save()

        return redirect('dashboard')

    return render(request, 'edit_habit.html', {'habit': habit})


@login_required
def delete_habit(request, id):

    habit = Habit.objects.get(
        id=id,
        user=request.user
    )

    habit.delete()

    return redirect('dashboard')


@login_required
def complete_habit(request, id):

    habit = Habit.objects.get(
        id=id,
        user=request.user
    )

    today = date.today()

    yesterday = today - timedelta(days=1)

    # CHECK IF ALREADY COMPLETED TODAY

    already_completed = HabitLog.objects.filter(
        habit=habit,
        date=today
    ).exists()

    if not already_completed:

        # CREATE LOG

        HabitLog.objects.create(
            habit=habit,
            completed=True,
            date=today
        )

        # STREAK LOGIC

        yesterday_completed = HabitLog.objects.filter(
            habit=habit,
            date=yesterday
        ).exists()

        if yesterday_completed:

            habit.streak += 1

        else:

            habit.streak = 1

        habit.save()

        # XP SYSTEM

        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

        profile.xp += 10

        # LEVEL SYSTEM

        if profile.xp >= 500:

            profile.level = 4

        elif profile.xp >= 250:

            profile.level = 3

        elif profile.xp >= 100:

            profile.level = 2

        else:

            profile.level = 1

        profile.save()

    return redirect('dashboard')





@login_required
def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="habit_logs.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Habit',
        'Date',
        'Completed'
    ])

    logs = HabitLog.objects.filter(
        habit__user=request.user
    )

    for log in logs:

        writer.writerow([
            log.habit.title,
            log.date,
            log.completed
        ])

    return response

    return redirect('dashboard')