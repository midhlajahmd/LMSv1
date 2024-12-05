from django.contrib import admin
from .models import Genres,Authors,Books

# Register your models here.
admin.site.register(Genres)
admin.site.register(Authors)
admin.site.register(Books)