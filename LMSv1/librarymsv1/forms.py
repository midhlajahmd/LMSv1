from django import forms
#from .models import Use
from django.forms import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

#LOGIN function
class LoginForm(AuthenticationForm): 
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    #REGISTER function
class UserRegistrationForm(forms.ModelForm):
# Password field
    password = forms.CharField(
    label='Password',
    widget=forms.PasswordInput,
    min_length=8,  # You can adjust password length as per requirements
    help_text="Password must be at least 8 characters long."
)

    # Confirm password field
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    # Custom validation for confirm password
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('The two password fields must match.')
        return cd['password2']