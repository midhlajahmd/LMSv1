from django.urls import path
from .views import user_login,librarian_dashboard,home_page,register

urlpatterns= [
    path('', home_page, name='home_page'),
    path('login/', user_login, name='login'),
    path('register/',register, name='signup' ),
    path('librarian-dashboard/', librarian_dashboard, name='librarian_dashboard'),
    
]