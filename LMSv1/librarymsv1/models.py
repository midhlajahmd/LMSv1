from django.db import models

# Create your models here.
#model for GENRES
class Genres(models.Model):
    genre_name= models.CharField(max_length=150)

    #order by
    class Meta:
        ordering= ['genre_name']

    def __str__(self):
        return self.genre
    
#model for AUTHORS
class Authors(models.Model):
    author_name= models.CharField(max_length=150)

    #order by
    class Meta:
        ordering= ['author_name']
    
    def __str__(self):
        return self.author
    
#model for BOOKS
class Books(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    book_name= models.CharField(max_length=200)
    genre= models.ForeignKey(Genres, related_name='book_genre',on_delete=models.SET_NULL, null=True)
    author= models.ForeignKey(Authors, related_name='book_author',on_delete=models.SET_NULL, null=True)
    ISBN= models.CharField(max_length=13, unique=True)  
    price= models.DecimalField(max_digits=8, decimal_places=2)
    rent= models.DecimalField(max_digits=8, decimal_places=2)
    status= models.CharField(max_length=13, choices=STATUS_CHOICES, default='available')

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