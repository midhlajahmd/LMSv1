from django.db import models
from django.utils import timezone

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
    
    #rent is automatically updated
    rent = models.DecimalField(max_digits=8, decimal_places=2, editable=False, null=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the rent as given by user
        self.rent = self.price * (self.rent_percentage / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.book_name

#model for MEMEBRSHIP PLANS
class MembershipPlan(models.Model):
    plan_name= models.CharField(max_length=100, unique=True)
    rent_limit= models.PositiveIntegerField()
    rent_duration= models.PositiveIntegerField()
    plan_duration= models.PositiveIntegerField()
    fee= models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.plan_name