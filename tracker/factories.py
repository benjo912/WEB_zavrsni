import factory
from django.contrib.auth.models import User
from tracker.models import Workout, FitnessGoal, Exercise
from django.core.files.base import ContentFile
from faker import Faker
from io import BytesIO
from PIL import Image
import random

fake = Faker()

# -----------------------------
# Factory za korisnika
# -----------------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

# -----------------------------
# Factory za Exercise sa PNG slikom
# -----------------------------
class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    name = factory.LazyAttribute(lambda x: fake.word().capitalize())
    muscle_group = factory.LazyAttribute(lambda x: fake.word().capitalize())
    calories_per_minute = factory.LazyAttribute(lambda x: random.randint(5, 15))

    @factory.lazy_attribute
    def image(self):
        # Kreiraj PNG sliku 200x200 s random bojom
        img = Image.new(
            'RGBA', 
            (200, 200), 
            color=(random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
        )
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return ContentFile(buffer.read(), f"{self.name}.png")

# -----------------------------
# Factory za FitnessGoal
# -----------------------------
class FitnessGoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FitnessGoal

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    target_weight = factory.LazyAttribute(lambda x: random.randint(60, 100))
    current_weight = factory.LazyAttribute(lambda x: random.randint(50, x.target_weight))
    deadline = factory.Faker('date_this_year')

# -----------------------------
# Factory za Workout
# -----------------------------
class WorkoutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workout

    user = factory.SubFactory(UserFactory)
    exercise = factory.LazyFunction(lambda: ExerciseFactory())
    duration_minutes = factory.LazyAttribute(lambda x: random.randint(10, 90))
    date = factory.Faker('date_this_year')
