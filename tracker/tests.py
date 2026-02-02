from django.test import TestCase
from .models import Exercise

class ExerciseTest(TestCase):
    def test_create(self):
        e = Exercise.objects.create(
            name="Pushups",
            muscle_group="Chest",
            calories_per_minute=5
        )
        self.assertEqual(e.name, "Pushups")
