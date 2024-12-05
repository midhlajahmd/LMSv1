from django.urls import path
from .views import user_login,librarian_dashboard,home_page,register,custom_logout

urlpatterns= [
    path('', home_page, name='home_page'),
    path('login/', user_login, name='login'),
    path('register/',register, name='signup' ),
    path('logout/', custom_logout, name="logout"),
    path('librarian-dashboard/', librarian_dashboard, name='librarian_dashboard'),
    
]