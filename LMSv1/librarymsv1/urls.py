from django.urls import path
from django.contrib.auth.views import LoginView  

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='librarymsv1/login.html'), name='login'),
]
