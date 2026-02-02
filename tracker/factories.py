import factory
from django.contrib.auth.models import User
from tracker.models import Workout, FitnessGoal, Exercise, Profile
from django.core.files.base import ContentFile
from faker import Faker
from io import BytesIO
from PIL import Image
import random

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    @factory.post_generation
    def create_profile(obj, create, extracted, **kwargs):
        if not create:
            return
        Profile.objects.get_or_create(
            user=obj, 
            defaults={'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=65)}
        )

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        obj.set_password("password123")
        obj.save()

class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    # Koristimo sekvencu ili iterator da izbjegnemo duplikate u kratkom batchu
    name = factory.Sequence(lambda n: f"{random.choice(['Push Ups', 'Squats', 'Deadlift', 'Plank', 'Running', 'Cycling', 'Pull Ups', 'Bench Press'])} {n}")
    muscle_group = factory.Iterator(['Chest', 'Legs', 'Back', 'Core', 'Full Body', 'Legs', 'Back', 'Chest'])
    calories_per_minute = factory.LazyFunction(lambda: random.randint(5, 15))

    @factory.lazy_attribute
    def image(self):
        # Generiranje PNG slike u boji
        width, height = 400, 400
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        img = Image.new("RGB", (width, height), color)
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        # POPRAVAK: Dodan 'name' argument koji je nedostajao
        return ContentFile(buffer.getvalue(), name=f"exercise_{random.randint(1000, 9999)}.png")

class FitnessGoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FitnessGoal

    user = factory.SubFactory(UserFactory)
    title = factory.Iterator(['Lose Weight', 'Build Muscle', 'Marathon Training', 'General Fitness'])
    description = factory.Faker('sentence', nb_words=10)
    target_weight = factory.LazyFunction(lambda: float(random.randint(70, 95)))
    current_weight = factory.LazyFunction(lambda: float(random.randint(80, 110)))
    deadline = factory.Faker('date_between', start_date='+30d', end_date='+1y')

class WorkoutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workout

    user = factory.SubFactory(UserFactory)
    exercise = factory.SubFactory(ExerciseFactory)
    duration_minutes = factory.LazyFunction(lambda: random.randint(15, 90))