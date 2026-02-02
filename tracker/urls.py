from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutView.as_view(), name="about"),

    path("exercises/", ExerciseList.as_view(), name="exercises"),
    path("exercises/add/", ExerciseCreate.as_view(), name="exercise_add"),
    path("exercises/<int:pk>/edit/", ExerciseUpdate.as_view(), name="exercise_edit"),
    path("exercises/<int:pk>/delete/", ExerciseDelete.as_view(), name="exercise_delete"),

    path("goals/", GoalList.as_view(), name="goals"),
    path("goals/add/", GoalCreate.as_view(), name="goal_add"),
    path("goals/<int:pk>/edit/", GoalUpdate.as_view(), name="goal_edit"),
    path("goals/<int:pk>/delete/", GoalDelete.as_view(), name="goal_delete"),

    path("workouts/", WorkoutList.as_view(), name="workouts"),
    path("workouts/add/", WorkoutCreate.as_view(), name="workout_add"),
    path("workouts/<int:pk>/edit/", WorkoutUpdate.as_view(), name="workout_edit"),
    path("workouts/<int:pk>/delete/", WorkoutDelete.as_view(), name="workout_delete"),
]
