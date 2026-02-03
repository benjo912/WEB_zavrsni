from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Workout, FitnessGoal, Exercise

# Form za registraciju s profilom
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.update_or_create(
            user=user,
            defaults={'birth_date': self.cleaned_data["birth_date"]}
        )
        return user

class GoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ['title', 'description', 'target_weight', 'current_weight', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'modern-input'}),
            'description': forms.Textarea(attrs={'class': 'modern-input', 'rows': 4}),
            'target_weight': forms.NumberInput(attrs={'class': 'modern-input'}),
            'current_weight': forms.NumberInput(attrs={'class': 'modern-input'}),
            'deadline': forms.DateInput(attrs={'class': 'modern-input', 'type': 'date'}),
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'duration_minutes']
        widgets = {
            'exercise': forms.Select(attrs={'class': 'modern-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'modern-input', 'placeholder': 'Enter minutes...'}),
        }