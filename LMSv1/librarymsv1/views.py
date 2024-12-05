from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm,UserRegistrationForm,BookForm,AuthorForm,GenreForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from .models import Books,Authors,Genres


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
            # Add the user to the default 'student' group
            group = Group.objects.get(name='student')
            new_user.groups.add(group)

            messages.success(request, 'Your account has been created successfully. Please log in.')
            return render(request, 'register_done.html', {'user_req_form': user_req_form})
        else:
            # If form is invalid, display error messages
            messages.error(request, 'There was an error with your signup. Please check the details and try again.')
    else:
        # Display an empty form if the request is not POST
        user_req_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_req_form': user_req_form})

#BOOKLIST Admin
def book_list(request):
    # Fetch the search term and filter status from the request
    search_term = request.GET.get('searchbook', '')
    status_filter = request.GET.get('status', '')

    # Start with all books
    books = Books.objects.all()

    # Apply search filter if a search term is provided
    if search_term:
        books = books.filter(book_name__icontains=search_term)  # Case-insensitive search

    # Apply status filter if a status is provided
    if status_filter:
        books = books.filter(status=status_filter)

    return render(request, 'books/book_list.html', {'books': books})

#ADD NEW BOOK
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect after saving
    else:
        form = BookForm()  # Empty form for adding a new book
    
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Add Book'})

#UPDATE EXISTING BOOK
def book_edit(request, pk):
    book = get_object_or_404(Books, pk=pk)

    # Dynamically adjust the form to limit editable fields to rent_percentage, price, quantity, status
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
        
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})

#DELETE BOOK
def book_delete(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# View to display list of authors
def author_list(request):
    authors = Authors.objects.all()
    return render(request, 'authors/author_list.html', {'authors': authors})

# View to add a new author
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'authors/author_form.html', {'form': form})

# View to edit an existing author
def edit_author(request, pk):
    author = get_object_or_404(Authors, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'authors/author_form.html', {'form': form})

# View to delete an author
def delete_author(request, pk):
    author = get_object_or_404(Authors, pk=pk)
    author.delete()
    return redirect('author_list')

# View to display the list of genres
def genre_list(request):
    genres = Genres.objects.all()
    return render(request, 'genres/genre_list.html', {'genres': genres})

# View to add a new genre
def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm()
    return render(request, 'genres/genre_form.html', {'form': form})

# View to edit an existing genre
def edit_genre(request, pk):
    genre = get_object_or_404(Genres, pk=pk)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm(instance=genre)
    return render(request, 'genres/genre_form.html', {'form': form})

# View to delete a genre
def delete_genre(request, pk):
    genre = get_object_or_404(Genres, pk=pk)
    genre.delete()
    return redirect('genre_list')