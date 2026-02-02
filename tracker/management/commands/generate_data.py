from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Workout, FitnessGoal, Exercise
from tracker.factories import UserFactory, WorkoutFactory, FitnessGoalFactory, ExerciseFactory
import random

class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):
        # Brišemo stare podatke (osim superusera)
        Workout.objects.all().delete()
        FitnessGoal.objects.all().delete()
        Exercise.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Kreiramo testne vježbe (npr. 10)
        exercises = [ExerciseFactory() for _ in range(10)]

        # Kreiramo testne korisnike, ciljeve i treninge
        for _ in range(25):
            user = UserFactory()
            FitnessGoalFactory(user=user)

            for _ in range(5):
                workout = WorkoutFactory(user=user, exercise=random.choice(exercises))

        self.stdout.write(self.style.SUCCESS("Test data generated successfully!"))
