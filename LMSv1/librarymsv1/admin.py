from django.contrib import admin
from .models import Genres,Authors,Books,MembershipPlan,BookContent,StudentProfile
# Register your models here.
admin.site.register(Genres)
admin.site.register(Authors)
admin.site.register(Books)
admin.site.register(MembershipPlan)
admin.site.register(BookContent)
admin.site.register(StudentProfile)