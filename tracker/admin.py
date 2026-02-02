from django.contrib import admin
from .models import FitnessGoal, Exercise, Workout

admin.site.register(FitnessGoal)
admin.site.register(Exercise)
admin.site.register(Workout)
