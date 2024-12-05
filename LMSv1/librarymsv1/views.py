from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm,UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on user roles or default
            if user.groups.filter(name='Librarian').exists():
                return redirect('librarian_dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('home_page')
            else:
                return HttpResponse("NOt assigned a role")
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'login_form': form})

def custom_logout(request):
    logout(request) #destroy all the session id for a particular user
    return redirect('login')

@login_required
def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html')

#@login_required
def home_page(request):
    return render(request, 'home_page.html')

def register(request):
    if request.method == 'POST':
        # Initialize the form with POST data
        user_req_form = UserRegistrationForm(request.POST)
        if user_req_form.is_valid():
            # Create the form but don't save it yet
            new_user = user_req_form.save(commit=False)
            # Set the password securely using set_password
            new_user.set_password(user_req_form.cleaned_data['password'])
            new_user.save()  # Save the user to the database
            messages.success(request, 'Your account has been created successfully. Please log in.')
            return render(request, 'register_done.html', {'user_req_form': user_req_form})
        else:
            # If form is invalid, display error messages
            messages.error(request, 'There was an error with your signup. Please check the details and try again.')
    else:
        # Display an empty form if the request is not POST
        user_req_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_req_form': user_req_form})