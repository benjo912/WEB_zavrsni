from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = ["username", "email"] # Lozinke UserCreationForm dodaje sam

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Kreiraj profil samo ako već ne postoji (sigurnija metoda)
        Profile.objects.update_or_create(
            user=user,
            defaults={'birth_date': self.cleaned_data["birth_date"]}
        )
        return user