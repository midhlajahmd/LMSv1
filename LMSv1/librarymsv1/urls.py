from django.urls import path
from .views import user_login,librarian_dashboard,home_page,register,custom_logout,book_list,book_add,book_edit,book_delete
from .views import author_list,add_author,edit_author,delete_author,genre_list,add_genre,edit_genre,delete_genre
from .views import add_or_edit_plan,manage_membership_plans,view_membership_plans,subscribe_to_plan,upgrade_plan,student_profile,plan_details
from .views import book_list_student,rent_book,return_book,rented_books,rent_details,process_payment,purchase_details,purchase_book,process_payment_buy
from .views import purchased_books,add_author_book,add_genre_book,student_list,admin_rental_list,admin_purchase_list
from .views import browse_books,read_book_interface,mark_notifications_as_read,book_view,get_book_name

urlpatterns= [
    # path('', home_page, name='home_page'),
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

    path('membership-plans/manage', manage_membership_plans, name='manage_membership_plans'),
    path('membership-plans/add/', add_or_edit_plan, name='add_plan'),
    path('membership-plans/edit/<int:pk>/', add_or_edit_plan, name='edit_plan'),

    path('plan/<int:plan_id>/', plan_details, name='plan_details'),
    path('subscribe/<int:plan_id>/', subscribe_to_plan, name='subscribe_to_plan'),
    path('membership-plans/view', view_membership_plans, name='view_membership_plans'),
    path('upgrade/<int:plan_id>/', upgrade_plan, name='upgrade_plan'),

    path('student/',student_profile, name='student_profile'),
    
    path('', book_list_student, name='book_list_student'),

    path('rentals/rent/<int:book_id>/', rent_details, name='rent_details'),
    path('rent/<int:book_id>/', rent_book, name='rent_book'),
    path('return/<int:rental_id>/', return_book, name='return_book'),
    path('rented/', rented_books, name='rented_books'),

    path('process_payment/<str:order_type_name>/<int:related_id>/', process_payment, name='process_payment'),
    path('process_payment_buy/<str:order_type_name>/<int:related_id>/', process_payment_buy, name='process_payment_buy'),

    path('purchase/purchase/<int:book_id>/', purchase_details, name='purchase_details'),
    path('purchase/purchasebook/<int:book_id>/', purchase_book, name='purchase_book'),
    path('purchase/purchased_books/', purchased_books, name='purchased_books'),

    path('add-author/', add_author_book, name='add_author_book'),
    path('add-genre/', add_genre_book, name='add_genre_book'),

    path('librarian-dashboard/students-list/', student_list, name='student_list'),
    path('librarian-dashboard/rented-books-list/', admin_rental_list, name='admin_rental_list'),
    path('librarian-dashboard/purchased-book-list/', admin_purchase_list, name='admin_purchase_list'),
    
    # path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book/<int:pk>/', book_view, name='book_detail'),
    path('browse/', browse_books, name='browse_books'),

    path('read/<int:book_id>/', read_book_interface, name='read_book_interface'),
    path('mark-notifications-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),

    path('get-book-name/<int:isbn_id>/', get_book_name, name='get_book_name'),
    
]
