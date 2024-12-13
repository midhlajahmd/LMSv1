from django import forms
from .models import Books,Authors, Genres, MembershipPlan, comments, Reviews,BookContent
from django.forms import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

#LOGIN
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

#REGISTER
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
    
#BOOKS
class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
        widgets = {
            'hidden': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            'bestseller': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            'noteworthy': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            'writeplace': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            'top20': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            'recommend': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 10px; height: 8px;',
            }),
            
        }
    # Override the form field for ISBN to display book name
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use 'id' as the value and 'book_name' as the label in the choices
        self.fields['ISBN'].queryset = BookContent.objects.all()
        self.fields['ISBN'].widget = forms.Select(
            choices=[(book.id, book.book_name) for book in BookContent.objects.all()]
        )
#AUTHORS
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ['author_name']
        widgets = {
            'author_name': forms.TextInput(attrs={'placeholder': 'Enter author name', 'class': 'form-control'})
        }

#GENRES
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = ['genre_name']
        widgets = {
            'genre_name': forms.TextInput(attrs={'placeholder': 'Enter genre name', 'class': 'form-control'})
        }

# Form for MEMBERSHIP PLAN
class MembershipPlanForm(forms.ModelForm):
    # class Meta:
    #     model = MembershipPlan
    #     fields = ['plan_name', 'rent_limit', 'rent_duration', 'plan_duration', 'fee']
    genres = forms.ModelMultipleChoiceField(
        queryset=Genres.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Genres"
    )

    class Meta:
        model = MembershipPlan
        fields = ['plan_name', 'rent_limit', 'rent_duration', 'plan_duration', 'fee', 'genres']

#REVIEW
class AddCommentForm(forms.ModelForm):
    class Meta:
        model=comments
        fields=('comment_text',)


class AddReviewForm(forms.ModelForm):
    class Meta:
        model= Reviews
        fields=('rating','title','description')