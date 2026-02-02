from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Exercise, FitnessGoal, Workout
from .forms import RegisterForm


def home(request):
    return render(request, "home.html")


class AboutView(TemplateView):
    template_name = "about.html"


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "register.html", {"form": form})


class ExerciseList(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = "exercise_list.html"


class ExerciseCreate(LoginRequiredMixin, CreateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")


class ExerciseUpdate(LoginRequiredMixin, UpdateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")


class ExerciseDelete(LoginRequiredMixin, DeleteView):
    model = Exercise
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("exercises")


class GoalList(LoginRequiredMixin, ListView):
    model = FitnessGoal
    template_name = "goal_list.html"


class GoalCreate(LoginRequiredMixin, CreateView):
    model = FitnessGoal
    fields = "__all__"
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")


class GoalUpdate(LoginRequiredMixin, UpdateView):
    model = FitnessGoal
    fields = "__all__"
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")


class GoalDelete(LoginRequiredMixin, DeleteView):
    model = FitnessGoal
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("goals")


class WorkoutList(LoginRequiredMixin, ListView):
    model = Workout
    template_name = "workout_list.html"


class WorkoutCreate(LoginRequiredMixin, CreateView):
    model = Workout
    fields = "__all__"
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")


class WorkoutUpdate(LoginRequiredMixin, UpdateView):
    model = Workout
    fields = "__all__"
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")


class WorkoutDelete(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("workouts")
