from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Workout, FitnessGoal, Exercise, Profile
from tracker.factories import UserFactory, WorkoutFactory, FitnessGoalFactory, ExerciseFactory
import random

class Command(BaseCommand):
    help = "Generira testne podatke. Može se specificirati --username za točno određenog korisnika."

    def add_arguments(self, parser):
        # Dodajemo opcionalni argument --username
        parser.add_argument('--username', type=str, help='Korisničko ime za kojeg generiramo podatke')

    def handle(self, *args, **options):
        username = options.get('username')

        # 1. Priprema vježbi (ako ih nema, kreiraj ih)
        exercises = list(Exercise.objects.all())
        if not exercises:
            self.stdout.write("Nema vježbi u bazi, kreiram 8 novih...")
            exercises = ExerciseFactory.create_batch(8)

        if username:
            # --- SCENARIJ A: Generiranje za SPECIFIČNOG korisnika ---
            try:
                target_user = User.objects.get(username=username)
                self.stdout.write(f"Generiranje podataka za korisnika: {username}...")
                
                # Kreiraj 2 cilja za tog usera
                FitnessGoalFactory.create_batch(2, user=target_user)
                
                # Kreiraj 10 treninga za tog usera
                for _ in range(10):
                    WorkoutFactory(user=target_user, exercise=random.choice(exercises))
                
                self.stdout.write(self.style.SUCCESS(f"Uspješno dodani podaci za {username}!"))
                
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Korisnik '{username}' ne postoji u bazi!"))
        
        else:
            # --- SCENARIJ B: Standardno generiranje (briše sve i radi ispočetka) ---
            self.stdout.write("Brisanje starih podataka i generiranje novih korisnika...")
            Workout.objects.all().delete()
            FitnessGoal.objects.all().delete()
            Exercise.objects.all().delete()
            Profile.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()

            # Ponovno kreiraj vježbe jer smo ih gore obrisali
            exercises = ExerciseFactory.create_batch(8)

            for _ in range(5):
                user = UserFactory()
                FitnessGoalFactory.create_batch(random.randint(1, 2), user=user)
                for _ in range(5):
                    WorkoutFactory(user=user, exercise=random.choice(exercises))

            self.stdout.write(self.style.SUCCESS("Uspješno generirani nasumični podaci!"))