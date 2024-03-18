from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Add this import

class SignUpForm(UserCreationForm):
    # Vous pouvez personnaliser ce formulaire selon vos besoins
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
