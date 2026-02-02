from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Exercise, FitnessGoal, Workout
from .forms import RegisterForm

def home(request):
    goals = []
    if request.user.is_authenticated:
        goals = FitnessGoal.objects.filter(user=request.user)
    
    return render(request, "home.html", {"goals": goals})

class AboutView(TemplateView):
    template_name = "about.html"

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "register.html", {"form": form})

# --- EXERCISES (Admin Only za CUD operacije) ---

class ExerciseList(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = "exercise_list.html"

class ExerciseCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")
    
    def test_func(self):
        return self.request.user.is_staff # Samo admini

class ExerciseUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exercise
    fields = "__all__"
    template_name = "exercise_form.html"
    success_url = reverse_lazy("exercises")
    
    def test_func(self):
        return self.request.user.is_staff # Samo admini

class ExerciseDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exercise
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("exercises")
    
    def test_func(self):
        return self.request.user.is_staff # Samo admini

# --- GOALS (Korisnik vidi i uređuje samo SVOJE) ---

class GoalList(LoginRequiredMixin, ListView):
    model = FitnessGoal
    template_name = "goal_list.html"

    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user)

class GoalCreate(LoginRequiredMixin, CreateView):
    model = FitnessGoal
    fields = ['title', 'description', 'target_weight', 'current_weight', 'deadline']
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")
    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FitnessGoal
    fields = ['title', 'description', 'target_weight', 'current_weight', 'deadline']
    template_name = "goal_form.html"
    success_url = reverse_lazy("goals")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user # Samo vlasnik može uređivati

class GoalDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FitnessGoal
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("goals")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

# --- WORKOUTS (Korisnik vidi i uređuje samo SVOJE) ---

class WorkoutList(LoginRequiredMixin, ListView):
    model = Workout
    template_name = "workout_list.html"
    
    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class WorkoutCreate(LoginRequiredMixin, CreateView):
    model = Workout
    fields = ['exercise', 'duration_minutes']
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    fields = ['exercise', 'duration_minutes']
    template_name = "workout_form.html"
    success_url = reverse_lazy("workouts")

    def test_func(self):
        workout = self.get_object()
        return workout.user == self.request.user

class WorkoutDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("workouts")

    def test_func(self):
        workout = self.get_object()
        return workout.user == self.request.user