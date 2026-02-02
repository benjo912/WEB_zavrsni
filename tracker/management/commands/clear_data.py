from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Workout, FitnessGoal, Exercise, Profile

class Command(BaseCommand):
    help = "Briše sve podatke iz baze (osim superusera)"

    def handle(self, *args, **kwargs):
        Workout.objects.all().delete()
        FitnessGoal.objects.all().delete()
        Exercise.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        
        self.stdout.write(self.style.SUCCESS("Baza podataka je uspješno očišćena!"))