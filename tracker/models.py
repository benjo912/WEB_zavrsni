from django.db import models
from django.contrib.auth.models import User

class FitnessGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    target_weight = models.FloatField()
    current_weight = models.FloatField()
    deadline = models.DateField()

    def progress(self):
        if self.target_weight == 0:
            return 0
        return int((self.current_weight / self.target_weight) * 100)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=100)
    calories_per_minute = models.IntegerField()
    image = models.ImageField(upload_to="exercises/", blank=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name}"
