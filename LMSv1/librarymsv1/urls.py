from django.urls import path
from .views import user_login,librarian_dashboard,home_page,register,custom_logout,book_list,book_add,book_edit,book_delete,author_list,add_author,edit_author,delete_author,genre_list,add_genre,edit_genre,delete_genre

urlpatterns= [
    path('', home_page, name='home_page'),
    path('login/', user_login, name='login'),
    path('register/',register, name='signup' ),
    path('logout/', custom_logout, name="logout"),
    path('librarian-dashboard/', librarian_dashboard, name='librarian_dashboard'),
    path('books/', book_list, name='book_list'),
    path('books/add/', book_add, name='book_add'),
    path('books/edit/<int:pk>/', book_edit, name='book_edit'),
    path('books/delete/<int:pk>/', book_delete, name='book_delete'),
    path('authors/', author_list, name='author_list'),
    path('authors/add/', add_author, name='add_author'),
    path('authors/edit/<int:pk>/', edit_author, name='edit_author'),
    path('authors/delete/<int:pk>/', delete_author, name='delete_author'),
    path('genres/', genre_list, name='genre_list'),
    path('genres/add/', add_genre, name='add_genre'),
    path('genres/edit/<int:pk>/', edit_genre, name='edit_genre'),
    path('genres/delete/<int:pk>/', delete_genre, name='delete_genre'),
    
]
