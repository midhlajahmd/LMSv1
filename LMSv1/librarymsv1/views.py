from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm,UserRegistrationForm,BookForm,AuthorForm,GenreForm,MembershipPlanForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from .models import Books,Authors,Genres,MembershipPlan,StudentProfile,Rental
from datetime import date, timedelta
from django.utils import timezone



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
                return redirect('book_list_student')
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

    # Editable fields
    editable_fields = ['price', 'rent_percentage', 'quantity', 'status','hidden']

    # Initialize the form with POST data or existing instance
    form = BookForm(
        request.POST or None, 
        instance=book
    )

    # Remove non-editable fields dynamically
    for field in list(form.fields):
        if field not in editable_fields:
            del form.fields[field]

    if form.is_valid():
        form.save()
        return redirect('book_list')

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
    # Get the search query from the GET request
    search_query = request.GET.get('searchauthor', '')
    
    # If there's a search query, filter authors by the author_name
    if search_query:
        authors = Authors.objects.filter(author_name__icontains=search_query)
    else:
        # If no search query, get all authors
        authors = Authors.objects.all()

    # Render the page with the filtered authors
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

#ADMIN SIDE plans
def manage_membership_plans(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'membership-plans/membership_plans.html', {'plans': plans})


def add_or_edit_plan(request, pk=None):
    if pk:
        plan = get_object_or_404(MembershipPlan, pk=pk)
    else:
        plan = None

    if request.method == 'POST':
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('manage_membership_plans')
    else:
        form = MembershipPlanForm(instance=plan)
    return render(request, 'membership-plans/add_or_edit_plan.html', {'form': form})

#USER SIDE plans
@login_required
def view_membership_plans(request):
    plans = MembershipPlan.objects.all()
    current_subscription = None

    # Check if the user has a subscription
    if hasattr(request.user, 'studentprofile') and request.user.studentprofile.membership_plan:
        current_subscription = request.user.studentprofile.membership_plan

    return render(request, 'membership-plans/view_membership_plans.html', {
        'plans': plans,
        'current_subscription': current_subscription
    })

@login_required
def subscribe_to_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, pk=plan_id)
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if student_profile.membership_plan == plan:
        messages.error(request, 'You are already subscribed to this plan.')
    else:
        student_profile.membership_plan = plan
        student_profile.subscription_date = date.today()
        student_profile.expiry_date = date.today() + timedelta(days=plan.plan_duration * 30)
        student_profile.save()
        messages.success(request, f'You have successfully subscribed to the {plan.plan_name} plan.')

    return redirect('view_membership_plans')

@login_required
def upgrade_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, pk=plan_id)
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if student_profile.membership_plan and student_profile.membership_plan.fee >= plan.fee:
        messages.error(request, 'You can only upgrade to a higher plan.')
    else:
        student_profile.membership_plan = plan
        student_profile.subscription_date = date.today()
        student_profile.expiry_date = date.today() + timedelta(days=plan.plan_duration * 30)
        student_profile.save()
        messages.success(request, f'You have successfully upgraded to the {plan.plan_name} plan.')

    return redirect('view_membership_plans')

def student_profile(request):
    return render(request, 'student_profile.html')

def book_list_student(request):
    books = Books.objects.filter(hidden=False)
    return render(request, 'home_page.html', {'books': books})

# Rent a book
# Check if the user is logged in and has a membership plan
def rent_book(request, book_id):
    try:
        # Get the book by ID
        book = Books.objects.get(id=book_id)

        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if not logged in

        # Check if the student profile exists
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            # If no profile exists, redirect to the profile creation page
            messages.error(request, "You need to create a student profile.")
            return redirect('view_membership_plans')  # Assuming 'student_profile' is the profile creation page

        # Check if the book is already rented by the student
        if Rental.objects.filter(student_profile=student_profile, book=book, is_rented=True).exists():
            messages.info(request, "You have already rented this book.")
            return redirect('rented_books')  # Redirect to the rented books page

        # Proceed with renting the book
        rental = Rental.objects.create(student_profile=student_profile, book=book, is_rented=True)
        rental.due_date = timezone.now() + timezone.timedelta(days=student_profile.membership_plan.rent_duration)
        rental.save()

        # Show success message
        messages.success(request, "Book rented successfully!")
        return redirect('rented_books')  # Redirect to the rented books page

    except Books.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('book_list_student')  # Redirect to the book list page


# Return a rented book
@login_required
def return_book(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)

    # Check if the book belongs to the logged-in user
    if rental.student_profile.user != request.user:
        message = 'You cannot return a book you did not rent.'
        return render(request, 'error_alert.html', {'message': message})

    # Mark the book as returned by setting is_rented to False
    rental.is_rented = False
    rental.save()

    return redirect('rented_books')

# List rented books
@login_required
def rented_books(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    rentals = Rental.objects.filter(student_profile=student_profile, is_rented=True)

    return render(request, 'rented_books.html', {'rentals': rentals})