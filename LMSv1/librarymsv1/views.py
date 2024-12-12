from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm,UserRegistrationForm,BookForm,AuthorForm,GenreForm,MembershipPlanForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from .models import Books,Authors,Genres,MembershipPlan,StudentProfile,Rental,BookContent,Payment,BookPurchase
from datetime import date, timedelta
from django.utils import timezone
from django.http import JsonResponse
import json
from django.urls import reverse
from django.db.models import Q
from django.http import Http404


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on user roles or default
            if user.groups.filter(name='Librarian').exists():
                # Display alert and redirect
                response = """
                    <script>
                        alert('Logged In Successfully.');
                        window.location.href = '{}';
                    </script>
                """.format(reverse('librarian_dashboard'))
                return HttpResponse(response)
            elif user.groups.filter(name='Student').exists():
                # Display alert and redirect
                response = """
                    <script>
                        alert('Logged In Successfully.');
                        window.location.href = '{}';
                    </script>
                """.format(reverse('book_list_student'))
                return HttpResponse(response)
            else:
                return HttpResponse("NOt assigned a role")
        else:
            # Display alert and redirect
            response = """
                <script>
                    alert('Invalid Username/Password');
                    window.location.href = '{}';
                </script>
            """.format(reverse('login'))
            return HttpResponse(response)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'login_form': form})

def custom_logout(request):
    logout(request) #destroy all the session id for a particular user
    response = """
        <script>
            alert('You are logged out.');
            window.location.href = '{}';
        </script>
    """.format(redirect('book_list_student').url)
    return HttpResponse(response)

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

            #messages.success(request, 'Your account has been created successfully. Please log in.')
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
    hidden_filter = request.GET.get('hidden', '')

    # Start with all books
    books = Books.objects.all()

    # Apply search filter if a search term is provided
    if search_term:
        books = books.filter(book_name__icontains=search_term)  # Case-insensitive search

    # Apply status filter if a status is provided
    if status_filter:
        books = books.filter(status=status_filter)

    # Exclude hidden books if a status filter is applied (Available or Unavailable)
    if status_filter and status_filter in ['available', 'unavailable']:
        books = books.exclude(hidden=True)
    
    # Apply hidden filter if a hidden status is provided
    if hidden_filter:
        # If hidden_filter is 'True', show hidden books, else show non-hidden books
        if hidden_filter.lower() == 'true':
            books = books.filter(hidden=True)
        else:
            books = books.filter(hidden=False)

    if not status_filter and not hidden_filter:
        books = books.exclude(hidden=True)    

    return render(request, 'books/book_list.html', {'books': books})

#ADD NEW BOOK
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            # Display alert and redirect
            response = """
                <script>
                    alert('Book added successfully!');
                    window.location.href = '{}';
                </script>
            """.format(reverse('book_list'))
            return HttpResponse(response)
            # return redirect('book_list')  # Redirect after saving
    else:
        form = BookForm()  # Empty form for adding a new book
    
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Add a New Book'})

#UPDATE EXISTING BOOK
def book_edit(request, pk):
    book = get_object_or_404(Books, pk=pk)

    # Editable fields
    editable_fields = ['price', 'rent_percentage', 'quantity', 'status','hidden','featured','bestseller','noteworthy','writeplace','top20','recommend',]

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
        # Display alert and redirect
        response = """
            <script>
                alert('Book Edited successfully!');
                window.location.href = '{}';
            </script>
        """.format(reverse('book_list'))
        return HttpResponse(response)

    return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})


#DELETE BOOK
def book_delete(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        book.hidden = True  # Set the 'hidden' field to True instead of deleting
        book.save()  # Save the updated book
        # Display alert and redirect
        response = """
            <script>
                alert('Book deleted successfully!');
                window.location.href = '{}';
            </script>
        """.format(reverse('book_list'))
        return HttpResponse(response)
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
    # Get the search query from the GET request
    search_query = request.GET.get('searchgenre', '')
    
    # If there's a search query, filter authors by the author_name
    if search_query:
        genres = Genres.objects.filter(genre_name__icontains=search_query)
    else:
        # If no search query, get all authors
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
def plan_details(request, plan_id):
    plan = get_object_or_404(MembershipPlan, pk=plan_id)
    return render(request, 'membership-plans/plan_details.html', {'plan': plan})

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

    # Check if the user is already subscribed to this plan
    if student_profile.membership_plan == plan:
        messages.error(request, 'You are already subscribed to this plan.')
        return redirect('view_membership_plans')

    # Redirect to the payment processing view to handle payment before finalizing the subscription
    return redirect('process_payment', order_type_name="membership", related_id=plan.id)

@login_required
def upgrade_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, pk=plan_id)
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if student_profile.membership_plan and student_profile.membership_plan.fee >= plan.fee:
        messages.error(request, 'You can only upgrade to a higher plan.')
        return redirect('view_membership_plans')

    # Redirect to the payment processing view to handle payment before finalizing the upgrade
    return redirect('process_payment', order_type_name="membership", related_id=plan.id)

def student_profile(request):
    return render(request, 'student_profile.html')

from django.db.models import Q

def book_list_student(request):
    # # Get the search query from the GET request
    # search_query = request.GET.get('searchbook', '').strip()

    # # Start with filtering books that are not hidden
    # books = Books.objects.filter(hidden=False)

    # if search_query:
    #     # Filter by book name, author name, and genre name
    #     books = books.filter(
    #         Q(book_name__icontains=search_query) |
    #         Q(author__author_name__icontains=search_query) |
    #         Q(genre__genre_name__icontains=search_query)
    #     )
    #     message = f"Search results for '{search_query}'" if books.exists() else f"No results for '{search_query}'"
    # else:
    #     message = f"No results for {search_query}"

    # return render(request, 'home_page.html', {'books': books, 'message': message, 'search_query': search_query})
    # Get the search query from the GET request
    search_query = request.GET.get('searchbook', '').strip()

    # Start with filtering books that are not hidden
    books = Books.objects.filter(hidden=False)

    if search_query:
        # Filter by book name, author name, and genre name
        books = books.filter(
            Q(book_name__icontains=search_query) |
            Q(author__author_name__icontains=search_query) |
            Q(genre__genre_name__icontains=search_query)
        )
        message = f"Search results for '{search_query}'" if books.exists() else f"No results for '{search_query}'"
        # Skip grouping by categories if search query is provided
        categories = None
    else:
        message = None
        # Group books by categories
        categories = {
            'Featured Books': books.filter(featured=True),
            'Bestsellers': books.filter(bestseller=True),
            'New & Noteworthy': books.filter(noteworthy=True),
            'The Writeplace Books': books.filter(writeplace=True),
            'Top 20': books.filter(top20=True),
            'QuillQuest Recommends': books.filter(recommend=True),
        }

    return render(request, 'home_page.html', {
        'categories': categories,
        'books': books if search_query else None,  # Pass all books only if a search is made
        'message': message,
        'search_query': search_query
    })


# Rent a book
# Check if the user is logged in and has a membership plan
# Integrated payment
@login_required
def rent_book(request, book_id):
    try:
        # Get the book by ID
        book = get_object_or_404(Books, id=book_id)

        # Ensure the user is logged in (this is already ensured by @login_required)
        # Check if the student profile exists
        student_profile = StudentProfile.objects.get(user=request.user)
        membership_plan = student_profile.membership_plan
        if not membership_plan:
            # Display alert and redirect
            response = """
                <script>
                    alert('You need to subscribe to a membership plan to rent books.');
                    window.location.href = '{}';
                </script>
            """.format(reverse('view_membership_plans'))
            return HttpResponse(response)
        
        
        # Check if the user has exceeded the rental limit
        active_rentals_count = Rental.objects.filter(
            student_profile=student_profile,
            is_rented=True
        ).count()

        # Check if the book is already rented by the student
        if Rental.objects.filter(student_profile=student_profile, book=book, is_rented=True).exists():
            messages.info(request, "You have already rented this book.")
            return redirect('rented_books')  # Redirect to the rented books page

        rental_limit = student_profile.membership_plan.rent_limit  # Assuming 'rental_limit' is a field in membership_plan
        if active_rentals_count >= rental_limit:
            return render(request, 'alert_and_redirect.html', {
                'alert_message': f"You cannot rent more than {rental_limit} books.",
                'redirect_url': 'book_list_student'  # Named URL for redirection
            })

        # Redirect to the payment processing view to handle payment before finalizing the rental
        return redirect('process_payment', order_type_name="rental", related_id=book.id)

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
    try:
        # Attempt to get the StudentProfile for the logged-in user
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        # If StudentProfile doesn't exist, alert the user
        messages.error(request, "No books to show. Please subscribe a plan")
        student_profile = None

    # If a valid student_profile is found, fetch rentals
    if student_profile:
        rentals = Rental.objects.filter(student_profile=student_profile, is_rented=True)
    else:
        rentals = []

    return render(request, 'rented_books.html', {'rentals': rentals})

def rent_details(request, book_id):
    try:
        # Fetch the book details
        book = Books.objects.get(pk=book_id)

        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')

        # Check if the student profile exists
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            messages.error(request, "You need to create a student profile first.")
            return redirect('view_membership_plans')

        # Check if the book is already rented by the user
        rental = Rental.objects.filter(
            student_profile=student_profile,
            book=book,
            is_rented=True
        ).first()

        # Fetch the book content (e.g., cover image) based on ISBN
        book_content = BookContent.objects.filter(id=book.ISBN_id).first()

        # Prepare data for rendering
        context = {
            'book': book,
            'rental': rental,
            'membership_plan': student_profile.membership_plan,
            'can_rent': rental is None,  # Indicate if the book can be rented
            'book_content': book_content,
        }

        return render(request, 'rentals/rent_details.html', context)

    except Books.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('book_list_student')
    
def process_payment(request, order_type_name, related_id):
    amount = 0  # Initialize the 'amount' variable
    current_date = timezone.now()

    if request.method == "POST":
        # Get payment details from form
        payment_type = request.POST.get('payment_type')
        user = request.user
        
        # Determine the amount based on order type
        if order_type_name == "rental":
            book = get_object_or_404(Books, id=related_id)
            amount = book.rent  # Assuming `rent` is the field in Books
        elif order_type_name == "membership":
            plan = get_object_or_404(MembershipPlan, id=related_id)
            amount = plan.fee  # Assuming `fee` is the field in MembershipPlan

        # Dummy payment processing logic: assume payment is successful
        if payment_type not in ['upi', 'cc', 'net_banking']:
            messages.error(request, "Invalid payment type.")
            return redirect('book_list_student')  # Redirect to an appropriate page

        # Create payment entry in the database
        payment = Payment.objects.create(
            user_id=user,
            purchase_type=order_type_name,
            related_id=related_id,
            amount=amount,
            payment_type=payment_type,
        )
        payment.save()

        # After payment success, finalize the rental or membership
        if order_type_name == "rental":
            book = get_object_or_404(Books, id=related_id)
            student_profile = get_object_or_404(StudentProfile, user=user)
            rental = Rental.objects.create(student_profile=student_profile, book=book, is_rented=True)
            rental.due_date = timezone.now() + timedelta(days=student_profile.membership_plan.rent_duration)
            rental.save()
            # Redirect to the success page
            messages.success(request, "Payment successful!")
            return redirect('rented_books')  # Or redirect to the appropriate page
        
        elif order_type_name == "membership":
            plan = get_object_or_404(MembershipPlan, id=related_id)
            student_profile = get_object_or_404(StudentProfile, user=user)
            student_profile.membership_plan = plan
            student_profile.subscription_date = date.today()
            student_profile.expiry_date = date.today() + timedelta(days=plan.plan_duration * 30)
            student_profile.save()
            # Redirect to the success page
            messages.success(request, "Payment successful!")
            return redirect('view_membership_plans')  # Or redirect to the appropriate page

        # Redirect to the success page
        messages.success(request, "Payment successful!")
        return redirect('rented_books')  # Or redirect to the appropriate page

    # Handle GET request to render the payment form
    if order_type_name == "rental":
        book = get_object_or_404(Books, id=related_id)
        amount = book.rent  # Fetch the rental fee for the book
    elif order_type_name == "membership":
        plan = get_object_or_404(MembershipPlan, id=related_id)
        amount = plan.fee  # Fetch the fee for the selected membership plan

    return render(request, 'payment/payment_form.html', {
        'order_type_name': order_type_name,
        'related_id': related_id,
        'amount': amount,
        'current_date': current_date
    })

#PURCHASE PAYMENT
def process_payment_buy(request, order_type_name, related_id):
    current_date = timezone.now()

    if request.method == "POST":
        # Get form data
        payment_type = request.POST.get('payment_type')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        quantity = int(request.POST.get('quantity'))

        user = request.user
        book = get_object_or_404(Books, id=related_id)

        # Calculate total amount
        amount = book.price * quantity

        # Validate quantity availability
        if book.quantity < quantity:
            messages.error(request, "Insufficient stock available.")
            return redirect('book_list')

        # Dummy payment processing logic
        if payment_type not in ['upi', 'cc', 'net_banking']:
            messages.error(request, "Invalid payment type.")
            return redirect('book_list')

        # Create payment entry
        Payment.objects.create(
            user_id=user,
            purchase_type=order_type_name,
            related_id=related_id,
            amount=amount,
            payment_type=payment_type,
        )

        # Create purchase entry
        BookPurchase.objects.create(
            user=user,
            book=book,
            purchase_date=current_date,
            quantity=quantity,
            price=amount,
            address=address,
            pincode=pincode,
            phone=phone,
        )

        # Update stock
        book.quantity -= quantity
        book.save()

        messages.success(request, "Purchase successful!")
        return redirect('purchased_books')  # Replace with the appropriate success page

    # Render payment form for GET request
    book = get_object_or_404(Books, id=related_id)
    amount = book.price  # Single unit price for the book

    return render(request, 'payment/payment_form_buy.html', {
        'order_type_name': order_type_name,
        'related_id': related_id,
        'amount': amount,
        'current_date': current_date
    })


#PURCHASE BOOK
def purchase_book(request, book_id):
    try:
        # Get the book by ID
        book = get_object_or_404(Books, id=book_id)

        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')
        # Redirect to the payment processing view to handle payment before finalizing the purchase
        return redirect('process_payment_buy', order_type_name="purchase", related_id=book.id)

    except Exception as e:
        # Handle any unexpected errors
        messages.error(request, "An error occurred: " + str(e))
        return redirect('book_list_student')  # Redirect to the book list page

#PURCHASE DETAILS
def purchase_details(request, book_id):
    try:
        # Fetch the book details
        book = Books.objects.get(pk=book_id)

        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')

        # Fetch the book content (e.g., cover image) based on ISBN
        book_content = BookContent.objects.filter(id=book.ISBN_id).first()

        # Prepare data for rendering
        context = {
            'book': book,
            'book_content': book_content,
        }

        return render(request, 'purchase/purchase_details.html', context)

    except Books.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('book_list_student')

#to view purchased books
@login_required
def purchased_books(request):
    purchases = BookPurchase.objects.filter(user=request.user).select_related('book', 'book__author', 'book__genre')
    return render(request, 'purchase/purchased_books.html', {'purchases': purchases})

#DYNAMIC AUTHOR AND GENRE ADDING
def add_author_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_author_name = data.get('author_name')
            if new_author_name:
                author = Authors.objects.create(author_name=new_author_name)
                return JsonResponse({'success': True, 'author_id': author.id, 'author_name': author.name})
            return JsonResponse({'success': False, 'error': 'Author name is required'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
def add_genre_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_genre_name = data.get('genre_name')
            if new_genre_name:
                genre = Genres.objects.create(genre_name=new_genre_name)
                return JsonResponse({'success': True, 'genre_id': genre.id, 'genre_name': genre.name})
            return JsonResponse({'success': False, 'error': 'Genre name is required'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})

#ADMIN VIEW STUDENT LIST
def student_list(request):
    # Get the search query
    search_query = request.GET.get('searchname', '')

    # Filter students by username or first name (case-insensitive)
    students = StudentProfile.objects.filter(user__isnull=False)
    if search_query:
        students = students.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query)
        )

    context = {
        'students': students,
        'search_query': search_query,
    }
    return render(request, 'student_list.html', context)

#ADMIN RENTAL LIST
def admin_rental_list(request):
    # Get the search query and rental status filter from the request
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    # Start with all rentals
    rentals = Rental.objects.select_related('student_profile', 'book')

    # Apply search filter if search_query is provided
    if search_query:
        rentals = rentals.filter(
            Q(student_profile__user__first_name__icontains=search_query) |  # Search by student's first name
            Q(book__book_name__icontains=search_query)  # Search by book name
        )

    # Apply status filter if status_filter is provided
    if status_filter:
        if status_filter == 'rented':
            rentals = rentals.filter(is_rented=True)
        elif status_filter == 'returned':
            rentals = rentals.filter(is_rented=False)

    context = {
        'rentals': rentals,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, 'admin_rental_list.html', context)

def admin_purchase_list(request):
    # Get the search query from GET parameters
    search_query = request.GET.get('search', '')
    
    # Filter purchases based on search query (search by book name, user's first name, etc.)
    purchases = BookPurchase.objects.all()

    if search_query:
        purchases = purchases.filter(
            Q(book__book_name__icontains=search_query) |
            Q(user__first_name__icontains=search_query)
        )

    context = {
        'purchases': purchases,
        'search_query': search_query,
    }
    return render(request, 'purchase_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book_content = book.ISBN  # Accessing the related BookContent through the ISBN ForeignKey
    return render(request, 'book_detail.html', {'book': book, 'book_content': book_content})

def browse_books(request):
    search_query = request.GET.get('searchbook', '')
    selected_genre_id = request.GET.get('genre')
    selected_author_id = request.GET.get('author')

    # Start with all books
    books = Books.objects.all()

    # Filter by genre if selected
    if selected_genre_id:
        books = books.filter(genre__id=selected_genre_id)

    # Filter by author if selected
    if selected_author_id:
        books = books.filter(author__id=selected_author_id)

    # Optionally add the search query filter
    if search_query:
        books = books.filter(
            Q(book_name__icontains=search_query) |
            Q(author__author_name__icontains=search_query) |
            Q(genre__genre_name__icontains=search_query)
        )

    # Get the genres and authors for the filters
    genres = Genres.objects.all()
    authors = Authors.objects.all()

    # Get the selected genre and author objects to pass to the template
    selected_genre = Genres.objects.filter(id=selected_genre_id).first() if selected_genre_id else None
    selected_author = Authors.objects.filter(id=selected_author_id).first() if selected_author_id else None

    return render(request, 'browse_books.html', {
        'books': books,
        'genres': genres,
        'authors': authors,
        'selected_genre': selected_genre,
        'selected_author': selected_author,
        'search_query': search_query,
        'message': 'Results found' if books else 'No results found',
    })

def     read_book_interface(request, book_id):
    # Fetch the book object
    book = get_object_or_404(Books, id=book_id)

    # Ensure the book has content available
    if not book.ISBN or not book.ISBN.book_content:
        raise Http404("PDF content not available for this book.")

    # Context to render the reading interface
    context = {
        'pdf_url': book.ISBN.book_content.url,  # URL for the PDF file
        'book_name': book.book_name,  # Book name for additional context
    }
    return render(request, 'read_book.html', context)