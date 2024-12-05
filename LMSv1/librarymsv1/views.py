from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Home Page
def home(request):
    return render(request, 'librarymsv1/home.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'librarymsv1/login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Library Dashboard (Require Login)
@login_required
def dashboard(request):
    # Add logic to fetch and display user-specific data
    return render(request, 'librarymsv1/dashboard.html')

# Book Search (Optional)
def book_search(request):
    query = request.GET.get('q', '')  # Get the search query
    books = []  # Add logic to filter books based on the query
    return render(request, 'librarymsv1/search.html', {'query': query, 'books': books})

