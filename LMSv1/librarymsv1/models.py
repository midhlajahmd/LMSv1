from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
#model for GENRES
class Genres(models.Model):
    genre_name= models.CharField(max_length=150, unique=True)

    #order by
    class Meta:
        ordering= ['genre_name']

    def __str__(self):
        return self.genre_name
    
#model for AUTHORS
class Authors(models.Model):
    author_name= models.CharField(max_length=150, unique=True)

    #order by
    class Meta:
        ordering= ['author_name']
    
    def __str__(self):
        return self.author_name

#model for BOOK CONTENTS
class BookContent(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    book_name= models.CharField(max_length=200, null=True)
    book_content = models.FileField(upload_to='book_contents/')  # PDF file upload path
    book_cover = models.ImageField(upload_to='book_covers/')     # Image upload path
    description = models.TextField(null=True, blank=True) 

    def __str__(self):
        return f'{self.isbn} - {self.book_name}'

#model for BOOKS
class Books(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    book_name= models.CharField(max_length=200)
    genre= models.ForeignKey(Genres, related_name='book_genre',on_delete=models.SET_NULL, null=True)
    author= models.ForeignKey(Authors, related_name='book_author',on_delete=models.SET_NULL, null=True)
    ISBN = models.ForeignKey(BookContent, related_name='book_isbn', on_delete=models.SET_NULL, null=True)  
    price= models.DecimalField(max_digits=8, decimal_places=2)
    rent_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    status= models.CharField(max_length=13, choices=STATUS_CHOICES, default='available')
    quantity = models.PositiveIntegerField(null= True)
    added_date = models.DateTimeField(default=timezone.now)
    hidden= models.BooleanField(default=False)
    featured= models.BooleanField(default=False)
    bestseller= models.BooleanField(default=False)
    noteworthy= models.BooleanField(default=False)
    writeplace= models.BooleanField(default=False)
    top20= models.BooleanField(default=False)
    recommend= models.BooleanField(default=False)
    
    #rent is automatically updated
    rent = models.DecimalField(max_digits=8, decimal_places=2, editable=False, null=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the rent as given by user
            # self.rent = self.price * (self.rent_percentage / 100)
            # super().save(*args, **kwargs)
        is_new = self.pk is None  # Check if this is a new book being added
        self.rent = self.price * (self.rent_percentage / 100)  # Calculate rent
        super().save(*args, **kwargs)
        
        # Send notifications if this is a new book
        if is_new:
            self.send_new_book_notifications()
    def send_new_book_notifications(self):
        message = f"New book '{self.book_name}' is available!"
        users = User.objects.all()  # Notify all users
        for user in users:
            Notification.objects.create(user=user, message=message)

    def __str__(self):
        return self.book_name

#model for MEMEBRSHIP PLANS
class MembershipPlan(models.Model):
    plan_name= models.CharField(max_length=100, unique=True)
    rent_limit= models.PositiveIntegerField()
    rent_duration= models.PositiveIntegerField()
    plan_duration= models.PositiveIntegerField()
    fee= models.DecimalField(max_digits=10, decimal_places=2)
    genres = models.ManyToManyField(Genres, related_name="membership_plans")

    def __str__(self):
        return self.plan_name
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True)
    membership_plan = models.ForeignKey(
        MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True
    )
    subscription_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    # Model for RENTALS
class Rental(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True)
    rental_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    is_rented = models.BooleanField(default=True)  # True means rented, False means returned

    def save(self, *args, **kwargs):
        if not self.due_date:
            # Calculate due date based on membership plan rental days
            if self.student_profile.membership_plan:
                self.due_date = self.rental_date + timezone.timedelta(days=self.student_profile.membership_plan.rent_duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.book_name} rented by {self.student_profile.user.username}"
    
#PAYMENT TABLE
class Payment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    purchase_type = models.CharField(max_length=100)
    related_id = models.IntegerField()  # ID of the corresponding record in rental, membership purchase, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=[('upi', 'UPI'), ('cc', 'Credit Card'), ('net_banking', 'Net Banking')])

    def __str__(self):
        return f"Payment for {self.purchase_type} - {self.related_id}"
    
#PURCHASE TABLE
class BookPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

#NOTIFICATIONS
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
#REVIEWS and RATINGS  
class comments(models.Model):
    book_comments=models.ForeignKey(Books,on_delete=models.CASCADE)
    comment_text=models.TextField()
    comment_published_datetime=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.comment_text
    
class Reviews(models.Model):
    stars=(
        (1,'one star'),
        (2,'two star'),
        (3,'three star'),
        (4,'four star'),
        (5,'five star')
    )
    post=models.ForeignKey(Books,related_name='review_of_book', on_delete=models.CASCADE)
    rating=models.PositiveSmallIntegerField(choices=stars,default=1)
    title=models.CharField(max_length=200)
    description =models.TextField(blank=True)
    review_author=models.ForeignKey(User,default=1 ,on_delete=models.CASCADE)

    def _str_(self):
        return self.title