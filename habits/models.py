from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(max_length=100)

    frequency = models.CharField(max_length=50)

    streak = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HabitLog(models.Model):

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE
    )

    completed = models.BooleanField(default=False)

    date = models.DateField()

    def __str__(self):
        return f"{self.habit.title} - {self.date}"