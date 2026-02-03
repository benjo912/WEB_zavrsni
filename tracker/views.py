from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Exercise, FitnessGoal, Workout
from .forms import RegisterForm, WorkoutForm, GoalForm

# Početna stranica - prikazuje ciljeve ulogiranog korisnika
def home(request):
    goals = []
    if request.user.is_authenticated:
        goals = FitnessGoal.objects.filter(user=request.user)
    return render(request, "home.html", {"goals": goals})

class AboutView(TemplateView):
    template_name = "about.html"

# Registracija novog korisnika
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "register.html", {"form": form})

# --- EXERCISES (Samo Admin/Staff može dodavati, mijenjati i brisati) ---

class ExerciseList(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = "exercise_list.html"

class ExerciseCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")
    def test_func(self):
        return self.request.user.is_staff

class ExerciseUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")
    def test_func(self):
        return self.request.user.is_staff

class ExerciseDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exercise
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("exercises")
    def test_func(self):
        return self.request.user.is_staff

# --- GOALS (Korisnik upravlja isključivo svojim ciljevima) ---

class GoalList(LoginRequiredMixin, ListView):
    model = FitnessGoal
    template_name = "goal_list.html"
    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user)

class GoalCreate(LoginRequiredMixin, CreateView):
    model = FitnessGoal
    form_class = GoalForm  # KORISTI FORMU
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FitnessGoal
    form_class = GoalForm  # KORISTI FORMU
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class GoalDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FitnessGoal
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("goals")
    # Provjera vlasništva
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

# --- WORKOUTS (Korisnik upravlja isključivo svojim treninzima) ---

class WorkoutList(LoginRequiredMixin, ListView):
    model = Workout
    template_name = "workout_list.html"
    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class WorkoutCreate(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class WorkoutDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("workouts")
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user