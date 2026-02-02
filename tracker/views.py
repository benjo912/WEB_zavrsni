from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Exercise, FitnessGoal, Workout


# HOME
def home(request):
    goals = FitnessGoal.objects.all()
    return render(request,"home.html",{"goals":goals})


# REGISTER
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "register.html", {"form": form})


# ------------------ EXERCISES ------------------

class ExerciseList(ListView):
    model = Exercise
    template_name = "exercise_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Exercise.objects.filter(name__icontains=query)
        return Exercise.objects.all()


class ExerciseCreate(CreateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")


class ExerciseUpdate(UpdateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")


class ExerciseDelete(DeleteView):
    model = Exercise
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("exercises")


# ------------------ GOALS ------------------

class GoalList(ListView):
    model = FitnessGoal
    template_name = "goal_list.html"


class GoalCreate(CreateView):
    model = FitnessGoal
    fields = "__all__"
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")


class GoalUpdate(UpdateView):
    model = FitnessGoal
    fields = "__all__"
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")


class GoalDelete(DeleteView):
    model = FitnessGoal
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("goals")


# ------------------ WORKOUTS ------------------

class WorkoutList(ListView):
    model = Workout
    template_name = "workout_list.html"


class WorkoutCreate(CreateView):
    model = Workout
    fields = "__all__"
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")


class WorkoutUpdate(UpdateView):
    model = Workout
    fields = "__all__"
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")


class WorkoutDelete(DeleteView):
    model = Workout
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("workouts")
