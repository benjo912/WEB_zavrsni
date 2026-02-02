from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Workout, FitnessGoal, Exercise

class Command(BaseCommand):
    help = "Clear all test data"

    def handle(self, *args, **kwargs):
        Workout.objects.all().delete()
        FitnessGoal.objects.all().delete()
        Exercise.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS("All test data cleared!"))
