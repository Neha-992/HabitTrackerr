from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from habits.models import Habit, HabitLog
from gamification.models import UserProfile
from datetime import date, timedelta
import json


def landing(request):

    return render(
        request,
        'landing.html'
    )


@login_required
def dashboard(request):

    # USER HABITS

    habits = Habit.objects.filter(
        user=request.user
    )

    # SEARCH

    search_query = request.GET.get('search')

    if search_query:

        habits = habits.filter(
            title__icontains=search_query
        )

    # CATEGORY FILTER

    category = request.GET.get('category')

    if category:

        habits = habits.filter(
            category=category
        )

    # TOTAL COMPLETED

    total_completed = HabitLog.objects.filter(
        habit__user=request.user
    ).count()

    # TOTAL HABITS

    total_habits = Habit.objects.filter(
        user=request.user
    ).count()

    # COMPLETION PERCENTAGE

    completion_percentage = 0

    if total_habits > 0:

        if total_completed > total_habits:

            completion_percentage = 100

        else:

            completion_percentage = int(
                (total_completed / total_habits) * 100
    )

    # WEEKLY CHART

    last_7_days = []

    last_7_counts = []

    for i in range(6, -1, -1):

        day = date.today() - timedelta(days=i)

        count = HabitLog.objects.filter(
            habit__user=request.user,
            date=day
        ).count()

        last_7_days.append(
            day.strftime("%a")
        )

        last_7_counts.append(count)

    # RECENT ACTIVITY

    recent_logs = HabitLog.objects.filter(
        habit__user=request.user
    ).order_by('-date')[:5]

    # USER PROFILE

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    # HEATMAP DATA

    heatmap_data = []

    for i in range(29, -1, -1):

        day = date.today() - timedelta(days=i)

        count = HabitLog.objects.filter(
            habit__user=request.user,
            date=day
        ).count()

        heatmap_data.append(count)

    # CONTEXT

    context = {

        'habits': habits,

        'total_completed': total_completed,

        'completion_percentage': completion_percentage,

        'last_7_days': json.dumps(last_7_days),

        'last_7_counts': json.dumps(last_7_counts),

        'recent_logs': recent_logs,

        'profile': profile,

        'heatmap_data': heatmap_data,

        'search_query': search_query,

        'selected_category': category,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    total_habits = Habit.objects.filter(
        user=request.user
    ).count()

    total_completed = HabitLog.objects.filter(
        habit__user=request.user
    ).count()

    context = {

        'profile': profile,

        'total_habits': total_habits,

        'total_completed': total_completed,
    }

    return render(
        request,
        'profile.html',
        context
    )

@login_required
def leaderboard(request):

    profiles = UserProfile.objects.all().order_by('-xp')

    context = {

        'profiles': profiles
    }

    return render(
        request,
        'leaderboard.html',
        context
    )